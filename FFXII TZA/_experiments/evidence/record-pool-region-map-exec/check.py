# EXP-107 record-pool-region-map-exec
#
# Executes the SHIPPED bytes of the actor record pool's allocation
# arithmetic and region-map dispatch — the CONTRACT-actor-record-pool-
# and-region-map section-7 residual — under Unicorn:
#
#   002679F0  ALLOC   ActorStorage_AllocateAndInitializeRecords:
#             rcx = manager slot.
#               r12 = q[rcx]            descriptor
#               r11d = d[rcx+0x20]      record count
#               r13d = w[desc+sx(d[desc+0x14])]           group count
#               r9d  = sum_i align16(w[TAB+i*4+2]) * w[desc+off+2+i*2]
#               esi  = align16(cnt*8 + 0x17)              ptr-table span
#               edi  = 2*esi                            record offset
#               pool = q[rcx+0x88](edi + r9d)           fn-ptr (planted)
#               memset(pool, 0, total)                  CRT thunk stub
#               d[pool] = cnt ; q[rcx+0x1F0] = pool+esi
#               per group i: w[rcx+TAB[i].kind*2+0x1D0] += cnt_i
#                 per record j: q[pool+j*8+8] = rdx
#                   b[rdx+3] = kind<<5 | i&0x1F  (packedKindAndSequence)
#                   rdx += align16(TAB[i].recsize)
#               prefix: w[rcx+0x1D8+k*2] = sum_{j<k} kindcnt[j]  (4x)
#               00266530(rcx, pool, ebp) per ebp<cnt    (boundary)
#               ret pool
#             TAB = shipped table 0x1E0C328, 8 x {u8 kind, u8 subflag,
#             u16 recsize} — real image bytes.
#
#   00266AD0  RMAP    region-map dispatch: rcx = record.
#               seq = b[rcx+3] & 0x1F ; seq > 7 -> ret
#               jump table 0x266BA4:
#                 g0:      +0xB8=0     +0xC0=0     r8=+0x120
#                 g1/2:    +0xB8=+0x120 +0xC0=0    r8=+0x1A0
#                 g3/4:    +0xB8=+0x120 +0xC0=0    r8=+0x140
#                 g5/6/7:  +0xB8=+0x120 +0xC0=+0x350 r8=+0x4D8
#               +0xA0 = r8
#               +0xA8 = r8 + (b[0x1E0C329+seq*4]==1 ? 0xC8 : 0xA0)
#             The sub-flag byte is TAB[seq].subflag — same shipped table.
#
# Scripted boundaries (disclosed):
#   00861EC0  memset CRT thunk — entry-intercepted, zero-fill implemented
#             harness-side (the IAT target is outside the image).
#   00266530  per-record init — full ~600 B ctor with 8 callees; arg
#             capture only (it calls 00266AD0 internally, which EXP-107
#             executes directly as subject B).
#   ALLOCVA   the planted allocator fn-ptr — returns the fixture pool.
#
# The contract's negative claim (no other arm touches these offsets)
# is not provable by replay; disclosed in the record.
#
# Trace tokens: a<size> alloc fn-ptr, ms<dst>:<n> memset, i<idx> init.
# Observables: ret, trace, final memory image (pool header, ptr-table,
# prefix words, record packed bytes, region-map qwords, memset tail).

import ctypes, hashlib, json, struct, sys

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, \
    UC_MODE_64, UC_PROT_ALL, Uc
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP, UC_X86_REG_RSP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

ALLOC  = 0x002679F0
RMAP   = 0x00266AD0
MEMSET = 0x00861EC0        # CRT thunk — entry-intercepted
INIT   = 0x00266530        # per-record init — scripted boundary
ALLOCVA = 0x63000000       # planted allocator fn-ptr stub

MGR    = HEAP + 0x000000   # manager slot
DESC   = HEAP + 0x100000   # descriptor (runtime-populated in game)
POOL   = HEAP + 0x400000   # allocator-returned pool
REC    = HEAP + 0x800000   # region-map record

TAB    = 0x01E0C328        # shipped table: 8 x {u8 kind, u8 sub, u16 size}
SUBTAB = 0x01E0C329        # TAB+1 — the sub-flag byte the RMAP reads

# shipped table contents (verified against the image):
#   grp: kind sub recsize        arm
#    0:    0   0   0x328        g0
#    1:    1   0   0x3a8        g1/2
#    2:    1   1   0x330        g1/2
#    3:    2   0   0x348        g3/4
#    4:    2   1   0x2d0        g3/4
#    5:    3   0   0x6e0        g5/6/7
#    6:    3   0   0x6e0        g5/6/7
#    7:    3   1   0x668        g5/6/7


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def s32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v
def align16(v): return (v + 0xF) & ~0xF


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
    return raw, secs


