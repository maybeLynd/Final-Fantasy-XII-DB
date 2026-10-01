"""sd7_rbp.py - SWE2-AUDIT-SPEC, SD-7 review: settle the E1 rbp-frame defect with numbers.

Defect named: the package's e1() exempts only rsp-based loads ("the stack" is one of OPUS's holders), so a load through
a FRAME POINTER rbp (a stack slot) is treated as a holder displacement and excluded. Instrument:

  R1  for every E1 row whose regval term is an rbp-based load (11 rows, pkg_rows.json), and for the 7 rows the first
      probe (sd7_indep.py C) flagged through rcx/rax/r8, emulate the prologue of the .pdata root with the lane loader:
      track rsp-relative values (push / sub rsp / mov r,rsp / lea r,[r+k]) from entry (entry rsp = 0, return address
      at +0); then check rbp (or the base register) is not rewritten between its set-up and the load (linear walk of
      the chunk holding the load). A base that resolves to entry+k is a stack slot: k >= +8 is the caller's frame
      (+8..+0x20 home area, +0x28 and up stack-passed arguments), k < 0 is the function's own local.
      Negative control: 0074C790 (rbp loaded from [rsp+0x188], a pointer) must come out NOT a frame base; positive
      control: 00739C9D (read by hand, rbp = entry-0x58) must come out a stack slot.
  R2  re-classify each stack-slot row with the package's own E2/E3/E4 functions (runpy of the package, stdout
      discarded, nothing written in the package dir): the corrected partition.
"""
import bisect, contextlib, io, json, os, re, runpy, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as L  # noqa: E402

IB = L.IB
dd = L.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = L.off(IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", L.raw, o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def chunk(va):
    j = bisect.bisect_right(ST, va - IB) - 1
    return PD[j] if j >= 0 and PD[j][0] <= va - IB < PD[j][1] else None


def root(e):
    while True:
        uo = L.off(IB + e[2])
        if not (L.raw[uo] >> 3) & 4:
            return e
        cnt = L.raw[uo + 2]
        e = struct.unpack_from("<III", L.raw, uo + 4 + ((cnt + 1) & ~1) * 2)


FAM = {}
for r64, subs in {"rax": "eax ax al ah", "rbx": "ebx bx bl bh", "rcx": "ecx cx cl ch", "rdx": "edx dx dl dh",
                  "rsi": "esi si sil", "rdi": "edi di dil", "rbp": "ebp bp bpl", "rsp": "esp sp spl"}.items():
    for s in [r64] + subs.split():
        FAM[s] = r64
for n in range(8, 16):
    for s in ("r%d" % n, "r%dd" % n, "r%dw" % n, "r%db" % n):
        FAM[s] = "r%d" % n


def writes(i):
    try:
        _, w = i.regs_access()
    except Exception:
        return set()
    return {FAM.get(i.reg_name(r), i.reg_name(r)) for r in w}


def prologue(fstart, stop):
    """emulate from entry to the first branch/call or `stop`; return {reg: entry-relative offset} and the trace"""
    val = {"rsp": 0}
    tr = []
    for i in L.dis(fstart, fstart + 0x100):
        if i.address >= stop or i.mnemonic.startswith("j") or i.mnemonic in ("call", "ret"):
            break
        ops = i.op_str.replace(" ", "")
        m = None
        if i.mnemonic == "push":
            val["rsp"] -= 8
        elif i.mnemonic == "sub" and re.match(r"rsp,(0x[0-9a-f]+|\d+)$", ops):
            val["rsp"] -= int(ops.split(",")[1], 0)
        elif i.mnemonic == "mov" and re.match(r"(\w+),(\w+)$", ops) and ops.split(",")[1] in val:
            d, s = ops.split(",")
            val[FAM.get(d, d)] = val[s]
        elif i.mnemonic == "lea" and re.match(r"(\w+),(?:qwordptr)?\[(\w+)([+-]0x[0-9a-f]+|[+-]\d+)?\]$", ops):
            m = re.match(r"(\w+),(?:qwordptr)?\[(\w+)([+-]0x[0-9a-f]+|[+-]\d+)?\]$", ops)
            if m.group(2) in val:
                val[m.group(1)] = val[m.group(2)] + (int(m.group(3), 0) if m.group(3) else 0)
            else:
                val.pop(m.group(1), None)
        else:
            for w in writes(i):
                if w != "rsp":
                    val.pop(w, None)
        tr.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
    return val, tr


def rewritten(reg, frm, to):
    """writes of reg on the linear walk of the chunk holding `to`, between max(frm, chunk start) and `to`"""
    e = chunk(to)
    a = IB + e[0]          # decode from the chunk start (aligned), count only writes after the set-up instruction
    return ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in L.dis(a, to)
            if reg in writes(i) and frm < i.address < to]


