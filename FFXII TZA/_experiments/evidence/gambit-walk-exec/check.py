#!/usr/bin/env python3
"""EXP-095 gambit-walk-exec - the gambit walk with its evaluator and notifier
executed as real shipped bodies.

Subject under test (per CONTRACT-gambit-walk.md): 00305CC0, the walk that turns a
gambit list into a priority list. The differential suite (diff_gambit_walk.py,
34 cases / 68 comparisons / 0 mismatches) established the contract-level trace
semantics with all three callees scripted. This experiment keeps the walk's own
body real AND executes two of the three callees as real shipped code:

    003014C0  AiOrder_EvaluateAndResolveActionTarget - REAL, with its bounded
              closure real: 00308EC0 target-spec resolve, 00301830 condition
              dispatch (spec table 0x1ED0460 is shipped .rdata), 00328370 LCG,
              002E9C00 unit-arm first gate.
    004697C0  third call on the success path - REAL, with 002F8E90 kill-kind
              classify (EXP-093 chain).
    0030F760  BattleUnit_CommitAction - SCRIPTED per-call (real execution is
              EXP-091's published evidence; here its answer is an input to the
              walk, supplied identically on both sides of the comparison).
    00301AD0  per-slot target resolver - SCRIPTED per-slot (804-body static
              closure = the condition-scan machinery; disclosed boundary).
              Answers are read from the record's slot aux fields, so the script
              is a deterministic function of record content, not call index.

The observable is the CALL TRACE, as in the differential suite: which records
were offered to eval/commit/notify, in what order, with what target/param/
mode args. Eval outcome is driven by real record/unit/global state:

    spec 0xFFFF            -> eval ret 0 (sentinel; target out written 0xFFFF)
    spec 0x4000..~0x4167 with table entry -> roll arm: chance==0 -> ret 1;
                              else LCG roll%100 < chance -> ret 1
    spec-table hole (e.g. 0x4200, 0x4038, 0x4128, >=0x4168) -> ret 0
    spec < 0x4000          -> unit arm: 002E9C00(unit+0x10) -> -1 -> ret 0
    suspension byte 0x2089340 & 0x20 -> ret 0 before any arm
    on eval match, out_target = spec and param = 0 (no slots)

NOT EXERCISED (disclosed): the unit-arm eligibility cascade past 002E9C00
(002FFCF0 + 00306480 + 00303BD0 ... the "is action performable" machinery is a
separate contract surface); consequently the 003087E0 combiner, param-write
tail and notify's ring-insert/latch arms (all need target < 0x21F or a target
in {0x4022,0x4124}, unreachable for records that eval-match) stay dark here.
"""
import ctypes, hashlib, json, struct, sys, os
from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

UNITB  = HEAP + 0x100000        # unit, 0x1000
STATS  = HEAP + 0x110000        # stats rec, 0x200
SPAWNB = HEAP + 0x111000        # unit+0x6A0 flags byte
SETB   = HEAP + 0x200000        # gambit set: 32B header + 12x24B records
CTXB   = HEAP + 0x300000        # resume ctx
HITOB  = HEAP + 0x310000        # scripted hit objects {+0x30 -> rec; rec+8 = param}
HITREC = HEAP + 0x311000        # hit records

WALK    = 0x00305CC0
EVAL    = 0x003014C0
COMMIT  = 0x0030F760
NOTIFY  = 0x004697C0
SLOTRES = 0x00301AD0

COOKIE   = 0x0000DEADBEEF
G_COOKIE = 0x1F44830
G_SUSP   = 0x2089340           # eval bit0x20 suspend; ring bits 0x3080
G_LCG    = 0x22C256C           # 00328370 state dword
CODE     = 0x63000000          # fixture routines
IAT_MEMSET = 0x8C2A60          # memset IAT slot -> thunk 00861EC0

