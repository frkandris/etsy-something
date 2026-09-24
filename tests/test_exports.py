"""The old deliverable must survive failed generation and interrupted commits."""
import pathlib
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'product' / 'pipeline'))
from exportlib import output_directory, require_valid  # noqa: E402


def test_bad_report_does_not_publish_or_destroy_old_files(tmp_path):
    dest = tmp_path / 'layers'
    dest.mkdir()
    (dest / 'old.svg').write_text('old')
    with pytest.raises(ValueError):
        with output_directory(dest) as stage:
            (stage / 'new.svg').write_text('new')
            require_valid({'all_ok': False})
    assert (dest / 'old.svg').read_text() == 'old'
    assert not (dest / 'new.svg').exists()


def test_success_replaces_whole_set_without_stale_layers(tmp_path):
    dest = tmp_path / 'layers'
    dest.mkdir()
    (dest / 'old.svg').write_text('old')
    with output_directory(dest) as stage:
        (stage / 'new.svg').write_text('new')
        require_valid({'all_ok': True})
    assert sorted(p.name for p in dest.iterdir()) == ['new.svg']


def test_commit_failure_restores_previous_output(tmp_path):
    dest = tmp_path / 'layers'
    dest.mkdir()
    (dest / 'old.svg').write_text('old')
    with patch('exportlib.os.replace', side_effect=OSError('disk error')):
        with pytest.raises(OSError):
            with output_directory(dest) as stage:
                (stage / 'new.svg').write_text('new')
    assert (dest / 'old.svg').read_text() == 'old'


def test_interrupted_rename_recovers_before_next_failed_run(tmp_path):
    dest = tmp_path / 'layers'
    previous = tmp_path / 'layers.previous'
    previous.mkdir()
    (previous / 'old.svg').write_text('old')
    with pytest.raises(RuntimeError):
        with output_directory(dest):
            assert (dest / 'old.svg').read_text() == 'old'
            raise RuntimeError('failed generation')
    assert (dest / 'old.svg').exists()


def test_draft_is_never_release_ready():
    report = {'all_ok': False}
    require_valid(report, draft=True)
    assert report['draft'] and not report['release_ready']


def test_another_process_cannot_enter_the_same_export(tmp_path):
    import subprocess
    destination = tmp_path / 'product'
    with output_directory(destination) as stage:
        (stage / 'new.svg').write_text('complete')
        code = ('from exportlib import output_directory\n'
                f'with output_directory({str(destination)!r}):\n'
                '    raise AssertionError("lock did not exclude the second writer")\n')
        result = subprocess.run([sys.executable, '-c', code],
                                cwd=pathlib.Path(__file__).resolve().parents[1] / 'product/pipeline',
                                capture_output=True, text=True, timeout=5)
        assert result.returncode == 1
        assert 'Another export is running' in result.stderr
    assert (destination / 'new.svg').read_text() == 'complete'
    assert sorted(p.name for p in tmp_path.iterdir()) == ['product']
