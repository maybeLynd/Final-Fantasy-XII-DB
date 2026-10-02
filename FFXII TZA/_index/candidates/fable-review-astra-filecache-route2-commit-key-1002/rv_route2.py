"""rv_route2.py - FABLE independent re-derivation for ASTRA packet filecache-route2-commit-key (81cbc06f0).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the insert-key-admission review).  Does not
import ASTRA's prove.py, capture drivers or the shared role adapter (reg_tracking.py).  Method: complete
linear decode of the five bodies (four against .pdata; the leaf hash has no .pdata record and is bounded by
its closed CFG, its single final ret and int3 padding), local CFGs from rvlib.Body, register-write censuses
for every key carrier, exact frame arithmetic for every stack-passed argument, dominance checks for the
out-key store and the hash's BTR, a census of every write that could reach source-record+28h between the
lookup and the commit read, and the reviewer's own finite abstract interpretation of the resolver's arm byte
r12b.  The controls patch a private in-memory copy of the image and require at least one named check to fail.
"""
import hashlib
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, SHA256 as SHA_PIN  # noqa: E402

RES = (0x0059EE90, 0x0059F1FC)    # resolver, 876 B
COMMIT = (0x0059A9B0, 0x0059AAD5)  # commit, 293 B
LOOK = (0x0020C1B0, 0x0020C2F2)   # lookup, 322 B
WRAP = (0x001D6D20, 0x001D6D6F)   # retained wrapper, 79 B
HASH = (0x00674A00, 0x00674A28)   # retained hash leaf, 40 B
COOKIE = (0x00808C40, 0x00808C61)
INSERT = 0x001D6A20
SLUG = "filecache-route2-commit-key"
MANIFEST_SHA = "f3365d0eb049fb0c84b6150f1d410a2d1e2b01e36f4025973dc3063c4215392d"

VALUE_OPS = {"and", "or", "xor", "btr", "bts", "btc", "shl", "shr", "sar", "sal", "rol", "ror", "rcl", "rcr",
             "imul", "mul", "add", "sub", "neg", "not", "movzx", "movsx", "movsxd", "crc32", "bswap", "inc", "dec",
             "lea", "cmovne", "cmove", "xchg", "bzhi", "pext", "andn", "setne", "sete"}


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


def T(B, a):
    I = B.ins.get(a)
    return I.text if I else "<no boundary>"


def rets_of(B):
    return [a for a in B.order if B[a].mnemonic == "ret"]


def frame_at(B, upto):
    """Bytes pushed + sub rsp,imm from entry to `upto` (straight prologue only)."""
    fr = 0
    for a in B.order:
        if a >= upto:
            break
        I = B[a]
        if I.mnemonic == "push":
            fr += 8
        elif I.mnemonic == "sub" and I.op_str.startswith("rsp, ") and I.imm:
            fr += I.imm[0]
    return fr


def bodies(img):
    return {k: Body(img, *r) for k, r in (("res", RES), ("commit", COMMIT), ("look", LOOK), ("wrap", WRAP),
                                         ("hash", HASH))}


def r12_states(B, lookup_call):
    """Reviewer's own finite abstract interpretation of the arm byte r12b over the resolver's local CFG.
    State = (pc, r12b in {0, 1, 'T'}, lookup_seen).  Every branch other than a test of r12b is taken both ways;
    callees preserve r12 (Win64 nonvolatile ABI premise).  Returns (all states, states at each pc)."""
    def after(a, r, seen):
        I = B[a]
        if "r12" in I.reg_writes and I.mnemonic not in ("push", "pop"):
            if I.text == "xor r12b, r12b":
                r = 0
            elif I.mnemonic == "mov" and I.op_str.startswith("r12b, ") and I.imm:
                r = 1 if I.imm[0] & 0xFF else 0
            else:
                r = "T"
        if I.mnemonic == "call" and I.direct_target() == lookup_call:
            seen = True
        return r, seen

    start = (B.start, "T", False)
    seen_states = set()
    st = [start]
    while st:
        s = st.pop()
        if s in seen_states:
            continue
        seen_states.add(s)
        a, r, seen = s
        r2, seen2 = after(a, r, seen)
        succ = B.succ(a)
        I = B[a]
        # constrain a je/jne that consumes `test r12b, r12b`
        prev = [p for p in B.order if p < a]
        if I.mnemonic in ("je", "jne") and prev and B[prev[-1]].text == "test r12b, r12b" and len(succ) == 2:
            fall, tgt = succ[0], succ[1]
            zero_goes = tgt if I.mnemonic == "je" else fall
            nz_goes = fall if I.mnemonic == "je" else tgt
            out = []
            if r2 in (0, "T"):
                out.append((zero_goes, 0, seen2))
            if r2 in (1, "T"):
                out.append((nz_goes, 1, seen2))
            st.extend(out)
            continue
        if I.mnemonic == "pop" and "r12" in I.reg_writes:
            r2 = "T"
        for n in succ:
            st.append((n, r2, seen2))
    return seen_states


