"""sd7_slot15_callers.py - who calls GameApplication slot 15 (0017D1A0)? (OPUS, 2026-09-30; register SD-7)

Facts the census stands on, each re-read here:
  * the application is a static object at 01F7E350: 0015BC40 constructs it there (lea rcx, 01F7E350 / call 00792350,
    then stores vtable 008C5760 into [01F7E350] at 0015BC61);
  * vtable 008C5760 slot 15 (+0x78) is 0017D1A0; the base vtable 01CB2508 has the shared stub 005C5230 there.
Method: the OV-5/8 (d) value-flow engine (../ov58d-pointer-flow-0930/ov58d_flow.py, callees under their argument values)
with two tokens: APP (the object: `lea 01F7E350`, or rcx on entry to each of the application's own vtable methods) and
APPVT (a load of [APP + 0] or `mov reg, [01F7E350]`). A hit is an indirect call through [APPVT + 0x78] (slot 15).
Also listed: direct calls/jumps to 0017D1A0, every qword in the image equal to 0017D1A0's address (a vtable or table
entry naming it), and indirect calls through [APPVT + d] for every d (so the census's own reach is visible: slots
14, 17 and 20 from the window procedure 00798FF0 must appear - control W).
"""
import collections, os, struct, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ov58d-pointer-flow-0930"))
import ov58d_flow as F  # noqa: E402
K, X, R = F.K, F.X, F.R

APP_OBJ, VT, BASE_VT, SLOT15 = 0x01F7E350, 0x008C5760, 0x01CB2508, 0x0017D1A0
# The window procedure 00798FF0 takes the application from the window: on WM_CREATE from CREATESTRUCT.lpCreateParams
# (`mov r15, [rsi]`, rsi = lParam, 00799057), otherwise from GetWindowLongPtrA(hwnd, GWLP_USERDATA = -21) through the
# import slot 008C2880 (00799064). Every GetWindowLongPtrA result is taken as APP (an over-approximation: it can only
# add candidates), and the window procedure is rooted with lParam as CS, whose first qword is APP.
GWLP_IAT, WNDPROC = 0x008C2880, 0x00798FF0
# The window procedure's own slot calls (14 at 0079914C, 20 at 007993ED) go through the object held in the global
# 02EA5368, not through the window data: that global is the framework's application pointer, so a load of it is APP
# and every function referencing it is a root.
APP_PTR = 0x02EA5368
calls_by_slot = collections.defaultdict(set)     # slot -> {(fn, addr)}
CUR = []

K.has_actor = lambda v: v is not K.UNK and any(b in ("APP", "APPVT", "CS") for b, _ in v)

_memaddr = K.memaddr


def memaddr(st, m, ins):
    if m.base == X.X86_REG_RIP and ins.address + ins.size + m.disp == APP_OBJ:
        return K.vs(("APP", 0))
    return _memaddr(st, m, ins)


K.memaddr = memaddr
F.K.memaddr = memaddr
_load = K.load_value


def load_value(st, addr):
    if addr is not K.UNK and addr and all(b == "APP" and o == 0 for b, o in addr):
        return K.vs(("APPVT", 0))
    if addr is not K.UNK and addr and all(b == "CS" and o == 0 for b, o in addr):
        return K.vs(("APP", 0))
    if addr is not K.UNK and addr and all(b == "G%08X" % APP_PTR and o == 0 for b, o in addr):
        return K.vs(("APP", 0))
    return _load(st, addr)


K.load_value = load_value
F.K.load_value = load_value


