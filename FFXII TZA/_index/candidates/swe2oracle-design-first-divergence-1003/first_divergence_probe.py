#!/usr/bin/env python3
"""first_divergence_probe.py - worked example for the SWE2-ORACLE first-divergence design note.

A bounded DB probe on the sealed suite mt-twist-simd-exec (EXP-111, the shipped MT19937 twist
00866B90). It needs no reconstruction. It re-runs the suite's own `run_twist` from its own check.py
and wraps `Uc` the way the execcov shim does. It never edits the suite and never writes its
result.json. Each run records an ordered state sequence:

  X <rip>                      every executed instruction (UC_HOOK_CODE)
  W <rip> <addr> <size> <hex>  every memory write; the bytes are read back when the NEXT instruction
                               starts, so 16-byte SIMD stores carry their real value
  R <rip> <addr>               a read of the mutated data address (data-constant mutants only)

and an observation-point stream: the dword writes into the 624-word state array and the MTI cell,
as (cell, value) in the order written. 16-byte stores are split into four dwords.

Comparisons (each prints one record in the design note's schema):

  D0  determinism   the baseline run twice: no divergence over the whole sequence. Without this
                    control a "first divergence" could be noise.
  M*  20 mutants    reference = the shipped bytes; candidate = the suite's own mutant (one patched
                    byte). The mutant stands in for a defective reconstruction whose defect site is
                    KNOWN. Control: the first divergence must fall at or after the first execution
                    of the patched instruction (or the first read of a patched constant), and never
                    before it. The record also shows what the suite itself sees: a mismatch in the
                    final 624-word state or MTI, i.e. the late visible mismatch.
  A0  arm parity    reference = scalar arm (flag 1), candidate = SIMD arm (flag 2): two
                    implementations of one contract. Instruction sequences part at the feature
                    gate, which is expected and not a divergence. The observation-point streams
                    must be equal: this is how a reconstruction (native code, no shared
                    instruction stream) has to be compared.
  F0  final-only    the same mutant compared only on the final state, as the sealed suite does:
                    first divergence UNKNOWN, late visible mismatch named.

Prints `FAILS N` (0 = every control holds) and writes first-divergence.tsv next to this file.
Run with system Python 3.14 (unicorn 2.1.4): the analysis venv's 2.1.0 rejects the SIMD arm.
"""
import os, sys, struct, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
SUITE = os.path.join(ROOT, "Database", "FFXII TZA", "_experiments", "evidence", "mt-twist-simd-exec")
sys.path.insert(0, SUITE)
import unicorn                                   # noqa: E402
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ   # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402
import check as S                                # the suite's own driver, imported, never edited  # noqa: E402

PACKAGE = "21-RNG-And-Determinism / MT19937 twist 00866B90 (EXP-111 mt-twist-simd-exec)"
CONTRACT = "21-RNG-And-Determinism/CONTRACT-gameplay-generators.md"
RESULT_SHA = hashlib.sha256(open(os.path.join(SUITE, "result.json"), "rb").read()).hexdigest()
STATE_LO, STATE_HI = S.STATE, S.STATE + S.N * 4
_md = Cs(CS_ARCH_X86, CS_MODE_64)
fails = []

_REAL_UC = S.Uc
_rec = {"events": None, "obs": None, "pending": [], "watch": None}


