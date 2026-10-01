#!/usr/bin/env python3
"""diff_angle_wrap.py - the sixth differential test, and the first that answers an OPEN QUESTION.

`DY-1` asks whether FFXII's two angle normalisers can disagree. They share all three constants -
`01CEBC50` = +pi, `00915620` = -pi, `01CEBC78` = 2pi - and use completely different arithmetic:

    003A1C50           a LOOP, add or subtract 2pi until in range      used by the mode setter
    the facing path    a truncating FMOD, one pass                     used by all four facing fns

So the test does three things, and only the first two are ordinary parity:

    1. loop form   : reconstruction vs the shipped 61 bytes at 003A1C50, run in Unicorn
    2. fmod form   : reconstruction vs the shipped wrap inside 0026C090, run in Unicorn
    3. DY-1        : the two SHIPPED forms against each other, over the same inputs

Neither reference side uses a stub. `003A1C50` is pure - one register in, one out, no calls.
`0026C090` needs an actor, a movement context and a steering record in memory, and with the actor's
kind byte set to 3 it writes the wrapped heading to `record->target_heading_34`, which the harness
reads back. **That is a real store through the real dispatch, not a value lifted out of a register.**

The loop form does not always terminate, and the first version confused that with slowness
-----------------------------------------------------------------------------------------
Once `|x|` is large enough that adding `2pi` is absorbed by float rounding, `x += 2pi` leaves `x`
unchanged and the loop **cannot** make progress. That threshold is derivable: absorption begins
when `ulp(x) > 2 * 2pi`, i.e. `2**(e-23) > 12.566`, i.e. `|x| >= 2**27` (about 1.34e8).

**A first version ran the emulator with a flat 2,000,000-instruction cap and called every
unfinished run "LOOPFOREVER". It was wrong on two inputs** - `1e7` and `-1e7`, where the loop needs
about 1.6 million iterations and roughly 6 million instructions. It terminates; the cap did not
reach it. **The reconstruction was right and the reference harness was wrong**, which is the less
common direction and worth recording.

So this version does not guess from a cap. Per input it decides:

    absorbed  -- x + 2pi == x in float32          -> cannot terminate, verified not assumed
    slow      -- estimated iterations > BUDGET    -> SKIPPED, and counted, and named
    otherwise -- emulate with a cap sized for that input's own estimate

The reconstruction still reproduces the unbounded loop faithfully; the *driver* applies its own
absorption check so it cannot hang, and that check is not part of the reconstruction.
"""

