"""Regression checks for the shell files that dispatch the product pipeline."""
from pathlib import Path
import json
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


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