class GuestMem:
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
        ctypes.memmove(self._ptr(addr, len(data)), bytes(data), len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)


class World:
    def __init__(self, case, raw, secs):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(STACK, 0x100000)
        gm.map(ALLOCVA, 0x1000, init=b"\xc3" + b"\xcc" * 0xFFF)

        # manager slot + descriptor (allocator fixture)
        cnt = case.get("count", 0)
        groups = case.get("groups", [])        # per-group record counts
        gm.w(MGR + 0x00, qw(case.get("desc", DESC)))
        gm.w(MGR + 0x20, dw(cnt))
        gm.w(MGR + 0x88, qw(ALLOCVA))
        # kind-count accumulators may be pre-seeded
        for k in range(4):
            gm.w(MGR + 0x1D0 + k * 2, hw(case.get("kseed", [0] * 4)[k]))
        desc = case.get("desc", DESC)
        off = case.get("doff", 0x40)
        gm.w(desc + 0x14, dw(off))
        gm.w(desc + off, hw(len(groups)))
        for i, c in enumerate(groups):
            gm.w(desc + off + 2 + i * 2, hw(c))
        # pool starts poisoned — a skipped memset leaves 0xAA behind
        gm.w(POOL, b"\xaa" * 0x100000)

        # region-map record
        gm.w(REC + 3, bytes([case.get("pk", 0) & 0xFF]))

        self.trace, self.faults, self.fired = [], [], set()
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in (MEMSET, INIT, ALLOCVA):
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def _pop_ret(self):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        uc.reg_write(UC_X86_REG_RIP, back)

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        gm = self.gm
        if addr == MEMSET:
            dst = uc.reg_read(UC_X86_REG_RCX)
            n = uc.reg_read(UC_X86_REG_R8)
            self.trace.append("ms%x:%x" % (dst & 0xFFFFFFFF, n))
            gm.w(dst, b"\x00" * n)
            self._pop_ret()
        elif addr == INIT:
            idx = uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF
            self.trace.append("i%d" % s32(idx))
            self._pop_ret()
        elif addr == ALLOCVA:
            n = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
            self.trace.append("a%x" % n)
            uc.reg_write(UC_X86_REG_RAX, POOL)
            self._pop_ret()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False