# Charter section 21's eleven dimensions. See ../PARITY-STANDARD.md for
# what each verdict requires; parity_status.py reads this without importing the module.
PARITY = {
    "subsystem": "angle_wrap",
    "entry": "003A1C50",
    "contract": "06-Movement-And-Navigation/CONTRACT-facing-and-steering.md",
    "dimensions": {
        "CALCULATION":      ("COVERED", "8280 comparisons over 4140 float bit patterns, both forms"),
        "STRUCTURAL":       ("COVERED", "the fmod form's result is read back from "
                                        "record->target_heading_34 - a real store, not a register"),
        "STATE-TRANSITION": ("N/A", "each call is independent; no state survives"),
        "CONTRACT":         ("NOT COVERED",
                            "3 of 7 testable claims exercised, of the contract's 9 section-15 "
                            "rows (2 record open questions); unexercised: the record is `0x80`, "
                            "inline, two of them; push/pop are the only slot callers; mode 4 "
                            "reads the `FrameLimit` base"),
        "EDGE-CASE":        ("COVERED", "the non-terminating region is identified by verifying "
                                        "x + 2pi == x, not by a timeout"),
        "SERIALIZATION":    ("N/A", "no byte stream on this path"),
        "RNG":              ("N/A", "no random draw on this path"),
        "TIMING":           ("N/A", "one call, no ordering"),
        "INTEGRATION":      ("NOT COVERED", "no real movement update drives either form"),
        "PRESENTATION":     ("NOT COVERED", "no character is turned"),
        "FULL-SUBSYSTEM":   ("NOT COVERED", "two normalisers of the facing subsystem"),
    },
}
# EM-1 -- charter section 21's CONTRACT dimension, mapped instead of defaulted.
#
# One row per claim in the contract's section 15 evidence table, in the contract's own order and
# with its own wording, because `parity_status.py` cross-checks these strings against that table
# and reports drift. Four statuses:
#
#   EXERCISED      at least one case reaches it, and a reconstruction that got it wrong FAILS
#   PARTIAL        touched, but not over the range the claim states
#   NOT EXERCISED  no case reaches it -- with a note on what would
#   OPEN QUESTION  the row records an UNKNOWN, so there is no behaviour to exercise
#
# **Marking a row EXERCISED asserts that breaking the claim breaks this test.** Where that is not
# true the row says NOT EXERCISED, however close the harness comes to it.
CONTRACT_MAP = [
    ("the record is `0x80`, inline, two of them",
     "NOT EXERCISED",
     "`00269F9F`'s `shl rax,7` plus `add rax,0x120` indexing is not emulated; `run_fmod` "
     "hands the callee one record at a fixed address"),
    ("the wrap and its three constants",
     "EXERCISED",
     "both shipped forms run over the real `01CEBC50`, `00915620` and `01CEBC78` bytes for "
     "every float bit pattern in the case set"),
    ("the bias cancels exactly only while x + bias stays in its binade",
     "EXERCISED",
     "the crossing at 4 - pi, its ulp neighbours, a 64-point spread across [4 - pi, 1), the "
     "negative mirror and the 8 - 2pi crossing are driven against the shipped bytes. The family "
     "exists because exhausting the bias branch's differing domains showed the crossing is where "
     "the branch becomes observable at all: 890,824 of the 1,065,353,216 floats in [+0.0, 1.0) "
     "distinguish the two biases and every one is at or above 4 - pi. It kills no mutant the "
     "old sweep did not already kill - the counts are 4/3/2 before and after - and it replaces "
     "incidental coverage of the crossing with named coverage"),
    ("the two facing variants are identical **for kind ≠ 3**",
     "EXERCISED",
     "checked on EVERY run, not inherited: both bodies are normalised -- RIP targets resolved, "
     "branch targets made relative to the entry -- and compared instruction by instruction. 29 "
     "each, exactly one differing, `xor r8d,r8d` against `mov r8d,1` at position 12"),
    ("`0026B6A0` never touches `r8` — but its kind-3 arm forwards it live",
     "PARTIAL",
     "the first half is checked on every run with capstone's regs_access, which reports "
     "IMPLICIT reads and writes too, so a `push r8` or an `xor r8d,r8d` would count: 0 of 30 "
     "instructions. A CONTROL on `rcx` finds 6, so a blind instrument cannot pass this "
     "silently. The second half -- the tail-jump forwarding `r8d` into `002E5FB0`/`002E5E10` "
     "-- is static evidence; `0026B6A0` kind 3 is not separately driven"),
    ("kind dispatch in `0026B6A0` and `0026C090`",
     "PARTIAL",
     "all THREE arms of `0026C090` now run per case, and they are behaviourally distinct at the "
     "observable: only kind 3 writes the record, kind 1 TAIL-JUMPS to `0026B6A0` (with the r8 it "
     "forwards live to `002E5FB0` when the kind is 3) and kind 2 does nothing at all. "
     "`0026B6A0`'s own dispatch is executed but "
     "not separately driven -- 3 of the 6 function-by-kind combinations"),
    ("push/pop are the only slot callers",
     "NOT EXERCISED",
     "a four-instrument reachability census over the image"),
    ("mode 4 reads the `FrameLimit` base",
     "NOT EXERCISED",
     "no case sets `+0x68`, so mode 4 is never reached"),
    ("`002E5FB0` is a 12-byte thunk into `002E5E10`: `context = actor[+0xB8]`, `xmm2 = context[+0xAC]` (the prior rate, handed back unchanged), `r9d = flag`",
     "NOT EXERCISED",
     "static derivation only; `0026B6A0` kind 3 is not separately driven, so the thunk never "
     "executes in this suite"),
    ("`002E5E10` is the kind-3 steering-record write: re-wraps the heading (third wrap site), stores `context[+0xA8]` and `{id,target}` fields `+0x50`/`+0x60`/`+0x70` via `003DA850` (a `[rcx+8]` leaf) — `+0x60`/`+0x70` only when `actor+0x0D` bit 5 clear — plus `record[+0x138]+0xF0` when that object exists, and finally `003EC260(word[record], prior_rate, heading, 0, flag!=0)`",
     "NOT EXERCISED",
     "static derivation only; reached only through the undriven kind-3 arm"),
    ("the flag is `003EC260`'s commit gate: 0 stages the `{rate, heading, 0}` triple into slot `+0x120`–`+0x128`; 1 additionally shifts it to `+0x250`–`+0x258` and calls `004288B0(slot,-1)` or `003B3CA0([slot+0x288],0x1E)`",
     "NOT EXERCISED",
     "static derivation only; `003EC260` is two calls below the undriven kind-3 arm"),
    ("`002E6300` is a 10-byte flag gate — `test r8b,r8b` / `js → 00265510` / `ret`",
     "NOT EXERCISED",
     "static derivation only; reached from the undriven mode/teardown paths"),
    ("`00265510`–`0026567F` is an eight-leaf kind-3 accessor cluster — each gated `(+3 & 0xE0)==0x60` (else 0): `sub[+0x64]` byte, `sub[+0x66]` word, `slot[+0xDC]` record `+0x34` float, slot-`edx` (clamped) record `+0x34`, `sub[+0x62]>>6 &1`, `sub[+0x28]&0x7F`, `cvttss2si(sub[+0x78])`, `movsx(sub[+0x68])`",
     "NOT EXERCISED",
     "static derivation only; the leaf getters are not driven"),
    ("`002627C0` copies the `0x80` steering record from slot `+0xDC` to slot `+0xDC+1`",
     "NOT EXERCISED",
     "static derivation only; the push helper is not on any driven path"),
    ("`002EC2C0` is the kind-3 vector-writer: stores `[rdx]` (a `Vec4`) into `[ctx+0xF0]+0x10`, clears `+0x62` bits 0–2, then `002E7B40`/`00265020`/`003A19A0`/`0026A8E0` apply a position-derived heading and `0026A870`/`0026A950` zero two channels",
     "NOT EXERCISED",
     "static derivation only; reached through `00263230`/`002EAAA0`/`002EBFA0`, none driven"),
    ("`002EBE50` is the mode initiator: `edx==0` zeroes `+0xB4`/`+0x224`; else snapshots `sub[+0x70]`/`+0x74` into them after `003A1C50`-wrapping the deltas, derives a frame count `abs(Δ)/sub[+0x6C]` (clamped by a constant) into `word[+0x60]` (`derived_turn_frames` in `_types/`), `+0x62` bit 5 cleared and bit 4 set, stamps `+0x63 = arg2`, then calls `002EC3F0` and `002E8EE0`",
     "NOT EXERCISED",
     "static derivation only; the mode arms are not driven"),
    ("`002EBFA0` steers toward a resolved target body: `003587C0` resolves the target, `[rsi+0xC0]` record must exist with `dword != -1`; writes the target triple `+0x10`/`+0x14`/`+0x18` and `003589B0(rsi)` id into `+0x1C` (`resume_target_handle` in `_types/`), `+0x62` bit 0 set and bits 1–2 cleared; heading from both `00265020` world positions via `003A19A0` → `0026A8E0`; fallback arms call `00265470`+`002EC2C0` or `002E64E0`",
     "NOT EXERCISED",
     "static derivation only; the target-steer path is not driven"),
    ("`002EAB80` is the push driver: gated `actor[+0x18]!=1` then kind-3 then `ctx[+0xDC]==0`; `002627C0` clones slot 0→1, `inc [+0xDC]`, `00269F90(ctx)`, `0026AE90(actor,0)`, `0026C120(actor,0)`",
     "NOT EXERCISED",
     "static derivation only; the push op is not driven"),
    ("`002EAAA0` is the pop driver: same `+0x18`/kind gates, then `ctx[+0xDC]!=0`; `dec [+0xDC]` (slot 0 was never overwritten — it is the saved pre-push state), `00269F90(ctx)`, then replays `sub[+0x62]&7` — 0 → `002EC2C0(actor,sub+0x10)`, 1 → `002EBFA0(actor,sub+0x10/0x14/0x18)`, else nothing — and always `002EC3F0`+`002E8EE0`",
     "NOT EXERCISED",
     "static derivation only; the pop op is not driven"),
    ("the push/pop caller side is a script op dispatch: `003DBDC0`→`00263230`(op==1) drives push; `003DB2A0`→`00263050`(op==4) drives pop only when `actor[+0xB]` bit 4 is set and clears that bit after",
     "NOT EXERCISED",
     "static derivation only; the script op dispatchers are not driven"),
    ("`002EC140` stamps resume shape 2: kind-3 gate, raw `{xmm1,xmm2}` into `sub+0x10`/`+0x14`, `+0x62 = (&0xFA) or 2`, then `0026A8E0`/`0026A870` apply and `0026A9C0`/`0026A950` zero",
     "NOT EXERCISED",
     "static derivation only; the look-at writers are not driven"),
    ("`002EC1C0` stamps resume shape 3: two-sided wrap (±π offset by arg sign, mod 2π) of `{xmm1,xmm2}` into `sub+0x10`/`+0x14`, `+0x62 = (&0xFB) or 3`, then `0026A8E0`/`0026A870` apply",
     "NOT EXERCISED",
     "static derivation only; the look-at writers are not driven"),
    ("the mode-4 timed turn interpolates `heading(t) = turn_start_heading(+0x38) + wrap(target_heading(+0x34) − +0x38) × min(turn_frame_index, turn_frames)/turn_frames`, then advances the frame index by 1; `0026C290` captures `+0x38` as the argument's two-sided wrap at arm time",
     "NOT EXERCISED",
     "static derivation only; the mode-4 arm is not among this suite's driven entries"),
    ("`+0x70`/`+0x74` are the two steer channels' wrapped targets (heading and aux/pitch): written only via wrap helpers `0026A8E0`/`0026A870`; the initiator `002EBE50` wraps `(+0x70 − ctx+0xB4)` against a mirror seeded from `ctx+0xA8` via `00265200`, derives `derived_turn_frames` from the residual, then snapshots both to `ctx+0xB4`/`ctx+0x224`",
     "NOT EXERCISED",
     "static derivation only; the initiator paths are not driven"),
    ("`+0x63` is `steer_arm_state` — the steer channel's armed-state byte: `002EBE50` stores its `edx` op verbatim and gates fresh-arm mirror reseeding on the byte being 0; the teardown/reset paths zero it in the same store sequence that clears `ctx+0xB4`/`ctx+0x224`",
     "NOT EXERCISED",
     "static derivation only; the initiator and teardown paths are not driven"),
    ("`+0x6C` is `initiator_turn_step` — the per-frame angular step the initiator divides the wrapped delta by to derive `derived_turn_frames` (`+0x60`): `max(1.0, abs(Δwrapped) / +0x6C)`; written by `0026AAD0` as the two-sided wrap of its argument times the rate global `[01DFE0BC]` — a rate-scaled step, not a bare residual",
     "NOT EXERCISED",
     "static derivation only; the initiator and writer paths are not driven"),
    ("`002EC3F0` is the steer dispatcher: it decodes two packed fields from `+0x62` — dispatch mode = bits 3–5 (`shr 3, &7`), resume shape = bits 0–2 (`&7`) — then tail-jumps one of six apply arms carrying `derived_turn_frames` as `xmm1` (shape ≤1: mode 1 → `002E7650`, mode 2 → `002E79A0`; shape 2: mode 1 → `002E7720`, mode 2 → `002E77F0`; shape 3: mode 1 → `002E78D0`, mode 2 → `002E7860`; the shape-2/3 arms also forward the `+0x10`/`+0x14` resume pair in `xmm2`/`xmm3`). `+0x6A` bit 0 is a one-shot latch that remaps mode 2 → mode 1 and is consumed (`&0xFE`) in the same pass",
     "NOT EXERCISED",
     "static derivation only; the dispatcher and its apply arms are not driven"),
    ("any runtime observation",
     "OPEN QUESTION",
     "none exists"),
]

