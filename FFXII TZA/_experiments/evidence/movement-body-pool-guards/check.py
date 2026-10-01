# EXP-087 - movement-body-pool consumer guards, isolated original-code execution.
#
# CONTRACT-movement-body-pool.md's §13 pilot executed only the allocator (003DA8A0) and the
# release (003DAD00); the document's own note says "No pilot drives any of these eight
# functions". The contract's central claim is that EVERY consumer of the exhausted-pool
# NULL re-loads the +0xC0/+0x138 chain and guards each hop, so exhaustion becomes a quiet
# loss of collision rather than a crash. This harness executes all six remaining bodies as
# shipped bytes at their canonical VAs, against the real pool array, list heads and codec
# table globals.
#
#   REAL (executed as shipped):
#     002E3500  the creation sequence (release-old, alloc, store WITHOUT testing, then
#               calls consumers 1-4 and tail-jumps consumer 5)
#     003DA8A0  allocator; 003DAD00 release (already piloted; here they run inside the
#               creator so exhaustion is produced by the real list state)
#     00380B80  body+0x30 sub-object initialiser (called by alloc)
#     003DA830  body+0xF0 epsilon-quaternion initialiser (called by alloc)
#     00269EC0  consumer 1: writes body+6, guarded on both hops
#     002681D0  consumer 2: kind-3-gated shape-code computer; writes body+0x80 and
#               actor+0x153, BOTH behind the +0x138 guard (split body: 0x2681D0-0x2681D9
#               and 0x2681E0-0x2682C5)
#     002682D0  consumer 3: three-hop guard, writes body+0x90 bits 0-1 from actor+0x151
#     002685F0  consumer 4: copies actor+0x148 to body+8; xorps substitute on null actor
#               is measurably DEAD (the second test rejects rax==0 before any store)
#     00268380  consumer 5: the shape sizer - kind-nibble dispatch, dominated (NOT
#               re-tested) re-loads of the chain for its last three calls
#     003DA710 / 006C0520 / 003DB130 / 003DB120 / 003DAF20  consumer-5 callees
#     003590D0 / 00263F10 / 00263FF0 / 003587C0 / 003589B0 / 002672B0  consumer-2 chain
#     00861EC0  memset thunk  (IAT 008C2A60 = VCRUNTIME140!memset   -> fixture rep-stosb)
#     00861F08  cosf thunk    (IAT 008C2BA8 = crt-math!cosf         -> fixture x87 fcos)
#     00861F0E  sinf thunk    (IAT 008C2BB0 = crt-math!sinf         -> fixture x87 fsin)
#
#   STUBBED WITH LOGGING (disclosed - deep predicates outside the contract's ownership;
#   patched to `ret`, args/order captured, eax controlled per case):
#     00265680  table predicate feeding ebx (gate global 0x2648E20 + deeper calls)
#     0037C860  final-override predicate (tail jmp into 00303EC0)
#
# Globals mapped at their real addresses:
#   pool array 02B4E4C0 (128 x 0x130), free head 02B57CC4, active head 02B57CC0
#   codec row table 02098E10 (stride 0x288; row+8 = slot array; 002672B0 iterates
#   row+0x17 value bytes gated by row+0x10 flag&1, rows 02098E10..0209985F),
#   consumer-2 compare global 022C7FE0, and the float divisor 008F312F used by
#   003DAF20 (real image bytes).
#
# All guest memory is host-backed (mem_map_ptr + ctypes buffers): the vendored and
# stock unicorn DLLs on this host intermittently report UC_ERR_*_UNMAPPED from the
# uc_mem_write/uc_mem_read API for pages that are mapped and executable - all
# fixture I/O therefore goes through the host pointers directly.
#
# Body layout used by fixtures: +0 prev idx, +2 next idx, +4 self idx (0xFFFF = null
# link; +4 is written once at pool init and release pushes it back as the free head).

import ctypes, hashlib, json, math, os, struct, sys

sys.path.insert(0, r"Database/Tools/work/ASTRA/python-libs")
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, UC_HOOK_BLOCK, UC_PROT_ALL
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000

# ---- fixture map -------------------------------------------------------------
CTX    = 0x60001000   # context: +3 kind nibble, +0xC flags, +0x18/19/1A alt-record, +0xB8 -> PB, +0xC0 -> ACT
ACT    = 0x60003000   # actor record: +0x138 -> body, +0x140/144/148 floats, +0x151/152 bytes, +0x153 result
ALT    = 0x60004000   # alternate record returned by 003587C0
PB     = 0x60005000   # param block (ctx+0xB8): +0x24/+0x38/+0x50/+0x68/+0xA8/+0xC0, +0x104..106
SLOTS  = 0x60006000   # slot array for 003587C0: +0 count, +8 entries (8B each)
CODE   = 0x6000F000   # fixture memset / cosf / sinf implementations
STACK  = 0x61000000
RETQ   = 0x62000000

