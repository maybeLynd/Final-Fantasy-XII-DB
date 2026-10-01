# EXP-086 - BattleStats_ChangeStatusAndProcessSideEffects (0030E360) isolated original-code
# execution.
#
# CONTRACT-status-write.md's dispatch surface was previously exercised only statically; the
# contract's own test matrix (six modes, already-in-state refusals, the ten named refusals,
# terminal dispatch, status-32 masking, the deliberate fault) names constructible offline work.
# This harness executes the shipped 0030E360 body at its canonical virtual address together
# with every bounded real callee whose semantics the contract owns:
#
#   REAL (executed as shipped):
#     0030E360  the operation itself (plus the in-image mode/case jump tables)
#     0030E360  the recursive self-call (real code, real re-entry)
#     0020E600  authored-offset codec resolver (EXP-083/084 subject)
#     00386A50  adding transition builder
#     00386A70  removing transition builder
#     003848E0  BattleResultRecord initialiser (via the builders)
#     003876D0  beat-duration default (row[+9] x beatScale x 30)
#     00387730  duration default (multi-row float formula, vitality-scaled)
#     0016D6A0  the ret-0 stand-in used for extraEffect on removing transitions
#     00808C40  __security_check_cookie (real; fixture cookie planted)
#
#   STUBBED WITH LOGGING (disclosed - deep side-effect systems outside the contract's
#   ownership; each patched to `ret` at its entry, arguments and order captured by a
#   per-address code hook, return value controlled per case):
#     0031B860  record->unit lookup (returns the planted unit or 0)
#     0030B9B0  low16 eligibility gate (controlled)
#     0030B8E0  high16/terminal eligibility gate (controlled)
#     00377C20  active-field bit15 predicate (controlled)
#     003112F0  transition-result applier
#     00300FC0  defeat cleanup
#     00312280  post-defeat rewards
#     00301140  recovery dispatch
#     003299B0  event dispatch (edx = event id)
#     00300140  case-4 predicate action
#     00307D10  case-4 secondary action
#     003284D0  status-applied reaction
#     0030FED0  final recompute
#     0046A800  add-direction extra effect
#
#   memset (IAT slot 008C2A60) resolves to a fixture rep-stosb implementation - the real
#   import is vcruntime140!memset; semantics identical, provenance disclosed.
#
# Executor signature (measured from the prologue):
#   rcx  = target BattleStatsRecord* (required; not null-checked)
#   rdx  = source BattleStatsRecord* (nullable)
#   r8b  = status id
#   r9d  = paramA (negative -> authored default)
#   [rsp+0x28] = paramB (negative -> authored default)   [caller's arg5]
#   [rsp+0x30] = flags                                  [caller's arg6]
#   [rsp+0x38] = mode                                   [caller's arg7]
#
# Key structure facts used by fixtures:
#   0031B860 is called on SOURCE first ([rsp+0x68] = source unit), then TARGET (rbx).
#   The two eligibility gates receive (rcx=target-unit, rdx=source-unit).
#   wasPresent = bit in (word2 | word1) - +0x38 is NOT part of presence, so mode 2/5
#   writes never trigger side effects.
#   The adding builder (00386A50) clears result+0x2C bit0 after init sets it, so the
#   transition applier 003112F0 can only fire on non-adding transitions.
#   The cascade's null-table path zeroes ecx and still executes mov eax,[rcx+0xC] -
#   a dereference of VA 0xC, not the contract's "empty mask, no dereference".

import hashlib, json, struct, sys, os

sys.path.insert(0, r"Database/Tools/work/ASTRA/python-libs")
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000  # canonical VAs already include it; never add it again

STATUS_BIN = (r"Database/Tools/work/repos-2d/vbf/ps2data/image/ff12/test_battle"
              r"/in/binaryfile/status_data.bin")

# ---- fixture map -------------------------------------------------------------
TGT   = 0x60001000   # target BattleStatsRecord (0x1C8)
SRC   = 0x60003000   # source BattleStatsRecord
UNIT  = 0x60005000   # BattleUnit (0xF50): +0x698 inner, +0x6B4/+0x714/+0xE9A predicate fields
INNER = 0x60007000   # unit's inner object: +4 type, +5 kind
HDR   = 0x60009000   # registry header: +8 stride(word), +0xC table offset(dword)
TBL   = 0x6000A000   # status_data rows planted verbatim
CODE  = 0x6000F000   # fixture memset implementation
STACK = 0x61000000
RETQ  = 0x62000000

EXEC = 0x30E360

# real bodies to execute
REAL = [
    (0x30E360, 0x5A0),   # body + mode jump table + case tables, all in-span
    (0x3848E0, 0x0D0),   # result-record init (ret at 0x3849AC)
    (0x386A50, 0x0A0),   # both builders
    (0x3876D0, 0x060),   # beat default
    (0x387730, 0x300),   # duration default (generous; ends ~0x3879Bx)
    (0x20E600, 0x040),   # codec resolver
    (0x16D6A0, 0x010),   # ret-0 stand-in
    (0x808C40, 0x020),   # __security_check_cookie
    (0x861EC0, 0x010),   # memset import thunk: jmp [IAT] -> fixture memset
]