def checks(img, R):
    Bs = bodies(img)
    RS, CM, LK, WR, HS = (Bs[k] for k in ("res", "commit", "look", "wrap", "hash"))

    # ---------------- bodies ----------------
    new = old = 0
    for k, (s, e) in (("res", RES), ("commit", COMMIT), ("look", LOOK), ("wrap", WRAP)):
        ents, ok = img.pdata_cover(s, e)
        R.check("body %08X + 0x%X (%d B) decodes exactly and one .pdata record covers it exactly (%s)" %
                (s, e - s, e - s, ",".join("%08X+0x%X fl%d" % (b, en - b, fl) for b, en, fl, rt in ents)),
                Bs[k].exact and ok and len(ents) == 1)
        if k == "wrap":
            old += e - s
        else:
            new += e - s
    s, e = HASH
    nx = e
    while img.read(nx, 1) == b"\xcc":
        nx += 1
    R.check("leaf %08X + 0x%X (%d B) decodes exactly; no .pdata covers it; int3 before entry and after the ret"
            % (s, e - s, e - s),
            HS.exact and img.pdata(s) is None and img.pdata(e - 1) is None and img.read(s - 1, 1) == b"\xcc" and
            nx - e >= 1, "int3 run after = %d B" % (nx - e))
    old += e - s
    R.check("new shipping bodies total 1491 B (876 + 293 + 322)", new == 1491, str(new))
    R.check("retained selected bodies total 119 B (79 wrapper + 40 hash)", old == 119, str(old))
    for k in ("res", "look", "wrap", "hash"):
        rets, tails, outs = Bs[k].exits()
        R.check("%08X local CFG closed: no tail/out branch, single ret is the last instruction" % Bs[k].start,
                not tails and not outs and rets == [Bs[k].order[-1]], "rets=%s tails=%s outs=%s" %
                (["%X" % x for x in rets], tails, outs))
    rets, tails, outs = CM.exits()
    R.check("0059A9B0 local CFG closed: no tail/out branch; two rets, 59A9F4 (early) and 59AAD4 (last)",
            not tails and not outs and rets == [0x59A9F4, 0x59AAD4] and CM.order[-1] == 0x59AAD4)
    R.check("resolver's single ret is 59F1FB, the last instruction (epilogue included in the body)",
            rets_of(RS) == [0x59F1FB] and RS.order[-1] == 0x59F1FB)

    # ---------------- claim 1: resolver -> 59A9B0 -> 1D6A20 ----------------
    R.check("59F1B0 `mov edx, dword ptr [r15 + 0x28]` is a 4-byte read; 59F1B4 rcx = r15; 59F1B7 call 59A9B0",
            T(RS, 0x59F1B0) == "mov edx, dword ptr [r15 + 0x28]" and RS[0x59F1B0].mems[0]["size"] == 4 and
            T(RS, 0x59F1B4) == "mov rcx, r15" and RS[0x59F1B7].direct_target() == COMMIT[0])
    R.check("resolver r15 = incoming rcx (59EEC4); r15 written nowhere else but the epilogue pop",
            T(RS, 0x59EEC4) == "mov r15, rcx" and writers(RS, "r15") == [0x59EEC4, 0x59F1F2],
            str(["%X" % x for x in writers(RS, "r15")]))
    R.check("the commit read is guarded by the arm byte: 59F1AB `test r12b, r12b`, 59F1AE `je 0x59f1bc`",
            T(RS, 0x59F1AB) == "test r12b, r12b" and T(RS, 0x59F1AE) == "je 0x59f1bc")
    R.check("59A9B0 saves the incoming key: `mov esi, edx` (59A9C3) with no rdx write before it, and before "
            "`setne dl` (59A9CA) overwrites dl",
            T(CM, 0x59A9C3) == "mov esi, edx" and writers(CM, "rdx", CM.start, 0x59A9C3) == [] and
            T(CM, 0x59A9CA) == "setne dl")
    rsiw = writers(CM, "rsi")
    R.check("59A9B0 rsi written only at 59A9C3 and the two epilogue restores (59A9EA, 59AACA)",
            rsiw == [0x59A9C3, 0x59A9EA, 0x59AACA] and T(CM, 0x59A9EA) == "mov rsi, qword ptr [rsp + 0x58]" and
            T(CM, 0x59AACA) == "mov rsi, qword ptr [rsp + 0x58]", str(["%X" % x for x in rsiw]))
    path = on_paths(CM, 0x59A9C3, 0x59AAA4)
    R.check("no rsi writer on any 59A9C3 -> 59AAA4 path; 59A9C3 dominates 59AAA4",
            not [x for x in path if "rsi" in CM[x].reg_writes and x != 0x59A9C3] and CM.dominates(0x59A9C3, 0x59AAA4),
            "%d insns on path" % len(path))
    R.check("59AAA2 `mov ecx, esi`, 59AAA4 call 1D6A20, no rcx write between",
            T(CM, 0x59AAA2) == "mov ecx, esi" and CM[0x59AAA4].direct_target() == INSERT)
    R.check("59A9B0 no value-changing op writes rsi anywhere in the body",
            not [a for a in CM.order if CM[a].mnemonic in VALUE_OPS and "rsi" in CM[a].reg_writes])
    R.check("1D6A20's other arguments are separate: rdx = &[rsp+50h] (1D6BB0 result, 59A9D4), r8d = edi = record+0 "
            "(59A9C5), r9d = signed byte record+18h (59AA93)",
            T(CM, 0x59AA98) == "lea rdx, [rsp + 0x50]" and T(CM, 0x59AA9D) == "mov r8d, edi" and
            T(CM, 0x59AA93) == "movsx r9d, byte ptr [rbx + 0x18]" and T(CM, 0x59A9C5) == "mov edi, dword ptr [rcx]"
            and T(CM, 0x59A9D4) == "mov qword ptr [rsp + 0x50], rax" and
            writers(CM, "rdi") == [0x59A9C5, 0x59A9F3, 0x59AAD3])
    R.check("59A9B0 frame: push rdi + sub 30h = 38h; rsi saved at entry SP+20h and restored from SP+58h",
            T(CM, 0x59A9B5) == "mov qword ptr [rsp + 0x20], rsi" and frame_at(CM, 0x59A9BF) == 0x38 and
            0x58 - 0x38 == 0x20)
    R.check("the insertion is gated on 1D6BB0: null result -> 59A9E1 `or rax, -1` and ret 59A9F4 without 1D6A20",
            CM[0x59A9CF].direct_target() == 0x1D6BB0 and T(CM, 0x59A9DC) == "test rax, rax" and
            T(CM, 0x59A9DF) == "jne 0x59a9f5" and 0x59AAA4 not in CM.reach(0x59A9E1))
    calls = sorted(set((x, CM[x].direct_target(), CM[x].op_str) for x in path if CM[x].mnemonic == "call"))
    R.note("callees on 59A9C3 -> 59AAA4 paths (ESI kept only by the Win64 nonvolatile ABI): %s" %
           ", ".join("%X->%s" % (x, ("%X" % t) if t else "IAT:" + iat_name(img, CM[x])) for x, t, o in calls))

    # ---------------- claim 2: lookup out-key ----------------
    R.check("resolver lookup call site: 59EFD2 edx = signed record+18h, 59EFD7 r9 = record+28h, 59EFDB r8 = &[rbp], "
            "59EFE2 rcx = name, 59EFE5 call 1D6D20; no r9 write between",
            T(RS, 0x59EFD2) == "movsx edx, byte ptr [r15 + 0x18]" and T(RS, 0x59EFD7) == "lea r9, [r15 + 0x28]" and
            T(RS, 0x59EFDB) == "lea r8, [rbp]" and T(RS, 0x59EFE2) == "mov rcx, rdi" and
            RS[0x59EFE5].direct_target() == WRAP[0] and writers(RS, "r9", 0x59EFD8, 0x59EFE5) == [])
    R.check("1D6D20: rbx = r9 (1D6D34), rbx written only there + epilogue restore, [rsp+20h] = rbx (1D6D47)",
            T(WR, 0x1D6D34) == "mov rbx, r9" and writers(WR, "rbx") == [0x1D6D34, 0x1D6D5A] and
            T(WR, 0x1D6D47) == "mov qword ptr [rsp + 0x20], rbx", str(["%X" % x for x in writers(WR, "rbx")]))
    fr = frame_at(WR, 0x1D6D34)
    R.check("1D6D20 frame 38h, so [rsp+20h] at the 20C1B0 call is the callee's entry SP+28h (fifth argument)",
            fr == 0x38 and WR[0x1D6D55].direct_target() == LOOK[0], "frame %X" % fr)
    R.check("1D6D20 other mappings: r9 = rdi = incoming r8, r8d = esi = incoming edx, rdx = rbp = incoming rcx, "
            "rcx = rax from 20C700",
            [T(WR, a) for a in (0x1D6D37, 0x1D6D3A, 0x1D6D3C, 0x1D6D44, 0x1D6D4C, 0x1D6D4F, 0x1D6D52)] ==
            ["mov rdi, r8", "mov esi, edx", "mov rbp, rcx", "mov rcx, rax", "mov r9, rdi", "mov r8d, esi",
             "mov rdx, rbp"] and WR[0x1D6D3F].direct_target() == 0x20C700)
    ww = [(x, m["base"], m["disp"]) for x, m in WR.mem_writes()]
    R.check("1D6D20 writes only its own stack (home slots and the fifth-argument slot); nothing through r9/rbx",
            ww and all(b == "rsp" for x, b, d in ww), str(ww))
    fr = frame_at(LK, 0x20C1BF)
    R.check("20C1B0 prologue: five pushes + sub 150h = 178h; rsp otherwise changed only by the epilogue",
            fr == 0x178 and all(x <= 0x20C1B8 or x >= 0x20C2E3 for x in LK.order
                                if "rsp" in LK[x].reg_writes and LK[x].mnemonic != "call"), "%X" % fr)
    R.check("20C1B0 out-key carrier: 20C1EE `mov r14, qword ptr [rsp + 0x1a0]` = entry SP+28h = fifth argument",
            T(LK, 0x20C1EE) == "mov r14, qword ptr [rsp + 0x1a0]" and 0x1A0 - fr == 0x28)
    R.check("20C1B0 r14 written only at 20C1EE and the epilogue pop 20C2EC",
            writers(LK, "r14") == [0x20C1EE, 0x20C2EC], str(["%X" % x for x in writers(LK, "r14")]))
    tw = [(x, m["disp"], m["size"]) for x, m in LK.mem_writes() if m["base"] == "r14" or m["index"] == "r14"]
    R.check("20C1B0 writes through r14 exactly once: 20C22D `mov dword ptr [r14], eax` (4 B)",
            tw == [(0x20C22D, 0, 4)] and T(LK, 0x20C22D) == "mov dword ptr [r14], eax", str(tw))
    r14use = [x for x in LK.order if "r14" in LK[x].reg_reads and
              not any(m["base"] == "r14" for m in LK[x].mems) and LK[x].mnemonic != "push"]
    R.check("r14 is used only as a memory base (never copied into an argument register)", not r14use,
            str(["%X %s" % (x, LK[x].text) for x in r14use]))
    R.check("the stored value is the hash's eax: 20C228 call 674A00, then 20C22D directly",
            LK[0x20C228].direct_target() == HASH[0] and LK.order[LK.order.index(0x20C228) + 1] == 0x20C22D)
    R.check("empty test: 20C218 `cmp byte ptr [rsp + 0x40], 0` (first byte of the normalized buffer), 20C21D "
            "`je 0x20c2c7`; the buffer is memset and passed to 20C440 as r8",
            T(LK, 0x20C218) == "cmp byte ptr [rsp + 0x40], 0" and T(LK, 0x20C21D) == "je 0x20c2c7" and
            T(LK, 0x20C1FE) == "lea rcx, [rsp + 0x40]" and LK[0x20C203].direct_target() == 0x861EC0 and
            T(LK, 0x20C208) == "lea r8, [rsp + 0x40]" and LK[0x20C213].direct_target() == 0x20C440)
    emp = LK.reach(0x20C2C7)
    R.check("empty arm 20C2C7 `or rax, -1` reaches the ret with no write through r14, no hash call, and only "
            "__security_check_cookie called; rax not rewritten after 20C2C7",
            T(LK, 0x20C2C7) == "or rax, 0xffffffffffffffff" and 0x20C22D not in emp and
            [LK[x].direct_target() for x in emp if LK[x].mnemonic == "call"] == [COOKIE[0]] and
            not [x for x in emp if x != 0x20C2C7 and "rax" in LK[x].reg_writes and LK[x].mnemonic != "call"])
    R.check("store dominance: every entry -> ret path passes 20C22D except through the empty branch 20C21D -> 20C2C7",
            LK.reach(0x20C223, avoid=[0x20C22D]).isdisjoint({LK.order[-1]}) and
            LK.order[-1] in LK.reach(LK.start, avoid=[0x20C22D]) and
            LK.order[-1] not in reach_avoid_edge(LK, LK.start, 0x20C21D, 0x20C2C7, 0x20C22D))
    R.check("the miss (20C2BE) and the hit (20C284) both follow the store: 20C22D dominates both",
            LK.dominates(0x20C22D, 0x20C2BE) and LK.dominates(0x20C22D, 0x20C284))
    arg_regs_before = [(x, LK[x].text) for x in LK.order if x < 0x20C228 and LK[x].mnemonic == "call"]
    R.check("calls before the hash are memset (861EC0) and the normalizer 20C440 only; neither gets r14",
            [LK[x].direct_target() for x, t in arg_regs_before] == [0x861EC0, 0x20C440])
    ck = Body(img, *COOKIE)
    R.check("__security_check_cookie (808C40) writes no rax on its returning path (cmp, rol rcx, test, ret)",
            ck.exact and not [x for x in ck.reach(ck.start) if "rax" in ck[x].reg_writes] and
            T(ck, 0x808C5C) == "jmp 0x809654")

    # ---------------- hash ----------------
    R.check("674A00: eax = 1505h, loop `imul eax, eax, 0x21` + movsx of the byte, then `btr eax, 0x1f` (674A23) and "
            "ret (674A27)",
            [T(HS, a) for a in (0x674A03, 0x674A10, 0x674A17, 0x674A1A, 0x674A23)] ==
            ["mov eax, 0x1505", "imul eax, eax, 0x21", "movsx edx, dl", "add eax, edx", "btr eax, 0x1f"] and
            rets_of(HS) == [0x674A27])
    R.check("674A00: the btr dominates the single ret, and eax is not written between them",
            HS.dominates(0x674A23, 0x674A27) and writers(HS, "rax", 0x674A24, 0x674A27) == [] and
            HS.order[HS.order.index(0x674A23) + 1] == 0x674A27)
    R.check("674A00 has no call, no memory write and no indirect jump", not HS.calls() and not HS.mem_writes())

    # ---------------- claim 3: composition ----------------
    lk_after = RS.reach(0x59EFF3)
    R.check("a non-negative lookup result returns: 59EFF1 `js 0x59f000`; from 59EFF3 the commit is unreachable",
            T(RS, 0x59EFF1) == "js 0x59f000" and 0x59F1B0 not in lk_after)
    r12w = [x for x in writers(RS, "r12") if RS[x].mnemonic not in ("pop",)]
    R.check("resolver r12 writers: 59EED6 `xor r12b, r12b`, 59EFC4 `mov r12b, 1`, 59EFCE `setne r12b` (+ pop)",
            r12w == [0x59EED6, 0x59EFC4, 0x59EFCE] and writers(RS, "r12")[-1] == 0x59F1F8,
            str(["%X %s" % (x, RS[x].text) for x in writers(RS, "r12")]))
    S = r12_states(RS, WRAP[0])
    cs = [s for s in S if s[0] == 0x59F1B7]
    R.check("own r12b abstract interpretation: every state at the 59F1B7 commit call has r12b != 0 and has passed "
            "the 59EFE5 lookup (%d states over %d instructions, bound %d; %d commit state(s))" %
            (len(S), len(RS.order), 6 * len(RS.order), len(cs)),
            cs and all(r != 0 and seen for a, r, seen in cs), str(sorted(cs)))
    R.note("those %d are analysis states (pc x r12b in {0,1,T} x lookup-seen), not executions" % len(S))
    seg = on_paths(RS, 0x59EFEA, 0x59F1B0)
    bad = []
    for x in seg:
        for m in RS[x].mems:
            if m["write"] and m["base"] == "r15" and m["disp"] < 0x2C and m["disp"] + m["size"] > 0x28:
                bad.append("%X" % x)
    R.check("no write through r15 overlaps record+28h..2Bh on any 59EFEA -> 59F1B0 path (%d insns)" % len(seg),
            not bad, str(bad))
    r15w = sorted(set((m["disp"], m["size"]) for x, m in RS.mem_writes() if m["base"] == "r15"))
    R.check("resolver writes through r15 anywhere: +0/4, +10h/8, +18h/1, +20h/8 only (the +20h qword ends at +27h)",
            r15w == [(0, 4), (0x10, 8), (0x18, 1), (0x20, 8)], str(r15w))
    r15nb = [x for x in seg if "r15" in RS[x].reg_reads and not any(m["base"] == "r15" for m in RS[x].mems)]
    R.check("on those paths r15 is used only as a memory base, so no callee receives a record pointer",
            not r15nb, str(["%X %s" % (x, RS[x].text) for x in r15nb]))
    cw = sorted(set(m["base"] for x in seg for m in RS[x].mems if m["write"] and m["base"] != "r15"))
    R.note("other writes on those paths use bases %s (stack / alloca buffers: private-frame premise)" % cw)
    R.note("callees on those paths: %s" % sorted("%X" % RS[x].direct_target() for x in seg
                                                 if RS[x].mnemonic == "call"))
    R.check("the archive fill gates the commit: 59F197 stores 19AEE0's result to record+10h, 59F19E `je 0x59f1c0` "
            "skips the commit when it is null",
            RS[0x59F192].direct_target() == 0x19AEE0 and T(RS, 0x59F19E) == "je 0x59f1c0" and
            0x59F1B7 not in RS.reach(0x59F1C0))
    cmw = [(x, m["disp"], m["size"]) for x, m in CM.mem_writes() if m["base"] == "rbx" and x < 0x59AAA4]
    R.check("59A9B0 writes no record+28h before its 1D6A20 call (rbx-based writes: +0, +8, +10h only)",
            all(not (d < 0x2C and d + s > 0x28) for x, d, s in cmw) and T(CM, 0x59A9C7) == "mov rbx, rcx",
            str(cmw))


