"""Preset second approach: back out twice, three W pulses, reopen menu; no adaptive pathing."""
import json
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parent
step = root.parent/'EXP-024-group-approach/step.py'
for name, key, hold in [('cancel-near-target', 'C', .3), ('close-near-menu', 'C', .3),
                        ('approach-w03', 'W', 1), ('approach-w04', 'W', 1),
                        ('approach-w05', 'W', 1), ('open-menu-final', 'Space', .3)]:
    out = root/(name+'.json')
    run = subprocess.run([sys.executable, str(step), '--pid', '38872', '--key', key,
                          '--hold', str(hold), '--field', '--out', str(out)], capture_output=True, text=True)
    assert run.returncode == 0, run.stdout+run.stderr
    d = json.loads(out.read_text())
    player = next(row for row in d['after']['rows'] if row['slot'] == 0)
    print(name, player['hp'], player['position'], flush=True)
    assert player['hp'] >= 35, 'health stop'
