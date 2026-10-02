"""rv_actordir.py - FABLE independent re-derivation for ASTRA packet actor-directory-kind-proof (317ebd1b8, OV-16).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the filecache-route2-commit-key review, sha256
69f9bc40be32abcc...).  Does not import or run ASTRA's prove.py, capture drivers, archive-member.py, control.py,
freeze/publication scripts or the shared role adapter (reg_tracking.py).

Method:
  * image sha256; complete linear decode of the allocator 002679F0, the initializer 00266530, the pre-preset leaf
    00266AD0, the preset leaf 00266BD0 and the filer 00268EA0.  Three are bounded by .pdata; the two leaves have no
    record and are bounded by their closed CFG (direct edges plus their own jump tables), their rets, int3/nop padding
    and the jump table that follows each body;
  * register-write censuses for every carrier of the ordinal, row, count offset, table pointer and record pointer;
    the descriptor-binding arithmetic; a census of every write through the record that meets +0x1C..+0x1F;
  * the map data is re-derived from the extracted game file D:/FFXII_TZA_extract (US copy), not from the packet's
    retained bytes; the packet's retained compressed blocks are separately re-read from the archive at their indexed
    offsets and strictly decoded;
  * a concrete emulation (unicorn) of the ORIGINAL allocator body over that data, with its allocation callback and
    memset served by the harness, and the ORIGINAL initializer for ordinal 25 with its two leaves and the address
    resolver 0020E600 run as shipped and every other callee (and the 003DB280 tail) replaced by a bare return.  The
    emulation therefore says nothing about those callees' effects; it is a second, independent reading of the loops;
  * controls: privately patched in-memory images and mutated in-memory copies of the map bytes.  Nothing on disk is
    written; the exe sha256 is rechecked at the end.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, SHA256 as SHA_PIN  # noqa: E402

ALLOC = (0x002679F0, 0x00267BA4)   # 436 B
INIT = (0x00266530, 0x00266ACF)    # 1439 B, exits by tail jmp 003DB280
PRE = (0x00266AD0, 0x00266BA3)     # 211 B leaf, jump table at 00266BA4
PRESET = (0x00266BD0, 0x00266C30)  # 96 B leaf, jump table at 00266C30
FILER = (0x00268EA0, 0x00269057)   # 439 B
RESOLVE = (0x0020E600, 0x0020E60A)
TAIL = 0x003DB280
KINDTAB = 0x01E0C328
PRE_TAB = 0x00266BA4
PRESET_TAB = 0x00266C30
SLUG = "actor-directory-kind-proof"
PRODUCER = "317ebd1b8"
US_EBP = "D:/FFXII_TZA_extract/ps2data/plan_master/us/plan_map/asp_a/asp_a03/global/asp_a03.ebp"
VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
TARGET = 25
STUBS = (0x003DB580, 0x00265FF0, 0x00265B60, 0x00268380, 0x002681E0, 0x003DBB60, 0x00268EA0)


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


def table(img, va, n):
    return [img.base + struct.unpack("<I", img.read(va + 4 * i, 4))[0] for i in range(n)]


def jt_reach(B, frm, jt):
    """Reach over direct edges plus jump-table edges {jmp_addr: [targets]}."""
    seen, st = set(), [frm]
    while st:
        a = st.pop()
        if a in seen or a not in B.ins:
            continue
        seen.add(a)
        if a in jt:
            st.extend(jt[a])
        else:
            st.extend(B.succ(a))
    return seen


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


# ------------------------------------------------------------------ data side (own parse of the map bytes)
def parse(d):
    S = struct.unpack_from("<I", d, 0x10)[0]          # container directory slot 0 = section_000
    sec = d[S:]
    ver = struct.unpack_from("<H", sec, 0)[0]
    t14 = struct.unpack_from("<i", sec, 0x14)[0]
    rows = struct.unpack_from("<H", sec, t14)[0]
    counts = list(struct.unpack_from("<%dH" % rows, sec, t14 + 2))
    t18 = struct.unpack_from("<i", sec, 0x18)[0]
    dircount = struct.unpack_from("<I", sec, t18)[0]
    stride = 48 if ver >= 8 else 32
    eoff = t18 + 4 + stride * TARGET
    ent = sec[eoff:eoff + 48]
    pool = struct.unpack_from("<I", sec, 0x4C)[0]
    nameoff = struct.unpack_from("<I", ent, 0)[0]
    raw = sec[pool + nameoff:].split(b"\0")[0]
    labels = [struct.unpack_from("<H", sec, t18 + 4 + stride * i + 4)[0] for i in range(dircount)]
    return dict(S=S, sec=sec, ver=ver, t14=t14, rows=rows, counts=counts, t18=t18, dircount=dircount, stride=stride,
                eoff=eoff, label=struct.unpack_from("<H", ent, 4)[0], pcid=struct.unpack_from("<H", ent, 6)[0],
                raw=raw, labels=labels)


def model_row(counts, i):
    """Row k with sum(counts[:k]) <= i < sum(counts[:k+1]); None if i is past the last row."""
    acc = 0
    for k, c in enumerate(counts):
        if acc <= i < acc + c:
            return k
        acc += c
    return None


def kindtab(img):
    raw = img.read(KINDTAB, 32)
    return [(raw[4 * k], raw[4 * k + 1], struct.unpack_from("<H", raw, 4 * k + 2)[0]) for k in range(8)]


# ------------------------------------------------------------------ concrete emulation of the original code
def emulate(img, d):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
    from unicorn import x86_const as X
    P = parse(d)
    pe = struct.unpack_from("<I", img.d, 0x3C)[0]
    soi = struct.unpack_from("<I", img.d, pe + 24 + 56)[0]
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(img.base, (soi + 0xFFF) & ~0xFFF)
    for name, va, vs, ra, rs in img.secs:
        n = min(rs, (vs + 0xFFF) & ~0xFFF)
        mu.mem_write(img.base + va, img.d[ra:ra + n])
    DESC, POOL, MGR, STK, RET = 0x40000000, 0x41000000, 0x42000000, 0x43000000, 0x44000000
    for a, n in ((DESC, 0x100000), (POOL, 0x100000), (MGR, 0x1000), (STK, 0x100000), (RET, 0x1000)):
        mu.mem_map(a, n)
    mu.mem_write(DESC, P["sec"])
    N = sum(P["counts"])                         # premise: the binder's +0x20 total covers the rows
    mu.mem_write(MGR, struct.pack("<Q", DESC))
    mu.mem_write(MGR + 0x20, struct.pack("<I", N))
    mu.mem_write(0x01F83530, struct.pack("<Q", 0))  # 0020E600's relative-reference base: 0 in the harness
    rsp = STK + 0x80000
    mu.mem_write(rsp, struct.pack("<Q", RET))
    mu.reg_write(X.UC_X86_REG_RSP, rsp)
    mu.reg_write(X.UC_X86_REG_RCX, MGR)
    st = {"stubs": [], "init_args": None, "after_preset": None, "tail": None, "req": None, "bad": None}
    allowed = [ALLOC, INIT, PRE, PRESET, RESOLVE]

    def u32(a):
        return struct.unpack("<I", bytes(mu.mem_read(a, 4)))[0]

    def ret_stub():
        sp = mu.reg_read(X.UC_X86_REG_RSP)
        ra = struct.unpack("<Q", bytes(mu.mem_read(sp, 8)))[0]
        mu.reg_write(X.UC_X86_REG_RSP, sp + 8)
        mu.reg_write(X.UC_X86_REG_RAX, 0)
        mu.reg_write(X.UC_X86_REG_RIP, ra)

    def hook(uc, addr, size, ud):
        if addr == 0x267A79:                                  # call [r15+0x88]: allocation callback
            st["req"] = mu.reg_read(X.UC_X86_REG_RCX) & 0xFFFFFFFF
            mu.reg_write(X.UC_X86_REG_RAX, POOL)
            mu.reg_write(X.UC_X86_REG_RIP, 0x267A80)
        elif addr == 0x267A8B:                                # call 00861EC0 memset(rcx, edx, r8)
            c, v, n = (mu.reg_read(X.UC_X86_REG_RCX), mu.reg_read(X.UC_X86_REG_RDX) & 0xFF,
                       mu.reg_read(X.UC_X86_REG_R8))
            if n > 0x100000:
                st["bad"] = "memset %X" % n
                uc.emu_stop()
                return
            mu.mem_write(c, bytes([v]) * n)
            mu.reg_write(X.UC_X86_REG_RIP, 0x267A90)
        elif addr == 0x267B79:                                # call 00266530(mgr, pool, ordinal)
            o = mu.reg_read(X.UC_X86_REG_R8) & 0xFFFFFFFF
            if o != TARGET:
                mu.reg_write(X.UC_X86_REG_RIP, 0x267B7E)
            else:
                st["init_args"] = (mu.reg_read(X.UC_X86_REG_RCX), mu.reg_read(X.UC_X86_REG_RDX), o)
        elif addr == 0x2665B6:                                # right after the 00266BD0 call returns
            rbx = mu.reg_read(X.UC_X86_REG_RBX)
            st["after_preset"] = (rbx, u32(rbx + 0x1C), bytes(mu.mem_read(rbx + 3, 1))[0])
        elif addr in STUBS:
            st["stubs"].append(addr)
            ret_stub()
        elif addr == TAIL:
            rcx = mu.reg_read(X.UC_X86_REG_RCX)
            st["tail"] = (rcx, bytes(mu.mem_read(rcx, 0x120)))
            ret_stub()
        elif addr == RET:
            pass
        elif not any(s <= addr < e for s, e in allowed):
            st["bad"] = "left the modelled code at %X" % addr
            uc.emu_stop()

    mu.hook_add(UC_HOOK_CODE, hook)
    mu.emu_start(ALLOC[0], RET, count=400000)
    st["N"] = N
    st["pool0"] = u32(POOL)
    st["ptrs"] = [struct.unpack("<Q", bytes(mu.mem_read(POOL + 8 + 8 * i, 8)))[0] for i in range(N)]
    st["plus3"] = [bytes(mu.mem_read(p, 4))[3] if p else None for p in st["ptrs"]]
    st["DESC"], st["POOL"], st["MGR"] = DESC, POOL, MGR
    return st


# ------------------------------------------------------------------ checks
def checks(img, R, d):
    A, I, PR, PS, F = (Body(img, *r) for r in (ALLOC, INIT, PRE, PRESET, FILER))
    D = parse(d)

    # ---- bodies
    for B, (s, e) in ((A, ALLOC), (I, INIT), (F, FILER)):
        ents, ok = img.pdata_cover(s, e)
        R.check("body %08X + 0x%X (%d B) decodes exactly and one .pdata record covers it exactly" % (s, e - s, e - s),
                B.exact and ok and len(ents) == 1)
    rets, tails, outs = I.exits()
    R.check("00266530 has no ret; its single exit is the last instruction, 00266530 + 0x59A `jmp 0x3db280`, then int3",
            rets == [] and tails == [(0x266ACA, TAIL)] and not outs and I.order[-1] == 0x266ACA and
            img.read(INIT[1], 1) == b"\xcc")
    pt = table(img, PRE_TAB, 8)
    R.check("00266AD0 dispatch: `cmp eax, 7` / `ja` to its ret, table 00266BA4 = image base + [r9 + rax*4 + 0x146ba4]",
            T(PR, 0x266ADC) == "cmp eax, 7" and T(PR, 0x266ADF) == "ja 0x266ba2" and
            T(PR, 0x266AE7) == "lea r9, [rip - 0x146aee]" and 0x266AEE - 0x146AEE == img.base and
            T(PR, 0x266AEE) == "mov eax, dword ptr [r9 + rax*4 + 0x146ba4]" and T(PR, 0x266AF9) == "jmp rax")
    reach = jt_reach(PR, PRE[0], {0x266AF9: pt})
    R.check("00266AD0 + 0xD3 (211 B): exact decode, no .pdata, all 8 table targets are boundaries, every instruction "
            "reached, one ret (00266AD0 + 0xD2) then one nop pad, then the table; int3 before entry",
            PR.exact and img.pdata(PRE[0]) is None and all(t in PR.ins for t in pt) and reach == set(PR.order) and
            [a for a in PR.order if PR[a].mnemonic == "ret"] == [0x266BA2] and PR.order[-1] == 0x266BA2 and
            img.read(0x266BA3, 1) == b"\x90" and PRE[1] + 1 == PRE_TAB and img.read(PRE[0] - 1, 1) == b"\xcc",
            "targets %s" % ",".join("%X" % t for t in pt))
    qt = table(img, PRESET_TAB, 8)
    reach = jt_reach(PS, PRESET[0], {0x266BF4: qt})
    prets = [a for a in PS.order if PS[a].mnemonic == "ret"]
    R.check("00266BD0 + 0x60 (96 B): exact decode, no .pdata, dispatch on `+3 & 0x1F` <= 7 through table 00266C30, "
            "every instruction reached, last instruction a ret abutting the table; 12 int3 before entry",
            PS.exact and img.pdata(PRESET[0]) is None and T(PS, 0x266BD0) == "movzx r8d, byte ptr [rcx + 3]" and
            T(PS, 0x266BD8) == "and eax, 0x1f" and T(PS, 0x266BDB) == "cmp eax, 7" and
            T(PS, 0x266BE9) == "mov edx, dword ptr [r9 + rax*4 + 0x146c30]" and T(PS, 0x266BF4) == "jmp rdx" and
            all(t in PS.ins for t in qt) and reach == set(PS.order) and PS.order[-1] == prets[-1] == 0x266C2F and
            img.read(PRESET[0] - 12, 12) == b"\xcc" * 12, "%d rets" % len(prets))

    # ---- allocator: carriers and the row/ordinal induction
    R.check("allocator: r12 = [rcx] (descriptor, 002679F0 + 0x1C), r15 = rcx (+0x25), N = [rcx+0x20] spilled to "
            "[rsp+0x50] (+0x21/+0x28); r12, r15 have no other writer but the epilogue pops",
            T(A, 0x267A0C) == "mov r12, qword ptr [rcx]" and T(A, 0x267A15) == "mov r15, rcx" and
            T(A, 0x267A11) == "mov r11d, dword ptr [rcx + 0x20]" and
            T(A, 0x267A18) == "mov dword ptr [rsp + 0x50], r11d" and
            writers(A, "r12") == [0x267A0C, 0x267BA0] and writers(A, "r15") == [0x267A15, 0x267B9A])
    R.check("count prefix: signed DWORD header +0x14 (002679F0 + 0x30), then the WORD row count (+0x35) in r13d; "
            "r13 has no other writer but the pop",
            T(A, 0x267A20) == "movsxd rax, dword ptr [r12 + 0x14]" and
            T(A, 0x267A25) == "movzx r13d, word ptr [rax + r12]" and writers(A, "r13") == [0x267A25, 0x267B9E])
    R.check("loop entry state: ebp = 0 (+0x1F); ebx = ebp (+0xA4), r10d = ebp (+0xA9), rdi = rbp (+0xC8), r8 = "
            "native table 01E0C328 (+0xCB); rbp written only at +0x1F, the call-loop inc (+0x18E) and the restore",
            T(A, 0x267A0F) == "xor ebp, ebp" and T(A, 0x267A94) == "mov ebx, ebp" and
            T(A, 0x267A99) == "mov r10d, ebp" and T(A, 0x267AB8) == "mov rdi, rbp" and
            T(A, 0x267ABB) == "lea r8, [rip + 0x1ba4866]" and 0x267AC2 + 0x1BA4866 == KINDTAB and
            writers(A, "rbp") == [0x267A0F, 0x267B7E, 0x267B8C])
    R.check("row k's count is WORD [descriptor + DWORD(+0x14) + 2 + rdi] (002679F0 + 0xD2..+0xDA); a zero count "
            "skips the inner loop (+0xED test / +0xEF jle to the row advance +0x13A)",
            T(A, 0x267AC2) == "movsxd rax, dword ptr [r12 + 0x14]" and T(A, 0x267AC7) == "add rax, rdi" and
            T(A, 0x267ACA) == "movzx ecx, word ptr [rax + r12 + 2]" and T(A, 0x267ADD) == "test ecx, ecx" and
            T(A, 0x267ADF) == "jle 0x267b2a")
    loop = [a for a in A.order if 0x267AC2 <= a < 0x267B3A]
    W = lambda f: [a for a in loop if f in A[a].reg_writes]
    R.check("inner loop runs exactly count times: r11d = count (+0xF5), `sub r11, 1` / `jne` (+0x134/+0x138); "
            "r11 has no other writer in the row loop",
            T(A, 0x267AE5) == "mov r11d, ecx" and T(A, 0x267B24) == "sub r11, 1" and T(A, 0x267B28) == "jne 0x267af0"
            and W("r11") == [0x267AE5, 0x267B24], str(["%X" % x for x in W("r11")]))
    R.check("publish: pool[1 + old ebx] = record pointer (`movsxd rax, ebx` +0x100, `inc ebx` +0x103, "
            "`mov qword ptr [r14 + rax*8 + 8], rdx` +0x105); ebx's only writer in the row loop is that inc",
            T(A, 0x267AF0) == "movsxd rax, ebx" and T(A, 0x267AF3) == "inc ebx" and
            T(A, 0x267AF5) == "mov qword ptr [r14 + rax*8 + 8], rdx" and W("rbx") == [0x267AF3] and
            writers(A, "r14") == [0x267A88, 0x267B9C] and T(A, 0x267A88) == "mov r14, rax")
    R.check("stamp: +3 low five bits = row (r9b = r10b & 0x1F, +0xF1/+0xF8; +0x10A..+0x114), upper three = the native "
            "table byte << 5 (+0x117..+0x123)",
            [T(A, a) for a in (0x267AE1, 0x267AE8, 0x267AFA, 0x267AFE, 0x267B01, 0x267B04, 0x267B07, 0x267B0A,
                               0x267B0E, 0x267B11, 0x267B13)] ==
            ["movzx r9d, r10b", "and r9b, 0x1f", "movzx ecx, byte ptr [rdx + 3]", "and cl, 0xe0", "or cl, r9b",
             "mov byte ptr [rdx + 3], cl", "and cl, 0x1f", "movzx eax, byte ptr [r8]", "shl al, 5", "or cl, al",
             "mov byte ptr [rdx + 3], cl"] and W("r9") == [0x267AE1, 0x267AE8])
    R.check("advance: rdx += (WORD [r8+2] + 15) & ~15 (+0x126..+0x131), rdx's only writer in the row loop",
            T(A, 0x267B16) == "movzx eax, word ptr [r8 + 2]" and T(A, 0x267B1B) == "add eax, 0xf" and
            T(A, 0x267B1E) == "and eax, 0xfffffff0" and T(A, 0x267B21) == "add rdx, rax" and W("rdx") == [0x267B21])
    R.check("outer step: inc r10d (+0x13A), rdi += 2 (+0x13D), r8 += 4 (+0x141), `cmp r10d, r13d` / `jl` (+0x145); "
            "each is its register's only writer in the row loop",
            T(A, 0x267B2A) == "inc r10d" and T(A, 0x267B2D) == "add rdi, 2" and T(A, 0x267B31) == "add r8, 4" and
            T(A, 0x267B35) == "cmp r10d, r13d" and T(A, 0x267B38) == "jl 0x267ac2" and W("r10") == [0x267B2A] and
            W("rdi") == [0x267B2D] and W("r8") == [0x267B31])
    P = preds(A)
    R.check("the two loop heads have no entries but their fall-in and their back-edge",
            P.get(0x267AF0) == {0x267AEC, 0x267B28} and P.get(0x267AC2) == {0x267ABB, 0x267B38},
            "%s %s" % (sorted("%X" % x for x in P.get(0x267AF0, ())), sorted("%X" % x for x in P.get(0x267AC2, ()))))
    R.check("records start after pool and second array: rdx = r14 + 2*esi, esi = (8N + 0x17) & ~0xF; pool[0] = N",
            T(A, 0x267A65) == "lea esi, [r11*8 + 0x17]" and T(A, 0x267A6D) == "and esi, 0xfffffff0" and
            T(A, 0x267A70) == "lea edi, [rsi + rsi]" and T(A, 0x267A9F) == "movsxd rdx, edi" and
            T(A, 0x267AA2) == "add rdx, r14" and T(A, 0x267AA5) == "mov dword ptr [r14], eax" and
            T(A, 0x267A90) == "mov eax, dword ptr [rsp + 0x50]")
    R.check("then 00266530(rcx = manager, rdx = pool, r8d = ordinal) for ordinal 0 .. N-1 (002679F0 + 0x173..+0x192)",
            [T(A, a) for a in (0x267B63, 0x267B70, 0x267B73, 0x267B76, 0x267B7E, 0x267B80, 0x267B82)] ==
            ["mov ebx, dword ptr [rsp + 0x50]", "mov r8d, ebp", "mov rdx, r14", "mov rcx, r15", "inc ebp",
             "cmp ebp, ebx", "jl 0x267b70"] and A[0x267B79].direct_target() == INIT[0])
    ar = [(x, m["disp"]) for x in A.order for m in A[x].mems if m["base"] == "r12" or m["index"] == "r12"]
    R.check("the allocator touches the descriptor only at +0x14 and the count table (the +0x3F operand is an "
            "address-only lea of the count WORDs); it never reads a directory entry",
            sorted(set(ar)) == [(0x267A20, 0x14), (0x267A25, 0), (0x267A2F, 2), (0x267AC2, 0x14), (0x267ACA, 2)] and
            A[0x267A2F].mnemonic == "lea", str([("%X" % x, dsp) for x, dsp in ar]))

    # ---- native table and the data model
    kt = kindtab(img)
    R.check("native table 01E0C328 row 6 = kind 3, sub 0, 0x6E0 (1760 B); stamp (3 << 5) | 6 = 0x66",
            kt[6] == (3, 0, 0x6E0) and ((kt[6][0] << 5) | 6) == 0x66, str(kt))
    R.check("extract asp_a03 (US): section_000 at file+0x80, version WORD 11 (stride 48), 8 rows, counts "
            "[9,11,0,0,0,4,72,0], sum 96 = directory count",
            D["S"] == 0x80 and D["ver"] == 11 and D["rows"] == 8 and D["counts"] == [9, 11, 0, 0, 0, 4, 72, 0] and
            sum(D["counts"]) == 96 == D["dircount"], "ver %d rows %d counts %s dir %d" %
            (D["ver"], D["rows"], D["counts"], D["dircount"]))
    r25 = model_row(D["counts"], TARGET)
    lo = sum(D["counts"][:6])
    R.check("own model: ordinal 25 is in row 6, whose interval is 24..95", r25 == 6 and lo == 24 and
            lo + D["counts"][6] - 1 == 95, "row %s" % r25)
    R.check("entry 25 is at section offset 0xD2A4 (= DWORD +0x18 0xCDF0 + 4 + 48*25), WORD +4 label 6, pcId 0xFF",
            D["eoff"] == 0xD2A4 and D["t18"] == 0xCDF0 and D["label"] == 6 and D["pcid"] == 0xFF,
            "eoff %X label %d" % (D["eoff"], D["label"]))
    try:
        nm = D["raw"].decode("cp932", errors="strict")
    except UnicodeDecodeError:
        nm = None
    R.check("entry 25's name (pool +0x4C + nameOff) decodes strictly as CP932 to ラバナ_通常_NPC01",
            nm == "ラバナ_通常_NPC01", D["raw"].hex())

    # ---- initializer: selection and binding
    R.check("00266530: rsi = [rcx] (+0x1C), r10 = movsxd r8d (+0x26), rbx = [rdx + r10*8 + 8] (+0x3A), r14 = rcx; "
            "no rdx write before +0x3A; rbx written only there and at the restore",
            T(I, 0x26654C) == "mov rsi, qword ptr [rcx]" and T(I, 0x266556) == "movsxd r10, r8d" and
            T(I, 0x26656A) == "mov rbx, qword ptr [rdx + r10*8 + 8]" and T(I, 0x266561) == "mov r14, rcx" and
            writers(I, "rdx", INIT[0], 0x26656A) == [] and writers(I, "rbx") == [0x26656A, 0x266AAE])
    seg = on_paths(I, 0x266556, 0x26671F)
    segcalls = sorted(I[x].direct_target() for x in seg if I[x].mnemonic == "call")
    R.check("r10 (volatile) has one writer (+0x26); between it and its last use (+0x1EF) the only calls are the two "
            "leaves 00266AD0 and 00266BD0, called with rcx = rbx (+0x76/+0x7E)",
            writers(I, "r10") == [0x266556] and segcalls == [PRE[0], PRESET[0]] and
            T(I, 0x2665A6) == "mov rcx, rbx" and T(I, 0x2665AE) == "mov rcx, rbx" and
            I[0x2665A9].direct_target() == PRE[0] and I[0x2665B1].direct_target() == PRESET[0],
            "calls %s" % ["%X" % c for c in segcalls])
    vol = {"rax", "rcx", "rdx", "r8", "r9"}
    pw = set().union(*(PR[a].reg_writes for a in PR.order)) - {"rflags", "rip", "rsp"}
    qw = set().union(*(PS[a].reg_writes for a in PS.order)) - {"rflags", "rip", "rsp"}
    R.check("the two leaves write only rax/rcx/rdx/r8/r9: r10 (ordinal) and r11 (image base) survive them",
            pw <= vol and qw <= vol, "00266AD0 %s 00266BD0 %s" % (sorted(pw), sorted(qw)))
    R.check("binding: rcx = descriptor + signed DWORD +0x18 (+0x1E0/+0x1E7); WORD +0 >= 8 gives rdi = 48*i "
            "(+0x1EF/+0x1F3), else 32*i (+0x1F9); +4 (+0x1FD), + rcx (+0x201), stored to record +0x40 (+0x204)",
            [T(I, a) for a in (0x266710, 0x266714, 0x266717, 0x26671A, 0x26671D, 0x26671F, 0x266723, 0x266729,
                               0x26672D, 0x266731, 0x266734)] ==
            ["movsxd rcx, dword ptr [rsi + 0x18]", "movzx eax, word ptr [rsi]", "add rcx, rsi", "cmp eax, 8",
             "jb 0x266729", "lea rdi, [r10 + r10*2]", "shl rdi, 4", "shl rdi, 5", "add rdi, 4", "add rdi, rcx",
             "mov qword ptr [rbx + 0x40], rdi"] and T(I, 0x266564) == "mov rdi, r10" and
            writers(I, "rsi", INIT[0], 0x266710) == [0x26654C] and
            [x for x in on_paths(I, 0x266564, 0x266729) if "rdi" in I[x].reg_writes and x != 0x266564] == [])
    er = sorted(set(m["disp"] for x in I.order for m in I[x].mems if m["base"] == "rdi" and 0x266734 <= x < 0x2667DC
                    and not m["write"]) | set(m["disp"] for x in I.order for m in I[x].mems if m["base"] == "rax" and
                                              x in (0x2668B7, 0x266900, 0x266973, 0x2669C2, 0x266A1C, 0x266A66)))
    R.check("the initializer reads the entry at +6, +8, +0x10, +0x14, +0x18 only; never the WORD +4 label",
            er == [6, 8, 0x10, 0x14, 0x18] and 4 not in er, str(["%X" % x for x in er]))

    # ---- pre-preset and preset
    rw = [(x, m["base"], m["disp"], m["size"]) for x in PR.order for m in PR[x].mems if m["write"]]
    row6 = jt_reach(PR, pt[6], {})
    R.check("00266AD0: row 6 goes to 00266AD0 + 0x84; the body's only writes are record +0xA0/+0xA8/+0xB8/+0xC0 "
            "through rdx = the record (+0x00); nothing writes +3",
            pt[6] == 0x266B54 and T(PR, 0x266AD0) == "mov rdx, rcx" and writers(PR, "rdx") == [0x266AD0] and
            all(b == "rdx" and dsp in (0xA0, 0xA8, 0xB8, 0xC0) for x, b, dsp, s in rw) and
            not [w for w in rw if w[2] <= 3 < w[2] + w[3]] and 0x266B9B in row6, str(rw))
    R.check("00266BD0: rows 5 and 6 go to 00266BD0 + 0x3E; row 6 stores DWORD 0x30004 at +0x1C (00266BD0 + 0x42), "
            "`cmp r8b, 5` / `jne` to the ret (+0x5F); 0x30004 has bits 16 and 17",
            qt[5] == qt[6] == 0x266C0E and T(PS, 0x266C0E) == "and r8b, 0x1f" and
            T(PS, 0x266C12) == "mov dword ptr [rcx + 0x1c], 0x30004" and PS[0x266C12].mems[0]["size"] == 4 and
            T(PS, 0x266C19) == "cmp r8b, 5" and T(PS, 0x266C1D) == "jne 0x266c2f" and (0x30004 & 0x30000) == 0x30000)
    R.check("00266BD0 and 00266AD0 never write rcx's +3, and the preset's +0x1C store is a full DWORD on every arm",
            all(not (m["disp"] <= 3 < m["disp"] + m["size"]) for x in PS.order for m in PS[x].mems if m["write"]) and
            all(m["size"] == 4 for x in PS.order for m in PS[x].mems if m["write"] and m["disp"] == 0x1C))

    # ---- later request-word writes
    w1c = [(x, I[x].text) for x in I.order for m in I[x].mems if m["write"] and m["base"] == "rbx" and
           m["disp"] < 0x20 and m["disp"] + m["size"] > 0x1C]
    expect6 = [0x2666F1, 0x266A3A, 0x266A4E, 0x266A89, 0x266A9E, 0x266AA4]
    keeps = all((I[x].mnemonic == "or") or (I[x].mnemonic == "and" and (I[x].imm[0] & 0x30000) == 0x30000)
                for x, t in w1c)
    R.check("00266530's direct writes that meet record +0x1C..+0x1F: exactly six, all after the preset call, each an "
            "OR or an AND whose mask keeps bits 16 and 17",
            [x for x, t in w1c] == expect6 and keeps and all(x > 0x2665B1 for x in expect6),
            "; ".join("%X %s" % w for w in w1c))
    rep = I[0x2668B0]
    R.check("the 0xFFFF fill is rep stosw over record +0xC8 for 0x12 WORDs (ends at +0xEC), clear of +0x1C",
            rep.text == "rep stosw word ptr [rdi], ax" and T(I, 0x2668A0) == "lea rdi, [rbx + 0xc8]" and
            T(I, 0x2668AB) == "mov ecx, 0x12")
    R.check("the initializer leaves by `jmp 0x3db280` with rcx = record (00266530 + 0x57B, + 0x59A)",
            T(I, 0x266AAB) == "mov rcx, rbx" and T(I, 0x266ACA) == "jmp 0x3db280")
    after = sorted(set(I[x].direct_target() for x in I.order if I[x].mnemonic == "call" and x > 0x2665B1))
    R.check("callees after the preset that could still reach the record: 0020E600 plus the seven stubbed in the "
            "emulation (003DB580, 00265FF0, 00265B60, 00268380, 002681E0, 003DBB60, 00268EA0)",
            after == sorted({RESOLVE[0]} | set(STUBS)), str(["%X" % a for a in after]))
    wb = [(x, I[x].text) for x in I.order for m in I[x].mems if m["write"] and m["base"] == "rbx" and
          m["disp"] <= 0xB < m["disp"] + m["size"]]
    R.check("00266530's direct writes to record +0x0B (byte stores of al after `and al, 0xf7` +0x107 and `and al, 0xfc`) "
            "never set bit 3; its two filer calls (+0x517, +0x569) are guarded by `test byte ptr [rbx + 0xb], 8`",
            [x for x, t in wb] == [0x266643, 0x266660] and T(I, 0x266637) == "and al, 0xf7" and
            T(I, 0x26665E) == "and al, 0xfc" and
            not [x for x in I.order if 0x266637 < x < 0x266660 and "rax" in I[x].reg_writes and
                 I[x].mnemonic not in ("and",)] and
            T(I, 0x266A3E) == "test byte ptr [rbx + 0xb], 8" and T(I, 0x266A90) == "test byte ptr [rbx + 0xb], 8" and
            I[0x266A47].direct_target() == FILER[0] and I[0x266A99].direct_target() == FILER[0],
            "; ".join("%X %s" % w for w in wb))
    R.check("filer 00268EA0 gates talkterm on +0x1C bit 17 (00268EA0 + 0x3C) and talkhold on bit 16 (+0x8B), rdi = rcx",
            T(F, 0x268EDC) == "test dword ptr [rcx + 0x1c], 0x20000" and
            T(F, 0x268F2B) == "test dword ptr [rdi + 0x1c], 0x10000" and T(F, 0x268ED9) == "mov rdi, rcx")

    # ---- emulation of the original code on the extract bytes
    E = emulate(img, d)
    ok_pool = E["bad"] is None and E["pool0"] == E["N"] and all(E["ptrs"])
    rowsize = [((kt[k][2] + 15) & ~15) for k in range(8)]
    rowsof = [model_row(D["counts"], i) for i in range(E["N"])]
    spacing = all(E["ptrs"][i + 1] - E["ptrs"][i] == rowsize[rowsof[i]] for i in range(E["N"] - 1)) if ok_pool else False
    stamps = ok_pool and all(E["plus3"][i] == ((kt[rowsof[i]][0] << 5) | rowsof[i]) for i in range(E["N"]))
    R.check("emulated original allocator: pool[0] = N = 96, all 96 pointers set, spaced by each row's rounded native "
            "size, and every +3 stamp = (kind << 5) | model row", ok_pool and spacing and stamps,
            "bad %s N %s pool0 %s" % (E["bad"], E["N"], E["pool0"]))
    in6 = [i for i in range(E["N"]) if E["plus3"][i] is not None and E["plus3"][i] & 0x1F == 6]
    R.check("emulated: the ordinals stamped row 6 are exactly 24..95, and ordinal 25's +3 is 0x66",
            in6 == list(range(24, 96)) and len(E["plus3"]) > TARGET and E["plus3"][TARGET] == 0x66,
            "row6 %s..%s" % (in6[:1], in6[-1:]))
    ap = E["after_preset"]
    R.check("emulated 00266530(25): it selects pool[26]; right after 00266BD0 returns, +0x1C = 0x30004 and +3 = 0x66",
            E["init_args"] is not None and E["init_args"][2] == TARGET and ap is not None and
            ap[0] == E["ptrs"][TARGET] and ap[1] == 0x30004 and ap[2] == 0x66, str(ap and (hex(ap[1]), hex(ap[2]))))
    tl = E["tail"]
    if tl:
        rec, b = tl
        p40 = struct.unpack_from("<Q", b, 0x40)[0]
        w0 = struct.unpack_from("<H", b, 0)[0]
        f1c = struct.unpack_from("<I", b, 0x1C)[0]
    R.check("emulated, at the 003DB280 tail with the seven callees stubbed: record +0x40 = descriptor + 0xD2A4, "
            "WORD +0 = 25, +0x1C keeps bits 16 and 17",
            tl is not None and rec == E["ptrs"][TARGET] and p40 == E["DESC"] + 0xD2A4 and w0 == TARGET and
            (f1c & 0x30000) == 0x30000, tl and "+0x40 = desc+%X, +0x1C = %X" % (p40 - E["DESC"], f1c))
    R.note("emulated stub order (effects NOT modelled): %s; final stubbed +0x1C = %s" %
           (" ".join("%X" % s for s in E["stubs"]), tl and hex(f1c)))


# ------------------------------------------------------------------ provenance, packet integrity
def archive_provenance(R, d):
    ev = evdir()
    am = json.load(open(os.path.join(ev, "archive-member-01.json"), encoding="utf-8"))
    sz = os.path.getsize(VBF)
    with open(VBF, "rb") as f:
        magic, hlen = struct.unpack("<4sI", f.read(8))
        nfiles = struct.unpack("<Q", f.read(8))[0]
        f.seek(0)
        hdr = f.read(hlen)
        idx = am["member"]["index"]
        roff = 0x10 + nfiles * 16 + 0x20 * idx
        sb, sb2, msize, moff, noff = struct.unpack_from("<IIQQQ", hdr, roff)
        stoff = 0x10 + nfiles * 16 + 0x20 * nfiles
        strlen = struct.unpack_from("<I", hdr, stoff)[0]
        name = hdr[stoff + 4 + noff:].split(b"\0")[0]
        blist = stoff + strlen
        nb = (msize + 0xFFFF) // 0x10000
        cs = [struct.unpack_from("<H", hdr, blist + 2 * (sb + i))[0] for i in range(nb)]
        out, pos, raws = b"", moff, []
        for i, c in enumerate(cs):
            f.seek(pos)
            raw = f.read(c)
            raws.append(raw)
            z = zlib.decompressobj()
            dec = z.decompress(raw) + z.flush()
            exp = 0x10000 if i < nb - 1 else msize - 0x10000 * (nb - 1)
            if not (z.eof and not z.unused_data and len(dec) == exp):
                dec = None
            out += dec if dec is not None else b"!"
            pos += c
    R.check("archive identity re-read: size 31,196,932,183, magic SRYK, header 11,995,716 B with the packet's sha256, "
            "89,414 members", sz == am["archive"]["bytes"] == 31196932183 and magic == b"SRYK" and
            hlen == am["archive"]["header_bytes"] and nfiles == 89414 and
            hashlib.sha256(hdr).hexdigest() == am["archive"]["header_sha256"], "%d %r %d" % (sz, magic, hlen))
    R.check("member 45552 record (own parse): blocks from 647240, 80,000 B at 24,281,213,565, name "
            "ps2data/plan_master/us/plan_map/asp_a/asp_a03/global/asp_a03.ebp",
            roff == am["member"]["index_record_offset"] and hdr[roff:roff + 32].hex() == am["member"]["index_record_hex"]
            and sb == 647240 and msize == 80000 and moff == 24281213565 and
            name == b"ps2data/plan_master/us/plan_map/asp_a/asp_a03/global/asp_a03.ebp")
    rb = [open(os.path.join(ev, "archive-block-%02d.bin" % i), "rb").read() for i in range(2)]
    R.check("the two compressed blocks (14,963 + 5,413 B) read from the archive equal the packet's retained blocks, "
            "decode strictly (zlib eof, no tail) to 65,536 + 14,464 B, and the 80,000 B equal the extract's US file",
            cs == [14963, 5413] and raws == rb and out == d and hashlib.sha256(d).hexdigest().startswith("e92d2689"),
            "blocks %s" % cs)


def evdir():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                        "FFXII TZA", "_experiments", "evidence", SLUG)


def packet_bytes(img, R):
    ev = evdir()
    mism, got = [], []
    for f in ("source-01.json", "source-binding-01.json", "source-setup-01.json"):
        for r in json.load(open(os.path.join(ev, f)))["ranges"]:
            s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
            got.append((s_, e_))
            if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"]:
                mism.append(r["start"])
    for sp in json.load(open(os.path.join(ev, "native-tables-01.json")))["spans"]:
        if img.read(int(sp["address"], 16), sp["bytes"]).hex() != sp["hex"]:
            mism.append(sp["address"])
    rs = json.load(open(os.path.join(ev, "region-switch-01.json")))
    if img.read(int(rs["address"], 16), rs["bytes"]).hex() != rs["hex"]:
        mism.append(rs["address"])
    R.check("packet's captured range hashes (6 ranges), both native table spans and the region-switch table equal "
            "this image's bytes", not mism and len(got) == 6, str(mism))
    rd = open(os.path.join(ev, "README.md"), encoding="utf-8").read()
    R.check("packet keeps open: transitive callbacks, the 266ACA -> 3DB280 tail, natural scene initialization and "
            "talkterm timing; no complete archive hash",
            "transitive callbacks" in rd and "3DB280" in rd and "natural scene initialization" in rd and
            "no complete archive hash" in rd.lower() and "timing" in rd)


def committed_manifest_sha():
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    b = subprocess.run(["git", "show", "%s:Database/FFXII TZA/_experiments/evidence/%s/manifest.json" %
                        (PRODUCER, SLUG)], capture_output=True, cwd=top).stdout
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------ controls
def p8(img, va, b):
    return img.patched(va, b)


IMG_CONTROLS = [
    ("002679F0 + 0x13D `add rdi, 2` -> `add rdi, 4` (count WORD stride)", 0x267B30, bytes([0x04])),
    ("002679F0 + 0x103 `inc ebx` -> two nops (ordinal not advanced)", 0x267AF3, bytes([0x90, 0x90])),
    ("002679F0 + 0x11E `shl al, 5` -> `shl al, 4` (kind bits misplaced)", 0x267B10, bytes([0x04])),
    ("002679F0 + 0xCB native table +4 (r8 starts at row 1's entry)", 0x267ABE, struct.pack("<i", 0x1BA4866 + 4)),
    ("00266530 + 0x1EA `cmp eax, 8` -> `cmp eax, 0xC` (version 11 takes stride 32)", 0x26671C, bytes([0x0C])),
    ("00266530 + 0x1F3 `shl rdi, 4` -> `shl rdi, 5` (stride 96)", 0x266726, bytes([0x05])),
    ("00266530 + 0x3A pool select +8 -> +0x10 (ordinal 25 gets record 26)", 0x26656E, bytes([0x10])),
    ("00266BD0 + 0x42 0x30004 -> 0x10004 (bit 17 missing)", 0x266C17, bytes([0x01])),
    ("preset table row 6 -> the 0x40 arm (00266BD0 + 0x36)", PRESET_TAB + 24, struct.pack("<I", 0x146C06)),
    ("00266AD0 + 0x8B `mov [rdx+0xb8], rax` -> `mov [rdx+3], al; 4 nops` (+3 overwritten)", 0x266B5B,
     bytes.fromhex("88420390909090")),
    ("00266BD0 + 0x3E `and r8b, 0x1f` -> `and r10b, 0x1f` (ordinal carrier written)", 0x266C0E, bytes.fromhex("4180e21f")),
    ("00266530 + 0x1C1 AND mask 0xffffdeff -> 0xfffcdeff (bits 16/17 cleared)", 0x2666F4, bytes.fromhex("ffdefcff")),
]


def mut(d, fn):
    b = bytearray(d)
    fn(b)
    return bytes(b)


def main():
    img = Img.load()
    d = open(US_EBP, "rb").read()
    R = Rep("rv_actordir")
    print("== packet integrity")
    csha = committed_manifest_sha()
    check_manifest(R, SLUG, csha)
    R.note("committed manifest at %s: sha256 %s" % (PRODUCER, csha))
    packet_bytes(img, R)
    print("== archive provenance (own VBF parse) and the extract's US file")
    archive_provenance(R, d)
    D = parse(d)
    lab_eq = sum(1 for i, l in enumerate(D["labels"]) if l == model_row(D["counts"], i))
    R.note("WORD +4 labels equal the count-prefix row for %d of %d US entries (agreement, not selection)" %
           (lab_eq, D["dircount"]))
    for lang in ("ch", "cn", "de", "es", "fr", "in", "it", "kr"):
        p = US_EBP.replace("/us/", "/%s/" % lang)
        L = parse(open(p, "rb").read())
        R.note("%s copy: counts %s, ordinal 25 row %s, label %d, name %s" %
               (lang, L["counts"], model_row(L["counts"], TARGET), L["label"], L["raw"].decode("cp932", "replace")))
    print("== shipping-image re-derivation (with the extract's US bytes)")
    checks(img, R, d)
    print("== controls (each private patched image / mutated map copy must FAIL at least one check above)")
    Rn = Rep("null")
    Rn.quiet = True
    checks(img.patched(0x267B30, img.read(0x267B30, 1)), Rn, bytes(d))
    R.check("null control: an unchanged private image copy (sha check off) and an unchanged data copy pass every check",
            Rn.fails == 0 and Rn.n > 0, "%d of %d" % (Rn.n - Rn.fails, Rn.n))
    nctl = 0
    S0 = D["S"]
    t14 = S0 + D["t14"]
    data_controls = [
        ("data: count WORD row 5 4 -> 6 (ordinal 25 moves to row 5)",
         lambda b: struct.pack_into("<H", b, t14 + 2 + 2 * 5, 6)),
        ("data: version WORD 11 -> 7 (stride 32)", lambda b: struct.pack_into("<H", b, S0, 7)),
        ("data: row count 8 -> 5 (row 6 never carved)", lambda b: struct.pack_into("<H", b, t14, 5)),
    ]
    for label, va, nb in IMG_CONTROLS:
        Pimg = img.patched(va, nb)
        if Pimg.d == img.d:
            raise SystemExit("control %s did not change the image" % label)
        nctl += 1
        R.check("control: " + label, run_ctl(Pimg, d), last_why[0])
    for label, fn in data_controls:
        md = mut(d, fn)
        assert md != d
        nctl += 1
        R.check("control: " + label, run_ctl(img, md), last_why[0])
    lab7 = mut(d, lambda b: struct.pack_into("<H", b, S0 + D["eoff"] + 4, 7))
    Rl = Rep("label")
    Rl.quiet = True
    try:
        checks(img, Rl, lab7)
        lf = [f for f in Rl.failed]
    except Exception as e:
        lf = ["refused %r" % e]
    nctl += 1
    R.check("countermodel: entry 25's WORD +4 label 6 -> 7 changes nothing but the label check (row 6, 0x66, 0x30004, "
            "binding all still PASS)", lf == [x for x in lf if x.startswith("entry 25 is at section offset")] and
            len(lf) == 1 and parse(lab7)["label"] == 7, str(lf))
    disk = hashlib.sha256(open(find_exe(), "rb").read()).hexdigest()
    R.check("exe on disk still hashes to the pinned sha256 after all controls", disk == SHA_PIN, disk)
    R.check("extract US asp_a03.ebp on disk unchanged after all controls",
            hashlib.sha256(open(US_EBP, "rb").read()).hexdigest() == hashlib.sha256(d).hexdigest())
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))


last_why = [""]


def run_ctl(im, d):
    Rc = Rep("c")
    Rc.quiet = True
    try:
        checks(im, Rc, d)
        last_why[0] = "%d failed: %s" % (Rc.fails, "; ".join(f[:70] for f in Rc.failed[:3]))
        return Rc.fails > 0
    except Exception as e:
        last_why[0] = "refused: %r after %d failed: %s" % (e, Rc.fails, "; ".join(f[:70] for f in Rc.failed[:3]))
        return True


if __name__ == "__main__":
    main()