def reach_avoid_edge(B, frm, ea, eb, avoid):
    """Reach from frm, not passing `avoid` and not taking the edge ea -> eb."""
    seen, st = set(), [frm]
    while st:
        a = st.pop()
        if a in seen or a == avoid or a not in B.ins:
            continue
        seen.add(a)
        for s in B.succ(a):
            if a == ea and s == eb:
                continue
            st.append(s)
    return seen


def iat_name(img, I):
    try:
        slot = I.address + I.size + I.mems[0]["disp"]
        hn = img.u64(slot)
        if hn >> 63:
            return "ordinal"
        return img.read(img.base + hn + 2, 64).split(b"\0")[0].decode("ascii", "replace")
    except Exception:
        return "?"


def capture_bytes(img, R):
    """The packet's captured and retained range hashes must equal this image's bytes (kept out of checks() so a
    patched control image cannot fail on this alone)."""
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    mism, got = [], []
    for f in ("source-01.json", "retained/filecache-key-boundaries-source-02.json",
              "retained/filecache-hash-loop-source-01.json"):
        for r in json.load(open(os.path.join(ev, f)))["ranges"]:
            s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
            got.append((s_, e_))
            if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"]:
                mism.append(r["start"])
    need = [RES, COMMIT, LOOK, WRAP, HASH]
    R.check("packet's captured/retained range sha256 values equal this image's bytes (%d ranges, incl. all five "
            "bodies)" % len(got), not mism and all(n in got for n in need), str(mism))
    rd = open(os.path.join(ev, "README.md"), encoding="utf-8").read()
    res = json.load(open(os.path.join(ev, "result-02.json")))
    R.check("packet frames the 606 as abstract states, not executions (README + result-02 limits)",
            "These are not606" in rd and "executions" in rd and res["arm_flag_proof"]["states"] == 606 and
            "no concrete path length, native execution" in res["arm_flag_proof"]["limits"])
    st = json.load(open(os.path.join(ev, "retained", "filecache-hash-loop-capture-01.status.json")))
    R.check("retained hash capture receipt is exit-only (no terminal flag, no driver hash) and result-02 labels it "
            "LEGACY_INCOMPLETE", set(st) == {"exit", "driver"} and
            res["retained_hash_invocation"].startswith("LEGACY_INCOMPLETE_INVOCATION_RECEIPT"), str(st))