POOL    = 0x2B4E4C0   # real pool VA: 128 bodies of 0x130
G_FREE  = 0x2B57CC4   # free-list head (word index)
G_ACTV  = 0x2B57CC0   # active-list head (word index)
G_CMP   = 0x22C7FE0   # consumer-2 compare global (003590D0)
T_ROW   = 0x2098E10   # codec row table base (00263FF0 lea target; stride 0x288; +8 = slot array)
P_FLAG  = 0x2098E20   # 002672B0 row enable flag (row_base+(-7), base=02098E27 stride 0x288)
P_VAL   = 0x2098E27   # 002672B0 row value byte (row_base+0); loop ends at 02099ACF (5 rows)
G_65680 = 0x2648E20   # 00265680 gate global (only read if ever run real - it is stubbed)

REAL = [
    (0x2E3500, 0x080),   # creator
    (0x3DA8A0, 0x148),   # alloc
    (0x3DAD00, 0x0E0),   # release
    (0x380B80, 0x0C0),   # body+0x30 init
    (0x3DA830, 0x014),   # body+0xF0 eps-quat init
    (0x269EC0, 0x01C),   # cons1
    (0x2681D0, 0x00A),   # cons2 head (test rcx; jne 0x2681E0; ret)
    (0x2681E0, 0x0E6),   # cons2 body
    (0x2682D0, 0x04F),   # cons3
    (0x2685F0, 0x030),   # cons4
    (0x268380, 0x1A4),   # cons5
    (0x3DA710, 0x015),   # two-dword copy
    (0x6C0520, 0x01A),   # quat write (reads arg5 at [rsp+0x28])
    (0x3DB130, 0x009),   # body+0xE0 = xmm1
    (0x3DB120, 0x009),   # body+0xE4 = xmm1
    (0x3DAF20, 0x0F3),   # rotation columns; calls cosf/sinf thunks
    (0x3590D0, 0x007),   # global getter
    (0x263F10, 0x02C),   # record resolver (calls 0x3587C0 when [rcx+0x18]==2)
    (0x263FF0, 0x015),   # row getter: 0x2649E10 + movsxd(ecx)*0x288
    (0x3587C0, 0x032),   # slot-array lookup
    (0x3589B0, 0x026),   # handle encoder
    (0x2672B0, 0x039),   # table predicate leaf
    (0x861EC0, 0x008),   # memset thunk
    (0x861F08, 0x008),   # cosf thunk
    (0x861F0E, 0x008),   # sinf thunk
]

STUBS = {
    0x265680: "pred_65680",
    0x37C860: "pred_37C860",
}

IAT_MEMSET = 0x8C2A60
IAT_COSF   = 0x8C2BA8
IAT_SINF   = 0x8C2BB0
DIVISOR    = 0x8F3130   # real float the rotation builder divides by

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def f32(v): return struct.unpack("<f", struct.pack("<I", v & 0xFFFFFFFF))[0]
def pf(v): return struct.pack("<f", v)

def load_exe():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs = []
    off = pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    def rd(va, n):
        r = va - BASE
        for sva, vs, ra, rs in secs:
            if sva <= r < sva + rs:
                return raw[ra + (r - sva):ra + (r - sva) + n]
        raise AssertionError("VA not in image: %x" % va)
    return rd

# memset: rcx=dst, dl=fill, r8=len -> rax=dst  (rep stosb)
MEMSET_FN = bytes.fromhex("4889c8574889cf88d04c89c1f3aa5fc3")
# cosf: cvtss2sd xmm0,xmm0; sub rsp,8; movsd [rsp],xmm0; fld; fcos; fstp; movsd xmm0,[rsp]; cvtsd2ss; add rsp,8; ret
COSF_FN = bytes.fromhex("f30f5ac0" "4883ec08" "f20f110424" "dd0424" "d9ff"
                        "dd1c24" "f20f100424" "f20f5ac0" "4883c408" "c3")
SINF_FN = bytes.fromhex("f30f5ac0" "4883ec08" "f20f110424" "dd0424" "d9fe"
                        "dd1c24" "f20f100424" "f20f5ac0" "4883c408" "c3")

class GuestMem:
    """Host-backed guest memory. Every region is a ctypes buffer handed to
    mem_map_ptr; all fixture reads/writes go through ctypes, bypassing
    uc_mem_write/uc_mem_read entirely (the vendored+stock DLLs intermittently
    return UNMAPPED for mapped pages while emulation still works - the API
    lookup path is unreliable in this environment)."""
    def __init__(self, uc):
        self.uc = uc
        self.bufs = []            # keep host buffers alive for the uc's lifetime
        self.regions = []         # (guest_base, size, host_ptr)
    def map(self, addr, size):
        buf = ctypes.create_string_buffer(size)
        self.bufs.append(buf)
        ptr = ctypes.addressof(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL, ptr)
        self.regions.append((addr, size, ptr))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x" % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), data, len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)

