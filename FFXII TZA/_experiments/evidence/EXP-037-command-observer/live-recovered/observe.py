"""Read-only EXP035 observer. Offline-tested preparation; no live validation yet."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import time

HERE = Path(__file__).resolve().parent
KIT = HERE.parents[4] / 'Tools/analysis-kit/gfz-scripts'
EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
TEXT_SHA = '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
EXE = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def qualify(reader, raw, base, verdict, modules, control_address, control_bytes):
    """Pure read-path qualification; module inventory comes from the runtime wrapper."""
    require(sha(raw) == EXE_SHA, 'executable identity mismatch')
    require(base == 0x120000, 'image base mismatch')
    require(verdict == 'clean' and bool(modules), 'module qualification failed')
    require(reader.read(control_address, len(control_bytes)) == control_bytes, 'read control mismatch')
    pe = struct.unpack_from('<I', raw, 0x3C)[0]
    require(raw[pe:pe + 4] == b'PE\0\0', 'PE signature missing')
    count = struct.unpack_from('<H', raw, pe + 6)[0]
    table = pe + 24 + struct.unpack_from('<H', raw, pe + 20)[0]
    texts = []
    for n in range(count):
        offset = table + 40 * n
        if raw[offset:offset + 8].rstrip(b'\0') != b'.text':
            continue
        virtual, rva, size, disk = struct.unpack_from('<4I', raw, offset + 8)
        length = min(virtual, size)
        expected = raw[disk:disk + length]
        actual = reader.read(base + rva, length)
        require(length == 7996981 and len(expected) == length, 'text extent mismatch')
        require(sha(expected) == TEXT_SHA, 'disk text identity mismatch')
        require(actual == expected, 'live text identity mismatch')
        texts.append(dict(rva=rva, bytes=length, disk_sha256=sha(expected), live_sha256=sha(actual)))
    require(len(texts) == 1, 'require exactly one text section')
    return dict(exe_sha256=sha(raw), image_base=base, module_verdict=verdict,
                modules=modules, code_identity=texts)


def capture(reader, sample, seconds, slot, minimum_hp, clock=time.perf_counter, sleep=time.sleep):
    """At most 100 samples at <=20Hz; reads may cross the nominal wall deadline."""
    result = dict(status='INVALID', samples=[])
    try:
        require(math.isfinite(seconds) and 0 < seconds <= 5, 'duration must be in (0,5]')
        require(0 <= slot < 32 and minimum_hp > 0, 'invalid slot or HP floor')
        start = clock()
        initial_hp = None
        identity = None
        for _ in range(100):
            elapsed = clock() - start
            if elapsed >= seconds:
                break
            row = sample(reader, slot=slot)
            result['samples'].append(dict(seconds=elapsed, observation=row))
            require(row['status'] == 'CONSISTENT_SAMPLE', 'ambiguous command/target selection')
            before = row['player_before']
            after = row['player_after']
            require(len(after) == 1, 'selected player missing after sample')
            current = (before['unit'], before['actor'])
            if identity is None:
                identity = current
            require(current == identity and (after[0]['unit'], after[0]['actor']) == identity,
                    'player identity changed across capture')
            hp = [before['hp'], after[0]['hp']]
            require(all(type(x) is int for x in hp), 'player HP unavailable')
            if initial_hp is None:
                initial_hp = hp[0]
            if min(hp) < minimum_hp or min(hp) < initial_hp:
                result['status'] = 'HEALTH_STOP'
                result['stop_hp'] = hp
                break
            sleep(min(.05, max(0, seconds - (clock() - start))))
        else:
            result['sample_cap_reached'] = True
        require(bool(result['samples']), 'no samples captured')
        if result['status'] != 'HEALTH_STOP':
            result['status'] = 'OBSERVED'
        result['elapsed_seconds'] = clock() - start
    except Exception as error:
        result['status'] = 'INVALID'
        result['error'] = repr(error)
    return result


def receipts():
    paths = [Path(__file__), HERE / 'dependencies.json']
    dependencies = json.loads((HERE / 'dependencies.json').read_text())
    for name, expected in dependencies.items():
        path = HERE / name
        require(sha(path.read_bytes()) == expected, 'dependency changed: ' + name)
        paths.append(path)
    return {str(path.resolve()): sha(path.read_bytes()) for path in paths}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pid', type=int, required=True)
    parser.add_argument('--seconds', type=float, default=3)
    parser.add_argument('--slot', type=int, default=0)
    parser.add_argument('--minimum-hp', type=int, default=35)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    # Exclusive creation prevents replacing earlier evidence even on failure.
    with args.out.open('x', encoding='utf-8') as output:
        record = dict(status='INVALID', command=sys.argv, pid=args.pid, start_unix=time.time())
        reader = None
        try:
            require(math.isfinite(args.seconds) and 0 < args.seconds <= 5, 'duration must be in (0,5]')
            require(0 <= args.slot < 32 and args.minimum_hp > 0, 'invalid slot or HP floor')
            record['sources_before'] = receipts()
            board_path = HERE.parents[3] / '_index/_inbox/TEAM.json'
            board = json.loads(board_path.read_text())
            reservations = [task for task in board['tasks'] if task['status'] == 'ACTIVE' and
                            any(resource['key'] == '@runtime' for resource in task['resources'])]
            require(len(reservations) == 1 and reservations[0]['agent'] == 'ASTRA',
                    'ASTRA must own the runtime reservation')
            record['runtime_reservation'] = reservations[0]
            record['board_revision'] = board['revision']
            sys.path[:0] = [str(KIT), str(HERE.parent.parent / 'EXP-024-group-approach'),
                           str(HERE.parent.parent / 'EXP-035-command-target-binding')]
            import runtime_probe as rp
            import ffxii_runtime as runtime
            from step import Reader
            from binding import sample
            found = rp.find_process('FFXII_TZA.exe')
            require(len(found) == 1 and found[0][0] == args.pid, 'require exactly the intended process')
            record['exe'] = found[0][1]
            require(Path(record['exe']).resolve() == EXE.resolve(), 'reference executable path mismatch')
            raw = Path(found[0][1]).read_bytes()
            record['exe_sha256'] = sha(raw)
            verdict, hits, modules = runtime.classify(args.pid)
            record['watched_modules'] = hits
            record['modules_before'] = modules
            reader = Reader(args.pid)
            record['qualification_before'] = qualify(reader, raw, rp.module_base(reader.handle),
                                                     verdict, modules, rp.CONTROL_ADDR, rp.CONTROL_BYTES)
            captured = capture(reader, sample, args.seconds, args.slot, args.minimum_hp)
            record['capture'] = captured
            verdict, hits, modules = runtime.classify(args.pid)
            record['watched_modules_after'] = hits
            record['qualification_after'] = qualify(reader, Path(record['exe']).read_bytes(),
                                                    rp.module_base(reader.handle), verdict, modules,
                                                    rp.CONTROL_ADDR, rp.CONTROL_BYTES)
            record['sources_after'] = receipts()
            require(record['sources_before'] == record['sources_after'], 'source identity changed')
            record['status'] = captured['status']
        except Exception as error:
            record['status'] = 'INVALID'
            record['error'] = repr(error)
        finally:
            if reader is not None:
                try:
                    reader.close()
                except Exception as error:
                    record['status'] = 'INVALID'
                    record['close_error'] = repr(error)
            record['end_unix'] = time.time()
            json.dump(record, output, indent=2)
            output.write('\n')
        print(record['status'], args.out)
        return 0 if record['status'] == 'OBSERVED' else 3


if __name__ == '__main__':
    raise SystemExit(main())