class AppCensus(F.Census):
    def step(self, f, st, i, depth, stack, caller_writes):
        ops = i.operands
        if i.mnemonic in ("call", "jmp") and ops and ops[0].type == X.X86_OP_MEM and ops[0].mem.base not in (0, X.X86_REG_RIP):
            bv = st.r.get(K.fullname(ops[0].mem.base)[0], K.UNK)
            if bv is not K.UNK:
                for b, o in bv:
                    if b == "APPVT" and o is not None and ops[0].mem.index == 0:
                        calls_by_slot[(o + ops[0].mem.disp) // 8].add((CUR[-1] if CUR else f, i.address))
        res = super().step(f, st, i, depth, stack, caller_writes)
        if (i.mnemonic == "call" and ops and ops[0].type == X.X86_OP_MEM and ops[0].mem.base == X.X86_REG_RIP
                and i.address + i.size + ops[0].mem.disp == GWLP_IAT):
            res[1].r["rax"] = K.vs(("APP", 0))
        return res

    def run(self, f, ctx, depth, stack):
        CUR.append(f)
        try:
            return super().run(f, ctx, depth, stack)
        finally:
            CUR.pop()


def vtable(addr, n=31):
    return list(struct.unpack("<%dQ" % n, R.at(addr, 8 * n)))


def main():
    t0 = time.time()
    refs, calls = F.scan()
    F.globals_root.clear()
    vt, bvt = vtable(VT), vtable(BASE_VT)
    print("vtable 008C5760 slot 15 = %08X; base 01CB2508 slot 15 = %08X" % (vt[15], bvt[15]))
    direct = sorted(calls.get(SLOT15, ()))
    print("direct call/jmp to 0017D1A0: %d %s" % (len(direct), " ".join("%08X" % c for c in direct)))
    # every aligned qword in the image's data equal to 0017D1A0
    import pefile
    pe = pefile.PE(R.b.EXE, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    names = []
    for s in pe.sections:
        data = s.get_data()
        va = base + s.VirtualAddress
        for off in range(0, len(data) - 7, 8):
            if struct.unpack_from("<Q", data, off)[0] in (SLOT15, SLOT15 - 0x00120000 + base):
                names.append(va + off)
    print("qwords naming 0017D1A0 (image base %X): %s" % (base, " ".join("%X" % a for a in names)))
    an = AppCensus()
    roots = set(f for f, _, _ in refs.get(APP_OBJ, ())) | set(f for f, _, _ in refs.get(APP_PTR, ()))
    stores = sorted((f, a) for f, a, isload in refs.get(APP_PTR, ()) if not isload)
    print("references to the app-pointer global 02EA5368: %d functions; non-load references %s" % (
        len(set(f for f, _, _ in refs.get(APP_PTR, ()))), " ".join("%08X@%08X" % x for x in stores)))
    for f in sorted(roots):
        an.summary(f, (), 0, ())
    gw = sorted(set(f for f, _, _ in refs.get(GWLP_IAT, ())))
    for f in gw:
        an.summary(f, (), 0, ())
    an.summary(WNDPROC, (("r9", K.vs(("CS", 0))),), 0, ())
    print("GetWindowLongPtrA callers rooted: %s" % " ".join("%08X" % f for f in gw))
    methods = sorted(set(x for x in vt[:31] if 0x00120000 <= x < 0x00900000))
    for f in methods:
        an.summary(f, (("rcx", K.vs(("APP", 0))),), 0, ())
    print("roots: %d functions referencing 01F7E350 or 02EA5368, %d vtable methods run with rcx = APP; bodies reached %d (%.0f s)" % (
        len(roots), len(methods), len(an.fns), time.time() - t0))
    w = {14, 17, 20} <= set(s for s, xs in calls_by_slot.items() if any(a in (0x0079914C, 0x007995C2, 0x00799611, 0x007993ED) for _, a in xs))
    print("%s  W the window procedure's slot-14/17/20 calls are reached" % ("PASS" if w else "FAIL"))
    for s in sorted(calls_by_slot):
        print("slot %2d (+0x%02X): %s" % (s, s * 8, " ".join("%08X@%08X" % x for x in sorted(calls_by_slot[s]))))
    print("slot 15 callers found: %d" % len(calls_by_slot.get(15, ())))
    esc = sorted(set(an.escapes))
    print("escapes of the application pointer into memory (a holder the census does not follow): %d" % len(esc))
    for e in esc:
        print("  ESCAPE   %08X %08X %-46s to %s" % e)
    print("indirect calls with APP/APPVT not resolved to a slot: %d" % len(set(an.indirect)))
    for e in sorted(set(an.indirect)):
        print("  INDIRECT %08X %08X %-46s args %s" % e)
    print("elapsed %.0f s" % (time.time() - t0))
    return 0 if w else 1


if __name__ == "__main__":
    sys.exit(main())
