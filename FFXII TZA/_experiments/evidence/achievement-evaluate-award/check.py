# EXP-089 — achievement evaluate+award + fire-helper execution
#
# CONTRACT-achievement-counters.md section 13 ran read `003166F0`, update
# `00316A50` and store `00316BF0` under diff_achievement_counters, but
# `00315E90` (evaluate+award, eight-arm descriptor-mode dispatch) and
# `003165C0` (fire helper: relative-offset chain -> bt mask -> rank-indexed
# threshold table) are "answered, not run". This harness executes them as
# shipped bytes at canonical VAs, plus the whole real call surface:
#
#   REAL (shipped bytes, canonical VA):
#     00315E90  evaluate+award        003165C0  fire helper (pure leaf)
#     00316760  counter lookup        003166F0  counter read
#     00316BF0  counter store         00316A50  update (+evaluate ordering)
#     002536A0  save-base getter      002536D0  playtime getter (clamp)
#     00254E80  playtime refresh      00320D50  playtime seconds (float+int)
#     00282DD0  inventory slot ptr    00282FA0  item rarity gate
#     00309EC0  family resolver entry (jmp [table+0x50] -> real resolver)
#     002FD970  fam3/4/6 resolver (u16-bitset test on edx=0 path)
#     00315420  mode-7 hunt-mark read 003160C0  mode-5 evaluator
#     003161A0  mode-6 evaluator      00264790  gated word getter (a)
#     00265270  gated word getter (b) 003148F0  fallback count getter
#     002EF2B0/002EF640  static addr chain      003779F0  u16 table lookup
#     003C4AD0  static object getter  00255060  bitfield popcount leaf
#     00255120  save record popcount  008632B0  award tail
#     0020CE00  platform object getter        0020CE60  platform award write
#
#   STUBBED WITH LOGGING (disclosed):
#     IAT 0x8C3190         - platform name->object getter inside 0020CE60;
#                            returns planted {+0x28: obj}
#     obj vtable +0x38/+0x50 - the two virtual calls the award write makes
#     fam3 entry +8        - shipped family table 0x1EEBCC0 has its DATA
#                            pointers runtime-initialised (zero on disk);
#                            counts +0x3C and resolver fnptrs +0x50 are
#                            shipped constants. The fixture plants only
#                            fam3's +8 u16-bitset pointer; the jmp-rax
#                            dispatch and resolver 002FD970 run real.
#
#   FIXTURE-PLANTED GLOBALS (disclosed):
#     [0x20927C0] = SAVEB  save image: awarded bitset +0x3844, counters
#                          +0x384C+desc[1], hunt marks +0x3404, records
#                          +0x224+i*0x20
#     [0x2092758] = playtime struct {+0xC dword seconds}
#     [0x2EBF190] = frame struct {+0x5AC8 float, +0x5ACC int} for 00320D50
#     [0x209AC30] = inventory base (items at +0x408+i*0xC0)
#     [0x2ADD100] = u16 lookup table {+4 count, +8 entries byte9<<8|byte8}
#     [0x22C2550] = THE chain root - shared by 003165C0 (4 link hops to the
#                   mask/rank table) and modes 5/6/7 (record at root+8 or
#                   1/3 link hops). Each case plants one interpretation.
#     [0x2098E20] = gate flag byte              [0x2098E10] = ptr for 00264790
#     [0x2098E58] = ptr for 00265270            [0x1F83450] = platform object
#     [0x1EEBCC0+idx*0x58] = shipped family table (counts+resolver fnptrs
#                            real; data pointers fixture-planted)
#
# Descriptor table 0xD10460 and award-code table 0xD10550 are the SHIPPED
# image bytes (not fixtures) unless a case patches a descriptor (disclosed).
#
# Entry signatures (measured against the bodies):
#   evaluate  00315E90  cl = id                    (return value unused)
#   fire      003165C0  cl = id         -> eax = threshold or 0
#   lookup    00316760  cl = id         -> eax = counter/-1/derived
#   read      003166F0  cl = id         -> eax = counter or -1
#   store     00316BF0  cl = id, edx = value
#   update    00316A50  cl = id, edx = amount
#
# Memory: GuestMem host buffers via mem_map_ptr (EXP-087 finding: this host's
# unicorn DLLs intermittently fail uc_mem_write/read on mapped pages).

import ctypes, hashlib, json, struct, sys, os
from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000
IMG_LO, IMG_HI = 0x120000, 0x2F800000

STUBS  = 0x50000000           # ret-stub page: 0x10-byte cells, hook supplies rax
TRAP   = 0x50010000           # unhandled-IAT trap page
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000
HIADDR = 0xFFFE0000           # pages for the 32-bit-wrap link guard case

# guest fixture addresses
SAVEB  = HEAP + 0x000000      # save image (0x4000 bytes)
PLAYT  = HEAP + 0x010000      # [0x2092758] -> {+0xC seconds}
FRAME  = HEAP + 0x020000      # [0x2EBF190] -> {+0x5AC8 f32, +0x5ACC i32}
INVB   = HEAP + 0x030000      # [0x209AC30] -> inventory, items +0x408+i*0xC0
U16T   = HEAP + 0x040000      # [0x2ADD100] -> {+4 count, +8 entries}
FROOT  = HEAP + 0x050000      # unused spare
MROOT  = HEAP + 0x060000      # [0x22C2550] -> fire chain / mode-5/6/7 root
MREC   = HEAP + 0x060080      # mode-6/7 record lands here
GPTR_A = HEAP + 0x070000      # [0x2098E10] -> word +0x7C source
GPTR_B = HEAP + 0x071000      # [0x2098E58] -> word +0 source
POBJ   = HEAP + 0x080000      # [0x1F83450] -> platform object
AWTBL  = HEAP + 0x090000      # [POBJ+8] -> award entries, code*0x198
OVTAB  = HEAP + 0x0A0000      # vtables for the two virtual calls
OBJA   = HEAP + 0x0B0000
OBJB   = HEAP + 0x0B1000
FAMT   = 0x1EEBCC0            # 00309EC0's shipped family table
FAM3BITS = HEAP + 0x0D0000     # u16 bitset for fam3 resolver (fixture)

