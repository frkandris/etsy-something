#!/usr/bin/env python3
"""Run a validated profile recipe and publish only a complete product directory."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

from exportlib import output_directory

ROOT = Path(__file__).resolve().parents[2]
PIPE = ROOT / 'product' / 'pipeline'
SCRIPTS = {'02_trace.py', '10_worldmap.py', '11_worldmap_flat.py'}
VIEWS = {'hero', 'angled', 'shelf', 'plate', 'styled', 'exploded', 'wall', 'macro', 'lifestyle'}


def load_profile(name):
    """Resolve a file, catalog family, or generic profile before doing any work."""
    path = Path(name)
    if not path.is_file():
        family = ROOT / 'product' / 'catalog' / name
        catalog = family / 'product.json'
        if catalog.is_file():
            product = json.loads(catalog.read_text())
            if not isinstance(product, dict):
                raise ValueError(f'Invalid catalog family: {name}')
            if latest := product.get('latest_run'):
                path = family / latest / 'profile.json'
            elif fallback := product.get('profile'):
                path = ROOT / 'product' / 'profiles' / f'{fallback}.json'
            else:
                raise ValueError(f'Catalog family {name} has no runnable recipe')
        else:
            path = ROOT / 'product' / 'profiles' / f'{name}.json'
    if not path.is_file():
        raise ValueError(f'Profile not found: {name} ({path})')
    profile = json.loads(path.read_text())
    if not isinstance(profile, dict) or not isinstance(profile.get('pipeline'), dict):
        raise ValueError('Profile must contain a pipeline object')
    recipe = profile['pipeline']
    if recipe.get('script') not in SCRIPTS:
        raise ValueError('Invalid pipeline script')
    args = recipe.get('args')
    if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
        raise ValueError('pipeline.args must be a list of strings')
    # The runner owns transaction paths and release mode, not the recipe.
    if any(arg.startswith('--') and any(key.startswith(arg.split('=', 1)[0])
           for key in ('--out', '--src', '--draft')) for arg in args):
        raise ValueError('Recipe cannot override --out, --src, --draft or use --')
    if not isinstance(profile.get('render', {}), dict):
        raise ValueError('render must be an object')
    validate_views(profile.get('views'))
    return path.resolve(), profile


def palette_inputs(profile):
    """The supported recipes' additional file inputs, including renderer overrides."""
    inputs = []
    args = profile['pipeline']['args']
    for i, arg in enumerate(args):
        if arg == '--palette':
            if i + 1 == len(args) or args[i + 1].startswith('--'):
                raise ValueError('--palette requires a file')
            inputs.append((i + 1, ROOT / args[i + 1], False))
        elif arg.startswith('--palette='):
            inputs.append((i, ROOT / arg.split('=', 1)[1], True))
    if palette := profile.get('render', {}).get('palette_file'):
        inputs.append((None, ROOT / palette, False))
    for _, path, _ in inputs:
        if not path.is_file():
            raise ValueError(f'Palette file not found: {path}')
    return inputs


def validate_views(views):
    if not isinstance(views, list) or not views or any(not isinstance(view, str) or view not in VIEWS for view in views):
        raise ValueError(f'views must be a nonempty list drawn from {sorted(VIEWS)}')
    if len(set(views)) != len(views):
        raise ValueError('Duplicate render views')
    return views


def validate_report(report, draft):
    """A truthy string or an inconsistent report cannot approve a release."""
    if not isinstance(report, dict):
        raise ValueError('Pipeline report must be an object')
    for key in ('all_ok', 'draft', 'release_ready'):
        if type(report.get(key)) is not bool:
            raise ValueError(f'Pipeline report requires boolean {key}')
    expected_release = report['all_ok'] and not draft
    if report['draft'] != draft or report['release_ready'] != expected_release:
        raise ValueError('Pipeline report has inconsistent release status')
    if not draft and not report['release_ready']:
        raise ValueError('Pipeline did not produce a validated release')


