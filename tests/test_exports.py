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


@pytest.mark.parametrize('unsafe', ['directory_symlink', 'public_directory', 'file_symlink', 'hardlink', 'fifo', 'public_file'])
def test_unsafe_lock_paths_are_rejected_before_generation(tmp_path, monkeypatch, unsafe):
    import hashlib
    import os
    import exportlib

    monkeypatch.setattr(exportlib.tempfile, 'gettempdir', lambda: str(tmp_path))
    lock_dir = tmp_path / f'etsy-export-locks-{os.getuid()}'
    destination = tmp_path / 'product'
    destination.mkdir()
    (destination / 'old.svg').write_text('previous output')
    victim = tmp_path / 'unrelated'
    victim.write_text('unchanged')
    if unsafe == 'directory_symlink':
        other = tmp_path / 'other'
        other.mkdir(mode=0o700)
        lock_dir.symlink_to(other, target_is_directory=True)
    else:
        lock_dir.mkdir(mode=0o700)
        lock_name = hashlib.sha256(str(destination.resolve()).encode()).hexdigest() + '.lock'
        lock = lock_dir / lock_name
        if unsafe == 'public_directory':
            lock_dir.chmod(0o777)
        elif unsafe == 'file_symlink':
            lock.symlink_to(victim)
        elif unsafe == 'hardlink':
            os.link(victim, lock)
        elif unsafe == 'public_file':
            lock.write_text('')
            lock.chmod(0o666)
        else:
            os.mkfifo(lock, mode=0o600)
    # A broken implementation may block opening a FIFO. Bound the real process
    # so that this regression fails instead of hanging the test suite.
    import subprocess
    code = ('import tempfile\n'
            f'tempfile.tempdir = {str(tmp_path)!r}\n'
            'from exportlib import output_directory\n'
            f'with output_directory({str(destination)!r}):\n'
            '    raise SystemExit(42)\n')
    result = subprocess.run([sys.executable, '-c', code],
                            cwd=pathlib.Path(__file__).resolve().parents[1] / 'product/pipeline',
                            capture_output=True, text=True, timeout=5)
    assert result.returncode == 1, result.stderr
    if unsafe in ('directory_symlink', 'file_symlink'):
        import errno
        assert any(f'[Errno {code}]' in result.stderr for code in (errno.ELOOP, errno.ENOTDIR))
    else:
        assert 'PermissionError:' in result.stderr
        expected = 'must be private' if unsafe == 'public_directory' else 'Unsafe export lock file'
        assert expected in result.stderr
    assert (destination / 'old.svg').read_text() == 'previous output'
    assert victim.read_text() == 'unchanged'
    assert not list(tmp_path.glob('.product.staging-*'))


def test_private_directory_accepts_legacy_readable_lock_file(tmp_path, monkeypatch):
    import hashlib
    import os
    import exportlib

    monkeypatch.setattr(exportlib.tempfile, 'gettempdir', lambda: str(tmp_path))
    destination = tmp_path / 'product'
    lock_dir = tmp_path / f'etsy-export-locks-{os.getuid()}'
    lock_dir.mkdir(mode=0o700)
    name = hashlib.sha256(str(destination.resolve()).encode()).hexdigest() + '.lock'
    lock = lock_dir / name
    lock.write_text('')
    lock.chmod(0o644)  # previous release used open("a") and the process umask
    with output_directory(destination) as stage:
        (stage / 'result.svg').write_text('complete')
    assert (destination / 'result.svg').read_text() == 'complete'