def body_addr(i):
    return POOL + i * 0x130

def init_pool(gm, n_free, active_idx=None):
    """n_free bodies chained on the free list (indices 0..n_free-1); the rest are
    unlinked. If active_idx is given, that body is the one-entry active list."""
    for i in range(128):
        b = body_addr(i)
        gm.w(b, b"\xcc" * 0x130)                 # poison: uninit reads stand out
        gm.w(b + 4, struct.pack("<H", i))         # self index (pool-init invariant)
    gm.w(G_ACTV, struct.pack("<H", 0xFFFF if active_idx is None else active_idx))
    if n_free == 0:
        gm.w(G_FREE, struct.pack("<H", 0xFFFF))
    else:
        gm.w(G_FREE, struct.pack("<H", 0))
        for i in range(n_free):
            b = body_addr(i)
            gm.w(b + 0, struct.pack("<H", 0xFFFF))
            gm.w(b + 2, struct.pack("<H", i + 1 if i + 1 < n_free else 0xFFFF))
    if active_idx is not None:
        a = body_addr(active_idx)
        gm.w(a + 0, struct.pack("<H", 0xFFFF))
        gm.w(a + 2, struct.pack("<H", 0xFFFF))

def build_world(case, rd):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    gm = GuestMem(uc)
    pages = set()
    for va, n in REAL:
        for p in range(va & ~0xFFF, (va + n + 0xFFF) & ~0xFFF, 0x1000):
            pages.add(p)
    for va in STUBS:
        pages.add(va & ~0xFFF)
    for g in (G_CMP, IAT_MEMSET, IAT_COSF, IAT_SINF, DIVISOR, G_65680, T_ROW, P_VAL):
        pages.add(g & ~0xFFF)
    # merge adjacent single pages into contiguous regions (fewer map_ptr calls)
    pages.update(range(0x2098000, 0x209A000, 0x1000))   # 002672B0's row window
    pages.update(range(0x2B4E000, 0x2B59000, 0x1000))   # pool + list heads
    ps = sorted(pages)
    runs = []
    for p in ps:
        if runs and p == runs[-1][0] + runs[-1][1]:
            runs[-1][1] += 0x1000
        else:
            runs.append([p, 0x1000])
    for p, s in runs:
        gm.map(p, s)
    for va, n in REAL:
        gm.w(va, rd(va, n))
    gm.w(DIVISOR & ~0xFFF, rd(DIVISOR & ~0xFFF, 0x1000))  # real .rdata page
    for va in STUBS:
        gm.w(va, b"\xc3")
    for a, s in [(0x60000000, 0x20000), (STACK, 0x100000), (RETQ, 0x1000)]:
        gm.map(a, s)
    gm.w(RETQ, b"\xc3")
    gm.w(CODE,            MEMSET_FN)
    gm.w(CODE + 0x40,     COSF_FN)
    gm.w(CODE + 0x80,     SINF_FN)
    gm.w(IAT_MEMSET, qw(CODE))
    gm.w(IAT_COSF,   qw(CODE + 0x40))
    gm.w(IAT_SINF,   qw(CODE + 0x80))

    # ---- globals
    gm.w(G_CMP, dw(case.get("cmp_global", 0xDEADBEEF)))

    # ---- codec/predicate row table (row 0 = T_ROW..+0x288)
    gm.w(T_ROW + 8, qw(SLOTS if case.get("slots", True) else 0))
    gm.w(P_FLAG, bytes([case.get("pred_flag", 1)]))
    gm.w(P_VAL,  bytes([case.get("pred_val", 3)]))
    gm.w(SLOTS, dw(case.get("slot_count", 1)))
    for i, ptr in enumerate(case.get("slot_entries", [ALT])):
        gm.w(SLOTS + 8 + i * 8, qw(ptr))

    # ---- pool
    init_pool(gm, case.get("n_free", 4), case.get("active_idx"))

    # ---- context / actor / param block
    gm.w(CTX, b"\0" * 0x200)
    gm.w(CTX + 3, bytes([case.get("kind", 0x60)]))           # kind nibble 3
    gm.w(CTX + 0xC, bytes([case.get("ctx_flags", 0x10)]))
    gm.w(CTX + 0x18, bytes([case.get("ctx18", 1)]))          # != 2 -> no alt resolve
    gm.w(CTX + 0x19, bytes([case.get("ctx19", 0) & 0xFF]))
    gm.w(CTX + 0x1A, struct.pack("<H", case.get("ctx1a", 0)))
    gm.w(CTX + 0xB8, qw(case.get("pb", PB)))
    gm.w(CTX + 0xC0, qw(case.get("actor", ACT)))

    gm.w(ACT, b"\0" * 0x200)
    gm.w(ACT + 0x138, qw(case.get("act_body", case.get("body", 0)) or 0))
    gm.w(ACT + 0x140, pf(case.get("r140", 2.0)))
    gm.w(ACT + 0x144, pf(case.get("r144", 3.0)))
    gm.w(ACT + 0x148, pf(case.get("r148", 9.5)))
    gm.w(ACT + 0x151, bytes([case.get("a151", 0)]))
    gm.w(ACT + 0x152, bytes([case.get("a152", 2)]))
    # handle fields consumed by 003589B0 on the resolved record
    rec = case.get("alt_record", CTX)
    gm.w(ALT, b"\0" * 0x100)
    gm.w(rec + 0x00, struct.pack("<H", case.get("h_w0", 0x123)))
    gm.w(rec + 0x15, bytes([case.get("h_b15", 5)]))
    gm.w(rec + 0x16, struct.pack("<H", case.get("h_w16", 0x456)))

    gm.w(PB, b"\0" * 0x200)
    gm.w(PB + 0x24, pf(case.get("pb24", 4.0)))
    gm.w(PB + 0x38, pf(case.get("pb38", 5.0)))
    gm.w(PB + 0x50, pf(case.get("pb50", 6.0)))
    gm.w(PB + 0x54, pf(case.get("pb54", 7.0)))
    gm.w(PB + 0x68, pf(case.get("pb68", 8.0)))
    gm.w(PB + 0xA8, pf(case.get("pbA8", 10.0)))
    gm.w(PB + 0xC0, pf(case.get("pbC0", 11.0)))
    gm.w(PB + 0x104, bytes([case.get("pb104", 0x41)]))
    gm.w(PB + 0x105, bytes([case.get("pb105", 0x42)]))
    gm.w(PB + 0x106, bytes([case.get("pb106", 0x43)]))

    # ---- mutants
    for va, data in case.get("patch", []):
        gm.w(va, data)

    # ---- hooks
    trace, faults, hist = [], [], []
    rets = case.get("rets", {})

    def on_stub(uc_, addr, size, _):
        sp = uc_.reg_read(UC_X86_REG_RSP)
        trace.append({"at": STUBS[addr],
                      "rcx": uc_.reg_read(UC_X86_REG_RCX),
                      "rdx": uc_.reg_read(UC_X86_REG_RDX),
                      "r8":  uc_.reg_read(UC_X86_REG_R8),
                      "r9":  uc_.reg_read(UC_X86_REG_R9)})
        uc_.reg_write(UC_X86_REG_RAX, rets.get(addr, 0))

    def on_bad(uc_, access, addr, size, value, _):
        faults.append((access, addr, uc_.reg_read(UC_X86_REG_RIP)))
        return False

    def on_block(uc_, addr, size, _):
        hist.append(addr)
        if len(hist) > 96:
            hist.pop(0)

    for va in STUBS:
        uc.hook_add(UC_HOOK_CODE, on_stub, begin=va, end=va)
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)
    uc.hook_add(UC_HOOK_BLOCK, on_block)
    return uc, gm, trace, faults, hist