rows = json.load(open(os.path.join(HERE, "pkg_rows.json")))
FLAG7 = {"00623B8D", "00623BEA", "00764FA1", "00765020", "00767BC6", "00767D51", "0078E4C1"}
targets = [r for r in rows if r["class"] == "E1" and (any("[rbp" in t[1] for t in r["terms"]) or r["site"] in FLAG7)]
print("== R1. %d E1 rows examined (11 rbp-based terms + the 7 first-probe flags)" % len(targets))
stack_rows = []
for r in targets:
    mt = [t for t in r["terms"] if t[0] == "M"]
    verdicts = []
    for t in mt:
        la = int(t[1][:8], 16)
        base = re.search(r"\[(\w+)", t[1]).group(1)
        disp = re.search(r"([+-] 0x[0-9a-f]+)\]", t[1])
        disp = int(disp.group(1).replace(" ", ""), 16) if disp else 0
        e = chunk(la)
        if not e:
            verdicts.append("%s: no .pdata" % t[1])
            continue
        rt = root(e)
        f0 = IB + rt[0]
        val, tr = prologue(f0, la)
        if base in val and base != "rsp":
            k = val[base]
            # find the instruction that set base in the prologue, then walk to the load for rewrites
            setter = [x for x in tr if re.match(r"\w+ (lea|mov) %s," % base, x)]
            sa = int(setter[-1][:8], 16) if setter else f0 - 1
            rw = rewritten(base, sa, la)
            slot = k + disp
            where = ("caller frame, home area" if 8 <= slot <= 0x20 else "caller frame, stack-passed argument"
                     if slot >= 0x28 else "own local" if slot < 0 else "return address?")
            verdicts.append("%s: %s = entry%+#x (set %s), slot entry%+#x = %s; %s rewrites before the load: %s" % (
                t[1], base, k, setter[-1][9:] if setter else "?", slot, where, base, rw or "none"))
            if not rw:
                stack_rows.append((r, slot, where))
        else:
            verdicts.append("%s: %s not rsp-derived in the prologue of %08X (prologue: %s)" % (
                t[1], base, f0, " | ".join(x[9:] for x in tr[:8])))
    print("  %s %s obj=%s terms=%s" % (r["func"], r["site"], r["obj"], r["terms"]))
    for v in verdicts:
        print("      " + v)
print("  stack-slot rows (base rsp-derived, not rewritten): %d" % len(stack_rows))
print("  negative control: 0074C790 rows among stack-slot rows: %d (must be 0: rbp is loaded from [rsp+0x188])" % sum(1 for r, _, _ in stack_rows if r["func"] == "0074C790"))
print("  positive control: 00739C9D (read by hand: rbp = entry-0x58) among stack-slot rows: %s (must be True)" % any(r["site"] == "00739C9D" for r, _, _ in stack_rows))

print("== R2. re-classify the stack-slot rows with the package's own E2/E3/E4")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    g = runpy.run_path(os.path.join(HERE, "..", "sd7-stored-app-pointer-0930", "sd7_app_pointer_sites.py"), run_name="__pkg__")
bysite = {"%08X" % a: (f, a, ld, obj, terms) for f, a, ld, obj, terms in g["rows"]}
moved = {"E2": 0, "E3": 0, "E4": 0, "RESIDUE": 0}
for r, slot, where in stack_rows:
    f, a, ld, obj, terms = bysite[r["site"]]
    assert g["e1"](terms)
    if g["e2"](terms):
        c = "E2"
    elif g["e3"](terms):
        c = "E3"
    else:
        ds = g["slot_disps"](f, ld.address, obj) if ld is not None and obj else []
        big = [x for x in ds if x[1] >= 31 * 8]
        c = "E4" if big else "RESIDUE"
    moved[c] += 1
    print("  %s %s slot entry%+#x (%s) -> %s" % (r["func"], r["site"], slot, where, c))
cnt = dict(re.findall(r"'(\w+)': (\d+)", buf.getvalue().split("classes: ")[1].splitlines()[0]))
cnt = {k: int(v) for k, v in cnt.items()}
n = len(stack_rows)
print("  package partition: %s" % cnt)
corr = dict(cnt)
corr["E1"] -= n
for k, v in moved.items():
    corr[k] = corr.get(k, 0) + v
print("  corrected partition (E1 without the %d stack-slot rows): %s; excluded total %d of %d" % (
    n, corr, sum(v for k, v in corr.items() if k != "RESIDUE"), sum(corr.values())))
