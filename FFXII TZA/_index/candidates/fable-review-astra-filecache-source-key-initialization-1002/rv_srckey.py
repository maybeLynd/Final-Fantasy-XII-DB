"""rv_srckey.py - FABLE independent re-derivation for ASTRA packet filecache-source-key-initialization (50dd4cc33).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the earlier FABLE reviews).  Does not import
ASTRA's prove.py, capture drivers or the shared role adapter (reg_tracking.py).

Method: complete linear decode of the three bodies against .pdata, local CFGs from rvlib.Body, and a small
forward data-flow over each CFG that tracks registers as (object + k), (stack + k), (incoming argument) or
(constant).  The meet keeps only facts that agree on every incoming edge.  At a call the Win64 volatile
registers (rax rcx rdx r8-r11) are dropped; the nonvolatile ones are kept (normal-ABI premise).  Every memory
write is resolved against that state into a byte interval [off, off + width) on the object or the stack, so a
write through a biased alias (rcx = object + 20h) is placed correctly.  Dominance comes from the CFG.

The controls patch a private in-memory copy of the image.  Each one names the check that must fail, and the
boundary control names one that must NOT fail.  The exe on disk is never written.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, fam  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG  # noqa: E402

CTOR = (0x00597930, 0x0059796B)    # standalone source-record constructor
READER = (0x00597970, 0x00597A12)  # reader-object constructor
REBIND = (0x0059ED70, 0x0059EE0C)  # rebind
RESOLVER = 0x0059EE90
SLUG = "filecache-source-key-initialization"
MANIFEST_SHA = "d5cc7655d068357ee5bd9496b5674f82d4e4679d30d12356ba5411d8b713350e"
KEY_IN_FRAME = 0x28   # DWORD key field, frame-relative
VOLATILE = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
MASK = {1: 0xFF, 2: 0xFFFF, 4: 0xFFFFFFFF, 8: 0xFFFFFFFFFFFFFFFF}


class Rep(Report):
    def __init__(self, title):
        Report.__init__(self, title)
        self.n = 0
        self.failed = []

    def check(self, name, cond, detail=""):
        self.n += 1
        if not cond:
            self.failed.append(name)
        return Report.check(self, name, cond, detail)


# ---------------------------------------------------------------- symbolic data-flow
def _rsym(I, st, op):
    """Value of a register operand (with width) under state st."""
    name = I.ci.reg_name(op.reg)
    s = st.get(fam(name))
    if s is None:
        return None
    if op.size == 8:
        return s
    if s[0] == "c":
        return ("c", s[1] & MASK[op.size])
    if s[0] == "arg":
        return ("argpart", s[1], op.size)
    return None


def _addr(I, st, m):
    if m["index"] is not None or m["base"] is None:
        return None
    b = st.get(fam(m["base"]))
    if b is None or b[0] not in ("obj", "stk"):
        return None
    return (b[0], b[1] + m["disp"])


def transfer(I, st):
    """Return (new_state, writes) where writes = [(region, off, size, value)] measured with the IN state."""
    ci = I.ci
    m = I.mnemonic
    ops = ci.operands
    out = dict(st)
    writes = []
    for k, mm in enumerate(I.mems):
        if mm["write"] and m not in ("push", "call"):
            a = _addr(I, st, mm)
            val = None
            if m == "mov" and len(ops) == 2:
                if ops[1].type == X86_OP_REG:
                    val = _rsym(I, st, ops[1])
                elif ops[1].type == X86_OP_IMM:
                    val = ("c", ops[1].imm & MASK[mm["size"]])
            writes.append((a[0] if a else None, a[1] if a else None, mm["size"], val))
    dst = fam(ci.reg_name(ops[0].reg)) if ops and ops[0].type == X86_OP_REG else None
    dsz = ops[0].size if dst else 0
    handled = set()
    if m == "call":
        for r in VOLATILE:
            out.pop(r, None)
        handled.add("rsp")
    elif m == "push":
        s = st.get("rsp")
        out["rsp"] = ("stk", s[1] - 8) if s and s[0] == "stk" else None
        handled.add("rsp")
    elif m == "pop":
        s = st.get("rsp")
        out["rsp"] = ("stk", s[1] + 8) if s and s[0] == "stk" else None
        out.pop(dst, None)
        handled |= {"rsp", dst}
    elif m == "xor" and dst and ops[1].type == X86_OP_REG and fam(ci.reg_name(ops[1].reg)) == dst and dsz >= 4:
        out[dst] = ("c", 0)
        handled.add(dst)
    elif m == "mov" and dst and dsz >= 4:
        if ops[1].type == X86_OP_REG:
            v = _rsym(I, st, ops[1])
            out[dst] = v if (dsz == 8 or (v and v[0] == "c")) else None
        elif ops[1].type == X86_OP_IMM:
            out[dst] = ("c", ops[1].imm & MASK[dsz])
        else:
            out[dst] = None
        handled.add(dst)
    elif m in ("add", "sub") and dst and dsz == 8 and ops[1].type == X86_OP_IMM:
        s = st.get(dst)
        d = ops[1].imm if m == "add" else -ops[1].imm
        out[dst] = (s[0], s[1] + d) if s and s[0] in ("obj", "stk") else None
        handled.add(dst)
    elif m == "lea" and dst and dsz == 8:
        a = _addr(I, st, I.mems[0])
        out[dst] = a
        handled.add(dst)
    for r in I.reg_writes:
        if r in handled or r in ("rflags", "rip"):
            continue
        out.pop(r, None)
    return dict((k, v) for k, v in out.items() if v is not None), writes


def dataflow(B):
    entry = {"rcx": ("obj", 0), "rsp": ("stk", 0),
             "rdx": ("arg", "rdx"), "r8": ("arg", "r8"), "r9": ("arg", "r9")}
    IN = {B.start: entry}
    work = [B.start]
    while work:
        a = work.pop()
        o, _ = transfer(B[a], IN[a])
        for s in B.succ(a):
            if s not in IN:
                IN[s] = dict(o)
                work.append(s)
            else:
                meet = dict((k, v) for k, v in IN[s].items() if o.get(k) == v)
                if meet != IN[s]:
                    IN[s] = meet
                    work.append(s)
    W = []
    for a in B.order:
        if a in IN:
            for w in transfer(B[a], IN[a])[1]:
                W.append((a,) + w)
    return IN, W


# ---------------------------------------------------------------- CFG helpers
def preds(B):
    p = {}
    for a in B.order:
        for s in B.succ(a):
            p.setdefault(s, set()).add(a)
    return p


def on_paths(B, src, dst):
    fwd = B.reach(src, avoid=[dst])
    P = preds(B)
    back, st = set(), [dst]
    while st:
        a = st.pop()
        for q in P.get(a, ()):
            if q not in back:
                back.add(q)
                st.append(q)
    return fwd & back


def overl(off, size, lo, hi):
    return off is not None and off < hi and lo < off + size


def resolver_calls(B):
    return [a for a, t in B.calls() if t == RESOLVER]


def fmtw(w):
    a, reg, off, size, val = w
    return "%X %s+%Xh/%d=%s" % (a, reg, off if off is not None else -1, size, val)


# ---------------------------------------------------------------- checks
def body_checks(img, R, Bs):
    tot = 0
    for name, (s, e) in (("CTOR", CTOR), ("READER", READER), ("REBIND", REBIND)):
        B = Bs[name]
        ents, ok = img.pdata_cover(s, e)
        R.check("B1 body %08X..%08X (%d B) decodes exactly and .pdata tiles it (%d record(s))" % (s, e, e - s, len(ents)),
                B.exact and ok)
        rets, tails, outs = B.exits()
        R.check("B2 %08X local CFG closed: no tail/out branch, single ret is the last instruction" % s,
                not tails and not outs and rets == [B.order[-1]], "rets=%s tails=%s outs=%s" % (
                    [hex(x) for x in rets], tails, outs))
        R.check("B3 %08X is bounded by int3 on both sides" % s,
                img.read(s - 1, 1) == b"\xcc" and img.read(e, 1) == b"\xcc")
        tot += e - s
    R.check("B4 three complete bodies total 377 B (59 + 162 + 156)", tot == 377, str(tot))


def ctor_like(img, R, B, tag, key_off, bias, carrier, store_at):
    """Shared checks for the two constructors.  key_off = object offset of the key DWORD."""
    IN, W = dataflow(B)
    rc = resolver_calls(B)
    R.check("%s1 %08X makes exactly one resolver call, and it is the body's first call" % (tag, B.start),
            len(rc) == 1 and B.calls()[0][0] == rc[0],
            str([(hex(a), hex(t) if t else None) for a, t in B.calls()]))
    if not rc:
        return None
    call = rc[0]
    zs = [w for w in W if w[1] == "obj" and w[2] == key_off and w[3] == 4 and w[4] == ("c", 0)]
    R.check("%s2 a DWORD constant-0 store to object+%Xh..%Xh exists" % (tag, key_off, key_off + 3),
            len(zs) >= 1, "; ".join(fmtw(w) for w in zs))
    dom = [w for w in zs if B.dominates(w[0], call)]
    R.check("%s3 that zero store dominates the resolver call %X (every entry path passes it)" % (tag, call),
            len(dom) >= 1, "; ".join(fmtw(w) for w in dom))
    path = on_paths(B, B.start, call)
    prefix = set(a for a in B.order if a < call)
    R.check("%s4 entry -> call is straight-line: the on-path set equals the linear prefix (%d insns)" % (tag, len(prefix)),
            path == prefix, "extra=%s missing=%s" % (sorted(hex(x) for x in path - prefix),
                                                    sorted(hex(x) for x in prefix - path)))
    later = [w for w in W if w[0] in path and (not dom or w[0] > dom[0][0]) and
             (w[1] in (None, "obj") and (w[1] is None or overl(w[2], w[3], key_off, key_off + 4)))]
    R.check("%s5 no write after the zero store and before the call overlaps object+%Xh..%Xh (and none is unresolved)" % (
        tag, key_off, key_off + 3), not later and dom, "; ".join(fmtw(w) for w in later))
    if dom:
        sa = dom[0][0]
        I = B[sa]
        src = I.ci.operands[1]
        srcn = fam(I.ci.reg_name(src.reg)) if src.type == X86_OP_REG else None
        wr = [a for a in B.order if a < sa and srcn in B[a].reg_writes]
        R.check("%s6 zero carrier: %s is written before %X only by %X `%s`" % (tag, carrier, sa, store_at[1],
                                                                          store_at[2]),
                srcn == carrier and wr == [store_at[1]] and B[store_at[1]].text == store_at[2] and sa == store_at[0],
                "src=%s writers=%s" % (srcn, [hex(x) for x in wr]))
    else:
        R.check("%s6 zero carrier" % tag, False, "no dominating zero store")
    rcx = IN[call].get("rcx")
    R.check("%s7 rcx at the resolver call = object + %Xh (frame bias)" % (tag, bias), rcx == ("obj", bias), str(rcx))
    other = [w for w in W if (w[1] is None or (w[1] == "obj" and overl(w[2], w[3], key_off, key_off + 4)))
             and not (dom and w[0] == dom[0][0])]
    R.check("%s8 whole body: no other write (before or after the call) overlaps object+%Xh..%Xh, none unresolved" % (
        tag, key_off, key_off + 3), not other and dom, "; ".join(fmtw(w) for w in other))
    return {"IN": IN, "W": W, "call": call, "rcx": rcx}


def frame_pattern(W, call, bias):
    """Pre-call object writes rebased to the resolver frame (frame offset, width, value-kind)."""
    out = []
    for a, reg, off, size, val in W:
        if a < call and reg == "obj" and off is not None and off >= bias:
            kind = val if (val and val[0] == "c") else ("arg" if val and val[0].startswith("arg") else None)
            out.append((off - bias, size, kind))
    return sorted(out)


def rebind_checks(img, R, B):
    IN, W = dataflow(B)
    rc = resolver_calls(B)
    calls = B.calls()
    R.check("F1 %08X's first call is the resolver %08X, and it is unconditional (dominates the ret)" % (B.start, RESOLVER),
            rc and calls and calls[0][0] == rc[0] and B.dominates(rc[0], B.order[-1]),
            str([(hex(a), hex(t) if t else None) for a, t in calls]))
    if not rc:
        return None
    call = rc[0]
    path = on_paths(B, B.start, call)
    pre_obj = [w for w in W if w[0] in path and w[1] != "stk"]
    pre_stk = [w for w in W if w[0] in path and w[1] == "stk"]
    R.check("F2 no object write (and no unresolved write) on any entry -> %X path; stack writes only" % call,
            not pre_obj, "; ".join(fmtw(w) for w in pre_obj))
    R.check("F3 the pre-call stack writes are the caller's home slots entry SP+8h..+27h",
            all(w[1] == "stk" and 8 <= w[2] and w[2] + w[3] <= 0x28 for w in pre_stk) and len(pre_stk) == 4,
            "; ".join(fmtw(w) for w in pre_stk))
    rcx = IN[call].get("rcx")
    R.check("F4 rcx at the resolver call = object + 20h (rebind frame bias)", rcx == ("obj", 0x20), str(rcx))
    unres = [w for w in W if w[1] is None]
    R.check("F5 every memory write in the whole body resolves to object or stack (none unresolved)", not unres,
            "; ".join(fmtw(w) for w in unres))
    hit = [w for w in W if w[1] == "obj" and overl(w[2], w[3], 0x48, 0x4C)]
    R.check("F6 no write anywhere in the body overlaps object+48h..4Bh (full byte intervals)", not hit and not unres,
            "; ".join(fmtw(w) for w in hit))
    objw = [(w[0], w[2], w[3]) for w in W if w[1] == "obj"]
    exp = [(0x59ED9F, 0x08, 4), (0x59EDCE, 0x10, 8), (0x59EDE3, 0x1C, 4), (0x59EDF0, 0x18, 4), (0x59EDF5, 0x1C, 4)]
    R.check("F7 the object writes are exactly five: +8h/4, +10h/8, +1Ch/4, +18h/4, +1Ch/4 (spans 8h..0Ch, 10h..20h)",
            objw == exp, str([(hex(a), hex(o), s) for a, o, s in objw]))
    R.check("F8 all five object writes lie after the resolver call",
            objw and all(a > call for a, o, s in objw) and all(a not in path for a, o, s in objw))
    return {"IN": IN, "W": W, "call": call, "rcx": rcx}


def resolver_note(img, R):
    """Beyond the packet: the resolver treats frame+28h as an out slot (pointer passed in r9)."""
    s, e = img.pdata(RESOLVER)
    B = Body(img, s, e)
    IN, W = dataflow(B)
    leas = [a for a in B.order if B[a].mnemonic == "lea" and a in IN and
            B[a].mems and _addr(B[a], IN[a], B[a].mems[0]) == ("obj", KEY_IN_FRAME)]
    direct = [w for w in W if w[1] == "obj" and overl(w[2], w[3], KEY_IN_FRAME, KEY_IN_FRAME + 4)]
    R.check("R1 resolver %08X (%d B, .pdata) forms frame+28h once, as `lea r9, [r15 + 0x28]`, and no store in its"
            " body resolves to frame+28h..2Bh" % (RESOLVER, e - s),
            B.exact and leas and all(B[a].text == "lea r9, [r15 + 0x28]" for a in leas) and not direct,
            "lea at %s; direct=%s" % ([hex(a) for a in leas], [fmtw(w) for w in direct]))
    nx = []
    for a in leas:
        i = B.order.index(a) + 1
        while B[B.order[i]].mnemonic != "call":
            i += 1
        nx.append((hex(a), hex(B[B.order[i]].direct_target() or 0)))
    R.note("resolver frame+28h address sites -> next call: %s" % nx)


def checks(img, R):
    Bs = dict((n, Body(img, s, e)) for n, (s, e) in (("CTOR", CTOR), ("READER", READER), ("REBIND", REBIND)))
    body_checks(img, R, Bs)
    c = ctor_like(img, R, Bs["CTOR"], "C", 0x28, 0x00, "rax", (0x597951, 0x597936, "xor eax, eax"))
    d = ctor_like(img, R, Bs["READER"], "D", 0x48, 0x20, "rbp", (0x5979A3, 0x597984, "xor ebp, ebp"))
    f = rebind_checks(img, R, Bs["REBIND"])
    # claim 3: alignment
    kc = (0x28 - c["rcx"][1]) if c and c["rcx"] and c["rcx"][0] == "obj" else None
    kd = (0x48 - d["rcx"][1]) if d and d["rcx"] and d["rcx"][0] == "obj" else None
    kf = (0x48 - f["rcx"][1]) if f and f["rcx"] and f["rcx"][0] == "obj" else None
    R.check("E1 key field in resolver-frame terms: record+28h - bias 0 = reader+48h - bias 20h = rebind+48h - bias 20h = 28h",
            kc == kd == kf == KEY_IN_FRAME, "%s %s %s" % (kc, kd, kf))
    if c and d:
        pc = frame_pattern(c["W"], c["call"], 0)
        pd = frame_pattern(d["W"], d["call"], 0x20)
        R.check("E2 corroboration: the reader's pre-call writes at object+20h.. rebased by -20h equal the record "
                "constructor's six pre-call writes (offset, width, constant/argument)", pc == pd and len(pc) == 6,
                "record=%s reader-20h=%s" % (pc, pd))
    else:
        R.check("E2 initializer pattern", False)
    # claim 5: composition (conditional)
    names = ("C2", "C3", "C4", "C5", "C7", "D2", "D3", "D4", "D5", "D7", "E1", "F1", "F2", "F4", "F6")
    bad = [x for x in R.failed if x.split(" ")[0] in names]
    R.check("G1 composition: both constructors enter the resolver with frame+28h = 0; rebind enters it with frame+28h "
            "untouched by its own code (conditional on ABI / valid distinct object / no interference)", not bad, str(bad))
    resolver_note(img, R)


def capture_bytes(img, R):
    """The packet's captured range hashes must equal this image's bytes (kept out of checks() so that a patched
    control image cannot fail on this alone)."""
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    src = json.load(open(os.path.join(ev, "source-01.json")))
    mism, rng = [], []
    for r in src["ranges"]:
        s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
        rng.append((s_, e_))
        if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"]:
            mism.append(r["start"])
    R.check("packet's three captured range sha256 values equal this image's bytes, and its ranges are the three "
            ".pdata bodies", not mism and sorted(rng) == sorted([CTOR, READER, REBIND]) and
            src["exe_sha256"] == img_sha(img), "%s %s" % (mism, [(hex(a), hex(b)) for a, b in rng]))


def img_sha(img):
    return hashlib.sha256(img.d).hexdigest()


NOP3 = bytes.fromhex("0F1F00")
# (label, [(va, bytes)], check ids that must fail, check ids that must NOT fail)
CONTROLS = [
    ("597951 key store +28h -> +2Ch", [(0x597953, b"\x2C")], ["C2"], []),
    ("597951 DWORD store -> byte store (`mov [rcx+0x28], al`)", [(0x597951, b"\x88")], ["C2"], []),
    ("597936 `xor eax, eax` -> `mov al, 1` (nonzero carrier)", [(0x597936, bytes.fromhex("B001"))], ["C2"], []),
    ("move the record zero store after the call: 597951 nop, 597962 -> `mov dword [rbx+0x28], 0`",
     [(0x597951, NOP3), (0x597962, bytes.fromhex("C7432800000000"))], ["C3"], ["C2"]),
    ("597949 -> `jmp 597954` + nops (a path skips the zero store)", [(0x597949, bytes.fromhex("EB09") + b"\x90" * 6)],
     ["C3", "C4"], []),
    ("597954 byte store +18h -> +28h (overwrites the key after the zero store)", [(0x597957, b"\x28")], ["C5"], []),
    ("5979A3 reader +48h zero store removed (nop)", [(0x5979A3, NOP3)], ["D2"], []),
    ("597984 `xor ebp, ebp` -> `or ebp, ebp` (carrier keeps caller's rbp)", [(0x597984, bytes.fromhex("0BED"))],
     ["D2"], []),
    ("5979B2 reader bias `add rcx, 0x20` -> 0x24", [(0x5979B5, b"\x24")], ["D7", "E1"], []),
    ("59ED90 rebind bias `add rcx, 0x20` -> 0x28", [(0x59ED93, b"\x28")], ["F4", "E1"], []),
    ("59ED94 -> `mov [rcx+0x28], ebp` (direct key reset through the biased pointer before the call)",
     [(0x59ED94, bytes.fromhex("896928"))], ["F2", "F6"], []),
    ("59ED9F `mov [rdi+8], eax` -> `mov [rdi+0x48], eax` (rebind writes the key)", [(0x59EDA1, b"\x48")], ["F6"], []),
    ("59EDCE qword store +10h -> +41h (8-byte span 41h..48h reaches the key)", [(0x59EDD1, b"\x41")], ["F6"], []),
    ("boundary: 59EDCE qword store +10h -> +40h (span 40h..47h is adjacent, must not be flagged)",
     [(0x59EDD1, b"\x40")], ["F7"], ["F6"]),
]


def run_controls(img, R):
    Rn = Rep("null")
    Rn.quiet = True
    checks(img.patched(CTOR[0], img.read(CTOR[0], 2)), Rn)
    R.check("null control: an unchanged private copy (sha check off) passes every check", Rn.fails == 0 and Rn.n > 0,
            "%d of %d" % (Rn.n - Rn.fails, Rn.n))
    n = 0
    for label, patches, must, mustnot in CONTROLS:
        P = img
        for va, nb in patches:
            P = P.patched(va, nb)
        if P.d == img.d:
            raise SystemExit("control did not change the image: " + label)
        Rc = Rep(label)
        Rc.quiet = True
        try:
            checks(P, Rc)
            ids = [x.split(" ")[0] for x in Rc.failed]
            ok = all(m in ids for m in must) and not any(m in ids for m in mustnot)
            why = "failed %s; required fail %s%s" % (sorted(set(ids)), must,
                                                     ("; required pass " + str(mustnot)) if mustnot else "")
        except Exception as e:
            ok = False
            why = "exception %r" % e
        n += 1
        R.check("control: " + label, ok, why)
    return n


def main():
    img = Img.load()
    R = Rep("rv_srckey")
    print("== packet integrity")
    check_manifest(R, SLUG, MANIFEST_SHA)
    print("== shipping-image re-derivation (image base %X, sha %s)" % (img.base, img_sha(img)))
    checks(img, R)
    capture_bytes(img, R)
    print("== controls (each patched private image must FAIL its named check(s))")
    nctl = run_controls(img, R)
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))
    # data used in REVIEW.md
    for name, (s, e) in (("CTOR", CTOR), ("READER", READER), ("REBIND", REBIND)):
        IN, W = dataflow(Body(img, s, e))
        print("WRITES %08X: %s" % (s, "; ".join(fmtw(w) for w in W)))


if __name__ == "__main__":
    main()