def run_case(case, rd):
    uc, gm, trace, faults, hist = build_world(case, rd)
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, case.get("rcx", CTX))
    uc.reg_write(UC_X86_REG_RDX, case.get("rdx", 0))
    entry = case.get("entry", 0x2E3500)
    fault = None
    try:
        uc.emu_start(entry, RETQ, count=200000)
    except Exception as e:
        fault = str(e)
    def r8(a):  return gm.r(a, 1)[0]
    def r16(a): return struct.unpack("<H", gm.r(a, 2))[0]
    def r32(a): return struct.unpack("<I", gm.r(a, 4))[0]
    def r64(a): return struct.unpack("<Q", gm.r(a, 8))[0]
    def rf(a):  return struct.unpack("<f", gm.r(a, 4))[0]
    b = case.get("body", 0)
    snap = {
        "fault": fault, "faults": faults, "trace": trace, "hist": hist[-24:],
        "act138":  r64(ACT + 0x138),
        "act153":  r8(ACT + 0x153),
        "free_h":  r16(G_FREE), "actv_h": r16(G_ACTV),
        "body6":   r8(b + 6)   if b else None,
        "body8":   rf(b + 8)   if b else None,
        "body80":  r16(b + 0x80) if b else None,
        "body90":  r32(b + 0x90) if b else None,
        "bodyE0":  rf(b + 0xE0) if b else None,
        "bodyE4":  rf(b + 0xE4) if b else None,
        "bodyF0":  [rf(b + 0xF0 + 4*i) for i in range(4)] if b else None,
        "body40":  [rf(b + 0x40 + 4*i) for i in range(4)] if b else None,
        "body94":  [rf(b + 0x94 + 4*i) for i in range(6)] if b else None,
        "nv_ok": all(uc.reg_read(r) == 0 for r in
                     (UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI,
                      UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15)),
    }
    return snap

def expect(name, snap, cond, why):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name + ("  -- " + why if not ok else ""))
    return ok