# stubbed callees (name, va) - patched to `ret`; hook logs args and sets rax
STUBS = {
    0x31B860: "unit_lookup",
    0x30B9B0: "gate_low16",
    0x30B8E0: "gate_high16",
    0x377C20: "field_bit15",
    0x3112F0: "applier",
    0x300FC0: "defeat_cleanup",
    0x312280: "rewards",
    0x301140: "recover",
    0x3299B0: "event",
    0x300140: "case4_action",
    0x307D10: "case4_second",
    0x3284D0: "reaction",
    0x30FED0: "recompute",
    0x46A800: "extra_add",
}

G_COOKIE  = 0x1F44830   # __security_cookie
G_REG     = 0x2EBF118   # status-definition registry slot
G_CODEC   = 0x1F83530   # authored-offset codec base
G_BEAT    = 0x1DFE0B4   # beat-duration scale
IAT_MEMSET = 0x8C2A60   # memset import slot

COOKIE = 0x0000DEADBEEF  # top 16 bits zero - passes the real check's rol/test gate

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)

# ---- PE extraction -----------------------------------------------------------
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

# fixture memset: rcx=dst, dl=fill, r8=len -> rax=dst
MEMSET_FN = bytes.fromhex("4889c8574889cf88d04c89c1f3aa5fc3")

# ---- world -------------------------------------------------------------------
def build_world(case, rd):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)

    pages = set()
    for va, n in REAL:
        p0 = va & ~0xFFF
        p1 = (va + n + 0xFFF) & ~0xFFF
        for p in range(p0, p1, 0x1000):
            pages.add(p)
    for va in STUBS:
        pages.add(va & ~0xFFF)
    for g in (G_COOKIE, G_REG, G_CODEC, G_BEAT, IAT_MEMSET):
        pages.add(g & ~0xFFF)
    pages.add(0x8F3000)  # .rdata constant the duration formula divides by (0x8F3134)
    for p in sorted(pages):
        uc.mem_map(p, 0x1000)

    for va, n in REAL:
        uc.mem_write(va, rd(va, n))
    uc.mem_write(0x8F3000, rd(0x8F3000, 0x1000))

    for va in STUBS:
        uc.mem_write(va, b"\xc3")          # ret - the hook supplies rax

    for a, s in [(0x60000000, 0x20000), (STACK, 0x100000), (RETQ, 0x1000)]:
        uc.mem_map(a, s)
    uc.mem_write(RETQ, b"\xc3")
    uc.mem_write(CODE, MEMSET_FN)
    uc.mem_write(IAT_MEMSET, qw(CODE))

    # ---- globals
    uc.mem_write(G_COOKIE, qw(COOKIE))
    uc.mem_write(G_CODEC, qw(case.get("codec_base", 0)))
    uc.mem_write(G_BEAT, dw(case.get("beat_scale", 4)))
    hdr_ptr = case.get("hdr", HDR)
    uc.mem_write(G_REG, qw(hdr_ptr))

    # ---- definition table (real shipped rows)
    rows = open(STATUS_BIN, "rb").read()[0x20:]
    uc.mem_write(TBL, rows)
    if hdr_ptr:
        uc.mem_write(HDR + 8, struct.pack("<H", 0x28))
        uc.mem_write(HDR + 0xC, dw(case.get("tbl_off", TBL)))

    # ---- records
    def record(base, masks, vitality, hp, kind):
        uc.mem_write(base, b"\0" * 0x1C8)
        uc.mem_write(base + 0x2C, bytes([vitality]))
        uc.mem_write(base + 0x48, dw(hp))
        uc.mem_write(base + 0x38, dw(masks.get(0x38, 0)))
        uc.mem_write(base + 0x3C, dw(masks.get(0x3C, 0)))
        uc.mem_write(base + 0x64, dw(masks.get(0x64, 0)))
        uc.mem_write(base + 5, bytes([kind]))        # kind byte read by case-2/5 arms
    record(TGT, case.get("tgt", {}), case.get("vit", 50), case.get("hp", 1000), 0)
    record(SRC, case.get("src", {}), case.get("src_vit", 60), 2000, case.get("src_kind", 0))

    # ---- unit + inner
    uc.mem_write(UNIT, b"\0" * 0x1000)
    uc.mem_write(UNIT, dw(case.get("unit_flags", 0)))
    uc.mem_write(UNIT + 0x698, qw(INNER if case.get("has_inner", True) else 0))
    uc.mem_write(UNIT + 0x6B4, bytes([case.get("u_6b4", 0)]))
    uc.mem_write(UNIT + 0x714, struct.pack("<H", case.get("u_714", 0)))
    uc.mem_write(UNIT + 0xE9A, bytes([case.get("u_e9a", 0)]))
    uc.mem_write(INNER + 4, bytes([case.get("inner_type", 0x1B)]))
    uc.mem_write(INNER + 5, bytes([case.get("inner_kind", 0)]))

    # ---- mutants (byte patches on the shipped body)
    for va, data in case.get("patch", []):
        uc.mem_write(va, data)

    # ---- hooks
    trace = []     # ordered stub calls
    entries = []   # 0030E360 entries (recursion visible)
    faults = []    # (access, addr, pc) of unmapped accesses
    rets = case.get("rets", {})

    def stub_ret(va, rcx):
        r = rets.get(va, 0)
        if va == 0x31B860:
            if rcx == SRC:
                return case.get("unit_src", 0)
            if rcx == TGT:
                return case.get("unit_tgt", UNIT)
            return 0
        return r

    def on_stub(uc_, addr, size, _):
        sp = uc_.reg_read(UC_X86_REG_RSP)
        arg5 = struct.unpack("<Q", uc_.mem_read(sp + 0x28, 8))[0]
        arg6 = struct.unpack("<Q", uc_.mem_read(sp + 0x30, 8))[0]
        trace.append({
            "at": STUBS[addr],
            "rcx": uc_.reg_read(UC_X86_REG_RCX),
            "rdx": uc_.reg_read(UC_X86_REG_RDX),
            "r8":  uc_.reg_read(UC_X86_REG_R8),
            "r9":  uc_.reg_read(UC_X86_REG_R9),
            "a5":  arg5, "a6": arg6,
        })
        uc_.reg_write(UC_X86_REG_RAX, stub_ret(addr, uc_.reg_read(UC_X86_REG_RCX)))

    def on_entry(uc_, addr, size, _):
        sp = uc_.reg_read(UC_X86_REG_RSP)
        a5 = struct.unpack("<i", uc_.mem_read(sp + 0x28, 4))[0]
        fl = struct.unpack("<I", uc_.mem_read(sp + 0x30, 4))[0]
        md = struct.unpack("<i", uc_.mem_read(sp + 0x38, 4))[0]
        entries.append({
            "rcx": uc_.reg_read(UC_X86_REG_RCX),
            "rdx": uc_.reg_read(UC_X86_REG_RDX),
            "st":  uc_.reg_read(UC_X86_REG_R8) & 0xFF,
            "pa":  uc_.reg_read(UC_X86_REG_R9),
            "pb": a5, "flags": fl, "mode": md,
        })

    def on_bad(uc_, access, addr, size, value, _):
        faults.append((access, addr, uc_.reg_read(UC_X86_REG_RIP)))
        return False   # do not service - let the error propagate like a real fault

    for va in STUBS:
        uc.hook_add(UC_HOOK_CODE, on_stub, begin=va, end=va)
    uc.hook_add(UC_HOOK_CODE, on_entry, begin=EXEC, end=EXEC)
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)
    return uc, trace, entries, faults