CALLS = {
    WALK:    "walk",
    EVAL:    "eval",
    COMMIT:  "commit",
    NOTIFY:  "notify",
    SLOTRES: "slotres",
    0x00308EC0: "tspec",
    0x00301830: "cond",
    0x00328370: "lcg",
    0x002E9C00: "uarm0",
    0x002FFCF0: "elig",
    0x0030F130: "tbuf",
    0x003087E0: "combine",
    0x002F8E90: "kkind",
    0x0046AB10: "kring",
    0x00808C40: "cookie",
    0x0020E600: "codec",
    0x00316CF0: "memsetw",
    0x00861EC0: "iat_memset",
}
# hooked-and-ret'd scripted callees (disclosed; answers supplied)
STUBS = {COMMIT: "commit", SLOTRES: "slotres"}

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def db(v): return struct.pack("<B", v & 0xFF)

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
    # IAT slots: parsed so every one can be nulled - an unplanted slot holds the
    # ILT hint RVA and an unexpected IAT call must fault, not execute name data
    iat = []
    def rva2off(rva):
        for sva, vs, ra, rs in secs:
            if sva <= rva < sva + rs:
                return ra + rva - sva
        return None
    imp_dir = pe + 24 + (112 if struct.unpack_from("<H", raw, pe + 24)[0] == 0x20B else 96) + 8
    imp_rva, _ = struct.unpack_from("<2I", raw, imp_dir)
    off2 = rva2off(imp_rva)
    i = 0
    while True:
        ilt, ts, fwd, name_rva, iat_rva = struct.unpack_from("<5I", raw, off2 + 20 * i)
        if name_rva == 0:
            break
        j = 0
        while True:
            e = struct.unpack_from("<Q", raw, rva2off(ilt or iat_rva) + 8 * j)[0]
            if e == 0:
                break
            iat.append(BASE + iat_rva + 8 * j)
            j += 1
        i += 1
    return raw, secs, iat

MEMSET_FN = bytes.fromhex("4889c8574889cf88d04c89c1f3aa5fc3")

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

HDR, RECS, STRIDE = 32, 0x20, 24

def rec_spec(spec=0x4100, chance=0, flags=0, slots=((0, 0, 0),) * 3):
    """24-byte gambit record. slots: (count u16, hitret i16, aux u16) per slot
    at +6/+0xC/+0x12; count>0 -> 00301AD0 is called and returns hitret."""
    r = bytearray(STRIDE)
    struct.pack_into("<H", r, 0, spec & 0xFFFF)
    struct.pack_into("<H", r, 2, chance & 0xFFFF)
    struct.pack_into("<H", r, 4, flags & 0xFFFF)
    for k, (cnt, hit, aux) in enumerate(slots[:3]):
        struct.pack_into("<H", r, 6 + k * 6, cnt & 0xFFFF)
        struct.pack_into("<H", r, 8 + k * 6, hit & 0xFFFF)
        struct.pack_into("<H", r, 10 + k * 6, aux & 0xFFFF)
    return bytes(r)

def rec_addr(i):
    return SETB + RECS + i * STRIDE