# ---- cases -------------------------------------------------------------------
def cases(rd):
    C = lambda **k: k
    B0 = body_addr(0)      # first free body (what alloc hands out)
    OLD = body_addr(120)   # planted active body for the replace path
    base = dict(body=B0)
    out = []
    # ---- creator -------------------------------------------------------------
    out += [
        C(name="create-fresh", entry=0x2E3500, n_free=4, act_body=0, body=B0,
          check=lambda s: (s["act138"] == B0 and s["free_h"] == 1 and s["actv_h"] == 0
                           and s["fault"] is None and s["body6"] == 0
                           and s["body80"] == 3 and s["act153"] == 3
                           and abs(s["body8"] - 9.5) < 1e-6
                           and abs(s["bodyE0"] - 44.0) < 1e-5),
          why="fresh: alloc returns body0, stored at actor+0x138; cons1 +6=0, cons2 edx=2 -> +0x80=3, cons4 +8=9.5, cons5 +0xE0=44"),
        C(name="create-replace", entry=0x2E3500, n_free=4, active_idx=120,
          act_body=body_addr(120), body=body_addr(120),
          check=lambda s: (s["act138"] == body_addr(120) and s["free_h"] == 0
                           and s["actv_h"] == 120 and s["fault"] is None
                           and s["body80"] == 3),
          why="replace: release(120) pushes it to the free head and alloc immediately re-pops it - "
              "the released body is ALWAYS the one recycled"),
        C(name="create-exhausted", entry=0x2E3500, n_free=0, act_body=0, body=None,
          a152=0, ctx_flags=0,
          cmp_global=(0x456 & 0x7FF) << 20 | (5 & 0xF) << 16 | 0x123,
          check=lambda s: (s["act138"] == 0 and s["free_h"] == 0xFFFF
                           and s["fault"] is None and s["act153"] == 0
                           and [t["at"] for t in s["trace"]] == ["pred_37C860"]),
          why="exhausted: alloc NULL stored UNTESTED at actor+0x138; consumers still run - "
              "with a152=0 the whole predicate chain executes, only the writes are skipped"),
        C(name="create-exhausted-replace", entry=0x2E3500, n_free=0, active_idx=120,
          act_body=body_addr(120), body=body_addr(120),
          check=lambda s: (s["act138"] == OLD and s["free_h"] == 0xFFFF
                           and s["actv_h"] == 120 and s["fault"] is None),
          why="exhausted+replace: release frees body120, alloc immediately re-pops it -> same body recycled"),
        C(name="create-null-actor", entry=0x2E3500, actor=0, n_free=4, body=None,
          check=lambda s: (s["fault"] is None and s["free_h"] == 0 and s["actv_h"] == 0xFFFF),
          why="null actor: creator tests [ctx+0xC0] itself and returns before alloc - pool untouched"),
        C(name="create-null-ctx", entry=0x2E3500, rcx=0, n_free=4, body=None,
          check=lambda s: s["fault"] is not None and any(a == 0xC0 for _, a, _ in s["faults"]),
          why="null ctx: creator does NOT guard rcx - [rcx+0xC0] faults at VA 0xC0"),
        C(name="create-kind0", entry=0x2E3500, kind=0x00, n_free=4, act_body=0, body=B0,
          check=lambda s: (s["act138"] == B0 and s["fault"] is None
                           and abs(s["bodyE0"] - 0.0) < 1e-6 and abs(s["bodyE4"] - 5.0) < 1e-6
                           and s["body80"] == 0xFFFF and s["act153"] == 0),
          why="kind0 through the whole creation sequence: cons2 kind-gate skips its writes "
              "(body+0x80 keeps the alloc-init sentinel 0xFFFF, actor+0x153 untouched), cons5 xmm6=0, xmm7=2+3"),
    ]
    # ---- consumer 1: byte writer ----------------------------------------------
    out += [
        C(name="c1-write", entry=0x269EC0, rdx=0xAB, body=B0,
          check=lambda s: s["body6"] == 0xAB and s["fault"] is None,
          why="both hops valid: body+6 = dl"),
        C(name="c1-noactor", entry=0x269EC0, rdx=0xAB, actor=0, body=None,
          check=lambda s: s["fault"] is None,
          why="actor null: first guard refuses, no write, no fault"),
        C(name="c1-nobody", entry=0x269EC0, rdx=0xAB, body=None,
          check=lambda s: s["fault"] is None,
          why="body null: second guard refuses, no write"),
    ]
    # ---- consumer 2: shape code ------------------------------------------------
    # edx dispatch on actor+0x152: 0 -> predicate chain; 2 -> ebx=3; 3 -> ebx=5; else 2.
    # then: 002672B0 returns 0 forces ebx=1; 0037C860 nonzero forces ebx=5.
    out += [
        C(name="c2-nullctx", entry=0x2681D0, rcx=0, body=None,
          check=lambda s: s["fault"] is None and not s["trace"],
          why="null ctx: the ONLY consumer that guards rcx at its own head"),
        C(name="c2-noactor", entry=0x2681D0, actor=0, body=None,
          check=lambda s: s["fault"] is None and not s["trace"],
          why="actor null: epilogue before the kind gate"),
        C(name="c2-kind1", entry=0x2681D0, kind=0x20, body=B0,
          check=lambda s: (s["fault"] is None and not s["trace"]
                           and s["body80"] == 0xCCCC and s["act153"] == 0),
          why="kind!=3: everything skipped, even the writes"),
        C(name="c2-edx2", entry=0x2681D0, a152=2, body=B0,
          check=lambda s: s["body80"] == 3 and s["act153"] == 3,
          why="actor+0x152==2 -> ebx=3 (pred ret 1, final pred ret 0)"),
        C(name="c2-edx3", entry=0x2681D0, a152=3, body=B0,
          check=lambda s: s["body80"] == 5 and s["act153"] == 5,
          why="actor+0x152==3 -> ebx=5"),
        C(name="c2-edx1", entry=0x2681D0, a152=1, body=B0,
          check=lambda s: s["body80"] == 2 and s["act153"] == 2,
          why="actor+0x152==1 (and 4+) -> ebx=2"),
        C(name="c2-edx0-mismatch", entry=0x2681D0, a152=0, body=B0,
          check=lambda s: s["body80"] == 1 and s["act153"] == 1,
          why="edx=0 with global!=encoded handle -> ebx=1 (jne arm)"),
        C(name="c2-edx0-match-flag0", entry=0x2681D0, a152=0, body=B0, ctx_flags=0,
          cmp_global=(0x456 & 0x7FF) << 20 | (5 & 0xF) << 16 | 0x123,
          check=lambda s: s["body80"] == 0 and s["act153"] == 0,
          why="edx=0, handle matches global, ctx flag 0x10 clear -> ebx=0"),
        C(name="c2-edx0-match-pred0", entry=0x2681D0, a152=0, body=B0,
          cmp_global=(0x456 & 0x7FF) << 20 | (5 & 0xF) << 16 | 0x123,
          rets={0x265680: 0},
          check=lambda s: s["body80"] == 0 and any(t["at"] == "pred_65680" for t in s["trace"]),
          why="handle match + flag set + pred returns 0 -> ebx=0"),
        C(name="c2-edx0-match-pred1", entry=0x2681D0, a152=0, body=B0,
          cmp_global=(0x456 & 0x7FF) << 20 | (5 & 0xF) << 16 | 0x123,
          rets={0x265680: 7},
          check=lambda s: s["body80"] == 1,
          why="handle match + flag set + pred nonzero -> ebx=esi=1"),
        C(name="c2-edx2-nopreds", entry=0x2681D0, a152=2, body=B0,
          check=lambda s: s["body80"] == 3 and not s["trace"],
          why="the edx!=0 arms JUMP DIRECTLY to the writes - no predicate calls at all"),
        C(name="c2-pred0-override", entry=0x2681D0, a152=0, body=B0, pred_val=0,
          cmp_global=(0x456 & 0x7FF) << 20 | (5 & 0xF) << 16 | 0x123, ctx_flags=0,
          check=lambda s: s["body80"] == 1 and s["act153"] == 1,
          why="002672B0 returns 0 (row byte &3 != 3) -> cmove forces ebx=1, overriding the matched-handle result"),
        C(name="c2-final5", entry=0x2681D0, a152=0, body=B0, rets={0x37C860: 1},
          cmp_global=(0x456 & 0x7FF) << 20 | (5 & 0xF) << 16 | 0x123, ctx_flags=0,
          check=lambda s: s["body80"] == 5 and any(t["at"] == "pred_37C860" for t in s["trace"]),
          why="0037C860 nonzero -> ebx=5 final override"),
        C(name="c2-nobody", entry=0x2681D0, a152=0, act_body=0, body=None,
          cmp_global=(0x456 & 0x7FF) << 20 | (5 & 0xF) << 16 | 0x123, ctx_flags=0,
          check=lambda s: (s["fault"] is None and s["act153"] == 0
                           and [t["at"] for t in s["trace"]] == ["pred_37C860"]),
          why="exhaustion: BOTH writes are behind the body guard - even actor+0x153 stays unwritten; the predicate chain still ran"),
        C(name="c2-alt-record", entry=0x2681D0, a152=0, body=B0, ctx18=2,
          ctx19=0, ctx1a=0, slot_count=1, slot_entries=[ALT], alt_record=ALT,
          h_w0=0x777, h_b15=9, h_w16=0x111,
          cmp_global=(0x111 & 0x7FF) << 20 | (9 & 0xF) << 16 | 0x777,
          ctx_flags=0,
          check=lambda s: s["body80"] == 0,
          why="[ctx+0x18]==2 -> resolver swaps record via table+slot; the ALT record's handle is what gets compared"),
        C(name="c2-alt-null", entry=0x2681D0, a152=0, body=B0, ctx18=2,
          ctx19=0, ctx1a=5, slot_count=1,     # oob slot -> resolver returns 0 -> cmovne keeps ACT
          cmp_global=(0x456 & 0x7FF) << 20 | (5 & 0xF) << 16 | 0x123,
          ctx_flags=0,
          check=lambda s: s["body80"] == 0,
          why="resolver returns 0 on oob slot -> cmovne keeps the original record"),
    ]
    # ---- consumer 3: flag merge ------------------------------------------------
    out += [
        C(name="c3-full", entry=0x2682D0, a151=0x03, body=B0,
          check=lambda s: (s["body90"] & 3) == 3 and s["fault"] is None,
          why="actor+0x151=3 -> body+0x90 bits0-1 = 3"),
        C(name="c3-preserve", entry=0x2682D0, a151=0x02, body=B0,
          check=lambda s: (s["body90"] & 3) == 2 and (s["body90"] & ~3) == (0xCCCCCCCC & ~3),
          why="bits0-1 replaced, upper bits of body+0x90 preserved"),
        C(name="c3-nullctx", entry=0x2682D0, rcx=0, body=None,
          check=lambda s: s["fault"] is None,
          why="null ctx refused at head"),
        C(name="c3-noactor", entry=0x2682D0, actor=0, body=None,
          check=lambda s: s["fault"] is None, why="actor null refused"),
        C(name="c3-nobody", entry=0x2682D0, a151=3, body=None,
          check=lambda s: s["fault"] is None, why="body null refused before the write"),
    ]
    # ---- consumer 4: float copy -------------------------------------------------
    out += [
        C(name="c4-copy", entry=0x2685F0, r148=9.5, body=B0,
          check=lambda s: abs(s["body8"] - 9.5) < 1e-6,
          why="body+8 = actor+0x148"),
        C(name="c4-noactor", entry=0x2685F0, actor=0, body=None,
          check=lambda s: s["fault"] is None,
          why="actor null: xorps path taken, then the SECOND test rejects rax before any store"),
        C(name="c4-nobody", entry=0x2685F0, body=None,
          check=lambda s: s["fault"] is None, why="body null: no store"),
    ]
    # ---- consumer 5: shape sizer -------------------------------------------------
    out += [
        C(name="c5-kind3", entry=0x268380, kind=0x60, body=B0,
          check=lambda s: (s["fault"] is None
                           and abs(s["bodyE0"] - 11.0 * 4.0) < 1e-5        # [b8+0xC0]*[b8+0x24]
                           and abs(s["bodyE4"] - 5.0) < 1e-6              # 2.0 + 3.0
                           and abs(s["bodyF0"][0] - 6.0) < 1e-6           # quat x = [b8+0x50] via 3DA710
                           and abs(s["bodyF0"][1] - 7.0) < 1e-6           # quat y = [b8+0x54]
                           and abs(s["bodyF0"][2] - 10.0) < 1e-6          # quat z = [b8+0xA8]
                           and s["bodyF0"][3] == 0.0),
          why="kind3: full pipeline - 3DA710 copy, xmm6=pbC0*pb24, xmm3=pbA8, rgb from pb+0x104..6"),
        C(name="c5-kind1", entry=0x268380, kind=0x20, body=B0,
          check=lambda s: (s["fault"] is None
                           and abs(s["bodyE0"] - 8.0) < 1e-6              # [b8+0x68]
                           and abs(s["bodyF0"][2] - 5.0) < 1e-6),         # xmm3 = [b8+0x38]
          why="kind1: xmm6 from +0x68, xmm3 from +0x38, rgb defaults 0x25/0x32/0x25"),
        C(name="c5-kind2", entry=0x268380, kind=0x40, body=B0,
          check=lambda s: (s["fault"] is None and abs(s["bodyE0"]) < 1e-6
                           and abs(s["bodyF0"][2]) < 1e-6),
          why="kind2: xmm6=0, xmm3=0 - the dispatch arms are 1 and 3 only"),
        C(name="c5-kind0", entry=0x268380, kind=0x00, body=B0,
          check=lambda s: s["fault"] is None,
          why="kind0: no 3DA710 call, zeros for xmm6/xmm3"),
        C(name="c5-noactor", entry=0x268380, actor=0, body=None,
          check=lambda s: s["fault"] is None,
          why="actor null -> epilogue, no writes"),
        C(name="c5-nobody", entry=0x268380, body=None,
          check=lambda s: s["fault"] is None,
          why="body null -> epilogue at 0x26851E, before the quat/matrix writes"),
    ]
    # ---- mutants -----------------------------------------------------------------
    # Each patch must change an observable. Byte sites verified against the image.
    M = [
        C(name="mut-c1-guard", entry=0x269EC0, rdx=0xAB, actor=0, body=None,
          patch=[(0x269ECA, b"\x90\x90")],          # je 0x269edb -> fallthrough
          check=lambda s: s["fault"] is not None and any(a == 0x138 for _, a, _ in s["faults"]),
          why="no actor guard -> reads [0+0x138], fault at 0x138"),
        C(name="mut-c2-guard", entry=0x2681D0, a152=2, body=None,
          patch=[(0x2682A5, b"\x90\x90")],          # je over the writes -> fallthrough
          check=lambda s: s["fault"] is not None and any(a == 0x80 for _, a, _ in s["faults"]),
          why="no body guard -> writes [0+0x80], fault at 0x80"),
        C(name="mut-c2-kind", entry=0x2681D0, kind=0x20, a152=2, body=B0,
          patch=[(0x268202, b"\x84")],              # jne -> je (near-jcc opcode byte)
          check=lambda s: s["body80"] == 3,
          why="inverted kind gate: kind1 now runs the kind3 pipeline (a152=2 -> ebx=3 written)"),
        C(name="mut-c2-cmove", entry=0x2681D0, a152=0, ctx_flags=0, body=B0,
          cmp_global=(0x456 & 0x7FF) << 20 | (5 & 0xF) << 16 | 0x123,
          patch=[(0x268277, b"\x89\xf3\x90")],      # cmove ebx,esi -> mov ebx,esi (always)
          check=lambda s: s["body80"] == 1,
          why="cmove->mov: on the flag-clear arm ebx=0 and 002672B0 returns 1 (cmove inert); "
              "the mutant forces ebx=esi=1 -> body80=1 instead of 0"),
        C(name="mut-c3-guard", entry=0x2682D0, a151=3, body=None,
          patch=[(0x2682EB, b"\x90\x90")],          # je -> fallthrough; rcx=0 -> r8=0x30
          check=lambda s: s["fault"] is not None and any(a == 0x90 for _, a, _ in s["faults"]),
          why="no body guard: lea makes r8=0x30 nonnull, write lands at [0x90]"),
        C(name="mut-c4-guard", entry=0x2685F0, body=None,
          patch=[(0x268618, b"\x90\x90")],
          check=lambda s: s["fault"] is not None and any(a == 0x8 for _, a, _ in s["faults"]),
          why="no body guard -> store to [0+8]"),
        C(name="mut-c5-guard", entry=0x268380, body=None,
          patch=[(0x2683C7, b"\x0f\x85")],          # je -> jne: null body falls through
          check=lambda s: s["fault"] is not None and any(a in (0xF0, 0xF4, 0xF8, 0xFC) for _, a, _ in s["faults"]),
          why="inverted body guard -> 6C0520 writes through r10=0 at +0xF0"),
        C(name="mut-c5-kind", entry=0x268380, kind=0x20, pb=0, body=B0,
          patch=[(0x268391, b"\x74")],              # jne -> je
          check=lambda s: s["fault"] is not None and any(a == 0x50 for _, a, _ in s["faults"]),
          why="inverted kind gate: kind1 reads [ctx+0xB8]=0 then [0+0x50] -> fault"),
        C(name="mut-store", entry=0x2E3500, n_free=4, body=B0,
          patch=[(0x2E3546, b"\x48\x89\x89\x38\x01\x00\x00")],  # mov [rcx+0x138],rcx
          check=lambda s: s["act138"] == ACT,
          why="the untested store, mutated: actor+0x138 = actor, not the allocated body"),
    ]
    out += M
    return out

