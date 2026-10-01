"""rc4b_pass3.py - RC-4 residue, the escape E1 (ORACLE, 2026-09-30). Static.

0060CE50 stores view + 8 at [ext + 0xA8], where ext = [A+8]. Every function in the 0060xxxx-0061xxxx module that
loads a qword from [reg + 0xA8] is listed, and each is analysed with pass 2's closed flow (self fields, vtables,
seeds). Each argument register in turn carries a token C, and a load from C + 0xA8 yields the six view+8 pointers
(A + 0x28, 0x1B8, 0x360, 0x4F0, 0x698, 0x828). Any store the flow then finds covering A+0xDAC is printed.
Control: the module scan must find 0060CE50's own +0xA8 store site's readers set to be non-empty, and a seeded
0018A120-style body must be reached (0060CE50 itself, seeded with rdx = view + 8, must reach its [rdx + 0xB0] load).
"""
import contextlib, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import rc4b_pass2 as P  # noqa: E402  (installs the closed flow: self fields, vtable resolution, seeds)
K = P.K
R = P.R
VIEW8 = [0x28, 0x1B8, 0x360, 0x4F0, 0x698, 0x828]
_prev = K.load_value


def load_value(st, addr):
    if addr is not K.UNK and len(addr) == 1:
        (b, o), = addr
        if b == "C" and o == 0xA8:
            return frozenset(("A", k) for k in VIEW8)
    return _prev(st, addr)


K.load_value = load_value


def readers():
    out = []
    for f in sorted(K.ext):
        if not (0x00600000 <= f < 0x00620000):
            continue
        for i in R.md.disasm(R.at(f, K.ext[f]), f):
            if i.mnemonic == "mov" and i.op_str.startswith("r") and ", qword ptr [r" in i.op_str and i.op_str.endswith("+ 0xa8]") \
                    and "rsp" not in i.op_str:
                out.append((f, i.address))
    return out


def main():
    rd = readers()
    fns = sorted(set(f for f, _ in rd))
    print("functions loading [reg + 0xA8] in the module: %s" % " ".join("%08X" % f for f in fns))
    for it in range(1, 6):  # pass 2's self-field fixpoint, re-established here
        an = P.run_once()
        grow = {o: v for o, v in P.NEWSELF.items() if not v <= P.SELF.get(o, set())}
        if not grow:
            break
        for o, v in grow.items():
            P.SELF.setdefault(o, set()).update(v)
    print("self fields at the fixpoint: %d (after %d iteration(s))" % (len(P.SELF), it))
    base = set(h[1] for h in an.hits)
    C = K.vs(("C", 0))
    for f in fns:
        for reg in ("rcx", "rdx", "r8", "r9"):
            an.summary(f, ((reg, C),), 0, ())
    an.summary(0x0060CE50, (("rcx", C), ("rdx", K.vs(("A", 0x360)))), 0, ())
    # E2: 001F0AD0 calls [[ext] + 0x10] with rcx = ext and r8 = a view pair. ext = app + 0xE8, constructed by
    # 005DDBA0 (vtable 00D498F0) from 00793250 (0079334F), the base constructor 0017CC70 calls; slot 2 = 00600D20.
    e2 = P.u64(0x00D498F0 + 0x10)
    ok = e2 == 0x00600D20 and P.dis(0x005DDBA0, 0x10).get(0x005DDBA7) == ("mov", "qword ptr [rcx], rax")
    print("%s  E2 target: vtable 00D498F0 slot 2 = %08X" % ("PASS" if ok else "FAIL", e2))
    for pair in (0x358, 0x690):
        an.summary(e2, (("rcx", C), ("r8", K.vs(("A", pair)))), 0, ())
    hits = sorted(set(an.hits))
    new = [h for h in hits if h[1] not in base]
    print("%s  control: the flow reached 0060CE50 under rdx = view + 8" % ("PASS" if any(k[0] == 0x0060CE50 for k in an.memo) else "FAIL"))
    print("stores covering A+0xDAC before E1: %d; after seeding the readers: %d; NEW: %d" % (len(base), len(set(h[1] for h in hits)), len(new)))
    for h in new:
        print("  NEW %08X %08X %-40s base %-24s value %s" % h)
    ind = sorted(set(e for e in an.indirect if e[0] in fns or e[0] in (0x0060CE50, 0x00600D20)))
    print("unresolved indirect calls receiving the object inside the E1 readers: %d" % len(ind))
    for e in ind:
        print("  UNRESOLVED %08X %08X %-40s args %s" % e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