def lcg_roll(state):
    """Mirror of 00328370: three LCG iterations, folded 30-bit output.
    Returns (new_state, value)."""
    a = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    c = (a * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    e = (c * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    edx = ((a >> 16) & 0x7FF) << 10
    r8 = (((c >> 16) & 0x3FF) ^ edx) << 10 & 0xFFFFFFFF
    out = (((e >> 16) & 0x3FF) ^ r8) & 0xFFFFFFFF
    return e, out

def pick_seed(pred):
    s = 1
    while True:
        ns, v = lcg_roll(s)
        if pred(v % 100):
            return s, v % 100
        s = ns

class World:
    def __init__(self, case, raw, secs, iat):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x800000), (STACK, 0x100000), (RETQ, 0x1000),
                     (CODE, 0x1000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")
        for va in STUBS:
            gm.w(va, b"\xc3")            # scripted callee entries -> ret
        for slot in iat:
            gm.w(slot, qw(0))
        gm.w(CODE, MEMSET_FN)
        gm.w(IAT_MEMSET, qw(CODE))

        # ---- globals
        gm.w(G_COOKIE, qw(COOKIE))
        gm.w(G_SUSP, db(case.get("susp", 0)))
        gm.w(G_LCG, dw(case.get("lcg", 0x12345)))

        # ---- stats block (kindclass: kind!=1 -> early ret 1 when
        #      atype-0x1B>0xC; keep atype=0 -> kind 1)
        st = bytearray(0x200)
        st[4] = case.get("atype", 0) & 0xFF
        st[5] = case.get("skind", 0) & 0xFF
        struct.pack_into("<I", st, 0x3C, case.get("m3c", 0))
        struct.pack_into("<I", st, 0x64, case.get("m64", 0))
        gm.w(STATS, st)
        gm.w(SPAWNB, db(case.get("spawnf", 0)))

        # ---- unit
        u = bytearray(0x1000)
        struct.pack_into("<I", u, 0, case.get("uflags", 0x10))   # bit4 -> stats path
        struct.pack_into("<Q", u, 0x10, case.get("u10", 0))       # unit-arm obj (0 -> -1)
        struct.pack_into("<Q", u, 0x698, STATS)
        struct.pack_into("<Q", u, 0x6A0, SPAWNB)
        ctxp = case.get("ctx_at", -1)
        if ctxp == -1:
            ctx = 0
        elif ctxp == -2:
            ctx = CTXB
            gm.w(CTXB + 4, hw(case.get("ctx_flags", 0)))
        else:
            ctx = rec_addr(ctxp)      # ctx == a record's address
        struct.pack_into("<Q", u, 0x708, ctx)
        struct.pack_into("<H", u, 0x714, case.get("word714", 0xFFFF))
        struct.pack_into("<Q", u, 0x730, case.get("u730", 0))
        struct.pack_into("<Q", u, 0x738, case.get("u738", 0))
        gm.w(UNITB, u)

        # ---- gambit set (page in front is mapped via the same heap region;
        #      SETB-1 byte drives the negative-index case)
        gm.w(SETB, bytes(HDR + 12 * STRIDE))
        counts = list(case.get("counts", [0] * HDR))[:HDR]
        gm.w(SETB, bytes(counts))
        gm.w(SETB - 1, db(case.get("pre_byte", 2)))
        for i, r in enumerate(case.get("recs", [])):
            gm.w(rec_addr(i), r)

        # ---- scripted-callee state
        self.commit_script = list(case.get("cm", (1,)))
        self.commit_calls = 0
        self.eval_calls = 0
        self.patch = case.get("patch", (-1, 0, 0))
        self.trace, self.faults = [], []

        # ---- mutant byte patches
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)

        self.calls = []        # all-callee chatter (evidence, not compared)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in CALLS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def _ret(self, value):
        sp = self.uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.uc.mem_read(sp, 8))[0]
        self.uc.reg_write(UC_X86_REG_RSP, sp + 8)
        self.uc.reg_write(UC_X86_REG_RAX, value & 0xFFFFFFFFFFFFFFFF)
        self.uc.reg_write(UC_X86_REG_RIP, back)

    def _ridx(self, ptr):
        return (ptr - (SETB + RECS)) // STRIDE

    def on_call(self, uc, addr, size, _):
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        r8  = uc.reg_read(UC_X86_REG_R8)  & 0xFFFFFFFFFFFFFFFF
        r9  = uc.reg_read(UC_X86_REG_R9)  & 0xFFFFFFFFFFFFFFFF
        name = CALLS[addr]
        if addr == EVAL:
            # rdx=record, r8=&target u16, r9=&param i32; real body runs
            self.trace.append(("E%d" % self._ridx(rdx),))
            i = self.eval_calls
            self.eval_calls += 1
            on, idx, val = self.patch
            if i == on:
                self.gm.w(SETB + idx, db(val))
            return
        if addr == COMMIT:
            self.trace.append(("C%d" % self._ridx(rdx), "t%X" % (r8 & 0xFFFF),
                               "p%X" % (r9 & 0xFFFFFFFF)))
            i = self.commit_calls
            self.commit_calls += 1
            v = self.commit_script[i] if i < len(self.commit_script) \
                else self.commit_script[-1]
            self._ret(v)
            return
        if addr == NOTIFY:
            self.trace.append(("N", "t%X" % (rdx & 0xFFFF), "w%X" % (r8 & 0xFFFF),
                               "f%X" % (r9 & 0xFFFFFFFF)))
            return  # real body runs (002F8E90 etc. traced)
        if addr == SLOTRES:
            # per-slot hit resolver: record rdx, slot r9d.
            # stack args at callee entry: [rsp+0x28]=tbuf, [rsp+0x30]=out cursor
            cnt = struct.unpack("<H", self.gm.r(rdx + 6 + r9 * 6, 2))[0]
            hit = struct.unpack("<h", self.gm.r(rdx + 8 + r9 * 6, 2))[0]
            aux = struct.unpack("<H", self.gm.r(rdx + 10 + r9 * 6, 2))[0]
            self.trace.append(("S%d.%d" % (self._ridx(rdx), r9),
                               "c%d" % cnt, "r%d" % hit))
            sp = uc.reg_read(UC_X86_REG_RSP)
            out = struct.unpack("<Q", uc.mem_read(sp + 0x30, 8))[0]
            if hit > 0:
                # write the hit list the combiner would read:
                # {+1 mode, +4 cnt, +8 entries {objptr, score} stride 0x10}
                self.gm.w(out + 1, db(aux & 0xFF))
                self.gm.w(out + 4, dw(hit))
                for k in range(min(hit, 4)):
                    obj = HITOB + k * 0x40
                    recp = HITREC + k * 0x40
                    self.gm.w(obj + 0x30, qw(recp))
                    self.gm.w(recp + 8, dw(0x5000 + k))   # would-be param
                    self.gm.w(out + 8 + k * 0x10, qw(obj))
                    self.gm.w(out + 8 + k * 0x10 + 8, qw(0))  # score 0.0f
            self._ret(hit)
            return
        self.calls.append((name, "rcx=%x" % rcx, "rdx=%x" % rdx,
                           "r8=%x" % r8, "r9=%x" % r9))

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False

