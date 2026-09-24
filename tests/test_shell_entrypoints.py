"""Regression checks for the shell files that dispatch the product pipeline."""
from pathlib import Path
import json
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('broken', [False, True])
@pytest.mark.parametrize('name', ['product/pipeline/run_theme.sh', 'new command.sh',
                                  'product/pipeline/new tool/run.sh', 'tests/helpers/check.sh'])
def test_check_script_discovers_shell_files(tmp_path, broken, name):
    shutil.copyfile(ROOT / 'check.sh', tmp_path / 'check.sh')
    py = tmp_path / '.venv/bin/python'
    py.parent.mkdir(parents=True)
    py.write_text('#!/bin/sh\nexit 0\n')
    py.chmod(0o755)
    existing = tmp_path / 'product/pipeline/run_theme.sh'
    existing.parent.mkdir(parents=True)
    existing.write_text('#!/bin/bash\nexit 0\n')
    shell = tmp_path / name
    shell.parent.mkdir(parents=True, exist_ok=True)
    shell.write_text('if [[ -n x ]; then\n' if broken else '#!/bin/bash\nexit 0\n')
    result = subprocess.run(['bash', str(tmp_path / 'check.sh')], capture_output=True, text=True)
    assert (result.returncode != 0) == broken
    assert ('== rendben ==' in result.stdout) != broken


def test_theme_wrapper_preserves_explicit_source_profile_and_spaces(tmp_path):
    root = tmp_path / 'repo'
    script = root / 'product/pipeline/run_theme.sh'
    script.parent.mkdir(parents=True)
    shutil.copyfile(ROOT / 'product/pipeline/run_theme.sh', script)
    capture = tmp_path / 'args.json'
    py = root / '.venv/bin/python'
    py.parent.mkdir(parents=True)
    py.write_text(f'#!{sys.executable}\nimport json,sys\n'
                  f'open({str(capture)!r},"w").write(json.dumps(sys.argv[1:]))\n')
    py.chmod(0o755)
    caller = tmp_path / 'caller'
    caller.mkdir()
    subprocess.run(['bash', str(script), 'german-shepherd', 'chosen source.png',
                    'magicvector-shepherd', '8'], cwd=caller, check=True)
    args = json.loads(capture.read_text())
    assert args[args.index('--src') + 1] == 'chosen source.png'
    assert args[args.index('--profile') + 1] == 'magicvector-shepherd'
    assert args[args.index('--levels') + 1] == '8'
    assert args[args.index('--out') + 1] == str(root / 'product/themes/german-shepherd/current')


def test_check_stops_when_shell_discovery_fails(tmp_path, monkeypatch):
    import os
    shutil.copyfile(ROOT / 'check.sh', tmp_path / 'check.sh')
    py = tmp_path / '.venv/bin/python'
    py.parent.mkdir(parents=True)
    py.write_text('#!/bin/sh\nexit 0\n')
    py.chmod(0o755)
    (tmp_path / 'product/pipeline').mkdir(parents=True)
    commands = tmp_path / 'commands'
    commands.mkdir()
    find = commands / 'find'
    find.write_text('#!/bin/sh\necho "simulated discovery failure" >&2\nexit 7\n')
    find.chmod(0o755)
    monkeypatch.setenv('PATH', str(commands) + os.pathsep + os.environ['PATH'])
    result = subprocess.run(['bash', str(tmp_path / 'check.sh')], capture_output=True, text=True)
    assert result.returncode == 7
    assert 'simulated discovery failure' in result.stderr
    assert '== pytest ==' not in result.stdout
    assert '== rendben ==' not in result.stdout
