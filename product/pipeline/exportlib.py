"""Staged, recoverable directory exports shared by the product pipelines."""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile


def require_valid(report, draft=False):
    """Drafts are explicit; failed validation must never look like a release."""
    report["draft"] = bool(draft)
    report["release_ready"] = (report.get("all_ok") is True) and not draft
    if report.get("all_ok") is not True and not draft:
        raise ValueError("Hibás vágásgeometria; export megszakítva. Részletek: "
                         + json.dumps(report, ensure_ascii=False))


@contextmanager
def _destination_lock(destination):
    """Hold a private regular-file lock, refusing redirected or shared paths.

    Keep lock inodes between runs: unlinking a live lock could let two writers
    lock different inodes. Temp-directory cleanup is safe only with no exports
    running. The directory descriptor pins the checked parent for file opening.
    """
    lock_dir = Path(tempfile.gettempdir()) / f"etsy-export-locks-{os.getuid()}"
    lock_dir.mkdir(mode=0o700, exist_ok=True)
    directory_fd = os.open(lock_dir, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        info = os.fstat(directory_fd)
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
            raise PermissionError(f"Export lock directory must be private and owned by this user: {lock_dir}")
        name = hashlib.sha256(str(destination).encode()).hexdigest() + ".lock"
        # NONBLOCK prevents a substituted FIFO from hanging before type checks.
        fd = os.open(name, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK,
                     0o600, dir_fd=directory_fd)
        try:
            info = os.fstat(fd)
            if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                    or info.st_nlink != 1 or stat.S_IMODE(info.st_mode) & 0o022):
                raise PermissionError(f"Unsafe export lock file: {lock_dir / name}")
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise BlockingIOError(f"Another export is running for {destination}") from exc
            yield
        finally:
            os.close(fd)
    finally:
        os.close(directory_fd)


@contextmanager
def output_directory(destination):
    """Keep old output until completion; recover an interrupted rename on retry.

    Directory replacement has a brief rename gap, so this is recoverable, not
    an atomic reader snapshot. A per-destination lock prevents concurrent writers.
    """
    destination = Path(destination).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    backup = destination.with_name(destination.name + ".previous")
    with _destination_lock(destination):
        if backup.exists():
            if not destination.exists():
                backup.rename(destination)
            else:
                shutil.rmtree(backup)
        stage = Path(tempfile.mkdtemp(prefix=f".{destination.name}.staging-",
                                      dir=destination.parent))
        try:
            yield stage
            if destination.exists():
                destination.rename(backup)
            try:
                os.replace(stage, destination)
            except BaseException:
                if backup.exists() and not destination.exists():
                    backup.rename(destination)
                raise
            if backup.exists():
                shutil.rmtree(backup)
        finally:
            if stage.exists():
                shutil.rmtree(stage)