# global cell addresses (fixed by the bodies)
G_SAVE   = 0x20927C0
G_PLAYT  = 0x2092758
G_FRAME  = 0x2EBF190
G_INV    = 0x209AC30
G_U16    = 0x2ADD100
G_MROOT  = 0x22C2550
G_FLAG   = 0x2098E20
G_PTRA   = 0x2098E10
G_PTRB   = 0x2098E58
G_POBJ   = 0x1F83450

DESC = 0xD10460               # shipped descriptor table, 30 x 8
AWARD = 0xD10550              # shipped award-code table, 30 x 4

IAT_NAME_STUB = 0x8C3190      # the name->object getter inside 0020CE60

# real bodies whose entry is traced (call-order evidence)
CALLS = {
    0x315E90: "eval",    0x3165C0: "fire",     0x316760: "lookup",
    0x3166F0: "read",    0x316BF0: "store",    0x316A50: "update",
    0x2536A0: "savebase",0x2536D0: "playtime", 0x254E80: "playrefresh",
    0x320D50: "secs",    0x282DD0: "invslot",  0x282FA0: "rarity",
    0x309EC0: "m2pred",  0x315420: "huntmark", 0x3160C0: "m5eval",
    0x3161A0: "m6eval",  0x264790: "worda",    0x265270: "wordb",
    0x3148F0: "fbcount", 0x2EF2B0: "ef2b0",    0x2EF640: "ef640",
    0x3779F0: "u16lk",   0x3C4AD0: "statobj",  0x255060: "popcount",
    0x255120: "reccount",0x8632B0: "awardtail",0x20CE00: "pobjget",
    0x20CE60: "paward",  0x2FD970: "fam3",
}

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)

def load_image():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    def rva2off(rva):
        for sva, vs, ra, rs in secs:
            if sva <= rva < sva + rs:
                return ra + rva - sva
        return None
    iat_names = {}
    imp_dir = pe + 24 + (112 if struct.unpack_from("<H", raw, pe + 24)[0] == 0x20B else 96) + 8
    imp_rva, _ = struct.unpack_from("<2I", raw, imp_dir)
    off2 = rva2off(imp_rva)
    i = 0
    while True:
        ilt, ts, fwd, name_rva, iat_rva = struct.unpack_from("<5I", raw, off2 + 20 * i)
        if name_rva == 0:
            break
        dll = raw[rva2off(name_rva):].split(b"\0")[0].decode()
        ilt = ilt or iat_rva
        j = 0
        while True:
            e = struct.unpack_from("<Q", raw, rva2off(ilt) + 8 * j)[0]
            if e == 0:
                break
            if e >> 63:
                nm = "#%x" % (e & 0xffff)
            else:
                no = rva2off(e & 0x7FFFFFFF)
                nm = raw[no + 2:].split(b"\0")[0].decode()
            iat_names[BASE + iat_rva + 8 * j] = "%s!%s" % (dll, nm)
            j += 1
        i += 1
    return raw, secs, iat_names

class GuestMem:
    """Host-backed guest memory via mem_map_ptr (EXP-087: this host's unicorn
    DLLs intermittently fail uc_mem_write/read on mapped pages)."""
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL, ctypes.addressof(buf))
        self.regions.append((addr, size, ctypes.addressof(buf)))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x" % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), data, len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)
    def wstr(self, addr):
        out = b""
        while True:
            c = self.r(addr, 2)
            if c == b"\0\0":
                break
            out += c; addr += 2
        return out.decode("utf-16-le")

