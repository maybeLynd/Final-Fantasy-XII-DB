"""be6_all_roles.py - BE-6: the five pump singletons left without a role on 2026-09-26, each given one from its bytes
(FABLE, Claude Opus 5.5, 2026-09-27). Static; companion to be6_two_singletons.py.
  R1 01F82D30 is the frame-end command-list teardown. Its "Ensure" 001E0550 allocates nothing: it sets byte 01F82D30
     to 0 and byte 01F82D31 to 1. Its update 001E0590 calls, in order: the renderer's 00185D80 (which moves
     +0xDBC to +0xDC0 and zeroes +0xDBC); the ordered command list's clear 0018B040; the owning vector's flush
     0018C8F0; then 001DB620. It then zeroes the two bytes.
  R2 01F81258 is the procedural-texture context. 001C0D40 allocates 0x1B8 and constructs with 001BE730, which
     formats the proceduralTexture_%s.ah path (008F99D0) and names proceduralTextureConfigs.txt (008F9A18). The
     update 001C0DD0 runs only while byte +8 is clear. It calls 001BF2E0 once 0019EB00 reports every element of the
     request loaded, then sets +8 to 1.
  R3 01F7F598 is the renderer: its accessor 00189120 is `mov rax, [01F7F598]; ret`, and GameApplication slot 8
     (render, 0017D090) calls it and then the render pass list 00187950.
  R4 01F810F0 is the pause-flag byte: 00199790 allocates 1 byte, zeroes it and stores the pointer; 001997D0 is its
     accessor, 00199780 reads the byte and 001997E0 writes it (`mov [rcx], dl; ret`).
  R5 01F81168 is the 0x520-byte map-art context 001A98B0 allocates (001A9903) and stores (001A9922).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(f): return list(cs.disasm(d[off(f):off(f) + SIZES[f]], f))
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) if m else None
def calls(f): return [int(x.op_str, 16) for x in ins(f) if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x") and not (f <= int(x.op_str, 16) < f + SIZES[f])]
def cstr(v): o = off(v); return d[o:d.index(b"\0", o)].decode("latin-1")
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

e = ins(0x1E0550); u = ins(0x1E0590); cu = calls(0x1E0590); r = ins(0x185D80)
ok1 = ([(x.mnemonic, rip(x)) for x in e[:2]] == [("mov", 0x1F82D31), ("mov", 0x1F82D30)] and 0x210EC0 not in calls(0x1E0550)
       and cu[:8] == [0x189120, 0x185D80, 0x18B4E0, 0x18B040, 0x18CA40, 0x18C8F0, 0x1DB620, 0x1A14D0][:len(cu[:8])] and len(cu) >= 7
       and [x.op_str for x in r[:3]] == ["eax, dword ptr [rcx + 0xdbc]", "dword ptr [rcx + 0xdc0], eax", "dword ptr [rcx + 0xdbc], 0"]
       and {rip(x) for x in u if x.mnemonic == "mov" and x.op_str.startswith("byte ptr")} == {0x1F82D30, 0x1F82D31})
check("R1 01F82D30: two latch bytes; the update ends the frame's command lists (clear 0018B040 before flush 0018C8F0)", ok1,
      "callees %s" % ["%08X" % c for c in cu])

a = ins(0x1C0D40); ca = calls(0x1C0D40); ctor = ins(0x1BE730); up = ins(0x1C0DD0); cup = calls(0x1C0DD0)
strs = {cstr(rip(x)) for x in ctor if x.mnemonic == "lea" and rip(x) and off(rip(x)) is not None and rip(x) in (0x8F99D0, 0x8F9A18)}
ok2 = (any(x.op_str == "ecx, 0x1b8" for x in a) and ca[:3] == [0x16D6A0, 0x210EC0, 0x1BE730]
       and any("proceduralTexture_%s.ah" in s for s in strs) and any("proceduralTextureConfigs.txt" in s for s in strs)
       and cup == [0x19EF80, 0x19EB00, 0x1BF2E0] and any(x.op_str == "byte ptr [rcx + 8], 0" for x in up)
       and any(x.op_str == "byte ptr [rbx + 8], 1" for x in up))
check("R2 01F81258: the procedural-texture context, set up once when its .ah request is loaded", ok2, str(sorted(strs)))

acc = ins(0x189120); rend = calls(0x17D090)
ok3 = len(acc) == 2 and rip(acc[0]) == 0x1F7F598 and acc[1].mnemonic == "ret" and rend[:2] == [0x189120, 0x187950]
vt = struct.unpack_from("<Q", d, off(0x8C5760 + 8 * 8))[0]
check("R3 01F7F598: the renderer - GameApplication slot 8 (render) fetches it and runs the pass list 00187950", ok3 and vt == 0x17D090,
      "slot 8 = %08X, callees %s" % (vt, ["%08X" % c for c in rend[:3]]))

en = ins(0x199790)
ok4 = (any(x.op_str == "ecx, 1" for x in en) and any(x.op_str == "byte ptr [rax], 0" for x in en)
       and {rip(x) for x in en if rip(x)} == {0x1F810F0}
       and [(x.mnemonic, x.op_str) for x in ins(0x1997E0)] == [("mov", "byte ptr [rcx], dl"), ("ret", "")]
       and [(x.mnemonic, x.op_str) for x in ins(0x199780)] == [("movzx", "eax, byte ptr [rcx]"), ("ret", "")]
       and rip(ins(0x1997D0)[0]) == 0x1F810F0)
check("R4 01F810F0: one byte, read by 00199780 and written by 001997E0 (the pause flag, BE-2)", ok4)

m = ins(0x1A98B0); at = {x.address: x for x in m}
ok5 = at[0x1A9903].op_str == "ecx, 0x520" and rip(at[0x1A9922]) == 0x1F81168 and at[0x1A9922].op_str.startswith("qword ptr [rip")
check("R5 01F81168: the 0x520-byte map-art context", ok5)
print("FAILS", fails)
sys.exit(1 if fails else 0)
