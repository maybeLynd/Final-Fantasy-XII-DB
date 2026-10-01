"""gd1_first_parameter.py - GD-1: the class of the render-item body 0060B980's first parameter (FABLE, Claude Opus 5.5,
2026-09-26; first read by a delegated read-only pass, every step re-checked here).

  G1 0060B980 uses the parameter as a polymorphic object: r14 = rcx (0060B9D4); it returns early unless bit 0 of
     dword +0x08 is set (0060B9D7) and unless +0x80 is non-null (0060B9EA); it calls vtable slot 2 through [r14]
     (0060BEB3/0060BEB9).
  G2 RTTI: vtable 00D49930 names Phyre::PRendering::PRenderer; 00D498F0 PRendererBase; 00D49910 PRendererForJobs.
     All three are 3-slot; PRenderer and PRendererBase share slot 2, PRendererForJobs has its own.
  G3 the constructor 005DC2F0 installs 00D49930 (005DC375/005DC37C) and stores the fields 0060B980 reads:
     +0x08, +0x20 (its rdx), +0x80, +0xA8, and the dword +0x220 through rdi = this.
  G4 its one caller is the PApplication constructor 00792350, on this + 0xE8 (00792414, 0079241E); 00792350 installs
     the vtable whose RTTI names Phyre::PFramework::PApplication (00792373).
  G5 one complete chain from that object to a 0060B980 call, each register checked for writes inside its window:
     0017D000 passes app + 0xE8 to 00189000 (0017D04F, 0017D06F); 00189000 hands it to 00184F20 (00189027, 0018905B,
     00189061), which stores it at the new object's +8 (00184F4C), and 00189000 publishes that object at 01F7F598
     (00189067); 001C2DB0 takes [01F7F598]+8 (001C2DD7 via 00189120, 001C2DDC) into rsi and passes it as rdx to
     001EA830 (001C2E1D, 001C2E2A); 001EA830 keeps it in rdi and passes it to 0067C260 (001EA84A, 001EA916,
     001EA919); 0067C260 keeps it in r10, sets its +0x80 (0067C2C2), reads its +0x220 (0067C2EA) and calls
     0060B980 with it (0067C2FD, 0067C300). The one call inside that window, 0067C2A7, is on a branch that
     returns (0067C2AE jmp 0067C306) and never reaches the render-item call.
  Control: the register-write test is sensitive - it flags rsi in 001C2DB0 once the window runs past the last use.
Scope: only this path is traced. 0060B980 has further callers that pass the object through; on a job path the dynamic
type could be PRendererForJobs, which shares the PRendererBase layout.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_REG
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
def ins(a, size=16): return list(cs.disasm(d[off(a):off(a) + size], a))
def at(a):
    x = ins(a)[0]; return "%s %s" % (x.mnemonic, x.op_str)
def target(a):
    x = ins(a)[0]; m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    return a + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
def q(v): return struct.unpack_from("<Q", d, off(v))[0]
def rtti(vt):
    td = BASE + struct.unpack_from("<IIII", d, off(q(vt - 8)))[3]; o = off(td + 16); return d[o:d.find(b"\0", o)].decode()
FAM = {"rsi": {"rsi", "esi", "si", "sil"}, "rdi": {"rdi", "edi", "di", "dil"}, "r10": {"r10", "r10d", "r10w", "r10b"},
       "rbp": {"rbp", "ebp", "bp", "bpl"}, "r14": {"r14", "r14d", "r14w", "r14b"}}
def writes(lo, hi, reg, skip=(0, 0)):
    """instructions strictly inside (lo, hi) that write reg (explicit destination, or a call clobbering a volatile);
    `skip` is a side branch that returns without rejoining, excluded only where the check proves that separately."""
    out = []
    for x in ins(lo, hi - lo):
        if not (lo < x.address < hi) or skip[0] <= x.address < skip[1]: continue
        if x.mnemonic == "call" and reg in ("r10",): out.append(x.address); continue
        try: _, w = x.regs_access()
        except Exception: w = []
        if any(x.reg_name(r) in FAM[reg] for r in w): out.append(x.address)
    return out
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
check("G1 0060B980: r14 = rcx; +0x08 bit 0 and +0x80 gate it; virtual slot 2 through [r14]",
      at(0x60B9D4) == "mov r14, rcx" and at(0x60B9D7) == "mov eax, dword ptr [rcx + 8]"
      and at(0x60B9EA) == "mov rax, qword ptr [rcx + 0x80]" and at(0x60BEB3) == "mov rax, qword ptr [r14]"
      and at(0x60BEB9) == "call qword ptr [rax + 0x10]" and writes(0x60B9D4, 0x60BEB3, "r14") == [])
names = {vt: rtti(vt) for vt in (0xD49930, 0xD498F0, 0xD49910)}
check("G2 RTTI names PRenderer / PRendererBase / PRendererForJobs; slot 2 shared by the first two, not the third",
      names[0xD49930] == ".?AVPRenderer@PRendering@Phyre@@" and names[0xD498F0].startswith(".?AVPRendererBase@")
      and names[0xD49910].startswith(".?AVPRendererForJobs@") and q(0xD49930 + 16) == q(0xD498F0 + 16) != q(0xD49910 + 16),
      str(names))
C = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in ins(0x5DC2F0, 0x100)}
rdi_is_this = any(v in ("mov rdi, rcx",) for a, v in C.items() if a < 0x5DC3DB)
check("G3 005DC2F0 installs 00D49930 and stores +0x08, +0x20 (rdx), +0x80, +0xA8 and +0x220 (rdi = this)",
      target(0x5DC375) == 0xD49930 and C.get(0x5DC37C) == "mov qword ptr [rcx], rax" and C.get(0x5DC312) == "mov qword ptr [rcx + 8], rsi"
      and C.get(0x5DC31D) == "mov qword ptr [rcx + 0x20], rdx" and C.get(0x5DC34B) == "mov qword ptr [rcx + 0x80], rsi"
      and C.get(0x5DC360) == "mov qword ptr [rcx + 0xa8], rsi" and C.get(0x5DC3DB) == "mov dword ptr [rdi + 0x220], esi" and rdi_is_this)
check("G4 the PApplication constructor 00792350 builds it at this + 0xE8",
      at(0x792414) == "lea rbp, [rcx + 0xe8]" and at(0x79241E) == "call 0x5dc2f0" and writes(0x792414, 0x79241E, "rbp") == []
      and rtti(target(0x792373)).startswith(".?AVPApplication@PFramework@Phyre@@"), rtti(target(0x792373)))
steps = [at(0x17D04F) == "lea rcx, [rbx + 0xe8]", at(0x17D06F) == "call 0x189000",
         at(0x189027) == "mov rbp, rcx", at(0x18905B) == "mov rdx, rbp", at(0x189061) == "call 0x184f20", writes(0x189027, 0x18905B, "rbp") == [],
         at(0x184F4C) == "mov qword ptr [rcx + 8], rdx", target(0x189067) == 0x1F7F598 and at(0x189067).endswith("rax"),
         at(0x1C2DD7) == "call 0x189120" and target(0x189120) == 0x1F7F598, at(0x1C2DDC) == "mov rsi, qword ptr [rax + 8]",
         at(0x1C2E1D) == "mov rdx, rsi", at(0x1C2E2A) == "call 0x1ea830", writes(0x1C2DDC, 0x1C2E1D, "rsi") == [],
         at(0x1EA84A) == "mov rdi, rdx", at(0x1EA916) == "mov rdx, rdi", at(0x1EA919) == "call 0x67c260", writes(0x1EA84A, 0x1EA916, "rdi") == [],
         at(0x67C26D) == "mov r10, rdx", at(0x67C2C2) == "mov qword ptr [r10 + 0x80], rcx", at(0x67C2EA) == "mov eax, dword ptr [r10 + 0x220]",
         at(0x67C2FD) == "mov rcx, r10", at(0x67C300) == "call 0x60b980",
         writes(0x67C26D, 0x67C2FD, "r10", skip=(0x67C28B, 0x67C2B0)) == [] and at(0x67C2AE) == "jmp 0x67c306"
         and at(0x67C27D) == "je 0x67c2b0" and at(0x67C289) == "jne 0x67c2b0"]
check("G5 the chain app+0xE8 -> 00189000 -> render singleton +8 -> 001C2DB0 -> 001EA830 -> 0067C260 -> 0060B980",
      all(steps), "failed steps %s" % [i for i, s in enumerate(steps) if not s])
late = writes(0x1C2DDC, 0x1C2F40, "rsi")
check("control: the write test flags rsi in 001C2DB0 once the window runs past its last use", late != [],
      "writes past the window %s" % ["%08X" % a for a in late[:3]])
print("FAILS", fails)
sys.exit(1 if fails else 0)