class World:
    def __init__(self, case, raw, secs, iat_names):
        self.case = case
        self.iat_names = iat_names
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x1000000), (STACK, 0x100000), (RETQ, 0x1000),
                     (STUBS & ~0xFFF, 0x20000), (0x60000000, 0x20000),
                     (HIADDR, 0x40000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")
        for va in range(STUBS, TRAP, 0x10):
            gm.w(va, b"\xc3")
        for va in range(TRAP, TRAP + 0x10000, 0x10):
            gm.w(va, b"\xc3")
        # every IAT slot -> index-encoded trap; known slot -> name stub
        self.trap_of_slot, self.slot_of_trap = {}, {}
        for i, slot in enumerate(sorted(iat_names)):
            tv = TRAP + (i % 0x1000) * 0x10
            self.trap_of_slot[slot] = tv
            self.slot_of_trap[tv] = slot
            gm.w(slot, qw(tv))
        gm.w(IAT_NAME_STUB, qw(STUBS + 0x0000))
        # global cells
        gm.w(G_SAVE,  qw(case.get("save", SAVEB)))
        gm.w(G_PLAYT, qw(PLAYT))
        gm.w(G_FRAME, qw(FRAME))
        gm.w(G_INV,   qw(INVB))
        gm.w(G_U16,   qw(U16T))
        gm.w(G_MROOT, qw(case.get("fire_root", case.get("mroot", MROOT))))
        gm.w(G_FLAG,  bytes([case.get("gate_flag", 1)]))
        gm.w(G_PTRA,  qw(case.get("ptra", GPTR_A)))
        gm.w(G_PTRB,  qw(case.get("ptrb", GPTR_B)))
        gm.w(G_POBJ,  qw(case.get("pobj", POBJ)))
        # platform object: +8 -> award table, +0x18 flag byte
        gm.w(POBJ + 8,    qw(AWTBL))
        gm.w(POBJ + 0x18, bytes([case.get("pobj_flag", 0)]))
        # object returned by the name getter: {+0x28 -> objB}; objB vtable
        gm.w(OBJA + 0x28, qw(OBJB))
        gm.w(OBJA,        qw(OVTAB))
        gm.w(OBJB + 0x28, qw(OBJB))
        gm.w(OBJB,        qw(OVTAB + 0x100))
        for off in (0x38, 0x50):
            gm.w(OVTAB + off,         qw(STUBS + 0x0100 + off))
            gm.w(OVTAB + 0x100 + off, qw(STUBS + 0x0200 + off))
        # save image
        gm.w(SAVEB, b"\0" * 0x4000)
        for off, data in case.get("save_fill", []):
            gm.w(SAVEB + off, data)
        # playtime/frame structs
        gm.w(PLAYT + 0xC, dw(case.get("playtime", 0)))
        gm.w(FRAME + 0x5AC8, struct.pack("<f", case.get("frame_f", 0.0)))
        gm.w(FRAME + 0x5ACC, dw(case.get("frame_i", 0)))
        # u16 lookup table for 003779F0: {+4 count, +8+i*2: byte+9<<8|byte+8}
        u16e = case.get("u16", [])
        gm.w(U16T + 4, dw(len(u16e)))
        for i, v in enumerate(u16e):
            gm.w(U16T + 8 + i * 2, bytes([v & 0xFF, v >> 8]))
        # inventory items at INVB+0x408+i*0xC0
        for i, itm in enumerate(case.get("inv", [])):
            gm.w(INVB + 0x408 + i * 0xC0, itm)
        # gated-word getters
        gm.w(GPTR_A + 0x7C, hw(case.get("word_a", 0)))
        gm.w(GPTR_B,        hw(case.get("word_b", 0)))
        # fire-helper chain: root+8 -> L1 -> L2 -> L3 -> T {+4 mask, +8 rank}
        fire = case.get("fire")
        if fire is not None:
            root = case.get("fire_root", case.get("mroot", MROOT))
            term = case.get("fire_term", MROOT + 0x300)
            chain = [MROOT + 0x200, MROOT + 0x208, MROOT + 0x210, term]
            prev = root + 8
            for nxt in chain:
                gm.w(prev, hw(nxt - prev))
                prev = nxt
            gm.w(term + 4, dw(fire.get("mask", 0)))
            for i, v in enumerate(fire.get("rank", [])):
                gm.w(term + 8 + i * 4, dw(v))
        # mode-5/6/7 structure at G_MROOT root:
        #   mode5: record IS at root+8 (m_links=0)
        #   mode6: root+8 holds one link -> record (m_links=1)
        #   mode7: root+8 -> L1 -> L2 -> record   (m_links=3)
        mroot = case.get("mroot", MROOT)
        if case.get("m_rec") is not None:
            nl = case.get("m_links", 0)
            if nl == 0:
                gm.w(mroot + 8, case["m_rec"])
            else:
                hops = [MROOT + 0x40 + 8 * i for i in range(nl - 1)] + [MREC]
                prev = mroot + 8
                for h in hops:
                    gm.w(prev, hw(h - prev)); prev = h
                gm.w(MREC, case["m_rec"])
        # fam3 data pointer (entry+8, runtime-init'd in the live game ->
        # disclosed fixture): the edx=0 resolver path in shipped 002FD970
        # tests word[idx>>4] bit (idx&15) in this u16 array.
        if "fam3_bits" in case:
            gm.w(FAM3BITS, b"".join(hw(v) for v in case["fam3_bits"]))
            gm.w(FAMT + 3 * 0x58 + 8, qw(FAM3BITS))
        # per-case byte patches (mutants + descriptor patches, disclosed)
        for va, data in case.get("patch", []):
            gm.w(va, data)
        # state
        self.trace, self.faults, self.trapped = [], [], []
        self.stub_vals = dict(case.get("stub_vals", {}))
        uc = self.uc
        uc.hook_add(UC_HOOK_CODE, self.on_code, begin=STUBS, end=TRAP + 0xFFFF)
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in CALLS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    # ---- stub dispatch -------------------------------------------------------
    def pop_ret(self):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        ret = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        return ret

    def on_call(self, uc, addr, size, _):
        self.trace.append((CALLS[addr], "rcx=%x" % uc.reg_read(UC_X86_REG_RCX),
                           "rdx=%x" % uc.reg_read(UC_X86_REG_RDX)))

    def on_code(self, uc, addr, size, _):
        if addr >= TRAP:
            slot = self.slot_of_trap.get(addr, 0)
            self.trapped.append(addr)
            self.faults.append(("TRAP", self.iat_names.get(slot, hex(addr)),
                                uc.reg_read(UC_X86_REG_RIP)))
            uc.emu_stop()
            return
        cell = addr - STUBS
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        if cell == 0x0000:                      # IAT name->object getter
            name = self.gm.wstr(rcx) if rcx else ""
            self.trace.append(("nameobj", name))
            uc.reg_write(UC_X86_REG_RAX, self.objA if False else OBJA)
        elif cell in (0x0138, 0x0150, 0x0238, 0x0250):   # vtable slots
            self.trace.append(("vt_%x" % cell, "rcx=%x" % rcx, "rdx=%x" % rdx))
            uc.reg_write(UC_X86_REG_RAX, self.stub_vals.get(cell, 1))
        else:
            self.trace.append(("STUB", hex(addr)))
            uc.reg_write(UC_X86_REG_RAX, 0)
        uc.reg_write(UC_X86_REG_RIP, self.pop_ret())

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False

def build(case, raw, secs, iat_names):
    return World(case, raw, secs, iat_names)

def invoke(w, va, rcx=0, rdx=0, r8=0, r9=0, stack_args=()):
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    for i, a in enumerate(stack_args):
        gm.w(sp - 0x100 + i * 8, qw(a))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, rcx)
    uc.reg_write(UC_X86_REG_RDX, rdx)
    uc.reg_write(UC_X86_REG_R8, r8)
    uc.reg_write(UC_X86_REG_R9, r9)
    try:
        uc.emu_start(va, RETQ, count=8_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    return uc.reg_read(UC_X86_REG_RAX)

def expect(name, snap, cond, why):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name + ("  -- " + why if not ok else ""))
    return ok

