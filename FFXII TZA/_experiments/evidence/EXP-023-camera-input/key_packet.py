"""Private EXP-023 single scan-code input candidate; preserve E0 identity."""
import ctypes
from pathlib import Path
import sys

kit = Path(__file__).resolve().parents[4] / 'Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import runtime_input_probe as probe

EXTENDED = 1
# Microsoft Keyboard Input Overview: dedicated arrows have E0 scans. On this
# host MapVirtualKeyW(type=4) still omits E0 for these four keys (control retained).
ARROW_SCANS = {0x25: 0x4B, 0x26: 0x48, 0x27: 0x4D, 0x28: 0x50}

def packet(vk, up):
    scan = probe.u32.MapVirtualKeyW(vk, 4)
    prefix = scan >> 8
    if not scan or prefix not in (0, 0xE0):
        raise ValueError('unmapped or unsupported scan prefix: %#x' % scan)
    if vk in ARROW_SCANS:
        if scan & 0xFF != ARROW_SCANS[vk]:
            raise ValueError('unexpected arrow scan mapping')
        prefix = 0xE0
    flags = probe.KEYEVENTF_SCANCODE | (EXTENDED if prefix == 0xE0 else 0)
    flags |= probe.KEYEVENTF_KEYUP if up else 0
    event = probe.INPUT()
    event.type = probe.INPUT_KEYBOARD
    event.u.ki = probe.KEYBDINPUT(0, scan & 0xFF, flags, 0, None)
    return event

def send_key(vk, up):
    event = packet(vk, up)
    count = probe.u32.SendInput(1, ctypes.byref(event), ctypes.sizeof(event))
    print('SCANINPUT vk=%#x scan=%#x flags=%#x up=%s accepted=%d requested=1' %
          (vk, event.u.ki.wScan, event.u.ki.dwFlags, up, count), flush=True)
    if count != 1:
        raise OSError(ctypes.get_last_error(), 'SendInput did not accept its event')
    return count

if __name__ == '__main__':
    probe.KEYS.extend([('C', 0x43), ('W', 0x57)])
    probe.send_key = send_key
    wanted = sys.argv[sys.argv.index('--keys') + 1].lower().split(',')
    selected = [(name, vk) for name, vk in probe.KEYS if name.lower() in wanted]
    if not selected or len(selected) != len(wanted):
        raise ValueError('keys must be a nonempty supported unique list')
    try:
        raise SystemExit(probe.main())
    finally:
        for name, vk in selected:
            send_key(vk, True)
