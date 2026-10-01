"""MXV / MXVW buffer alias and return residue (OPUS, 2026-09-27), consuming ASTRA's matrix-buffer-alias after a
non-author re-read. Static, certified EXE; the replay is a scalar MODEL of the leaf's instruction order, not a native run.
  L1 00217060 loads the four vector words (r8+0/+8/+0xC/+4) before its first store (002170CE)
  L2 matrix reads are interleaved with the stores: [rdx+8] is read at 002170FF after the store to [rcx] (002170CE);
     [rdx+0xC] is read at 00217104, before the store to [rcx+4] (0021710D)
  L3 replaying the leaf's own instruction order over a memory model: v = (1,2,3,1), m = diag(2,3,4) with last row
     (10,20,30,2): disjoint out gives (12,26,42,2); out = m + 8 gives (12,26,54,2); NEGATIVE control: a per-column
     reload model after each store is not what the body does and gives a different W
  W1 00202B70 passes a private rsp+0x20 as out, then copies 16 bytes to the caller's out (00202B83 / 00202B86) and never
     sets rax to the caller's out (rax = the leaf's out, 00217069)
  S  REGRESSION: the primitives page's MXV / MXVW rows state the alias hazard and the rax residue (FAILS before)
"""
import os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
d = open(os.path.join(os.path.dirname(DB), "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read(); B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
INS = list(cs.disasm(d[off(0x217060):off(0x217060) + 235], 0x217060))
X = {i.address: (i.mnemonic, i.op_str) for i in INS}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
first_store = min(i.address for i in INS if i.mnemonic == "movss" and i.op_str.startswith("dword ptr [rcx"))
vec = [i.address for i in INS if "[r8" in i.op_str]
check("L1 the four vector words are read before the first store", len(vec) == 4 and max(vec) < first_store == 0x2170CE, str(["%08X" % a for a in vec]))
check("L2 matrix reads interleave with stores (word 2 after the first store, word 3 before the second)",
      X[0x2170CE] == ("movss", "dword ptr [rcx], xmm2") and X[0x2170FF] == ("mulss", "xmm0, dword ptr [rdx + 8]")
      and X[0x217104] == ("mulss", "xmm4, dword ptr [rdx + 0xc]") and X[0x21710D] == ("movss", "dword ptr [rcx + 4], xmm3")
      and X[0x217069] == ("mov", "rax, rcx"))
def f32(x): return struct.unpack("<f", struct.pack("<f", x))[0]
def run(mem, regs, reload_after_store=False):
    x = {}
    def addr(s):
        m = re.match(r"(?:dword|xmmword) ptr \[(\w+)(?: \+ (0x[0-9a-f]+|\d+))?\]", s)
        return regs[m.group(1)] + (int(m.group(2), 0) if m.group(2) else 0)
    for i in INS:
        o = [p.strip() for p in i.op_str.split(",")] if i.op_str else []
        if i.mnemonic == "ret": break
        if (i.mnemonic in ("sub", "add") and o[0] == "rsp") or "rsp" in i.op_str: continue
        if i.mnemonic == "mov": regs[o[0]] = regs[o[1]]; continue
        if i.mnemonic in ("movss", "movaps"):
            if "ptr" in o[0]: mem[addr(o[0])] = x[o[1]]
            else: x[o[0]] = x[o[1]] if o[1].startswith("xmm") else mem.get(addr(o[1]), 0.0)
            continue
        v = x[o[1]] if o[1].startswith("xmm") else mem.get(addr(o[1]), 0.0)
        if i.mnemonic == "mulss": x[o[0]] = f32(x[o[0]] * v); continue
        if i.mnemonic == "addss": x[o[0]] = f32(x[o[0]] + v); continue
        raise SystemExit("unmodelled " + i.mnemonic)
def case(alias):
    M = [2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 10, 20, 30, 2]; V = [1, 2, 3, 1]; mem = {}
    for k, v in enumerate(M): mem[0x1000 + 4 * k] = float(v)
    for k, v in enumerate(V): mem[0x2000 + 4 * k] = float(v)
    ob = 0x1008 if alias else 0x3000
    run(mem, {"rcx": ob, "rdx": 0x1000, "r8": 0x2000, "rax": 0})
    return [mem[ob + 4 * k] for k in range(4)]
def column_reload_model(alias):
    # the WRONG model: each output column recomputed from the current memory after all earlier columns are stored
    M = [2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 10, 20, 30, 2]; V = [1, 2, 3, 1]; mem = {}
    for k, v in enumerate(M): mem[0x1000 + 4 * k] = float(v)
    ob = 0x1008 if alias else 0x3000
    for j in range(4):
        mem[ob + 4 * j] = sum(V[r] * mem[0x1000 + 4 * (4 * r + j)] for r in range(4))
    return [mem[ob + 4 * k] for k in range(4)]
dis, ali, wrong = case(False), case(True), column_reload_model(True)
check("L3 replay: disjoint (12,26,42,2), out = m+8 (12,26,54,2); the column-reload model differs",
      dis == [12, 26, 42, 2] and ali == [12, 26, 54, 2] and wrong != ali, "replay %s / %s, reload model %s" % (dis, ali, wrong))
Wr = [(i.mnemonic, i.op_str) for i in cs.disasm(d[off(0x202B70):off(0x202B70) + 31], 0x202B70)]
check("W1 the wrapper stages into rsp+0x20, copies 16 bytes after the leaf, and leaves rax on the temporary",
      Wr == [("push", "rbx"), ("sub", "rsp, 0x30"), ("mov", "rbx, rcx"), ("lea", "rcx, [rsp + 0x20]"), ("call", "0x217060"),
             ("movups", "xmm0, xmmword ptr [rax]"), ("movups", "xmmword ptr [rbx], xmm0"), ("add", "rsp, 0x30"), ("pop", "rbx"), ("ret", "")])
page = open(os.path.join(DB, "00-Engine-Core-Runtime", "Shared-Transform-Workbench", "the-two-transform-primitives.md"), encoding="utf-8").read()
rows = {r.split("|")[1].strip(): r for r in page.splitlines() if r.startswith("| `00217060`") or r.startswith("| `00202B70`")}
check("S the MXV / MXVW rows state the alias hazard and the rax residue",
      "OUTPUT MUST NOT OVERLAP THE MATRIX" in rows.get("`00217060`", "") and "RAX IS NOT THE CALLER'S OUT" in rows.get("`00202B70`", "")
      and all(r.count("|") == 4 for r in rows.values()))
print("FAILS", fails)
sys.exit(1 if fails else 0)