def run_case(case, rd):
    uc, trace, entries, faults = build_world(case, rd)
    sp = STACK + 0x80000
    uc.mem_write(sp, qw(RETQ))
    uc.mem_write(sp + 0x28, dw(case.get("paramB", 0)))
    uc.mem_write(sp + 0x30, dw(case.get("flags", 0)))
    uc.mem_write(sp + 0x38, dw(case.get("mode", 0)))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, TGT)
    uc.reg_write(UC_X86_REG_RDX, case.get("src_ptr", SRC))
    uc.reg_write(UC_X86_REG_R8,  case.get("status", 7))
    uc.reg_write(UC_X86_REG_R9D, case.get("paramA", 0) & 0xFFFFFFFF)
    fault = None
    try:
        uc.emu_start(EXEC, RETQ, count=400000)
    except Exception as e:
        fault = str(e)
    def rd32(a): return struct.unpack("<I", uc.mem_read(a, 4))[0]
    def rd16(a): return struct.unpack("<H", uc.mem_read(a, 2))[0]
    st = case.get("status", 7) & 0xFF
    snap = {
        "fault": fault,
        "faults": faults,
        "w38": rd32(TGT + 0x38), "w3C": rd32(TGT + 0x3C), "w64": rd32(TGT + 0x64),
        "paramA_st":  rd32(TGT + 0xBC + 4 * min(st, 33)),
        "paramA_32":  rd32(TGT + 0xBC + 4 * 32),     # status-32 slot lands at +0x13C
        "timer_st":   rd16(TGT + 0x13C + 2 * min(st, 33)),
        "timer_32":   rd16(TGT + 0x13C + 2 * 32),    # status-32 slot lands at +0x17C
        "u_e9a":  uc.mem_read(UNIT + 0xE9A, 1)[0],
        "trace":  trace,
        "entries": entries,
        "nv_ok": all(uc.reg_read(r) == 0 for r in
                     (UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI,
                      UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15)),
    }
    return snap

