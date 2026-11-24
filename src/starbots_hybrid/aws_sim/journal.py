"""Installation-local OS lock and hash-chained simulation journal."""
from contextlib import contextmanager
import json
import os
from pathlib import Path

from ..io import ValidationError, digest, fail, json_bytes, parse_json, read_bytes, write_bytes


def canonical_state_dir():
    # Tied to the resolved checkout/venv, never TEMP/TMP or caller input.
    source = Path(__file__).resolve()
    if source.parents[2].name == 'src':
        anchor = source.parents[3]
    elif source.parents[2].name == 'site-packages':
        anchor = source.parents[4]
    else:
        fail('PATH_DENIED', 'Unsupported simulation installation layout')
    return anchor / '.local-evidence' / 'aws-sim-state'


def _state_root(value):
    root = canonical_state_dir()
    if value is not None and Path(value).resolve() != root:
        fail('PATH_DENIED', 'Simulation state root is fixed for this installation')
    if (root.parent.is_symlink() or root.is_symlink() or
            (root.exists() and not root.is_dir())):
        fail('PATH_DENIED', 'Invalid simulation state directory')
    root.mkdir(parents=True, exist_ok=True)
    return root


@contextmanager
def locked_journal(state_dir, account_id, region, approval_id):
    root = _state_root(state_dir)
    scope = digest((account_id + ':' + region).encode('ascii'))[:24]
    lock_path = root / (scope + '.lock')
    with lock_path.open('a+b') as handle:
        if lock_path.stat().st_size == 0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            fail('LOCK_BUSY', 'Another simulation holds the account and region lock')
        try:
            approval_scope = digest(approval_id.encode('ascii'))[:24]
            yield Journal(root / (scope + '-' + approval_scope + '.jsonl'))
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class Journal:
    def __init__(self, path):
        self.path = path
        self.entries = []
        previous = '0' * 64
        if path.exists():
            for raw in path.read_bytes().splitlines():
                entry = parse_json(raw)
                if (set(entry) != {'previous','event','hash'} or entry['previous'] != previous
                        or entry['hash'] != digest(json_bytes({'previous':previous,'event':entry['event']}))):
                    fail('JOURNAL_TAMPERED', 'Simulation journal integrity failed')
                evidence_ref = entry['event'].get('evidence_ref')
                if evidence_ref is not None:
                    try:
                        if digest(read_bytes(path.parent,evidence_ref['path'])) != evidence_ref['sha256']:
                            fail('JOURNAL_TAMPERED', 'Simulation audit snapshot changed')
                    except (ValidationError, KeyError, TypeError):
                        fail('JOURNAL_TAMPERED', 'Simulation audit snapshot is invalid')
                self.entries.append(entry['event'])
                previous = entry['hash']
        self.previous = previous

    def last_for(self, approval_id):
        matching = [e for e in self.entries if e['approval_id'] == approval_id]
        return matching[-1] if matching else None

    def evidence(self, stage, data):
        name = f'evidence/{self.path.stem}/{len(self.entries):06d}-{stage}.json'
        raw = json_bytes(data)
        write_bytes(self.path.parent, name, raw)
        return {'path':name,'sha256':digest(raw)}

    def append(self, event):
        raw_entry = {'previous':self.previous,'event':event}
        raw_entry['hash'] = digest(json_bytes(raw_entry))
        with self.path.open('ab') as handle:
            handle.write(json.dumps(raw_entry,sort_keys=True,separators=(',',':')).encode('utf-8') + b'\n')
            handle.flush()
            os.fsync(handle.fileno())
        self.previous = raw_entry['hash']
        self.entries.append(event)
