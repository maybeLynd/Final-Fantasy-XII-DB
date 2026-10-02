"""rv_order.py - FABLE independent re-derivation for ASTRA packet notification-retirement-order (e46090c35).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the filecache-route2-commit-key review).  Does not
import ASTRA's prove.py, capture.py, control.py or the shared role adapter (reg_tracking.py).  Method: complete
linear decode of the eight bodies (four against .pdata, one of them a three-record chain; four leaves with no
record, bounded by their closed CFG, final ret and int3 / neighbouring-record padding), local CFGs from rvlib.Body,
dominance and post-dominance for the order claim, a census of every write that could reach actor+60h before the
notification attempt, the reviewer's own reverse reaching-definition walk for every return value that a claim
names, and exact descriptor/stack arithmetic for the posted descriptor.  The controls patch a private in-memory
copy of the image and require at least one named check to fail.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, SHA256 as SHA_PIN  # noqa: E402

SLOT = (0x00263FF0, 0x00264005)    # actor-slot table address leaf, 21 B
RESOLVE = (0x003587C0, 0x003587F2)  # requester resolve, 50 B
REM = (0x003DB2A0, 0x003DB41A)     # ActorResource_RemoveActiveEntry, 378 B
ORD = (0x003DB550, 0x003DB573)     # GetEntryByOrdinal leaf, 35 B
REL = (0x003DB650, 0x003DB6D5)     # free-list relink leaf, 133 B
ALLOC = (0x003DBCF0, 0x003DBDB2)   # AllocateAndSubmitEntry, 194 B (three chained .pdata records)
POST = (0x003DC0D0, 0x003DC12D)    # end-notification post, 93 B
UNL = (0x003DC1B0, 0x003DC239)     # link unhook leaf, 137 B
ALL = [SLOT, RESOLVE, REM, ORD, REL, ALLOC, POST, UNL]
PDATA_BODIES = [RESOLVE, REM, POST]
LEAVES = [SLOT, ORD, REL, UNL]
SLUG = "notification-retirement-order"
PRODUCER = "e46090c35"
MANIFEST_SHA = "814b83ad013385518de8a269ee75b4ac949ba574ad8b998940231065edb0f7cd"


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


def rets_of(B):
    return [a for a in B.order if B[a].mnemonic == "ret"]


def rdefs(B, at, fam):
    """Reviewer's reverse reaching-definition walk: the instructions whose write of register family `fam`
    reaches `at` along some local path.  A call is a definition (volatile clobber); reaching the entry with no
    definition yields 'entry'."""
    P = preds(B)
    out, seen = set(), set()
    st = list(P.get(at, ()))
    if at == B.start:
        out.add("entry")
    while st:
        a = st.pop()
        if a in seen:
            continue
        seen.add(a)
        I = B[a]
        if fam in I.reg_writes or I.mnemonic == "call":
            out.add(a)
            continue
        if a == B.start:
            out.add("entry")
        st.extend(P.get(a, ()))
    return out


def postdominates(B, p, a):
    """Every path from a to any ret passes p (a != p)."""
    r = B.reach(a, avoid=[p])
    return not [x for x in r if B[x].mnemonic == "ret"]


def bodies(img):
    return dict((s, Body(img, s, e)) for s, e in ALL)


def checks(img, R):
    Bs = bodies(img)
    SL, RS, RM, OD, RL, AL, PS, UN = (Bs[s] for s, e in ALL)

    # ---------------- bodies ----------------
    tot = 0
    for s, e in PDATA_BODIES:
        ents, ok = img.pdata_cover(s, e)
        R.check("body %08X + 0x%X (%d B) decodes exactly and one .pdata record covers it exactly (%s)" %
                (s, e - s, e - s, ",".join("%08X+0x%X fl%d" % (b, en - b, fl) for b, en, fl, rt in ents)),
                Bs[s].exact and ok and len(ents) == 1)
        tot += e - s
    s, e = ALLOC
    ents, ok = img.pdata_cover(s, e)
    R.check("body 003DBCF0 + 0xC2 (194 B) decodes exactly; three .pdata records tile it, the first unchained at the "
            "entry and both later ones CHAININFO records rooted at 003DBCF0 (%s)" %
            ",".join("%08X+0x%X fl%d root %08X" % (b, en - b, fl, rt) for b, en, fl, rt in ents),
            AL.exact and ok and len(ents) == 3 and [x[0] for x in ents] == [0x3DBCF0, 0x3DBD21, 0x3DBD47])
    tot += e - s
    for s, e in LEAVES:
        B = Bs[s]
        before = img.read(s - 1, 1)
        prev_rec = img.pdata(s - 1)
        nx = e
        while img.read(nx, 1) == b"\xcc":
            nx += 1
        ents, ok = img.pdata_cover(s, e)
        R.check("leaf %08X + 0x%X (%d B) decodes exactly; no .pdata record begins in or covers it; before entry: %s; "
                "after the last ret: %d B int3" % (s, e - s, e - s,
                                                    "int3" if before == b"\xcc" else
                                                    ("a record ending at the entry" if prev_rec and prev_rec[1] == s
                                                     else "ret byte"), nx - e),
                B.exact and not ents and img.pdata(s) is None and img.pdata(e - 1) is None and
                (before == b"\xcc" or (prev_rec and prev_rec[1] == s) or before == b"\xc3") and nx - e >= 1 and
                B[B.order[-1]].mnemonic == "ret")
        tot += e - s
    R.check("eight bodies total 1041 B (21 + 50 + 378 + 35 + 133 + 194 + 93 + 137)", tot == 1041, str(tot))
    for s, e in ALL:
        rets, tails, outs = Bs[s].exits()
        R.check("%08X local CFG closed: no tail or out-of-body branch; last instruction is a ret (rets %s)" %
                (s, ",".join("%X" % x for x in rets)),
                not tails and not outs and rets and rets[-1] == Bs[s].order[-1])

    # ---------------- removal 003DB2A0: entry, flags, selection ----------------
    R.check("3DB2A0: rsi = movsxd edx (index), rbx = rcx (actor); index 0xFF -> 3DB2B8 `mov eax, 1` and ret 3DB2C7",
            T(RM, 0x3DB2AA) == "movsxd rsi, edx" and T(RM, 0x3DB2AD) == "mov rbx, rcx" and
            T(RM, 0x3DB2B0) == "cmp esi, 0xff" and T(RM, 0x3DB2B6) == "jne 0x3db2c8" and
            T(RM, 0x3DB2B8) == "mov eax, 1" and RM.reach(0x3DB2B8) & set(rets_of(RM)) == {0x3DB2C7})
    R.check("3DB2A0: entry = [actor+0A0h] + index*20 (3DB2D7..3DB2E2, 14h-byte entries) held in rdi",
            [T(RM, a) for a in (0x3DB2D7, 0x3DB2DE, 0x3DB2E2)] ==
            ["mov rax, qword ptr [rbx + 0xa0]", "lea rcx, [rsi + rsi*4]", "lea rdi, [rax + rcx*4]"])
    R.check("3DB2A0: rdi written only at 3DB2E2, 3DB2E8 (null actor), 3DB334 (non-head walk) and the restore 3DB3FD",
            writers(RM, "rdi") == [0x3DB2E2, 0x3DB2E8, 0x3DB334, 0x3DB3FD],
            str(["%X" % x for x in writers(RM, "rdi")]))
    R.check("3DB2A0: r14d = byte entry+12h AND 1 (3DB2EA movzx, 3DB2EF and), read before any call",
            T(RM, 0x3DB2EA) == "movzx r14d, byte ptr [rdi + 0x12]" and T(RM, 0x3DB2EF) == "and r14d, 1" and
            not [a for a in RM.order if a < 0x3DB2EA and RM[a].mnemonic == "call"])
    R.check("3DB2A0: r14 written only at 3DB2EA, 3DB2EF and the restore 3DB405",
            writers(RM, "r14") == [0x3DB2EA, 0x3DB2EF, 0x3DB405], str(["%X" % x for x in writers(RM, "r14")]))
    rd = {}
    for r in rets_of(RM):
        rd[r] = rdefs(RM, r, "rax")
    R.check("3DB2A0 return EAX (own reverse reaching definitions): ret 3DB2C7 <- 3DB2B8 `mov eax, 1` only; ret 3DB419 "
            "<- 3DB402 `mov eax, r14d` only",
            rd.get(0x3DB2C7) == {0x3DB2B8} and rd.get(0x3DB419) == {0x3DB402} and
            T(RM, 0x3DB402) == "mov eax, r14d" and len(rd) == 2,
            str(dict(("%X" % k, sorted("%X" % x if isinstance(x, int) else x for x in v)) for k, v in rd.items())))
    R.check("3DB2A0: mode byte entry+10h == 4 -> ebp = -1 (3DB311); else rbp = signed byte entry+2 (channel), "
            "negative -> actor+61h list (3DB314), else head = byte [rbp+rbx+94h]",
            T(RM, 0x3DB2F8) == "cmp byte ptr [rdi + 0x10], 4" and T(RM, 0x3DB2FC) == "je 0x3db311" and
            T(RM, 0x3DB2FE) == "movsx rbp, byte ptr [rdi + 2]" and T(RM, 0x3DB305) == "js 0x3db314" and
            T(RM, 0x3DB307) == "movzx ecx, byte ptr [rbp + rbx + 0x94]" and T(RM, 0x3DB311) == "or ebp, 0xffffffff"
            and T(RM, 0x3DB314) == "movzx ecx, byte ptr [rbx + 0x61]")
    R.check("3DB2A0: head == index -> 3DB32B `cmp esi, eax` / 3DB32D `je 0x3db346` with eax = the list head "
            "(3DB318); a 0xFF head exits to 3DB3FD with no unlink",
            T(RM, 0x3DB318) == "movzx eax, cl" and T(RM, 0x3DB320) == "je 0x3db3fd" and
            T(RM, 0x3DB32B) == "cmp esi, eax" and T(RM, 0x3DB32D) == "je 0x3db346" and
            0x3DB346 not in RM.reach(0x3DB3FD))
    R.check("3DB346 `call 0x3dc1b0` (unhook) with rcx = actor, edx = index; it dominates the notification call 3DB37D",
            RM[0x3DB346].direct_target() == UNL[0] and T(RM, 0x3DB326) == "mov edx, esi" and
            T(RM, 0x3DB328) == "mov rcx, rbx" and RM.dominates(0x3DB346, 0x3DB37D))
    R.check("notification gate: 3DB34D `jns` (channel >= 0), 3DB36B 16-bit `cmp word [rdi+6], 8000h` / `je` skip, "
            "3DB371 `cmp byte [rdi+10h], 3` / `jne` skip; then rdx = entry, rcx = actor, 3DB37D call 3DC0D0",
            T(RM, 0x3DB34D) == "jns 0x3db366" and T(RM, 0x3DB366) == "mov eax, 0x8000" and
            T(RM, 0x3DB36B) == "cmp word ptr [rdi + 6], ax" and RM[0x3DB36B].mems[0]["size"] == 2 and
            T(RM, 0x3DB36F) == "je 0x3db382" and T(RM, 0x3DB371) == "cmp byte ptr [rdi + 0x10], 3" and
            T(RM, 0x3DB375) == "jne 0x3db382" and T(RM, 0x3DB377) == "mov rdx, rdi" and
            T(RM, 0x3DB37A) == "mov rcx, rbx" and RM[0x3DB37D].direct_target() == POST[0])
    R.check("the negative-channel / mode-4 branch (3DB34F) reaches the relink without any notification call",
            0x3DB37D not in RM.reach(0x3DB34F) and 0x3DB3F0 in RM.reach(0x3DB34F))
    R.check("3DB37D's result is discarded: 3DB382 `movzx eax, byte ptr [rdi + 0x12]` rewrites eax next",
            RM.order[RM.order.index(0x3DB37D) + 1] == 0x3DB382 and T(RM, 0x3DB382) == "movzx eax, byte ptr [rdi + 0x12]")
    R.check("order: relink 3DB3F0 `call 0x3db650` and head publish 3DB3F9 `mov byte ptr [rbx + 0x60], sil` "
            "post-dominate the attempt's return 3DB382; 3DB3F0 precedes 3DB3F9 on every path",
            RM[0x3DB3F0].direct_target() == REL[0] and T(RM, 0x3DB3F9) == "mov byte ptr [rbx + 0x60], sil" and
            postdominates(RM, 0x3DB3F0, 0x3DB382) and postdominates(RM, 0x3DB3F9, 0x3DB382) and
            RM.dominates(0x3DB3F0, 0x3DB3F9))
    R.check("no path returns from 3DB3F0/3DB3F9 to the attempt (3DB37D unreachable from the relink)",
            0x3DB37D not in RM.reach(0x3DB3F0) and 0x3DB346 not in RM.reach(0x3DB3F0))
    R.check("relink arguments: 3DB3E6 edx = byte actor+60h (current free head), 3DB3EA r8d = index, rcx = actor",
            T(RM, 0x3DB3E6) == "movzx edx, byte ptr [rbx + 0x60]" and T(RM, 0x3DB3EA) == "mov r8d, esi" and
            T(RM, 0x3DB3ED) == "mov rcx, rbx")
    pre = RM.reach(RM.start, avoid=[0x3DB37D]) - RM.reach(0x3DB382)
    w60 = [(a, m["base"], m["disp"]) for a in sorted(pre) for m in RM[a].mems
           if m["write"] and m["base"] != "rsp" and m["disp"] <= 0x60 < m["disp"] + m["size"]]
    wact = [(a, m["base"], m["disp"]) for a, m in RM.mem_writes() if m["base"] == "rbx" and m["disp"] == 0x60]
    R.check("census: before the attempt the removal writes nothing that overlaps actor+60h; its only actor+60h "
            "write in the whole body is 3DB3F9", not w60 and wact == [(0x3DB3F9, "rbx", 0x60)], str(w60 + wact))
    R.check("flags: 3DB386 `cmp al, 2` / 3DB388 `jb` (unsigned) skips 3DB392 `call 0x263050` for flags 0/1; "
            "edx = flags >> 1; 263050 lies after the attempt",
            T(RM, 0x3DB386) == "cmp al, 2" and T(RM, 0x3DB388) == "jb 0x3db397" and
            T(RM, 0x3DB390) == "shr edx, 1" and RM[0x3DB392].direct_target() == 0x263050 and
            not RM.dominates(0x3DB392, 0x3DB3F9) and 0x3DB37D not in RM.reach(0x3DB392) and
            RM.dominates(0x3DB386, 0x3DB392))
    R.check("non-head walk: 3DB326 `mov edx, esi` passes the removed index, not the walked index, to 3DB550 on every "
            "iteration (3DB33F `jne 0x3db326`)",
            T(RM, 0x3DB33F) == "jne 0x3db326" and RM[0x3DB32F].direct_target() == ORD[0] and
            T(RM, 0x3DB334) == "mov rdi, rax" and T(RM, 0x3DB337) == "movzx eax, byte ptr [rax]")

    # ---------------- unhook 003DC1B0 ----------------
    uw = [(a, m["base"], m["disp"], m["size"]) for a, m in UN.mem_writes()]
    R.check("3DC1B0 writes three bytes, all through entry-pool pointers derived from [actor+0A0h]: 3DC220 "
            "next.prev = prev, 3DC230 prev.next = next, 3DC233 entry+11h = 0; nothing through the actor (r9)",
            uw == [(0x3DC220, "rax", 1, 1), (0x3DC230, "r10", 0, 1), (0x3DC233, "r8", 0x11, 1)] and
            T(UN, 0x3DC233) == "mov byte ptr [r8 + 0x11], 0" and T(UN, 0x3DC1B3) == "mov r9, rcx" and
            writers(UN, "r9") == [0x3DC1B3], str(uw))
    R.check("3DC1B0: the entry+11h clear 3DC233 dominates its single ret; there are no calls",
            UN.dominates(0x3DC233, 0x3DC238) and rets_of(UN) == [0x3DC238] and not UN.calls())
    rw = [(a, m["base"], m["disp"]) for a, m in RL.mem_writes()]
    R.check("3DB650 relink writes only entry bytes (bases r8/r9/r10 from [actor+0A0h]); no actor field, no calls",
            rw and all(b in ("r8", "r9", "r10") for a, b, d in rw) and not RL.calls(), str(rw))

    # ---------------- post 003DC0D0 ----------------
    R.check("3DC0D0: rbx = entry; edx = word entry+6 zero-extended (requester), ecx = dword entry+8; call 3587C0; "
            "a NULL requester skips the post (3DC0E8 `je 0x3dc127`)",
            T(PS, 0x3DC0D6) == "mov rbx, rdx" and T(PS, 0x3DC0D9) == "movzx edx, word ptr [rdx + 6]" and
            T(PS, 0x3DC0DD) == "mov ecx, dword ptr [rbx + 8]" and PS[0x3DC0E0].direct_target() == RESOLVE[0] and
            T(PS, 0x3DC0E8) == "je 0x3dc127" and 0x3DC122 not in PS.reach(0x3DC127))
    sw = sorted((m["disp"], m["size"], a) for a, m in PS.mem_writes() if m["base"] == "rsp")
    dw = PS[0x3DC115]
    fid = struct.pack("<I", dw.imm[0] & 0xFFFFFFFF)[0:2] if dw.imm else b"??"
    R.check("3DC0D0 descriptor at [rsp+20h]: +0 word 402h, +2 byte entry+3, +4 dword 80000000h (WORD at +4 = 0, the "
            "function id), +8 byte 1, +0Ch entry+8, +10h entry+0Ch; no other store overlaps +4..+5",
            T(PS, 0x3DC10E) == "mov word ptr [rsp + 0x20], 0x402" and
            T(PS, 0x3DC0F3) == "mov byte ptr [rsp + 0x22], cl" and T(PS, 0x3DC0EA) == "movzx ecx, byte ptr [rbx + 3]"
            and dw.text == "mov dword ptr [rsp + 0x24], 0x80000000" and fid == b"\x00\x00" and
            T(PS, 0x3DC11D) == "mov byte ptr [rsp + 0x28], 1" and T(PS, 0x3DC107) == "mov dword ptr [rsp + 0x2c], ecx"
            and T(PS, 0x3DC100) == "mov dword ptr [rsp + 0x30], ecx" and
            [a for d, sz, a in sw if d < 0x26 and d + sz > 0x24] == [0x3DC115], str(sw))
    R.check("3DC122 `call 0x3dbcf0` with rcx = requester (rax), rdx = &descriptor, r8d = 1; return 3DC127 is the call "
            "origin",
            PS[0x3DC122].direct_target() == ALLOC[0] and T(PS, 0x3DC10B) == "mov rcx, rax" and
            T(PS, 0x3DC0EE) == "lea rdx, [rsp + 0x20]" and T(PS, 0x3DC0F7) == "mov r8d, 1" and
            not writers(PS, "rdx", 0x3DC0EF, 0x3DC122) and 0x3DC122 + 5 == 0x3DC127)
    R.check("3DC0D0 writes only its own stack (the descriptor)", all(m["base"] == "rsp" for a, m in PS.mem_writes()))
    R.check("3587C0: requester = [list + 8 + index*8] where list = [slot+8], slot = 2098E10h + (int)entry+8 * 288h; "
            "NULL list, negative or out-of-range index (signed jge vs dword [list]) -> 0",
            [T(RS, a) for a in (0x3587C6, 0x3587CE, 0x3587D5, 0x3587D9, 0x3587DB, 0x3587DD, 0x3587DF, 0x3587EA)] ==
            ["movsxd rbx, edx", "mov rcx, qword ptr [rax + 8]", "je 0x3587ea", "js 0x3587ea",
             "cmp ebx, dword ptr [rcx]", "jge 0x3587ea", "mov rax, qword ptr [rcx + rbx*8 + 8]", "xor eax, eax"] and
            RS[0x3587C9].direct_target() == SLOT[0] and
            [T(SL, a) for a in (0x263FF0, 0x263FFA)] == ["movsxd rax, ecx", "imul rax, rax, 0x288"] and
            SL[0x263FF3].mems[0]["disp"] + 0x263FFA == 0x2098E10)
    R.check("3587C0 / 263FF0 / 3DB550 write no memory (stack pushes only)",
            not [1 for B in (RS, SL, OD) for a, m in B.mem_writes() if m["base"] != "rsp"])

    # ---------------- allocation 003DBCF0 ----------------
    R.check("3DBCF0 admission: rax = [actor+48h] (function table), r9d = word descriptor+4 (function id), "
            "3DBD0C `cmp r9d, dword ptr [rax]` / 3DBD0F `jb` (unsigned): id >= count -> eax = 3 (3DBD11), ret 3DBD20",
            T(AL, 0x3DBCFA) == "mov rax, qword ptr [rcx + 0x48]" and T(AL, 0x3DBD01) == "movzx r9d, word ptr [rdx + 4]"
            and T(AL, 0x3DBD0C) == "cmp r9d, dword ptr [rax]" and T(AL, 0x3DBD0F) == "jb 0x3dbd21" and
            T(AL, 0x3DBD11) == "mov eax, 3" and AL.reach(0x3DBD11) & set(rets_of(AL)) == {0x3DBD20})
    R.check("3DBCF0 capacity: 3DBD26 `movzx edi, byte ptr [rcx + 0x60]` (rcx = incoming actor, unwritten before it) "
            "/ `cmp edi, 0xff` / 3DBD30 `jne`: FF -> eax = 2 (3DBD32), ret 3DBD46",
            T(AL, 0x3DBD26) == "movzx edi, byte ptr [rcx + 0x60]" and T(AL, 0x3DBD2A) == "cmp edi, 0xff" and
            T(AL, 0x3DBD30) == "jne 0x3dbd47" and T(AL, 0x3DBD32) == "mov eax, 2" and
            not writers(AL, "rcx", AL.start, 0x3DBD26) and AL.reach(0x3DBD32) & set(rets_of(AL)) == {0x3DBD46})
    R.check("function-0 admission precedes capacity: 3DBD0C dominates 3DBD26, and no path reaches 3DBD26 from 3DBD11",
            AL.dominates(0x3DBD0C, 0x3DBD26) and 0x3DBD26 not in AL.reach(0x3DBD11))
    p3 = AL.reach(AL.start) - AL.reach(0x3DBD21)
    p2 = AL.reach(AL.start, avoid=[0x3DBD47]) - p3 | set()
    p2 = set(a for a in AL.reach(AL.start, avoid=[0x3DBD47, 0x3DBD11]))
    bad3 = [a for a in p3 if AL[a].mnemonic == "call" or any(m["write"] and m["base"] != "rsp" for m in AL[a].mems)]
    bad2 = [a for a in p2 if AL[a].mnemonic == "call" or any(m["write"] and m["base"] != "rsp" for m in AL[a].mems)]
    R.check("the result-3 and result-2 paths make no call and write only the own stack home slots",
            not bad3 and not bad2 and 0x3DBD46 in p2 and 0x3DBD20 in p3, str(["%X" % x for x in bad3 + bad2]))
    ad = dict((r, rdefs(AL, r, "rax")) for r in rets_of(AL))
    R.check("3DBCF0 return EAX (own reverse reaching definitions): 3DBD20 <- 3DBD11, 3DBD46 <- 3DBD32, 3DBDB1 <- "
            "3DBDA0 `mov eax, ebp` (ebp = 3DB7A0 result, 3DBD64)",
            ad == {0x3DBD20: {0x3DBD11}, 0x3DBD46: {0x3DBD32}, 0x3DBDB1: {0x3DBDA0}} and
            T(AL, 0x3DBDA0) == "mov eax, ebp" and T(AL, 0x3DBD64) == "mov ebp, eax" and
            AL[0x3DBD5F].direct_target() == 0x3DB7A0, str(dict(("%X" % k, sorted("%X" % x for x in v if isinstance(x, int))) for k, v in ad.items())))
    cl = [("%X" % a, "%X" % t) for a, t in AL.calls()]
    R.check("a non-FF free head reaches the insertion helpers: 3DBD4E 3DC130, 3DBD5F 3DB7A0, then only when that "
            "returns 3: 3DBD75 3DB650, 3DBD82 263FF0, 3DBD96 263E40",
            cl == [("3DBD4E", "3DC130"), ("3DBD5F", "3DB7A0"), ("3DBD75", "3DB650"), ("3DBD82", "263FF0"),
                   ("3DBD96", "263E40")] and T(AL, 0x3DBD66) == "cmp eax, 3" and T(AL, 0x3DBD69) == "jne 0x3dbd9b",
            str(cl))

    # ---------------- composition ----------------
    pw = [a for B in (UN, OD, PS, RS, SL) for a, m in B.mem_writes() if m["base"] in ("r9", "rcx") and
          m["disp"] <= 0x60 < m["disp"] + m["size"]]
    R.check("composition: between removal entry and 3DBD26 nothing writes actor+60h through the actor pointer "
            "(removal census above; 3DC1B0, 3DB550, 3DC0D0, 3587C0 and 263FF0 write no actor field), so with the "
            "requester resolving to the same actor the capacity byte read at 3DBD26 is actor+60h as at removal entry",
            not pw and not w60)


def git_manifest_sha():
    exe = find_exe()
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(exe)))))
    rel = "Database/FFXII TZA/_experiments/evidence/%s/manifest.json" % SLUG
    out = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (PRODUCER, rel)], capture_output=True)
    return hashlib.sha256(out.stdout).hexdigest() if out.returncode == 0 else "git show failed"


def packet_checks(img, R):
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    g = git_manifest_sha()
    R.check("committed manifest at %s hashes as the working-tree manifest" % PRODUCER, g == MANIFEST_SHA, g)
    mism, got = [], []
    for r in json.load(open(os.path.join(ev, "source-01.json")))["ranges"]:
        s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
        got.append((s_, e_))
        if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"]:
            mism.append(r["start"])
    R.check("packet's captured range sha256 values equal this image's bytes (%d ranges = the eight bodies)" % len(got),
            not mism and sorted(got) == sorted(ALL), str(mism))
    ri = json.load(open(os.path.join(ev, "retained-body-identities.json")))["bodies"]
    bad = [b["entry"] for b in ri if hashlib.sha256(img.read(int(b["entry"], 16), b["length"])).hexdigest()
           != b["sha256"]]
    R.check("retained-body-identities: %d bodies, lengths sum 1041, each sha256 equals the image" % len(ri),
            not bad and sum(b["length"] for b in ri) == 1041 and len(ri) == 8, str(bad))
    res = json.load(open(os.path.join(ev, "result-01.json")))
    R.check("result-01 names the order 3DB346 -> 3DB37D/3DC122 -> 3DB3F0 -> 3DB3F9 and limits flags >= 2 to 263050",
            [x.split()[0] for x in res["facts"]["order"]] == ["003DB346", "003DB37D", "003DB3F0", "003DB3F9"] and
            "263050" in res["facts"]["excluded"])


CONTROLS = [
    ("3DB37D `call 0x3dc0d0` -> five nops (no attempt)", 0x3DB37D, bytes([0x90] * 5)),
    ("3DB2F3 `mov [rsp+30h], rbp` -> `mov [rbx+60h], sil; nop` (slot published before the attempt)", 0x3DB2F3,
     bytes.fromhex("4088736090")),
    ("3DB3A6 `jne 3DB3D1` -> `jne 3DB3FD` (a path after the attempt skips relink and publish)", 0x3DB3A6,
     bytes.fromhex("7555")),
    ("3DB2EF `and r14d, 1` -> `and r14d, 3` (return no longer bit 0)", 0x3DB2EF, bytes.fromhex("4183e603")),
    ("3DB402 `mov eax, r14d` -> `nop; mov eax, ebp` (return from another carrier)", 0x3DB402, bytes.fromhex("908bc5")),
    ("3DC115 descriptor dword 80000000h -> 80000001h (function id 1)", 0x3DC119, bytes.fromhex("01000080")),
    ("3DBD0F `jb` -> `jl` (signed admission compare)", 0x3DBD0F, bytes([0x7C])),
    ("3DBD30 `jne 3DBD47` -> `je 3DBD47` (FF head admitted)", 0x3DBD30, bytes([0x74])),
    ("3DBD32 `mov eax, 2` -> `call 3DC130` (a call on the full-pool path)", 0x3DBD32,
     b"\xe8" + struct.pack("<i", 0x3DC130 - (0x3DBD32 + 5))),
    ("3DC233 `mov byte [r8+11h], 0` -> [r8+12h]", 0x3DC236, bytes([0x12])),
    ("3DB371 `cmp byte [rdi+10h], 3` -> 4 (mode gate)", 0x3DB374, bytes([0x04])),
    ("3DB388 `jb 3DB397` -> two nops (263050 for flags 0/1)", 0x3DB388, bytes.fromhex("9090")),
    ("3DC220 `mov [rax+1], r11b` -> `mov [r9+60h], r11b` (unhook writes the free head)", 0x3DC220,
     bytes.fromhex("45885960")),
    ("3DBD26 `movzx edi, byte [rcx+60h]` -> [rcx+61h]", 0x3DBD29, bytes([0x61])),
    ("3DB366 `mov eax, 8000h` -> 8001h (requester sentinel)", 0x3DB367, bytes([0x01])),
]


def main():
    img = Img.load()
    R = Rep("rv_order")
    print("== packet integrity")
    check_manifest(R, SLUG, MANIFEST_SHA)
    packet_checks(img, R)
    print("== shipping-image re-derivation")
    checks(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null control")
    Rn.quiet = True
    same = img.patched(0x3DB2A0, img.read(0x3DB2A0, 4))
    checks(same, Rn)
    R.check("null control: an unchanged private copy (sha check off) passes every check", Rn.fails == 0 and Rn.n > 0,
            "%d of %d" % (Rn.n - Rn.fails, Rn.n))
    nctl = 0
    for label, va, nb in CONTROLS:
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