def run_case(case, raw, secs, iat):
    w = World(case, raw, secs, iat)
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    gm.w(sp + 0x28, b"\xCD" * 0x30)
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, UNITB)
    uc.reg_write(UC_X86_REG_RDX, 0 if case.get("null_set") else SETB)
    uc.reg_write(UC_X86_REG_R8, case.get("subgroup", 0) & 0xFFFFFFFF)
    uc.reg_write(UC_X86_REG_R9, case.get("resume", 0) & 0xFFFFFFFF)
    try:
        uc.emu_start(WALK, RETQ, count=16_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    ret = ctypes.c_int32(uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF).value
    tr = " ".join(" ".join(t) for t in w.trace)
    return ret, (tr if tr else "-"), w.faults, w

# ---- cases -------------------------------------------------------------------

def build_cases():
    """Records default to spec 0x4100 (spec-table hole -> eval 0)."""
    C_ = []
    def A(name, ret, trace, **kw):
        C_.append(dict(kw, name=name, want_ret=ret, want_trace=trace))

    NM   = rec_spec(spec=0x4200)                  # spec-table hole -> eval 0
    MT   = rec_spec(spec=0x4086, chance=0)        # roll arm, chance 0 -> eval 1
    SENT = rec_spec(spec=0xFFFF)                  # sentinel -> eval 0
    UARM = rec_spec(spec=0x300)                   # unit arm -> 2E9C00 -1 -> 0

    # a roll seed whose roll%100 lands >= 50 and one landing < 50, so the
    # chance gate is driven both ways through the real LCG
    s_hi, r_hi = pick_seed(lambda v: v >= 50)
    s_lo, r_lo = pick_seed(lambda v: v < 50)

    # 10.1 null set -> ret 0, empty trace
    A("null-set", 0, "-", null_set=1)
    # 10.3 empty subgroup -> ret 0, empty trace
    A("empty-sub", 0, "-", counts=[0] + [4] * 5, recs=[MT] * 6)
    A("empty-sub3", 0, "-", subgroup=3, counts=[2, 2, 2, 0, 4],
      recs=[MT] * 8)
    # subgroup 0/1 skip the offset loop; base = sum(counts[0..idx-1])
    A("sub0-match", 1, "E0 C0 t4086 p0", counts=[3, 2, 2], recs=[MT, NM, NM])
    A("sub1-match", 1, "E3 C3 t4086 p0", subgroup=1, counts=[3, 2, 2],
      recs=[NM, NM, NM, MT, NM])
    # even/odd subgroup indices -> unrolled pair loop + leftover
    A("sub2-walk", 1, "E3 C3 t4086 p0", subgroup=2, counts=[1, 2, 1, 2, 1, 3],
      recs=[NM] * 3 + [MT])
    A("sub3-walk", 1, "E4 C4 t4086 p0", subgroup=3, counts=[1, 2, 1, 2, 1, 3],
      recs=[NM] * 4 + [MT, NM])
    A("sub4-walk", 1, "E6 C6 t4086 p0", subgroup=4, counts=[1, 2, 1, 2, 1, 3],
      recs=[NM] * 6 + [MT])
    A("sub5-walk", 1, "E7 C7 t4086 p0", subgroup=5, counts=[1, 2, 1, 2, 1, 3],
      recs=[NM] * 7 + [MT])
    # matched-then-failed-commit continues to later records (contract 7)
    A("commit-fail-cont", 1,
      "E0 C0 t4086 p0 E1 C1 t4086 p0 E2 C2 t4086 p0",
      counts=[4], recs=[MT, MT, MT, NM], cm=(0, 0, 1))
    A("commit-never", 0,
      "E0 C0 t4086 p0 E1 C1 t4086 p0 E2 C2 t4086 p0 E3 C3 t4086 p0",
      counts=[4], recs=[MT] * 4, cm=(0, 0, 0, 0))
    A("eval-then-match", 1, "E0 E1 C1 t4086 p0", counts=[4],
      recs=[NM, MT, NM, NM], cm=(1,))
    A("all-nomatch", 0, "E0 E1 E2 E3", counts=[4], recs=[NM] * 4, cm=(1,))
    # resume bits: resuming (mode AND ctx 0x4000) -> only 0x40 records offered;
    # mode alone -> 0x80 records skipped
    A("res-40-skip", 1, "E1 E2 C2 t4086 p0", resume=1, ctx_at=-2,
      ctx_flags=0x4000, counts=[4],
      recs=[MT, rec_spec(spec=0x4200, flags=0x40),
            rec_spec(spec=0x4086, flags=0x40), MT])
    A("res-40-noctx", 1, "E0 E1 C1 t4086 p0", resume=1, ctx_at=-2,
      ctx_flags=0, counts=[4],
      recs=[NM, rec_spec(spec=0x4086, flags=0x40), NM, NM])
    A("res-80-skip", 1, "E0 E2 C2 t4086 p0", resume=1, ctx_at=-1,
      counts=[4],
      recs=[NM, rec_spec(spec=0x4086, flags=0x80), MT, NM])
    A("res-c0", 1, "E2 C2 t4086 p0", resume=1, ctx_at=-2,
      ctx_flags=0x4000, counts=[4],
      recs=[MT, rec_spec(spec=0x4086, flags=0xC0),
            rec_spec(spec=0x4086, flags=0x40), MT])
    A("res-mode0", 1, "E0 E1 E2 E3 C3 t4086 p0", counts=[4],
      recs=[NM, rec_spec(spec=0x4200, flags=0x80),
            rec_spec(spec=0x4200, flags=0x40), MT])
    # resume point: ctx == record addr -> ret 1 before evaluating it
    A("resume-at-rec", 1, "E0", resume=1, ctx_at=1,
      counts=[4], recs=[SENT, MT, MT, NM])
    # unrelated-bit separation: ctx 0x2001 (no 0x4000) must not pass resuming
    A("res-ctx-4001", 1, "E0 E1 C1 t4086 p0", resume=1, ctx_at=-2,
      ctx_flags=0x2001, counts=[4],
      recs=[NM, rec_spec(spec=0x4086, flags=0x40), NM, NM])
    # record flags 0x41 vs 0x40, 0x81 vs 0x80
    A("res-rec-41", 1, "E1 C1 t4086 p0", resume=1, ctx_at=-2,
      ctx_flags=0x4000, counts=[4],
      recs=[NM, rec_spec(spec=0x4086, flags=0x41), NM, NM])
    A("res-rec-81", 1, "E0 E2 C2 t4086 p0", resume=1, ctx_at=-1,
      counts=[4],
      recs=[NM, rec_spec(spec=0x4086, flags=0x81), MT, NM])
    # count byte re-read every iteration: rewritten mid-walk, shorter+longer
    A("count-shrink", 0, "E0 E1", counts=[4], recs=[NM, NM, MT, NM],
      patch=(1, 0, 1))                     # counts[0] -> 1 at eval call 1
    A("count-grow", 1, "E0 E1 E2 C2 t4086 p0", counts=[1],
      recs=[NM, NM, MT, NM], patch=(0, 0, 3))
    # third call: mode set AND word714 != 0xFFFF -> N after commit
    A("notify-sent", 1, "E0 C0 t4086 p0 N t4086 w20 f4",
      resume=1, word714=0x20, counts=[2], recs=[MT, NM])
    A("notify-sentinel", 1, "E0 C0 t4086 p0", resume=1, word714=0xFFFF,
      counts=[2], recs=[MT, NM])
    A("notify-nomode", 1, "E0 C0 t4086 p0", counts=[2], recs=[MT, NM],
      word714=0x20)
    # negative subgroup index: count byte read before the header (planted 2)
    A("neg-index", 1, "E0 E1 C1 t4086 p0", subgroup=-1, counts=[0, 4],
      recs=[NM, MT, NM, NM])
    # suspension bit kills every eval before any arm
    A("suspended", 0, "E0 E1 E2", counts=[3], recs=[MT, NM, MT], susp=0x20)
    # sentinel spec -> eval 0
    A("sentinel", 0, "E0 E1", counts=[2], recs=[SENT, NM])
    # unit-arm entry: spec < 0x4000 -> 002E9C00 -> -1 -> eval 0
    A("unit-arm-neg", 0, "E0 E1", counts=[2], recs=[UARM, NM])
    # roll gate through the real LCG: match iff roll%100 < chance
    A("roll-nomatch", 0, "E0 E1", counts=[2], lcg=s_hi,
      recs=[rec_spec(spec=0x4086, chance=r_hi), NM])       # roll >= chance
    A("roll-match", 1, "E0 C0 t4086 p0", counts=[2], lcg=s_lo,
      recs=[rec_spec(spec=0x4086, chance=r_lo + 1), NM])  # roll < chance
    # slot resolver: count>0 -> scripted 00301AD0; ret<=0 aborts eval
    A("slotfail", 0, "E0 S0.0 c1 r0 E1", counts=[2],
      recs=[rec_spec(spec=0x4086, slots=((1, 0, 0), (0, 0, 0), (0, 0, 0))), NM])
    A("slot-hit-match", 1, "E0 S0.0 c1 r2 C0 t4086 p0", counts=[2],
      recs=[MTS if False else
            rec_spec(spec=0x4086, chance=0,
                     slots=((1, 2, 0), (0, 0, 0), (0, 0, 0))), NM])
    return C_

# ---- mutants ------------------------------------------------------------------
# (name, va, bytes, why-killed). Patch sites verified against shipped bytes;
# va is the exact byte offset of the field being rewritten. Walk mutants target
# 00305CC0; eval mutants target 003014C0 / 00301830.

MUTANTS = [
    ("m-stride",     0x305E07, db(0x30),
     "add rbx,0x18 -> +0x30: record stride doubles, every offer shifts"),
    ("m-count-loop", 0x305E08, bytes.fromhex("3BFB"),
     "cmp edi,eax -> cmp edi,ebx: loop bound reads the wrong register"),
    ("m-respt",      0x305DA7, b"\x90" * 6,
     "je 0x305e5f removed: resume-point record is evaluated, not returned"),
    ("m-40gate",     0x305DB5, db(0x20),
     "record flag mask 0x40 -> 0x20: resuming records with 0x40 get offered"),
    ("m-80gate",     0x305DBF, db(0x40),
     "record flag mask 0x80 -> 0x40: mode-only skip reads wrong bit"),
    ("m-ctx4000",    0x305D75, bytes.fromhex("00200000"),
     "mov eax,0x4000 -> 0x2000: resuming computed from the wrong ctx bit"),
    ("m-commit",     0x305DFB, db(0x74),
     "jne -> je: commit-failure takes the success path"),
    ("m-notify-const", 0x305E4B, dw(5),
     "mov r9d,4 -> 5: notify kind arg changes"),
    ("m-notify-gate",  0x305E42, db(0xEB),
     "je -> jmp: word714==0xFFFF no longer suppresses the third call"),
    ("m-w714",       0x305CE9, bytes.fromhex("16070000"),
     "movzx [r13+0x714] -> +0x716: latched word read from the wrong offset"),
    ("m-susp",       0x301517, db(0x40),
     "test [0x2089340],0x20 -> 0x40: suspension bit never consulted"),
    ("m-eval-ret",   0x3016B0, db(0x8D),
     "jle -> jge: slot-resolver <=0 abort inverted"),
    ("m-roll",       0x301962, db(0x7C),
     "jge -> jl: chance gate inverted, chance records flip match/nomatch"),
    ("m-sx",         0x305CCC, bytes.fromhex("4489C090"),
     "movsxd rax,r8d -> mov eax,r8d: subgroup index loses sign extension"),
]

def main():
    raw, secs, iat = load_image()
    out = {"exe_sha256": SHA, "cases": [], "mutants": [], "faults": []}
    npass = nfail = 0
    for case in build_cases():
        ret, tr, faults, w = run_case(case, raw, secs, iat)
        ok = (ret == case["want_ret"] and tr == case["want_trace"]
              and not [f for f in faults if f[0] == "MEM"])
        npass += ok; nfail += (not ok)
        if not ok:
            print("FAIL %s  ret=%d want=%d\n  got:  %s\n  want: %s\n  faults=%s"
                  % (case["name"], ret, case["want_ret"], tr,
                     case["want_trace"], faults))
        else:
            print("PASS %s" % case["name"])
        out["cases"].append({"name": case["name"], "ret": ret,
                             "trace": tr, "ok": bool(ok),
                             "calls": w.calls,
                             "faults": faults})
    print("cases: %d/%d" % (npass, npass + nfail))

    base = {r[0]: (r[1], r[2]) for r in
            [(c["name"], c["ret"], c["trace"]) for c in out["cases"]]}
    for name, va, data, why in MUTANTS:
        # patch bytes are applied over the shipped image at canonical VAs
        n_diff = 0; diffs = []
        for case in build_cases():
            c = dict(case); c["patch_bytes"] = [(va, data)]
            try:
                ret, tr, faults, w = run_case(c, raw, secs, iat)
            except Exception as e:
                diffs.append((case["name"], "FAULT %s" % e))
                n_diff += 1
                continue
            if (ret, tr) != base[case["name"]] or \
               [f for f in faults if f[0] == "MEM"]:
                n_diff += 1
                diffs.append((case["name"], "ret=%d tr=%s f=%s" % (ret, tr, faults)))
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
