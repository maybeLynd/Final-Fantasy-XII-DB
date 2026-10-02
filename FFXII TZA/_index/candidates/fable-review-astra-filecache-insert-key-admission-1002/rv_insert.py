"""rv_insert.py - FABLE independent re-derivation for ASTRA packet filecache-insert-key-admission (1b2154feb).

Own reader (rvlib.py: struct + capstone 5).  Does not import ASTRA's prove.py, capture drivers or the shared
role adapter (reg_tracking.py).  Method: complete linear decode of the seven bodies against .pdata (the leaf
16D840 has no .pdata record, so it is bounded by its closed CFG, its final ret and int3 padding on both sides),
local CFGs from rvlib.Body, exact frame arithmetic, register-write censuses for every key carrier, flag-consumer
checks for every key comparison, and an identification of every 16-byte copy site.  The controls patch a
private in-memory copy of the image and require at least one named check to fail.
"""
import hashlib
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe  # noqa: E402

ENTRY = (0x001D6A20, 0x001D6A6D)
INS = (0x0020B680, 0x0020B83B)
PREP = (0x0020B5F0, 0x0020B675)
HINT = (0x001AE9B0, 0x001AEAFC)
UNIQ = (0x001AE850, 0x001AE9A8)
TAIL = (0x0020BA70, 0x0020BB0C)
BAL = (0x0016D840, 0x0016DA54)
GETTER = 0x0020C700
REPL = 0x0020C300
SLUG = "filecache-insert-key-admission"
MANIFEST_SHA = "6efd33a9b850a11bdded356cc64cc04ae411f5f5f75d52e2bbb75edd790f874d"

UNSIGNED = {"jb", "jae", "jbe", "ja", "je", "jne", "setb", "setae", "setbe", "seta", "sete", "setne"}
VALUE_OPS = {"and", "or", "xor", "btr", "bts", "btc", "shl", "shr", "sar", "sal", "rol", "ror", "rcl", "rcr",
             "imul", "mul", "add", "sub", "neg", "not", "movzx", "movsx", "movsxd", "crc32", "bswap", "inc", "dec",
             "lea", "cmovne", "cmove", "xchg", "bzhi", "pext", "andn"}


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


def writers(B, fam, lo=None, hi=None):
    return [a for a in B.order if fam in B[a].reg_writes and (lo is None or lo <= a) and (hi is None or a < hi)]


def preds(B):
    p = {}
    for a in B.order:
        for s in B.succ(a):
            p.setdefault(s, set()).add(a)
    return p


def on_paths(B, src, dst):
    """Instructions on some path src -> dst that does not pass dst first (dst excluded)."""
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


def flag_consumer(B, a):
    i = B.order.index(a) + 1
    while i < len(B.order):
        I = B[B.order[i]]
        if I.mnemonic.startswith("j") or I.mnemonic.startswith("set") or I.mnemonic.startswith("cmov"):
            return I
        if I.mnemonic in ("cmp", "test", "add", "sub", "and", "or", "xor", "inc", "dec", "call", "ret"):
            return None
        i += 1
    return None


def bodies(img):
    return {k: Body(img, *r) for k, r in (("entry", ENTRY), ("ins", INS), ("prep", PREP), ("hint", HINT),
                                         ("uniq", UNIQ), ("tail", TAIL), ("bal", BAL))}


def T(B, a):
    I = B.ins.get(a)
    return I.text if I else "<no boundary>"