CONTROLS = [
    ("674A23 `btr eax, 0x1f` -> four nops (hash no longer clears bit 31)", 0x674A23, bytes([0x90] * 4)),
    ("674A0A empty-string `je 674A23` -> `je 674A27` (an exit that skips the btr)", 0x674A0B, bytes([0x1B])),
    ("20C1EE out-key carrier [rsp+1A0h] -> [rsp+1A8h] (sixth slot)", 0x20C1F2, bytes([0xA8])),
    ("20C22D `mov [r14], eax` -> `nop; mov [rsi], eax` (store moved off the carrier)", 0x20C22D,
     bytes.fromhex("908906")),
    ("20C21D empty-key `je 20C2C7` retargeted to 20C22D (early return moved after the store)", 0x20C21D, None),
    ("59F1B0 `mov edx, [r15+28h]` -> [r15+2Ch]", 0x59F1B3, bytes([0x2C])),
    ("59AAA2 `mov ecx, esi` -> `mov ecx, edi` (size passed as the key)", 0x59AAA2, bytes.fromhex("8BCF")),
    ("59AA47 `mov r8d, esi` -> `mov esi, r8d` (59A9B0 overwrites ESI before the call)", 0x59AA47,
     bytes.fromhex("418BF0")),
    ("1D6D47 fifth-argument store [rsp+20h] -> [rsp+28h]", 0x1D6D4B, bytes([0x28])),
    ("59EFD7 `lea r9, [r15+28h]` -> [r15+2Ch]", 0x59EFDA, bytes([0x2C])),
    ("59EED6 `xor r12b, r12b` -> `mov r12b, 1` (commit armed without the lookup)", 0x59EED6, bytes.fromhex("41B401")),
    ("59EFEA `mov [r15+20h], rax` -> [r15+28h] (record+28h written after the lookup)", 0x59EFED, bytes([0x28])),
    ("1D6D34 `mov rbx, r9` -> `mov rbx, r8` (fourth argument forwarded as the out-key)", 0x1D6D34,
     bytes.fromhex("498BD8")),
]


def main():
    img = Img.load()
    R = Rep("rv_route2")
    print("== packet integrity")
    check_manifest(R, SLUG, MANIFEST_SHA)
    print("== shipping-image re-derivation")
    checks(img, R)
    capture_bytes(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null control")
    Rn.quiet = True
    same = img.patched(0x674A23, img.read(0x674A23, 4))
    checks(same, Rn)
    R.check("null control: an unchanged private copy (sha check off) passes every check", Rn.fails == 0 and Rn.n > 0,
            "%d of %d" % (Rn.n - Rn.fails, Rn.n))
    nctl = 0
    for label, va, nb in CONTROLS:
        if nb is None:
            nb = bytes([0x0F, 0x84]) + struct.pack("<i", 0x20C22D - (va + 6))
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
    disk = hashlib.sha256(open(find_exe(), "rb").read()).hexdigest()
    R.check("exe on disk still hashes to the pinned sha256 after all controls", disk == SHA_PIN, disk)
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))


if __name__ == "__main__":
    main()