def main():
    rd = load_exe()
    cs = cases(rd)
    results, fails = [], 0
    for c in cs:
        snap = run_case(c, rd)
        ok = expect(c["name"], snap, snap.pop("_ok", None) if "_ok" in snap else c["check"](snap), c["why"])
        results.append({"name": c["name"], "ok": ok, "why": c["why"], "snap": snap})
        if not ok:
            fails += 1
            print("   fault=%s faults=%s act138=%x free=%04x actv=%04x body80=%s body90=%s E0=%s E4=%s F0=%s 40=%s trace=%s"
                  % (snap["fault"], snap["faults"], snap["act138"], snap["free_h"],
                     snap["actv_h"], snap["body80"], snap["body90"], snap["bodyE0"],
                     snap["bodyE4"], snap["bodyF0"], snap["body40"], snap["trace"]))
    n_mut = sum(1 for c in cs if c["name"].startswith("mut-"))
    n_mut_killed = sum(1 for c, r in zip(cs, results) if c["name"].startswith("mut-") and r["ok"])
    print("\n%d/%d pass; mutants detected %d/%d" % (len(cs) - fails, len(cs), n_mut_killed, n_mut))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json")
    json.dump({"total": len(cs), "passed": len(cs) - fails,
               "mutants": n_mut, "mutants_detected": n_mut_killed,
               "cases": results}, open(out, "w"), indent=1)
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
