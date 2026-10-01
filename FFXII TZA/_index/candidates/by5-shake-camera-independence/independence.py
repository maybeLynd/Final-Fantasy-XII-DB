"""independence.py - control for BY-5 (FABLE, Claude Opus 5.5, 2026-09-26): nothing in the engine makes the shake pair
(section_010 / 011) depend on the camera pair (section_008 / 009).

L1 in the ATEL subresource registration 003306E0, each request's guard is its own lookup: the call 0032E400(0xFF, record)
   whose rdx is that request's record, stored to its own stack word, then reloaded and tested (`js` skips the request)
   immediately before that request is built. CAMC uses rbp+0x3F0 / [rsp+0x34], SHKD rbp+0xB60 / [rsp+0x38],
   SHKC rbp+0x500 / [rsp+0x3C]; no shake guard reads a camera guard word.
L2 the shake name resolver 003DD120 reads the slot's shake list (+0xF0) and slot index (+0x28), resets side B's four
   entries (+0x178..+0x1C2), and never touches the camera list (+0xD8).
L3 Shk1_FindByName 0037DB80 indexes its own per-slot shake bank 02ADD980 + slot*0x3D0.
Known positive: L1 must also find CAMC's guard; a pairing search that finds nothing cannot pass.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
R = ins(0x3306E0, 0xF00)
txt = ["%s %s" % (x.mnemonic, x.op_str) for x in R]
def rip_target(x):
    m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + int(m.group(1), 16) if m else None
# the guard lookups: lea rdx,[rbp+REC] ... call 0x32e400 ... mov dword ptr [rsp+SLOT], eax
guards = {}
for i, x in enumerate(R):
    if x.mnemonic == "call" and x.op_str == "0x32e400":
        rec = next((R[j].op_str.split("+ ")[1].rstrip("]") for j in range(i - 1, max(0, i - 6), -1)
                    if R[j].mnemonic == "lea" and R[j].op_str.startswith("rdx, [rbp + ")), None)
        slot = next((R[j].op_str.split("+ ")[1].split("]")[0] for j in range(i + 1, min(len(R), i + 4))
                     if R[j].mnemonic == "mov" and R[j].op_str.startswith("dword ptr [rsp + ") and R[j].op_str.endswith(", eax")), None)
        if rec and slot: guards[slot] = rec
# each tag block: the tag string lea, and the guard word reloaded and tested before it
TAGS = {0xD109E4: ("CAMC", "0x34", "0x3f0"), 0xD109EC: ("SHKD", "0x38", "0xb60"), 0xD109F4: ("SHKC", "0x3c", "0x500")}
for i, x in enumerate(R):
    t = rip_target(x) if x.mnemonic == "lea" else None
    if t in TAGS:
        name, slot, rec = TAGS[t]
        loads = [R[j] for j in range(max(0, i - 40), i) if R[j].mnemonic == "mov" and "dword ptr [rsp + 0x" in R[j].op_str
                 and R[j].op_str.split(", ")[0] in ("esi", "ecx")]
        last = loads[-1].op_str if loads else ""
        after_rec = [R[j].op_str for j in range(i, min(len(R), i + 14)) if R[j].mnemonic == "lea" and R[j].op_str.startswith("rcx, [rbp + ")]
        ok = last.endswith("[rsp + %s]" % slot) and guards.get(slot) == rec and after_rec and after_rec[0] == "rcx, [rbp + %s]" % rec
        check("L1 %s is guarded only by its own lookup (record rbp+%s -> [rsp+%s])" % (name, rec, slot), bool(ok),
              "(guard load: %s; request record: %s)" % (last, after_rec[:1]))
r = ins(0x3DD120, 0xCD); rt = " | ".join("%s %s" % (x.mnemonic, x.op_str) for x in r)
check("L2 003DD120 reads +0xF0 and +0x28, resets +0x178..+0x1C2, never touches +0xD8",
      "rcx + 0xf0]" in rt and "rbp + 0x28]" in rt and "rcx + 0x1c2]" in rt and "0xd8]" not in rt)
s = ins(0x37DB80, 0x40)
bank = [rip_target(x) for x in s if x.mnemonic == "lea"]
check("L3 Shk1_FindByName indexes 02ADD980 + slot*0x3D0", 0x2ADD980 in bank and any(x.op_str.endswith("0x3d0") for x in s))
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
