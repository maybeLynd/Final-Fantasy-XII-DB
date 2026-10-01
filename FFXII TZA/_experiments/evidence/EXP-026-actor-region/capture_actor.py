"""Read one independently anchored kind-3 actor; preserve disagreements as observations."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
import time

root = Path(__file__).resolve().parent
kit = root.parents[3] / 'Tools/analysis-kit/gfz-scripts'
sys.path[:0] = [str(root.parent / 'EXP-024-group-approach'), str(kit)]
import step
import runtime_probe as rp

def decode(raw, address):
    if len(raw) < 0x120:
        raise ValueError('short actor header')
    kind, seq = raw[3] >> 5, raw[3] & 31
    if kind != 3 or seq not in (5, 6, 7):
        raise ValueError('unsupported kind/sequence')
    size, wait_offset, nwait, nresource = (0x668, 0x578, 6, 8) if seq == 7 else (0x6E0, 0x5A0, 8, 10)
    if len(raw) != size:
        raise ValueError('wrong per-sequence extent')
    expected = {0xA0: 0x4D8, 0xA8: wait_offset, 0xB8: 0x120, 0xC0: 0x350}
    pointers = {hex(off): struct.unpack_from('<Q', raw, off)[0] for off in expected}
    cursor = struct.unpack_from('<b', raw, 0x11)[0]
    return dict(kind=kind, sequence=seq, size=size, pointers=pointers,
                pointer_deltas={k: v-address if v else None for k, v in pointers.items()},
                expected_deltas={hex(k): v for k, v in expected.items()},
                region_map_matches=all(pointers[hex(k)] == address+v for k, v in expected.items()),
                cursor=cursor, observed_counts=list(raw[0x88:0x8A]),
                expected_counts=[nwait, nresource], cursor_in_array=0 <= cursor < raw[0x88],
                ordinal_bytes=list(raw[0x60:0x64]),
                resource_slots=[raw[0x4D8+i*0x14:0x4D8+(i+1)*0x14].hex() for i in range(nresource)],
                wait_slots=[raw[wait_offset+i*0x28:wait_offset+(i+1)*0x28].hex() for i in range(nwait)])

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pid', type=int, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    assert not a.out.exists()
    source_paths = [Path(__file__), Path(step.__file__), kit/'runtime_probe.py',
                    kit/'window_focus.py', kit/'runtime_input_probe.py', kit/'runtime_poke.py',
                    root.parent/'EXP-023-camera-input/key_packet.py']
    result = dict(status='INCOMPLETE', pid=a.pid, command=sys.argv, start_unix=time.time(), samples=[],
                  sources={str(x): hashlib.sha256(x.read_bytes()).hexdigest() for x in source_paths})
    r = None
    try:
        found = rp.find_process('FFXII_TZA.exe')
        assert len(found) == 1 and found[0][0] == a.pid
        result['exe_sha256'] = hashlib.sha256(Path(found[0][1]).read_bytes()).hexdigest()
        assert result['exe_sha256'] == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
        r = step.Reader(a.pid)
        assert rp.module_base(r.handle) == rp.IMAGE_BASE
        assert r.read(rp.CONTROL_ADDR, len(rp.CONTROL_BYTES)) == rp.CONTROL_BYTES
        start = time.perf_counter()
        for index in range(40):
            sample = dict(index=index, seconds=time.perf_counter()-start, frame_before=r.num(0x0208D45C, '<I'))
            field = r.field()
            player = next(row for row in field['rows'] if row['slot'] == 0)
            actor = player['actor']
            managers = []
            memberships = []
            for slot in range(5):
                manager = 0x02098E10 + slot*0x288
                header = r.read(manager, 0x18)
                pool = struct.unpack_from('<Q', header, 8)[0]
                entry = dict(slot=slot, address=manager, header_raw=header.hex(), pool=pool)
                if pool:
                    count = r.num(pool, '<I')
                    assert 0 <= count <= 4096, ('manager count', slot, count)
                    raw = r.read(pool+8, count*8) if count else b''
                    entry.update(count=count, table_raw=raw.hex())
                    memberships += [dict(manager_slot=slot, ordinal=j) for j in range(count)
                                    if struct.unpack_from('<Q', raw, j*8)[0] == actor]
                managers.append(entry)
            head = r.read(actor, 0x120)
            assert head[3] >> 5 == 3 and head[3] & 31 in (5, 6, 7)
            raw = r.read(actor, 0x668 if head[3] & 31 == 7 else 0x6E0)
            sample.update(player=player, managers=managers, memberships=memberships,
                          actor_raw=raw.hex(), decoded=decode(raw, actor),
                          frame_after=r.num(0x0208D45C, '<I'))
            result['samples'].append(sample)
            time.sleep(.05)
        result['status'] = 'OBSERVED'
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        if r:
            r.close()
        result['end_unix'] = time.time()
        a.out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(json.dumps(dict(status=result['status'], samples=len(result['samples']), error=result.get('error'))))

if __name__ == '__main__':
    main()
