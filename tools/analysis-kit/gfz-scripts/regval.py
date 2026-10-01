"""regval.py - the set of values a register can hold at an instruction, walked backward over the function's CFG and into
its callers (OPUS, 2026-09-30; written for SD-166, the arena-push census).

  python -B regval.py FUNC SITE REG [--depth N]      e.g.  regval.py 00267BB0 00267BD4 rcx
  python -B regval.py --self-test

value_at(func, site, reg, depth) returns a set of terms for `reg` just before the instruction at `site`:
  ('C', n)      a constant
  ('M', text)   a memory load (address and operand), not followed
  ('R', target) the return value of a call, not followed
  ('U', why)    unresolved: an operation the walk does not model, a clobbering call, a missing caller, the depth limit

What it models (everything else that writes the register - by capstone's regs_access, so implicit writers such as
cdq, xchg, rep-prefixed string ops, one-operand mul/div and pop count - yields U):
  mov/movzx/movsx/movsxd of an immediate, a register or memory; xor r,r; lea [r +- k]; add/sub of an immediate;
  cmovCC (the union of both values); a call (rax -> R, other volatile registers -> U, non-volatile pass through).
Paths: fall-through and direct jump targets inside the function body (retool's sizes()); an edge `cmp R, imm` / `test R, R`
followed by je-taken or jne-not-taken pins R to that constant. Loops are cut (a node on the current path contributes
its other entries' values). Function arguments rcx/rdx/r8/r9 at entry are followed into every direct caller's call site.
It does not see indirect callers, callers through tail jumps into the middle of a body, or stack-passed arguments,
nor jump-table (indirect `jmp`) edges into a node that also has a direct predecessor (such a node gives no U), nor
jumps into the body from code outside its extent. `movzx`/`movsx` from an 8- or 16-bit register is treated as a copy
of the whole register, and a `cmp`/`test` on a sub-register pins the whole register.
(Limits added 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's review
Database/FFXII TZA/_index/candidates/auditspec-review-sd166-0930/REVIEW.md.)
"""
import argparse, re, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import retool as T  # noqa: E402

R, SZ, SC = T.R, T.sizes(), T.scan()
FAM = {}
for fam in (("rax", "eax", "ax", "al", "ah"), ("rbx", "ebx", "bx", "bl", "bh"), ("rcx", "ecx", "cx", "cl", "ch"),
            ("rdx", "edx", "dx", "dl", "dh"), ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"),
            ("rbp", "ebp", "bp", "bpl"), ("rsp", "esp", "sp", "spl")):
    for r in fam:
        FAM[r] = fam[0]
for n in range(8, 16):
    for suf in ("", "d", "w", "b"):
        FAM["r%d%s" % (n, suf)] = "r%d" % n
VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
ARGS = ["rcx", "rdx", "r8", "r9"]
IMM = re.compile(r"(0x[0-9a-f]+|\d+)$")
_fcache, _memo = {}, {}


def canon(r):
    return FAM.get(r)


def body(f):
    if f not in _fcache:
        ins = list(R.md.disasm(R.at(f, SZ.get(f, 0x400)), f))
        idx = {i.address: k for k, i in enumerate(ins)}
        preds = {k: [] for k in range(len(ins))}
        for k, i in enumerate(ins):
            m = i.mnemonic
            if k + 1 < len(ins) and m not in ("jmp", "ret", "int3"):
                preds[k + 1].append(k)
            if m.startswith("j") and re.match(r"0x[0-9a-f]+$", i.op_str) and int(i.op_str, 16) in idx:
                preds[idx[int(i.op_str, 16)]].append(k)
        _fcache[f] = (ins, idx, preds)
    return _fcache[f]


def ops(i):
    p = [o.strip() for o in i.op_str.split(",", 1)]
    return p[0], (p[1] if len(p) > 1 else None)


def writes(i):
    try:
        return {canon(R.md.reg_name(r)) for r in i.regs_access()[1]} - {None}
    except Exception:
        return set()


def edge_pin(f, p, k, reg):
    ins, idx, preds = body(f)
    j = ins[p]
    if j.mnemonic not in ("je", "jne") or p == 0:
        return None
    taken = bool(re.match(r"0x[0-9a-f]+$", j.op_str)) and int(j.op_str, 16) == ins[k].address and k != p + 1
    if not ((j.mnemonic == "je" and taken) or (j.mnemonic == "jne" and not taken and k == p + 1)):
        return None
    c = ins[p - 1]
    d, s = ops(c)
    if canon(d) != reg:
        return None
    if c.mnemonic == "cmp" and s and IMM.match(s):
        return int(s, 0)
    if c.mnemonic == "test" and s and canon(s) == reg:
        return 0
    return None


