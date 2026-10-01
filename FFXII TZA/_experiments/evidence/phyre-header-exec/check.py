# EXP-094 - phyre PClusterHeader loader execution
#
# CONTRACT-phyre-cluster-header-load.md scripted the stream read, the
# descriptor-driven header swap, and the namespace byte-swap callees of
# 0059A3B0. This harness re-drives the loader ladder from shipped bytes:
#
#   ENTRY BODY (shipped bytes, canonical VA):
#     0059A3B0  59A3B0(stream=rcx, hdrbuf=rdx, nsRec=r8 {+0 cap|bit31,
#                +8 buf}, gvec=r9 {+0 size|bit31, +8 buf},
#                arg5=swapFlagOut byte*, arg6=outLen dword*)
#
#   STATIC INIT (real):
#     00160210  CRT init: constructs descriptor 0x2CAA0A0 via 00597690
#     00597690  PClusterHeader PClassDescriptorConcrete ctor
#     00632D80  descriptor record init (vtbl/name/size 0x54/lists)
#     006373D0  TLS ctx getter: gs:[0x58] -> slot array, idx [0x2EAED3C],
#               ctx+4 vs lazy-state [0x2CF94EC] -> returns 0x1F2E330
#     0063DC80/0063DF90/0063DFA0  member quick-slot stores (+0xC0/C8/D0)
#
#   LOADER (real):
#     0059A3B0  read 0x54 hdr via stream vtbl+0x28; marker 0x50485952;
#               on mismatch 0063E2E0(&0x2CAA0A0, buf, 1) then retest;
#               id checks vs 00686D00 (0x44583131 @+0xC) / 0069E780
#               (0x424C4C54 @+0x44) when swapped flag set; nsRec realloc
#               via 0017D260/00584730; outLen=[hdr+4] paths (==0x54 direct
#               nsread; >0x54 grow gvec + read ext; <0x54 memcpy tail into
#               nsbuf via 00861EBA IAT + partial read); 0059A6F0 ns read.
#     0063E2E0  descriptor swap walk: cursor {+0 acc,+4 descsize,+8 buf,
#               +0x10 flag}; r8b!=0 -> forward over desc+0x80 list,
#               r8b==0 -> reverse over desc+0x88; per node calls 0063CE80;
#               then recurses parent chain desc+0x78.
#     0063CE80  member dispatch: node vtbl+8 -> declType (kind [x+0x5C]);
#               flags node+0x28 bit1 skip / bit6 strong; dest =
#               buf + (node+0x48 - [node+0x18]->+0xF4); resolver node+0x50
#               else typeObj node+0x30; then 0059FDB0.
#     0059FDB0  per-element engine: stride [typeObj+0x38], count r8d,
#               calls [typeObj vtbl+0](typeObj, addr, flagByte) per element,
#               ORs results.
#     0059A6F0  ns read: stream+0x28 len bytes into buf; +0x18 accounting;
#               ret 9 short, 0 ok; if flag && buf -> 0059C180.
#     0059C180  ns swap: bswap 8 fixed dwords +0x00..0x1C; N1=[ns+8]
#               tail dword table at ns+0x20 via 0059A8B0; N2=[ns+0xC]
#               0x24-byte records at ns+4*(N1+8) via 0059A780; N3=[ns+0x10]
#               0x18-byte records at ns+4*(N2*9+N1+8) inlined bswap x6.
#     0059A780  0x24-record swap (9 dwords; manual-bswap forms == bswap)
#     0059A8B0  SSE2 dword-table bswap (2x16B/iter, scalar tail)
#     0067B100  gvec grow: 0017D260(size,1) + 005847730 free + store
#     00686D00 / 0069E780  id constants 0x44583131 / 0x424C4C54
#     00584730  free thunk (test rcx; jne 0x19C570)
#
#   STUBBED BOUNDARIES (disclosed; patched ret + hooked):
#     0x19C580  deep allocator (0017D260 tail target) -> fixture bump alloc
#     0x19C570  deep free -> logged, ret
#     0x808B90  atexit registration -> ret
#     0x8092FC  lazy-init header -> ret (state planted so it is unreached)
#     0x80929C  lazy-init footer -> ret
#
#   FIXTURE (disclosed):
#     stream vtbl slot+0x28 read: min(len,remaining) copy + cursor advance
#     member nodes spliced into the REAL desc+0x80 list built by the real
#       ctor (deferred member-finalize machinery is out of package scope)
#     member type objects + vtbl slot-0 swap leaf (manual dword bswap that
#       also logs (addr,flag) into LEAFLOG) - the per-type transform is the
#       boundary; the WALK and dispatch are shipped bytes.
#     memcpy IAT slot [0x8C2A68] -> fixture rep-movsb memcpy.
#
#   KEY GLOBALS: [0x1F44830] cookie, [0x2EAED3C] TLS index,
#     [0x2CF94EC] lazy-state (planted 0 -> direct return), gs:[0x58] ->
#     slot array -> [3] -> ctx, [ctx+4]=count.
#
# Memory: GuestMem host buffers via mem_map_ptr (EXP-087 finding: this
# host's unicorn DLLs intermittently fail uc_mem_write on mapped pages).