def checks(img, R):
    Bs = bodies(img)
    E, N, P, H, U, TL, BL = (Bs[k] for k in ("entry", "ins", "prep", "hint", "uniq", "tail", "bal"))

    # ---------------- bodies ----------------
    tot1 = tot2 = 0
    for k, (s, e) in (("entry", ENTRY), ("ins", INS), ("prep", PREP), ("hint", HINT), ("uniq", UNIQ), ("tail", TAIL)):
        ents, ok = img.pdata_cover(s, e)
        R.check("body %08X..%08X (%d B) decodes exactly and .pdata tiles it (%d record(s))" % (s, e, e - s, len(ents)),
                Bs[k].exact and ok)
        if k in ("entry", "ins", "prep"):
            tot1 += e - s
        else:
            tot2 += e - s
    s, e = BAL
    pad_after = img.read(e, 0x0016DA60 - e)
    R.check("leaf %08X..%08X (%d B) decodes exactly; no .pdata covers it; int3 padding on both sides; next .pdata "
            "begins 0016DA60" % (s, e, e - s),
            BL.exact and img.pdata(s) is None and img.pdata(e - 1) is None and img.read(s - 1, 1) == b"\xcc" and
            pad_after == b"\xcc" * len(pad_after) and img.pdata(0x0016DA60) == (0x0016DA60, 0x0016DDC3))
    tot2 += e - s
    R.check("capture-01 bodies total 653 B (77 + 443 + 133)", tot1 == 653, str(tot1))
    R.check("capture-02 bodies total 1364 B (332 + 344 + 156 + 532)", tot2 == 1364, str(tot2))
    for k in ("entry", "ins", "prep", "hint", "uniq", "tail", "bal"):
        rets, tails, outs = Bs[k].exits()
        R.check("%08X local CFG closed: no tail/out branch, single ret is the last instruction" % Bs[k].start,
                not tails and not outs and rets == [Bs[k].order[-1]], "rets=%s tails=%s outs=%s" % (rets, tails, outs))

    # ---------------- claim 1: 1D6A20 ----------------
    R.check("1D6A20 carriers: ebx=r9d, edi=r8d, rsi=rdx, ebp=ecx before the getter call",
            [T(E, a) for a in (0x1D6A34, 0x1D6A37, 0x1D6A3A, 0x1D6A3D, 0x1D6A3F)] ==
            ["mov ebx, r9d", "mov edi, r8d", "mov rsi, rdx", "mov ebp, ecx", "call 0x%x" % GETTER])
    R.check("1D6A20 getter result is the receiver: rcx = rax at 1D6A44, no rcx write before call 20B680",
            T(E, 0x1D6A44) == "mov rcx, rax" and writers(E, "rcx", 0x1D6A45, 0x1D6A53) == [] and
            T(E, 0x1D6A53) == "call 0x20b680")
    R.check("1D6A20 forwards: [rsp+20h]=ebx (kind32), r9d=edi (value32), r8=rsi (64-bit pointer), edx=ebp (key32)",
            [T(E, a) for a in (0x1D6A47, 0x1D6A4B, 0x1D6A4E, 0x1D6A51)] ==
            ["mov dword ptr [rsp + 0x20], ebx", "mov r9d, edi", "mov r8, rsi", "mov edx, ebp"])
    R.check("1D6A20 key carriers: ebp written only at 1D6A3D (+ epilogue restore), edx only at 1D6A51",
            writers(E, "rbp") == [0x1D6A3D, 0x1D6A5D] and writers(E, "rdx") == [0x1D6A51],
            "rbp %s rdx %s" % ([hex(a) for a in writers(E, "rbp")], [hex(a) for a in writers(E, "rdx")]))
    R.check("1D6A20 no value-changing op (and/btr/shift/arith) on rcx/rbp/rdx anywhere in the body",
            not [a for a in E.order if E[a].mnemonic in VALUE_OPS and E[a].reg_writes & {"rbp", "rdx"}] and
            not [a for a in E.order if a < 0x1D6A3D and "rcx" in E[a].reg_writes])
    fr = 0
    for a in E.order:
        if a >= 0x1D6A53:
            break
        if E[a].mnemonic == "push":
            fr += 8
        elif E[a].text.startswith("sub rsp, "):
            fr += E[a].imm[0]
    R.check("1D6A20 [rsp+20h] at the call is the callee's entry SP+28h (fifth argument); frame 38h",
            fr == 0x38 and 0x20 + 8 == 0x28)
    dst = [E[a].op_str.split(",")[0] for a in (0x1D6A34, 0x1D6A37, 0x1D6A3A, 0x1D6A3D)]
    R.check("1D6A20 the four incoming carriers land in four distinct callee-saved registers, none rewritten "
            "before its forward", len({E[a].reg_writes.copy().pop() for a in (0x1D6A34, 0x1D6A37, 0x1D6A3A, 0x1D6A3D)}) == 4
            and all(not writers(E, f, s0 + 1, 0x1D6A53) for f, s0 in (("rbx", 0x1D6A34), ("rdi", 0x1D6A37),
                                                                       ("rsi", 0x1D6A3A), ("rbp", 0x1D6A3D))), str(dst))

    # ---------------- claim 2: 20B680 ----------------
    R.check("20B680 entry: `mov dword ptr [rsp + 0x10], edx` before any push (key home = entry SP+10h, 4 B)",
            E is not None and T(N, 0x20B680) == "mov dword ptr [rsp + 0x10], edx" and N[0x20B680].mems[0]["size"] == 4)
    fr, pushes = 0, 0
    a = 0x20B684
    while a <= 0x20B68F:
        I = N[a]
        if I.mnemonic == "push":
            fr += 8
            pushes += 1
        elif I.text == "sub rsp, 0x40":
            fr += 0x40
        a += I.size
    R.check("20B680 prologue: seven pushes + sub 40h = 78h", pushes == 7 and fr == 0x78, "%d %X" % (pushes, fr))
    rspw = [x for x in N.order if "rsp" in N[x].reg_writes and N[x].mnemonic not in ("call",)]
    R.check("20B680 rsp changed only by the prologue and epilogue (no alloca)",
            all(x <= 0x20B68F or x >= 0x20B82B for x in rspw), str([hex(x) for x in rspw]))
    R.check("key home current SP+88h = entry SP+10h; fifth arg current SP+A0h = entry SP+28h",
            0x88 - fr == 0x10 and 0xA0 - fr == 0x28)
    R.check("20B680 ebp = edx at 20B6AA; ebp written nowhere else but the epilogue pop",
            T(N, 0x20B6AA) == "mov ebp, edx" and writers(N, "rbp") == [0x20B6AA, 0x20B839],
            str([hex(x) for x in writers(N, "rbp")]))
    R.check("20B680 r12 = r8 (pointer), r14d = r9d (value32); each written once (+ epilogue)",
            T(N, 0x20B6A7) == "mov r12, r8" and T(N, 0x20B6A4) == "mov r14d, r9d" and
            writers(N, "r12") == [0x20B6A7, 0x20B835] and writers(N, "r14") == [0x20B6A4, 0x20B831])
    kcmp = [x for x in N.order if N[x].mnemonic == "cmp" and "rbp" in N[x].reg_reads]
    bad = [(hex(x), N[x].text, (flag_consumer(N, x) or N[x]).mnemonic) for x in kcmp
           if not (flag_consumer(N, x) and flag_consumer(N, x).mnemonic in UNSIGNED and
                   N[x].mems and N[x].mems[0]["size"] == 4 and N[x].mems[0]["disp"] == 0x20)]
    R.check("20B680 every key compare is a DWORD cmp against node+20h with an unsigned consumer (%d found)" % len(kcmp),
            len(kcmp) == 2 and not bad, str(bad))
    R.check("20B680 existing-key test: rbx==header -> new; `cmp ebp,[rbx+20h]` jae keeps rbx (equal key)",
            T(N, 0x20B6DE) == "cmp rbx, rcx" and T(N, 0x20B6E3) == "cmp ebp, dword ptr [rbx + 0x20]" and
            T(N, 0x20B6E6) == "jae 0x20b6eb" and T(N, 0x20B6EF) == "cmp rbx, rax" and T(N, 0x20B6F2) == "je 0x20b73f")
    ex = N.reach(0x20B6F4)
    R.check("existing-key arm: 20C300 gets edx = ebp (20B721), rcx = receiver, fifth = kind from SP+A0h",
            (0x20B726, REPL) in [(x, N[x].direct_target()) for x in ex if N[x].mnemonic == "call"] and
            T(N, 0x20B721) == "mov edx, ebp" and T(N, 0x20B723) == "mov rcx, rsi" and
            T(N, 0x20B70F) == "mov eax, dword ptr [rsp + 0xa0]" and T(N, 0x20B716) == "mov dword ptr [rsp + 0x20], eax"
            and not writers(N, "rdx", 0x20B722, 0x20B726))
    R.check("existing-key arm never calls 20B5F0", 0x20B5F0 not in [N[x].direct_target() for x in ex])
    R.check("new arm: 20B7D0 `lea rdx, [rsp + 0x88]` (key home) then call 20B5F0 with rcx = receiver+20h",
            T(N, 0x20B7D0) == "lea rdx, [rsp + 0x88]" and T(N, 0x20B7D8) == "lea rcx, [rsi + 0x20]" and
            N[0x20B7DC].direct_target() == 0x20B5F0)
    path = on_paths(N, N.start, 0x20B7DC)
    over = []
    for x in path:
        if x == 0x20B680:
            continue
        for m in N[x].mems:
            if m["write"] and m["base"] == "rsp" and N[x].mnemonic != "lea":
                if m["disp"] < 0x8C and m["disp"] + m["size"] > 0x88:
                    over.append((hex(x), N[x].text))
    R.check("no own stack write overlapping key home 88h..8Bh on any entry -> 20B7DC path (%d insns)" % len(path),
            not over, str(over))
    R.note("stack writes on that path: %s" % sorted("%X %s" % (x, N[x].text) for x in path
                                                    for m in N[x].mems if m["write"] and m["base"] == "rsp"))
    R.check("new arm is gated on the 1BA860 result: `test rax,rax; je 20B7E4` skips 20B5F0",
            N[0x20B746].direct_target() == 0x1BA860 and T(N, 0x20B758) == "test rax, rax" and
            T(N, 0x20B75B) == "je 0x20b7e4" and 0x20B7DC not in N.reach(0x20B7E4))
    R.check("after 20B5F0: `mov qword ptr [rax], rbx` stores the descriptor pointer through the returned slot",
            T(N, 0x20B7E1) == "mov qword ptr [rax], rbx")

    # ---------------- claim 3: 20B5F0 ----------------
    kr = [(x, m["size"]) for x in P.order for m in P[x].mems if m["base"] == "rdx" and m["disp"] == 0]
    R.check("20B5F0 reads the key only as full DWORDs through rdx (20B607, 20B62F, 20B633)",
            [x for x, s in kr] == [0x20B607, 0x20B62F, 0x20B633] and all(s == 4 for x, s in kr),
            str([(hex(x), s) for x, s in kr]))
    R.check("20B5F0 rdx never rewritten before the call", writers(P, "rdx", P.start, 0x20B649) == [])
    R.check("20B5F0 r9 written only at 20B607 (key load) and 20B635 (pair address)",
            writers(P, "r9") == [0x20B607, 0x20B635], str([hex(x) for x in writers(P, "r9")]))
    R.check("20B5F0 compares are unsigned: 20B610 cmp [r8+20h],r9d -> jb; 20B62F cmp [rdx],ecx -> jae",
            T(P, 0x20B610) == "cmp dword ptr [r8 + 0x20], r9d" and T(P, 0x20B614) == "jb 0x20b61f" and
            T(P, 0x20B62C) == "mov ecx, dword ptr [rax + 0x20]" and T(P, 0x20B62F) == "cmp dword ptr [rdx], ecx" and
            T(P, 0x20B631) == "jae 0x20b66c" and
            all(flag_consumer(P, x).mnemonic in UNSIGNED for x in P.order if P[x].mnemonic == "cmp"))
    R.check("20B5F0 pair: ecx = [rdx] (20B633), [rsp+30h] = ecx (20B64E), qword [rsp+38h] = 0 (20B659); no rcx "
            "write between", T(P, 0x20B633) == "mov ecx, dword ptr [rdx]" and
            T(P, 0x20B64E) == "mov dword ptr [rsp + 0x30], ecx" and
            T(P, 0x20B659) == "mov qword ptr [rsp + 0x38], 0" and writers(P, "rcx", 0x20B634, 0x20B64E) == [])
    pw = [(x, m["disp"], m["size"]) for x in P.order for m in P[x].mems if m["write"] and m["base"] == "rsp"]
    R.check("20B5F0 stack writes are 50h/8, 30h/4, 20h/1, 38h/8 only (pair+4..+7 is never written)",
            sorted((d, s) for x, d, s in pw) == [(0x20, 1), (0x30, 4), (0x38, 8), (0x50, 8)], str(pw))
    R.check("20B5F0 passes the pair: r9 = rsp+30h, rcx = map, rdx = out rsp+60h, then call 1AE9B0",
            T(P, 0x20B635) == "lea r9, [rsp + 0x30]" and T(P, 0x20B652) == "mov rcx, r10" and
            T(P, 0x20B649) == "lea rdx, [rsp + 0x60]" and P[0x20B662].direct_target() == HINT[0])
    R.check("20B5F0 returns out-node + 28h; 20B66C is also the target of the existing-key jae (find-or-insert)",
            T(P, 0x20B667) == "mov rax, qword ptr [rsp + 0x60]" and T(P, 0x20B66C) == "add rax, 0x28" and
            P[0x20B631].direct_target() == 0x20B66C)

    # ---------------- claim 4: copy sites ----------------
    pairreg = {"hint": ("r14", 0x1AE9CB, "mov r14, r9"), "uniq": ("r15", 0x1AE874, "mov r15, r8"),
               "tail": ("rbp", 0x20BA8D, "mov rbp, r9")}
    sites = []
    loads = stores = 0
    for k, B in (("hint", H), ("uniq", U), ("tail", TL)):
        reg, at, txt = pairreg[k]
        for x in B.order:
            for m in B[x].mems:
                if m["size"] == 16:
                    if m["write"]:
                        stores += 1
                    else:
                        loads += 1
            if B[x].mnemonic == "movups" and B[x].mems and not B[x].mems[0]["write"]:
                sites.append((k, x))
        R.check("%s pair register %s set once from the incoming pair arg (`%s` at %X) + epilogue restore" %
                (B.start and "%08X" % B.start, reg, txt, at),
                T(B, at) == txt and [w for w in writers(B, reg) if B[w].mnemonic != "pop" and
                                     not (B[w].mnemonic == "mov" and B[w].mems and B[w].mems[0]["base"] == "rsp")] == [at],
                str([hex(w) for w in writers(B, reg)]))
    R.check("exactly five 16-byte loads and five 16-byte stores in 1AE9B0/1AE850/20BA70", loads == 5 and stores == 5,
            "%d loads %d stores" % (loads, stores))
    good = []
    for k, x in sites:
        B = Bs[k]
        reg = pairreg[k][0]
        idx = B.order.index(x)
        ld, st = B[x], B[B.order[idx + 1]]
        jz, addi, mvn, call = (B[B.order[idx - j]] for j in (1, 2, 3, 4))
        ld_ok = ld.mems[0]["base"] == reg and ld.mems[0]["disp"] == 0 and not ld.mems[0]["index"]
        st_ok = st.mnemonic == "movups" and st.mems and st.mems[0]["write"] and st.mems[0]["base"] == "rax" and \
            st.mems[0]["disp"] == 0 and st.mems[0]["size"] == 16
        node = mvn.op_str.split(",")[0] if mvn.mnemonic == "mov" and mvn.op_str.endswith(", rax") else None
        guard = addi.text == "add rax, 0x20" and jz.mnemonic == "je" and jz.direct_target() == st.address + st.size
        alloc = call.text == "call qword ptr [rax + 0x10]" and \
            [B[B.order[idx - j]].text for j in (6, 5)] == ["xor r8d, r8d", "lea edx, [r8 + 0x30]"]
        # node register reaches 16D840 as rcx with no rewrite
        nxt = [y for y in B.order if y > st.address and B[y].mnemonic == "call"][0]
        ok_bal = B[nxt].direct_target() == BAL[0] and any(B[y].text == "mov rcx, %s" % node for y in B.order
                                                           if st.address < y < nxt)
        ok_reg = not writers(B, reg, B.start + 1, x) or writers(B, reg, B.start, x) == [pairreg[k][1]]
        good.append((k, x, ld_ok and st_ok and guard and alloc and ok_bal and ok_reg and bool(node)))
        R.note("copy site %X/%X in %08X: `%s` ; `%s`; node %s; guard `%s`/`%s`; alloc 30h; then %s(rcx=%s)" %
               (x, st.address, B.start, ld.text, st.text, node, addi.text, jz.text, "%X" % B[nxt].direct_target(), node))
    R.check("all five copy sites load [pair+0] 16 B and store to fresh 30h node+20h (guard skips only when "
            "node+20h == 0), node then passed to 16D840",
            len(good) == 5 and all(g for k, x, g in good), str([(k, hex(x), g) for k, x, g in good]))
    R.check("copy sites are 1AEA28, 1AEAA4 (1AE9B0), 1AE91A, 1AE95B (1AE850), 20BAD1 (20BA70)",
            sorted(x for k, x in sites) == sorted([0x1AEA28, 0x1AEAA4, 0x1AE91A, 0x1AE95B, 0x20BAD1]))
    R.check("1AE9B0 forwards the same pair: `mov r9, r14` -> 20BA70; `mov r8, r14` -> 1AE850",
            T(H, 0x1AEA4B) == "mov r9, r14" and H[0x1AEA59].direct_target() == TAIL[0] and
            T(H, 0x1AEAD4) == "mov r8, r14" and H[0x1AEADA].direct_target() == UNIQ[0])
    nw = []
    for k, B in (("hint", H), ("uniq", U), ("tail", TL)):
        for x in B.order:
            for m in B[x].mems:
                if m["write"] and m["base"] == pairreg[k][0]:
                    nw.append((k, hex(x)))
    R.check("no write through a pair register in the three bodies", not nw, str(nw))
    kc = []
    for k, B in (("hint", H), ("uniq", U), ("tail", TL)):
        for x in B.order:
            I = B[x]
            if I.mnemonic == "cmp" and I.mems and I.mems[0]["size"] == 4:
                c = flag_consumer(B, x)
                kc.append((k, x, c.mnemonic if c else None))
    R.check("every DWORD key compare in the three tree bodies has an unsigned consumer (%d)" % len(kc),
            kc and all(c in UNSIGNED for k, x, c in kc), str([(k, hex(x), c) for k, x, c in kc if c not in UNSIGNED]))
    R.check("1AE9B0/1AE850/20BA70 write no node+20h..2Fh after the copy (only [map+28h] inc, out slot, flag)",
            not [(k, hex(x)) for k, B in (("hint", H), ("uniq", U), ("tail", TL)) for x in B.order
                 for m in B[x].mems if m["write"] and m["base"] not in ("rsp", "rax") and 0x20 <= m["disp"] < 0x30
                 and not (B[x].mnemonic == "inc" and m["disp"] == 0x28 and m["base"] in ("rdi", "rbp", "rbx"))])
    R.check("1AE850 existing-key exit 1AE97F stores the found node with flag 0 and makes no copy",
            T(U, 0x1AE97F) == "mov qword ptr [rsi], rbx" and T(U, 0x1AE982) == "mov byte ptr [rsi + 8], 0" and
            not [x for x in U.reach(0x1AE97F) if U[x].mnemonic in ("movups", "call")])

    # ---------------- claim 5: 16D840 ----------------
    R.check("16D840 has no call, no indirect jump and no rsp use",
            not BL.calls() and not [x for x in BL.order if BL[x].mnemonic.startswith("j") and
                                    BL[x].direct_target() is None] and
            not [x for x in BL.order if "rsp" in BL[x].reg_reads | BL[x].reg_writes and BL[x].mnemonic != "ret"])
    bw = [(x, m) for x in BL.order for m in BL[x].mems if m["write"]]
    R.check("every 16D840 write is [reg+disp] with no index and lies in 0h..19h (%d writes)" % len(bw),
            bw and all(m["index"] is None and m["base"] in ("rcx", "rdx", "r8", "r9", "rax") and 0 <= m["disp"] and
                       m["disp"] + m["size"] <= 0x19 for x, m in bw),
            str([("%X" % x, m["base"], m["disp"], m["size"]) for x, m in bw if m["disp"] + m["size"] > 0x19]))
    R.note("16D840 write spans: %s" % sorted({(m["disp"], m["disp"] + m["size"]) for x, m in bw}))
    R.check("16D840 initialises the new node (rcx): +10h = parent rdx, +0/+8 = 0, byte +18h = 0",
            [T(BL, a) for a in (0x16D840, 0x16D842, 0x16D846, 0x16D849, 0x16D84D)] ==
            ["xor eax, eax", "mov qword ptr [rcx + 0x10], rdx", "mov qword ptr [rcx], rax",
             "mov qword ptr [rcx + 8], rax", "mov byte ptr [rcx + 0x18], al"])

    # ---------------- beyond the packet: the two tree-step callees reached before a copy ----------------
    steps = []
    for s0, e0, call_sites in ((0x16D6D0, 0x16D714, ((H, 0x1AE9E5),)), (0x16D720, 0x16D77E, ((U, 0x1AE8C3),))):
        S = Body(img, s0, e0)
        rets, tails, outs = S.exits()
        pad = img.read(e0, 2)
        steps.append(S.exact and not tails and not outs and S.order[-1] in rets and pad == b"\xcc\xcc" and
                     not S.calls() and not S.mem_writes() and img.pdata(s0) is None and
                     all(B[c].direct_target() == s0 for B, c in call_sites))
    R.check("16D6D0 (68 B) and 16D720 (94 B), the only direct callees before a copy site, are read-only leaves "
            "(no call, no memory write)", all(steps), str(steps))
    pre = []
    for k, B in (("hint", H), ("uniq", U), ("tail", TL)):
        for k2, x in [(kk, xx) for kk, xx in [(k, y) for y in B.order] if B[xx].mnemonic == "movups" and
                      B[xx].mems and not B[xx].mems[0]["write"]]:
            for c in on_paths(B, B.start, x):
                if B[c].mnemonic == "call":
                    pre.append((B.start, c, B[c].direct_target()))
    fw = sorted({(c, H[c].direct_target()) for d in (0x1AEA59, 0x1AEADA) for c in on_paths(H, H.start, d)
                 if H[c].mnemonic == "call"})
    R.check("1AE9B0 entry -> its 20BA70 / 1AE850 forwards passes no call but 16D6D0 (1AE9E5)",
            fw == [(0x1AE9E5, 0x16D6D0)], str(fw))
    R.check("calls on any entry -> copy-site path: the 30h allocator callback and 16D6D0 / 16D720 only",
            all(t in (None, 0x16D6D0, 0x16D720) and (t is not None or B_text_is_alloc(Bs, s, c))
                for s, c, t in pre), str([("%X" % s, "%X" % c, t) for s, c, t in pre]))