# ---- entries -----------------------------------------------------------------
EVAL, FIRE, LOOKUP, READ, STORE, UPDATE = \
    0x315E90, 0x3165C0, 0x316760, 0x3166F0, 0x316BF0, 0x316A50

_raw = [None]
def img_read_raw(va, n):
    return _raw[0](va, n)

def desc_of(id_):
    return img_read_raw(DESC + id_ * 8, 8)

def save_bitset(id_):
    return [(0x3844 + (id_ >> 3), bytes([1 << (id_ & 7)]))]

def save_counter(id_, val):
    desc = desc_of(id_)
    off = 0x384C + desc[1]
    return [(off, hw(val))] if desc[0] == 2 else [(off, dw(val))]

def fire_chain(mask, rank):
    return {"mask": mask, "rank": rank}

def m7_l3(count, entries):
    """mode-7 terminal record: {+2 count u16, +4 u16 entries[count]}"""
    out = bytearray(0x40)
    struct.pack_into("<H", out, 2, count)
    for i, e in enumerate(entries):
        struct.pack_into("<H", out, 4 + i * 2, e)
    return bytes(out)

def m6_l1(outer_count, inner):
    """mode-6 record: {+2 outer, +6 inner_count, +8 entries 4B {key,arg}}"""
    out = bytearray(0x100)
    struct.pack_into("<H", out, 2, outer_count)
    struct.pack_into("<H", out, 6, len(inner))
    for i, (k, a) in enumerate(inner):
        struct.pack_into("<H", out, 8 + i * 4, k)
        struct.pack_into("<H", out, 8 + i * 4 + 2, a)
    return bytes(out)

def m5_rec(count, setbits):
    """mode-5 record at root+8: {+2 count, +4 bitset bytes}"""
    out = bytearray(0x100)
    struct.pack_into("<H", out, 2, count)
    for b in setbits:
        out[4 + (b >> 3)] |= 1 << (b & 7)
    return bytes(out)

def item(word60=3, flag0=0, ba=5):
    itm = bytearray(0xC0)
    itm[0] = flag0
    itm[0x60:0x62] = hw(word60)
    itm[0xBA] = ba
    return bytes(itm)

def run_case(case, raw, secs, iat_names):
    w = build(case, raw, secs, iat_names)
    rets = []
    for ph in case.get("phases", [{}]):
        rets.append(invoke(w, ph.get("entry", case.get("entry", EVAL)),
                           rcx=ph.get("rcx", case.get("rcx", 0)),
                           rdx=ph.get("rdx", case.get("rdx", 0)),
                           r8=ph.get("r8", case.get("r8", 0)),
                           r9=ph.get("r9", case.get("r9", 0))))
    sv = w.gm.r(case.get("save", SAVEB), 0x4000)
    flags = {c: w.gm.r(AWTBL + c * 0x198 + 0x190, 1)[0] for c in range(30)}
    snap = {
        "rets": [hex(r & 0xFFFFFFFF) for r in rets],
        "bitset": sv[0x3844:0x3848].hex(),
        "counters": sv[0x384C:0x3890].hex(),
        "hunt": sv[0x3404:0x3410].hex(),
        "award_flags": flags,
        "award_codes_set": sorted(c for c, v in flags.items() if v),
        "trace": [list(t) if isinstance(t, tuple) else t for t in w.trace],
        "faults": [list(f) if isinstance(f, tuple) else f for f in w.faults],
        "trapped": [hex(t) for t in w.trapped],
        "playt": struct.unpack("<I", w.gm.r(PLAYT + 0xC, 4))[0],
    }
    return snap, w

