"""Inspect old and candidate packets with real OS mapping and intercepted delivery."""
import ctypes
import hashlib
import json
from pathlib import Path
import key_packet as candidate

root = Path(__file__).resolve().parent
probe = candidate.probe
original = probe.u32.SendInput
packets = []

def intercept(n, ptr, size):
    assert size == ctypes.sizeof(probe.INPUT) == 40
    items = ctypes.cast(ptr, ctypes.POINTER(probe.INPUT))
    packets.append([dict(vk=items[i].u.ki.wVk, scan=items[i].u.ki.wScan,
                         flags=items[i].u.ki.dwFlags) for i in range(n)])
    return n

try:
    probe.u32.SendInput = intercept
    cases = []
    for name, vk in [('Right', 0x27), ('Left', 0x25), ('Up', 0x26), ('Down', 0x28), ('W', 0x57)]:
        for up in [False, True]:
            probe.send_key(vk, up)
            old = packets[-1]
            candidate.send_key(vk, up)
            new = packets[-1]
            assert len(old) == 2 and len(new) == 1
            assert old[1]['scan'] == new[0]['scan']
            assert old[1]['flags'] & 1 == 0
            assert new[0]['flags'] & 1 == (0 if name == 'W' else 1)
            assert bool(new[0]['flags'] & 2) == up
            assert new[0]['vk'] == 0
            cases.append(dict(name=name, up=up, map_type0=probe.u32.MapVirtualKeyW(vk, 0),
                              map_type4=probe.u32.MapVirtualKeyW(vk, 4), old=old, candidate=new))
finally:
    probe.u32.SendInput = original
report = dict(status='PACKET_CONTROLS_PASS', input_events_delivered=0, cases=cases,
              sources={str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in [Path(__file__), Path(candidate.__file__), Path(probe.__file__)]},
              limitation='Packet identity only. Expected game bytes and visible camera rotation require a live control.')
(root / 'packet-controls.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print('PASS: 10 packet cases; no input delivered')