def B_text_is_alloc(Bs, start, c):
    B = [b for b in Bs.values() if b.start == start][0]
    i = B.order.index(c)
    return B[c].text == "call qword ptr [rax + 0x10]" and B[B.order[i - 1]].text == "lea edx, [r8 + 0x30]"


def capture_bytes(img, R):
    """The packet's captured range hashes must equal this image's bytes (kept out of checks() so that a
    patched control image cannot fail on this alone)."""
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    mism = []
    nr = 0
    for f in ("source-01.json", "source-02.json"):
        for r in json.load(open(os.path.join(ev, f)))["ranges"]:
            s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
            nr += 1
            if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"]:
                mism.append(r["start"])
    R.check("packet's seven captured range sha256 values equal this image's bytes", nr == 7 and not mism, str(mism))


CONTROLS = [
    ("20B60A alignment nop -> `btr r9d, 31` (mask the key in 20B5F0)", 0x20B60A, bytes.fromhex("410FBAF11F90")),
    ("1D6A51 `mov edx, ebp` -> `mov edx, edi` (forward value32 as key)", 0x1D6A51, bytes.fromhex("8BD7")),
    ("20B6AA `mov ebp, edx` -> `and ebp, edx`", 0x20B6AA, bytes.fromhex("23EA")),
    ("20B6CB unsigned jb -> signed jl", 0x20B6CB, bytes([0x7C])),
    ("20B614 unsigned jb -> signed jl", 0x20B614, bytes([0x7C])),
    ("20B680 key home [rsp+10h] -> [rsp+14h]", 0x20B683, bytes([0x14])),
    ("20B7D0 `lea rdx,[rsp+88h]` -> [rsp+8Ch]", 0x20B7D4, bytes([0x8C])),
    ("20B74E descriptor spill [rsp+80h] -> [rsp+84h] (overlaps key home)", 0x20B752, bytes([0x84])),
    ("20B659 pair+8 seed [rsp+38h] -> [rsp+40h]", 0x20B65D, bytes([0x40])),
    ("1AEA22 copy store node+20h -> node+18h", 0x1AEA25, bytes([0x18])),
    ("1AE91A copy loads [r14] (node) instead of the pair [r15]", 0x1AE91D, bytes([0x06])),
    ("16D84D colour byte store +18h -> +20h", 0x16D84F, bytes([0x20])),
    ("16D885 alignment nop -> call 16D6D0 (+6 nop)", 0x16D885, None),
    ("20B66C returned slot +28h -> +20h", 0x20B66F, bytes([0x20])),
    ("16D6D0 `mov rax, rcx` -> `mov qword ptr [rcx], rax` (step helper writes)", 0x16D6D0, bytes.fromhex("488901")),
]


