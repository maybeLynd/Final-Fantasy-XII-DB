"""rv_slots.py - FABLE independent re-derivation for ASTRA packet ov42-slot-id-producer (0ada51452, OV-42).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the filecache-route2-commit-key review, sha256
69f9bc40be32abcc...).  Does not import or run ASTRA's prove.py, capture drivers, control.py, freeze/publication
scripts or the shared role adapter (reg_tracking.py).

Method:
  * image sha256; complete linear decode of the allocator 0030D070 and the acquire wrapper 0030CFB0, each against
    the image's own .pdata, closed local CFGs, every ret;
  * register-write censuses for the action WORD, the identity, the slot index and the slot pointers; the marker
    compare; the scan bound; every memory write of both bodies with its base, displacement and width;
  * the reviewer's own finite reading of the scan index r8b (values reachable at each test), which decides the
    null-record, sign and > 31 arms;
  * a concrete emulation (unicorn) of the ORIGINAL two bodies over synthetic slot arrays and synthetic rows (all
    33 occupancy positions, the 24 candidate words 511..534, FFFF, the D0..F1 exception and the three wrapper
    gates), recording every memory write.  Only the address resolver 0020E600 is run besides the two bodies;
  * a raw E8/E9 rel32 census of direct callers of both bodies;
  * controls patch a private in-memory copy of the image; the exe on disk is never written and its sha256 is
    rechecked at the end.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, SHA256 as SHA_PIN  # noqa: E402

ALLOC = (0x0030D070, 0x0030D155)   # 229 B
WRAP = (0x0030CFB0, 0x0030D069)    # 185 B = 166 B retained prefix + 19 B suffix
RESOLVE = (0x0020E600, 0x0020E60A)
SLOTS = 0x022C17B0
HEAD, TAILP = 0x022BE978, 0x022BEB88
FLAGS = 0x022C2158
SEQ = 0x022C2160
ROWDESC = 0x02EBF138
RELBASE = 0x01F83530
SLUG = "ov42-slot-id-producer"
PRODUCER = "0ada51452"
CANDS = list(range(511, 535))


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


def readers(B, fam):
    return [a for a in B.order if fam in B[a].reg_reads]


def rip_target(I):
    m = I.mems[0]
    return I.address + I.size + m["disp"]


# ------------------------------------------------------------------ emulation of the original code
class Emu(object):
    """Minimal unicorn host: the two bodies, 0020E600, the .data cells they use, a stack and a synthetic row area."""

    def __init__(self, img):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_MEM_WRITE, UC_HOOK_CODE
        from unicorn import x86_const as X
        self.X = X
        mu = self.mu = Uc(UC_ARCH_X86, UC_MODE_64)
        pages = set()
        for s, e in (ALLOC, WRAP, RESOLVE):
            for p in range(s & ~0xFFF, (e + 0xFFF) & ~0xFFF, 0x1000):
                pages.add(p)
        for a in (SLOTS, SLOTS + 32 * 48, HEAD, TAILP, FLAGS, SEQ, ROWDESC, RELBASE):
            pages.add(a & ~0xFFF)
        for p in sorted(pages):
            mu.mem_map(p, 0x1000)
            buf = bytearray(0x1000)
            try:
                o = img.off(p)
                buf[:] = img.d[o:o + 0x1000].ljust(0x1000, b"\0")
            except ValueError:
                pass  # .data virtual tail: zero
            mu.mem_write(p, bytes(buf))
        self.STK, self.RET, self.UNIT, self.ROWS = 0x7F000000, 0x7E000000, 0x7D000000, 0x30000000
        mu.mem_map(self.STK, 0x10000)
        mu.mem_map(self.RET, 0x1000)
        mu.mem_map(self.UNIT, 0x1000)
        mu.mem_map(self.ROWS, 0x400000)
        self.writes = []
        self.left = None
        self.allowed = [ALLOC, WRAP, RESOLVE]

        def wh(uc, access, addr, size, value, ud):
            self.writes.append((uc.reg_read(X.UC_X86_REG_RIP), addr, size, value))

        def ch(uc, addr, size, ud):
            if addr != self.RET and not any(s <= addr < e for s, e in self.allowed):
                self.left = addr
                uc.emu_stop()

        mu.hook_add(UC_HOOK_MEM_WRITE, wh)
        mu.hook_add(UC_HOOK_CODE, ch)
        # synthetic row descriptor: [02EBF138] -> desc; [desc+0xC] = 0x100; WORD [desc+8] = 60 (row stride)
        # 0020E600 adds [01F83530] = ROWS, so the first row is ROWS + 0x100.
        self.DESC = self.ROWS
        mu.mem_write(ROWDESC, struct.pack("<Q", self.DESC))
        mu.mem_write(RELBASE, struct.pack("<Q", self.ROWS))
        mu.mem_write(self.DESC + 0xC, struct.pack("<I", 0x100))
        mu.mem_write(self.DESC + 8, struct.pack("<H", 60))

    def set_slots(self, free):
        """free: set of slot indices whose marker WORD +0x1C is FFFF; others get 0x0001."""
        for i in range(32):
            self.mu.mem_write(SLOTS + 48 * i, b"\0" * 48)
            self.mu.mem_write(SLOTS + 48 * i + 0x1C, struct.pack("<H", 0xFFFF if i in free else 0x0001))
        self.mu.mem_write(HEAD, b"\0" * 8)
        self.mu.mem_write(TAILP, b"\0" * 8)

    def row(self, word, bit30):
        a = self.ROWS + 0x100 + word * 60
        self.mu.mem_write(a + 0xC, struct.pack("<I", 0x40000000 if bit30 else 0))

    def u32(self, a):
        return struct.unpack("<I", bytes(self.mu.mem_read(a, 4)))[0]

    def u16(self, a):
        return struct.unpack("<H", bytes(self.mu.mem_read(a, 2)))[0]

    def call(self, entry, rcx, rdx, r8):
        X = self.X
        sp = self.STK + 0x8000
        self.mu.mem_write(sp, struct.pack("<Q", self.RET))
        self.mu.reg_write(X.UC_X86_REG_RSP, sp)
        self.mu.reg_write(X.UC_X86_REG_RCX, rcx)
        self.mu.reg_write(X.UC_X86_REG_RDX, rdx)
        self.mu.reg_write(X.UC_X86_REG_R8, r8)
        self.mu.reg_write(X.UC_X86_REG_RAX, 0x1111111111111111)
        self.mu.reg_write(X.UC_X86_REG_RDI, 0x2222222222222222)
        self.writes = []
        self.left = None
        self.mu.emu_start(entry, self.RET, count=20000)
        return self.mu.reg_read(X.UC_X86_REG_RAX)

    def nonframe(self):
        return [w for w in self.writes if not (self.STK <= w[1] < self.STK + 0x10000)]


def slot_writes(ws, k):
    base = SLOTS + 48 * k
    return sorted((a - base, s, v) for pc, a, s, v in ws if base <= a < base + 48)


def emu_checks(img, R):
    E = Emu(img)
    # --- allocator alone: every first-free position, the full array, candidates and FFFF
    sel_ok, writes_ok = True, True
    bad = []
    for k in range(32):
        E.set_slots({k} | set(range(k + 3, 32, 5)))
        ax = E.call(ALLOC[0], 0xABCD1234, 0x1FF + (k % 24), 0)
        nf = E.nonframe()
        sw = slot_writes(nf, k)
        exp = sorted([(0, 8, 0), (8, 8, 0), (0x10, 4, 1), (0x14, 4, 1), (0x18, 4, 1), (0x1C, 2, 0x1FF + (k % 24)),
                      (0x20, 4, 0xABCD1234)])
        others = [w for w in nf if not (SLOTS + 48 * k <= w[1] < SLOTS + 48 * k + 48) and w[1] not in (HEAD, TAILP)]
        if E.left or (ax & 0xFFFFFFFF) != k:
            sel_ok = False
            bad.append("k%d ax %X left %s" % (k, ax, E.left))
        if sw != exp or others or E.u16(SLOTS + 48 * k + 0x1C) != 0x1FF + (k % 24):
            writes_ok = False
            bad.append("k%d writes %s others %s" % (k, sw, others[:2]))
    R.check("emulated 0030D070, first free slot at each k = 0..31 (later free slots present): returns EAX = k; its "
            "only non-frame writes are slot k +0/+8 (links), +0x10/+0x14/+0x18 = DWORD 1, +0x20 = ECX, WORD +0x1C = "
            "the incoming DX, plus the list head/tail cells", sel_ok and writes_ok, "; ".join(bad[:3]))
    E.set_slots(set())
    ax = E.call(ALLOC[0], 0x55, 0x1FF, 0)
    R.check("emulated 0030D070 with all 32 markers occupied: AL = 0xFF, no non-frame write at all",
            (ax & 0xFF) == 0xFF and E.nonframe() == [] and not E.left, "rax %X writes %s" % (ax, E.nonframe()[:3]))
    R.note("all-occupied return: RAX = %X (the arm sets AL only; the rest is the last index's movsx)" % ax)
    stored = []
    for w in CANDS + [0xFFFF, 0xD0, 0xF1, 0x0000]:
        E.set_slots({7, 9})
        ax = E.call(ALLOC[0], 0x77, 0xABCD0000 | w, 0)
        stored.append((w, ax & 0xFFFFFFFF, E.u16(SLOTS + 48 * 7 + 0x1C), E.u16(SLOTS + 48 * 9 + 0x1C)))
    R.check("emulated 0030D070: each of 511..534, FFFF, D0, F1 and 0 (upper RDX bits set) is stored unchanged in the "
            "first free slot 7, and slot 9 stays free", all(a == 7 and s7 == w and s9 == 0xFFFF for w, a, s7, s9 in
                                                             stored), str([x for x in stored if x[2] != x[0]][:3]))
    E.set_slots({7})
    E.call(ALLOC[0], 0x77, 0xFFFF, 0)
    R.check("sentinel: after a FFFF word slot 7 still reads free (marker FFFF) although +0x10/+0x14/+0x18/+0x20 and "
            "the links were written", E.u16(SLOTS + 48 * 7 + 0x1C) == 0xFFFF and E.u32(SLOTS + 48 * 7 + 0x10) == 1 and
            E.u32(SLOTS + 48 * 7 + 0x20) == 0x77)
    # --- the wrapper's gates
    U = E.UNIT
    res = {}

    def wrap(word, bit30, unit4=0xFF, flags=0, seq=0, free=frozenset({3})):
        E.set_slots(set(free))
        E.row(word, bit30)
        E.mu.mem_write(U, b"\0" * 16)
        E.mu.mem_write(U + 4, bytes([unit4]))
        E.mu.mem_write(FLAGS, struct.pack("<I", flags))
        E.mu.mem_write(SEQ, struct.pack("<I", seq))
        E.call(WRAP[0], U, 0x99, word)
        nf = E.nonframe()
        slot = [w for w in nf if SLOTS <= w[1] < SLOTS + 32 * 48]
        return dict(u4=bytes(E.mu.mem_read(U + 4, 1))[0], flags=E.u32(FLAGS), slot=slot, nf=nf, left=E.left,
                    marker=E.u16(SLOTS + 3 * 48 + 0x1C), ident=E.u32(SLOTS + 3 * 48 + 0x20))
    r = wrap(511, False, unit4=5)
    R.check("emulated 0030CFB0: unit+4 = 5 (not FF) returns without calling the allocator and with no non-frame write",
            r["u4"] == 5 and r["nf"] == [] and not r["left"], str(r["nf"][:3]))
    oks = []
    for w in CANDS:
        r = wrap(w, False)
        oks.append(r["u4"] == 3 and r["marker"] == w and r["ident"] == 0x99 and r["flags"] == 0)
    R.check("emulated 0030CFB0, bit-30 clear: each of 511..534 lands in free slot 3 with identity EDX, and AL = 3 "
            "becomes unit+4; 022C2158 untouched", all(oks), "%d of 24" % sum(oks))
    r1 = wrap(511, True, flags=0)
    r2 = wrap(511, True, flags=2)
    R.check("emulated 0030CFB0, bit-30 set, word 511: flag bit 1 clear -> sets it and allocates; bit 1 set -> no "
            "allocation, unit+4 stays FF",
            r1["u4"] == 3 and r1["marker"] == 511 and r1["flags"] == 2 and r2["u4"] == 0xFF and r2["slot"] == [] and
            r2["flags"] == 2, "%s / %s" % ((r1["u4"], r1["flags"]), (r2["u4"], r2["slot"][:1])))
    r3 = wrap(0xD5, True, flags=2, seq=5)
    r4 = wrap(0xD5, True, flags=2, seq=4)
    R.check("emulated 0030CFB0: a D0..F1 word with bit 30 bypasses the set flag only while 022C2160 is 5 or 6",
            r3["u4"] == 3 and r3["marker"] == 0xD5 and r4["u4"] == 0xFF, "%s %s" % (r3["u4"], r4["u4"]))
    r5 = wrap(511, True, flags=0, free=frozenset())
    R.check("emulated 0030CFB0, bit-30 set, all slots occupied: unit+4 = FF and 022C2158 bit 1 is left SET",
            r5["u4"] == 0xFF and r5["flags"] == 2 and r5["slot"] == [], "u4 %X flags %X" % (r5["u4"], r5["flags"]))
    r6 = wrap(0xFFFF, False)
    R.check("emulated 0030CFB0 with word FFFF: unit+4 = 3 while slot 3's marker still reads FFFF (free)",
            r6["u4"] == 3 and r6["marker"] == 0xFFFF and r6["ident"] == 0x99)


def raw_callers(img, targets):
    name, va, vs, ra, rs = [s for s in img.secs if s[0] == ".text"][0]
    code = img.d[ra:ra + min(vs, rs)]
    base = img.base + va
    out = {t: [] for t in targets}
    for i in range(len(code) - 5):
        op = code[i]
        if op in (0xE8, 0xE9):
            t = base + i + 5 + struct.unpack_from("<i", code, i + 1)[0]
            if t in out:
                out[t].append((base + i, "call" if op == 0xE8 else "jmp"))
        elif op == 0x0F and 0x80 <= code[i + 1] <= 0x8F and i + 6 <= len(code):
            t = base + i + 6 + struct.unpack_from("<i", code, i + 2)[0]
            if t in out:
                out[t].append((base + i, "jcc"))
    return out


def checks(img, R):
    A, W = Body(img, *ALLOC), Body(img, *WRAP)
    for B, (s, e) in ((A, ALLOC), (W, WRAP)):
        ents, ok = img.pdata_cover(s, e)
        R.check("body %08X + 0x%X (%d B) decodes exactly and one .pdata record covers it exactly" % (s, e - s, e - s),
                B.exact and ok and len(ents) == 1)
    R.check("wrapper 185 B = the 166 B retained prefix (0030CFB0 .. + 0xA6) + the 19 B suffix (+ 0xA6 .. + 0xB9)",
            WRAP[1] - WRAP[0] == 185 == 166 + 19 and (WRAP[0] + 166) in W.ins and T(W, WRAP[0] + 166) ==
            "mov byte ptr [rdi + 4], al")
    rets, tails, outs = A.exits()
    R.check("0030D070 local CFG closed: three rets (+0x51 full, +0x5E sign arm, +0xE4 success, the last instruction), "
            "no tail, no call, no indirect jump",
            rets == [0x30D0C1, 0x30D0CE, 0x30D154] and not tails and not outs and A.order[-1] == 0x30D154 and
            not A.calls() and not [a for a in A.order if A[a].mnemonic == "jmp" and A[a].direct_target() is None])
    rets, tails, outs = W.exits()
    R.check("0030CFB0 local CFG closed: one ret, the last instruction; calls only 0020E600 (twice) and 0030D070",
            rets == [W.order[-1]] and not tails and not outs and
            [t for a, t in W.calls()] == [RESOLVE[0], RESOLVE[0], ALLOC[0]])

    # ---- allocator carriers
    R.check("ECX (identity) -> R11D at 0030D070 + 0x5; r11 has no other writer and one reader, the DWORD store +0x20 "
            "(0030D070 + 0xDB)", T(A, 0x30D075) == "mov r11d, ecx" and writers(A, "r11") == [0x30D075] and
            readers(A, "r11") == [0x30D14B] and T(A, 0x30D14B) == "mov dword ptr [rcx + 0x20], r11d")
    rdx_r = [a for a in readers(A, "rdx") if a < 0x30D0F2]
    R.check("DX -> R10D by zero extension at 0030D070 + 0x14, the only read of the incoming RDX (RDX is next written at "
            "+0x82); r10 has one writer and one reader, the final WORD store 0030D070 + 0xDF",
            T(A, 0x30D084) == "movzx r10d, dx" and rdx_r == [0x30D084] and writers(A, "rdx")[0] == 0x30D0F2 and
            writers(A, "r10") == [0x30D084] and readers(A, "r10") == [0x30D14F] and
            T(A, 0x30D14F) == "mov word ptr [rcx + 0x1c], r10w" and A.order[-2] == 0x30D14F,
            " ".join("%X" % x for x in rdx_r))
    cmps = [(a, A[a].text) for a in A.order if A[a].mnemonic in ("cmp", "test")]
    R.check("no compare or test in 0030D070 reads r10, rdx or r11 (no action-range, category or identity test)",
            not [a for a, t in cmps if A[a].reg_reads & {"r10", "rdx", "r11"}], "; ".join("%X %s" % c for c in cmps))
    R.check("slot base: rdi = 022C17B0 (0030D070 + 0x8), written only there and at the three restores; slot i = rdi + "
            "48*i in all three pointer formations (+0x2A/+0x2E, +0x69/+0x6D, +0x82/+0x86)",
            rip_target(A[0x30D078]) == SLOTS and writers(A, "rdi") == [0x30D078, 0x30D0BC, 0x30D0C9, 0x30D12D] and
            [T(A, a) for a in (0x30D09A, 0x30D09E, 0x30D0A2, 0x30D0D9, 0x30D0DD, 0x30D0E1, 0x30D0F2, 0x30D0F6,
                               0x30D0FA)] ==
            ["lea r9, [rax + rax*2]", "shl r9, 4", "add r9, rdi", "lea rcx, [rax + rax*2]", "shl rcx, 4",
             "add rcx, rdi", "lea rdx, [rax + rax*2]", "shl rdx, 4", "add rdx, rdi"])
    R.check("marker: ecx = 0xFFFF (0030D070 + 0xF), no rcx write inside the scan, WORD compare +0x1C (+0x3A), `je` "
            "to the found arm",
            T(A, 0x30D07F) == "mov ecx, 0xffff" and not writers(A, "rcx", 0x30D090, 0x30D0BA) and
            T(A, 0x30D0AA) == "cmp word ptr [r9 + 0x1c], cx" and A[0x30D0AA].mems[0]["size"] == 2 and
            T(A, 0x30D0AF) == "je 0x30d0c2")
    R.check("scan index r8b: 0 (+0x18), `inc r8b` (+0x41), `cmp r8b, 0x20` / `jl` back (+0x44/+0x48); r8 has no "
            "other writer", T(A, 0x30D088) == "xor r8b, r8b" and T(A, 0x30D0B1) == "inc r8b" and
            T(A, 0x30D0B4) == "cmp r8b, 0x20" and T(A, 0x30D0B8) == "jl 0x30d090" and
            writers(A, "r8") == [0x30D088, 0x30D0B1])
    # own finite reading: r8b at the loop head takes 0..31 only; decide each arm
    head_vals, v = [], 0
    while True:
        head_vals.append(v)
        v = (v + 1) & 0xFF
        sv = v - 256 if v > 127 else v
        if not sv < 0x20:
            break
    dead_null = all(not (x > 0x1F) for x in head_vals)       # ja (unsigned) at +0x24
    dead_sign = all(x < 0x80 for x in head_vals)              # jns at +0x55 always taken
    dead_gt = all(not (x > 0x1F) for x in head_vals)          # jg (signed) at +0x63 / +0x7C
    R.check("own reading of r8b: the loop head sees exactly 0..31, so the null-record arm (+0x37), the sign arm "
            "(+0x57) and both > 31 arms (+0x76, +0x7C) are dead for this body",
            head_vals == list(range(32)) and dead_null and dead_sign and dead_gt and
            T(A, 0x30D094) == "ja 0x30d0a7" and T(A, 0x30D0C5) == "jns 0x30d0cf" and T(A, 0x30D0D3) == "jg 0x30d0e6"
            and T(A, 0x30D0EC) == "jg 0x30d12d")
    R.check("the link block always runs on success: `je` at +0x8D tests ZF of `add rdx, rdi`, and 022C17B0 + 48k is "
            "never 0", T(A, 0x30D0FD) == "je 0x30d12d" and all(SLOTS + 48 * k != 0 for k in range(32)))
    mw = [(a, m["base"], m["disp"], m["size"]) for a, m in A.mem_writes()]
    full = A.reach(0x30D0BA)
    R.check("0030D070 memory writes: entry home slot; slot +0/+8 links; head 022BE978 / tail 022BEB88; slot "
            "+0x18/+0x14/+0x10 DWORD 1; +0x20 DWORD; +0x1C WORD - and none on the full-array path",
            mw == [(0x30D070, "rsp", 8, 8), (0x30D106, "rdx", 0, 8), (0x30D112, "rip", 0x1FB185F, 8),
                   (0x30D119, "rdx", 8, 8), (0x30D11F, "rax", 0, 8), (0x30D122, "rdx", 8, 8),
                   (0x30D126, "rip", 0x1FB1A5B, 8), (0x30D136, "rcx", 0x18, 4), (0x30D13D, "rcx", 0x14, 4),
                   (0x30D144, "rcx", 0x10, 4), (0x30D14B, "rcx", 0x20, 4), (0x30D14F, "rcx", 0x1C, 2)] and
            rip_target(A[0x30D112]) == HEAD and rip_target(A[0x30D126]) == TAILP and
            rip_target(A[0x30D0FF]) == TAILP and not [a for a, b, d, s in mw if a in full],
            "; ".join("%X %s+%X/%d" % w for w in mw))
    R.check("success return: EAX = movzx r8b (0030D070 + 0xC2); full return: `mov al, 0xff` (+0x4A)",
            T(A, 0x30D132) == "movzx eax, r8b" and T(A, 0x30D0BA) == "mov al, 0xff")

    # ---- wrapper
    R.check("0030CFB0: `cmp byte ptr [rcx + 4], 0xff` (+0xF) / `jne` to the epilogue (+0x1C -> +0xA9): a set unit+4 "
            "skips the call and the unit+4 store", T(W, 0x30CFBF) == "cmp byte ptr [rcx + 4], 0xff" and
            T(W, 0x30CFCC) == "jne 0x30d059" and 0x30D051 not in W.reach(0x30D059))
    R.check("carriers: ebx = zero-extended R8W (+0x13), esi = EDX (+0x17), rdi = RCX (+0x19); each written only "
            "there and at its restore",
            T(W, 0x30CFC3) == "movzx ebx, r8w" and T(W, 0x30CFC7) == "mov esi, edx" and T(W, 0x30CFC9) == "mov rdi, rcx"
            and writers(W, "rbx") == [0x30CFC3, 0x30D059] and writers(W, "rsi") == [0x30CFC7, 0x30D05E] and
            writers(W, "rdi") == [0x30CFC9, 0x30D067])
    R.check("call: EDX = zero-extended BX (+0x9C), ECX = ESI (+0x9F), `call 0x30d070` (+0xA1), then "
            "`mov byte ptr [rdi + 4], al` (+0xA6)",
            T(W, 0x30D04C) == "movzx edx, bx" and T(W, 0x30D04F) == "mov ecx, esi" and
            W[0x30D051].direct_target() == ALLOC[0] and T(W, 0x30D056) == "mov byte ptr [rdi + 4], al" and
            W.order[W.order.index(0x30D051) + 1] == 0x30D056)
    ww = [(a, m["base"], m["disp"], m["size"]) for a, m in W.mem_writes()]
    R.check("0030CFB0's own writes: two home slots, 022C2158 (DWORD), unit+4 (byte); none at +0x1C and none into "
            "the slot array - the WORD store is the allocator's",
            ww == [(0x30CFB0, "rsp", 8, 8), (0x30CFB5, "rsp", 0x10, 8), (0x30D046, "rip", 0x1FB510C, 4),
                   (0x30D056, "rdi", 4, 1)] and rip_target(W[0x30D046]) == FLAGS,
            "; ".join("%X %s+%X/%d" % w for w in ww))
    R.check("row: rcx = low32(WORD [desc+8] * BX + low32(0020E600([desc+0xC]))), desc = [02EBF138]; a null desc or a "
            "null first resolve sets rcx = 0 and still reads [rcx + 0xC]",
            rip_target(W[0x30CFD2]) == ROWDESC and T(W, 0x30D001) == "movzx edx, word ptr [rcx + 8]" and
            T(W, 0x30D005) == "movzx ecx, bx" and T(W, 0x30D008) == "imul ecx, edx" and T(W, 0x30D00B) ==
            "add ecx, eax" and T(W, 0x30D00F) == "xor ecx, ecx" and
            T(W, 0x30D011) == "test dword ptr [rcx + 0xc], 0x40000000")
    R.check("bit 30 clear -> straight to the call (+0x68 `je` +0x9C); set -> D0..F1 test: `sub ax, cx` with cx = 0xD0, "
            "`cmp ax, 0x21` / `ja` to the flag gate; inside, 022C2160 - 5 <= 1 allocates",
            T(W, 0x30D018) == "je 0x30d04c" and T(W, 0x30D01A) == "mov ecx, 0xd0" and T(W, 0x30D022) == "sub ax, cx"
            and T(W, 0x30D025) == "cmp ax, 0x21" and T(W, 0x30D029) == "ja 0x30d039" and
            rip_target(W[0x30D02B]) == SEQ and T(W, 0x30D031) == "add eax, -5" and T(W, 0x30D037) == "jbe 0x30d04c")
    R.check("flag gate: 022C2158 bit 1 set -> epilogue without the call (+0x91); clear -> set bit 1 (+0x93/+0x96) "
            "then call", rip_target(W[0x30D039]) == FLAGS and T(W, 0x30D03F) == "test al, 2" and
            T(W, 0x30D041) == "jne 0x30d059" and T(W, 0x30D043) == "or eax, 2" and
            not [a for a in W.order if a > 0x30D051 and W[a].mems and W[a].mems[0].get("disp") == 0x1FB510C])
    R.check("candidates 511..534: WORD (w - 0xD0) is 303..326 > 0x21, so they take the flag gate, not the exception",
            [((w - 0xD0) & 0xFFFF) for w in CANDS] == list(range(303, 327)))
    emu_checks(img, R)


def packet_bytes(img, R):
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    mism, got = [], []
    for f in ("retained/slot-action-id-raw-01.json", "source-tail-01.json"):
        for r in json.load(open(os.path.join(ev, f)))["ranges"]:
            s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
            got.append((s_, e_))
            if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"]:
                mism.append(r["start"])
    R.check("packet's retained allocator, wrapper prefix and new suffix range hashes equal this image's bytes "
            "(allocator 0030D070..+0xE5, prefix 0030CFB0..+0xA6, suffix 0030CFB0 + 0xA6..+0xB9)",
            not mism and got == [(0x30D070, 0x30D155), (0x30CFB0, 0x30D056), (0x30D056, 0x30D069)],
            " ".join("%X..%X" % g for g in got))
    rd = open(os.path.join(ev, "README.md"), encoding="utf-8").read()
    R.check("packet keeps open: upstream producers, natural FFFF submission, pool ownership/reuse, whole OV-42",
            "upstream" in rd and "No natural FFFF submission" in rd and "pool ownership/reuse" in rd and
            "whole OV-42" in rd)


def committed_manifest_sha():
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    b = subprocess.run(["git", "show", "%s:Database/FFXII TZA/_experiments/evidence/%s/manifest.json" %
                        (PRODUCER, SLUG)], capture_output=True, cwd=top).stdout
    return hashlib.sha256(b).hexdigest()


CONTROLS = [
    ("0030D070 + 0xF marker 0xFFFF -> 0xFFFE", 0x30D080, bytes.fromhex("feff")),
    ("0030D070 + 0x44 scan bound 0x20 -> 0x1F (31 slots)", 0x30D0B7, bytes([0x1F])),
    ("0030D070 + 0x2E scan stride `shl r9, 4` -> `shl r9, 5` (96 B)", 0x30D0A1, bytes([0x05])),
    ("0030D070 + 0x41 `inc r8b` -> `dec r8b` (scan direction)", 0x30D0B1, bytes.fromhex("41fec8")),
    ("0030D070 + 0xDF WORD store r10w -> r11w (identity stored as the action)", 0x30D14F, bytes.fromhex("664489591c")),
    ("0030D070 + 0xDB identity store r11d -> r10d", 0x30D14B, bytes.fromhex("44895120")),
    ("0030D070 + 0x14 `movzx r10d, dx` -> `movzx r10d, cx` (marker copied instead of the word)", 0x30D084,
     bytes.fromhex("440fb7d1")),
    ("0030D070 + 0x4C full-arm restore -> `mov [rcx], rdi` + 2 nops (a non-frame write on the full path)", 0x30D0BC,
     bytes.fromhex("4889399090")),
    ("0030CFB0 + 0x9C `movzx edx, bx` -> `movzx edx, si` (identity forwarded as the word)", 0x30D04C,
     bytes.fromhex("0fb7d6")),
    ("0030CFB0 + 0xA6 unit+4 -> unit+5", 0x30D058, bytes([0x05])),
    ("0030CFB0 + 0x13 `movzx ebx, r8w` -> `nop; movzx ebx, dx`", 0x30CFC3, bytes.fromhex("900fb7da")),
    ("0030CFB0 + 0xA6 `mov byte [rdi+4], al` -> `mov dword [rdi+0x1c], eax` (the wrapper writing a +0x1C word, the "
     "attribution being corrected)", 0x30D056, bytes.fromhex("89471c")),
    ("0030CFB0 + 0x8F flag test bit 1 -> bit 2", 0x30D040, bytes([0x04])),
]


def main():
    img = Img.load()
    R = Rep("rv_slots")
    print("== packet integrity")
    csha = committed_manifest_sha()
    check_manifest(R, SLUG, csha)
    R.note("committed manifest at %s: sha256 %s" % (PRODUCER, csha))
    packet_bytes(img, R)
    print("== raw direct-reference census (E8/E9 rel32 and 0F 8x jcc, .text)")
    rc = raw_callers(img, [ALLOC[0], WRAP[0]])
    R.check("0030D070 has one raw direct reference: the call at 0030CFB0 + 0xA1", rc[ALLOC[0]] == [(0x30D051, "call")],
            " ".join("%X %s" % x for x in rc[ALLOC[0]]))
    R.note("0030CFB0 raw direct references: %s (indirect callers not covered)" %
           ", ".join("%X %s" % x for x in rc[WRAP[0]]))
    print("== shipping-image re-derivation")
    checks(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null")
    Rn.quiet = True
    checks(img.patched(0x30D080, img.read(0x30D080, 2)), Rn)
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
            why = "%d failed: %s" % (failed, "; ".join(f[:70] for f in Rc.failed[:3]))
        except Exception as e:
            failed = 1
            why = "refused: %r after %d failed: %s" % (e, Rc.fails, "; ".join(f[:70] for f in Rc.failed[:3]))
        nctl += 1
        R.check("control: " + label, failed > 0, why)
    disk = hashlib.sha256(open(find_exe(), "rb").read()).hexdigest()
    R.check("exe on disk still hashes to the pinned sha256 after all controls", disk == SHA_PIN, disk)
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))


if __name__ == "__main__":
    main()
