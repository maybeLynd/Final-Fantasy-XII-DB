"""rv_cancel.py - FABLE independent re-derivation for ASTRA packet request-cancel-notification (011e013c7).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the filecache-route2-commit-key review).  Does not
import ASTRA's prove.py, capture/unwind drivers, control.py or the shared role adapter (reg_tracking.py).  Method:
complete linear decode of the three new bodies (00352980, 00353660, 003DB420) and the eight retained bodies, bounded
by the image's own .pdata (following CHAININFO records) or, for leaves without a record, by a closed CFG ending in
ret; local CFGs from rvlib.Body; register-write censuses for every carrier; flag-producer checks for the cmov/jcc
pairs; a premise-driven path walker through the retained removal; reverse reaching definitions for every EAX at a
ret; the call closure in front of the notification attempt.  Controls patch a private in-memory copy of the image
and require at least one named check to fail.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, SHA256 as SHA_PIN  # noqa: E402

FREQ = (0x00352980, 0x003529AE)    # freqcancel native carrier, 46 B
FREQ2 = (0x00353660, 0x003536AC)   # two-argument carrier, 76 B
RECYC = (0x003DB420, 0x003DB550)   # ActorResource_RecycleEntryRange, 304 B
RETAINED = [(0x00263FF0, 0x00264005), (0x003587C0, 0x003587F2), (0x003DB2A0, 0x003DB41A),
            (0x003DB550, 0x003DB573), (0x003DB650, 0x003DB6D5), (0x003DBCF0, 0x003DBDB2),
            (0x003DC0D0, 0x003DC12D), (0x003DC1B0, 0x003DC239)]
REMOVE, POST, UNHOOK, GETENT, RESOLVE, SLOTARR, ALLOC = (0x3DB2A0, 0x3DC0D0, 0x3DC1B0, 0x3DB550, 0x3587C0,
                                                        0x263FF0, 0x3DBCF0)
SCHED = 0x003DB6E0
POP, ACTRES = 0x00267E10, 0x00264010
INTERP = 0x0025E4C0                 # WorldActorScriptVM_InterpretBytecode
SLUG = "request-cancel-notification"
PARENT = "notification-retirement-order"
PRODUCER = "011e013c7"
MANIFEST_SHA = "8a463282899676c2b8a1248a23bacf8c48280431105374d9bd49481146d461b2"
FLAG_SETTERS = {"cmp", "test", "add", "sub", "and", "or", "xor", "inc", "dec", "neg", "shl", "shr", "sar", "rol",
                "ror", "imul", "bt", "btr", "bts", "sbb", "adc"}


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


def T(B, a):
    I = B.ins.get(a)
    return I.text if I else "<no boundary>"


def writers(B, fam, lo=None, hi=None):
    return [a for a in B.order if fam in B[a].reg_writes and (lo is None or lo <= a) and (hi is None or a < hi)]


def preds(B):
    p = {}
    for a in B.order:
        for s in B.succ(a):
            p.setdefault(s, set()).add(a)
    return p


def between(B, a, b):
    """Instructions strictly between a and b in linear order."""
    return [x for x in B.order if a < x < b]


def rax_defs_reaching(B, use):
    """Reverse reaching definitions of rax at `use`: walk predecessors until an instruction writes rax (a call
    clobbers rax)."""
    P = preds(B)
    defs, seen, st = set(), set(), list(P.get(use, ()))
    while st:
        a = st.pop()
        if a in seen:
            continue
        seen.add(a)
        I = B[a]
        if "rax" in I.reg_writes or I.mnemonic == "call":
            defs.add(a)
            continue
        st.extend(P.get(a, ()))
    return defs


def rax_read_before_write(B, frm):
    """Instructions reachable from `frm` (exclusive) that read rax before any write to it on some path."""
    bad, seen, st = [], set(), list(B.succ(frm))
    while st:
        a = st.pop()
        if a in seen:
            continue
        seen.add(a)
        I = B[a]
        selfzero = I.mnemonic == "xor" and len(set(I.op_str.split(", "))) == 1
        if "rax" in I.reg_reads and not selfzero:
            bad.append(a)
            continue
        if "rax" in I.reg_writes or I.mnemonic == "call":
            continue
        st.extend(B.succ(a))
    return bad


def walk(B, start, decisions, stop, limit=400):
    """Deterministic path walker: each conditional branch on the path must have a premise decision
    (True = taken).  Returns the instruction list up to and including `stop`, or None."""
    path, a = [], start
    for _ in range(limit):
        path.append(a)
        if a == stop:
            return path
        I = B[a]
        s = B.succ(a)
        if I.mnemonic.startswith("j") and I.mnemonic != "jmp":
            if a not in decisions:
                return None
            a = s[1] if decisions[a] else s[0]
        elif len(s) == 1:
            a = s[0]
        else:
            return None
    return None


def pdata_chain(img, s, e):
    """Every RUNTIME_FUNCTION inside [s,e): (begin, end, unwind flags, DIRECT chain target begin or None)."""
    po = img.off(img.base + img.exc_rva)
    out = []
    for i in range(img.exc_size // 12):
        b, en, u = struct.unpack_from("<III", img.d, po + i * 12)
        b += img.base
        en += img.base
        if s <= b < e:
            ui = img.off(img.base + u)
            fl = img.d[ui] >> 3
            n = img.d[ui + 2]
            tgt = None
            if fl & 4:
                co = ui + 4 + ((n + 1) & ~1) * 2
                tgt = struct.unpack_from("<I", img.d, co)[0] + img.base
            out.append((b, en, fl, tgt))
    return sorted(out)


def leaf_bounded(img, B):
    rets, tails, outs = B.exits()
    nb = img.read(B.end, 1)
    return (B.exact and not tails and not outs and B[B.order[-1]].mnemonic == "ret" and img.pdata(B.start) is None
            and (nb == b"\xcc" or img.pdata(B.end) is not None))


def indirect_calls(B):
    return [a for a in B.order if B[a].mnemonic == "call" and B[a].direct_target() is None]


REMOVAL_PREMISES = {
    0x3DB2B6: True,    # jne: entry index != 0xFF
    0x3DB2D5: False,   # je: actor non-null
    0x3DB2FC: False,   # je: entry+10 != 4 (not on the detached list)
    0x3DB305: False,   # js: entry+2 channel >= 0
    0x3DB320: False,   # je: channel head != 0xFF
    0x3DB32D: True,    # je: channel head == this entry (valid head)
    0x3DB34D: True,    # jns: channel >= 0
    0x3DB36F: False,   # je: requester word +6 != 0x8000
    0x3DB375: False,   # jne: entry+10 == 3 (mode-3 descriptor)
}


def checks(img, R):
    Bf, Bf2, BR = Body(img, *FREQ), Body(img, *FREQ2), Body(img, *RECYC)
    RB = {s: Body(img, s, e) for s, e in RETAINED}
    BM, BP, BU, BG, BV, BS = RB[REMOVE], RB[POST], RB[UNHOOK], RB[GETENT], RB[RESOLVE], RB[SLOTARR]

    # ---------------- extents ----------------
    for nm, (s, e), B in (("00352980", FREQ, Bf), ("00353660", FREQ2, Bf2)):
        ents, ok = img.pdata_cover(s, e)
        R.check("body %s + 0x%X (%d B) decodes exactly and one .pdata record covers it exactly" % (nm, e - s, e - s),
                B.exact and ok and len(ents) == 1)
    ch = pdata_chain(img, *RECYC)
    ents, ok = img.pdata_cover(*RECYC)
    R.check("body 003DB420 + 0x130 (304 B) decodes exactly and the .pdata records inside it tile it exactly",
            BR.exact and ok, ", ".join("%X+0x%X fl%d" % (b, en - b, fl) for b, en, fl, t in ch))
    R.check("003DB420's first .pdata record is 003DB420 + 0x1C (28 B), flags 0 (the primary record)",
            ch and ch[0][:3] == (0x3DB420, 0x3DB43C, 0), "%X..%X fl%d" % ch[0][:3] if ch else "")
    direct = dict((b, t) for b, en, fl, t in ch)
    roots = {}
    for b in direct:
        r, hops = b, 0
        while direct.get(r) is not None and hops < 8:
            r, hops = direct[r], hops + 1
        roots[b] = (r, hops)
    R.check("the other %d records are CHAININFO (flag 4): 3DB43C, 3DB53E, 3DB545 chain directly to 3DB420; "
            "3DB491 and 3DB51F chain to 3DB43C; every chain resolves to 3DB420 in at most 2 hops" % (len(ch) - 1),
            len(ch) == 6 and all(fl == 4 for b, en, fl, t in ch[1:]) and
            direct == {0x3DB420: None, 0x3DB43C: 0x3DB420, 0x3DB491: 0x3DB43C, 0x3DB51F: 0x3DB43C,
                       0x3DB53E: 0x3DB420, 0x3DB545: 0x3DB420} and
            all(r == 0x3DB420 and h <= 2 for r, h in roots.values()),
            str(["%X->%s" % (b, "%X" % t if t else None) for b, en, fl, t in ch[1:]]))
    R.check("the primary record's 28 B end at 003DB420 + 0x1C, which is before the first branch target "
            "outside it (003DB545) and before the removal call (003DB506)",
            ch and ch[0][1] < 0x3DB545 and ch[0][1] < 0x3DB506 and BR[0x3DB42C].direct_target() == 0x3DB545)
    rets, tails, outs = BR.exits()
    R.check("003DB420 local CFG closed: no tail/out branch; rets exactly 3DB53D and 3DB54F (the last instruction)",
            not tails and not outs and rets == [0x3DB53D, 0x3DB54F] and BR.order[-1] == 0x3DB54F,
            "rets=%s tails=%s outs=%s" % (["%X" % x for x in rets], tails, outs))
    for B in (Bf, Bf2):
        rets, tails, outs = B.exits()
        R.check("%08X local CFG: no ret, single exit is the final tail jmp to 003DB6E0" % B.start,
                not rets and not outs and tails == [(B.order[-1], SCHED)])
    R.check("new original bytes total 426 (46 + 76 + 304)",
            sum(e - s for s, e in (FREQ, FREQ2, RECYC)) == 426, str(sum(e - s for s, e in (FREQ, FREQ2, RECYC))))
    tot, desc = 0, []
    for s, e in RETAINED:
        B = RB[s]
        if img.pdata(s) is not None:
            ents, ok = img.pdata_cover(s, e)
            good = B.exact and ok
            desc.append("%X:%d rec" % (s, len(ents)))
        else:
            good = leaf_bounded(img, B)
            desc.append("%X:leaf" % s)
        R.check("retained body %08X + 0x%X (%d B) decodes exactly and is bounded (.pdata chain, or closed leaf CFG)"
                % (s, e - s, e - s), good)
        tot += e - s
    R.check("retained bodies total 1041 B over 8 bodies", tot == 1041 and len(RETAINED) == 8, "%d; %s" % (tot, desc))

    # ---------------- native carriers ----------------
    R.check("00352980: rbx = incoming rdx (352989), the popped value (267E10's eax) -> edx, r8d = 4, rcx = rbx, "
            "call 3DB420 (35299C)",
            T(Bf, 0x352986) == "mov rcx, r9" and T(Bf, 0x352989) == "mov rbx, rdx" and
            Bf[0x35298C].direct_target() == POP and T(Bf, 0x352991) == "mov r8d, 4" and
            T(Bf, 0x352997) == "mov edx, eax" and T(Bf, 0x352999) == "mov rcx, rbx" and
            Bf[0x35299C].direct_target() == RECYC[0] and writers(Bf, "rbx") == [0x352989, 0x3529A8])
    R.check("00352980: after 3DB420, rcx = rbx again and the body tail-jumps to 003DB6E0 (3529A9); 3DB420's EAX "
            "is never read", T(Bf, 0x3529A1) == "mov rcx, rbx" and T(Bf, 0x3529A9) == "jmp 0x3db6e0" and
            not rax_read_before_write(Bf, 0x35299C))
    R.check("00353660: first pop -> edi (353678), second pop -> ecx -> 264010 (353681); r8d = 4; "
            "edx = `lea edx, [rdi + 1]` (35368C); rcx = rbx = 264010's rax; call 3DB420 (353695)",
            T(Bf2, 0x35366A) == "mov rcx, r9" and T(Bf2, 0x35366D) == "mov rbx, r9" and
            Bf2[0x353670].direct_target() == POP and T(Bf2, 0x353675) == "mov rcx, rbx" and
            T(Bf2, 0x353678) == "mov edi, eax" and Bf2[0x35367A].direct_target() == POP and
            T(Bf2, 0x35367F) == "mov ecx, eax" and Bf2[0x353681].direct_target() == ACTRES and
            T(Bf2, 0x353686) == "mov r8d, 4" and T(Bf2, 0x35368C) == "lea edx, [rdi + 1]" and
            T(Bf2, 0x35368F) == "mov rcx, rax" and T(Bf2, 0x353692) == "mov rbx, rax" and
            Bf2[0x353695].direct_target() == RECYC[0])
    R.check("00353660: rdi written only at 353678 (+ epilogue pop); the lower bound is a 32-bit lea, so first "
            "pop 0x7FFFFFFF wraps to a negative bound", writers(Bf2, "rdi") == [0x353678, 0x3536A6],
            str(["%X" % x for x in writers(Bf2, "rdi")]))
    R.check("00353660: after 3DB420, rcx = rbx (the resolved actor, possibly NULL) and the body tail-jumps to "
            "003DB6E0 (3536A7)", T(Bf2, 0x35369A) == "mov rcx, rbx" and T(Bf2, 0x3536A7) == "jmp 0x3db6e0" and
            writers(Bf2, "rbx", 0x353693, 0x35369D) == [])
    Bpop = Body(img, POP, 0x267E5E)
    R.check("00267E10 (the pop both carriers call): empty stack (count <= 0) returns 0; type byte 1 returns the "
            "DWORD, type 2 returns `cvttss2si` of the float, any other type calls 008620C0(1) and returns 0",
            Bpop.exact and T(Bpop, 0x267E18) == "jle 0x267e3b" and T(Bpop, 0x267E3B) == "xor eax, eax" and
            T(Bpop, 0x267E51) == "mov eax, dword ptr [rcx + r8*4 + 0x184]" and
            T(Bpop, 0x267E42) == "cvttss2si eax, dword ptr [rcx + r8*4 + 0x184]" and
            Bpop[0x267E36].direct_target() == 0x8620C0 and Bpop.succ(0x267E36) == [0x267E3B])
    Ba = Body(img, ACTRES, 0x264045)
    R.check("00264010 can return NULL: `xor eax, eax` + ret at 26403E, reached when 3590D0 returns 0 for a "
            "negative input", Ba.exact and T(Ba, 0x26403E) == "xor eax, eax" and 0x26403E in Ba.reach(0x26402A))
    Bsch = Body(img, SCHED, 0x3DB703)
    R.check("003DB6E0 reads byte [rcx + 0x63] at 3DB6E6 before any test of rcx (push rdi, sub rsp only before it)",
            Bsch.exact and T(Bsch, 0x3DB6E6) == "cmp byte ptr [rcx + 0x63], 0" and
            [T(Bsch, a) for a in Bsch.order[:2]] == ["push rdi", "sub rsp, 0x20"])

    # ---------------- recycler: range ----------------
    R.check("NULL actor: 3DB429 `test rcx, rcx`, 3DB42C `je 0x3db545`; 3DB545 `mov eax, 1` then ret, no call",
            T(BR, 0x3DB429) == "test rcx, rcx" and T(BR, 0x3DB42C) == "je 0x3db545" and
            T(BR, 0x3DB545) == "mov eax, 1" and not [a for a in BR.reach(0x3DB545) if BR[a].mnemonic == "call"])
    nb = between(BR, 0x3DB441, 0x3DB44F)
    R.check("lower bound = max(0, signed edx): 3DB43A `xor eax, eax`, 3DB441 `test edx, edx`, 3DB44F "
            "`cmovns eax, edx`, no flag producer between", T(BR, 0x3DB43A) == "xor eax, eax" and
            T(BR, 0x3DB441) == "test edx, edx" and T(BR, 0x3DB44F) == "cmovns eax, edx" and
            not [a for a in nb if BR[a].mnemonic in FLAG_SETTERS] and writers(BR, "rdx", BR.start, 0x3DB44F) == [],
            str([T(BR, a) for a in nb]))
    R.check("mode 3 alone narrows the range (3DB466 `cmp r8d, 3`, 3DB46A `jne 0x3db473` skips it for mode 4)",
            T(BR, 0x3DB466) == "cmp r8d, 3" and T(BR, 0x3DB46A) == "jne 0x3db473" and
            T(BR, 0x3DB46C) == "lea r9d, [rax + 1]" and T(BR, 0x3DB470) == "xor r8d, r8d")
    R.check("start channel = byte actor+88h - 1 (3DB432, 3DB47D, 3DB481 movsxd rbp); lower bound r15 = movsxd eax "
            "(3DB476)", T(BR, 0x3DB432) == "movzx r9d, byte ptr [rcx + 0x88]" and
            T(BR, 0x3DB47D) == "lea ecx, [r9 - 1]" and T(BR, 0x3DB481) == "movsxd rbp, ecx" and
            T(BR, 0x3DB476) == "movsxd r15, eax" and writers(BR, "r9", 0x3DB433, 0x3DB47D) == [0x3DB46C])
    R.check("the range compares are signed 64-bit: 3DB488 `cmp rbp, r15` / `jl 0x3db53e`, 3DB510 `cmp rbp, r15` / "
            "`jge 0x3db4a0`; rbp is decremented once per channel (3DB50D)",
            T(BR, 0x3DB488) == "cmp rbp, r15" and T(BR, 0x3DB48B) == "jl 0x3db53e" and
            T(BR, 0x3DB510) == "cmp rbp, r15" and T(BR, 0x3DB513) == "jge 0x3db4a0" and
            T(BR, 0x3DB50D) == "dec rbp")
    R.check("rbp written only at 3DB481, 3DB50D (+ restore 3DB52E); r15 only at 3DB476 (+ restore 3DB533)",
            writers(BR, "rbp") == [0x3DB481, 0x3DB50D, 0x3DB52E] and writers(BR, "r15") == [0x3DB476, 0x3DB533],
            str(["%X" % x for x in writers(BR, "rbp") + writers(BR, "r15")]))
    # ---------------- recycler: active-bit snapshot ----------------
    R.check("active bits are a snapshot: r12d = WORD actor+6 at 3DB457, r12 not written in the loop (only the "
            "3DB524 restore); 3DB4A9 `test r12d, edi` / `je 0x3db50b` gates each channel",
            T(BR, 0x3DB457) == "movzx r12d, word ptr [rcx + 6]" and writers(BR, "r12") == [0x3DB457, 0x3DB524] and
            T(BR, 0x3DB4A9) == "test r12d, edi" and T(BR, 0x3DB4AC) == "je 0x3db50b")
    R.check("channel bit mask: edi = 1 rotated left by cl = low byte of (count - 1) (3DB496, 3DB49B, no rcx write "
            "after 3DB47D), then `ror edi, 1` per channel (3DB50B)",
            T(BR, 0x3DB496) == "mov edi, 1" and T(BR, 0x3DB49B) == "rol edi, cl" and
            writers(BR, "rcx", 0x3DB47E, 0x3DB49B) == [] and T(BR, 0x3DB50B) == "ror edi, 1" and
            writers(BR, "rdi") == [0x3DB496, 0x3DB49B, 0x3DB50B, 0x3DB515])
    # ---------------- recycler: mode 4 normalises the filter ----------------
    nb = between(BR, 0x3DB479, 0x3DB484)
    R.check("mode filter r14d = (r8d != 4) ? r8d : 0: 3DB473 `xor r14d, r14d`, 3DB479 `cmp r8d, 4`, 3DB484 "
            "`cmovne r14d, r8d`, no flag producer between", T(BR, 0x3DB473) == "xor r14d, r14d" and
            T(BR, 0x3DB479) == "cmp r8d, 4" and T(BR, 0x3DB484) == "cmovne r14d, r8d" and
            not [a for a in nb if BR[a].mnemonic in FLAG_SETTERS], str([T(BR, a) for a in nb]))
    R.check("r14 written only at 3DB473, 3DB484 (+ restore 3DB51F); r8 before 3DB479 written only on the mode-3 "
            "arm (3DB470)", writers(BR, "r14") == [0x3DB473, 0x3DB484, 0x3DB51F] and
            writers(BR, "r8", BR.start, 0x3DB479) == [0x3DB470], str(["%X" % x for x in writers(BR, "r14")]))
    # ---------------- recycler: selection ----------------
    R.check("per channel: head = BYTE [actor + channel + 94h] (3DB4A0); 0xFF head skips (3DB4B0/3DB4B7)",
            T(BR, 0x3DB4A0) == "movzx r8d, byte ptr [rbx + rbp + 0x94]" and
            T(BR, 0x3DB4B0) == "cmp r8d, 0xff" and T(BR, 0x3DB4B7) == "je 0x3db50b")
    R.check("entry state = BYTE entry+11h, entry stride 14h (3DB4B9 entries = actor+A0h, 3DB4C0 r8*5, 3DB4C4 "
            "[rcx+rdx*4+0x11]); 3DB4CA `test r9d, r9d` / `jne 0x3db4dc` selects any nonzero state",
            T(BR, 0x3DB4B9) == "mov rcx, qword ptr [rbx + 0xa0]" and T(BR, 0x3DB4C0) == "lea rdx, [r8 + r8*4]" and
            T(BR, 0x3DB4C4) == "movzx r9d, byte ptr [rcx + rdx*4 + 0x11]" and BR[0x3DB4C4].mems[0]["size"] == 1 and
            T(BR, 0x3DB4CA) == "test r9d, r9d" and T(BR, 0x3DB4CD) == "jne 0x3db4dc")
    R.check("a zero state follows the entry's +0 link (3DB4D3) under a signed count bound (3DB4CF `cmp eax, esi`, "
            "3DB4D1 `jg`, esi = BYTE actor+89h at 3DB448)",
            T(BR, 0x3DB4D3) == "movzx r8d, byte ptr [rcx + rdx*4]" and T(BR, 0x3DB4CF) == "cmp eax, esi" and
            T(BR, 0x3DB4D1) == "jg 0x3db50b" and T(BR, 0x3DB448) == "movzx esi, byte ptr [rcx + 0x89]" and
            T(BR, 0x3DB4D8) == "inc eax" and T(BR, 0x3DB4DA) == "jmp 0x3db4b0")
    p4 = walk(BR, 0x3DB4DC, {0x3DB4E2: True}, 0x3DB506)
    R.check("mode 4 (r14d = 0): 3DB4DC -> 3DB4E2 `je 0x3db500` -> 3DB500 edx = r8d (the walked entry) -> "
            "3DB503 rcx = actor -> 3DB506 call 3DB2A0; no r9 (state) read on that path",
            p4 == [0x3DB4DC, 0x3DB4DF, 0x3DB4E2, 0x3DB500, 0x3DB503, 0x3DB506] and
            T(BR, 0x3DB4DF) == "test r14d, r14d" and T(BR, 0x3DB500) == "mov edx, r8d" and
            T(BR, 0x3DB503) == "mov rcx, rbx" and BR[0x3DB506].direct_target() == REMOVE and
            not [a for a in p4 if "r9" in BR[a].reg_reads], str(["%X" % a for a in (p4 or [])]))
    R.check("the only call in 003DB420 is 3DB506 -> 003DB2A0; no indirect call",
            BR.calls() == [(0x3DB506, REMOVE)] and not indirect_calls(BR))
    P = preds(BR)
    R.check("the walk's back edge into 3DB4B0 comes only from the zero-state arm 3DB4DA (and 3DB4AE falls in)",
            sorted(P.get(0x3DB4B0, ())) == [0x3DB4AE, 0x3DB4DA] and BR.succ(0x3DB4CD)[0] == 0x3DB4CF)
    R.check("once per channel: 3DB506's only successor is 3DB50B; from the nonzero arm 3DB4DC no path re-enters "
            "the entry walk (3DB4B0) without passing `dec rbp` (3DB50D)",
            BR.succ(0x3DB506) == [0x3DB50B] and 0x3DB4B0 not in BR.reach(0x3DB4DC, avoid=[0x3DB50D]))
    R.check("3DB2A0's EAX is dead in the recycler: every path from 3DB506 writes rax before reading it",
            not rax_read_before_write(BR, 0x3DB506), str(rax_read_before_write(BR, 0x3DB506)))
    # ---------------- recycler: return value ----------------
    d1, d2 = rax_defs_reaching(BR, 0x3DB53D), rax_defs_reaching(BR, 0x3DB54F)
    R.check("reverse reaching definitions: EAX at ret 3DB53D <- {3DB51A, 3DB53E}; at ret 3DB54F <- {3DB545}; all "
            "three are `mov eax, 1`", d1 == {0x3DB51A, 0x3DB53E} and d2 == {0x3DB545} and
            all(T(BR, a) == "mov eax, 1" for a in d1 | d2),
            "3DB53D<-%s 3DB54F<-%s" % (sorted("%X" % a for a in d1), sorted("%X" % a for a in d2)))
    R.check("the three normal outcomes map to those definitions: empty range 3DB48B -> 3DB53E; loop exit 3DB513 "
            "falls to 3DB515 -> 3DB51A; NULL actor -> 3DB545",
            BR[0x3DB48B].direct_target() == 0x3DB53E and BR.succ(0x3DB513)[0] == 0x3DB515 and
            0x3DB51A in BR.reach(0x3DB515) and BR[0x3DB42C].direct_target() == 0x3DB545)

    # ---------------- retained removal 003DB2A0 ----------------
    path = walk(BM, BM.start, REMOVAL_PREMISES, 0x3DB37D)
    R.check("removal premise path: index != FF, actor non-null, +10h != 4, +2 >= 0, head != FF, head == index, "
            "+6 != 8000h, +10h == 3 reaches 3DB37D `call 0x3dc0d0` (%d instructions)" % (len(path) if path else 0),
            path is not None and BM[0x3DB37D].direct_target() == POST and
            [T(BM, a) for a in (0x3DB2B0, 0x3DB2F8, 0x3DB303, 0x3DB31B, 0x3DB32B, 0x3DB36B, 0x3DB371)] ==
            ["cmp esi, 0xff", "cmp byte ptr [rdi + 0x10], 4", "test ebp, ebp", "cmp eax, 0xff", "cmp esi, eax",
             "cmp word ptr [rdi + 6], ax", "cmp byte ptr [rdi + 0x10], 3"])
    rd = sorted(set((m["base"], m["disp"]) for a in (path or []) for m in BM[a].mems if m["read"] and
                    BM[a].mnemonic != "lea" and m["base"] != "rsp"))
    R.check("that path reads entry +12h, +10h, +2, +6 and the head byte; it never reads entry +11h (run state)",
            path is not None and not [x for x in rd if x[0] == "rdi" and x[1] == 0x11] and
            ("rdi", 0x6) in rd and ("rdi", 0x10) in rd, str(rd))
    pc = [BM[a].direct_target() for a in (path or []) if BM[a].mnemonic == "call"]
    R.check("the only call before 3DB37D on that path is the unhook 3DB346 -> 003DC1B0", pc == [UNHOOK, POST],
            str(["%X" % x for x in pc]))
    R.check("3DB37D precedes the flags test (3DB386 `cmp al, 2`) and the 00263050 call (3DB392): the attempt "
            "does not depend on entry +12h", path is not None and 0x3DB386 not in path and
            BM[0x3DB392].direct_target() == 0x263050 and T(BM, 0x3DB386) == "cmp al, 2")
    R.check("removal EAX = BYTE entry+12h & 1 (3DB2EA, 3DB2EF, 3DB402); r14 has no other writer (+ restore)",
            T(BM, 0x3DB2EA) == "movzx r14d, byte ptr [rdi + 0x12]" and T(BM, 0x3DB2EF) == "and r14d, 1" and
            T(BM, 0x3DB402) == "mov eax, r14d" and writers(BM, "r14") == [0x3DB2EA, 0x3DB2EF, 0x3DB405])
    loop = [0x3DB326, 0x3DB328, 0x3DB32B, 0x3DB32D, 0x3DB32F, 0x3DB334, 0x3DB337, 0x3DB33A, 0x3DB33F]
    R.check("non-head search: the loop 3DB326..3DB33F reloads edx = esi each turn (3DB326 `mov edx, esi`) and "
            "calls 003DB550 with the same index; rsi has no writer in it",
            T(BM, 0x3DB326) == "mov edx, esi" and BM[0x3DB32F].direct_target() == GETENT and
            not [a for a in loop if "rsi" in BM[a].reg_writes] and T(BM, 0x3DB33F) == "jne 0x3db326" and
            T(BM, 0x3DB337) == "movzx eax, byte ptr [rax]")
    R.check("003DB550 is pure: no memory write, no call; returns &entries[edx] or 0",
            not BG.mem_writes() and not BG.calls() and T(BG, 0x3DB56B) == "lea rax, [rax + rdx*4]")
    R.check("so a non-head index leaves the loop only to 3DB346 (its own +0 link == index) or to 3DB3FD "
            "(+0 link == FF); 3DB3FD reaches neither 3DC1B0 nor 3DC0D0",
            BM[0x3DB341].direct_target() == 0x3DB3FD and 0x3DB37D not in BM.reach(0x3DB3FD) and
            0x3DB346 not in BM.reach(0x3DB3FD))
    # ---------------- unhook 003DC1B0 ----------------
    R.check("003DC1B0 clears entry +11h: 3DC233 `mov byte ptr [r8 + 0x11], 0` dominates its ret; no call",
            T(BU, 0x3DC233) == "mov byte ptr [r8 + 0x11], 0" and BU.dominates(0x3DC233, 0x3DC238) and
            not BU.calls())
    # ---------------- post 003DC0D0 ----------------
    R.check("003DC0D0: rbx = entry (3DC0D6); 3587C0(dword +8, word +6) (3DC0D9..3DC0E0); NULL -> 3DC127 skips "
            "the 3DC122 call to 003DBCF0",
            T(BP, 0x3DC0D6) == "mov rbx, rdx" and T(BP, 0x3DC0D9) == "movzx edx, word ptr [rdx + 6]" and
            T(BP, 0x3DC0DD) == "mov ecx, dword ptr [rbx + 8]" and BP[0x3DC0E0].direct_target() == RESOLVE and
            T(BP, 0x3DC0E8) == "je 0x3dc127" and BP[0x3DC122].direct_target() == ALLOC and
            0x3DC122 not in BP.reach(0x3DC127) and T(BP, 0x3DC10B) == "mov rcx, rax")
    R.check("003587C0 returns NULL for a null table, a negative ordinal or ordinal >= count; else the slot",
            [T(BV, a) for a in (0x3587D2, 0x3587D9, 0x3587DB, 0x3587DD)] ==
            ["test rcx, rcx", "js 0x3587ea", "cmp ebx, dword ptr [rcx]", "jge 0x3587ea"] and
            T(BV, 0x3587EA) == "xor eax, eax")
    # ---------------- interpreter-free closure in front of the attempt ----------------
    before = {}
    before[RECYC[0]] = [t for a, t in BR.calls() if a < 0x3DB506]
    before[REMOVE] = [t for t in pc if t != POST]
    before[POST] = [BP[a].direct_target() for a in BP.order if BP[a].mnemonic == "call" and a < 0x3DC122]
    clos = {RECYC[0], REMOVE, POST}
    st = [UNHOOK, RESOLVE] + list(before[POST])
    while st:
        f = st.pop()
        if f in clos:
            continue
        clos.add(f)
        B = RB.get(f)
        if B is not None:
            st.extend(t for a, t in B.calls())
    leafs = [f for f in clos if f in RB and not RB[f].calls()]
    R.check("call closure in front of the 3DC122 attempt = {3DB420, 3DB2A0, 3DC1B0, 3DC0D0, 3587C0, 263FF0}: no "
            "0025E4C0 (interpreter), no indirect call, every callee below it is a leaf",
            clos == {RECYC[0], REMOVE, UNHOOK, POST, RESOLVE, SLOTARR} and INTERP not in clos and
            not any(indirect_calls(RB[f]) for f in clos if f in RB) and not indirect_calls(BR) and
            sorted(leafs) == [SLOTARR, UNHOOK], str(sorted("%X" % f for f in clos)))
    R.check("the recycler's own path from entry to 3DB506 contains no call", before[RECYC[0]] == [] and
            BR.calls()[0][0] == 0x3DB506)


def packet_files(img, R):
    """Packet-side checks kept out of checks() so a patched control image cannot fail on them alone."""
    db = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe()))))
    ev = os.path.join(db, "FFXII TZA", "_experiments", "evidence", SLUG)
    mism, got = [], []
    for f in ("source-01.json", os.path.join("retained", "source-01.json")):
        for r in json.load(open(os.path.join(ev, f)))["ranges"]:
            s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
            got.append((s_, e_))
            if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"]:
                mism.append(r["start"])
    need = [FREQ, FREQ2, RECYC] + RETAINED
    R.check("packet's %d captured/retained range sha256 values equal this image's bytes (all 11 bodies)" % len(got),
            not mism and sorted(got) == sorted(need), str(mism))
    ids = json.load(open(os.path.join(ev, "retained", "retained-body-identities.json")))["bodies"]
    bad = [b["entry"] for b in ids if hashlib.sha256(img.read(int(b["entry"], 16), b["length"])).hexdigest()
           != b["sha256"]]
    R.check("retained-body-identities: 8 bodies, 1041 B, each hash equals the image", len(ids) == 8 and not bad and
            sum(b["length"] for b in ids) == 1041, str(bad))
    uw = json.load(open(os.path.join(ev, "unwind-fragment-result-01.json")))
    rv = int(uw["record_va"], 16)
    R.check("unwind-fragment result: record at %s has the image's bytes, 28 B fragment hash equals the image"
            % uw["record_va"], img.read(rv, 12).hex() == uw["record_bytes"] and uw["fragment_bytes"] == 28 and
            hashlib.sha256(img.read(0x3DB420, 28)).hexdigest() == uw["fragment_sha256"])
    res = json.load(open(os.path.join(ev, "result-01.json")))
    rrd = res["facts"]["return_reaching_definitions"]
    R.check("result-01's return reaching definitions equal this review's ({3DB51A, 3DB53E} and {3DB545})",
            sorted(rrd["0x3db53d"]) == ["0x3db51a", "0x3db53e"] and rrd["0x3db54f"] == ["0x3db545"] and
            res["new_original_bytes"] == 426)
    pm = open(os.path.join(ev, "retained", "manifest.json"), "rb").read()
    pp = open(os.path.join(db, "FFXII TZA", "_experiments", "evidence", PARENT, "manifest.json"), "rb").read()
    R.check("retained/manifest.json is byte-identical to the parent packet %s's manifest.json" % PARENT, pm == pp,
            hashlib.sha256(pm).hexdigest()[:16])
    try:
        root = os.path.dirname(db)
        cm = subprocess.run(["git", "show", "%s:Database/FFXII TZA/_experiments/evidence/%s/manifest.json" %
                             (PRODUCER, SLUG)], cwd=root, capture_output=True).stdout
    except Exception:
        cm = b""
    R.check("the producer commit's manifest.json (git show %s) hashes to the same %s..." % (PRODUCER, MANIFEST_SHA[:16]),
            hashlib.sha256(cm).hexdigest() == MANIFEST_SHA, hashlib.sha256(cm).hexdigest()[:16])
    rd = open(os.path.join(ev, "README.md"), encoding="utf-8").read()
    R.check("README scopes the claim: head entry, mode-3 descriptor, non-8000 requester, flags 0/1 for the "
            "no-opaque composition, notification not proven admitted/delivered",
            "valid head entry" in rd and "mode-3" in rd and "non-8000" in rd and "flags 0/1" in rd and
            "admitted, delivered" in rd)


def rel32(at, size, tgt):
    return struct.pack("<i", tgt - (at + size))


CONTROLS = [
    ("3DB484 `cmovne r14d, r8d` -> `mov r14d, r8d; nop` (mode 4 no longer normalised)", 0x3DB484,
     bytes.fromhex("458BF090")),
    ("3DB44F `cmovns eax, edx` -> `cmovs eax, edx` (negative bound kept, positive dropped)", 0x3DB44F,
     bytes.fromhex("0F48C2")),
    ("3DB48B `jl` -> `jb` (unsigned range test)", 0x3DB48C, bytes([0x82])),
    ("3DB4CD `jne 3DB4DC` -> `je` (zero state selected)", 0x3DB4CD, bytes([0x74])),
    ("3DB50B `ror edi, 1` -> `jmp 3DB4B0` (re-walk the same channel after a removal)", 0x3DB50B, bytes.fromhex("EBA3")),
    ("3DB51A `mov eax, 1` -> `mov eax, 0` (loop-exit return no longer 1)", 0x3DB51A, bytes.fromhex("B800000000")),
    ("3DB457 `movzx r12d, word [rcx+6]` -> [rcx+4] (snapshot of another word)", 0x3DB45B, bytes([0x04])),
    ("3DB375 `jne 3DB382` -> `jmp 3DB382` (mode-3 post skipped)", 0x3DB375, bytes([0xEB])),
    ("3DB371 `cmp byte [rdi+0x10], 3` -> [rdi+0x11] (post gated on run state)", 0x3DB373, bytes([0x11])),
    ("3DC0E0 call 3587C0 -> call 0025E4C0 (interpreter in front of the attempt)", 0x3DC0E0, "INTERP"),
    ("3DB326 `mov edx, esi` -> `mov edx, eax` (removal search becomes a real walk)", 0x3DB326, bytes.fromhex("8BD0")),
    ("352991 `mov r8d, 4` -> `mov r8d, 3` (freqcancel passes mode 3)", 0x352993, bytes([0x03])),
    ("35368C `lea edx, [rdi+1]` -> `lea edx, [rdi]` (two-argument bound without +1)", 0x35368E, bytes([0x00])),
    ("3DB420 primary .pdata record end 3DB43C -> 3DB440 (records no longer tile the body)", 0x2FC24A8,
     struct.pack("<I", 0x3DB440 - 0x120000)),
]


def main():
    img = Img.load()
    R = Rep("rv_cancel")
    print("== packet integrity")
    check_manifest(R, SLUG, MANIFEST_SHA)
    print("== shipping-image re-derivation")
    checks(img, R)
    packet_files(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null control")
    Rn.quiet = True
    checks(img.patched(0x3DB51A, img.read(0x3DB51A, 5)), Rn)
    R.check("null control: an unchanged private copy (sha check off) passes every check", Rn.fails == 0 and Rn.n > 0,
            "%d of %d" % (Rn.n - Rn.fails, Rn.n))
    nctl = 0
    for label, va, nb in CONTROLS:
        if nb == "INTERP":
            nb = bytes([0xE8]) + rel32(va, 5, INTERP)
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