import ctypes, hashlib, json, struct, sys, os
from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000
IMG_LO, IMG_HI = 0x120000, 0x3000000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000
TLS    = 0x60000000

# fixture blocks
STREAM  = HEAP + 0x000000    # {+0 vtbl, +0x18 bytecount, +0x20 cursor,
                             #  +0x28 remaining}
STREAMVT= HEAP + 0x010000    # vtbl: +0x28 = read fn
DATA    = HEAP + 0x020000    # serialized input
HDRBUF  = HEAP + 0x040000    # 0x54-byte header buf
NSREC   = HEAP + 0x050000    # {+0 cap|bit31, +8 buf}
GVEC    = HEAP + 0x051000    # {+0 size|bit31, +8 buf}
FLAGB   = HEAP + 0x052000    # swapFlag out byte
OUTL    = HEAP + 0x052008    # outLen dword
CDESC   = HEAP + 0x053000    # member class-desc stub (+0xF4 = 0)
MNODE   = HEAP + 0x060000    # member nodes, stride 0x80
NODEVT  = HEAP + 0x070000    # node vtbls (+8 = getType leaf)
TOBJ    = HEAP + 0x080000    # type objs, stride 0x80
TVTBL   = HEAP + 0x090000    # type vtbls (+0 = swap leaf)
LEAFLOG = HEAP + 0x0A0000    # (addr,flag) pairs appended by swap leaf
ARENA   = HEAP + 0x0B0000    # bump arena for alloc stub
CODE    = HEAP + 0x0F8000    # fixture routines

LOADER  = 0x59A3B0
INIT    = 0x160210

# real bodies, entry-hooked for the trace manifest
CALLS = {
    0x59A3B0: "loader",     0x63E2E0: "descswap",  0x63CE80: "memnode",
    0x59FDB0: "swengine",   0x59A6F0: "nsread",    0x59C180: "nsswap",
    0x59A780: "nsrec24",    0x59A8B0: "nsdwtab",   0x686D00: "id1",
    0x69E780: "id2",        0x67B100: "vgrow",     0x584730: "free_t",
    0x17D260: "alloc_t",    0x160210: "init",      0x597690: "ctor",
    0x632D80: "dinit",      0x6373D0: "tlsctx",    0x63DC80: "mslot0",
    0x63DF90: "mslot1",     0x63DFA0: "mslot2",    0x861EBA: "memcpy_t",
}

# disclosed boundaries: patched ret, hooked
STUBS = {
    0x19C580: "alloc",
    0x19C570: "free",
    0x808B90: "atexit",
    0x8092FC: "lazy_init",
    0x80929C: "lazy_done",
}

G_COOKIE  = 0x1F44830
G_TLSIDX  = 0x2EAED3C    # dword tls index for 6373D0
G_LAZYST  = 0x2CF94EC    # lazy-state dword for 6373D0
CTXOBJ    = 0x1F2E330    # returned ctx object (its real image contents)
DESC      = 0x2CAA0A0    # PClusterHeader descriptor (built by real ctor)
IAT_MEMCPY= 0x8C2A68

MARKER  = 0x50485952
ID1     = 0x44583131
ID2     = 0x424C4C54

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def db(v): return struct.pack("<B", v & 0xFF)
def bs(v): return struct.unpack(">I", struct.pack("<I", v & 0xFFFFFFFF))[0]

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

# ---- fixture routines (assembled, disclosed) --------------------------------
# CODE+0x00  stream read: rcx=stream, rdx=buf, r8=len -> rax=n
#   n = min(len, [stream+0x28]); copy [stream+0x20]->buf; cursor+=n; rem-=n
READ_FN = bytes.fromhex(
    "56"                # push rsi
    "57"                # push rdi
    "4c8b4920"          # mov r9, [rcx+0x20]     cursor
    "4c8b5128"          # mov r10,[rcx+0x28]     remaining
    "4c89c0"            # mov rax, r8
    "4c39d0"            # cmp rax, r10
    "490f47c2"          # cmova rax, r10         n = min
    "48014120"          # add [rcx+0x20], rax
    "48294128"          # sub [rcx+0x28], rax
    "4c89ce"            # mov rsi, r9
    "4889d7"            # mov rdi, rdx
    "4889c1"            # mov rcx, rax
    "f3a4"              # rep movsb
    "5f"                # pop rdi
    "5e"                # pop rsi
    "c3")
# CODE+0x40  memcpy: rcx=dst, rdx=src, r8=len -> rax=dst
MEMCPY_FN = bytes.fromhex(
    "56"                # push rsi
    "57"                # push rdi
    "4889c8"            # mov rax, rcx
    "4889d6"            # mov rsi, rdx
    "4889cf"            # mov rdi, rcx
    "4c89c1"            # mov rcx, r8
    "f3a4"              # rep movsb
    "5f"                # pop rdi
    "5e"                # pop rsi
    "c3")
