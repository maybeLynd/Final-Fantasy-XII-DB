"""check.py - FABLE byte check for the UQ-147 consumption clauses (FABLE, 2026-10-03).

Checks every site the three staged clauses cite, at the shipping image (sha256 pinned by rvlib), with FABLE's own
reader (rvlib.py from fable-review-astra-ov42-caller-quotient-bound-1002, imported unchanged; struct + capstone only).
It does not run or import ASTRA's producers or the shared role adapter.

Groups (each a function over an image, so a control can rerun it on a patched private copy):
  A  Dismiss stage   - classifier quotient 275 -> kind 2; kind table; the conditional +0x5B04 bit-0 clear at 00306A81
                       precedes the routine's only direct 022C2160 write (state 5) at 00306ADF; kind 1 sets the bit.
  B  defeat leg      - 0030111C xor / 0030111E call 003138D0 / 00301123 call 0023B040 straight-line under the gates.
  C  seam and tail   - 0031395D is 003138D0's one seam call; 00311CF0's 0x113 refusal and +0x5AD0 bit-0 clear (CS-1,
                       OPUS); no commit-field write; 00317E60's own write at 00317E9A and call 0033C9B0; 0025AAD0(1,0)
                       skips five publication stores and 002F1710; no direct call to 00306760, no +0x5B04 write.
  D  selector        - 0031B8C0(3) -> 00263750 -> 0209A208 -> 00263E30 (+0x30): no writes, no other calls, no status
                       read.
  E  mode query      - 0030D9A0 reads [[02EBF190]+0x5B04] twice around 00377C20; the 133-byte chain writes nothing and
                       calls only its own chain; field cell 021654C4, signed clamp, descriptor NULL / >= count -> 0,
                       bit 15.
  F  early return    - 003138D0's NULL-slot and 0x113 exits skip 0031395D and 00313981; the 0031B7E0-NULL exits skip
                       the seam but not the 00313981 write.
Plus the three evidence manifests (hashes SWE2-AUDIT-SPEC recorded), and eleven controls, each a patched private copy
of the image (the exe on disk is never written) that must make its group FAIL. Prints FAILS N last.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img, Body, Report, expect, run_control, check_manifest  # noqa: E402

BASE = 0x120000
BATTLE = 0x2EBF190
KIND, STATE = 0x22C215C, 0x22C2160


def rip_target(I):
    for m in I.mems:
        if m["base"] == "rip":
            return I.address + I.size + m["disp"]
    return None


def nonstack_writes(B, addrs=None):
    out = []
    for a in B.order:
        if addrs is not None and a not in addrs:
            continue
        for m in B[a].mems:
            if m["write"] and m["base"] not in ("rsp",) and B[a].mnemonic not in ("push", "call"):
                out.append(a)
    return out


# ---------------------------------------------------------------- A
def grp_dismiss(img, R):
    # classifier tail 00306C5B..00306CEC
    C = Body(img, 0x306C5B, 0x306CEC)
    R.check("A classifier body 00306C5B-00306CEC decodes exactly", C.exact)
    expect(R, C, 0x306C82, "div ecx")
    expect(R, C, 0x306C84, "add eax, 0xffffff6c")
    expect(R, C, 0x306C89, "cmp eax, 0x7f")
    sel = img.read(0x306D08 + (0x113 - 0x94), 1)[0]
    R.check("A quotient 0x113 -> map byte [00306D08+127] = 5", sel == 5, "got %d" % sel)
    tgt = img.u32(0x306CEC + 4 * sel) + BASE
    R.check("A jump entry 5 -> 00306CB0", tgt == 0x306CB0, "%X" % tgt)
    expect(R, C, 0x306CB0, "mov ebx, 2")
    R.check("A 00306CDB stores EBX to the kind word 022C215C",
            C[0x306CDB].text.endswith(", ebx") and rip_target(C[0x306CDB]) == KIND)
    # dispatch and kind table
    D = Body(img, 0x306760, 0x306AEF)
    R.check("A 00306760-00306AEF decodes exactly (911 B, stops before the 00306AF0 table)", D.exact)
    R.check("A 003067AA reads the kind word", rip_target(D[0x3067AA]) == KIND and not D[0x3067AA].mems[0]["write"])
    expect(R, D, 0x3067B0, "dec eax")
    t = [img.u32(0x306AF0 + 4 * i) + BASE for i in range(6)]
    R.check("A kind table: kind 1 -> 00306931, kind 2 -> 00306A3D", t[0] == 0x306931 and t[1] == 0x306A3D,
            " ".join("%X" % x for x in t))
    # the kind-2 arm
    expect(R, D, 0x306A44, "test byte ptr [rax + 0x5ad0], 1")
    expect(R, D, 0x306A4F, "call 0x35dae0")
    expect(R, D, 0x306A68, "call 0x306d90")
    R.check("A 00306A6D reloads [02EBF190]", rip_target(D[0x306A6D]) == BATTLE)
    expect(R, D, 0x306A74, "mov eax, dword ptr [rcx + 0x5b04]")
    expect(R, D, 0x306A7A, "test al, 1")
    expect(R, D, 0x306A7C, "je 0x306a95")
    expect(R, D, 0x306A7E, "and eax, 0xfffffffe")
    I = D.ins.get(0x306A81)
    R.check("A 00306A81 is a dword store to [rcx+0x5B04] (the mode word)",
            I is not None and I.mems and I.mems[0]["write"] and I.mems[0]["base"] == "rcx"
            and I.mems[0]["disp"] == 0x5B04 and I.mems[0]["size"] == 4)
    expect(R, D, 0x306A87, "call 0x35c620")
    expect(R, D, 0x306798, "call 0x3098d0")
    expect(R, D, 0x3067A5, "call 0x3299b0")
    expect(R, D, 0x306A9A, "call 0x236850")
    expect(R, D, 0x306AA3, "call 0x236820")
    expect(R, D, 0x306AC0, "and dword ptr [rax], 0xfffffcff")
    expect(R, D, 0x306AC6, "lea rax, [rax + 0xf50]")
    expect(R, D, 0x306AD3, "mov ecx, 3")
    expect(R, D, 0x306AD8, "call 0x332130")
    J = D.ins.get(0x306ADF)
    R.check("A 00306ADF writes the immediate 5 to the state word 022C2160",
            J is not None and rip_target(J) == STATE and J.mems[0]["write"] and J.imm and J.imm[-1] == 5)
    # order on the arm's CFG
    reach81 = D.reach(0x306A81)
    R.check("A 00306ADF is reachable after 00306A81", 0x306ADF in reach81)
    R.check("A 00306A81 is not reachable after 00306ADF", 0x306A81 not in D.reach(0x306ADF))
    R.check("A bit-already-clear path reaches 00306ADF without 00306A81",
            0x306ADF in D.reach(0x306A3D, avoid=[0x306A81]))
    # census over the whole body: who touches 022C2160 and +0x5B04
    st = [(a, D[a].mems[0]["write"]) for a in D.order if rip_target(D[a]) == STATE]
    R.check("A census: the only reference to 022C2160 in 00306760 is the write at 00306ADF",
            st == [(0x306ADF, True)], str([("%X" % a, w) for a, w in st]))
    mw = [a for a in nonstack_writes(D) if any(m["disp"] == 0x5B04 for m in D[a].mems)]
    R.check("A census: +0x5B04 writers in 00306760 are 00306949 (kind 1, bit 0), 00306A16 (kind 5, bit 1), 00306A81"
            " (kind 2)", mw == [0x306949, 0x306A16, 0x306A81], str(["%X" % a for a in mw]))
    arm = D.reach(0x306A3D)
    R.check("A on the kind-2 arm the only +0x5B04 writer is 00306A81", [a for a in mw if a in arm] == [0x306A81])
    expect(R, D, 0x306946, "or ecx, 1")
    expect(R, D, 0x306A13, "or ecx, 2")


# ---------------------------------------------------------------- B
def grp_defeat(img, R):
    F = Body(img, 0x300FC0, 0x301133)
    R.check("B 00300FC0-00301133 decodes exactly (371 B)", F.exact)
    for a, s in [(0x3010F6, "test edi, edi"), (0x3010F8, "jne 0x301128"), (0x3010FA, "call 0x30d9a0"),
                 (0x3010FF, "cmp eax, 1"), (0x301102, "jne 0x301128"),
                 (0x30110B, "movzx ecx, byte ptr [rax + 0x5ad5]"), (0x301112, "call 0x31b770"),
                 (0x301117, "cmp rbx, rax"), (0x30111A, "jne 0x301128"), (0x30111C, "xor ecx, ecx"),
                 (0x30111E, "call 0x3138d0"), (0x301123, "call 0x23b040"), (0x301132, "ret")]:
        expect(R, F, a, s)
    R.check("B 00301104 loads [02EBF190]", 0x301104 in F.ins and rip_target(F[0x301104]) == BATTLE)
    R.check("B straight line: the instruction after 0030111E is 00301123",
            F.succ(0x30111E) == [0x301123] and F.succ(0x301123) == [0x301128])


# ---------------------------------------------------------------- C
def grp_seam(img, R):
    S = Body(img, 0x3138D0, 0x313993)
    R.check("C 003138D0-00313993 decodes exactly (195 B)", S.exact)
    sc = [a for a, t in S.calls() if t == 0x311CF0]
    R.check("C 003138D0's one call to 00311CF0 is at 0031395D", sc == [0x31395D], str(["%X" % a for a in sc]))
    expect(R, S, 0x31394A, "mov r9d, ebp")
    expect(R, S, 0x3138FE, "mov ebp, 0x113")
    W = Body(img, 0x311CF0, 0x311E0B)
    R.check("C 00311CF0-00311E0B decodes exactly (283 B)", W.exact)
    expect(R, W, 0x311D45, "cmp word ptr [rbx + 0x714], ax")
    expect(R, W, 0x311D4C, "je 0x311df1")
    expect(R, W, 0x311D5E, "and word ptr [rax + 0x5ad0], cx")
    expect(R, W, 0x311DF1, "mov eax, 0xfffffffe")
    expect(R, W, 0x311D7A, "mov word ptr [rbx + 0xba0], si")
    expect(R, W, 0x311D72, "test ecx, 0x8800203b")
    expect(R, W, 0x311D78, "jne 0x311ded")
    expect(R, W, 0x311DED, "xor eax, eax")
    expect(R, W, 0x311D1B, "je 0x311df1")
    expect(R, W, 0x311D35, "je 0x311df1")
    cw = [a for a in nonstack_writes(W) if any(m["disp"] in (0x708, 0x710, 0x714) for m in W[a].mems)]
    R.check("C 00311CF0 writes none of +0x708/+0x710/+0x714", not cw, str(["%X" % a for a in cw]))
    T = Body(img, 0x317E60, 0x317EB7)
    R.check("C 00317E60-00317EB7 decodes exactly (87 B)", T.exact)
    expect(R, W, 0x311DE8, "call 0x317e60")
    R.check("C 00317E69 tests bit 4 of byte 02089340",
            rip_target(T[0x317E69]) == 0x2089340 and T[0x317E69].text.endswith(", 0x10"))
    expect(R, T, 0x317E8B, "test byte ptr [rax], 8")
    expect(R, T, 0x317E90, "movabs rcx, 0x100000000")
    I = T.ins.get(0x317E9A)
    R.check("C 00317E9A is 00317E60's own qword RMW write on the unit",
            I is not None and I.mnemonic == "or" and I.mems and I.mems[0]["write"] and I.mems[0]["size"] == 8)
    R.check("C 00317E60's only non-stack write is 00317E9A", nonstack_writes(T) == [0x317E9A],
            str(["%X" % a for a in nonstack_writes(T)]))
    expect(R, T, 0x317E9D, "lea rcx, [rax + 0x80]")
    expect(R, T, 0x317EA4, "call 0x33c9b0")
    expect(R, T, 0x317EA9, "xor edx, edx")
    expect(R, T, 0x317EAB, "lea ecx, [rdx + 1]")
    expect(R, T, 0x317EB2, "jmp 0x25aad0")
    P = Body(img, 0x25AAD0, 0x25AB22)
    R.check("C 0025AAD0-0025AB22 decodes exactly (82 B)", P.exact)
    expect(R, P, 0x25AAD6, "mov ebx, ecx")
    expect(R, P, 0x25AADA, "call 0x3588b0")
    expect(R, P, 0x25AADF, "test ebx, ebx")
    expect(R, P, 0x25AAE1, "jne 0x25ab1c")
    pw = nonstack_writes(P)
    R.check("C 0025AAD0's non-stack writes are the five publication stores",
            pw == [0x25AAF2, 0x25AAF8, 0x25AB00, 0x25AB06, 0x25AB15], str(["%X" % a for a in pw]))
    skipped = P.reach(0x25AB1C)
    R.check("C with EBX = 1 the taken jne at 0025AAE1 skips all five stores and the 002F1710 call (0025AB10)",
            P[0x25AB10].text == "call 0x2f1710" and P[0x25AAE1].direct_target() == 0x25AB1C
            and not (set(pw) | {0x25AB10}) & skipped)
    # nothing on the invocation chain calls the Dismiss arm's routine or writes the mode word
    bodies = [Body(img, 0x300FC0, 0x301133), S, W, T, P]
    direct = [(b.start, a) for b in bodies for a in b.order
              if b[a].direct_target() == 0x306760 and (b[a].mnemonic == "call" or b[a].mnemonic.startswith("j"))]
    R.check("C no direct transfer to 00306760 in 00300FC0/003138D0/00311CF0/00317E60/0025AAD0", not direct)
    mw = [(b.start, a) for b in bodies for a in nonstack_writes(b) if any(m["disp"] == 0x5B04 for m in b[a].mems)]
    R.check("C no +0x5B04 write in those five bodies", not mw)


# ---------------------------------------------------------------- D
def grp_selector(img, R):
    S = Body(img, 0x3138D0, 0x313993)
    expect(R, S, 0x3138DD, "cmp eax, 1")
    expect(R, S, 0x3138E6, "lea ecx, [rax + 2]")
    expect(R, S, 0x3138E9, "call 0x31b8c0")
    a = Body(img, 0x31B8C0, 0x31B8DF)
    b = Body(img, 0x263750, 0x263767)
    c = Body(img, 0x263E30, 0x263E35)
    R.check("D 0031B8C0 (31 B), 00263750 (23 B), 00263E30 (5 B) decode exactly", a.exact and b.exact and c.exact)
    R.check("D 0031B8C0 has a .pdata root; 00263750 and 00263E30 have none",
            img.pdata(0x31B8C0) == (0x31B8C0, 0x31B8DF) and img.pdata(0x263750) is None
            and img.pdata(0x263E30) is None)
    R.check("D 0031B8C0 calls only 00263750 and tail-jumps to 00263E30",
            a.calls() == [(0x31B8C4, 0x263750)] and a.exits()[1] == [(0x31B8DA, 0x263E30)])
    expect(R, a, 0x31B8CC, "jne 0x31b8d3")
    expect(R, a, 0x31B8D2, "ret")
    expect(R, b, 0x263750, "cmp ecx, 3")
    expect(R, b, 0x263753, "ja 0x263764")
    R.check("D 00263758 forms the roster base 0209A1F0; index 3 -> qword 0209A208",
            rip_target(b[0x263758]) == 0x209A1F0 and b[0x26375F].text == "mov rax, qword ptr [rcx + rax*8]"
            and 0x209A1F0 + 8 * 3 == 0x209A208)
    expect(R, c, 0x263E30, "mov rax, qword ptr [rcx + 0x30]")
    allw = [x for B in (a, b, c) for x in B.order for m in B[x].mems if m["write"]]
    R.check("D no memory write of any kind in the three bodies", not allw, str(["%X" % x for x in allw]))
    st = [x for B in (a, b, c) for x in B.order for m in B[x].mems if m["disp"] in (0x3C, 0x48, 0x64, 0x698)]
    R.check("D no read of a status/HP/stats field (+0x3C/+0x48/+0x64/+0x698)", not st)
    R.check("D no call in 00263750 or 00263E30", not b.calls() and not c.calls())


# ---------------------------------------------------------------- E
def grp_mode(img, R):
    M = Body(img, 0x30D9A0, 0x30DA09)
    R.check("E 0030D9A0-0030DA09 decodes exactly (105 B)", M.exact)
    loads = [x for x in M.order if rip_target(M[x]) == BATTLE]
    words = [x for x in M.order for m in M[x].mems if m["disp"] == 0x5B04 and m["read"] and not m["write"]]
    R.check("E [02EBF190] loaded twice (0030D9A4, 0030D9E2)", loads == [0x30D9A4, 0x30D9E2],
            str(["%X" % x for x in loads]))
    R.check("E the mode word +0x5B04 read twice (0030D9AB, 0030D9E9)", words == [0x30D9AB, 0x30D9E9],
            str(["%X" % x for x in words]))
    expect(R, M, 0x30D9B1, "test cl, 8")
    expect(R, M, 0x30D9C0, "test cl, 4")
    expect(R, M, 0x30D9CF, "call 0x377c20")
    expect(R, M, 0x30D9EF, "test cl, 2")
    expect(R, M, 0x30DA01, "and eax, 1")
    R.check("E order: bits 3/2 read, then 00377C20, then the second read",
            0x30D9AB < 0x30D9B1 < 0x30D9C0 < 0x30D9CF < 0x30D9E9 < 0x30D9EF)
    ch = [Body(img, 0x377C20, 0x377C6E), Body(img, 0x3148F0, 0x31490B), Body(img, 0x2EF2B0, 0x2EF2C4),
          Body(img, 0x2EF640, 0x2EF648)]
    R.check("E the chain decodes exactly: 78 + 27 + 20 + 8 = 133 B, 23 + 8 + 5 + 2 = 38 instructions",
            all(B.exact for B in ch) and sum(B.end - B.start for B in ch) == 133
            and [len(B.order) for B in ch] == [23, 8, 5, 2])
    w = [x for B in ch for x in B.order for m in B[x].mems if m["write"]]
    R.check("E no memory write of any kind in the chain", not w, str(["%X" % x for x in w]))
    cl = [B.calls() for B in ch]
    R.check("E calls are exactly the chain 00377C20->003148F0->002EF2B0->002EF640",
            cl == [[(0x377C24, 0x3148F0)], [(0x3148F4, 0x2EF2B0)], [(0x2EF2B4, 0x2EF640)], []]
            and all(not B.exits()[1] for B in ch))
    R.check("E 002EF640 forms 02164280 with lea (a fixed image address, no load)",
            ch[3][0x2EF640].mnemonic == "lea" and rip_target(ch[3][0x2EF640]) == 0x2164280)
    expect(R, ch[2], 0x2EF2B9, "add rax, 0x200")
    expect(R, ch[1], 0x3148FB, "mov eax, dword ptr [rax + 0x1044]")
    expect(R, ch[1], 0x314903, "cmovs eax, ecx")
    R.check("E field cell 02164280 + 0x200 + 0x1044 = 021654C4", 0x2164280 + 0x200 + 0x1044 == 0x21654C4)
    Q = ch[0]
    R.check("E 00377C29 loads the descriptor qword 02ADD100", rip_target(Q[0x377C29]) == 0x2ADD100)
    expect(R, Q, 0x377C33, "je 0x377c5f")
    expect(R, Q, 0x377C35, "cmp eax, dword ptr [r8 + 4]")
    expect(R, Q, 0x377C39, "jae 0x377c5f")
    expect(R, Q, 0x377C42, "movzx edx, byte ptr [rcx + rax + 9]")
    expect(R, Q, 0x377C4B, "movzx ecx, byte ptr [rcx + rax + 8]")
    expect(R, Q, 0x377C55, "shr edx, 0xf")
    expect(R, Q, 0x377C5F, "mov edx, 0xfff")
    R.check("E pdata: three roots, 002EF640 a leaf without a row",
            img.pdata(0x377C20) == (0x377C20, 0x377C6E) and img.pdata(0x3148F0) == (0x3148F0, 0x31490B)
            and img.pdata(0x2EF2B0) == (0x2EF2B0, 0x2EF2C4) and img.pdata(0x2EF640) is None)


# ---------------------------------------------------------------- F
def grp_early(img, R):
    S = Body(img, 0x3138D0, 0x313993)
    expect(R, S, 0x3138E0, "jne 0x31398d")
    expect(R, S, 0x3138F1, "je 0x31398d")
    expect(R, S, 0x313903, "bt rdx, 0xe")
    expect(R, S, 0x31390A, "movzx ecx, word ptr [rax + 0xba0]")
    expect(R, S, 0x313913, "je 0x313988")
    expect(R, S, 0x313915, "cmp word ptr [rax + 0x714], bp")
    expect(R, S, 0x31391C, "je 0x313988")
    I = S.ins.get(0x313981)
    R.check("F 00313981 writes word +0x5AD0 (bit 0 := argument)",
            I is not None and I.text == "xor word ptr [rcx + 0x5ad0], ax" and S[0x31397A].text == "xor ax, si"
            and S[0x31397D].text == "and ax, 1")
    for tgt in (0x313988, 0x31398D):
        r = S.reach(tgt)
        R.check("F exit %X reaches neither 0031395D nor 00313981" % tgt, 0x31395D not in r and 0x313981 not in r)
    early = S.reach(0x3138D0, avoid=[0x31391E])
    R.check("F the early-exit paths do not contain 0031395D or 00313981",
            0x31395D not in early and 0x313981 not in early)
    ew = nonstack_writes(S, early)
    sw = [a for a in early for m in S[a].mems if m["write"] and m["base"] == "rsp"]
    R.check("F the early-exit paths' only memory store is the [rsp+0x48] home slot", not ew and sw == [0x3138F9],
            "nonstack %s stack %s" % (["%X" % a for a in ew], ["%X" % a for a in sw]))
    expect(R, S, 0x31392D, "call 0x31b7e0")
    expect(R, S, 0x31393C, "call 0x31b7e0")
    expect(R, S, 0x313941, "test ebx, ebx")
    expect(R, S, 0x313943, "je 0x31394a")
    expect(R, S, 0x313938, "je 0x313962")
    expect(R, S, 0x313948, "je 0x313962")
    r = S.reach(0x313962)
    R.check("F the 0031B7E0-NULL exits skip 0031395D but still reach 00313981",
            0x31395D not in r and 0x313981 in r)


GROUPS = [grp_dismiss, grp_defeat, grp_seam, grp_selector, grp_mode, grp_early]


def rel32(at, size, target):
    return struct.pack("<i", target - (at + size))


def main():
    img = Img.load()
    R = Report("fable-uq147")
    print("NOTE  image sha256 pinned by rvlib (73461d08...21f8), base %X" % img.base)
    R.check("image base is 0x120000", img.base == BASE)
    for g in GROUPS:
        g(img, R)
    check_manifest(R, "uq147-dismiss-stage", "8138136d62841224f88f0c756b0959fc2448d00c134cad78078b420dd78ab478")
    check_manifest(R, "uq147-local-boundaries", "d6df38e07fca5621a9222d68f1dcb24faad7d41a7f2cf5e0b1097e84a9ca0c8f")
    check_manifest(R, "uq147-mode-query", "f6d762b35072e327ba67f46b48a87a88cf83dbca60faf90981d400d40dd7bf0e")

    inj = b"\xC7\x05" + rel32(0x306A5B, 10, STATE) + struct.pack("<I", 5) + b"\x90\x90\x90"
    controls = [
        ("c1 selector byte map[127] 5 -> 4 (quotient 275 no longer kind 2)", grp_dismiss,
         lambda: img.patched(0x306D08 + 127, b"\x04")),
        ("c2 00306A81 displacement +0x5B04 -> +0x5AD0 (the clear is not the mode word)", grp_dismiss,
         lambda: img.patched(0x306A81, b"\x89\x81\xd0\x5a\x00\x00")),
        ("c3 a direct 022C2160 write injected at 00306A5B, before 00306A81", grp_dismiss,
         lambda: img.patched(0x306A5B, inj)),
        ("c4 00306ADF target 022C2160 -> 022C215C (the 5 is not the state word)", grp_dismiss,
         lambda: img.patched(0x306ADF + 2, rel32(0x306ADF, 10, KIND))),
        ("c5 00301123 call 0023B040 -> nops (no same-call recompute)", grp_defeat,
         lambda: img.patched(0x301123, b"\x90" * 5)),
        ("c6 00317E9A or qword [rax],rcx -> nops (no own write)", grp_seam,
         lambda: img.patched(0x317E9A, b"\x90" * 3)),
        ("c7 0025AAE1 jne -> nops (the tail no longer skips the publication)", grp_seam,
         lambda: img.patched(0x25AAE1, b"\x90\x90")),
        ("c8 00263E30 load -> store [rcx+0x30],rax (selector writes)", grp_selector,
         lambda: img.patched(0x263E30, b"\x48\x89\x41\x30")),
        ("c9 0030D9E9 second mode read -> mov ecx,ecx (one read only)", grp_mode,
         lambda: img.patched(0x30D9E9, b"\x8b\xc9\x90\x90\x90\x90")),
        ("c10 003148FB field read -> store [rax+0x1044],eax (chain writes)", grp_mode,
         lambda: img.patched(0x3148FB, b"\x89\x80\x44\x10\x00\x00")),
        ("c11 0031391C je 00313988 -> je 00313962 (committed-0x113 exit runs the +0x5AD0 write)", grp_early,
         lambda: img.patched(0x31391C, b"\x74\x44")),
    ]
    for label, grp, fac in controls:
        # a control is only sensitive if its group PASSES on the unpatched image first
        base_ok = run_control(label + " (baseline)", lambda: img, grp, must_fail=False)
        R.check("CONTROL %s: group %s passes unpatched, FAILS on the patched copy" % (label, grp.__name__),
                base_ok and run_control(label, fac, grp))
    R.check("image on disk unchanged after the controls (sha256 re-read)", Img.load() is not None)
    print("FAILS %d" % R.fails)
    return 1 if R.fails else 0


if __name__ == "__main__":
    sys.exit(main())
