"""check_s31.py - FABLE, 2026-10-03: the S-31 licence board's grid and the writers of licenceOwnedBits (+0x194).

Settles, against the certified image (sha256 73461d08..., base 00120000), the claims of section.txt
("## 8a. The board grid and the writers of the owned bits"), which CONTRACT-license-check.md is to receive.

  python check_s31.py            run everything; prints PASS/FAIL lines and FAILS N last

Parts
  S  static: bytes at the cited sites, raw reference indexes (E8/E9, 0F 8x, EB/7x, rip, [reg+RVA], .rdata/.data
     pointers) of the writer and loader entries, and a route-filtered displacement census of every write into the
     46-byte bitmap (record-relative 0x194..0x1C1, block-relative 0x19C..0x1C9, all widths, base+index forms).
  X  executed under Unicorn (shipped bytes, no live game): the shipped battle_pack.bin (us) is relocated and its node
     table bound by the shipped 003846F0 / 003845F0, exactly as 00236C30 does; the shipped board_1.bin (in) is
     planted in board slot 0 (02EBF1A0).  The setter 00323910, the purchase gate 00323D10, the licence check's
     00323BB0 and the reset's 00328990 then run REAL.  Stubs, each disclosed per case: 0030FED0 (the recompute,
     a side-effect sink) everywhere; 00323D10 / 00308FF0 / 0030A310 only in the two rank-byte cases; 0030B0E0 in
     the reset cases (it only sets bit 0 of the query buffer's +0x24, which 00328990 never reads).
  C  sensitivity controls: the same executed cases on MUTATED images must FAIL (bts->btr at 00323A04; cmp eax,0xc ->
     cmp eax,0xb at 00323B15; the reset's keep test 00328A68 jne -> nops), and a mutated census expectation must FAIL.
"""
import hashlib
import io
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, data_refs, disp_sweep, decode_fn, X86_OP_MEM, X86_REG_RIP  # noqa: E402
from capstone import CS_AC_WRITE  # noqa: E402
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,  # noqa: E402
                               UC_X86_REG_RIP, UC_X86_REG_RAX)
import unicorn  # noqa: E402

DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.abspath(os.path.join(DB, "..", ".."))
EXTRACT = r"D:\FFXII_TZA_extract\ps2data\image\ff12\test_battle"
PACK = os.path.join(EXTRACT, "us", "binaryfile", "battle_pack.bin")
PACK_SHA = "d1bb89aac759cfcd4eb181715d9e88afb78d62a9a3fcffa6242f365f182cbc98"   # = OPUS's s31 shipped replay
BOARD1 = os.path.join(EXTRACT, "in", "binaryfile", "board_1.bin")
BOARD1_SHA = "5a220b2d8e3cc2c78042cd5bd5161407f7f4dbadb811b7c1380b573e39fb380d"

SETTER, GATE, PREREQ, RESET_BOARD, RESET_JOBS = 0x323910, 0x323D10, 0x323BB0, 0x328990, 0x328BD0
RELOCATE, SLOTBIND, RECOMPUTE, GRADE, ROWID, QMODE0, POPCNT = 0x3846F0, 0x3845F0, 0x30FED0, 0x308FF0, 0x30A310, 0x30B0E0, 0x324020
NODES, BLOBCELL, BOARDS, BLOCK = 0x2EBF038, 0x208E680, 0x2EBF1A0, 0x2EBF190

FAILS = [0]
QUIET = [False]


def check(tag, ok, text):
    if not ok:
        FAILS[0] += 1
    if not QUIET[0]:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))
    return ok


def note(s):
    if not QUIET[0]:
        print("      " + s)


# ----------------------------------------------------------------------------------------------------------------
# the emulator
# ----------------------------------------------------------------------------------------------------------------
STACK, STACK_SZ, RET, TRAP, HEAP = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x10000000
B, REC, BOARD = 0x10000000, 0x10800000, 0x10900000