# CODE+0x60  type swap leaf: rcx=typeObj, rdx=addr, r8=flag -> al=1
#   appends (rdx,r8) to LEAFLOG via shared cursor cell LEAFLOG+0x8000,
#   then bswaps [rdx]
SWAP_FN = (b"\x48\xb8" + qw(LEAFLOG + 0x8000) +   # movabs rax, &cursor
           bytes.fromhex(
    "4c8b08"            # mov r9, [rax]          cursor
    "498911"            # mov [r9], rdx          record addr
    "4d894108"          # mov [r9+8], r8         record flag
    "4983c110"          # add r9, 0x10
    "4c8908"            # mov [rax], r9          store cursor
    "8b02"              # mov eax, [rdx]
    "0fc8"              # bswap eax
    "8902"              # mov [rdx], eax
    "b001"              # mov al, 1
    "c3"))
# CODE+0x90  node getType leaf: rcx=node -> rax=0 (declType null)
GETTYPE_FN = bytes.fromhex("31c0c3")
# CODE+0xA0  ready leaf: -> al=1  (stream vtbl+0x10, used by callers of loader)
READY_FN = bytes.fromhex("b001c3")


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        img += b"\x00" * ((-len(img)) & 0xFFF)
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x1000000), (STACK, 0x100000),
                     (RETQ, 0x1000), (TLS, 0x10000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")

        # fixture routines
        gm.w(CODE, READ_FN)
        gm.w(CODE + 0x40, MEMCPY_FN)
        gm.w(CODE + 0x60, SWAP_FN)
        gm.w(CODE + 0x90, GETTYPE_FN)
        gm.w(CODE + 0xA0, READY_FN)

        # TLS: gs base = TLS; gs:[0x58] = slot array ptr (TLS+0x1000);
        # slot[idx=3] = ctx (TLS+0x8000); ctx+4 = count 4; lazy-state = 0
        self.uc.reg_write(UC_X86_REG_GS_BASE, TLS)
        gm.w(TLS + 0x58, qw(TLS + 0x1000))
        gm.w(G_TLSIDX, dw(3))
        gm.w(TLS + 0x1000 + 3 * 8, qw(TLS + 0x8000))
        gm.w(TLS + 0x8000 + 4, dw(4))
        gm.w(G_LAZYST, dw(0))
        gm.w(G_COOKIE, qw(0x0000DEADBEEF))

        # IAT: memcpy slot -> fixture memcpy
        gm.w(IAT_MEMCPY, qw(CODE + 0x40))

        # stream object
        gm.w(STREAM + 0x00, qw(STREAMVT))
        gm.w(STREAMVT + 0x10, qw(CODE + 0xA0))   # ready check
        gm.w(STREAMVT + 0x28, qw(CODE + 0x00))   # read
        gm.w(STREAM + 0x18, dw(0))               # byte count (real field)
        gm.w(STREAM + 0x20, qw(DATA))            # cursor
        data = case.get("data", b"")
        gm.w(DATA, data)
        gm.w(STREAM + 0x28, qw(case.get("avail", len(data))))  # remaining

        # out params / records
        gm.w(NSREC + 0, dw(case.get("nscap", 0)))
        gm.w(NSREC + 8, qw(case.get("nsbuf", 0)))
        gm.w(GVEC + 0, dw(case.get("gvec_size", 0)))
        gm.w(GVEC + 8, qw(case.get("gvec_buf", 0)))
        gm.w(FLAGB, b"\xAA")                     # poison
        gm.w(OUTL, dw(0xDEADBEEF))               # poison
        gm.w(LEAFLOG + 0x8000, qw(LEAFLOG))      # swap-leaf log cursor

        # mutants
        for va, pdata in case.get("patch", []):
            gm.w(va, pdata)

        # stubs patched to ret
        for va in STUBS:
            gm.w(va, b"\xc3")

        self.trace, self.faults = [], []
        self.bump = ARENA
        self.allocs, self.frees = [], []
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in CALLS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)
        for va in STUBS:
            uc.hook_add(UC_HOOK_CODE, self.on_stub, begin=va, end=va)

    def on_call(self, uc, addr, size, _):
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        r8  = uc.reg_read(UC_X86_REG_R8)  & 0xFFFFFFFFFFFFFFFF
        r9  = uc.reg_read(UC_X86_REG_R9)  & 0xFFFFFFFFFFFFFFFF
        self.trace.append((CALLS[addr], "rcx=%x" % rcx, "rdx=%x" % rdx,
                           "r8=%x" % r8, "r9=%x" % r9))

    def on_stub(self, uc, addr, size, _):
        name = STUBS[addr]
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        self.trace.append(("STUB", name, "rcx=%x" % rcx, "rdx=%x" % rdx))
        if name == "alloc":
            # bump arena, aligned to rdx (align arg); rcx = size
            align = max(rdx, 1)
            p = (self.bump + align - 1) & ~(align - 1)
            self.bump = p + rcx
            self.allocs.append((rcx, p))
            uc.reg_write(UC_X86_REG_RAX, p)
        elif name == "free":
            self.frees.append(rcx)
            uc.reg_write(UC_X86_REG_RAX, 0)
        else:
            uc.reg_write(UC_X86_REG_RAX, 0)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False

    def run_init(self):
        """Run 00160210 real: constructs descriptor 0x2CAA0A0."""
        uc, gm = self.uc, self.gm
        sp = STACK + 0x80000
        gm.w(sp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, sp)
        uc.emu_start(INIT, RETQ, count=5_000_000)
        uc.reg_write(UC_X86_REG_RAX, 0)

    def plant_members(self, specs, desc=DESC, mbase=MNODE):
        """Splice fixture member nodes into a descriptor's +0x80 list.
        Each spec: {"off": memberOffset, "stride": typeStride(4)}.
        Node layout per 0063CE80: +0 nodeVtbl, +8 fwd, +0x10 back,
        +0x18 classDesc(+0xF4 baseoff=0), +0x28 flags, +0x30 typeObj,
        +0x48 member offset, +0x50 resolver(0)."""
        gm = self.gm
        n = len(specs)
        head = desc + 0x80
        idx0 = (mbase - MNODE) // 0x80
        nodes = [mbase + i * 0x80 for i in range(n)]
        for i, spec in enumerate(specs):
            j = idx0 + i
            node = nodes[i]
            tobj = TOBJ + j * 0x80
            tvt  = TVTBL + j * 0x40
            nvt  = NODEVT + j * 0x40
            fwd = (nodes[i + 1] + 8) if i + 1 < n else head
            bak = (nodes[i - 1] + 8) if i > 0 else head
            gm.w(nvt + 8, qw(CODE + 0x90))        # getType -> 0
            gm.w(tvt + 0, qw(CODE + 0x60))        # swap leaf
            gm.w(tobj + 0x00, qw(tvt))
            gm.w(tobj + 0x38, dw(spec.get("stride", 4)))
            gm.w(node + 0x00, qw(nvt))
            gm.w(node + 0x08, qw(fwd))
            gm.w(node + 0x10, qw(bak))
            gm.w(node + 0x18, qw(CDESC))
            gm.w(node + 0x28, dw(spec.get("flags", 0)))
            gm.w(node + 0x30, qw(tobj))
            gm.w(node + 0x48, dw(spec["off"]))
            gm.w(node + 0x50, qw(0))
        gm.w(head + 0, qw(nodes[0] + 8))
        gm.w(head + 8, qw(nodes[-1] + 8))