def _flush(uc):
    for rip, a, n in _rec["pending"]:
        b = bytes(uc.mem_read(a, n))
        _rec["events"].append(("W", rip, a, n, b.hex()))
        for k in range(0, n, 4):                 # observation points: state cells and MTI
            c = a + k
            if (STATE_LO <= c < STATE_HI or c == S.MTI) and k + 4 <= n:
                cell = "mti" if c == S.MTI else "s[%d]" % ((c - STATE_LO) // 4)
                _rec["obs"].append((cell, b[k:k + 4].hex()))
    _rec["pending"] = []


def _on_code(uc, a, n, _u):
    if _rec["pending"]:
        _flush(uc)
    _rec["events"].append(("X", a))


def _on_write(uc, access, a, n, v, _u):
    _rec["pending"].append((uc.reg_read(unicorn.x86_const.UC_X86_REG_RIP), a, n))


def _on_read(uc, access, a, n, v, _u):
    w = _rec["watch"]
    if a <= w < a + n:                           # the access covers the patched byte
        _rec["events"].append(("R", uc.reg_read(unicorn.x86_const.UC_X86_REG_RIP), w))


class _Recording(object):
    """stands in for unicorn.Uc inside the suite: a real Uc with the three hooks."""

    def __new__(cls, *a, **kw):
        uc = _REAL_UC(*a, **kw)
        uc.hook_add(UC_HOOK_CODE, _on_code)
        uc.hook_add(UC_HOOK_MEM_WRITE, _on_write)
        if _rec["watch"] is not None:
            # a range hook fires on the access START address: a 16-byte load at 01CCFE00 covering a
            # patched byte at 01CCFE03 is missed by begin=end=site (m-simd-hi, first run of this probe)
            uc.hook_add(UC_HOOK_MEM_READ, _on_read, begin=_rec["watch"] - 15, end=_rec["watch"])
        _orig = uc.emu_start

        def emu_start(*aa, **kk):
            try:
                return _orig(*aa, **kk)
            finally:
                _flush(uc)
        uc.emu_start = emu_start
        return uc


S.Uc = _Recording


def run(state, flag, patch=(), watch=None):
    _rec.update(events=[], obs=[], pending=[], watch=watch)
    faults, out, mti, can = S.run_twist(state, flag, RAW, SECS, patch=list(patch))
    return dict(events=_rec["events"], obs=_rec["obs"], faults=faults, out=out, mti=mti, canary=can)


def first_diff(a, b):
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            return i
    return None if len(a) == len(b) else min(len(a), len(b))


def insn_at(va):
    off = None
    for sva, vs, ra, rs in SECS:
        if sva <= va - S.IMG_LO < sva + rs:
            off = ra + (va - S.IMG_LO - sva)
    for i in _md.disasm(RAW[off:off + 16], va):
        return "%s %s" % (i.mnemonic, i.op_str)
    return "?"


def containing_insn(site, events):
    """the executed instruction whose bytes contain the patched site (code mutants)."""
    for e in events:
        if e[0] == "X" and e[1] <= site < e[1] + 15:
            for i in _md.disasm(bytes(16), e[1]):
                pass
    xs = sorted({e[1] for e in events if e[0] == "X"})
    for a in reversed(xs):
        if a <= site:
            return a
    return None


def classify(ev_ref, ev_cand):
    """divergence class from the addendum's list, from the KIND of the first differing event."""
    if ev_ref is None or ev_cand is None:
        return "state transition", "one run ended early (sequence length differs)"
    if ev_ref[0] == "X" and ev_cand[0] == "X":
        return "branch condition", "control flow parts: next instruction %08X vs %08X" % (ev_ref[1], ev_cand[1])
    if ev_ref[0] == "W" and ev_cand[0] == "W":
        if ev_ref[2] != ev_cand[2]:
            return "field/type/layout", "write target differs: %08X vs %08X" % (ev_ref[2], ev_cand[2])
        return "state transition", "same write target %08X, value %s vs %s" % (ev_ref[2], ev_ref[4], ev_cand[4])
    return "ordering", "event kinds differ: %s vs %s" % (ev_ref[0], ev_cand[0])


def fmt(e):
    if e is None:
        return "<end of sequence>"
    if e[0] == "X":
        return "X %08X %s" % (e[1], insn_at(e[1]))
    if e[0] == "W":
        return "W @%08X -> %08X len %d = %s" % (e[1], e[2], e[3], e[4])
    return "R @%08X <- %08X" % (e[1], e[2])


def late_visible(ref, cand):
    if ref["faults"] != cand["faults"]:
        return "fault: %s" % (cand["faults"] or ref["faults"])[0]
    for i in range(S.N):
        if ref["out"][i] != cand["out"][i]:
            return "final s[%d] %08X vs %08X" % (i, ref["out"][i], cand["out"][i])
    if ref["mti"] != cand["mti"]:
        return "final mti %d vs %d" % (ref["mti"], cand["mti"])
    if ref["canary"] != cand["canary"]:
        return "stack canary only (contract state equal)"
    return "none"


ROWS = []
HDR = ("record\tpackage\texpected_contract\treference_result\treconstruction_result\tcompared_from\t"
       "first_divergent_step\tdivergence_class\tlikely_ownership\tlate_visible_mismatch\tevidence\tstatus")


def row(rec, ref_desc, cand_desc, compared_from, step, cls, owner, late, status):
    ROWS.append("\t".join([rec, PACKAGE, CONTRACT, ref_desc, cand_desc, compared_from, step, cls, owner, late,
                           "evidence/mt-twist-simd-exec result.json sha256 %s; this probe" % RESULT_SHA[:12],
                           status]))


def check(name, ok, detail):
    print("%-14s %s %s" % (name, "PASS" if ok else "FAIL", detail))
    if not ok:
        fails.append(name)


RAW, SECS = S.load_image()
STATE = S.build_states()["rand"]

# D0 determinism: two runs of the same sealed case
b1, b2 = run(STATE, 1), run(STATE, 1)
d = first_diff(b1["events"], b2["events"])
check("D0 determinism", d is None and b1["obs"] == b2["obs"],
      "%d events, %d observation points, no divergence" % (len(b1["events"]), len(b1["obs"])))
row("D0", "shipped bytes, scalar arm, state 'rand' (run 1)", "same (run 2)", "event 0 (entry 00866B90)",
    "NONE over %d events" % len(b1["events"]), "-", "-", "none", "NO DIVERGENCE")

# M*: the suite's 20 mutants as candidates with a known defect site
base = {1: b1, 2: run(STATE, 2)}
for name, va, orig, patch, arm in S.MUTS:
    flag = 1 if arm == 0 else 2
    data_const = not (0x866B90 <= va < 0x866D60)
    cand = run(STATE, flag, patch=[(va, bytes([patch]))], watch=va if data_const else None)
    ref = base[flag]
    if data_const:
        # the reference must see the same read to align: re-run it watching the same address
        ref = run(STATE, flag, watch=va)
    i = first_diff(ref["events"], cand["events"])
    e_r = ref["events"][i] if i is not None and i < len(ref["events"]) else None
    e_c = cand["events"][i] if i is not None and i < len(cand["events"]) else None
    cls, why = classify(e_r, e_c)
    late = late_visible(ref, cand)
    if data_const:
        first_touch = next((k for k, e in enumerate(cand["events"]) if e[0] == "R"), None)
        touch = "first read of the patched constant %08X at event %s" % (va, first_touch)
    else:
        ins = containing_insn(va, cand["events"])
        first_touch = next((k for k, e in enumerate(cand["events"]) if e[0] == "X" and e[1] == ins), None)
        touch = "first execution of the patched instruction %08X at event %s" % (ins or 0, first_touch)
    ok = i is not None and first_touch is not None and i >= first_touch
    io = first_diff(ref["obs"], cand["obs"])
    pad = [("<end>", "")]
    obs = ("observation point %d (ref %s=%s vs cand %s=%s)" % ((io,) + (ref["obs"] + pad)[io] + (cand["obs"] + pad)[io])
           if io is not None else "no observation-point divergence")
    check(name, ok, "first divergence at event %s (%s); %s; %s; late visible: %s" % (i, cls, touch, obs, late))
    print("               ref  %s\n               cand %s" % (fmt(e_r), fmt(e_c)))
    step = ("event %d: ref %s | cand %s (%s); contract level: %s" % (i, fmt(e_r), fmt(e_c), why, obs)
            if i is not None else "NONE")
    row(name, "shipped bytes, %s arm, state 'rand'" % ("scalar" if flag == 1 else "SIMD"),
        "suite mutant %s: byte %08X %02X->%02X" % (name, va, orig, patch), "event 0 (entry 00866B90)",
        step, cls, "implementation (candidate; defect site known by construction)", late,
        "FIRST DIVERGENCE ESTABLISHED" if ok else "CONTROL FAILED")

# A0: two implementations of one contract
sc, si = base[1], base[2]
ix = first_diff(sc["events"], si["events"])
io = first_diff(sc["obs"], si["obs"])
check("A0 arm parity", io is None and sc["out"] == si["out"] and sc["mti"] == si["mti"],
      "instruction streams part at event %s (the feature gate, expected); observation streams (%d points) equal"
      % (ix, len(sc["obs"])))
row("A0", "scalar arm (flag 1), state 'rand'", "SIMD arm (flag 2), same input",
    "observation point 0 (first state write)", "NONE at observation points (%d); instruction streams part at "
    "event %s by design" % (len(sc["obs"]), ix), "-", "-", "none", "NO DIVERGENCE (contract level)")

# F0: final-state-only comparison of one mutant, as the sealed suite compares
m = [x for x in S.MUTS if x[0] == "m-sc2-m"][0]
cand = run(STATE, 1, patch=[(m[1], bytes([m[3]]))])
late = late_visible(b1, cand)
check("F0 final-only", late != "none", "late visible mismatch %s; earlier states not compared" % late)
row("F0", "shipped bytes, scalar arm, state 'rand' (final state only)", "suite mutant m-sc2-m (final state only)",
    "final state only", "UNKNOWN (earlier states were not compared)", "unknown", "UNKNOWN", late,
    "LATE MISMATCH ONLY")

with open(os.path.join(HERE, "first-divergence.tsv"), "w", newline="\n") as f:
    f.write(HDR + "\n" + "\n".join(ROWS) + "\n")
print("rows %d -> first-divergence.tsv" % len(ROWS))
print("FAILS %d" % len(fails))
sys.exit(1 if fails else 0)