def run_case(case, raw, secs):
    w = World(case, raw, secs)
    uc = w.uc
    sp = STACK + 0x80000
    w.gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    entry = case.get("entry", ALLOC)
    uc.reg_write(UC_X86_REG_RCX,
                 case.get("rcx", MGR if entry == ALLOC else REC))
    try:
        uc.emu_start(entry, RETQ, count=200_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))

    gm = w.gm
    obs = {"ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF}
    if entry == ALLOC:
        cnt = s32(case.get("count", 0))
        total = model_total(case, raw, secs)
        obs["hdr"] = struct.unpack("<I", gm.r(POOL, 4))[0]
        obs["ptrtbl"] = struct.unpack("<Q", gm.r(MGR + 0x1F0, 8))[0]
        obs["kcnt"] = [struct.unpack("<H", gm.r(MGR + 0x1D0 + k * 2, 2))[0]
                       for k in range(4)]
        obs["pfx"] = [struct.unpack("<H", gm.r(MGR + 0x1D8 + k * 2, 2))[0]
                      for k in range(4)]
        obs["xtra"] = {k: struct.unpack("<H", gm.r(MGR + 0x1D0 + k * 2, 2))[0]
                       for k in range(4, 16)}
        tab = []
        for j in range(min(max(cnt, 0), 8)):
            tab.append(struct.unpack("<Q", gm.r(POOL + 8 + j * 8, 8))[0])
        obs["tab"] = tab

        def pk_of(t):
            if not t:
                return -1
            try:
                return gm.r(t + 3, 1)[0]
            except KeyError:
                return -2
        obs["pk"] = [pk_of(t) for t in tab[:4]]
        if total:
            obs["tail"] = gm.r(POOL + total - 1, 1)[0]
    else:
        for name, off in (("b8", 0xB8), ("c0", 0xC0), ("a0", 0xA0),
                          ("a8", 0xA8)):
            obs[name] = struct.unpack("<Q", gm.r(REC + off, 8))[0]
    return " ".join(w.trace) or "-", w.faults, w, obs


# ---- model -------------------------------------------------------------------

def model_total(case, raw, secs):
    cnt = s32(case.get("count", 0)) & 0xFFFFFFFF
    groups = case.get("groups", [])
    r9 = 0
    for i in range(len(groups)):
        kind, sub, size = raw_tab(raw, secs, i)
        r9 = (r9 + align16(size) * (groups[i] & 0xFFFF)) & 0xFFFFFFFF
    esi = ((cnt * 8 + 0x17) & 0xFFFFFFFF) & 0xFFFFFFF0
    return (2 * esi + r9) & 0xFFFFFFFF


def model(case, raw, secs):
    tr, obs = [], {}
    entry = case.get("entry", ALLOC)
    if entry == RMAP:
        seq = case.get("pk", 0) & 0x1F
        if seq > 7:
            # ja -> ret with rax = cdqe(seq)
            return "-", {"ret": seq, "b8": 0, "c0": 0, "a0": 0, "a8": 0}
        sub = raw_tab(raw, secs, seq)[1]
        b8 = c0 = 0
        if seq == 0:
            r8 = REC + 0x120
        elif seq <= 2:
            b8, r8 = REC + 0x120, REC + 0x1A0
        elif seq <= 4:
            b8, r8 = REC + 0x120, REC + 0x140
        else:
            b8, c0 = REC + 0x120, REC + 0x350
            r8 = REC + 0x4D8
        a0 = r8
        # cmp flag,1; mov eax,0xC8; jne skips mov eax,0xA0
        a8 = r8 + (0xA0 if sub == 1 else 0xC8)
        return "-", {"ret": a8, "b8": b8, "c0": c0, "a0": a0, "a8": a8}

    cnt = s32(case.get("count", 0))
    cntu = cnt & 0xFFFFFFFF
    groups = case.get("groups", [])
    ng = len(groups)

    r9 = 0
    for i in range(ng):
        kind, sub, size = raw_tab(raw, secs, i)
        r9 = (r9 + align16(size) * (groups[i] & 0xFFFF)) & 0xFFFFFFFF
    esi = ((cntu * 8 + 0x17) & 0xFFFFFFFF) & 0xFFFFFFF0
    edi = (2 * esi) & 0xFFFFFFFF
    total = (edi + r9) & 0xFFFFFFFF

    tr.append("a%x" % total)
    tr.append("ms%x:%x" % (POOL, total))

    ntab = min(max(cnt, 0), 8)
    npk = min(max(cnt, 0), 4)
    kcnt = list(case.get("kseed", [0] * 4))
    xtra = {}        # kind>=4 prefix writes land outside the 4-word row
    tab, pk = [], []
    rdx = POOL + edi
    j = 0
    for i in range(ng):
        kind, sub, size = raw_tab(raw, secs, i)
        cw = groups[i] & 0xFFFF
        c = s32(cw)
        if cw and kind >= 8:
            # kinds 4-7 are dead writes (the prefix loop overwrites those
            # slots afterwards); kinds >=8 land past the prefix row
            xtra[kind] = (xtra.get(kind, 0) + cw) & 0xFFFF
        elif cw and kind < 4:
            kcnt[kind] += cw
        for _ in range(max(c, 0)):
            if j < ntab:
                tab.append(rdx)
            if j < npk:
                pk.append(((kind << 5) | (i & 0x1F)) & 0xFF)
            j += 1
            rdx += align16(size)
    while len(tab) < ntab:
        tab.append(0)
    while len(pk) < npk:
        pk.append(-1)

    run = 0
    pfx = []
    for k in range(4):
        pfx.append(run & 0xFFFF)
        run += kcnt[k]

    for i in range(max(cnt, 0)):
        tr.append("i%d" % i)

    # d[pool]=cnt is written before the record loop; when edi==0 the first
    # record sits at POOL+0 and its packed +3 write clobbers hdr byte 3
    hdr = cntu
    if edi == 0 and j > 0:
        i0 = next(i for i in range(ng) if s32(groups[i] & 0xFFFF) > 0)
        k0 = raw_tab(raw, secs, i0)[0]
        hdr = (hdr & 0x00FFFFFF) | (((k0 << 5) | (i0 & 0x1F)) << 24)

    # fixed obs window: kinds 4-7 show the prefix values (written last),
    # kinds 8-15 show the accumulated counts
    xw = {k: pfx[k - 4] for k in range(4, 8)}
    for k in range(8, 16):
        xw[k] = xtra.get(k, 0)

    obs = {"ret": POOL, "hdr": hdr & 0xFFFFFFFF, "ptrtbl": (POOL + esi) & 0xFFFFFFFFFFFFFFFF,
           "kcnt": [k & 0xFFFF for k in kcnt], "xtra": xw,
           "pfx": pfx, "tab": tab, "pk": pk, "tail": 0,
           "_total": total}
    return " ".join(tr), obs


def raw_tab(raw, secs, i):
    """shipped table row i: (kind, subflag, recsize) — image bytes."""
    rva = TAB - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva < sva + rs:
            off = ra + (rva - sva) + i * 4
            kind, sub = raw[off], raw[off + 1]
            size = struct.unpack_from("<H", raw, off + 2)[0]
            return kind, sub, size
    raise KeyError("table outside image")


# ---- cases -------------------------------------------------------------------

def build_cases():
    C = []

    def A(name, **kw):
        C.append(dict(name=name, **kw))

    # ---- ALLOC ----
    A("alloc-1grp", count=3, groups=[3])
    A("alloc-2grp", count=5, groups=[3, 2])
    A("alloc-4grp", count=10, groups=[2, 3, 2, 3])
    A("alloc-8grp", count=16, groups=[1, 2, 1, 2, 3, 2, 3, 2])
    A("alloc-0grp", count=4, groups=[])
    A("alloc-0cnt", count=0, groups=[2])
    A("alloc-0both", count=0, groups=[])
    A("alloc-neg-cnt", count=0xFFFFFFFE, groups=[1])
    A("alloc-kseed", count=4, groups=[2, 2], kseed=[7, 0, 0, 0])
    A("alloc-doff", count=4, groups=[4], doff=0x80)
    A("alloc-mixed-kind", count=7, groups=[0, 4, 0, 3])
    A("alloc-grp-skip", count=5, groups=[0, 5])
    # 17 groups: group 16's record is j=0; TAB[16]={kind 3, size 0}
    # discriminates i&0x1F (pk=0x70) from i&0x0F (pk=0x60)
    A("alloc-grp16", count=1, groups=[0] * 16 + [1])
    # ---- RMAP: every group arm + sub-flag selection ----
    for g in range(8):
        A("rm-g%d" % g, entry=RMAP, pk=g)
    A("rm-g2-hikind", entry=RMAP, pk=0xE2)     # kind 7<<5 | 2 — arm by seq
    A("rm-g5-hikind", entry=RMAP, pk=0x65)
    A("rm-seq8", entry=RMAP, pk=8)
    A("rm-seq1f", entry=RMAP, pk=0x1F)
    A("rm-seq20-wrap", entry=RMAP, pk=0x20)    # &0x1F -> 0
    A("rm-seqff", entry=RMAP, pk=0xFF)
    return C


# ---- mutants -----------------------------------------------------------------

MUTANTS = [
    # ALLOC arithmetic
    ("m-addf",    0x267A52, b"\x1f",
     "align16 add 0xF -> 0x1F: record-span totals shift"),
    ("m-shr4",    0x267A55, b"\x05",
     "size shr 4 -> 5: half-size records"),
    ("m-shl4",    0x267A5B, b"\x05",
     "total shl 4 -> 5: double-size span"),
    ("m-tab17",   0x267A6C, b"\x27",
     "ptr-table bias 0x17 -> 0x27: table span shifts"),
    ("m-andf0",   0x267A6F, b"\xe0",
     "ptr-table mask 0xF0 -> 0xE0: misaligned span"),
    ("m-2x",      0x267A72, b"\x76",
     "edi = rsi+rsi -> rsi+rsi*2 (scale 2): 3x table span"),
    ("m-fnptr",   0x267A7C, b"\x90\x00\x00\x00",
     "fn-ptr +0x88 -> +0x90: wrong allocator slot"),
    ("m-hdr",     0x267AA6, b"\x46\x08",
     "pool header d[0] -> d[+8]: count lands in table A"),
    ("m-pt1f0",   0x267AAC, b"\xf8\x01\x00\x00",
     "mgr+0x1F0 -> +0x1F8: ptr-table published wrong"),
    ("m-kindacc", 0x267AD8, b"\xd8\x01\x00\x00",
     "kind-count +0x1D0 -> +0x1D8: counts land in prefix row"),
    ("m-tab8",    0x267AFA, b"\x10",
     "table-A slot +8 -> +0x10: entries shift one slot"),
    # NOTE: `and cl,0xE0` at 0x267B00 is unobservable — its write to
    # rec+3 is always overwritten by the second store in the same
    # iteration; no final-state mutation of the mask can diverge.
    ("m-pk-seq",  0x267AEB, b"\x0f",
     "seq mask 0x1F -> 0x0F: group index truncated"),
    ("m-pk-kind", 0x267B10, b"\x04",
     "kind shl 5 -> 4: packed byte halves the kind"),
    ("m-rstride", 0x267B20, b"\xe0",
     "record stride mask 0xF0 -> 0xE0: records misalign"),
    ("m-grp-lp",  0x267B38, b"\x7d",
     "outer jl -> jge: group loop never runs"),
    ("m-init-lp", 0x267B82, b"\x7d",
     "init jl -> jge: per-record init never runs"),
    ("m-pfx8",    0x267B55, b"\x0a",
     "prefix word +8 -> +0xA: prefix row lands wrong"),
    ("m-lea-b",   0x267ABF, b"\x70\x48\xba\x01",
     "loop2 table 0x1E0C318 -> +0x10: wrong rows"),
    # RMAP dispatch
    ("m-rm-mask", 0x266ADB, b"\x0f",
     "seq mask 0x1F -> 0x0F: high groups alias low"),
    ("m-rm-bnd",  0x266ADE, b"\x06",
     "dispatch bound 7 -> 6: group 7 refused"),
    ("m-rm-ja",   0x266AE0, b"\x82",
     "ja -> jb: every in-range group falls through"),
    ("m-rm-a0",   0x266B7D, b"\xb0\x00\x00\x00",
     "+0xA0 write -> +0xB0: pointer lands wrong"),
    ("m-rm-sub",  0x266B8B, b"\x02",
     "sub-flag cmp 1 -> 2: addend selection inverts"),
    ("m-rm-c8",   0x266B8E, b"\xc0\x00\x00\x00",
     "addend 0xC8 -> 0xC0: sub-flagged row short by 8"),
    ("m-rm-a8",   0x266B9F, b"\xb0\x00\x00\x00",
     "+0xA8 write -> +0xB0: pointer lands wrong"),
    ("m-rm-230",  0x266B64, b"\x20\x02\x00\x00",
     "arm5-7 +0x230 -> +0x220: c0/a0 shift"),
    # NOTE: the sub-flag seq mask `and eax,0x1F` at 0x266B82 is equivalent
    # under the dispatch — only seq<=7 reaches it, where bit4 is already 0.
]


def main():
    raw, secs = load_image()
    out = {"exe_sha256": SHA, "cases": [], "mutants": []}
    npass = nfail = 0
    results = {}
    cases = build_cases()
    for case in cases:
        tr, faults, w, obs = run_case(case, raw, secs)
        exp_tr, exp_obs = model(case, raw, secs)
        total = exp_obs.pop("_total", None)
        mem_faults = [f for f in faults if f[0] == "MEM"]
        ok = bool(tr == exp_tr and not mem_faults and obs == exp_obs)
        if not ok and obs.get("ret") == exp_obs.get("ret"):
            # find the first differing key for the report
            for k in sorted(set(obs) | set(exp_obs)):
                if obs.get(k) != exp_obs.get(k):
                    print("DIFF %s key=%s got=%s want=%s"
                          % (case["name"], k, obs.get(k), exp_obs.get(k)))
        npass += ok
        nfail += (not ok)
        results[case["name"]] = (tr, obs, bool(mem_faults))
        if not ok:
            print("FAIL %s\n  got:  %s ret=%x fault=%s\n  want: %s ret=%x"
                  % (case["name"], tr, obs["ret"], mem_faults,
                     exp_tr, exp_obs["ret"]))
        else:
            print("PASS %s" % case["name"])
        out["cases"].append({"name": case["name"], "trace": tr,
                             "ok": bool(ok), "obs": obs,
                             "exp_trace": exp_tr, "faults": faults})
    print("cases: %d/%d" % (npass, npass + nfail))

    base = {c["name"]: results[c["name"]] for c in cases}
    for name, va, data, why in MUTANTS:
        n_diff, diffs = 0, []
        for case in cases:
            c = dict(case)
            c["patch_bytes"] = [(va, data)]
            tr, faults, w, obs = run_case(c, raw, secs)
            mem = bool([f for f in faults if f[0] == "MEM"])
            if (tr, obs, mem) != base[case["name"]]:
                n_diff += 1
                diffs.append((case["name"], "tr=%s ret=%x" % (tr, obs["ret"])))
        killed = n_diff > 0
        print(("KILL " if killed else "SURV") + " %s  (%d divergent) %s"
              % (name, n_diff, why))
        out["mutants"].append({"name": name, "va": "0x%X" % va,
                               "killed": killed, "divergent": n_diff,
                               "why": why, "sample": diffs[:3]})
    json.dump(out, open("result.json", "w"), indent=1,
              default=lambda o: o.hex() if isinstance(o, bytes) else str(o))
    return 0 if nfail == 0 and all(m["killed"] for m in out["mutants"]) else 1


if __name__ == "__main__":
    sys.exit(main())