# ---- cases -------------------------------------------------------------------
def main():
    global _raw
    raw, secs, iat_names = load_image()
    def _img(va, n):
        r = va - BASE
        for sva, vs, ra, rs in secs:
            if sva <= r < sva + rs:
                return raw[ra + (r - sva):ra + (r - sva) + n]
        raise AssertionError("VA not in image: %x" % va)
    _raw[0] = _img

    only = sys.argv[1] if len(sys.argv) > 1 else None
    results = {}
    npass = nfail = 0

    def run(name, case, checks):
        nonlocal npass, nfail
        if only and only not in name:
            return
        snap, w = run_case(case, raw, secs, iat_names)
        results[name] = snap
        ok = True
        for cond, why in checks(snap):
            ok &= expect(name, snap, cond, why)
        if ok: npass += 1
        else:  nfail += 1

    tr = lambda s: [t[0] for t in s["trace"]]

    # ======================= fire helper 003165C0 ==========================
    FB = fire_chain(0b100101, [11, 22, 33])       # mask bits {0,2,5}
    run("fire-null-root", {"entry": FIRE, "rcx": 0, "fire_root": 0},
        lambda s: [(s["rets"] == ["0x0"], "null root -> 0")])
    run("fire-rank0", {"entry": FIRE, "rcx": 0, "fire": FB},
        lambda s: [(s["rets"] == ["0xb"], "id0 rank0 -> T[0]=11")])
    run("fire-rank1", {"entry": FIRE, "rcx": 2, "fire": FB},
        lambda s: [(s["rets"] == ["0x16"], "id2: popcount(mask&3)=1 -> T[1]=22")])
    run("fire-bit-clear", {"entry": FIRE, "rcx": 1, "fire": FB},
        lambda s: [(s["rets"] == ["0x0"], "id1: mask bit1 clear -> 0")])
    run("fire-id31", {"entry": FIRE, "rcx": 31,
                      "fire": fire_chain(0x80000000, [77])},
        lambda s: [(s["rets"] == ["0x4d"], "id31: bit31 -> rank0 -> 77")])
    run("fire-id32", {"entry": FIRE, "rcx": 32, "fire": FB},
        lambda s: [(s["rets"] == ["0x0"], "id32 >= 0x20 -> 0")])
    run("fire-root-neg8", {"entry": FIRE, "rcx": 0,
                           "fire_root": 0xFFFFFFFFFFFFFFF8},
        lambda s: [(s["rets"] == ["0x0"], "root=-8: add 8 wraps to 0 -> fail")])
    # 32-bit-wrap link guard: link node at 0xFFFF0001 holding 0xFFFF ->
    # low32(addr)+w = 0x100000000 -> eax=0 -> the `je` after `add` fires
    run("fire-wrap-guard", {"entry": FIRE, "rcx": 0,
                            "fire_root": 0xFFFEFFF9,
                            "patch": [(0xFFFF0001, hw(0xFFFF))]},
        lambda s: [(s["rets"] == ["0x0"], "link sum wraps to 0 -> fail"),
                   (s["faults"] == [], "no fault")])
    run("fire-mask-0", {"entry": FIRE, "rcx": 0, "fire": fire_chain(0, [9])},
        lambda s: [(s["rets"] == ["0x0"], "mask 0 -> 0")])

    # ======================= evaluate 00315E90 ==============================
    E0 = {"entry": EVAL, "fire": fire_chain(1, [10])}
    run("eval-id31-bound", {"entry": EVAL, "rcx": 0x1F},
        lambda s: [(tr(s) == ["eval"], "id 0x1f rejected before any call"),
                   (s["faults"] == [], "no fault")])
    run("eval-id30-alias", dict(E0, rcx=30),
        lambda s: [(s["faults"] == [], "id30 dispatches on aliased award-table bytes"),
                   (tr(s) == ["eval", "fire", "lookup", "read", "savebase"],
                    "mode0 arm on aliased desc: fire->lookup->read(-1) -> fail"),
                   (s["award_codes_set"] == [], "no award")])
    run("eval-awarded-early", dict(E0, rcx=0, save_fill=save_bitset(0)),
        lambda s: [(tr(s) == ["eval", "savebase"],
                    "awarded bit -> one getter, no dispatch"),
                   (s["award_codes_set"] == [], "no award write")])
    run("eval-m0-below", dict(E0, rcx=0),
        lambda s: [(tr(s) == ["eval", "savebase", "fire", "lookup", "read",
                              "savebase"],
                    "counter 0 < thr 10 -> no award"),
                   (s["award_codes_set"] == [], "no award"),
                   (s["bitset"] == "00000000", "bit not set")])
    run("eval-m0-at", dict(E0, rcx=0, save_fill=save_counter(0, 10)),
        lambda s: [(s["award_codes_set"] == [1], "counter 10 >= 10 -> award code 1"),
                   (s["bitset"][:2] == "01", "awarded bit written"),
                   (tr(s)[-4:] == ["awardtail", "pobjget", "pobjget", "paward"],
                    "tail order: awardtail->pobjget x2->paward")])
    run("eval-m0-fire0-fallback", {"entry": EVAL, "rcx": 0,
                                   "fire": fire_chain(0, [])},
        lambda s: [(s["award_codes_set"] == [1],
                    "fire=0 -> param 0 fallback -> counter 0 >= 0 -> award")])
    run("eval-m1-dead", {"entry": EVAL, "rcx": 19,
                         "fire": fire_chain(0xFFFFFFFF, [0] * 20)},
        lambda s: [(tr(s) == ["eval", "savebase"],
                    "id19 mode1 -> epilogue after bit check"),
                   (s["award_codes_set"] == [], "no award"),
                   (s["bitset"][4:6] == "00", "bit19 not set")])
    # mode-2 arm: id 9 param 0x30513000 -> loop bx=0x3000..0x3050, family 3,
    # REAL shipped resolver 002FD970 against the planted bitset.
    M2 = {"entry": EVAL, "rcx": 9, "fam3_bits": [0xFFFF] * 8,
          "fire": fire_chain(0, [])}
    run("eval-m2-all", dict(M2),
        lambda s: [(len([t for t in tr(s) if t == "fam3"]) == 0x51,
                    "81 resolver calls (0x3000..0x3050)"),
                   (s["award_codes_set"] == [15], "all pass -> award code 15")])
    run("eval-m2-one-missing", dict(M2, fam3_bits=[0xFFFF, 0xFFFE] + [0xFFFF] * 6),
        lambda s: [(len([t for t in tr(s) if t == "fam3"]) == 0x11,
                    "loop stops at first zero bit (idx 0x10)"),
                   (s["award_codes_set"] == [], "no award")])
    run("eval-m2-idx-arg", dict(M2, fam3_bits=[0xFFFE] + [0xFFFF] * 7),
        lambda s: [(next(t for t in s["trace"] if t[0] == "fam3")
                    [1] == "rcx=3000", "resolver sees FULL id in ecx"),
                   (next(t for t in s["trace"] if t[0] == "fam3")
                    [2] == "rdx=0", "edx always 0")])
    # 00309EC0 rejects index > count-1 with 0 (fail) but returns -1 for
    # sentinel ids (cx==0xFFFF or (cx&0xF000) > 0xE000) -> those auto-PASS
    run("eval-m2-oob-fail", {"entry": EVAL, "rcx": 18,
        "patch": [(DESC + 18 * 8 + 2, b"\x02"),
                  (DESC + 18 * 8 + 4, dw(0x30523000))],
        "fam3_bits": [0xFFFF] * 8, "fire": fire_chain(0, [])},
        lambda s: [(len([t for t in tr(s) if t == "fam3"]) == 0x51,
                    "0x51 in-bounds calls; idx 0x51 rejected before resolver"),
                   (len([t for t in tr(s) if t == "m2pred"]) == 0x52,
                    "resolver entry called for the OOB id too"),
                   (s["award_codes_set"] == [], "OOB index -> no award")])
    run("eval-m2-sentinel-pass", {"entry": EVAL, "rcx": 18,
        "patch": [(DESC + 18 * 8 + 2, b"\x02"),
                  (DESC + 18 * 8 + 4, dw(0xFFF8FFF0))],
        "fam3_bits": [0xFFFF] * 8, "fire": fire_chain(0, [])},
        lambda s: [(len([t for t in tr(s) if t == "fam3"]) == 0,
                    "sentinel ids never reach the resolver"),
                   (len([t for t in tr(s) if t == "m2pred"]) == 8,
                    "8 sentinel calls 0xFFF0..0xFFF7"),
                   (s["award_codes_set"] == [6],
                    "sentinel -1 counts as present -> award code 6")])
    # mode-3 arm: id 13 (kind2 mode3 param16); counter word at +0x384C+0x0a
    run("eval-m3-popcount", {"entry": EVAL, "rcx": 13,
                             "fire": fire_chain(0, []),
                             "save_fill": save_counter(13, 0xFFFF)},
        lambda s: [(s["award_codes_set"] == [19],
                    "fire=0 -> 16; popcount(0xFFFF as movsx)=16 >= 16 -> award")])
    run("eval-m3-below", {"entry": EVAL, "rcx": 13,
                          "fire": fire_chain(0, []),
                          "save_fill": save_counter(13, 0x7FFF)},
        lambda s: [(s["award_codes_set"] == [],
                    "popcount 15 < 16 -> no award")])
    run("eval-m3-fire-threshold", {"entry": EVAL, "rcx": 13,
                                   "fire": fire_chain(1 << 13, [3]),
                                   "save_fill": save_counter(13, 0b111)},
        lambda s: [(s["award_codes_set"] == [19],
                    "fire=3 -> popcount 3 >= 3 -> award")])
    # mode-5 arm: id 15 -> 003160C0; record at root+8
    # word_a=7 -> u16 table [7]=0 -> esi=0; bitset {0,1,2}; 255120(bx) counts
    rec = lambda i, b: (0x224 + i * 0x20, bytes([b]) + b"\0" * 31)
    run("eval-m5-pass", {"entry": EVAL, "rcx": 15, "m_rec": m5_rec(3, {0, 1, 2}),
                         "m_links": 0, "u16": [0] * 8, "word_a": 7,
                         "save_fill": [rec(0, 1), rec(1, 3), rec(2, 7)]},
        lambda s: [(s["award_codes_set"] == [18],
                    "all set bits pass reccount -> award code 18")])
    run("eval-m5-fail", {"entry": EVAL, "rcx": 15, "m_rec": m5_rec(3, {0, 1, 2}),
                         "m_links": 0, "u16": [0] * 8, "word_a": 7,
                         "save_fill": [rec(0, 1), rec(2, 7)]},
        lambda s: [(s["award_codes_set"] == [],
                    "bit1 set but record empty -> reccount=0 -> no award")])
    # mode-6 arm: id 16 -> 003161A0. outer 2: bx=0 (no entry -> 315420(0)),
    # bx=1 via inner {key=1 fam0, arg=5} -> wordb 9 >= 5
    run("eval-m6-pass", {"entry": EVAL, "rcx": 16, "m_rec": m6_l1(2, [(1, 5)]),
                         "m_links": 1, "word_b": 9,
                         "save_fill": [(0x3404, bytes([2]))]},
        lambda s: [(s["award_codes_set"] == [14],
                    "outer0 via huntmark(0)=1>0, outer1 via wordb 9>=5 -> award")])
    run("eval-m6-fail", {"entry": EVAL, "rcx": 16, "m_rec": m6_l1(2, [(1, 5)]),
                         "m_links": 1, "word_b": 2,
                         "save_fill": [(0x3404, bytes([2]))]},
        lambda s: [(s["award_codes_set"] == [],
                    "outer1 wordb 2<5 -> no award")])
    # mode-7 arm: ids 20.. param selects entry; 315420(entry)=mark-1>0 iff >=2
    M7 = {"entry": EVAL, "m_rec": m7_l3(4, [1, 7, 2, 9]), "m_links": 3,
          "save_fill": [(0x3404, bytes([0, 3, 9, 0]))]}
    run("eval-m7-pass", dict(M7, rcx=20),
        lambda s: [(s["award_codes_set"] == [22],
                    "param0 -> entry1 -> mark[1]=3 -> 2>0 -> award code 22")])
    run("eval-m7-fail", dict(M7, rcx=21),
        lambda s: [(s["award_codes_set"] == [],
                    "param1 -> entry7 -> mark[7]=0 -> -1 -> no award")])
    run("eval-m7-oob", dict(M7, rcx=24),
        lambda s: [(s["award_codes_set"] == [],
                    "param4 >= count4 -> reject before huntmark"),
                   ("huntmark" not in tr(s), "315420 never called")])
    # modes 1/4 dead: patch a descriptor's mode byte (disclosed image patch)
    run("eval-mode1-dead-patched", {"entry": EVAL, "rcx": 0,
        "patch": [(DESC + 0 * 8 + 2, b"\x01")],
        "save_fill": save_counter(0, 9999), "fire": fire_chain(1, [0])},
        lambda s: [(tr(s) == ["eval", "savebase"],
                    "mode1 descriptor -> epilogue after bit check"),
                   (s["award_codes_set"] == [], "no award")])
    run("eval-mode4-dead-patched", {"entry": EVAL, "rcx": 0,
        "patch": [(DESC + 0 * 8 + 2, b"\x04")],
        "save_fill": save_counter(0, 9999), "fire": fire_chain(1, [0])},
        lambda s: [(tr(s) == ["eval", "savebase"],
                    "mode4 descriptor -> epilogue after bit check"),
                   (s["award_codes_set"] == [], "no award")])
    run("eval-mode8-reject", {"entry": EVAL, "rcx": 0,
        "patch": [(DESC + 0 * 8 + 2, b"\x08")],
        "save_fill": save_counter(0, 9999), "fire": fire_chain(1, [0])},
        lambda s: [(tr(s) == ["eval", "savebase"],
                    "mode>7 descriptor -> epilogue after bit check"),
                   (s["award_codes_set"] == [], "no award")])

    # ======================= lookup 00316760 ================================
    run("lookup-kind2", {"entry": LOOKUP, "rcx": 0,
                         "save_fill": save_counter(0, 0x1234)},
        lambda s: [(s["rets"] == ["0x1234"], "word counter read")])
    run("lookup-kind4", {"entry": LOOKUP, "rcx": 6,
                         "save_fill": save_counter(6, 0x1000)},
        lambda s: [(s["rets"] == ["0x1000"], "dword counter read")])
    run("lookup-kind0-neg1", {"entry": LOOKUP, "rcx": 18},
        lambda s: [(s["rets"] == ["0xffffffff"], "kind0 id18 -> -1")])
    run("lookup-id5-playtime", {"entry": LOOKUP, "rcx": 5,
                                "frame_f": 3600.0, "frame_i": 7},
        lambda s: [(s["rets"] == ["0xe17"], "id5: playtime 3600+7=3607"),
                   (s["playt"] == 3607, "playrefresh wrote [0x2092758]+0xC"),
                   (tr(s) == ["lookup", "read", "savebase", "playrefresh",
                              "secs", "playtime"], "refresh-then-read order")])
    run("lookup-id8-empty-inv", {"entry": LOOKUP, "rcx": 8},
        lambda s: [(s["rets"] == ["0x0"], "id8 no qualifying items -> 0 (not -1)")])
    run("lookup-id8-avg", {"entry": LOOKUP, "rcx": 8,
                           "inv": [item()] * 6 + [item(word60=9)] * 3},
        lambda s: [(s["rets"] == ["0x5"], "6 items, avg byte[+0xBA]=5 -> 5"),
                   (len([t for t in tr(s) if t == "invslot"]) == 9,
                    "all 9 slots scanned")])
    run("lookup-id8-five", {"entry": LOOKUP, "rcx": 8,
                            "inv": [item()] * 5 + [item(word60=9)] * 4},
        lambda s: [(s["rets"] == ["0x0"], "5 qualifying < 6 -> 0, not avg")])

    # ======================= update 00316A50 ================================
    # ordering: evaluate sees the PRE-ADD counter (call 315E90 before store)
    O = {"entry": UPDATE, "rcx": 0, "fire": fire_chain(1, [10])}
    run("upd-order-first", dict(O, rdx=5),
        lambda s: [(s["award_codes_set"] == [],
                    "counter 0 +5: evaluate saw 0 <10 -> no award this call"),
                   (s["counters"][0:4] == "0500", "new value 5 still stored"),
                   (tr(s).index("eval") < tr(s).index("store"),
                    "eval before store in trace")])
    run("upd-order-real", dict(O,
        phases=[{"entry": UPDATE, "rcx": 0, "rdx": 15},
                {"entry": UPDATE, "rcx": 0, "rdx": 0}]),
        lambda s: [(s["award_codes_set"] == [1],
                    "phase2 evaluate sees stored 15 >= 10 -> award lands one update late"),
                   (s["bitset"][:2] == "01", "awarded bit set")])
    run("upd-kind0-mode0", {"entry": UPDATE, "rcx": 18, "rdx": 7,
                            "fire": fire_chain(1 << 18, [7])},
        lambda s: [(s["award_codes_set"] == [6],
                    "kind0 mode0: amount 7 >= fire-thr 7 -> award code 6")])
    run("upd-kind0-mode0-below", {"entry": UPDATE, "rcx": 18, "rdx": 5,
                                  "fire": fire_chain(1 << 18, [7])},
        lambda s: [(s["award_codes_set"] == [],
                    "amount 5 < 7 -> no award")])
    run("upd-kind0-m1-eq", {"entry": UPDATE, "rcx": 19, "rdx": 0xD07F},
        lambda s: [(s["award_codes_set"] == [17],
                    "id19 amount==param 0xD07F -> award code 17 via update dispatch")])
    run("upd-kind0-m1-ne", {"entry": UPDATE, "rcx": 19, "rdx": 5},
        lambda s: [(s["award_codes_set"] == [], "amount 5 != param -> no award")])
    run("upd-m3-bts", {"entry": UPDATE, "rcx": 13, "rdx": 0xE2 + 3,
                       "fire": fire_chain(0, [])},
        lambda s: [(s["counters"][0x14:0x18] == "0800",
                    "mode3 update: bts bit (0xE5-0xE2)=3 -> word 0x0008")])
    run("upd-sat-word", {"entry": UPDATE, "rcx": 0, "rdx": 0x7FFFFFF0,
                         "save_fill": save_counter(0, 100),
                         "fire": fire_chain(0, [])},
        lambda s: [(s["counters"][0:4] == "ff7f", "kind2 saturates at 0x7FFF")])
    run("upd-neg-clamp", {"entry": UPDATE, "rcx": 0, "rdx": (-200) & 0xFFFFFFFF,
                          "save_fill": save_counter(0, 100),
                          "fire": fire_chain(0, [])},
        lambda s: [(s["counters"][0:4] == "0000", "negative sum clamps to 0")])
    run("upd-id-bound", {"entry": UPDATE, "rcx": 30, "rdx": 5},
        lambda s: [(tr(s) == ["update"], "id30 rejected (update bound is 0x1e)")])
    run("upd-mode8-skip", {"entry": UPDATE, "rcx": 0, "rdx": 5,
        "patch": [(DESC + 0 * 8 + 2, b"\x08")],
        "fire": fire_chain(0, [])},
        lambda s: [(s["counters"][0:4] == "0000", "mode8: no store"),
                   (s["award_codes_set"] == [], "no award"),
                   ("eval" not in tr(s), "evaluate not called")])

    # ======================= award tail 008632B0/0020CE60 ===================
    run("award-null-pobj", {"entry": EVAL, "rcx": 0, "pobj": 0,
                            "save_fill": save_counter(0, 99),
                            "fire": fire_chain(0, [])},
        lambda s: [(tr(s)[-2:] == ["awardtail", "pobjget"],
                    "pobj null -> awardtail returns after pobjget"),
                   (s["bitset"][:2] == "01", "awarded bit still set")])
    run("award-obj-flag", dict(E0, rcx=0, save_fill=save_counter(0, 10),
                             pobj_flag=1),
        lambda s: [(len([t for t in tr(s) if t == "nameobj"]) == 2,
                    "pobj+0x18 set -> two name lookups"),
                   (len([t for t in tr(s) if t.startswith("vt_")]) == 2,
                    "two vtable calls"),
                   (s["award_codes_set"] == [1], "entry flag written")])

    # ======================= mutants (byte patches) =========================
    M = []
    def mut(name, case, patch, checks):
        c = dict(case)
        c["patch"] = c.get("patch", []) + [patch]
        M.append((name, c, checks))

    MUT = dict(E0, rcx=0, save_fill=save_counter(0, 10))
    mut("mut-eval-bound31->30", dict(MUT, rcx=30), (0x315E92, b"\x1e"),
        lambda s: [(tr(s) == ["eval"], "id30 now rejected by widened bound")])
    mut("mut-awarded-invert", dict(MUT), (0x315EE0, b"\x84"),   # jne->je
        lambda s: [(tr(s) == ["eval", "savebase"],
                    "unawarded id now early-returns"),
                   (s["award_codes_set"] == [], "no award")])
    mut("mut-jt-bound7->3", {"entry": EVAL, "rcx": 15,
                             "m_rec": m5_rec(3, {0, 1, 2}), "m_links": 0,
                             "u16": [0] * 8, "word_a": 7,
                             "save_fill": [rec(0, 1), rec(1, 3), rec(2, 7)]},
        (0x315F05, b"\x03"),
        lambda s: [(s["award_codes_set"] == [], "mode5 > 3 -> epilogue"),
                   (tr(s) == ["eval", "savebase"], "no arm executed")])
    mut("mut-m0-jl->jle", dict(MUT), (0x315F3C, b"\x8e"),
        lambda s: [(s["award_codes_set"] == [],
                    "counter==threshold no longer awards")])
    mut("mut-m3-loop16->8", {"entry": EVAL, "rcx": 13,
                             "fire": fire_chain(1 << 13, [5]),
                             "save_fill": save_counter(13, 0xFF00)},
        (0x315FCA, b"\x08"),
        lambda s: [(s["award_codes_set"] == [],
                    "popcount over low 8 bits = 0 < 5 -> no award")])
    mut("mut-fire-idbound32->16", {"entry": FIRE, "rcx": 16,
        "fire": fire_chain(0x10000, [55])},
        (0x316601, b"\x10"),
        lambda s: [(s["rets"] == ["0x0"], "id16 now rejected")])
    mut("mut-lookup-avg6->5", {"entry": LOOKUP, "rcx": 8,
        "inv": [item()] * 5 + [item(word60=9)] * 4},
        (0x3167DB, b"\x05"),
        lambda s: [(s["rets"] == ["0x5"], "5 items now enough -> avg 5")])
    mut("mut-upd-e2->e0", {"entry": UPDATE, "rcx": 13, "rdx": 0xE2 + 3,
                           "fire": fire_chain(0, [])},
        (0x316B75, b"\x20"),
        lambda s: [(s["counters"][0x14:0x18] == "2000",
                    "bts bit 5 instead of 3 -> word 0x0020")])
    mut("mut-sat-7fff->7ffe", {"entry": UPDATE, "rcx": 0, "rdx": 0x7FFFFFF0,
                               "save_fill": save_counter(0, 100),
                               "fire": fire_chain(0, [])},
        (0x316B97, b"\xfe"),
        lambda s: [(s["counters"][0:4] == "fe7f", "saturates at 0x7FFE")])

    nmut_pass = nmut_fail = 0
    for name, case, checks in M:
        if only and only not in name:
            continue
        snap, w = run_case(case, raw, secs, iat_names)
        results[name] = snap
        ok = True
        for cond, why in checks(snap):
            ok &= expect(name, snap, cond, why)
        if ok: nmut_pass += 1
        else:  nmut_fail += 1

    print("\n%d/%d cases, %d/%d mutants detected" %
          (npass, npass + nfail, nmut_pass, nmut_pass + nmut_fail))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "result.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1)
    return 0 if nfail + nmut_fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
