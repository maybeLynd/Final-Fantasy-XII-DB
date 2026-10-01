"""ga1_status_order_keys.py - GA-1: five status_data.bin bytes are order keys for five status listings, and 0xFF
leaves a status out of a listing (FABLE, Claude Opus 5.5, 2026-09-26). Static reads of the shipping image plus the
status table ASTRA retained (status-row-key-qualification/status-table.bin, sha256 c5ea6807...).

  K1 the status arm of the query filler 0031C5D0 copies row bytes into the class-26 record:
     +0x10 -> +0x20, +0x26 -> +0x21, +0x27 -> +0x22, +0x13 -> +0x23, +0x02 -> +0x24 (0031E22C-0031E24C).
  K2 002D02C0(out, count, mask, kind) selects record +0x20 + kind (kind 0..4) as the key, emits {id, key, +0x25 bit 0}
     per status in the mask and counts keys that are not 0xFF; the sort 002D03B0 orders entries by the key byte
     through the comparator 002D0270 (0x002D03D3 - 0x163; signed, so 0xFF sorts first).
  K3 00273BA0 fills the shared cache 022C8B08 (built once by 0035D490) with the 32 class-26 records and stores the
     orderings for kinds 1..4 as 32-pointer tables at cache +0x1500, +0x1600, +0x1700, +0x1800 (the store loops start
     from lea +0x1508 and write 0x18 below the advanced pointer).
  K4 00275E40(mask, kind, unit) counts the statuses of a mask whose selected key is not 0xFF
     (kind 1 -> +0x23, 2 -> +0x22, 3 -> +0x24, otherwise +0x21).
  K5 the battle reaction queue 003BBD00 refuses a status reaction (returns 0xFF) when record +0x24, row +0x02, is 0xFF.
  K6 data: the 0xFF sets - +0x10 none; +0x27 HP Critical; +0x13 KO, Stone, HP Critical, X-Zone; +0x02 KO, Invisible,
     HP Critical, X-Zone; +0x26 twelve rows, Protect, Shell, Haste, Bravery, Faith, Invisible, Regen, Float, Berserk,
     Bubble, Libra and HP Critical (Reflect keeps its key). Where a key is
     present it equals +0x10.
  K7 sensitivity: the +0x13 set differs from the +0x02 set (Stone for Invisible) - the reading the 2026-09-15 text
     gave, "+0x13 0xFF in exactly KO, Invisible, HP Critical and X-Zone", fails here.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import hashlib, json, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

a = dis(0x31E22C, 0x31E250)
pairs = [("movzx eax, byte ptr [rbp + 0x10]", "mov byte ptr [rbx + 0x20], al"), ("movzx eax, byte ptr [rbp + 0x26]", "mov byte ptr [rbx + 0x21], al"),
         ("movzx eax, byte ptr [rbp + 0x27]", "mov byte ptr [rbx + 0x22], al"), ("movzx eax, byte ptr [rbp + 0x13]", "mov byte ptr [rbx + 0x23], al"),
         ("movzx eax, byte ptr [rbp + 0x2]", "mov byte ptr [rbx + 0x24], al")]
seq = list(a.values())
check("K1 the status arm copies row +0x10/+0x26/+0x27/+0x13/+0x02 to record +0x20..+0x24",
      all(seq[2 * i] == p[0].replace("0x2]", "2]") and seq[2 * i + 1] == p[1] for i, p in enumerate(pairs)), " | ".join(seq[:10]))
b = dis(0x2D02C0, 0x2D02C0 + 0xE1)
sel = {v for v in b.values() if re.fullmatch(r"movzx edx, byte ptr \[rcx \+ 0x2[0-4]\]", v)}
cmp = dis(0x2D0270, 0x2D027D)
srt = dis(0x2D03B0, 0x2D03B0 + 0x53)
check("K2 002D02C0 keys on record +0x20 + kind, counts non-0xFF; 002D03B0 sorts on byte +1 (signed)",
      len(sel) == 5 and "cmp dl, 0xff" in b.values() and "movsx r8d, byte ptr [rcx + 1]" in cmp.values()
      and "call 0x249ce0" in srt.values() and srt.get(0x2D03CC) == "lea rax, [rip - 0x163]", "%d key selects" % len(sel))
c = dis(0x273BA0, 0x273BA0 + 0x283)
acc = dis(0x35D490, 0x35D4D1)
k3 = all(any(("[rbx + 0x%x]" % t) in v for v in c.values()) for t in (0x1508, 0x1608, 0x1708, 0x1808)) \
     and [v for v in c.values() if v.startswith("mov r9d, ")] == ["mov r9d, 1", "mov r9d, 2", "mov r9d, 3", "mov r9d, 4"] \
     and "mov ecx, 0x1a" in c.values() and "call 0x273ba0" in acc.values()
check("K3 00273BA0 caches the 32 status records and four orderings (kinds 1..4) at cache +0x1500..+0x18FF", k3)
e = dis(0x275E40, 0x275E40 + 0xC8)
k4 = all(x in e.values() for x in ("mov ecx, 0x1a", "cmp byte ptr [rdx + 0x21], 0xff", "cmp byte ptr [rdx + 0x24], 0xff",
                                    "movzx ecx, byte ptr [rax + 0x22]", "cmp byte ptr [rdx + 0x23], 0xff", "cmp ebx, 0x20"))
check("K4 00275E40 counts a mask's statuses whose selected key is not 0xFF", k4)
f = dis(0x3BBD66, 0x3BBD80)
check("K5 the battle reaction queue refuses a status reaction whose row +0x02 is 0xFF",
      f.get(0x3BBD66) == "cmp byte ptr [rsi + 0xc], 2" and f.get(0x3BBD6F) == "mov ecx, 0x1a" and f.get(0x3BBD79) == "cmp byte ptr [rax + 0x24], 0xff"
      and f.get(0x3BBD7D) == "je 0x3bbd4e" and dis(0x3BBD4E, 0x3BBD50).get(0x3BBD4E) == "mov al, 0xff")
EV = DB / "_experiments/evidence/status-row-key-qualification"
t = (EV / "status-table.bin").read_bytes()
names = [r["name"] for r in sorted(json.loads((EV / "observation.json").read_text(encoding="utf-8"))["decoded_bank5_records"], key=lambda r: r["entry"])]
rows = [t[0x20 + i * 40:0x20 + (i + 1) * 40] for i in range(32)]
ff = {o: sorted(names[i] for i, r in enumerate(rows) if r[o] == 0xFF) for o in (0x10, 0x26, 0x27, 0x13, 0x02)}
agree = all(r[o] == r[0x10] for r in rows for o in (0x26, 0x27, 0x13, 0x02) if r[o] != 0xFF)
k6 = (hashlib.sha256(t).hexdigest().startswith("c5ea6807") and ff[0x10] == [] and ff[0x27] == ["HP Critical"]
      and ff[0x13] == sorted(["KO", "Stone", "HP Critical", "X-Zone"]) and ff[0x02] == sorted(["KO", "Invisible", "HP Critical", "X-Zone"])
      and len(ff[0x26]) == 12 and "Reflect" not in ff[0x26] and agree)
check("K6 the shipped 0xFF sets, and present keys equal +0x10", k6, repr({"%02X" % k: v for k, v in ff.items()}))
check("K7 sensitivity: +0x13's set is not +0x02's (the 2026-09-15 reading fails)",
      ff[0x13] != ff[0x02] and "Invisible" not in ff[0x13] and "Stone" in ff[0x13])
print("FAILS", fails)
sys.exit(1 if fails else 0)
