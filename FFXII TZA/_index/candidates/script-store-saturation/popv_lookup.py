"""popv_lookup.py - POPV's call to 0032F240 is a read-only lookup whose result POPV discards (FABLE, Claude Opus 5.5, 2026-09-28, on
ASTRA-REQ-FABLE-SCRIPT-POPV-LOOKUP). Decoded from the certified image; nothing executed.

  L1 0032F240 (32 B) is closed: no call and no memory write; it reads the enable byte at 022C6D18 + i and, when set, returns the dword
     at 022C6D28 + 4i, else -1 (two ret)
  L2 POPV calls it (00267F2D) only when uint32(slot +0x28 - 1) <= 2 and esi == 0 (00267F1E..00267F2B); the next instructions are
     'lea rcx, [rsp + 0x30] / call 0026D530' with no read of eax between
  L3 the store 0026D530 does not read rax before 0026D53B 'mov eax, dword ptr [r9 + 0x18]' overwrites it - so on POPV's path the
     returned id is unused: POPV emits no notification and its store does not depend on the lookup
  C  control: the use test flags a planted 'mov dword ptr [rsp + 0x50], eax' after the call as a use of the returned value
  Not claimed: other callers' use of the id (the voice verbs use it), table values, writers, or reachability
"""
import hashlib, os, re, struct, sys
import capstone
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8": print("REFUSED  not the certified image"); sys.exit(2)
pe = struct.unpack_from("<I", d, 0x3c)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + 40 * i + 8) for i in range(ns)]
off = lambda v: next(ra + v - 0x120000 - va for vs, va, rs, ra in SECS if va <= v - 0x120000 < va + rs)
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
L = [(i.address, i.mnemonic, i.op_str) for i in MD.disasm(d[off(0x32F240):off(0x32F240) + 32], 0x32F240)]
writes = [x for x in L if x[1] in ("mov", "or", "and", "add") and x[2].split(",")[0].strip().endswith("]")]
ok("L1", len(L) == 8 and not any(m == "call" for a, m, o in L) and not writes and sum(1 for a, m, o in L if m == "ret") == 2
   and L[2][2] == "byte ptr [rax + rcx + 0x21a6d18], 0" and L[4][2] == "eax, dword ptr [rcx + rax*4 + 0x21a6d28]"
   and 0x32F243 + 7 - 0x20F24A + 0x21A6D18 == 0x22C6D18,
   "closed 32-byte body, no call, no write; enable byte 022C6D18 + i, id 022C6D28 + 4i, else -1")
P = [(i.address, (i.mnemonic + " " + i.op_str).strip()) for i in MD.disasm(d[off(0x267F1E):off(0x267F1E) + 0x1E], 0x267F1E)]
Pd = dict(P)
def uses_eax_after(seq, start):
    """first instruction after 'start' that reads eax/rax (as a source) - None if the path ends in a call that overwrites first."""
    after = [s for a, s in seq if a > start]
    for s in after:
        ops = s.split(None, 1)[1] if " " in s else ""
        parts = [p.strip() for p in ops.split(",")]
        if s.startswith("call"): return None
        srcs = parts[1:] if len(parts) > 1 else []
        if any(re.search(r"\b(e|r)ax\b", p) for p in srcs) or (parts and "[" in parts[0] and re.search(r"\b(e|r)ax\b", parts[0])): return s
    return None
ok("L2", Pd[0x267F1E] == "mov ecx, dword ptr [rdi + 0x28]" and Pd[0x267F21] == "lea eax, [rcx - 1]" and Pd[0x267F24] == "cmp eax, 2"
   and Pd[0x267F29] == "test esi, esi" and Pd[0x267F2D] == "call 0x32f240" and Pd[0x267F32] == "lea rcx, [rsp + 0x30]"
   and Pd[0x267F37] == "call 0x26d530" and uses_eax_after(P, 0x267F2D) is None,
   "gate uint32(+0x28 - 1) <= 2 and esi == 0; nothing reads eax between the lookup and the store call")
S4 = [(i.address, (i.mnemonic + " " + i.op_str).strip()) for i in MD.disasm(d[off(0x26D530):off(0x26D530) + 16], 0x26D530)][:4]
reads_before = [s for a, s in S4[:3] if re.search(r"\b(e|r)ax\b", s)]
ok("L3", S4[3] == (0x26D53B, "mov eax, dword ptr [r9 + 0x18]") and not reads_before,
   "0026D530's first three instructions do not touch rax; 0026D53B overwrites eax")
planted = P[:4] + [(0x267F32, "mov dword ptr [rsp + 0x50], eax")] + P[4:]
ok("C", uses_eax_after(planted, 0x267F2D) == "mov dword ptr [rsp + 0x50], eax", "a planted store of eax after the call is reported as a use")
print("FAILS", fails); sys.exit(1 if fails else 0)
