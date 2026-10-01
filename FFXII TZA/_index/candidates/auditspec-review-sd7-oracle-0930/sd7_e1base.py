"""sd7_e1base.py - SWE2-AUDIT-SPEC, SD-7 review: sweep EVERY E1 row's load terms for a stack-derived base, not only the
rbp ones. For each `M` term [B+d], take the LAST write of B before the load on the aligned linear walk of the .pdata
chunk holding the load (a leaf without .pdata: back-decode). Stack-derived if that write is `mov B,rsp`,
`lea B,[rsp+k]`, or (for B = rbp) the prologue frame set-up `lea rbp,[rax-k]` with rax = entry rsp.
Positive control: the 8 rows of sd7_rbp.py must all come out stack-derived; negative control: 0074C790 / 00771B30
(rbp loaded from a stack slot = a pointer) must not.
A load in a secondary (chained) chunk whose base is not written in that chunk falls back to the root prologue
(sd7_rbp.prologue). Limit: the last write on the linear walk is not flow-aware (a join from another path is not seen)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import sd7_rbp as S  # noqa: E402
L = S.L
rows = json.load(open(os.path.join(HERE, "pkg_rows.json")))
E1 = [r for r in rows if r["class"] == "E1"]
stack, other, nowalk = [], 0, []
for r in E1:
    hit = []
    for t in r["terms"]:
        if t[0] != "M":
            continue
        la = int(t[1][:8], 16)
        mb = re.search(r"\[(\w+)", t[1])
        base = mb.group(1)
        if base in ("rip",) or "*" in t[1]:
            continue
        e = S.chunk(la)
        if e:
            ins = L.dis(S.IB + e[0], la + 16)
        else:
            ins = []
            for back in (0x80, 0x60, 0x40, 0x30):
                ii = L.dis(la - back, la + 16)
                if any(i.address == la for i in ii):
                    ins = ii
                    break
        if not any(i.address == la for i in ins):
            nowalk.append((r["site"], t[1]))
            continue
        w = [i for i in ins if i.address < la and base in S.writes(i)]
        last = w[-1] if w else None
        s = ("%s %s" % (last.mnemonic, last.op_str)) if last else "(none: incoming)"
        st = bool(last) and (re.match(r"(mov %s, rsp|lea %s, \[rsp)" % (base, base), s) is not None or
                             (base == "rbp" and re.match(r"lea rbp, \[rax - 0x", s) is not None and
                              "mov rax, rsp" in ["%s %s" % (i.mnemonic, i.op_str) for i in ins[:3]]))
        if not last and e and S.root(e) != e:
            # the load sits in a secondary (chained) chunk and the base is not written there: use the root prologue
            rt = S.root(e)
            val, tr = S.prologue(S.IB + rt[0], S.IB + rt[1])
            if base in val and base != "rsp":
                st = True
                s = "root %08X prologue: %s = entry%+#x" % (S.IB + rt[0], base, val[base])
        if st:
            hit.append("%s (last write %s)" % (t[1], ("%08X %s" % (last.address, s)) if last else s))
    if hit:
        stack.append((r["func"], r["site"], hit))
    else:
        other += 1
print("E1 rows %d: with a stack-derived load base %d, others %d; loads not on an aligned walk: %s" % (
    len(E1), len(stack), other, nowalk))
for x in stack:
    print("  %s %s %s" % (x[0], x[1], x[2]))
eight = {"00739C9D", "0073A753", "0073A894", "0073C4FF", "0073C56A", "0073E63A", "0073E8DC", "0073E9BE"}
got = {x[1] for x in stack}
print("positive control (8 rbp-frame rows all found): %s" % ("PASS" if eight <= got else "FAIL missing %s" % sorted(eight - got)))
print("negative control (0074C8EC / 0074CA3D / 00771C06 not found): %s" % (
    "PASS" if not ({"0074C8EC", "0074CA3D", "00771C06"} & got) else "FAIL"))
print("stack-derived rows beyond the 8: %s" % sorted(got - eight))