def build(case, raw, secs):
    w = World(case, raw, secs)
    w.run_init()
    if "members" in case:
        w.plant_members(case["members"])
    if "parent_members" in case:
        w.plant_members(case["parent_members"], desc=0x2CA9DA0,
                        mbase=MNODE + 0x8000)
    return w


def case_get(w, key, default):
    return w.case.get(key, default)


def invoke_loader(w):
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))             # [rsp] = return address
    gm.w(sp + 0x28, qw(FLAGB))     # arg5 swapFlag out (caller rsp+0x20)
    gm.w(sp + 0x30, qw(OUTL))      # arg6 outLen      (caller rsp+0x28)
    gm.w(sp + 0x38, qw(case_get(w, "arg7", 1)))  # arg7 id-check gate
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, STREAM)
    uc.reg_write(UC_X86_REG_RDX, HDRBUF)
    uc.reg_write(UC_X86_REG_R8, NSREC)
    uc.reg_write(UC_X86_REG_R9, GVEC)
    try:
        uc.emu_start(LOADER, RETQ, count=16_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    return uc.reg_read(UC_X86_REG_RAX)


def invoke_descswap(w, flag):
    """Direct 0063E2E0(desc, HDRBUF, flag) for walk-order cases."""
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, DESC)
    uc.reg_write(UC_X86_REG_RDX, HDRBUF)
    uc.reg_write(UC_X86_REG_R8, flag)
    uc.emu_start(0x63E2E0, RETQ, count=1_000_000)


def expect(name, snap, cond, why):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name + ("  -- " + why if not ok else ""))
    return ok

def rd8(a, gm):  return gm.r(a, 1)[0]
def rd32(a, gm): return struct.unpack("<I", gm.r(a, 4))[0]
def rd64(a, gm): return struct.unpack("<Q", gm.r(a, 8))[0]

# ---- header / stream builders ------------------------------------------------
def hdr_le(ns_len=0x40, out_len=0x54, id1=ID1, id2=ID2):
    b = bytearray(0x54)
    struct.pack_into("<I", b, 0, MARKER)
    struct.pack_into("<I", b, 4, out_len)
    struct.pack_into("<I", b, 8, ns_len)
    struct.pack_into("<I", b, 0x0C, id1)
    struct.pack_into("<I", b, 0x44, id2)
    return bytes(b)

