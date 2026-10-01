"""sp_indep.py - SWE2-AUDIT-SPEC independent re-derivation for ASTRA-REQ-SPEC-SPATTACK-REMAP-0930 (2026-09-30).

Written without the packet's checker or capture drivers: pefile + capstone over the certified image (sha256 asserted).
Canonical VAs include the image base 0x120000.

  A  decode the load-bearing bodies and assert each instruction the packet's claims rest on (30DB70 all three encoders,
     3068D4's encoder, reader 309C00, script adapters 348330 / 348870, 30EEA0, 30CFB0, 30D070, 387090)
  B  exact-semantics arithmetic, written from the decoded instructions (32-bit sub / lea, cmp -1, 16-bit add), over
     every 16-bit word, for each of the three encoders; then 511..534 and the alias set
  C  every instruction image-wide whose memory operand OVERLAPS the dword cell 022C2178 (rip-relative, image-base-relative
     [reg+disp] and absolute), plus 8-byte VA / 4-byte RVA values in any section; known positives and an adjacent-cell
     negative control
  D  callers of 309C00 / 30EEA0 / 348870 / 30DB70 / the 3068D4 body: E8/E9 (own scan), jcc 0F 8x, stored VA / RVA
  E  .pdata rows for 309C00, 30D720, 30EEA0, 30DB70, 3068D4 (the failed01 leaf lesson)
"""
import hashlib, struct, sys
import numpy as np
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM
from capstone.x86 import X86_REG_RIP, X86_REG_INVALID

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "image hash mismatch"
pe = pefile.PE(data=raw, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
assert IB == 0x120000
SECS = [(s.Name.rstrip(b"\0").decode(), IB + s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData,
         bool(s.Characteristics & 0x20000000)) for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
FAILS = []


def off(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def dis(a, b):
    o = off(a)
    return list(md.disasm(raw[o:o + (b - a)], a))


def say(*a):
    print(*a)


def check(cond, what):
    say(("PASS " if cond else "FAIL ") + what)
    if not cond:
        FAILS.append(what)


def ins_map(a, b):
    L = dis(a, b)
    check(sum(i.size for i in L) == b - a, "decode %08X..%08X covers %d B (%d instructions)" % (a, b, b - a, len(L)))
    return {i.address: i for i in L}


def want(M, pc, mn, ops):
    i = M.get(pc)
    got = (i.mnemonic, i.op_str) if i else None
    check(got == (mn, ops), "%08X %s %s%s" % (pc, mn, ops, "" if got == (mn, ops) else "   got %r" % (got,)))


def riptgt(i):
    for op in i.operands:
        if op.type == CS_OP_MEM and op.mem.base == X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


say("== A. decoded anchors (own decode of the image)")
M = ins_map(0x30DB70, 0x30DCA6)
for pc, mn, ops in [
        (0x30DB84, "je", "0x30dc34"), (0x30DB97, "je", "0x30dc24"),
        (0x30DB9D, "movzx", "r8d, word ptr [rbx + 4]"), (0x30DBA5, "sub", "edx, 0xf2"), (0x30DBAB, "je", "0x30dc06"),
        (0x30DBB0, "je", "0x30dbff"), (0x30DBB5, "je", "0x30dbf8"), (0x30DBBE, "call", "0x2ffcf0"),
        (0x30DBC5, "jne", "0x30dc24"), (0x30DBC7, "movzx", "ecx, word ptr [rbx + 4]"), (0x30DBCB, "mov", "eax, 0xffff"),
        (0x30DBD2, "cmp", "cx, ax"), (0x30DBD5, "je", "0x30dbea"), (0x30DBD7, "movzx", "eax, cx"),
        (0x30DBDA, "sub", "eax, 0xd0"), (0x30DBE5, "jmp", "0x30dc8b"), (0x30DBEA, "or", "eax, 0xffffffff"),
        (0x30DC24, "mov", "eax, 1"),
        # NULL-record branch: second encoder
        (0x30DC34, "movzx", "eax, word ptr [rip + 0x1fb4555]"), (0x30DC48, "cmp", "ax, 0xf"), (0x30DC4C, "jbe", "0x30dc83"),
        (0x30DC55, "call", "0x2f8d60"), (0x30DC5A, "movzx", "edi, ax"), (0x30DC62, "mov", "ebx, edi"),
        (0x30DC6F, "je", "0x30dc83"), (0x30DC76, "cmp", "di, ax"), (0x30DC79, "je", "0x30dc83"),
        (0x30DC7B, "lea", "eax, [rbx - 0xd0]"), (0x30DC83, "or", "eax, 0xffffffff"),
        (0x30DC98, "mov", "dword ptr [rip + 0x1fb44da], eax")]:
    want(M, pc, mn, ops)
check(riptgt(M[0x30DC98]) == 0x22C2178, "30DC98 stores the dword cell 022C2178")
check(riptgt(M[0x30DC34]) == 0x22C2190, "30DC34 reads the word at 022C2190 (NULL-record branch source)")
# the three special words F2/F3/F4 leave through 300BC0 and return 1 without the store
want(M, 0x30DC1F, "call", "0x300bc0")
say("  30DB70 store paths: record branch (2FFCF0==0, word not F2/F3/F4) -> 30DBDA sub / 30DBEA -1; NULL-record branch"
    " -> 30DC7B lea / 30DC83 -1; both join 30DC8B and store at 30DC98")

M3 = ins_map(0x3068BA, 0x3068E5)
for pc, mn, ops in [(0x3068BD, "mov", "edx, 0xffff"), (0x3068C2, "cmp", "ax, dx"), (0x3068C5, "je", "0x3068d1"),
                    (0x3068C7, "movzx", "eax, ax"), (0x3068CA, "sub", "eax, 0xd0"), (0x3068D1, "or", "eax, 0xffffffff"),
                    (0x3068D4, "mov", "dword ptr [rip + 0x1fbb89e], eax")]:
    want(M3, pc, mn, ops)
check(riptgt(M3[0x3068D4]) == 0x22C2178, "3068D4 is a third encoder store to 022C2178 (same word - 0xD0 / FFFF -> -1)")

R = ins_map(0x309C00, 0x309C32)
for pc, mn, ops in [(0x309C00, "mov", "eax, dword ptr [rip + 0x1fb8572]"), (0x309C06, "cmp", "eax, -1"),
                    (0x309C09, "jne", "0x309c0e"), (0x309C0B, "xor", "eax, eax"), (0x309C0D, "ret", ""),
                    (0x309C13, "mov", "dword ptr [rdx], eax"),
                    (0x309C22, "mov", "dword ptr [rip + 0x1fb854c], 0xffffffff"), (0x309C2C, "mov", "eax, 1"),
                    (0x309C31, "ret", "")]:
    want(R, pc, mn, ops)
check(riptgt(R[0x309C00]) == 0x22C2178 and riptgt(R[0x309C22]) == 0x22C2178,
      "309C00 reads and 309C22 re-arms (-1) the same cell 022C2178: the read consumes the value")

S = ins_map(0x348330, 0x3483D5)
want(S, 0x348381, "mov", "rdx, rsi")
want(S, 0x34838A, "call", "0x309c00")
want(S, 0x3483D0, "jmp", "0x26b4e0")
A = ins_map(0x348870, 0x3488AC)
for pc, mn, ops in [(0x348880, "call", "0x267e10"), (0x348888, "mov", "ebx, eax"), (0x34888A, "call", "0x267e10"),
                    (0x34888F, "mov", "edx, ebx"), (0x348891, "mov", "ecx, eax"), (0x348893, "call", "0x30eea0")]:
    want(A, pc, mn, ops)
say("  348870: FIRST popped integer -> EDX (the id), SECOND popped integer -> ECX (to 31B7E0)")

E = ins_map(0x30EEA0, 0x30EF17)
for pc, mn, ops in [(0x30EEA6, "mov", "ebx, edx"), (0x30EEA8, "cmp", "edx, -1"), (0x30EEAB, "je", "0x30eeb7"),
                    (0x30EEAD, "mov", "eax, 0xd0"), (0x30EEB2, "add", "bx, ax"), (0x30EEB7, "mov", "ebx, 0xffff"),
                    (0x30EEBC, "call", "0x31b7e0"), (0x30EEC4, "jne", "0x30eecf"), (0x30EEC6, "or", "eax, 0xffffffff"),
                    (0x30EECF, "cmp", "dword ptr [rip + 0x1fb329a], 4"), (0x30EED6, "je", "0x30eee3"),
                    (0x30EED8, "mov", "eax, 0xfffffffe"), (0x30EEF5, "movzx", "r8d, bx"),
                    (0x30EEF9, "mov", "word ptr [rax + 0x758], bx"), (0x30EF00, "call", "0x30cfb0")]:
    want(E, pc, mn, ops)
check(riptgt(E[0x30EECF]) == 0x22C2170, "30EECF gate reads 022C2170 == 4 before the 30CFB0 call (else returns -2)")

W = ins_map(0x30CFB0, 0x30D069)
for pc, mn, ops in [(0x30CFBF, "cmp", "byte ptr [rcx + 4], 0xff"), (0x30CFC3, "movzx", "ebx, r8w"),
                    (0x30CFCC, "jne", "0x30d059"), (0x30D011, "test", "dword ptr [rcx + 0xc], 0x40000000"),
                    (0x30D022, "sub", "ax, cx"), (0x30D025, "cmp", "ax, 0x21"), (0x30D029, "ja", "0x30d039"),
                    (0x30D041, "jne", "0x30d059"), (0x30D04C, "movzx", "edx, bx"), (0x30D051, "call", "0x30d070")]:
    want(W, pc, mn, ops)
say("  30CFB0 carries its own 0..0x21 (id-0xD0) test, but only under flag 0x40000000 and only to pick the once-bit"
    " 022C2158&2 path; the bit30 gate is the separate prior review, not this remap")
Z = ins_map(0x30D070, 0x30D0C2)
want(Z, 0x30D084, "movzx", "r10d, dx")
want(Z, 0x30D0AA, "cmp", "word ptr [r9 + 0x1c], cx")
want(Z, 0x30D0B4, "cmp", "r8b, 0x20")
Z2 = ins_map(0x30D0FD, 0x30D155)
want(Z2, 0x30D14F, "mov", "word ptr [rcx + 0x1c], r10w")
P2 = ins_map(0x304D70, 0x304E29)
want(P2, 0x304E12, "call", "0x387090")
want(P2, 0x304E1A, "movzx", "r8d, ax")
want(P2, 0x304E24, "call", "0x30cfb0")
say("  30CFB0 argument sources (callers counted in D): 304E24 via the 387090 result, 30EF00 via 30EEA0)")
G = ins_map(0x387090, 0x387125)
want(G, 0x387100, "mov", "ecx, 0x9f")
want(G, 0x387105, "cmp", "word ptr [rax + 0x714], cx")
want(G, 0x38710E, "movzx", "eax, word ptr [rbx + 0x10]")
want(G, 0x387118, "movzx", "eax, word ptr [rax + 0x714]")

say("\n== B. exact-semantics arithmetic over all 65536 words (own model of the decoded instructions)")
M32 = 0xFFFFFFFF


def s32(x):
    x &= M32
    return x - (1 << 32) if x & 0x80000000 else x


def enc_30dbda(w):          # movzx ecx,word; cmp cx,0xffff; je -> or eax,-1 ; else movzx eax,cx; sub eax,0xd0
    return -1 if w == 0xFFFF else s32(w - 0xD0)


def enc_30dc7b(w):          # movzx edi,ax; mov ebx,edi; cmp di,0xffff; je -> -1; else lea eax,[rbx-0xd0] (32-bit)
    return -1 if w == 0xFFFF else s32(w - 0xD0)


def enc_3068ca(w):          # cmp ax,0xffff; je -> -1; else movzx eax,ax; sub eax,0xd0
    return -1 if w == 0xFFFF else s32(w - 0xD0)


def reader(cell):           # 309C00: cmp eax,-1; jne -> copy, return 1; else return 0
    return (cell != -1), (cell if cell != -1 else None)


def adapter_30eea0(edx):    # mov ebx,edx; cmp edx,-1; je -> ebx=0xffff; else add bx,0xd0 (16-bit); movzx r8d,bx
    ebx = edx & M32
    if s32(edx) == -1:
        ebx = 0xFFFF
    else:
        ebx = (ebx & 0xFFFF0000) | (((ebx & 0xFFFF) + 0xD0) & 0xFFFF)
    return ebx & 0xFFFF


for name, enc in [("30DBDA", enc_30dbda), ("30DC7B", enc_30dc7b), ("3068CA", enc_3068ca)]:
    unavailable = [w for w in range(65536) if not reader(enc(w))[0]]
    alias = [w for w in range(65536) if reader(enc(w))[0] and adapter_30eea0(reader(enc(w))[1]) != w]
    comp_alias = [w for w in range(65536) if adapter_30eea0(enc(w)) != w]
    cand = [(w, enc(w), reader(enc(w))[0], adapter_30eea0(enc(w))) for w in range(511, 535)]
    ok = all(a and d == w for w, e, a, d in cand)
    say("  %s: reader-unavailable words %s; available-but-changed %s; composed (ignoring reader) changed %s"
        % (name, ["%04X" % w for w in unavailable], alias, ["%04X" % w for w in comp_alias]))
    say("  %s: 511..534 -> queued %d..%d, all available and decode unchanged: %s"
        % (name, cand[0][1], cand[-1][1], ok))
    check(unavailable == [0xCF, 0xFFFF] and alias == [] and comp_alias == [0xCF] and ok,
          "%s: exactly CF and FFFF are unavailable, no available word changes, candidates survive" % name)
say("  note: in 30DB70's record branch words F2/F3/F4 and any 2FFCF0 != 0 leave before the store; the NULL branch"
    " stores -1 for (word-0xE2) u16 <= 0xF and when 322C50 returns 0. These narrow which words reach the cell,"
    " they add no alias.")
check(enc_30dbda(0) == -208 and reader(-208)[0] and adapter_30eea0(-208) == 0,
      "word 0 queues -208 (negative but not -1): the reader passes it and 30EEA0 restores 0 by the 16-bit add")

say("\n== C. image-wide references that overlap the dword cell 022C2178 (all forms)")
CELL, CEND = 0x22C2178, 0x22C217C
REL = CELL - IB
hits = {}


def dwords(blob):
    b = np.frombuffer(blob, dtype=np.uint8).astype(np.int64)
    u = b[:-3] | (b[1:-2] << 8) | (b[2:-1] << 16) | (b[3:] << 24)
    return np.where(u >= 1 << 31, u - (1 << 32), u)


for n, v, vs, p, rs, x in SECS:
    if not x:
        continue
    blob = raw[p:p + min(vs, rs)]
    d = dwords(blob)
    pos = np.arange(len(d), dtype=np.int64)
    near = np.zeros(len(d), dtype=bool)
    for t in (0, 1, 2, 4):
        tg = v + pos + 4 + t + d
        near |= (tg >= CELL - 16) & (tg < CEND)
    near |= (d >= CELL - 16 - IB) & (d < CEND - IB)
    du = d & M32
    near |= (du >= CELL - 16) & (du < CEND)
    for o in np.nonzero(near)[0].tolist():
        d0 = int(d[o])
        ib_near = CELL - 16 - IB <= d0 < CEND - IB
        for st in range(max(0, o - 11), o):
            i = next(md.disasm(blob[st:st + 15], v + st, count=1), None)
            if not i or not (st + i.size >= o + 4):
                continue
            for op in i.operands:
                if op.type != CS_OP_MEM:
                    continue
                m = op.mem
                if m.base == X86_REG_RIP:
                    t, form = i.address + i.size + m.disp, "rip"
                elif m.base != X86_REG_INVALID and m.disp == d0 and ib_near:
                    t, form = IB + m.disp, "imagebase[%s]" % i.reg_name(m.base)
                elif m.base == X86_REG_INVALID and m.index == X86_REG_INVALID:
                    t, form = m.disp & M32, "abs"
                else:
                    continue
                if t < CEND and t + op.size > CELL:
                    hits[i.address] = (i.mnemonic, i.op_str, form, op.size, t)
for a in sorted(hits):
    mn, ops, form, sz, t = hits[a]
    say("  %08X  %-6s %-45s %s width %d -> %08X" % (a, mn, ops, form, sz, t))
say("  overlapping instructions: %d" % len(hits))
for pc in (0x309C00, 0x309C22, 0x30D722, 0x3068D4, 0x30DC98):
    check(pc in hits, "known positive %08X found by the overlap sweep" % pc)
check(0x30D751 not in hits, "adjacent-cell negative: 30D751 qword store at 022C217C does not overlap the cell")
check(0x30D745 not in hits, "adjacent-cell negative: 30D745 dword store at 022C2174 does not overlap the cell")
# image-base-relative sensitivity: a known [reg+disp] jump-table read (00582860, table 00582F54)
ib_ctrl = []
for n, v, vs, p, rs, x in SECS:
    if not x:
        continue
    blob = raw[p:p + min(vs, rs)]
    k = blob.find(struct.pack("<i", 0x582F54 - IB))
    while k >= 0:
        ib_ctrl.append(v + k)
        k = blob.find(struct.pack("<i", 0x582F54 - IB), k + 1)
check(any(0x582860 <= a < 0x582F54 for a in ib_ctrl), "image-base-relative control: disp32 0x462F54 found inside"
      " 00582860 (the msg-18 table read) at %s" % ["%08X" % a for a in ib_ctrl])
vals = []
for n, v, vs, p, rs, x in SECS:
    blob = raw[p:p + min(vs, rs)]
    for pat, what in [(struct.pack("<Q", CELL), "va64"), (struct.pack("<I", REL), "rva32")]:
        k = blob.find(pat)
        while k >= 0:
            vals.append((n, v + k, what))
            k = blob.find(pat, k + 1)
say("  stored 64-bit VA / 32-bit RVA of the cell in any section: %s" % vals)

say("\n== D. callers (own E8/E9 scan, jcc 0F 8x scan, stored VA64 / RVA32)")
TEXT = [(v, raw[p:p + min(vs, rs)]) for n, v, vs, p, rs, x in SECS if x]


CALLS = {}


def build_calls():
    for v, blob in TEXT:
        b = np.frombuffer(blob, dtype=np.uint8)
        d = dwords(blob)
        pos = np.arange(len(d), dtype=np.int64)
        e8 = np.nonzero((b[:-4] == 0xE8) | (b[:-4] == 0xE9))[0]
        e8 = e8[e8 + 1 < len(d)]
        for o, t in zip(e8.tolist(), (v + e8 + 5 + d[e8 + 1]).tolist()):
            CALLS.setdefault(t, ([], []))[0].append(v + o)
        j = np.nonzero((b[:-5] == 0x0F) & (b[1:-4] >= 0x80) & (b[1:-4] <= 0x8F))[0]
        j = j[j + 2 < len(d)]
        for o, t in zip(j.tolist(), (v + j + 6 + d[j + 2]).tolist()):
            CALLS.setdefault(t, ([], []))[1].append(v + o)


build_calls()


def callers(tgt):
    e8, jcc = CALLS.get(tgt, ([], []))
    st = []
    for n, v, vs, p, rs, x in SECS:
        blob = raw[p:p + min(vs, rs)]
        for pat, what in [(struct.pack("<Q", tgt), "va64"), (struct.pack("<I", tgt - IB), "rva32")]:
            k = blob.find(pat)
            while k >= 0:
                st.append("%s %s@%08X" % (what, n, v + k))
                k = blob.find(pat, k + 1)
    return e8, jcc, st


# known-positive control for the E8 scan
check(0x25DAED in callers(0x32FC30)[0], "E8 scan control: 0025DAED -> 0032FC30 found")
PD = []
for n, v, vs, p, rs, x in SECS:
    if n == ".pdata":
        blob = raw[p:p + min(vs, rs)]
        for k in range(0, len(blob) - 11, 12):
            a, b, u = struct.unpack_from("<III", blob, k)
            if a:
                PD.append((a + IB, b + IB, u + IB))


def pdrow(pc):
    return [r for r in PD if r[0] <= pc < r[1]]


for tgt in (0x309C00, 0x30EEA0, 0x348870, 0x348330, 0x30DB70, 0x30D720, 0x30CFB0):
    e8, jcc, st = callers(tgt)
    rv = [r for r in st if r.startswith("rva32 .pdata") is False]
    say("  %08X: E8/E9 %s; jcc %s; stored %s" % (tgt, ["%08X" % a for a in e8], ["%08X" % a for a in jcc], st))
e8, jcc, st = callers(0x309C00)
check(sorted(e8) == [0x2D6175, 0x34838A] and not jcc, "309C00 has exactly two direct callers 002D6175 and 0034838A")
e8b, jccb, stb = callers(0x30CFB0)
check(sorted(e8b) == [0x304E24, 0x30EF00] and not jccb, "30CFB0 has exactly two E8/E9 callers 00304E24 and 0030EF00, no jcc")
D2 = ins_map(0x2D616B, 0x2D6184)
want(D2, 0x2D616B, "lea", "rdx, [rsp + 0x20]")
want(D2, 0x2D6175, "call", "0x309c00")
want(D2, 0x2D617A, "mov", "ecx, 5")
say("  002D6175 calls the reader with stack out-pointers and overwrites ecx next: it drains the cell (309C22 re-arms"
    " -1) outside the script path; whether its result is used later in that body is not read here")

say("\n== E. .pdata rows")
for pc in (0x309C00, 0x30D720, 0x30D722, 0x30D758, 0x30EEA0, 0x30DB70, 0x30DC98, 0x3068D4, 0x348870):
    say("  %08X: %s" % (pc, ["%08X..%08X unwind %08X" % r for r in pdrow(pc)]))
check(pdrow(0x309C00) == [] and pdrow(0x30D722) == [], "309C00 and 30D720 are leaves with no .pdata row (failed01 lesson)")

say("\n== F. base pointers formed at or below the cell (indirect-alias spot check, not a closure)")
for lo, hi, reg, lea in [(0x30D82D, 0x30D8A0, "rbp", 0x30D832), (0x313239, 0x3133B6, "r13", 0x313267)]:
    L = dis(lo, hi)
    li = [i for i in L if i.address == lea]
    check(bool(li) and riptgt(li[0]) == 0x22C2170, "%08X lea %s -> 022C2170" % (lea, reg))
    for i in L:
        if reg in i.op_str and i.address != lea:
            say("    %08X %s %s" % (i.address, i.mnemonic, i.op_str))
say("  every use indexes a table at +0x22..+0x48 from 022C2170 (022C2192 and up) with a register index, or"
    " restores the register; 313399 forms r13+edx (edx 0..3 from the loop above) for a byte store at +0x22."
    " None reaches 022C2178 for a non-negative index; the index signs at 30D86B/313320 are not bounded here.")

say("\nFAILS %d" % len(FAILS))
for f in FAILS:
    say("  " + f)