# ---- cases -------------------------------------------------------------------
def cases():
    C = lambda **k: k
    # shorthand: which stubs appear in a normal non-adding transition (mode0/1/2/5 on
    # a presence-changing write): builder is real; applier + recover-or-tail + recompute
    # are stubs. For adding (mode3/4): no applier (builder cleared bit0), but
    # reaction + extra_add appear when a unit exists.
    return [
        # ---- mode table ------------------------------------------------------
        C(name="m0-set", status=7, mode=0, tgt={0x64: 0x80}, paramA=11, paramB=12,
          why="mode0 clears +0x64: presence flips, arrays written (initialising), removing builder -> applier fires"),
        C(name="m0-absent", status=7, mode=0,
          why="mode0 on a clear bit refuses: nothing is written, no side effects"),
        C(name="m1-set", status=7, mode=1, tgt={0x3C: 0x80}, paramA=11, paramB=12,
          why="mode1 clears +0x3C (initialising? no - only modes 0/3) -> arrays untouched"),
        C(name="m1-absent", status=7, mode=1, why="mode1 on a clear bit refuses"),
        C(name="m2-set", status=7, mode=2, tgt={0x38: 0x80},
          why="mode2 clears +0x38: presence does not include +0x38 -> write lands, no side effects, no arrays"),
        C(name="m2-absent", status=7, mode=2, why="mode2 on a clear bit refuses"),
        C(name="m3-set", status=7, mode=3, paramA=11, paramB=12,
          why="mode3 sets +0x64, writes arrays, adding builder -> applier skipped, reaction + extra_add fire"),
        C(name="m3-conflict", status=7, mode=3, tgt={0x38: 0x80},
          why="mode3 refuses when the bit is already set in +0x38"),
        C(name="m3-already", status=7, mode=3, tgt={0x64: 0x80},
          why="mode3 refuses when the bit is already set in +0x64"),
        C(name="m4-set", status=7, mode=4,
          why="mode4 sets +0x3C: adding, but not initialising -> arrays untouched"),
        C(name="m4-already", status=7, mode=4, tgt={0x3C: 0x80}, why="mode4 on a set bit refuses"),
        C(name="m5-set", status=7, mode=5,
          why="mode5 sets +0x38: presence unchanged -> early return, zero side effects"),
        C(name="m5-already", status=7, mode=5, tgt={0x38: 0x80}, why="mode5 on a set bit refuses"),
        C(name="m6", status=7, mode=6, why="mode>5 refuses before touching anything"),
        C(name="m-neg", status=7, mode=-1,
          why="mode -1: movsxd makes eax FFFFFFFF; unsigned ja refuses"),
        # ---- eligibility gates -------------------------------------------------
        C(name="g1-refuse", status=7, mode=3, rets={0x30B9B0: 1},
          why="low16 gate nonzero with flags bit0 clear -> early return, mask untouched"),
        C(name="g2-term", status=1, mode=3, rets={0x30B8E0: 1},
          why="high16 gate nonzero on a TERMINAL status -> refuse"),
        C(name="g2-nonterm", status=7, mode=3, rets={0x30B8E0: 1}, paramA=1, paramB=2,
          why="high16 gate nonzero on a non-terminal status -> the refusal is skipped"),
        C(name="flag0-bypass", status=7, mode=3, flags=1, paramA=1, paramB=2,
          rets={0x30B9B0: 1, 0x30B8E0: 1},
          why="flags bit0: both gates are skipped entirely - stubs never called"),
        # ---- party-type terminal handling -------------------------------------
        C(name="party-term", status=1, mode=3,
          why="adding Stone to a party-type unit (inner kind0, type 0x1B): defeat_cleanup only, masks untouched"),
        C(name="party-otype", status=1, mode=3, inner_type=0x28, paramA=1, paramB=2,
          why="inner type 0x28 is out of the 0x1B..0x27 band: normal apply path"),
        C(name="party-kind1", status=1, mode=3, inner_kind=1, paramA=1, paramB=2,
          why="inner kind nonzero: normal apply path"),
        C(name="term-second-blocked", status=1, mode=3, inner_type=0x28, tgt={0x64: 1},
          why="adding Stone while KO already present and field-bit15 clear -> refuse"),
        C(name="term-second-allowed", status=1, mode=3, inner_type=0x28, tgt={0x64: 1},
          rets={0x377C20: 1}, paramA=1, paramB=2,
          why="same but field-bit15 set -> the refusal is bypassed"),
        # ---- defaults / arrays -------------------------------------------------
        C(name="def-paramA", status=8, mode=3, paramA=-1, paramB=0,
          why="paramA<0: 00387730 computes the authored duration for status 8 (dur=50, flag 0x2000 set, vitality-scaled)"),
        C(name="def-paramB", status=8, mode=3, paramA=0, paramB=-1,
          why="paramB<0: 003876D0 computes beat 120 x scale 4 x 30 = 14400"),
        C(name="expl-params", status=8, mode=3, paramA=0x11223344, paramB=0xAABB,
          why="non-negative params stored verbatim"),
        C(name="m4-noarrays", status=8, mode=4, paramA=-1, paramB=-1,
          why="mode4 is adding but NOT initialising: negative params are ignored, arrays untouched"),
        # ---- cascade -----------------------------------------------------------
        C(name="cascade-10", status=10, mode=4, tgt={0x64: 1 << 25},
          why="status10 clearMask has bit25: the real shipped row drives one recursive mode-0 clear of +0x64 bit25, inner call sees flags|0x200"),
        C(name="cascade-absent", status=10, mode=4,
          why="clearMask fires regardless of target state: inner mode0 on absent bit25 refuses inside"),
        C(name="cascade-20", status=20, mode=4, tgt={0x64: 1 << 15},
          why="status20 clearMask bit15: second shipped-row witness"),
        # ---- terminal dispatch ---------------------------------------------------
        C(name="t0-add", inner_type=0x28, status=0, mode=4,
          why="KO added: case0 adding arm -> defeat_cleanup(unit,0) then rewards(src,unit)"),
        C(name="t0-remove", status=0, mode=1, tgt={0x3C: 1},
          why="KO removed: case0 non-adding -> recover(unit)"),
        C(name="t1-add", inner_type=0x28, status=1, mode=4,
          why="Stone added: case1 -> event 0x200C then cleanup+rewards"),
        C(name="t1-remove", status=1, mode=1, tgt={0x3C: 2},
          why="Stone removed: case1 -> recover only"),
        C(name="t31-add", inner_type=0x28, status=31, mode=4,
          why="Vanished added: case6 -> event 0x200E then cleanup+rewards"),
        C(name="t31-remove", status=31, mode=1, tgt={0x3C: 1 << 31},
          why="Vanished removed: recover only"),
        C(name="t4-add", status=4, mode=4, why="Sleep added: case3 -> event 0x2001"),
        C(name="t4-remove", status=4, mode=1, tgt={0x3C: 0x10},
          why="Sleep removed: case3 -> same event 0x2001"),
        C(name="t5-add-allow", status=5, mode=4, u_714=0x200,
          why="Confuse added, predicate allows: case4 -> case4_action(unit,1)+case4_second(unit)"),
        C(name="t5-add-deny", status=5, mode=4, unit_flags=1 << 24, u_714=0x113,
          why="Confuse added, word[+0x714]==0x113: case4 -> case4_action(unit,0)"),
        C(name="t5-remove", status=5, mode=1, tgt={0x3C: 0x20},
          u_714=0x200,
          why="case4 runs its predicate on REMOVES too - no adding test in that arm"),
        C(name="t27-add", status=27, mode=4, u_714=0x200,
          why="Berserk shares case4 with Confuse"),
        C(name="t2-add-src", status=2, mode=4,
          why="Petrify added with a kind-0 source: unit+0xE9A bit1 set"),
        C(name="t2-add-nosrc", status=2, mode=4, src_ptr=0,
          why="Petrify added with NULL source: bit1 stays clear"),
        C(name="t8-add", status=8, mode=4,
          why="Poison added with kind-0 source: unit+0xE9A bit0 set"),
        C(name="t6-add", status=6, mode=4,
          why="Doom has no terminal case (case7 shared tail): only the recompute stub fires"),
        C(name="null-unit", status=1, mode=4, unit_tgt=0,
          why="unit lookup returns 0: terminal dispatch skipped, mask still written"),
        # ---- status-32 masking ---------------------------------------------------
        C(name="st32-mode4", status=32, mode=4, inner_type=0x30,
          why="status 32: shl masks the count to 0 -> bit0 (KO's own bit) in +0x3C; terminal gates still see the terminal bit; dispatch table skipped (32>31)"),
        C(name="st32-mode3", status=32, mode=3, inner_type=0x30, paramA=77, paramB=88,
          why="status 32 initialising: paramA[32] lands at +0x13C (timer[0]), timer[32] lands at +0x17C past the array"),
        # ---- deliberate faults ---------------------------------------------------
        C(name="fault-def-a", status=8, mode=3, hdr=0, paramA=-1, paramB=0,
          why="registry null + paramA default: 00387730 derefs [rcx+8] with rcx=0 -> read fault at VA 8"),
        C(name="fault-def-b", status=8, mode=3, hdr=0, paramA=0, paramB=-1,
          why="registry null + paramB default: 003876D0 derefs [rcx+9] -> read fault at VA 9"),
        C(name="fault-casc", status=10, mode=4, hdr=0, tgt={0x64: 1 << 25},
          why="registry null + adding: the cascade's 'guarded' path still executes mov eax,[rcx+0xC] with rcx=0 -> read fault at VA 0xC (refutes the contract's no-deref claim)"),
        C(name="fault-casc-nullbase", status=10, mode=4, tbl_off=0, tgt={0x64: 1 << 25},
          why="registry present, table offset 0 with codec base 0: resolver returns 0 -> same [0xC] fault"),
        # ---- flag bits -------------------------------------------------------------
        C(name="flag9-skip", status=4, mode=4, flags=0x200,
          why="flags bit9: the tail recompute is skipped"),
        C(name="flag1-skip", status=7, mode=4, flags=0x2,
          why="flags bit1: extra effect skipped - no extra_add call"),
        C(name="flag4-skip", status=7, mode=4, flags=0x10,
          why="flags bit4: the applied-reaction call is skipped"),
        C(name="src-null", status=7, mode=3, src_ptr=0, paramA=1, paramB=2,
          why="source NULL: gates get rdx=0, everything else proceeds"),
        # ---- mutants ---------------------------------------------------------------
        C(name="mut-addmask", status=7, mode=0, tgt={0x64: 0x80}, paramA=1, paramB=2,
          patch=[(0x30E3C9, b"\x93")],    # setbe -> setae: mode0 counted as 'adding'
          why="MUTANT: removing becomes adding - builder swapped, applier skipped, reaction fires"),
        C(name="mut-init3", status=7, mode=3, paramA=11, paramB=12,
          patch=[(0x30E3DD, b"\x04")],    # cmp edx,3 -> cmp edx,4
          why="MUTANT: mode3 loses initialising - arrays stay zero"),
        C(name="mut-bound6", status=7, mode=6,
          patch=[(0x30E4CD, b"\x07")],    # cmp eax,5 -> cmp eax,7
          why="MUTANT: mode6 reads jump-table[6] = the case-target table's head -> lands in the case0 arm"),
        C(name="mut-termmask", status=1, mode=3, inner_type=0x28, rets={0x30B8E0: 1}, paramA=1, paramB=2,
          patch=[(0x30E456, b"\x01")],    # test edi,0x80000003 -> 0x80000001
          why="MUTANT: Stone no longer 'terminal' for the gate2 refusal -> apply proceeds"),
        C(name="mut-mode0-not", status=7, mode=0, tgt={0x64: 0x80}, paramA=1, paramB=2,
          patch=[(0x30E4F4, b"\x87\xc0")], # not eax -> xchg eax,eax
          why="MUTANT: mode0 writes the bit back unchanged -> presence-equal early return"),
        C(name="mut-shl", status=7, mode=3, inner_type=0x28, paramA=11, paramB=12,
          patch=[(0x30E410, b"\xd1\xe7")], # shl edi,cl -> shl edi,1
          why="MUTANT: every status collapses to bit1"),
        C(name="mut-pres-src", status=7, mode=5,
          patch=[(0x30E5BC, b"\x38")],    # or eax,[rsi+0x64] -> [rsi+0x38]
          why="MUTANT: the AFTER presence read includes +0x38 -> mode5 now 'changes presence' and fires side effects"),
        C(name="mut-cascflag", status=10, mode=4, tgt={0x64: 1 << 25},
          patch=[(0x30E6B1, b"\x08")],    # bts eax,9 -> bts eax,8
          why="MUTANT: cascade calls get flags|0x100 not |0x200 -> inner recompute fires"),
        C(name="mut-termbound", status=32, mode=4, inner_type=0x30,
          patch=[(0x30E739, b"\x20")],    # cmp ecx,0x1F -> 0x20
          why="MUTANT: status32 indexes case-byte[32] - one past the table"),
    ]