def hdr_be(ns_len=0x40, out_len=0x54, id1=ID1, id2=ID2, extra=None):
    """Header with the member-covered dwords pre-byteswapped (as the wire
    would carry them for the opposite-endian variant). Fields not covered
    by planted members stay as authored."""
    b = bytearray(0x54)
    struct.pack_into("<I", b, 0, bs(MARKER))
    struct.pack_into("<I", b, 4, bs(out_len))
    struct.pack_into("<I", b, 8, bs(ns_len))
    struct.pack_into("<I", b, 0x0C, bs(id1))
    struct.pack_into("<I", b, 0x44, bs(id2))
    if extra:
        for off, v in extra.items():
            struct.pack_into("<I", b, off, v)
    return bytes(b)

def ns_block(n1, n2, n3, fill=0x11):
    """Namespace buffer: 8 fixed dwords + N1 dword table + N2 0x24 records
    + N3 0x18 records. Returns (bytes, layout dict)."""
    n = 0x20 + 4 * n1 + 0x24 * n2 + 0x18 * n3
    b = bytearray(n)
    struct.pack_into("<I", b, 8, n1)
    struct.pack_into("<I", b, 0x0C, n2)
    struct.pack_into("<I", b, 0x10, n3)
    for i in range(n // 4):
        if i in (2, 3, 4):
            continue
        struct.pack_into("<I", b, i * 4, 0x10000000 + fill * 0x100 + i)
    return bytes(b), {"n1": n1, "n2": n2, "n3": n3, "size": n}

def ns_block_be(n1, n2, n3, fill=0x11):
    """Same, but every dword byteswapped (as the wire carries it)."""
    raw_b, lay = ns_block(n1, n2, n3, fill)
    b = bytearray(raw_b)
    for i in range(len(b) // 4):
        struct.pack_into("<I", b, i * 4, bs(struct.unpack_from("<I", raw_b, i * 4)[0]))
    return bytes(b), lay

# members covering the loader-inspected fields: marker,size,nslen,id1,id2
MEMBERS5 = [{"off": 0}, {"off": 4}, {"off": 8}, {"off": 0x0C}, {"off": 0x44}]

def leafhits(s):
    """Ordered (addr,flag) list the swap leaf recorded."""
    out = []
    for i in range(64):
        a = rd64(LEAFLOG + i * 0x10, s["gm"])
        if a == 0:
            break
        f = rd64(LEAFLOG + i * 0x10 + 8, s["gm"])
        out.append((a, f))
    return out

def build_cases():
    C = []
    A = C.append

    # -- ctor sanity: real 00160210 built the descriptor
    A({"name": "ctor-real", "data": b"", "skip_loader": True,
       "check": lambda s: s["d_vtbl"] == 0xD249A8 and s["d_size"] == 0x54 and
                          s["d_m0"] == 0x2CA9C00 and s["d_m1"] == 0x2CA9C60 and
                          s["d_m2"] == 0x2CA9CC0 and s["d_flag"] == 0 and
                          s["d_l80"] == DESC + 0x80 and s["d_parent"] == 0x2CA9DA0})

    # -- LE plain load: marker ok, ns read through real 59A6F0
    A({"name": "le-basic", "data": hdr_le(0x40) + bytes(0x40),
       "check": lambda s: s["ret"] == 0 and s["flag"] == 0 and
                          s["outl"] == 0x54 and s["scount"] == 0x54 + 0x40 and
                          s["nsbuf"] != 0 and s["nscap"] == 0x40})

    # -- short header read -> 9
    A({"name": "short-hdr", "data": hdr_le(0)[:0x30],
       "check": lambda s: s["ret"] == 9 and s["scount"] == 0x30})

    # -- bad marker, empty member list -> swap walk no-op -> retest fail -> 6
    A({"name": "bad-marker-nomem", "data": b"XXXX" + hdr_le(0)[4:],
       "check": lambda s: s["ret"] == 6 and trhas(s, "descswap") and
                          s["leaf_n"] == 0})

    # -- BE header: planted members bswap the inspected fields -> accept
    A({"name": "be-basic", "data": hdr_be(0x40) + bytes(0x40),
       "members": MEMBERS5,
       "check": lambda s: s["ret"] == 0 and s["flag"] == 1 and
                          s["outl"] == 0x54 and s["leaf_n"] == 5 and
                          s["scount"] == 0x54 + 0x40})

    # -- BE but member list does not cover +0 -> marker stays bad -> 6
    A({"name": "be-marker-uncovered", "data": hdr_be(0) + bytes(0),
       "members": [{"off": 4}, {"off": 8}, {"off": 0x0C}, {"off": 0x44}],
       "check": lambda s: s["ret"] == 6 and s["leaf_n"] == 4})

    # -- BE, marker recovers, id1 wrong -> 6
    A({"name": "be-badid1", "data": hdr_be(0x40, id1=0xDEADBEEF) + bytes(0x40),
       "members": MEMBERS5,
       "check": lambda s: s["ret"] == 6})

    # -- BE, id2 nonzero wrong -> 6
    A({"name": "be-badid2", "data": hdr_be(0x40, id2=0xDEADBEEF) + bytes(0x40),
       "members": MEMBERS5,
       "check": lambda s: s["ret"] == 6})

    # -- BE, id2==0 allowed
    A({"name": "be-id2zero", "data": hdr_be(0x40, id2=0) + bytes(0x40),
       "members": MEMBERS5,
       "check": lambda s: s["ret"] == 0})

    # -- ns short read -> 9 (read attempted, partial swapped)
    A({"name": "ns-short", "data": hdr_le(0x40) + bytes(0x20),
       "check": lambda s: s["ret"] == 9 and s["scount"] == 0x54 + 0x20})

    # -- null nsbuf is a hard error (6) even when ns len is 0:
    #    59A4D3 test r13,r13 -> 0x59A598 ret 6
    A({"name": "ns-nullbuf", "data": hdr_le(0),
       "check": lambda s: s["ret"] == 6})

    # -- ns len 0, buf planted: no stream read for ns, no swap
    A({"name": "ns-zero", "data": hdr_le(0), "nsbuf": ARENA,
       "check": lambda s: s["ret"] == 0 and s["scount"] == 0x54 and
                          s["nsbuf"] == ARENA and trabsent(s, "nsswap")})

    # -- arg7=0 (id-check gate clear): wrong ids are tolerated
    A({"name": "arg7-skip-ids", "data": hdr_le(0, id1=0xDEADBEEF,
                                              id2=0xCAFEBABE),
       "nsbuf": ARENA, "arg7": 0,
       "check": lambda s: s["ret"] == 0})

    # -- arg7=1 (real caller sets it): wrong id1 on an LE header -> 6
    A({"name": "le-badid1", "data": hdr_le(0, id1=0xDEADBEEF),
       "nsbuf": ARENA,
       "check": lambda s: s["ret"] == 6})

    # -- ns realloc: cap mismatch -> alloc stub, old buf freed
    A({"name": "ns-realloc", "data": hdr_le(0x40) + bytes(0x40),
       "nscap": 0x20, "nsbuf": ARENA + 0x8000,
       "check": lambda s: s["ret"] == 0 and s["nscap"] == 0x40 and
                          s["nsbuf"] != ARENA + 0x8000 and
                          len(s["allocs"]) == 1 and
                          ARENA + 0x8000 in s["frees"]})

    # -- ns cap equal -> no alloc
    A({"name": "ns-cap-eq", "data": hdr_le(0x40) + bytes(0x40),
       "nscap": 0x40, "nsbuf": ARENA + 0x8000,
       "check": lambda s: s["ret"] == 0 and s["nsbuf"] == ARENA + 0x8000 and
                          len(s["allocs"]) == 0})

    # -- real ns swap: BE header+ns, verify 59C180 regions in place
    nsbe, _lay = ns_block_be(2, 1, 1)
    nsle, _ = ns_block(2, 1, 1)
    A({"name": "ns-swap-full", "data": hdr_be(len(nsle)) + nsbe,
       "members": MEMBERS5,
       "check": lambda s: s["ret"] == 0 and s["nsbytes"] == nsle and
                          trhas(s, "nsswap", "nsrec24", "nsdwtab")})

    # -- LE ns: no swap (flag=0 -> 59C180 not called)
    A({"name": "ns-le-noswap", "data": hdr_le(len(nsle)) + nsle,
       "check": lambda s: s["ret"] == 0 and s["nsbytes"] == nsle and
                          trabsent(s, "nsswap")})

    # -- extended header: outLen > 0x54 -> gvec grows, tail read from stream
    A({"name": "hdr-ext-big", "data": hdr_le(0x20, out_len=0x60) +
        bytes(0xC) + bytes(0x20),
       "check": lambda s: s["ret"] == 0 and trhas(s, "vgrow") and
                          s["gvec_buf"] != 0})

    # -- extended header BE: swapped flag + outLen!=0x54 -> second 63E2E0
    #    pass re-swaps the header before the ext-tail read
    A({"name": "be-ext", "data": hdr_be(0x20, out_len=0x60) +
        bytes(0xC) + bytes(0x20), "members": MEMBERS5,
       "check": lambda s: s["ret"] == 0 and s["leaf_n"] == 10 and
                          trhas(s, "vgrow")})

    # -- short header: outLen < 0x54 -> tail memcpy'd into nsbuf, rest read
    A({"name": "hdr-ext-small", "data": hdr_le(0x30, out_len=0x40) +
        bytes(0x30),
       "check": lambda s: s["ret"] == 0 and trhas(s, "memcpy_t")})

    # -- direct 63E2E0 walk order: flag=1 forward, flag=0 reverse
    A({"name": "walk-fwd", "data": b"", "members":
       [{"off": 0x10}, {"off": 0x20}, {"off": 0x30}],
       "direct_swap": 1,
       "check": lambda s: s["leafhits"] ==
                          [(HDRBUF + 0x10, 1), (HDRBUF + 0x20, 1),
                           (HDRBUF + 0x30, 1)]})
    A({"name": "walk-rev", "data": b"", "members":
       [{"off": 0x10}, {"off": 0x20}, {"off": 0x30}],
       "direct_swap": 0,
       "check": lambda s: s["leafhits"] ==
                          [(HDRBUF + 0x30, 0), (HDRBUF + 0x20, 0),
                           (HDRBUF + 0x10, 0)]})

    # -- member flag bit1 skips the member (real 63CE80 test al,al)
    A({"name": "walk-skipbit", "data": b"", "members":
       [{"off": 0x10}, {"off": 0x20, "flags": 2}, {"off": 0x30}],
       "direct_swap": 1,
       "check": lambda s: [a for a, f in s["leafhits"]] ==
                          [HDRBUF + 0x10, HDRBUF + 0x30]})

    # -- parent chain: own list first, then desc+0x78 (0x2CA9DA0) members
    A({"name": "walk-parent", "data": b"",
       "members": [{"off": 0x10}],
       "parent_members": [{"off": 0x20}, {"off": 0x24}],
       "direct_swap": 1,
       "check": lambda s: [a for a, f in s["leafhits"]] ==
                          [HDRBUF + 0x10, HDRBUF + 0x20, HDRBUF + 0x24]})

    # ======== mutants =========================================================
    M = []
    B = M.append
    # marker compare imm at 0x59A3FF and the post-swap retest at 0x59A419
    # (cmp dword [rsi], 0x50485952 = 81 3E imm32): imm @ +2
    B({"name": "mut-marker", "patch": [(0x59A401, dw(0x50485953)),
                                      (0x59A41B, dw(0x50485953))],
       "case": {"data": hdr_le(0)},
       "check": lambda s: s["ret"] == 6})
    # header size ebp=0x54 at 0x59A3C6 (mov ebp,0x54: imm @ +1): read asks
    # 0x55, stream only has 0x54 -> short -> ret = ebp-0x4B = 0xA
    B({"name": "mut-hdrsize", "patch": [(0x59A3C7, dw(0x55))],
       "case": {"data": hdr_le(0)},
       "check": lambda s: s["ret"] == 0xA})
    # stream+0x18 accounting nop'd: add [r14+0x18],eax @0x59A3DA (4B) and
    # add [rbx+0x18],eax @0x59A726 in 59A6F0 (3B)
    B({"name": "mut-acct", "patch": [(0x59A3DA, b"\x90" * 4),
                                    (0x59A726, b"\x90" * 3)],
       "case": {"data": hdr_le(0), "nsbuf": ARENA},
       "check": lambda s: s["ret"] == 0 and s["scount"] == 0})
    # swapped flag forced set: movzx edi,byte[rsp+0x80] @0x59A445 (8B) ->
    # mov edi,1 -> id checks run on an LE header -> wrong id2 fails
    B({"name": "mut-idgate", "patch": [(0x59A445,
                                       b"\xbf\x01\x00\x00\x00\x90\x90\x90")],
       "case": {"data": hdr_le(0x40, id2=0xDEADBEEF) + bytes(0x40)},
       "check": lambda s: s["ret"] == 6})
    # walk direction: je 0x63E370 @0x63E30E (74 60) -> eb: flag=1 takes the
    # reverse arm -> member order flips
    B({"name": "mut-dir", "patch": [(0x63E30E, b"\xeb")],
       "case": {"data": b"", "direct_swap": 1,
                "members": [{"off": 0x10}, {"off": 0x20}, {"off": 0x30}]},
       "check": lambda s: [a for a, f in s["leafhits"]] ==
                          [HDRBUF + 0x30, HDRBUF + 0x20, HDRBUF + 0x10]})
    # ns fixed-dword swap killed: bswap eax @0x59C18B (0F C8) -> 66 90
    B({"name": "mut-nsbswap", "patch": [(0x59C18B, b"\x66\x90")],
       "case": {"data": hdr_be(len(nsle)) + nsbe, "members": MEMBERS5},
       "check": lambda s: s["nsbytes"] != nsle})
    # per-element dispatch killed: mov r9,[rsi] @0x59FDE0 (4C 8B 0E) ->
    # mov r9,[rsi+8] (typeObj+8 = 0) -> call [0] fault, no leaf hits
    B({"name": "mut-vtbl", "patch": [(0x59FDE0, b"\x4c\x8b\x4e\x08")],
       "case": {"data": b"", "direct_swap": 1,
                "members": [{"off": 0x10}]},
       "check": lambda s: s["leaf_n"] == 0})
    # member-skip flag dword: [rdx+0x28] -> [rdx+0x2C] in 63CE80
    # (8B 5A 28 @0x63CE99, disp @ +2 = 0x63CE9B)
    B({"name": "mut-skipoff", "patch": [(0x63CE9B, b"\x2c")],
       "case": {"data": b"", "direct_swap": 1,
                "members": [{"off": 0x10}, {"off": 0x20, "flags": 2}]},
       "check": lambda s: [a for a, f in s["leafhits"]] ==
                          [HDRBUF + 0x10, HDRBUF + 0x20]})
    # short-read compare: cmp eax,esi @0x59A72B (3B C6) -> cmp eax,eax ->
    # cmove always yields success -> short ns read returns 0
    B({"name": "mut-nsshort", "patch": [(0x59A72B, b"\x3b\xc0")],
       "case": {"data": hdr_le(0x40) + bytes(0x20)},
       "check": lambda s: s["ret"] == 0})
    # parent-chain recursion killed: jne 0x63E310 @0x63E358 (75 B6) ->
    # 90 90: parent descriptor's member list never walked
    B({"name": "mut-parent", "patch": [(0x63E358, b"\x90\x90")],
       "case": {"data": b"", "direct_swap": 1,
                "members": [{"off": 0x10}],
                "parent_members": [{"off": 0x20}]},
       "check": lambda s: [a for a, f in s["leafhits"]] == [HDRBUF + 0x10]})
    return C, M


def trhas(s, *names):
    t = [x[0] for x in s["trace"]]
    return all(n in t for n in names)

def trabsent(s, *names):
    t = [x[0] for x in s["trace"]]
    return all(n not in t for n in names)


def snap_case(w, case):
    gm = w.gm
    snap = {
        "ret": w.last_ret,
        "flag": rd8(FLAGB, gm),
        "outl": rd32(OUTL, gm),
        "scount": rd32(STREAM + 0x18, gm),
        "nscap": rd32(NSREC + 0, gm),
        "nsbuf": rd64(NSREC + 8, gm),
        "gvec_size": rd32(GVEC + 0, gm),
        "gvec_buf": rd64(GVEC + 8, gm),
        "d_vtbl": rd64(DESC + 0, gm),
        "d_size": rd32(DESC + 0x38, gm),
        "d_m0": rd64(DESC + 0xC0, gm),
        "d_m1": rd64(DESC + 0xC8, gm),
        "d_m2": rd64(DESC + 0xD0, gm),
        "d_flag": rd32(DESC + 0x19C, gm),
        "d_l80": rd64(DESC + 0x80, gm),
        "d_parent": rd64(DESC + 0x78, gm),
        "nsbytes": (gm.r(rd64(NSREC + 8, gm), rd32(NSREC + 0, gm))
                    if rd64(NSREC + 8, gm) else b""),
        "leafhits": leafhits({"gm": gm}),
        "leaf_n": sum(1 for i in range(64)
                      if rd64(LEAFLOG + i * 0x10, gm)),
        "allocs": w.allocs,
        "frees": w.frees,
        "gm": gm,
        "trace": w.trace,
        "faults": w.faults,
    }
    return snap


def run_case(case, raw, secs):
    w = build(case, raw, secs)
    w.last_ret = -1
    try:
        if "direct_swap" in case:
            invoke_descswap(w, case["direct_swap"])
            w.last_ret = 0
        elif case.get("skip_loader"):
            pass
        else:
            w.last_ret = invoke_loader(w)
    except UcError as e:
        w.faults.append(("EMU", str(e),
                         "rip=%x" % w.uc.reg_read(UC_X86_REG_RIP)))
    snap = snap_case(w, case)
    ok = False
    try:
        ok = bool(case["check"](snap))
    except Exception as e:
        snap["checkerr"] = str(e)
    snap.pop("gm", None)
    return snap, ok


def run_all():
    raw, secs = load_image()
    cases, mutants = build_cases()
    results, mres = [], []
    passed = total = 0
    for case in cases:
        snap, ok = run_case(case, raw, secs)
        total += 1
        passed += ok
        expect(case["name"], snap, ok, "see result.json")
        results.append({"name": case["name"], "ok": ok, "snap": snap})
    mkilled = mtotal = 0
    for mut in mutants:
        case = dict(mut["case"])
        case["name"] = mut["name"]
        case["patch"] = mut["patch"]
        case["check"] = mut["check"]
        snap, ok = run_case(case, raw, secs)
        if ok:
            mkilled += 1
        else:
            print("MUTANT SURVIVED " + mut["name"])
        mres.append({"name": mut["name"], "killed": ok, "snap": snap})
        mtotal += 1

    print("\n=== SUMMARY ===")
    print("%d/%d cases passed, %d/%d mutants killed" %
          (passed, total, mkilled, mtotal))
    for r in results + mres:
        if ("ok" in r and r["ok"]) or ("killed" in r and r["killed"]):
            continue
        s = r["snap"]
        print("  %s ret=%s flag=%s outl=%x scount=%x" %
              (r["name"], s["ret"], s["flag"], s["outl"], s["scount"]))
        print("    trace:", [x[:2] for x in s["trace"]][:24])
        if s["faults"]:
            print("    faults:", s["faults"][:4])
        if "checkerr" in s:
            print("    checkerr:", s["checkerr"])
    with open("result.json", "w") as f:
        json.dump({"total": total, "passed": passed,
                   "mutants": mtotal, "killed": mkilled,
                   "results": results, "mutant_results": mres},
                  f, indent=2,
                  default=lambda o: o.hex() if isinstance(o, bytes) else o)

if __name__ == "__main__":
    run_all()