class Emu(object):
    def __init__(self, img):
        self.img = img
        uc = self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        d = img.d
        uc.mem_map(img.base, 0x1000)
        uc.mem_write(img.base, d[:0x400])
        for name, va, vs, ra, rs in img.secs:
            size = (max(vs, rs) + 0xFFF) & ~0xFFF
            uc.mem_map(img.base + va, size)
            uc.mem_write(img.base + va, d[ra:ra + min(rs, max(vs, rs))])
        uc.mem_map(STACK, STACK_SZ)
        uc.mem_map(RET, 0x1000)
        uc.mem_write(RET, b"\xF4")
        uc.mem_map(TRAP, 0x10000)
        uc.mem_write(TRAP, b"\xC3" * 0x10000)
        uc.mem_map(HEAP, 0x1000000)
        # IAT: every slot -> a trap; memset / memcpy / memmove are serviced by name, anything else stops the run
        self.imports = {}
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        opt = pe + 24
        irva, isz = struct.unpack_from("<II", d, opt + 112 + 8)
        k = 0
        o = img.off(img.base + irva)
        while True:
            oft, ts, fc, nm, ft = struct.unpack_from("<IIIII", d, o)
            if ft == 0:
                break
            t = ft
            while True:
                v = img.u64(img.base + t)
                if v == 0:
                    break
                name = "ordinal" if v >> 63 else img.read(img.base + v + 2, 64).split(b"\0")[0].decode("ascii", "replace")
                addr = TRAP + 16 * k
                self.imports[addr] = name
                uc.mem_write(img.base + t, struct.pack("<Q", addr))
                k += 1
                t += 8
            o += 20
        self.stubs = {}
        self.calls = {}
        self.bad = []
        uc.hook_add(UC_HOOK_CODE, self._code)
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self._unmapped)

    def _code(self, uc, a, n, _):
        if a in self.stubs:
            self.calls[a] = self.calls.get(a, 0) + 1
            v = self.stubs[a]
            uc.reg_write(UC_X86_REG_RAX, v(uc) if callable(v) else v)
            sp = uc.reg_read(UC_X86_REG_RSP)
            ra = struct.unpack("<Q", bytes(uc.mem_read(sp, 8)))[0]
            uc.reg_write(UC_X86_REG_RSP, sp + 8)
            uc.reg_write(UC_X86_REG_RIP, ra)
            return
        if a in self.imports:
            name = self.imports[a]
            self.calls[name] = self.calls.get(name, 0) + 1
            rcx, rdx, r8 = (uc.reg_read(r) for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8))
            if name == "memset":
                uc.mem_write(rcx, bytes([rdx & 0xFF]) * r8)
                uc.reg_write(UC_X86_REG_RAX, rcx)
            elif name in ("memcpy", "memmove"):
                uc.mem_write(rcx, bytes(uc.mem_read(rdx, r8)))
                uc.reg_write(UC_X86_REG_RAX, rcx)
            else:
                self.bad.append("import " + name)
                uc.emu_stop()

    def _unmapped(self, uc, access, a, size, value, _):
        self.bad.append("unmapped %s %X at rip %X" % (access, a, uc.reg_read(UC_X86_REG_RIP)))
        return False

    def call(self, fn, rcx=0, rdx=0, r8=0, r9=0):
        uc = self.uc
        sp = STACK + STACK_SZ - 0x1008
        uc.mem_write(sp, struct.pack("<Q", RET))
        uc.reg_write(UC_X86_REG_RSP, sp)
        for r, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9)):
            uc.reg_write(r, v & 0xFFFFFFFFFFFFFFFF)
        self.bad = []
        try:
            uc.emu_start(fn, RET, count=5000000)
        except UcError as e:
            self.bad.append("UcError %s at %X" % (e, uc.reg_read(UC_X86_REG_RIP)))
        ok = uc.reg_read(UC_X86_REG_RIP) == RET and not self.bad
        if not ok:
            raise RuntimeError("run %X stopped: %s" % (fn, self.bad[:3] or "rip %X" % uc.reg_read(UC_X86_REG_RIP)))
        return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF

    def w(self, a, fmt, *v):
        self.uc.mem_write(a, struct.pack(fmt, *v))

    def r(self, a, fmt):
        return struct.unpack(fmt, bytes(self.uc.mem_read(a, struct.calcsize(fmt))))


def build(img):
    """Relocate the shipped battle_pack.bin and bind the node table, as 00236C30 does (00236D5C-00236D67)."""
    E = Emu(img)
    pack = open(PACK, "rb").read()
    E.uc.mem_write(B, pack)
    E.stubs[RECOMPUTE] = 0
    E.call(RELOCATE, BLOBCELL, B, 0)
    E.call(SLOTBIND, NODES, E.r(B + 0x34, "<I")[0])
    board = open(BOARD1, "rb").read()
    E.uc.mem_write(BOARD, board)
    E.w(BOARDS, "<Q", BOARD)
    return E


def node_table(E):
    h = E.r(NODES, "<Q")[0]
    _, n, stride, _, enc = E.r(h, "<IIHHI")
    return h, n, stride, enc


def row(E, i):
    h, n, stride, enc = node_table(E)
    a = (enc + stride * i) & 0xFFFFFFFF
    return a, bytes(E.uc.mem_read(a, stride))