def run_product(options, profile, views):
    """Keep external processes at the boundary; publish after every stage succeeds."""
    with output_directory(options.out) as out:
        profile = copy.deepcopy(profile)
        input_hashes = {}
        for index, path, joined in palette_inputs(profile):
            target = out / 'inputs' / 'palettes' / f'{index if index is not None else "render"}.json'
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            input_hashes[str(target.relative_to(out))] = hashlib.sha256(target.read_bytes()).hexdigest()
            if index is None:
                profile['render']['palette_file'] = str(target)
            else:
                profile['pipeline']['args'][index] = ('--palette=' if joined else '') + str(target)
        snapshot = out / 'profile.json'
        snapshot.write_text(json.dumps(profile, indent=2, ensure_ascii=False))
        cmd = [sys.executable, str(PIPE / profile['pipeline']['script']),
               *profile['pipeline']['args'], '--out', str(out / 'layers')]
        source_hash = None
        if options.src:
            # Hash the exact bytes supplied to the generator, even if the original
            # illustration is edited while Blender is running.
            inputs = out / 'inputs' / 'source'
            inputs.mkdir(parents=True)
            source = inputs / options.src.name
            shutil.copyfile(options.src, source)
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            input_hashes[str(source.relative_to(out))] = source_hash
            cmd += ['--src', str(source)]
        if options.levels is not None:
            cmd += ['--levels', str(options.levels)]
        if options.draft:
            cmd += ['--draft']
        subprocess.run(cmd, check=True, cwd=ROOT)
        report = json.loads((out / 'layers' / 'report.json').read_text())
        validate_report(report, options.draft)
        if not list((out / 'layers').glob('layer_*_of_*.svg')):
            raise ValueError('Pipeline produced no layer SVG files')
        palette_args = []
        if (out / 'layers' / 'palette.json').is_file() and not profile.get('render', {}).get('palette_file'):
            palette_args = ['--palette-file', str(out / 'layers' / 'palette.json')]
        render_commands = []
        if not options.no_render:
            for view in views:
                image = out / f'{view}.png'
                render_cmd = ['blender', '-b', '--python-exit-code', '1', '-P',
                                str(ROOT / 'product/render_blender.py'), '--',
                                str(out / 'layers'), str(image), view,
                                '--profile', str(snapshot), *palette_args]
                subprocess.run(render_cmd, check=True, cwd=ROOT)
                render_commands.append(render_cmd)
                if not image.is_file() or image.stat().st_size == 0:
                    raise ValueError(f'Render missing or empty: {view}')
        def published(value):
            return value.replace(str(out), str(options.out.resolve()))

        profile['pipeline']['args'] = [published(arg) for arg in profile['pipeline']['args']]
        if profile.get('render', {}).get('palette_file'):
            profile['render']['palette_file'] = published(profile['render']['palette_file'])
        snapshot.write_text(json.dumps(profile, indent=2, ensure_ascii=False))
        manifest = {'profile': profile, 'source': str(options.src) if options.src else None,
                    'source_sha256': source_hash,
                    'input_sha256': input_hashes,
                    'command': [published(arg) for arg in cmd],
                    'render_commands': [[published(arg) for arg in command] for command in render_commands],
                    'views': [] if options.no_render else views,
                    'release_ready': report['release_ready']}
        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    ap.add_argument('--profile', required=True)
    ap.add_argument('--src', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--views', help='Comma-separated views; default: profile views')
    ap.add_argument('--no-render', action='store_true')
    ap.add_argument('--draft', action='store_true')
    ap.add_argument('--levels', type=int, help='Explicit recipe override')
    a = ap.parse_args()
    try:
        profile_path, profile = load_profile(a.profile)
        views = validate_views(a.views.split(',') if a.views is not None else profile['views'])
        palettes = palette_inputs(profile)
    except (OSError, ValueError, TypeError) as exc:
        ap.error(str(exc))
    script = profile['pipeline']['script']
    if profile.get('validation_status') == 'experimental':
        print('Experimental profile: no validated full run; geometry validation may stop export.', file=sys.stderr)
    if script == '02_trace.py' and (not a.src or not a.src.is_file()):
        ap.error('--src must name an existing source image')
    if a.src and script != '02_trace.py':
        ap.error('--src is only supported by the image tracing pipeline')
    if a.levels is not None and (script != '02_trace.py' or a.levels < 2):
        ap.error('--levels must be at least 2 and is only supported by the image tracing pipeline')
    if profile_path.is_relative_to(a.out.resolve()) or (a.src and a.src.resolve().is_relative_to(a.out.resolve())):
        ap.error('--out must not contain the source image or the input profile')
    if any(path.resolve().is_relative_to(a.out.resolve()) for _, path, _ in palettes):
        ap.error('--out must not contain an input palette')
    if not a.no_render and not shutil.which('blender'):
        ap.error('Blender is missing from PATH')
    if script == '02_trace.py' and not shutil.which('potrace'):
        ap.error('potrace is missing from PATH')
    run_product(a, profile, views)
    print(f'Complete: {a.out}')


if __name__ == '__main__':
    main()
