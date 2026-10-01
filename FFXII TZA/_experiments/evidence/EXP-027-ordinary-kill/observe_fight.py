"""Bounded read-only fight observation with a player-health stop; no input or debugger."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

root = Path(__file__).resolve().parent
kit = root.parents[3] / 'Tools/analysis-kit/gfz-scripts'
sys.path[:0] = [str(root.parent/'EXP-024-group-approach'), str(kit)]
import step
import runtime_probe as rp

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pid', type=int, required=True)
    p.add_argument('--target', type=int, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    assert not a.out.exists()
    sources = [Path(__file__), Path(step.__file__), kit/'runtime_probe.py',
               kit/'runtime_input_probe.py', kit/'runtime_poke.py', kit/'window_focus.py',
               root.parent/'EXP-023-camera-input/key_packet.py']
    result = dict(pid=a.pid, target=a.target, command=sys.argv, start_unix=time.time(),
                  status='INCOMPLETE', samples=[],
                  sources={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
    r = None
    try:
        found = rp.find_process('FFXII_TZA.exe')
        assert len(found) == 1 and found[0][0] == a.pid
        assert hashlib.sha256(Path(found[0][1]).read_bytes()).hexdigest() == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
        r = step.Reader(a.pid)
        assert rp.module_base(r.handle) == rp.IMAGE_BASE
        assert r.read(rp.CONTROL_ADDR, len(rp.CONTROL_BYTES)) == rp.CONTROL_BYTES
        start = time.perf_counter()
        while time.perf_counter()-start < 30:
            field = r.field()
            for row in field['rows']:
                page = r.num(row['unit']+0x698, '<Q')
                row['stats_page'] = page
                row['hp_raw_recheck'] = r.read(page+0x48, 4).hex() if page else None
            result['samples'].append(dict(seconds=time.perf_counter()-start, field=field))
            player = next(row for row in field['rows'] if row['slot'] == 0)
            target = next((row for row in field['rows'] if row['actor'] == a.target), None)
            if player['hp'] < 35:
                result['status'] = 'PLAYER_HEALTH_STOP'
                break
            if target is None:
                result['status'] = 'TARGET_ABSENT_NOT_DEATH_PROOF'
                break
            if target['hp'] is not None and target['hp'] <= 0:
                result['status'] = 'TARGET_ZERO_HP_REQUIRES_DEFEAT_CORROBORATION'
                break
            time.sleep(.05)
        else:
            result['status'] = 'WINDOW_EXPIRED'
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