def new_rec(E, slot=0, kind=0, lp=0, owned=()):
    E.uc.mem_write(REC, bytes(0x1C8))
    E.w(REC + 4, "<BB", slot, kind)
    E.w(REC + 0x190, "<I", lp)
    for b in owned:
        v = E.r(REC + 0x194 + b // 8, "<B")[0]
        E.w(REC + 0x194 + b // 8, "<B", v | (1 << (b % 8)))


def bits(E):
    return bytes(E.uc.mem_read(REC + 0x194, 46))


def lp(E):
    return E.r(REC + 0x190, "<I")[0]


def mask_of(nodes):
    m = bytearray(46)
    for b in nodes:
        m[b // 8] |= 1 << (b % 8)
    return bytes(m)


# ----------------------------------------------------------------------------------------------------------------
# executed cases (each returns True when every assertion inside it held; prints PASS/FAIL lines)
# ----------------------------------------------------------------------------------------------------------------
def x_bind(E, pack):
    h, n, stride, enc = node_table(E)
    ok = check("X1", n == 361 and stride == 24 and h == B + 0x8E48,
               "shipped 003846F0 + 003845F0 bind the node table: %d x %d at blob+%X (00236D5C-00236D67's call)"
               % (n, stride, h - B))
    cell = E.r(BLOBCELL, "<I")[0]
    ok &= check("X1b", cell == B, "0208E680 holds the encoded handle of the battle_pack.bin blob after 003846F0 "
                "(00384709 `mov [rdi], eax`, eax = 0020E620(blob) = blob - [01F83530]; got %X, blob %X)" % (cell, B))
    a, rb = row(E, 360)
    ok &= check("X1c", pack[a - B:a - B + 24] == rb and rb[5] == 0x1E,
                "node 360's row is the file's own bytes (offset %X) and its category +5 is 0x1E" % (a - B))
    return ok


def pick_ordinary(E, lo=31):
    """Nodes > 30 whose row has kind +6 == 0 and category +5 != 0x1E: the gate 00323D10 returns 0 for them."""
    out = []
    h, n, stride, enc = node_table(E)
    for i in range(lo, n):
        a, rb = row(E, i)
        if rb[6] == 0 and rb[5] != 0x1E:
            out.append(i)
    return out


def x_setter(E):
    ok = True
    ords = pick_ordinary(E)
    N = ords[0]
    a, rb = row(E, N)
    cost = rb[4]
    # silent grant (flags bit 0 set): the bit, no LP change
    new_rec(E, slot=0, lp=100)
    r = E.call(SETTER, REC, N, 1, 1)
    ok &= check("X2", r == 0 and bits(E) == mask_of([N]) and lp(E) == 100,
                "00323910(rec, %d, set=1, flags=1) returns 0, sets only byte %d bit %d (got %s), LP 100 -> %d"
                % (N, N >> 3, N & 7, bits(E)[N >> 3:N // 8 + 1].hex(), lp(E)))
    # the gate reads what the setter wrote
    g = E.call(GATE, REC, N, 0)
    ok &= check("X2b", g == 1, "00323D10 on the same node now returns reason 1 (owned; read at 00323D85): %d" % g)
    # duplicate grant: refused by the gate, nothing changes
    before = bits(E), lp(E)
    r = E.call(SETTER, REC, N, 1, 0)
    ok &= check("X3", r == 0xFFFFFFFF and (bits(E), lp(E)) == before,
                "a second grant returns -1 (00323972-00323979) with no write and no LP change")
    # charged grant: LP -= row +4
    new_rec(E, slot=0, lp=100)
    r = E.call(SETTER, REC, N, 1, 0)
    ok &= check("X4", r == 0 and lp(E) == max(0, 100 - cost) and bits(E) == mask_of([N]),
                "charged grant: LP 100 - row.b[+4] (%d) = %d (003239C3-003239E1), bit set" % (cost, lp(E)))
    # insufficient LP still grants, floored at 0
    dear = [i for i in ords if row(E, i)[1][4] > 0][0]
    new_rec(E, slot=0, lp=0)
    r = E.call(SETTER, REC, dear, 1, 0)
    ok &= check("X5", r == 0 and lp(E) == 0 and bits(E) == mask_of([dear]),
                "with LP 0 and cost %d the grant still lands and LP floors at 0 (`jns` 003239D1 / `mov edx, ebx`)"
                % row(E, dear)[1][4])
    # cap: 99,999
    new_rec(E, slot=0, lp=0xFFFFFFF0)
    E.call(SETTER, REC, ords[1], 1, 1)
    # rejects: node out of range, kind byte non-zero, null record
    new_rec(E, slot=0, lp=7)
    r1 = E.call(SETTER, REC, 361, 1, 1)
    new_rec(E, slot=0, kind=1, lp=7)
    r2 = E.call(SETTER, REC, N, 1, 1)
    r3 = E.call(SETTER, 0, N, 1, 1)
    new_rec(E, slot=0, lp=7)
    ok &= check("X6", (r1, r2, r3) == (0xFFFFFFFF,) * 3 and bits(E) == bytes(46) and lp(E) == 7,
                "node 361 (class-0x19 validator, 0032394C), kind byte +5 = 1 (0032393D) and a null record "
                "(00323930) each return -1 and write nothing")
    # revoke arm (no caller passes set = 0, S3): clears the bit, no gate, no refund
    new_rec(E, slot=0, lp=5, owned=[N])
    r = E.call(SETTER, REC, N, 0, 0)
    ok &= check("X7", r == 0 and bits(E) == bytes(46) and lp(E) == 5,
                "set = 0 clears the bit with `btr` (00323A26), skips 00323D10 (`je 00323A09` at 0032395F) and "
                "refunds nothing")
    return ok


def x_cross(E):
    """The licence check reads, at 00323C18, exactly the bit the purchase setter writes at 00323A29."""
    ok = True
    found = None
    for N in pick_ordinary(E):
        a, rb = row(E, N)
        ids = [struct.unpack_from("<H", rb, 8 + 2 * k)[0] for k in range(8)]
        for aid in ids:
            if aid in (0, 0xFFFF):
                continue
            new_rec(E, slot=0)
            if E.call(PREREQ, REC, 1, aid) == 0:
                new_rec(E, slot=0, owned=[N])
                if E.call(PREREQ, REC, 1, aid) == 1:
                    found = (N, aid)
                    break
        if found:
            break
    if not found:
        return check("X8", False, "no ordinary node lists an id the kind-1 check licenses")
    N, aid = found
    new_rec(E, slot=0, lp=500)
    before = E.call(PREREQ, REC, 1, aid)
    E.call(SETTER, REC, N, 1, 0)
    after = E.call(PREREQ, REC, 1, aid)
    ok &= check("X8", (before, after) == (0, 1),
                "action %#x: 00323BB0(rec, 1, id) is 0 before and 1 after the PURCHASE SETTER grants node %d - the "
                "check's byte-wise read `[rbx+rdx+0x194]` (00323C18) and the setter's `bts` byte (00323A29) agree" % (aid, N))
    return ok


def x_rank(E):
    """The rank byte +0x20: Quickening nodes 0..17 raise it to min(count, 3); nodes 18..30 INCLUSIVE take 00308FF0."""
    ok = True
    E.stubs[GATE] = 0
    E.stubs[ROWID] = 0          # id 0 is outside 0xD0..0xE1, so 00300B80 is skipped (00323ABF)
    E.stubs[GRADE] = 2
    new_rec(E, slot=0)
    seen = []
    for q in range(4):
        E.call(SETTER, REC, q, 1, 1)
        seen.append(E.r(REC + 0x20, "<B")[0])
    ok &= check("X9", seen == [1, 2, 3, 3],
                "granting Quickening nodes 0,1,2,3 leaves +0x20 at %s: max(cur, min(popcount 0..17, 3)) - esi keeps "
                "00324020's count (00323A69) into 00323B64 (stubs: 00323D10 -> 0, 0030A310 -> 0)" % seen)
    res = {}
    for node in (17, 18, 30, 31):
        new_rec(E, slot=0)
        E.call(SETTER, REC, node, 1, 1)
        res[node] = E.r(REC + 0x20, "<B")[0]
    ok &= check("X10", res == {17: 1, 18: 2, 30: 2, 31: 0},
                "+0x20 after one grant: %s - node 30 (0x1E) IS in the 00308FF0 arm (`lea eax,[rbp-0x12]` / `cmp eax,0xc` / "
                "`ja`, 00323B12-00323B18), node 31 is not (stub 00308FF0 -> 2)" % res)
    for k in (GATE, ROWID, GRADE):
        del E.stubs[k]
    return ok


def x_reset(E):
    """00328990(rec, slot, board): un-learn the board's owned squares the slot does not start with, refund their cost."""
    ok = True
    E.stubs[QMODE0] = 0
    blob = open(BOARD1, "rb").read()
    w, h = struct.unpack_from("<HH", blob, 4)
    cells = [struct.unpack_from("<H", blob, 8 + 2 * i)[0] for i in range(w * h)]
    on = sorted(set(c for c in cells if c != 0xFFFF))
    slot = None
    for s in range(6):
        keep = [c for c in on if row(E, c)[1][7] & (1 << s)]
        drop = [c for c in on if not (row(E, c)[1][7] & (1 << s)) and row(E, c)[1][4] > 0]
        if keep and drop:
            slot = s
            break
    if slot is None:
        return check("X11", False, "board_1 has no square that slot 0..5 starts with")
    off = [i for i in range(361) if i not in on][-1]
    K, D = keep[0], drop[0]
    cost = row(E, D)[1][4]
    new_rec(E, slot=slot, lp=10, owned=[K, D, off])
    r = E.call(RESET_BOARD, REC, slot, 0)
    ok &= check("X11", r == 0 and bits(E) == mask_of([K, off]) and lp(E) == 10 + cost,
                "board_1 (%dx%d, %d squares), slot %d: owned {%d start-owned, %d, %d off-board} -> {%d, %d}; LP 10 -> %d "
                "(+%d = row.b[+4] via query +0x20, 00328A7E); the start mask is row.b[+7] via query +0x36 (0031E0E9) "
                "tested at 00328A5B-00328A68 (stub 0030B0E0 -> 0)"
                % (w, h, len(on), slot, K, D, off, K, off, lp(E), cost))
    # every owned square of the board, LP refund = sum of costs of the dropped ones, capped at 99,999
    new_rec(E, slot=slot, lp=99990, owned=on)
    E.call(RESET_BOARD, REC, slot, 0)
    kept = [c for c in on if row(E, c)[1][7] & (1 << slot)]
    refund = sum(row(E, c)[1][4] for c in on if c not in kept)
    ok &= check("X12", bits(E) == mask_of(kept) and lp(E) == min(99999, 99990 + refund),
                "all %d squares owned: %d start-owned kept, refund %d, LP 99990 -> %d (cap 0x1869F, 00328AE6-00328AEF)"
                % (len(on), len(kept), refund, lp(E)))
    # board index: > 11 and the 0xFF selector (movsx -> -1) are refused before any read
    new_rec(E, slot=slot, lp=3, owned=[D])
    r12 = E.call(RESET_BOARD, REC, slot, 12)
    rm1 = E.call(RESET_BOARD, REC, slot, 0xFFFFFFFF)
    ok &= check("X13", (r12, rm1) == (0xFFFFFFFF,) * 2 and bits(E) == mask_of([D]) and lp(E) == 3,
                "board 12 and board -1 (the unset selector 0xFF, sign-extended at 00328C16) return -1 at 003289A4 "
                "(`cmp r8d, 0xb` / `ja`, unsigned) and change nothing")
    # the magic is never read
    bad = b"XXXX" + blob[4:]
    E.uc.mem_write(BOARD, bad)
    new_rec(E, slot=slot, lp=10, owned=[K, D, off])
    E.call(RESET_BOARD, REC, slot, 0)
    ok &= check("X14", bits(E) == mask_of([K, off]) and lp(E) == 10 + cost,
                "with the magic 'licd' overwritten the reset does exactly the same (no reader of +0x00)")
    # height 0: nothing is read, LP rewritten unchanged
    E.uc.mem_write(BOARD, blob[:6] + b"\0\0" + blob[8:])
    new_rec(E, slot=slot, lp=10, owned=[K, D])
    E.call(RESET_BOARD, REC, slot, 0)
    ok &= check("X15", bits(E) == mask_of([K, D]) and lp(E) == 10,
                "height 0: the row loop never runs (003289D3 `cmp dx, [r8+6]` / `jae`), nothing is un-learned")
    E.uc.mem_write(BOARD, blob)
    del E.stubs[QMODE0]
    return ok


def run_executed(img, pack, which=("bind", "setter", "cross", "rank", "reset")):
    E = build(img)
    ok = True
    if "bind" in which:
        ok &= x_bind(E, pack)
    if "setter" in which:
        ok &= x_setter(E)
    if "cross" in which:
        ok &= x_cross(E)
    if "rank" in which:
        ok &= x_rank(E)
    if "reset" in which:
        ok &= x_reset(E)
    note("calls serviced: %s" % dict((("%08X" % k) if isinstance(k, int) else k, v) for k, v in sorted(E.calls.items(), key=str)))
    return ok


# ----------------------------------------------------------------------------------------------------------------
# static part
# ----------------------------------------------------------------------------------------------------------------
def text_at(img, a):
    pd, ins = decode_fn(img, a)
    if ins is None:
        ci = next(img.cs.disasm(img.read(a, 16), a))
    else:
        ci = ins.get(a)
    return (ci.mnemonic + " " + ci.op_str).strip() if ci else "<no boundary>"


SITES = [
    (0x323930, "test rcx, rcx"), (0x32393D, "cmp byte ptr [rcx + 5], 0"), (0x323943, "mov ecx, 0x19"),
    (0x32395C, "test r14d, r14d"), (0x32396D, "call 0x323d10"), (0x32397E, "not esi"), (0x323980, "test sil, 1"),
    (0x3239C3, "movzx ecx, byte ptr [rcx + 4]"), (0x3239D1, "jns 0x3239d7"), (0x3239D7, "mov eax, 0x1869f"),
    (0x3239E1, "mov dword ptr [rdi + 0x190], edx"),
    (0x3239FC, "movzx ecx, byte ptr [rdx + rdi + 0x194]"), (0x323A04, "bts ecx, eax"),
    (0x323A26, "btr ecx, eax"), (0x323A29, "mov byte ptr [rdx + rdi + 0x194], cl"),
    (0x323A30, "cmp ebp, 0xe5"), (0x323A3B, "call 0x31b860"), (0x323A48, "call 0x324470"),
    (0x323A4D, "test r14d, r14d"), (0x323A58, "cmp ebp, 0x11"), (0x323A64, "call 0x324020"),
    (0x323AAF, "call 0x30a310"), (0x323B0D, "call 0x300b80"),
    (0x323B12, "lea eax, [rbp - 0x12]"), (0x323B15, "cmp eax, 0xc"), (0x323B18, "ja 0x323b64"),
    (0x323B5D, "call 0x308ff0"), (0x323B7C, "mov byte ptr [rdi + 0x20], bl"), (0x323B87, "call 0x30fed0"),
    # the check's read of the same byte
    (0x323C18, "movzx ecx, byte ptr [rbx + rdx + 0x194]"), (0x323C20, "test byte ptr [rdx], cl"),
    # the menu grant wrapper and its one caller
    (0x3235C0, "cmp cl, 0x27"), (0x3235CA, "xor r9d, r9d"), (0x3235D5, "xor r9d, r9d"),
    (0x55DA60, "mov r8d, 1"), (0x55DA6E, "call 0x3235c0"),
    # the two start-licence grants: set = 1, flags = 1, row.b[+7] bit slot
    (0x23AE68, "test byte ptr [r8 + 7], dl"), (0x23AE6E, "mov r9d, 1"), (0x23AE76, "mov r8d, r9d"),
    (0x23AE7C, "call 0x323910"), (0x23AE10, "cmp esi, 6"), (0x23ACBD, "call 0x861ec0"), (0x23ACA4, "mov r8d, 0x1c8"),
    (0x239D41, "test byte ptr [r8 + 7], dl"), (0x239D47, "mov r9d, 1"), (0x239D4F, "mov r8d, r9d"),
    (0x239D55, "call 0x323910"), (0x239C4F, "cmp word ptr [rbp + 0x20], r13w"), (0x239C5D, "call 0x16d6a0"),
    (0x16D6A0, "ret 0"),
    (0x239C0D, "mov qword ptr [rbx + 0x194], rax"), (0x239C39, "mov word ptr [rbx + 0x1c0], ax"),
    # the block clear
    (0x2370CD, "mov r8d, 0x7410"), (0x2370D3, "call 0x861ec0"),
    # resetJobs -> 00328BD0 -> 00328990 x2
    (0x342242, "jmp 0x328bd0"), (0x328BD9, "cmp ebx, 5"), (0x328C16, "movsx r8d, byte ptr [rdi + 0x1c3]"),
    (0x328C23, "call 0x328990"), (0x328C28, "movsx r8d, byte ptr [rdi + 0x1c4]"), (0x328C35, "call 0x328990"),
    (0x328D52, "mov word ptr [rdi + 0x1c3], 0xffff"), (0x328D5D, "mov byte ptr [rdi + 0x1c5], 0xff"),
    (0x3289A4, "cmp r8d, 0xb"), (0x3289B2, "lea rcx, [rip + 0x2b967e7]"), (0x3289D3, "cmp dx, word ptr [r8 + 6]"),
    (0x328A14, "movzx esi, word ptr [r8 + rcx*2 + 8]"), (0x328A1C, "mov esi, 0xffff"),
    (0x328A2D, "mov dword ptr [rsp + 0x20], 0x20"), (0x328A35, "call 0x31c5d0"),
    (0x328A51, "test byte ptr [rdx + r14 + 0x194], al"), (0x328A5B, "movzx eax, byte ptr [rsp + 0x56]"),
    (0x328A68, "jne 0x328a86"), (0x328A73, "btr eax, edi"), (0x328A76, "mov byte ptr [rdx + r14 + 0x194], al"),
    (0x328A7E, "movzx eax, byte ptr [rsp + 0x40]"), (0x328AF2, "mov dword ptr [r14 + 0x190], edx"),
    (0x31E093, "movzx eax, byte ptr [rdi + 4]"), (0x31E097, "mov byte ptr [rbx + 0x20], al"),
    (0x31E0E9, "movzx eax, byte ptr [rdi + 7]"), (0x31E0ED, "mov byte ptr [rbx + 0x36], al"),
    # the board loader
    (0x2369E5, "lea rdi, [rip + 0x2c887b4]"), (0x236A01, "rep stosq qword ptr [rdi], rax"),
    (0x236A1A, "call 0x238260"), (0x236A21, "cmp ebx, 0xc"), (0x22A41A, "call 0x2368d0"),
    (0x238304, "cmp cl, 0xb"), (0x238324, "test rax, rax"), (0x238329, "call 0x233e00"),
    (0x23836A, "add ecx, 0x47"), (0x23837D, "call 0x384420"),
    (0x238399, "mov rcx, qword ptr [rip + 0x2c86e00]"), (0x2383A5, "call 0x3844f0"),
    (0x2383AA, "mov qword ptr [rip + 0x2c86def], rbx"),
    (0x233E8D, "cmp r9d, 6"), (0x233E91, "setl r10b"),
    (0x237632, "cmp cl, 0xb"), (0x237642, "cmp qword ptr [rdx + rcx*8], rax"),
    (0x55C0A8, "mov rdx, qword ptr [rdx + rax*8 + 0x2d9f1a0]"),
    # the builder's bit order, the blob-handle store, the setter's bit index, the cell bounds, the null-row reads
    (0x2F907D, "movzx ecx, byte ptr [rdx + r15]"), (0x2F9082, "bts ecx, eax"),
    (0x384704, "call 0x20e620"), (0x384709, "mov dword ptr [rdi], eax"),
    (0x3239E7, "mov eax, ebp"), (0x3239F4, "sar ecx, 3"), (0x3239C0, "mov rcx, rbx"),
    (0x31E090, "mov rdi, rsi"), (0x328A01, "jge 0x328a1c"), (0x328A0A, "jge 0x328a1c"),
    (0x323A09, "mov eax, ebp"), (0x32395F, "je 0x323a09"),
    (0x22A0B0, "push rbx"), (0x236A17, "movzx ecx, bl"), (0x236A24, "jl 0x236a17"), (0x3235C5, "xor ecx, ecx"),
    (0x3235D8, "imul rcx, rax, 0x1c8"), (0x3235ED, "add rcx, rax"), (0x328AC2, "mov ecx, dword ptr [r14 + 0x190]"),
]


def static_part(img):
    bad = [(a, t, text_at(img, a)) for a, t in SITES if text_at(img, a) != t]
    check("S1", not bad, "%d cited instructions decode as quoted%s" % (len(SITES), "" if not bad else
                                                                         ": " + "; ".join("%08X want `%s` got `%s`" % x for x in bad[:5])))

    def refset(va):
        refs, unc = text_refs(img, va)
        return sorted(r["site"] for r in refs), unc

    exp = {
        SETTER: [0x239D55, 0x23AE7C, 0x3235CD, 0x3235F0],
        0x3235C0: [0x55DA6E],
        RESET_BOARD: [0x328C23, 0x328C35],
        RESET_JOBS: [0x342242],
        0x342230: [],
        0x238260: [0x236A1A],
        0x233E00: [0x238329],
        0x2368D0: [0x22A41A],
        0x237630: [0x558BE3],
        0x23AC80: [0x237E26, 0x239AC4, 0x23A7A9],
        0x239960: [0x234349],
        0x2370C0: [0x2399E9, 0x23AF56],
    }
    for k, (va, want) in enumerate(sorted(exp.items())):
        got, unc = refset(va)
        check("S2.%d" % k, got == sorted(want) and not unc,
              "raw .text references to %08X: %s" % (va, ["%08X" % g for g in got] or "none"))
    dr = data_refs(img, 0x342230)
    check("S2.v", [(s, "%08X" % a, f) for s, a, f, v in dr] == [(".data", "01EF91E0", "va64"), (".data", "01EF91E0", "u32")],
          "00342230's only pointer is the native-table slot 01EF91E0 (verb 0x05D6 resetJobs, "
          "01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-dispatch.tsv)")
    # .rdata u32 hits on 00323910 are its chained-unwind records (the parent RUNTIME_FUNCTION copy)
    ur = [(a, img.u32(a + 4)) for s, a, f, v in data_refs(img, SETTER) if f == "u32"]
    check("S2.u", ur and all(e == 0x203955 for a, e in ur),
          "00323910's .rdata u32 hits %s are CHAININFO copies of its primary entry (next dword = end RVA 0x203955)"
          % ["%08X" % a for a, e in ur])
    import census_s31 as CS

    def fn_of(a):
        rt = CS.root_of(img, a)
        if rt:
            return rt
        p = a
        while img.read(p - 1, 1)[0] != 0xCC:
            p -= 1
        return p

    refs, _ = text_refs(img, BOARDS, BOARDS + 0x60)
    by = {}
    for r in refs:
        by.setdefault(fn_of(r["site"]), []).append(r["site"])
    setters = dict((0x238390 + 0x30 * k, 2) for k in range(12))
    others = {0x233E00: 2, 0x2368D0: 1, 0x237630: 1, 0x238260: 1, RESET_BOARD: 1, 0x3FC900: 1, 0x55B3F0: 1,
              0x55BFF0: 1, 0x55E2C0: 1, 0x55E600: 1, 0x55F830: 2, 0x560070: 1, 0x560610: 1}
    want_by = dict(setters)
    want_by.update(others)
    got_by = dict((f, len(v)) for f, v in by.items())
    check("S3", got_by == want_by,
          "raw references into the board array 02EBF1A0..02EBF1FF: %d sites in %d functions = 12 generated setters "
          "00238390 + 0x30k (a load and a store each) + clear 002368D0, request 00238260, gate 00233E00, predicate "
          "00237630 and 9 readers %s" % (sum(got_by.values()), len(got_by),
                                         ["%08X" % f for f in sorted(others) if f not in (0x233E00, 0x2368D0, 0x237630, 0x238260)]))
    if got_by != want_by:
        note("got %s" % dict(("%08X" % k, v) for k, v in sorted(got_by.items())))

    return census_part(img)


def census_part(img):
    import census_s31 as CS

    def fn_of(a):
        rt = CS.root_of(img, a)
        if rt:
            return rt
        p = a
        while img.read(p - 1, 1)[0] != 0xCC:
            p -= 1
        return p

    # --- the bitmap writer census -------------------------------------------------------------------------------
    rows, route = CS.census(img)
    ws = rows["route"]
    DISP = {
        "00239C0D": "BITMAP: 00239960 zeroes bytes 0..7 (SetSaveData preset apply, before the start grants)",
        "00239C17": "BITMAP: 00239960, bytes 8..15", "00239C1E": "BITMAP: 00239960, bytes 16..23",
        "00239C25": "BITMAP: 00239960, bytes 24..31", "00239C2C": "BITMAP: 00239960, bytes 32..39",
        "00239C33": "BITMAP: 00239960, bytes 40..43", "00239C39": "BITMAP: 00239960, bytes 44..45",
        "00323A29": "BITMAP: 00323910 sets / clears one bit (the purchase / start-grant setter)",
        "00328A76": "BITMAP: 00328990 clears one bit (resetJobs' un-learn)",
        "0023A035": "not the record: BattleUnit +0x19C (same body loads the unit's stats record from [rdi+0x698], 00239FDA)",
        "00305867": "not the record: BattleUnit +0x19C (the body reads the actor at [rbx+0x10])",
        "0023ACD5": "record +0x1C3 selectors (block window only; base rdi is the record)",
        "0023ACDD": "record +0x1C5 selector", "00328D52": "record +0x1C3 selectors", "00328D5D": "record +0x1C5 selector",
        "0030C496": "record +0x1C2 level", "0030C7BB": "record +0x1C2 level",
    }
    got = sorted("%08X" % a for a, t, rt in ws)
    want = sorted(DISP)
    check("S4", got == want,
          "route-filtered writes into +0x194..+0x1C1 (record) / +0x19C..+0x1C9 (block), %d route functions "
          "(roots referencing 02EBF190, 02EBF038 or 02EBF1A0.., or in the record accesses TSV): %d sites, each dispositioned"
          % (len(route), len(got)))
    for a, t, rt in ws:
        note("%08X  fn %08X  %-48s %s" % (a, rt, t, DISP.get("%08X" % a, "UNDISPOSITIONED")))
    bm = [a for a in got if DISP.get(a, "").startswith("BITMAP")]
    check("S4a", bm == sorted(["00239C0D", "00239C17", "00239C1E", "00239C25", "00239C2C", "00239C33", "00239C39",
                               "00323A29", "00328A76"]),
          "displacement-form bitmap writers: 00323910 (00323A29), 00328990 (00328A76), 00239960 (00239C0D-00239C39)")

    # index forms outside the route, image-wide: byte stores must be shown to sit in a larger object
    byte_idx = [(a, t, rt) for a, t, rt, sz in rows["index"] if sz == 1]
    bad = []
    for a, t, rt in byte_idx:
        base = re.match(r"\[(\w+) \+ (\w+)", t[t.index("["):])
        regs = set(base.groups()) if base else set()
        pd, ins = decode_fn(img, a)
        far = False
        for x in ins.values():
            for op in x.operands:
                if op.type == X86_OP_MEM and op.mem.disp >= 0x1C8 and op.mem.base and x.reg_name(op.mem.base) in regs:
                    far = True
        if not far:
            bad.append("%08X" % a)
    roots = sorted(set("%08X" % rt for a, t, rt in byte_idx))
    check("S4c", not bad and roots == ["004453D0", "00447020", "00447ED0", "00449AB0"],
          "byte-wide index-form writes off the route (%d sites, image-wide) are all in %s, whose same base registers "
          "also address displacements >= 0x1C8 (an object larger than the 0x1C8-byte record, e.g. +0x1F0 at 00445895)%s"
          % (len(byte_idx), roots, "" if not bad else "; NOT shown for %s" % bad))
    note("non-byte index-form writes off the route: %d (dword/qword/xmm, roots %s)" % (
        len(rows["index"]) - len(byte_idx), sorted(set("%08X" % rt for a, t, rt, sz in rows["index"] if sz != 1))))
    # leaf writers (no .pdata): none on a route, and the ones in record-addressing leaves are the selectors
    onroute = [x for x in rows["leaf"] if any(c in ("%08X" % r) for r in route for c in x[2])]
    blockleaf = []
    brefs = set(r["site"] for r in text_refs(img, BLOCK, BLOCK + 8)[0])
    for a, t, c in rows["leaf"]:
        p = fn_of(a)
        if any(p <= s < a for s in brefs):
            blockleaf.append(("%08X" % a, t))
    check("S4b", not onroute and sorted(x[0] for x in blockleaf) ==
          ["00323722", "00323729", "00323772", "00323779", "00324341", "0032434B"] and
          all(CS._disp(t) >= 0x1C2 for x, t in blockleaf),
          "%d leaf (no .pdata) writes on a real boundary: none called from a route function; the six in leaves that "
          "load 02EBF190 are record +0x1C3..+0x1C5 selector stores %s" % (len(rows["leaf"]), [x for x, t in blockleaf]))
    note("all write hits in the window before the route filter: %d; stack-frame forms dropped: %d"
         % (rows["total"], rows["stack"]))
    return got, want


def main():
    img = Img.load()
    print("FABLE check_s31 - licence board grid and the writers of licenceOwnedBits (2026-10-03)")
    try:
        head = os.popen('git -C "%s" rev-parse --short HEAD' % REPO).read().strip()
    except Exception:
        head = "?"
    print("HEAD %s   unicorn %s" % (head, unicorn.__version__))
    pack = open(PACK, "rb").read()
    check("P0", hashlib.sha256(pack).hexdigest() == PACK_SHA and
          hashlib.sha256(open(BOARD1, "rb").read()).hexdigest() == BOARD1_SHA and unicorn.__version__ == "2.1.4",
          "inputs: battle_pack.bin (us) d1bb89aa..., board_1.bin (in) 5a220b2d..., unicorn 2.1.4")
    got, want = static_part(img)
    run_executed(img, pack)

    # ---- sensitivity controls ----
    def control(tag, patch, which, text):
        QUIET[0] = True
        f0 = FAILS[0]
        try:
            run_executed(img.patched(*patch), pack, which)
            failed = FAILS[0] > f0
        except Exception:
            failed = True
        FAILS[0] = f0
        QUIET[0] = False
        check(tag, failed, text)

    control("C1", (0x323A04, bytes.fromhex("0fb3c1")), ("setter", "cross"),
            "image mutated bts -> btr at 00323A04: X2/X8 now FAIL")
    control("C2", (0x323B15 + 2, bytes([0x0B])), ("rank",),
            "image mutated `cmp eax, 0xc` -> `cmp eax, 0xb` at 00323B15: X10 (node 30 in the arm) now FAILS")
    control("C3", (0x328A68, bytes.fromhex("9090")), ("reset",),
            "image mutated: the reset's keep test `jne` at 00328A68 NOPed: X11/X12 now FAIL")
    QUIET[0] = True
    f0 = FAILS[0]
    census_part(img.patched(0x239C39 + 3, bytes([0xC2])))
    failed = FAILS[0] > f0
    FAILS[0] = f0
    QUIET[0] = False
    check("C4", failed, "image mutated: 00239960's last zeroing store moved from +0x1C0 to +0x1C2 (00239C3C): the "
          "census no longer matches its dispositions (S4/S4a FAIL)")
    print("FAILS %d" % FAILS[0])
    raise SystemExit(1 if FAILS[0] else 0)


if __name__ == "__main__":
    main()