import argparse
import os
import struct
import subprocess
import sys
import tempfile

try:
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UcError
    from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RSP, UC_X86_REG_XMM0,
                                   UC_X86_REG_XMM1)
except ImportError:
    sys.stderr.write("diff_angle_wrap: needs unicorn (pip install unicorn)\n")
    raise SystemExit(2)

LOOP_VA, LOOP_LEN = 0x003A1C50, 61
FMOD_VA, FMOD_LEN = 0x0026C090, 129          # wraps, then dispatches on the actor kind

ACTOR_VA = 0x30000000
CTX_VA = 0x30010000
REC_VA = 0x30020000
STACK_BASE = 0x40000000
RET_MAGIC = 0x50000000
ITER_BUDGET = 200_000            # iterations we are willing to emulate for one input
INSN_PER_ITER = 5                # add, comiss, jcc, and the loop's own overhead
FMOD_INSN_CAP = 200_000


def read_exe(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs = []
    off = pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40

    def rd(va, n):
        r = va - base
        for sva, vs, ra, rs in secs:
            if sva <= r < sva + rs:      # SizeOfRawData, never the virtual size
                return d[ra + (r - sva):ra + (r - sva) + n]
        return None
    return rd


def f2b(f):
    return struct.unpack("<I", struct.pack("<f", f))[0]


def b2f(b):
    return struct.unpack("<f", struct.pack("<I", b))[0]


def new_uc(rd, va, ln, extra_pages=()):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    page = lambda a: a & ~0xFFF
    uc.mem_map(page(va), 0x2000)
    code = rd(va, ln)
    if code is None or len(code) < ln:
        raise SystemExit("cannot read %08X" % va)
    uc.mem_write(va, code)
    # the wrap constants live in .rdata and .data; map both pages the functions touch
    for c in (0x00915620, 0x01CEBC50, 0x01CEBC78):
        try:
            uc.mem_map(page(c), 0x2000)
        except UcError:
            pass
        blk = rd(page(c), 0x2000)
        if blk:
            uc.mem_write(page(c), blk)
    for p in extra_pages:
        try:
            uc.mem_map(p, 0x2000)
        except UcError:
            pass
    uc.mem_map(STACK_BASE, 0x10000)
    sp = STACK_BASE + 0x8000
    uc.mem_write(sp, struct.pack("<Q", RET_MAGIC))
    uc.reg_write(UC_X86_REG_RSP, sp)
    return uc


PI32 = b2f(0x40490FDB)
TWOPI32 = b2f(0x40C90FDB)


def f32(x):
    """Round a Python double to float32, the way every step of the shipped loop does."""
    return struct.unpack("<f", struct.pack("<f", x))[0]


def loop_prognosis(bits):
    """('absorbed'|'slow'|'run', estimated_iterations) - decided, never guessed from a cap."""
    x = b2f(bits)
    if x != x:                                   # NaN: comiss is unordered, both jbe are taken
        return ("run", 0)
    if x in (float("inf"), float("-inf")):
        return ("absorbed", 0)
    if x < -PI32:
        if f32(x + TWOPI32) == x:
            return ("absorbed", 0)
        n = int((-PI32 - x) / TWOPI32) + 2
    elif x > PI32:
        if f32(x - TWOPI32) == x:
            return ("absorbed", 0)
        n = int((x - PI32) / TWOPI32) + 2
    else:
        return ("run", 0)
    return (("run" if n <= ITER_BUDGET else "slow"), n)


def run_loop(rd, bits):
    kind, n = loop_prognosis(bits)
    if kind == "absorbed":
        return ("LOOPFOREVER", None)
    if kind == "slow":
        return ("SKIPPED", n)
    uc = new_uc(rd, LOOP_VA, LOOP_LEN)
    uc.reg_write(UC_X86_REG_XMM0, bits)
    try:
        uc.emu_start(LOOP_VA, RET_MAGIC, count=(n + 32) * INSN_PER_ITER + 64)
    except UcError as e:
        return ("ERROR", str(e))
    if uc.reg_read(UC_X86_REG_RSP) != STACK_BASE + 0x8000 + 8:
        # Should be unreachable: the estimate is generous. If it fires, the estimate is wrong and
        # that is a harness bug, not a finding -- say so rather than reporting non-termination.
        return ("ESTIMATE-TOO-LOW", n)
    return ("OK", uc.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF)


# ---------------------------------------------------------------------------------------------
# The contract makes two claims about function BODIES rather than about behaviour, and both were
# recorded as PROVEN on a reading. They are mechanically checkable, so the harness checks them on
# every run instead of inheriting them:
#
#   "the two facing variants are identical"   0026B5A0 vs 0026B620, one differing instruction
#   "0026B6A0 never touches r8"               so the argument they disagree about is never read
#
# `Database/Tools/analysis-kit/gfz-scripts/fn_audit.py` is the general tool; this is the same two
# checks, inline, so the harness stays standalone.
VAR0_VA, VAR0_LEN = 0x0026B5A0, 117
VAR1_VA, VAR1_LEN = 0x0026B620, 120
CALLEE_VA, CALLEE_LEN = 0x0026B6A0, 120
BRANCH = set("jmp je jne jz jnz jl jle jg jge jb jbe ja jae js jns jo jno jp jnp call".split())


def _norm(rd, va, length):
    """Instructions reduced to text, with RIP targets RESOLVED and branch targets made relative
    to the entry -- so two bodies at different addresses compare equal only when they really do
    the same thing to the same globals."""
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_REG_RIP
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    out = []
    for ins in md.disasm(rd(va, length), va):
        text = ins.op_str
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.value.mem.base == X86_REG_RIP:
                tgt = ins.address + ins.size + op.value.mem.disp
                text = text.replace("rip + 0x%x" % op.value.mem.disp, "ABS:%08X" % tgt)
                text = text.replace("rip - 0x%x" % (-op.value.mem.disp), "ABS:%08X" % tgt)
        if ins.mnemonic in BRANCH and ins.op_str.startswith("0x"):
            t = int(ins.op_str, 16)
            text = "+%d" % (t - va) if va <= t < va + length else "OUT:%08X" % t
        out.append("%s %s" % (ins.mnemonic, text))
    return out


def _touches(rd, va, length, family):
    """capstone's regs_access, so IMPLICIT reads and writes count -- `xor r8d,r8d`, `push r8`,
    a `div`'s implicit rdx. An operand-text regex would miss exactly those."""
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    hits = []
    for ins in md.disasm(rd(va, length), va):
        r, w = ins.regs_access()
        names = {ins.reg_name(x).lower() for x in tuple(r) + tuple(w) if ins.reg_name(x)}
        if names & family:
            hits.append((ins.address - va, "%s %s" % (ins.mnemonic, ins.op_str)))
    return hits


def static_claims(rd):
    """-> (ok, lines). Two contract claims, checked rather than believed."""
    lines, ok = [], True
    a, b = _norm(rd, VAR0_VA, VAR0_LEN), _norm(rd, VAR1_VA, VAR1_LEN)
    diff = [i for i in range(min(len(a), len(b))) if a[i] != b[i]]
    same_shape = len(a) == len(b)
    lines.append("  the two facing variants  : %d and %d instructions, %d differing"
                 % (len(a), len(b), len(diff) if same_shape else -1))
    for i in diff:
        lines.append("      [%2d]  %-34s |  %s" % (i, a[i], b[i]))
    if not (same_shape and len(diff) == 1):
        ok = False
        lines.append("      ** the contract says 29 each differing in exactly one **")

    r8 = _touches(rd, CALLEE_VA, CALLEE_LEN, {"r8", "r8d", "r8w", "r8b"})
    ctl = _touches(rd, CALLEE_VA, CALLEE_LEN, {"rcx", "ecx", "cx", "cl"})
    lines.append("  0026B6A0 touching r8     : %d instruction(s)" % len(r8))
    for off, t in r8:
        lines.append("      +%-3d %s" % (off, t))
    lines.append("  CONTROL, touching rcx    : %d instruction(s)  (0 would mean the instrument "
                 "is blind)" % len(ctl))
    if not ctl:
        ok = False
        lines.append("      ** the control found nothing; the r8 result is unproven **")
    if r8:
        ok = False
        lines.append("      ** the contract says r8 is never touched **")
    return ok, lines


def run_fmod(rd, bits, kind=3):
    uc = new_uc(rd, FMOD_VA, FMOD_LEN,
                extra_pages=(ACTOR_VA, CTX_VA, REC_VA))
    # Kind 1 TAIL-JUMPS to 0026B6A0, so that body has to be present or the arm cannot be run at
    # all. Mapping it is not a stub: it is the real callee, at its real address, executed.
    # ONE page: new_uc already maps 0x2000 at 0026C000, and 0026B000+0x2000 would overlap it.
    uc.mem_map(CALLEE_VA & ~0xFFF, 0x1000)
    uc.mem_write(CALLEE_VA, rd(CALLEE_VA, CALLEE_LEN))
    uc.mem_write(ACTOR_VA + 3, bytes([kind << 5]))         # the actor kind the dispatch reads
    uc.mem_write(ACTOR_VA + 0xB8, struct.pack("<Q", CTX_VA))
    uc.mem_write(CTX_VA + 0xF0, struct.pack("<Q", REC_VA))
    uc.mem_write(REC_VA + 0x34, struct.pack("<I", 0xDEADBEEF))
    uc.reg_write(UC_X86_REG_RCX, ACTOR_VA)
    uc.reg_write(UC_X86_REG_XMM1, bits)
    try:
        uc.emu_start(FMOD_VA, RET_MAGIC, count=FMOD_INSN_CAP)
    except UcError as e:
        return ("ERROR", str(e))
    return ("OK", struct.unpack("<I", uc.mem_read(REC_VA + 0x34, 4))[0])


def cases():
    out = []
    for v in (0.0, -0.0, 1.0, -1.0, 3.14159274, -3.14159274, 3.15, -3.15,
              6.28318548, -6.28318548, 6.3, -6.3, 100.0, -100.0, 1000.0, -1000.0,
              1e6, -1e6, 1e7, -1e7, 1.34e8, -1.34e8, 1e9, -1e9, 1e30, -1e30,
              1e-30, -1e-30, 1.1754944e-38, float("inf"), float("-inf"), float("nan")):
        out.append(f2b(v))
    # every angle from -4pi to 4pi in 1/512 steps, plus the ulp neighbours of +-pi
    step = 8 * 3.14159274 / 4096.0
    for i in range(4097):
        out.append(f2b(-4 * 3.14159274 + i * step))
    for base in (3.14159274, -3.14159274, 6.28318548, -6.28318548):
        b = f2b(base)
        out += [b - 2, b - 1, b, b + 1, b + 2]
    # The BINADE CROSSING at 4 - pi, and it is the bias branch that makes it observable.
    # `Angle_WrapFmod` adds bias, takes q, subtracts q*2pi and subtracts bias again; for
    # |x| < pi the q is 0 and the whole thing is a round trip. That round trip is exact only
    # while x + bias stays in the binade the constant is in. At x = 4 - pi the sum crosses
    # 4.0, the ulp doubles, and (x + pi) - pi comes back one ulp low while (x - pi) + pi does
    # not - so which bias the branch picked is visible in the result.
    #
    # Found while adjudicating the mutation campaign's survivors. Exhausting the differing
    # domain of `bias = (x >= 0.0f)` -> `(x >= 1.0f)` - every float32 in [+0.0, 1.0), compiled
    # with this pilot's compiler and flags - gives 890,824 inputs that distinguish the two
    # biases, every one at or above 4 - pi. That mutant is KILLED with or without this family:
    # the sweep above lands on roughly twenty inputs past the crossing by accident. The family
    # changes no mutation count (4 KILLED / 3 EQUIVALENT / 2 SURVIVED either way); it makes the
    # coverage deliberate and named, and it drives both sides of the crossing rather than one.
    # The two survivors are on the same line and are equivalent, each proven by exhausting its
    # own differing domain: `>=` -> `>` differs only at +-0.0, and `0.0f` -> `0.1f` differs only
    # below 0.1, where nothing distinguishes the bias at all.
    for sign in (1.0, -1.0):
        edge = f2b(sign * (4.0 - 3.14159274101257324))
        out += [edge - 2, edge - 1, edge, edge + 1, edge + 2]
        one = f2b(sign * 1.0)
        lo, hi = (edge, one) if sign > 0 else (one, edge)
        step = max(1, (hi - lo) // 64)
        out += list(range(lo, hi, step))
    # The same crossing one binade up, so the family is not a single accident: 8 - 2pi is
    # where x + 2pi crosses 8.0.
    for sign in (1.0, -1.0):
        edge = f2b(sign * (8.0 - 6.28318548202514648))
        out += [edge - 2, edge - 1, edge, edge + 1, edge + 2]
    seen, uniq = set(), []
    for b in out:
        if b not in seen:
            seen.add(b)
            uniq.append(b)
    return uniq


KINDS = (1, 2, 3)          # the three arms of `sub ecx,1 / cmp ecx,2`; the harness pinned 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True)
    ap.add_argument("--driver", required=True)
    a = ap.parse_args()
    rd = read_exe(a.exe)

    print("STATIC CLAIMS, checked rather than inherited")
    static_ok, static_lines = static_claims(rd)
    for l in static_lines:
        print(l)
    print("  verdict                  : %s" % ("all hold" if static_ok else "**A CLAIM FAILED**"))
    print()

    cs = cases()

    tmp = tempfile.mkdtemp(prefix="anglewrap")
    cf = os.path.join(tmp, "cases.txt")
    with open(cf, "w") as f:
        for b in cs:
            f.write("%08X\n" % b)
    got = subprocess.run([a.driver, cf], capture_output=True, text=True)
    if got.returncode != 0:
        sys.stderr.write(got.stderr)
        return 2
    mine = [l.split() for l in got.stdout.splitlines() if l.strip()]
    if len(mine) != len(cs):
        sys.stderr.write("driver produced %d lines for %d cases\n" % (len(mine), len(cs)))
        return 2

    by_kind = {}
    bad_loop = bad_fmod = 0
    loopforever = skipped = compared = 0
    disagree = []
    examples = []
    for b, (m_loop, m_fmod) in zip(cs, mine):
        k_l, v_l = run_loop(rd, b)
        k_f, v_f = run_fmod(rd, b)
        if k_f != "OK":
            raise SystemExit("fmod reference failed on %08X: %s" % (b, v_f))
        # THE KIND DISPATCH: the harness used to pin kind 3. Run all three arms and record
        # whether the wrap's result depends on which one is taken.
        for k in KINDS:
            kk, vv = run_fmod(rd, b, k)
            if kk != "OK":
                raise SystemExit("fmod kind %d failed on %08X: %s" % (k, b, vv))
            by_kind.setdefault(k, set()).add(vv == v_f)
        if k_l in ("ERROR", "ESTIMATE-TOO-LOW"):
            raise SystemExit("loop reference failed on %08X: %s %s" % (b, k_l, v_l))

        if k_l == "SKIPPED":
            skipped += 1
        else:
            ref_loop = "LOOPFOREVER" if k_l == "LOOPFOREVER" else "%08X" % v_l
            if ref_loop != m_loop:
                bad_loop += 1
                if len(examples) < 8:
                    examples.append(("loop", b, m_loop, ref_loop))
        if "%08X" % v_f != m_fmod:
            bad_fmod += 1
            if len(examples) < 8:
                examples.append(("fmod", b, m_fmod, "%08X" % v_f))

        if k_l == "LOOPFOREVER":
            loopforever += 1
        elif k_l == "OK":
            compared += 1
            if v_l != v_f:
                disagree.append((b, v_l, v_f))

    print("kind dispatch: all %d arms run per case, not just kind 3" % len(KINDS))
    for k in sorted(by_kind):
        agrees = by_kind[k]
        print("  kind %d : result equals kind 3's on %s of the cases"
              % (k, "every one" if agrees == {True} else
                    "NONE" if agrees == {False} else "some but not all"))
    print()
    print("cases: %d distinct float bit patterns" % len(cs))
    print()
    print("  1. loop form  003A1C50   vs reconstruction : %s"
          % ("OK" if not bad_loop else "%d MISMATCH" % bad_loop))
    print("  2. fmod form  0026C090   vs reconstruction : %s"
          % ("OK" if not bad_fmod else "%d MISMATCH" % bad_fmod))
    print()
    print("  3. DY-1 - the two SHIPPED forms against each other")
    print("     inputs where the loop form CANNOT TERMINATE : %d  (x + 2pi == x, verified)"
          % loopforever)
    print("     inputs too slow to emulate, SKIPPED         : %d  (> %d iterations)"
          % (skipped, ITER_BUDGET))
    print("     inputs compared                             : %d" % compared)
    print("     ...of those, the two forms DISAGREE         : %d  (%.1f %%)"
          % (len(disagree), 100.0 * len(disagree) / compared if compared else 0.0))
    for b, l, f in disagree[:10]:
        print("        in %08X (%-14.6g)  loop %08X (%-12.6g)  fmod %08X (%.6g)"
              % (b, b2f(b), l, b2f(l), f, b2f(f)))
    if len(disagree) > 10:
        print("        ... and %d more" % (len(disagree) - 10))

    if not static_ok:
        print()
        print("RESULT: a STATIC CONTRACT CLAIM FAILED - see the top of this run")
        return 1
    if examples:
        print("\nfirst mismatches:")
        for which, b, m, r in examples:
            print("  %-5s in %08X  mine %s  ref %s" % (which, b, m, r))
        return 1
    print("\n%d comparisons, 0 mismatches against the shipped bytes." % (len(cs) * 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
