"""Staged, recoverable directory exports shared by the product pipelines."""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
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
    """One writer per destination. The lock file is left in place on purpose:
    deleting a held lock would let a second writer lock a fresh inode."""
    digest = hashlib.sha256(str(destination).encode()).hexdigest()[:16]
    lock = Path(tempfile.gettempdir()) / f"etsy-export-{os.getuid()}-{digest}.lock"
    with open(lock, "a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise BlockingIOError(f"Another export is running for {destination}") from exc
        yield


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