# ---- expectations --------------------------------------------------------------
def tr(s, name): return [t for t in s["trace"] if t["at"] == name]
def names(s): return [t["at"] for t in s["trace"]]
# refusals still run the front pipeline: unit lookup x2, low16 gate, and (for the
# adding modes 3/4) the high16 gate. The mode arm's refusal is what stops the rest.
PRE  = ["unit_lookup", "unit_lookup", "gate_low16"]
PREA = PRE + ["gate_high16"]
def expect(c, s):
    F = []
    def chk(what, got, want):
        if got != want:
            F.append("%s: got %r want %r" % (what, got, want))
    n = c["name"]

    if n == "m0-set":
        chk("fault", s["fault"], None)
        chk("w64", s["w64"], 0)
        chk("paramA", s["paramA_st"], 11)
        chk("timer", s["timer_st"], 12)
        chk("applier", len(tr(s, "applier")), 0)   # BOTH builders clear result+0x2C bit0
        chk("recover", len(tr(s, "recover")), 0)
        chk("recompute", len(tr(s, "recompute")), 1)
        chk("reaction", len(tr(s, "reaction")), 0)      # removing: no reaction
        chk("extra_add", len(tr(s, "extra_add")), 0)   # removing -> the ret-0 stand-in
        chk("entries", len(s["entries"]), 1)
        return F
    if n in ("m0-absent", "m1-absent", "m2-absent", "m5-already", "m6", "m-neg"):
        chk("fault", s["fault"], None)
        chk("trace", names(s), PRE)
        chk("w38", s["w38"], c.get("tgt", {}).get(0x38, 0))
        chk("w3C", s["w3C"], c.get("tgt", {}).get(0x3C, 0))
        chk("w64", s["w64"], c.get("tgt", {}).get(0x64, 0))
        return F
    if n in ("m3-conflict", "m3-already", "m4-already"):
        chk("fault", s["fault"], None)
        chk("trace", names(s), PREA)
        chk("w38", s["w38"], c.get("tgt", {}).get(0x38, 0))
        chk("w3C", s["w3C"], c.get("tgt", {}).get(0x3C, 0))
        chk("w64", s["w64"], c.get("tgt", {}).get(0x64, 0))
        return F
    if n == "m1-set":
        chk("w3C", s["w3C"], 0)
        chk("paramA", s["paramA_st"], 0)   # not initialising
        chk("applier", len(tr(s, "applier")), 0)
        chk("recompute", len(tr(s, "recompute")), 1)
        return F
    if n == "m2-set":
        chk("w38", s["w38"], 0)
        chk("trace", names(s), PRE)      # +0x38 is not presence: no side effects
        chk("paramA", s["paramA_st"], 0)
        return F
    if n == "m3-set":
        chk("w64", s["w64"], 0x80)
        chk("paramA", s["paramA_st"], 11)
        chk("timer", s["timer_st"], 12)
        chk("applier", len(tr(s, "applier")), 0)       # adding builder cleared bit0
        chk("reaction", len(tr(s, "reaction")), 1)
        chk("extra_add", len(tr(s, "extra_add")), 1)
        chk("recompute", len(tr(s, "recompute")), 1)
        chk("cleanup", len(tr(s, "defeat_cleanup")), 0)  # st7 -> case7
        return F
    if n == "m4-set":
        chk("w3C", s["w3C"], 0x80)
        chk("paramA", s["paramA_st"], 0)   # not initialising
        chk("reaction", len(tr(s, "reaction")), 1)
        chk("extra_add", len(tr(s, "extra_add")), 1)
        chk("recompute", len(tr(s, "recompute")), 1)
        return F
    if n == "m5-set":
        chk("w38", s["w38"], 0x80)
        chk("trace", names(s), PRE)
        return F
    if n == "g1-refuse":
        chk("w64", s["w64"], 0)
        chk("trace", names(s), PRE)
        return F
    if n == "g2-term":
        chk("w64", s["w64"], 0)
        chk("gate_high16", len(tr(s, "gate_high16")), 1)
        return F
    if n == "g2-nonterm":
        chk("w64", s["w64"], 0x80)
        chk("gate_high16", len(tr(s, "gate_high16")), 1)
        return F
    if n == "flag0-bypass":
        chk("w64", s["w64"], 0x80)
        chk("gates", len(tr(s, "gate_low16")) + len(tr(s, "gate_high16")), 0)
        return F
    if n == "party-term":
        chk("w64", s["w64"], 0)
        chk("trace", names(s), PREA + ["defeat_cleanup"])
        c0 = tr(s, "defeat_cleanup")[0]
        chk("cleanup args", (c0["rcx"], c0["rdx"]), (UNIT, 0))
        return F
    if n in ("party-otype", "party-kind1"):
        chk("w64", s["w64"], 2)            # mode3 sets bit1 in +0x64
        chk("cleanup_at_end", len(tr(s, "defeat_cleanup")), 1)  # terminal case fires after write
        chk("event id", tr(s, "event")[0]["rdx"], 0x200C)
        return F
    if n == "term-second-blocked":
        chk("w64", s["w64"], 1)
        chk("trace", names(s), PREA + ["field_bit15"])
        return F
    if n == "term-second-allowed":
        chk("w64", s["w64"], 3)      # KO bit already there, Stone bit added
        chk("field_bit15", len(tr(s, "field_bit15")), 1)
        return F
    if n == "def-paramA":
        chk("paramA_nonzero", s["paramA_st"] != 0 and s["paramA_st"] != 0xFFFFFFFF, True)
        chk("paramA_val", s["paramA_st"], s["paramA_st"])  # recorded, value is the evidence
        return F
    if n == "def-paramB":
        chk("timer", s["timer_st"], 120 * 4 * 30)
        return F
    if n == "expl-params":
        chk("paramA", s["paramA_st"], 0x11223344)
        chk("timer", s["timer_st"], 0xAABB)
        return F
    if n == "m4-noarrays":
        chk("paramA", s["paramA_st"], 0)
        chk("timer", s["timer_st"], 0)
        return F
    if n == "cascade-10":
        chk("entries", len(s["entries"]), 2)
        inner = s["entries"][1]
        chk("inner st/mode", (inner["st"], inner["mode"]), (25, 0))
        chk("inner params", (inner["pa"], inner["pb"]), (0, 0))
        chk("inner flags", inner["flags"] & 0x200, 0x200)
        chk("w64", s["w64"], 0)          # bit25 cleared by the recursive call
        chk("recompute", len(tr(s, "recompute")), 1)  # outer only
        return F
    if n == "cascade-absent":
        chk("entries", len(s["entries"]), 2)
        chk("w64", s["w64"], 0)
        return F
    if n == "cascade-20":
        chk("entries", len(s["entries"]), 2)
        chk("inner st", s["entries"][1]["st"], 15)
        chk("w64", s["w64"], 0)
        return F
    if n == "t0-add":
        chk("w3C", s["w3C"], 1)
        chk("cleanup", len(tr(s, "defeat_cleanup")), 1)
        chk("rewards", len(tr(s, "rewards")), 1)
        r = tr(s, "rewards")[0]
        chk("rewards args", (r["rcx"], r["rdx"]), (SRC, UNIT))
        chk("recover", len(tr(s, "recover")), 0)
        return F
    if n == "t0-remove":
        chk("w3C", s["w3C"], 0)
        chk("recover", len(tr(s, "recover")), 1)
        chk("recover arg", tr(s, "recover")[0]["rcx"], UNIT)
        chk("cleanup", len(tr(s, "defeat_cleanup")), 0)
        return F
    if n == "t1-add":
        ev = tr(s, "event")
        chk("event", len(ev), 1)
        chk("event id", ev[0]["rdx"], 0x200C)
        chk("cleanup", len(tr(s, "defeat_cleanup")), 1)
        chk("rewards", len(tr(s, "rewards")), 1)
        return F
    if n in ("t1-remove", "t31-remove"):
        chk("recover", len(tr(s, "recover")), 1)
        chk("event", len(tr(s, "event")), 0)
        chk("cleanup", len(tr(s, "defeat_cleanup")), 0)
        return F
    if n == "t31-add":
        ev = tr(s, "event")
        chk("event id", ev[0]["rdx"], 0x200E)
        chk("cleanup", len(tr(s, "defeat_cleanup")), 1)
        return F
    if n in ("t4-add", "t4-remove"):
        ev = tr(s, "event")
        chk("event", len(ev), 1)
        chk("event id", ev[0]["rdx"], 0x2001)
        chk("cleanup", len(tr(s, "defeat_cleanup")), 0)
        return F
    if n in ("t5-add-allow", "t27-add"):
        a = tr(s, "case4_action")
        chk("case4_action", len(a), 1)
        chk("predicate", a[0]["rdx"], 1)
        chk("case4_second", len(tr(s, "case4_second")), 1)
        return F
    if n == "t5-add-deny":
        a = tr(s, "case4_action")
        chk("predicate", a[0]["rdx"], 0)
        return F
    if n == "t5-remove":
        chk("case4_action", len(tr(s, "case4_action")), 1)
        return F
    if n == "t2-add-src":
        chk("u_e9a", s["u_e9a"] & 2, 2)
        return F
    if n == "t2-add-nosrc":
        chk("u_e9a", s["u_e9a"] & 2, 0)
        return F
    if n == "t8-add":
        chk("u_e9a", s["u_e9a"] & 1, 1)
        return F
    if n == "t6-add":
        chk("cleanup+recover+event",
            len(tr(s, "defeat_cleanup")) + len(tr(s, "recover")) + len(tr(s, "event")), 0)
        chk("recompute", len(tr(s, "recompute")), 1)
        return F
    if n == "null-unit":
        chk("w3C", s["w3C"], 2)
        chk("cleanup", len(tr(s, "defeat_cleanup")), 0)
        chk("recompute", len(tr(s, "recompute")), 1)
        return F
    if n == "st32-mode4":
        chk("w3C", s["w3C"], 1)            # bit0 = KO's own bit
        chk("cleanup", len(tr(s, "defeat_cleanup")), 0)  # dispatch skipped
        chk("recompute", len(tr(s, "recompute")), 1)
        return F
    if n == "st32-mode3":
        chk("w64", s["w64"], 1)
        chk("paramA_32", s["paramA_32"], 77)     # landed at +0x13C = timer[0] dword
        chk("timer_32", s["timer_32"], 88)       # landed at +0x17C = past the array
        return F
    if n in ("fault-def-a", "fault-def-b", "fault-casc", "fault-casc-nullbase"):
        chk("fault", s["fault"] is not None, True)
        want = {"fault-def-a": 8, "fault-def-b": 9,
                "fault-casc": 0xC, "fault-casc-nullbase": 0xC}[n]
        addrs = [a for _, a, _ in s["faults"]]
        chk("fault addr", want in addrs, True)
        return F
    if n == "flag9-skip":
        chk("recompute", len(tr(s, "recompute")), 0)
        chk("event", len(tr(s, "event")), 1)
        return F
    if n == "flag1-skip":
        chk("extra_add", len(tr(s, "extra_add")), 0)
        chk("w3C", s["w3C"], 0x80)
        return F
    if n == "flag4-skip":
        chk("reaction", len(tr(s, "reaction")), 0)
        return F
    if n == "src-null":
        chk("w64", s["w64"], 0x80)
        g = tr(s, "gate_low16")[0]
        chk("gate src arg", g["rdx"], 0)
        return F
    # ---- mutants: each must diverge from its baseline -------------------------
    if n == "mut-addmask":
        chk("w64", s["w64"], 0)                     # the clear still happened
        chk("applier", len(tr(s, "applier")), 0)    # but as 'adding': no applier
        chk("reaction", len(tr(s, "reaction")), 1)  # and the reaction ran
        return F
    if n == "mut-init3":
        chk("w64", s["w64"], 0x80)
        chk("paramA", s["paramA_st"], 0)
        return F
    if n == "mut-bound6":
        # jt[6] lands in the case0 arm with edi still holding the status BIT
        # (the adding-flag reload at 0030E5E6 was skipped) -> nonzero -> the
        # adding arm runs: cleanup + rewards, then the tail recompute.
        chk("cleanup", len(tr(s, "defeat_cleanup")), 1)
        chk("rewards", len(tr(s, "rewards")), 1)
        return F
    if n == "mut-termmask":
        chk("w64", s["w64"], 2)                     # Stone applied despite gate2
        return F
    if n == "mut-mode0-not":
        chk("w64", s["w64"], 0x80)                  # bit written back -> still set
        chk("trace", names(s), PRE)                 # presence-equal early return
        return F
    if n == "mut-shl":
        chk("w64", s["w64"], 2)                     # bit1, not bit7
        return F
    if n == "mut-pres-src":
        chk("w38", s["w38"], 0x80)
        chk("trace_nonempty", len(s["trace"]) > 0, True)
        return F
    if n == "mut-cascflag":
        chk("entries", len(s["entries"]), 2)
        chk("inner flags", s["entries"][1]["flags"] & 0x200, 0)
        chk("recompute", len(tr(s, "recompute")), 2)
        return F
    if n == "mut-termbound":
        # byte past the case table decides - must differ from baseline skip
        chk("diverged", s["w3C"] != 1 or
            len(tr(s, "defeat_cleanup")) != 0 or len(tr(s, "event")) != 0 or
            s["fault"] is not None, True)
        return F
    return ["no checker"]

# ---- driver --------------------------------------------------------------------
def main():
    rd = load_exe()
    results = []
    npass = 0
    for c in cases():
        try:
            snap = run_case(c, rd)
        except Exception as e:
            snap = {"fault": "harness: %r" % e, "trace": [], "entries": []}
        fails = expect(c, snap)
        ok = not fails
        npass += ok
        results.append({
            "name": c["name"], "ok": ok, "why": c["why"],
            "failures": fails, "snap": snap,
        })
        print("%-24s %s" % (c["name"], "PASS" if ok else "FAIL " + "; ".join(fails)))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1, default=lambda o: list(o) if isinstance(o, (bytes, bytearray)) else o)
    print("%d/%d pass" % (npass, len(results)))

if __name__ == "__main__":
    main()
