"""BJ-1 bounded read/reduction seam; no launcher, input, hooks or writes.

This module deliberately has no live attach CLI. The existing runtime session
owner must supply its validated Probe and state/health receipts. Controls use
only a disposable process owned by control_bj1_guard_capture.py.
Read order is not atomic. Epoch equality does not prove absence of interference.
"""
import csv
import hashlib
import json
from pathlib import Path
import struct
import time

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Database').is_dir())
DB = ROOT / 'Database/FFXII TZA'
GUARDS = DB / '_index/candidates/bj1-opus-replay-boot-statics/bj1-guards.tsv'
CAPTURES = DB / '_experiments/evidence/phyre-startup-globals'
BASE = 0x120000
EPOCH = 0x1F44850
COUNT = 1681
AUTHORITY = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def guard_rows(path=GUARDS):
    rows = list(csv.DictReader(Path(path).read_text().splitlines(), delimiter='\t'))
    addresses = [int(r['guard_va'], 16) for r in rows]
    if (len(rows) != COUNT or len(set(addresses)) != COUNT or
            addresses != sorted(addresses) or
            any(r['section'] != '.data' or int(r['header_sites']) <= 0 for r in rows) or
            sum(int(r['header_sites']) for r in rows) != 1732):
        raise ValueError('guard population prerequisite failed')
    return rows


def decode_guard(value):
    if value == 0:
        return {'observed_state': 'zero', 'local_rule': 'not completed / not currently building'}
    if value == 0xFFFFFFFF:
        return {'observed_state': 'building_sentinel', 'order': None}
    if 0x80000001 <= value <= 0xFFFFFFFE:
        return {'observed_state': 'completion_token', 'epoch_offset': value - 0x80000000}
    return {'observed_state': 'outside_prepared_rule', 'order': None}


def collect(reader, rows, *, load_base, epoch_address, control_address,
            control_bytes, seconds=3.0, expected_count=COUNT):
    """Actual focused observation path. Failure retains partial raw reads.

    No all-zero fallback; every DWORD is an exact read. Staged epoch reads and
    constant controls bracket the sample. A successful transport capture is
    CONTEXT_PENDING until the session owner verifies title/field and health.
    Replay's 19 guards are annotations, not observer positive controls.
    """
    if len(rows) != expected_count or expected_count <= 0 or not 0 < seconds <= 10:
        raise ValueError('bounded request prerequisite failed')
    result = dict(status='INVALID', evidence_kind='read transport; state/health unverified',
                  reads=[], guard_values=[], seconds_limit=seconds,
                  load_base=load_base, collection_atomic=False)
    start = time.monotonic()

    def read(address, size, purpose):
        if time.monotonic() - start > seconds:
            raise ValueError('bounded read budget exceeded')
        before = time.time()
        raw = reader.read(address, size)
        result['reads'].append(dict(address=address, size=size, purpose=purpose,
                                    start_unix=before, end_unix=time.time(),
                                    hex=None if raw is None else raw.hex()))
        if raw is None or len(raw) != size:
            raise ValueError('failed/short read; never zero-fill')
        return raw

    try:
        if read(control_address, len(control_bytes), 'positive-before') != control_bytes:
            raise ValueError('positive read control failed')
        if reader.read(0, 16) is not None:
            raise ValueError('null read negative control failed')
        result['null_rejected'] = True
        epoch_before = struct.unpack('<I', read(epoch_address, 4, 'epoch-before'))[0]
        for row in rows:
            va = int(row['guard_va'], 16)
            addr = va - BASE + load_base
            value = struct.unpack('<I', read(addr, 4, 'guard'))[0]
            result['guard_values'].append(dict(guard_va=row['guard_va'], runtime_address=addr,
                                               value=value, replay_step=row.get('replay_step', ''),
                                               **decode_guard(value)))
        epoch_after = struct.unpack('<I', read(epoch_address, 4, 'epoch-after'))[0]
        result.update(epoch_before=epoch_before, epoch_after=epoch_after,
                      epoch_bracket_equal=epoch_before == epoch_after)
        if read(control_address, len(control_bytes), 'positive-after') != control_bytes:
            raise ValueError('positive after control failed')
        result['status'] = 'COLLECTED_CONTEXT_PENDING'
    except Exception as exc:
        result['error'] = repr(exc)
    result['elapsed_seconds'] = time.monotonic() - start
    return result


def retained_coverage():
    rows = guard_rows()
    targets = [(int(r['guard_va'], 16), r['guard_va']) for r in rows] + [(EPOCH, 'EPOCH')]
    out = dict(method='A retained read interval analysis; no new process observation',
               guard_list_sha256=digest(GUARDS), guard_count=len(rows), captures=[],
               acceptance='Coverage only, not new semantic acceptance of EXP124 or INVALID captures')
    for name in ['title-defaults.json', 'title-pilot-readable.json', 'title-full.json']:
        path = CAPTURES / name
        data = json.loads(path.read_text())
        if data.get('exe_sha256') != AUTHORITY:
            raise ValueError('wrong retained binary identity')
        reads = data.get('reads', [])
        hits = []
        for address, label in targets:
            observations = []
            for i, read in enumerate(reads):
                if read.get('hex') is None:
                    continue
                raw = bytes.fromhex(read['hex'])
                if len(raw) != read['size']:
                    raise ValueError('retained short read cannot pass')
                offset = address - read['address']
                if 0 <= offset and offset + 4 <= len(raw):
                    observations.append(dict(read_index=i, value=int.from_bytes(raw[offset:offset+4], 'little'),
                                             purpose=read['purpose']))
            if observations:
                hits.append(dict(target=label, observations=observations))
        out['captures'].append(dict(path=str(path.relative_to(ROOT)), sha256=digest(path),
                                     status=data['status'], covered_targets=len(hits), hits=hits,
                                     closure_eligible=False if data['status']=='INVALID' else None))
    out['result'] = 'Valid title capture spans cover zero requested guards/epoch. Three INVALID provisional guard values do not close BJ1.'
    return out


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--retained-coverage', type=Path, required=True)
    args = ap.parse_args()
    if args.retained_coverage.exists():
        raise ValueError('immutable output already exists')
    result = retained_coverage()
    args.retained_coverage.write_text(json.dumps(result, indent=2)+'\n')
    print('BJ1 retained coverage complete; valid requested targets=0; invalid provisional targets=3; no live closure')
