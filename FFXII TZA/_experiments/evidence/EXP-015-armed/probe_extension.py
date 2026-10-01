"""Existing probe with the on-screen Back key C added, and SendInput receipts.

No shared instrument source changes. The original tool's negative verdict is not
promoted: delivered OS events and readable zero bytes alone do not prove liveness.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'Tools/analysis-kit/gfz-scripts'))
import runtime_input_probe as probe
probe.KEYS.append(('C', 0x43))
original_send = probe.send_key
def recorded_send(vk, up):
    result = original_send(vk, up)
    print('SENDINPUT vk=%#x up=%s accepted=%d requested=2' % (vk, up, result), flush=True)
    return result
probe.send_key = recorded_send
try:
    raise SystemExit(probe.main())
finally:
    # Always release the explicitly requested keys, including after interruption.
    wanted = sys.argv[sys.argv.index('--keys') + 1].lower().split(',')
    for name, vk in probe.KEYS:
        if name.lower() in wanted:
            recorded_send(vk, True)