def main():
    img = Img.load()
    R = Rep("rv_insert")
    print("== packet integrity")
    check_manifest(R, SLUG, MANIFEST_SHA)
    print("== shipping-image re-derivation")
    checks(img, R)
    capture_bytes(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null control")
    Rn.quiet = True
    same = img.patched(0x20B60A, img.read(0x20B60A, 6))
    checks(same, Rn)
    R.check("null control: an unchanged private copy (sha check off) passes every check", Rn.fails == 0 and Rn.n > 0,
            "%d of %d" % (Rn.n - Rn.fails, Rn.n))
    nctl = 0
    for label, va, nb in CONTROLS:
        if nb is None:
            nb = bytes([0xE8]) + struct.pack("<i", 0x16D6D0 - (va + 5)) + bytes([0x90] * 6)
        Pimg = img.patched(va, nb)
        if Pimg.d == img.d:
            raise SystemExit("control %s did not change the image" % label)
        Rc = Rep(label)
        Rc.quiet = True
        try:
            checks(Pimg, Rc)
            failed = Rc.fails
            why = "%d failed: %s" % (failed, "; ".join(Rc.failed[:3]))
        except Exception as e:
            failed = 1
            why = "refused: %r" % e
        nctl += 1
        R.check("control: " + label, failed > 0, why)
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))


if __name__ == "__main__":
    main()
