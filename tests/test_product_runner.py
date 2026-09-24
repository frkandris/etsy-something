"""The transactional output replacement must never consume its own inputs."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('inside', ['source', 'profile', 'palette', 'render_palette'])
def test_runner_rejects_output_containing_an_input(tmp_path, inside):
    out = tmp_path / 'product'
    out.mkdir()
    source = (out if inside == 'source' else tmp_path) / 'source.png'
    source.write_bytes(b'preserve this source')
    profile = (out if inside == 'profile' else tmp_path) / 'profile.json'
    args, render = [], {}
    if inside in ('palette', 'render_palette'):
        palette = out / 'palette.json'
        palette.write_text('[[10,20,30]]')
        if inside == 'palette':
            args = ['--palette', str(palette)]
        else:
            render = {'palette_file': str(palette)}
    profile.write_text(json.dumps({'pipeline': {'script': '02_trace.py', 'args': args},
                                   'render': render, 'views': ['plate']}))
    result = subprocess.run([sys.executable, str(ROOT / 'product/pipeline/run_product.py'),
                             '--src', str(source), '--profile', str(profile),
                             '--out', str(out), '--no-render'], capture_output=True, text=True)
    assert result.returncode == 2
    assert 'must not contain' in result.stderr
    assert source.read_bytes() == b'preserve this source'
    assert profile.is_file()

# Stub only the external process boundary: exercise real staging, validation,
# publication and manifest writing without launching Blender in the fast suite.
sys.path.insert(0, str(ROOT / 'product/pipeline'))
import run_product as runner  # noqa: E402
from argparse import Namespace  # noqa: E402
import hashlib  # noqa: E402


@pytest.fixture
def recipe():
    return {'pipeline': {'script': '02_trace.py', 'args': []}, 'render': {}, 'views': ['plate']}


@pytest.mark.parametrize('views', [[], ['typo'], ['../outside'], ['plate', 'plate'], 'plate'])
def test_unknown_or_unsafe_views_are_rejected(views):
    with pytest.raises(ValueError):
        runner.validate_views(views)


@pytest.mark.parametrize('change', [
    {'script': 'run_product.py'}, {'args': '--levels 6'}, {'args': [6]},
    {'args': ['--out=/tmp/escape']}, {'args': ['--draft']}, {'args': ['--src', 'other.png']},
])
def test_profile_rejects_invalid_or_runner_owned_arguments(tmp_path, recipe, change):
    recipe['pipeline'].update(change)
    path = tmp_path / 'profile.json'
    path.write_text(json.dumps(recipe))
    with pytest.raises(ValueError):
        runner.load_profile(str(path))


@pytest.mark.parametrize('report', [
    {}, {'all_ok': True, 'draft': False, 'release_ready': 'false'},
    {'all_ok': False, 'draft': False, 'release_ready': True},
    {'all_ok': True, 'draft': True, 'release_ready': True},
])
def test_inconsistent_reports_cannot_approve_a_release(report):
    with pytest.raises(ValueError):
        runner.validate_report(report, draft=False)


@pytest.mark.parametrize('failure', ['generator', 'report', 'missing_svg', 'renderer', 'missing_png', 'empty_png', None])
def test_whole_product_transaction_preserves_old_output_on_failure(tmp_path, monkeypatch, recipe, failure):
    dest = tmp_path / 'output'
    dest.mkdir()
    (dest / 'old.svg').write_text('previous release')
    source = tmp_path / 'source.png'
    source.write_bytes(b'original source bytes')
    options = Namespace(out=dest, src=source, levels=None, draft=False, no_render=False)
    calls = []

    def process(cmd, **kwargs):
        assert kwargs['check'] is True
        calls.append(cmd)
        if cmd[0] != 'blender':
            if failure == 'generator':
                raise subprocess.CalledProcessError(1, cmd)
            supplied = Path(cmd[cmd.index('--src') + 1])
            assert supplied.read_bytes() == b'original source bytes'
            source.write_bytes(b'edited while running')
            layers = Path(cmd[cmd.index('--out') + 1])
            layers.mkdir()
            (layers / 'report.json').write_text(json.dumps({
                'all_ok': failure != 'report', 'draft': False, 'release_ready': failure != 'report'}))
            if failure != 'missing_svg':
                (layers / 'layer_1_of_1.svg').write_text('<svg/>')
        else:
            if failure == 'renderer':
                raise subprocess.CalledProcessError(1, cmd)
            assert cmd[cmd.index('--python-exit-code') + 1] == '1'
            if failure != 'missing_png':
                image = Path(cmd[cmd.index('--') + 2])
                image.write_bytes(b'' if failure == 'empty_png' else b'rendered image')

    monkeypatch.setattr(runner.subprocess, 'run', process)
    if failure:
        with pytest.raises((ValueError, subprocess.CalledProcessError)):
            runner.run_product(options, recipe, ['plate'])
        assert (dest / 'old.svg').read_text() == 'previous release'
        assert not (dest / 'manifest.json').exists()
        if failure in ('generator', 'report', 'missing_svg'):
            assert len(calls) == 1
    else:
        runner.run_product(options, recipe, ['plate'])
        manifest = json.loads((dest / 'manifest.json').read_text())
        assert manifest['release_ready'] is True
        assert manifest['source_sha256'] == hashlib.sha256(b'original source bytes').hexdigest()
        assert (dest / 'inputs/source/source.png').read_bytes() == b'original source bytes'
        assert not (dest / 'old.svg').exists()
        assert (dest / 'plate.png').read_bytes() == b'rendered image'
    assert not list(tmp_path.glob('.output.staging-*'))


def test_palette_snapshots_survive_original_changes_and_deletion(tmp_path, monkeypatch, recipe):
    palette = tmp_path / 'palette.json'
    palette.write_text('[[10,20,30]]')
    recipe['pipeline']['args'] = ['--palette', str(palette)]
    recipe['render']['palette_file'] = str(palette)
    options = Namespace(out=tmp_path / 'out', src=None, levels=None, draft=False, no_render=False)

    def process(cmd, **_):
        if cmd[0] != 'blender':
            assert Path(cmd[cmd.index('--palette') + 1]).read_text() == '[[10,20,30]]'
            palette.write_text('[[200,200,200]]')
            layers = Path(cmd[cmd.index('--out') + 1])
            layers.mkdir()
            (layers / 'layer_1_of_1.svg').write_text('<svg/>')
            (layers / 'report.json').write_text(json.dumps({'all_ok': True, 'draft': False, 'release_ready': True}))
        else:
            p = json.loads(Path(cmd[cmd.index('--profile') + 1]).read_text())
            assert Path(p['render']['palette_file']).read_text() == '[[10,20,30]]'
            Path(cmd[cmd.index('--') + 2]).write_bytes(b'png')

    monkeypatch.setattr(runner.subprocess, 'run', process)
    runner.run_product(options, recipe, ['plate'])
    palette.unlink()
    _, saved = runner.load_profile(str(options.out / 'profile.json'))
    assert all(p.read_text() == '[[10,20,30]]' for _, p, _ in runner.palette_inputs(saved))
    manifest = json.loads((options.out / 'manifest.json').read_text())
    assert len(manifest['input_sha256']) == 2
    assert len(manifest['render_commands']) == 1
    assert all((options.out / p).is_file() for p in manifest['input_sha256'])


def test_catalog_family_without_run_uses_declared_profile():
    _, profile = runner.load_profile('vyva-worldmap')
    assert profile['pipeline']['script'] == '10_worldmap.py'
    with pytest.raises(ValueError, match='no runnable recipe'):
        runner.load_profile('early-concepts')