def val(f, k, reg, depth, onpath):
    ins, idx, preds = body(f)
    if not preds[k]:
        return entry(f, reg, depth) if k == 0 else {("U", "no predecessor %08X" % ins[k].address)}
    out = set()
    for p in preds[k]:
        pin = edge_pin(f, p, k, reg)
        if pin is not None:
            out.add(("C", pin))
            continue
        key = (f, p, reg, depth)
        if key in _memo:
            out |= _memo[key]
            continue
        if key in onpath:
            continue
        onpath.add(key)
        res = through(f, p, reg, depth, onpath)
        onpath.discard(key)
        _memo[key] = res
        out |= res
    return out


def through(f, p, reg, depth, onpath):
    """the value of reg just after instruction p"""
    ins, idx, preds = body(f)
    i = ins[p]
    m = i.mnemonic
    d, s = ops(i)
    if m == "call":
        if reg == "rax":
            return {("R", i.op_str)}
        if reg in VOLATILE:
            return {("U", "clobbered by the call at %08X" % i.address)}
        return val(f, p, reg, depth, onpath)
    if reg not in writes(i) and not (d and canon(d) == reg and m in ("mov", "movzx", "movsx", "movsxd", "lea", "xor")):
        return val(f, p, reg, depth, onpath)
    if canon(d) == reg:
        if m in ("mov", "movzx", "movsx", "movsxd"):
            if IMM.match(s):
                return {("C", int(s, 0))}
            if canon(s):
                return val(f, p, canon(s), depth, onpath)
            return {("M", "%08X %s" % (i.address, s))}
        if m == "xor" and s and canon(s) == reg:
            return {("C", 0)}
        if m == "lea":
            mm = re.match(r"\[(\w+)(?: ([+-]) (0x[0-9a-f]+|\d+))?\]$", s)
            if mm and canon(mm.group(1)):
                k = int(mm.group(3), 0) * (1 if mm.group(2) == "+" else -1) if mm.group(2) else 0
                return {("C", v[1] + k) if v[0] == "C" else ("U", "lea over %s" % (v,))
                        for v in val(f, p, canon(mm.group(1)), depth, onpath)}
            return {("U", "%08X lea %s" % (i.address, s))}
        if m.startswith("cmov"):
            return val(f, p, reg, depth, onpath) | (val(f, p, canon(s), depth, onpath) if canon(s) else {("M", s)})
        if m in ("add", "sub") and s and IMM.match(s):
            k = int(s, 0) * (1 if m == "add" else -1)
            return {("C", v[1] + k) if v[0] == "C" else ("U", "%s over %s" % (m, v)) for v in val(f, p, reg, depth, onpath)}
    return {("U", "%08X %s %s" % (i.address, m, i.op_str))}


def entry(f, reg, depth):
    if reg not in ARGS:
        return {("U", "entry %s of %08X" % (reg, f))}
    if depth <= 0:
        return {("U", "depth: argument %s of %08X" % (reg, f))}
    sites = SC["calls"].get(f, ())
    if not sites:
        return {("U", "argument %s of %08X: no direct caller" % (reg, f))}
    out = set()
    for cf, cs in sites:
        out |= value_at(cf, cs, reg, depth - 1)
    return out


def value_at(f, site, reg, depth=4):
    ins, idx, preds = body(f)
    if site not in idx:
        return {("U", "site %08X is not an instruction of %08X" % (site, f))}
    return val(f, idx[site], canon(reg), depth, set())


def self_test():
    cases = [((0x00267BB0, 0x00267BD4, "rcx"), {("C", 5), ("C", 13)}),   # two paths: jne over `mov ecx, edx`
             ((0x003DD4C0, 0x003DD5A1, "rcx"), {("C", 11)}),             # cmp eax, 2 / jne pins rax, then lea [rax + 9]
             ((0x0026FAD0, 0x0026FB22, "rcx"), {("C", 8)}),              # test rax, rax / jne pins 0, then lea [rax + 8]
             ((0x003E9F80, 0x003EA031, "rcx"), {("C", 2), ("C", 12)})]   # cmovne esi, eax
    bad = [(a, sorted(value_at(*a), key=str)) for a, want in cases if value_at(*a) != want]
    for a, got in bad:
        print("SELF-TEST FAIL %s -> %s" % (a, got))
    print("self-test %d/%d" % (len(cases) - len(bad), len(cases)))
    return not bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("func", nargs="?")
    ap.add_argument("site", nargs="?")
    ap.add_argument("reg", nargs="?")
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(0 if self_test() else 1)
    for v in sorted(value_at(int(a.func, 16), int(a.site, 16), a.reg, a.depth), key=str):
        print(v)
