"""check.py (SWE2-FRONTIER, 2026-10-03): 0022B7E0's mode byte is 02064AD3 itself; 02064AD4 takes no part.
1. 0022B84F loads byte 02064AD3, 0022B858 cmove ecx, ebx (ebx = 2 from 0022B841), 0022B85B stores cl back to 02064AD3.
2. 0022B8A1 compares byte 02064AD3 with bl (2) before 0022B8AB call 00184960 (ecx = 2).
3. No instruction of 0022B7E0 references 02064AD4 rip-relatively. Control: the same reference scan finds 02064AD3
   (three sites), so it is not blind to this body's rip-relative bytes.
4. The page carries the correction with the original struck. Exit 0 with FAILS 0."""
import os, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
os.chdir(ROOT / "Database/Tools/work/FABLE/pub140-scratch")
exec(open("disw.py").read().split("fn = int")[0])
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ins = []
for i in Cs(CS_ARCH_X86, CS_MODE_64).disasm(bytes(d[off(0x0022B7E0):off(0x0022B8BB)]), 0x0022B7E0):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    t = i.address + i.size + (1 if m and m.group(1) == "+" else -1) * int(m.group(2), 16) if m else None
    ins.append((i.address, i.mnemonic, i.op_str, t))
at = {a: (mn, op, t) for a, mn, op, t in ins}
fails = 0


def ok(c, msg):
    global fails
    print(("PASS  " if c else "FAIL  ") + msg)
    fails += 0 if c else 1


ok(at.get(0x0022B841, ("", ""))[:2] == ("mov", "ebx, 2"), "1a ebx = 2 at 0022B841")
ok(at.get(0x0022B84F, (0, 0, 0))[2] == 0x02064AD3 and at[0x0022B84F][0] == "movzx", "1b 0022B84F loads byte 02064AD3")
ok(at.get(0x0022B858, ("", ""))[:2] == ("cmove", "ecx, ebx"), "1c 0022B858 cmove ecx, ebx (2 when 0037C2E0 returned 0)")
ok(at.get(0x0022B85B, (0, 0, 0))[2] == 0x02064AD3 and at[0x0022B85B][1].startswith("byte ptr"), "1d 0022B85B stores the byte back to 02064AD3")
ok(at.get(0x0022B8A1, (0, 0, 0))[2] == 0x02064AD3 and at.get(0x0022B8AB, ("", ""))[:2] == ("call", "0x184960"),
   "2 0022B8A1 tests 02064AD3 against 2 before 00184960")
refs = lambda cell: [a for a, mn, op, t in ins if t == cell]
ok(refs(0x02064AD4) == [], "3 no rip-relative reference to 02064AD4 in 0022B7E0")
ok(len(refs(0x02064AD3)) == 3, "3C control: the same scan finds 02064AD3 three times (%d)" % len(refs(0x02064AD3)))
page = (ROOT / "Database/FFXII TZA/02-Resource-And-Asset-Pipeline/authored-data-table-registry.md").read_text(encoding="utf-8").replace("\r\n", "\n")
ok("~~while the machine works,\n`02064AD4` mirrors" in page and "the byte at `02064AD3` is re-stored with its own value" in page,
   "4 the page carries the correction with the original struck")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
