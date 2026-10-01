"""Normalize observation receipts without assigning an experiment verdict."""
import hashlib
import json
from pathlib import Path

out = Path(__file__).resolve().parent
rows = []
for path in sorted(out.glob('*-window.json')):
    r = json.loads(path.read_text())
    s = r['samples']
    intervals = []
    for start in range(0, int(s[-1]['seconds']) - 4, 5):
        lo = next(x for x in s if x['seconds'] >= start)
        hi = next(x for x in s if x['seconds'] >= start+5)
        intervals.append(dict(start=start, cpu_fraction=(hi['cpu_seconds']-lo['cpu_seconds']) /
                              (hi['seconds']-lo['seconds'])))
    debug = [x['seconds'] for x in s if x['debugger_present']]
    row = dict(file=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
               status=r['status'], pid=r['pid'], start_unix=r['window_start_unix'],
               seconds=s[-1]['seconds'], intervals=intervals,
               focus_misses=sum(x['foreground_pid'] != r['pid'] for x in s),
               held=sorted({i for x in s for i in x['held']}),
               final_held=s[-1]['held'], debugger_sample_count=len(debug),
               first_debug_seconds=debug[0] if debug else None,
               last_debug_seconds=debug[-1] if debug else None,
               final_debugger_present=s[-1]['debugger_present'],
               code_identity=r['code_identity'], modules=r['modules'])
    rows.append(row)
    print(path.name, 'CPU intervals', [round(x['cpu_fraction'],3) for x in intervals],
          'focus misses', row['focus_misses'], 'held', row['held'],
          'debug samples',len(debug),'final debug',row['final_debugger_present'])
(out/'observations.json').write_text(json.dumps(rows,indent=2)+'\n')
