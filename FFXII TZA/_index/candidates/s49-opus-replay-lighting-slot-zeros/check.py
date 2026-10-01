"""Regression for a corrected claim (OPUS, 2026-09-25): PDeferredLightingSlot0080's zero spans were described as 'NO DEFAULT SET
HERE ... the preparation did not write here' from a SAMPLED default buffer (EXP-124), where a zero cannot distinguish untouched
storage from an explicit zero write. This executes the producer - the PDeferredLightingBase constructor 006458A0 - over a
0xA5-poisoned buffer: untouched bytes would stay 0xA5; the eight spans end 0, written by the constructor's own stores.

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session) supplies the image, the IAT
traps and the named bridges. No application stub and no stop boundary. Fixtures: six idle objects at 0x76300000, a 0x41D8-byte
object buffer filled 0xA5. The sampled bytes come from EXP-124's defaults (not re-read here); this run does not claim that the
sampled default buffer was produced by this constructor - the default-buffer copy was never traced.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RIP

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
CTOR = 0x6458A0
W.ALLOWED |= {0x16D6A0} | W.closure(CTOR)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
IDLE = 0x76300000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
OBJ, SIZE = 0x76280000, 0x41D8
ZERO_SPANS = [(0x000, 4), (0x008, 4), (0x010, 8), (0x01C, 20), (0x040, 20), (0x05C, 4), (0x064, 8), (0x074, 12)]   # the 8 corrected rows
VALUES = {0x004: 0x3F800000, 0x00C: 0x3F800000, 0x018: 0x3F800000, 0x030: 0x3F800000, 0x034: 0x3F800000, 0x038: 0x3F800000,
          0x03C: 0x3F800000, 0x054: 0x42480000, 0x058: 0x42C80000, 0x060: 0x3F800000, 0x06C: 0x3F800000, 0x070: 0x7F7FFFFF}

writers = {}
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: [writers.setdefault(a + k - OBJ, "%08X" % u.reg_read(UC_X86_REG_RIP))
                                                           for k in range(n)], begin=OBJ, end=OBJ + SIZE - 1)
uc.mem_write(OBJ, b"\xA5" * SIZE)
ok = S.call(CTOR, OBJ)
buf = bytes(uc.mem_read(OBJ, SIZE))

records, bad = 129, []
for k in range(records):
    base = 0x50 + 0x80 * k
    for off, n in ZERO_SPANS:
        seg = buf[base + off: base + off + n]
        if seg != bytes(n) or any((base + off + j) not in writers for j in range(n)):
            bad.append({"record": k, "span": "+%03X" % off, "bytes": seg.hex()})
    for off, v in VALUES.items():
        if struct.unpack_from("<I", buf, base + off)[0] != v:
            bad.append({"record": k, "value_at": "+%03X" % off, "got": "%08X" % struct.unpack_from("<I", buf, base + off)[0]})
untouched = [o for o in range(0x50, 0x50 + 0x80 * records) if buf[o] == 0xA5]
result = {"ok": bool(ok) and not bad and not untouched, "constructor_returned": bool(ok), "records": records,
          "zero_spans_checked": len(ZERO_SPANS), "mismatches": bad[:5], "bytes_left_A5_in_slot_array": len(untouched),
          "writer_sites_of_zero_spans": sorted({writers[0x50 + 0x80 * k + off] for k in (0, 1, 128) for off, n in ZERO_SPANS}),
          "note": "every byte of all 129 records is stored by 006458A0 (none left 0xA5); the eight zero spans hold explicit zero stores"}
json.dump(result, open(os.path.join(HERE, "result.json"), "w"), indent=1)
print("ok" if result["ok"] else "NOT ok", result["bytes_left_A5_in_slot_array"], result["writer_sites_of_zero_spans"], bad[:2])
