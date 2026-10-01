"""Normalize raw observation windows without assigning a scientific verdict."""
import hashlib
import json
from pathlib import Path

out = Path(__file__).resolve().parent
summary = {}
for name in ['baseline','noarm','post','visual','final-post']:
    f = out / (name+'-window.json')
    r = json.loads(f.read_text())
    assert r['status'] == 'OBSERVED', (name, r.get('error'))
    s = r['samples']
    assert s and r['code_identity'][0]['matches']
    windows = []
    for lo in range(0, int(s[-1]['seconds'])+1, 5):
        part = [x for x in s if lo <= x['seconds'] < lo+5]
        if len(part) < 2:
            continue
        wall = part[-1]['seconds']-part[0]['seconds']
        cpu = part[-1]['cpu_seconds']-part[0]['cpu_seconds']
        windows.append(dict(start_seconds=lo, wall_seconds=wall,cpu_seconds=cpu,one_core_percent=100*cpu/wall))
    debug = [x['seconds'] for x in s if x['debugger_present']]
    summary[name] = dict(raw=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
                        window_start_unix=r['window_start_unix'],sample_count=len(s),
                        foreground_pids=sorted({x['foreground_pid'] for x in s}),
                        held_indices=sorted({i for x in s for i in x['held']}),
                        debugger_seconds=[min(debug),max(debug)] if debug else [],cpu_windows=windows)
    print(name, 'CPU %', [round(x['one_core_percent'],2) for x in windows], 'debug',summary[name]['debugger_seconds'])
for filename in ['attached-screenshot-time.json','attached-close-screenshot-time.json']:
    capture = json.loads((out/filename).read_text())
    visual = summary['visual']
    offset = capture['captured_unix']-visual['window_start_unix']
    assert visual['debugger_seconds'][0] < offset < visual['debugger_seconds'][1], 'screenshot outside attachment'
    capture['observer_seconds'] = offset
    summary[filename] = capture
summary['screenshot_file_timestamps'] = {f.name:f.stat().st_mtime for f in out.glob('*.jpg')}
(out/'normalized.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
