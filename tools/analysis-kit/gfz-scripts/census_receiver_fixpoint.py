"""Receiver-tracked field census, iterated to a fixpoint over a type's method set.

WHAT IT IS FOR. A type whose rows read "no censused access" has usually not been
searched with its receiver PROVEN. A displacement sweep asks "who touches +0x38?" and
answers with every type in the image; this asks "what does THIS object's pointer reach?"
and follows only that. On 2026-09-21 it corrected four types the store recorded as
unobserved, including Manager0209AC60, whose four rows said no censused access and which
turned out to carry 1,315 accesses across 454 functions.

    python census_receiver_fixpoint.py <cell> [embed] [extent]
    DEBT='[[off,len],...]'  breaks the result down per declared span.
    CAP=<n>                 raises the frontier cap (default 400).
    SEED=cell|slots|call|static|vtable|ctor  how the FIRST receiver is obtained (default cell).

  cell    the .data slot holding the object POINTER, not the object's own address
  embed   offset of the sub-object inside what the cell points at, 0 if none
  extent  the type's size; displacements outside [0,extent) are dropped

NO SINGLE SEED IS COMPLETE. RUN EVERY APPLICABLE ONE AND UNION. This is the strongest
thing learned on 2026-09-21 and it was found by accident, controlling the vtable seed
against a type that already had two others. PApplication gives 61 distinct displacements
from its CELL, 229 through its GETTER and 146 through its VTABLE - three receiver-proven
views of one object that see genuinely different things, because each starts somewhere
different in the call graph. Unioned, 9 of its 25 gap spans are reached where the getter
alone found 7. A census run from one seed is a lower bound on that type, not a result,
and a ZERO from one seed is much weaker than a zero from all of them.

FINDING THE GETTER: DO NOT CONFUSE IT WITH A FIELD ACCESSOR. A first audit looked only
for bodies of 24 bytes or less matching `mov rax,[cell]; ret` and found one getter across
eight cells - but BattleUnit's is 37 bytes and bounds-checks, so that shape was missed.
Widening the size bound naively is WORSE, not better: it returns every small
`mov rax,[cell]; mov eax,[rax+N]; ret` FIELD ACCESSOR, and seeding SEED=call on one of
those censuses whatever a field value happens to address. The test that separates them is
whether anything is DEREFERENCED AFTER the cell is loaded - a getter's cell value flows to
the return untouched or with address arithmetic only. With that filter at 80 bytes the
audit finds BattleUnit's 00236820 correctly, plus true getters for six of eight cells.

AND THE HONEST SCOPE OF THE UNION, measured after the fact rather than assumed from the
PApplication result: applying those getters changed NOTHING on ImageBackedStateBlock
(1 of 8 spans before and after) or ManagerSingleton0209BE80 (2 of 29), whose cell seeds
already dominated, and nothing on BattleUnit or BootSingleton01F7F598 either. The union
has so far gained TWO SPANS, all on PApplication. The rule is right - a single seed is a
lower bound - and its practical yield is small on the types measured so far. Both halves
of that belong in the record.

A ROUTE DESCRIBES STORAGE; A GETTER DESCRIBES ACCESS. Seed on the second. Two types
proved this on 2026-09-21 and both had correct routes that led almost nowhere:

  * BattleUnit's route (PARRAY base, stride 0xF50, index=slot) is accurate, and censusing
    from the base gives 3 displacements. Its elements are reached through
    BattleUnit_GetBySlotIndex (00236820), which bounds-checks the slot, multiplies, adds
    the base from memory and RETURNS the element. SEED=call on the getter: 24
    displacements, 133 accesses, 26 functions. Eight times as many displacements.
  * Manager0209AC60's route names a static object that EXACTLY ONE function references -
    its lazy init. Every real access goes through the pointer cell 0x0209AC30.

WHEN A CENSUS COMES BACK THIN, LOOK FOR THE GETTER BEFORE CONCLUDING ANYTHING. I recorded
BattleUnit as beyond the tool's reach after guessing twice at its element-selection idiom;
both guesses were wrong and reading 00236820 settled it in one look.

PICK THE SEED FROM THE ROUTE, AND CHECK IT STARTED. The wrong seed does not give a wrong
answer, it gives ZERO FUNCTIONS - and that zero is a failure to start, not a negative
about the type. Never write it onto a row. The three seeds, each added because a real
type could not be censused without it:

  SEED=cell   (STATIC / PTR / CHAIN) a .data slot holds the object pointer.
  SEED=slots  (SLOTPTR) `cell` is the BASE OF A POINTER ARRAY. Code leas the base and
              indexes it, so the base register is marked with a sentinel and only an
              indexed load off it seeds a real receiver. MessageWindowRecord censused as
              zero FUNCTIONS under SEED=cell and as 20 displacements / 51 accesses here.
  SEED=call   (FN) `cell` is a GETTER's address and the object is its return value in rax.
              PersistentFlagPayload is SaveImage_GetActiveBuffer() + 0x200 and has no cell
              at all; it converges over 100 functions under this seed and cannot start
              under any other.
  SEED=static (STATIC) `cell` IS the object, not a pointer to it - a static route names
              the object's own address, so the register an lea puts it in is the receiver.
  SEED=vtable `cell` is the class's VTABLE. Every slot is entered with `this` in rcx by
              definition, so each slot seeds the fixpoint at base 0. THIS IS THE ONLY WAY
              INTO A TYPE THE CLUSTER SYSTEM CREATES - no cell, no getter, nothing to
              track from. PScheduler goes from 1 displacement to 22 and
              PMeshParticleSystemBase from 9 to 21. It covers VIRTUAL methods and whatever
              they call; a non-virtual member reached by a direct call from outside the
              class is still invisible, and a zero from this seed must say so.

HOW IT WORKS. Each tracked register carries a BASE OFFSET. A load of the cell starts a
register at 0. An lea of [r+d], a register copy, and an add or sub of an immediate all
propagate the base. Any write to a register drops it. An access at [r+d] is recorded at
base(r)+d. A call made while a tracked register is in rcx enqueues the callee at that
base, and the worklist iterates (function, base, argument-register) pairs to a
fixpoint - the entry register is always rcx unless ARGREGS=1 (below) widens the
enqueue rule to rdx/r8/r9 and lets a pair record which register carried the object
in.

FOUR THINGS IT GOT WRONG BEFORE IT GOT THEM RIGHT. Each cost a run and each is the
reason for a line of code, so do not simplify them back out:

  1. An lea was counted as an access. It computes an address and touches no memory.
     Leaving it in invented 22 phantom fields at unaligned +1/+2/+3 offsets.
  1b. SO WERE MULTI-BYTE ALIGNMENT NOPS - `nop dword ptr [rax]`, `nop word ptr [rax+rax]`.
     They carry a memory operand and access nothing. Excluding them removed 16 phantom
     accesses from the control alone (1,414 to 1,398) and a phantom 4-byte access at +0x00
     of ManagerSingleton0209BE80 that had helped fire the contamination canary. Found by
     reading a flagged site, 0028F3B4, and discovering it was padding. EVERY ACCESS COUNT
     PUBLISHED BEFORE THIS FIX IS INFLATED, by roughly 1% on the control.
  2. Interior pointers were not followed at all, so an embedded sub-object reported
     7 accesses for 4,368 bytes. An embedded object is reached by an lea and never by
     a field read - the same blindness that makes an offset census useless for it.
  3. Interior pointers formed by ARITHMETIC were still missed. The engine forms
     ManagerSub0209BE80_8FA0 with an add of 0x8FA0 at 26 sites and never an lea.
  4. One level of call depth was not enough: it reported zero accesses in every span
     of that type. The fixpoint found them.

IT SEPARATES READS FROM WRITES, AND YOU USUALLY WANT THE READS. Counting "any access"
is not enough for the question this tool exists to answer. On UQ-5 the first sites it
surfaced for every field were the BUILDER 001CCB20 writing defaults; reporting those as
consumers would have answered *who reads this* with a writer. Each (displacement,width)
row now prints `rN wN`, and a span whose accesses are all writes is called out as
WRITE-ONLY - nothing consumes it. The control splits 1,225 reads to 234 writes, and
UQ-5's +0xAB8 resolves to exactly `r1 w1`: 001CCBB1 writes the default, 001CDCD4 reads it.

IT OVER-ATTRIBUTES THROUGH GENERIC CALLEES, AND THIS IS ITS BIGGEST WEAKNESS. The
call-enqueue rule follows any call made while a tracked register is in rcx (or any
argument register under ARGREGS=1). When the
callee is a GENERIC HELPER - something many types call - its accesses are credited to the
seeded type, and nothing in the tool notices. Measured on 2026-09-21: PApplication's
getter census reports accesses at OFFSET 0 from `InputManager_TranslateBindingProfileTo
ControlState` (001973B9, `mov r8,[rax]`), FUN_0018d850 (0018E223, a 4-BYTE `mov ecx,[rax]`)
and FUN_001eb3d0 (001EB3D4, a 16-BYTE `movups xmm5,[rcx]`). None of those is touching a
PApplication - its +0x00 is an 8-byte vtable pointer.

  * AND IT IS GATED ON POLYMORPHISM, WHICH THE TOOL WILL NOT GUESS. The canary's whole
    premise is a vtable pointer at +0x00 that nothing may overwrite, so it says nothing
    about a type that has no vtable: Manager0209AC60 is memset at init and its +0x00 is a
    FLAGS DWORD - 00249425 `or dword ptr [rcx], 2`, 0024942B `test byte ptr [rcx], 2` -
    and the canary fired on it for three versions running. Gating it on an OBSERVED
    vtable install then broke the case it was built for: a getter-seeded closure never
    reaches the constructor, so PApplication showed no install and went silent too.
    ABSENCE OF AN OBSERVED INSTALL IS NOT ABSENCE OF A VTABLE. So: POLY=1 asserts the
    type is polymorphic and runs the canary, POLY=0 asserts it is not and stays quiet,
    and UNSET prints the widths seen at +0x00 with no verdict and says which flag to pass.
    HOW TO DECIDE WHICH TO PASS, without re-deriving it: LOOK AT THE STORE'S OWN +0x00
    ROW. A type whose +0x00 is declared as a non-pointer field is not polymorphic -
    BootSingleton01F7F598 carries `ctorWord0`, a 2-byte field, because its constructor
    00184F20 opens `mov word ptr [rcx], 0`, and Manager0209AC60's +0x00 is a flags dword.
    Both had the canary firing on them and both are POLY=0. A type whose +0x00 row is a
    vtable pointer - PApplication's `vptr_PApplication` - is POLY=1.
  * THE CANARY IS A FLAG, NOT A PROOF, AND I GOT THIS WRONG TWICE BEFORE SETTLING IT.
    First I said "any write to offset 0 of a type with a vtable proves mis-attribution" -
    false, a constructor legitimately writes offset 0, and the check fired on nearly
    every type. Then I narrowed it to "mixed widths at +0x00 including 8" and called it
    correct in both directions on the strength of a `tail -2` that had cut the canary's
    own output off; the control had been firing all along. The honest version: mixed
    widths at +0x00 MIGHT mean a generic callee is being credited here, and might equally
    be a 1-byte read of a pointer's low byte or a 16-byte copy of the object's head, both
    ordinary. ONLY READING THE SITES SETTLES IT - on PApplication, 0018E223 and 001EB3D4
    sit in unrelated bodies, which is what made that one a confirmed contamination.
    It fires on 5 of the 6 types censused on 2026-09-21; ONE of those is verified.
  * THE OLD FORM OF THIS NOTE, kept because it is the mistake: "the sharp canary is the
    width at offset 0, not the presence of a write. A constructor
    legitimately writes offset 0 (it installs the vtable), so "any write to 0" fires on
    almost every type and says nothing. But on a POLYMORPHIC type, ANY ACCESS AT +0x00
    THAT IS NOT AN 8-BYTE POINTER MOVE cannot be coherently touching the vtable, and is a
    mis-attribution. A 4-byte or 16-byte access at +0x00 is the tell.
  * WHAT TO TRUST, IN ORDER. A field read out of a NAMED writer or reader you have
    disassembled is evidence. A per-span reached/not-reached verdict is weaker. A raw
    DISPLACEMENT COUNT from a deep fixpoint is the weakest of the three and should be
    quoted as an upper bound, because contamination only ever adds.

ITS ONE KNOWN FALSE POSITIVE, and the cheap check for it. The call-enqueue rule adds a
callee at the caller's tracked base. That is right when the callee really receives that
object and WRONG when the tracked register is not what reaches rcx on the path that
matters - and then every offset the callee touches is attributed to the wrong type. It
happened once, on 2026-09-21: 00633070 was enqueued for PApplication and its interior
list-head writes were reported at +0x28 and +0x38, contradicting the constructor's byte
at +0x29 and qword at +0x2C. THE TELL WAS AT OFFSET ZERO: 00633070 opens with
`mov qword ptr [rcx], rcx`, and on a polymorphic type that would destroy the vtable
pointer. SO: IF A CENSUS CLAIMS A WRITE TO OFFSET 0 OF A TYPE WITH A VTABLE, THE
ATTRIBUTION IS WRONG. Check that before believing a surprising offset.

WHAT IT STILL MISSES, and a negative from this tool must say so. A pointer spilled to
the stack and reloaded; an access through an index register, which is skipped rather
than resolved - though since 2026-09-28 it is at least COUNTED: sites of the form
[tracked + idx*scale + disp] whose displacement could land inside the extent are
deduped into `indexed_skips`, printed after the totals and emitted in EMIT_JSON
(control Manager0209AC60: 70 such sites; measured shape is embedded sub-arrays -
pointer tables and per-index flag bytes like [rdx + rdi + 0xB2E]).
A pointer passed in a register other than rcx is missed ONLY UNDER
THE DEFAULT: ARGREGS=1 enqueues rdx/r8/r9 receivers too, each pair seeded on the
register the caller used. Measured demand before the option existed: 24 of 1,740
direct call sites of object/member-returning getters moved the return into a
non-rcx argument register (enumeration of 2026-09-30). THE OPTION ALSO WIDENS
THE PAIR SPACE: a function reached through two argument registers is scanned
once per register, so a hub closure spends CAP faster - measured 2026-09-28 on
the 33-type rerun cohort: cell 0209BE80/022C6F28 seeds that converged at 147
functions/1170 pairs rcx-only truncated at the 400 cap under ARGREGS=1 and
converged at CAP=8000 (1463 pairs / 149 functions on 0209BE80, 717 pairs / 369
functions on 022C6F28). Raise CAP on truncated widened runs, same rule as below.

IT REPORTS CONVERGENCE OR TRUNCATION EXPLICITLY. A run that hit the cap is not a
converged one and must not be quoted as though it were. THE DEFAULT CAP OF 400 IS NOT
ENOUGH FOR A WIDELY-USED SINGLETON, and this is not theoretical: BootSingleton01F7F598
through its getter hit the cap at 401 pairs on the first run. Raising CAP to 3000
converged in 13 rounds over 536 pairs and 489 functions, at 483 displacements and 1,794
accesses - and the truncated run had already reported 483 displacements, so the numbers
looked finished while the frontier was not. WITHOUT THE FLAG THAT RUN WOULD HAVE BEEN
WRITTEN UP AS COMPLETE. Raise the cap and re-run whenever it fires.

IT NAMES ITS OWN FALSE POSITIVES. _guard_check_icall reached a method set at a measured
rate of 1 in 15, because Control Flow Guard passes the call target in rcx. Guard and
thunk names are excluded; any survivor should be reported, not quietly dropped.

WRITE PER-SPAN RESULTS PER SPAN. A result measured over some spans must not be written
onto all of a type's rows. Doing that produced a published false negative on
ManagerSub0209BE80_8FA0 +0x1050, corrected in d192ec027.

--self-test runs the Manager0209AC60 control: cell 0x0209AC30 must yield at least 130
distinct displacements. Any change dropping below that has lost coverage. The 130 was
measured (147) after the CFG-walk + call-clobber fix of 2026-09-22 - the earlier 150
threshold was calibrated on clobber-inflated numbers and was retired with them.

FLOW-SENSITIVITY, added 2026-09-22 (FRONTIER, per OPUS-REQ-FRONTIER-SHARED-CENSUS-
WALKS-LINEARLY-NO-CFG). The pass now runs a per-instruction dataflow fixpoint over the
function's control-flow graph instead of walking bytes in address order, with a
GENEROUS join: a register's candidate bases union across predecessors, capped at 16
and saturating to a TOP that still propagates but never records. A receiver killed on
one arm (`xor ebx,ebx` in MSVC's inline out-of-range stub) therefore no longer stays
dead past the merge - on the type OPUS measured, the same enumeration went from 41
accesses/19 functions to 173/33. Jump-table arms and other resolved-edge orphans are
still visited, seeded from the union of indirect-jump exit states (or of all exit
states where there is no dispatch site) - the flat pass's whole-extent coverage is
preserved, now as an explicit approximation. AND `call` drops rax/rcx/rdx/r8-r11 from
tracking: capstone's regs_access does not report the volatile clobber, so a receiver
in a volatile register used to survive the call and mis-attribute everything after
it (161 -> 134 on the control from this fix alone). BOTH CHANGES MOVE PUBLISHED
NUMBERS: positives are re-derived by re-running; negatives published before this fix
were measured under a walk that could lose a receiver at any branch merge, and must
be re-run before being cited.

ITS SIBLING, AND WHY BOTH EXIST. `receiver_census.py` in this directory is also mine, a
session earlier, and it censuses ONE function's extent robustly given a receiver. This
file finds WHICH functions reach a type from its route and iterates call edges to a
fixpoint. I built this one without looking at that one, which was the mistake - not the
code - and the two hardening fixes it had and this did not are now PORTED HERE:

  * COMPUTED BASES. `add reg, REG` - a selector times a stride, selecting an array
    element - keeps the receiver, with the base unadvanced so displacements stay
    element-relative. Previously the receiver was dropped there.
  * FRAME RESTORE vs GENUINE RELOAD, told apart exactly rather than guessed. A store of a
    tracked register to `[rsp+d]` or `[rbp+d]` remembers that slot's base; only a load
    from a REMEMBERED slot restores it. A load from anywhere else still kills, because a
    reload from an object field is a different object. Without this, a `mov rbx,[rsp+0x50]`
    in one arm's epilogue killed the receiver for the rest of the flat pass - on one proc
    the sibling measured 3 offsets against 20 found by hand.
  * Already shared: both flat-pass the WHOLE extent, which is what makes jump-table arms
    visible; a linear walker cannot follow `jmp r8`.

WHAT THE FIXES CHANGED, measured rather than assumed. The control gained accesses (1,397
to 1,400) at the same 160 displacements; `SavePayload` gained 4 displacements and 4
accesses. **AND NOT ONE OF THE NEW FINDS LANDED IN A DECLARED DEBT SPAN**: the reached-span
counts for every type whose negative was published are unchanged - SavePayload 0 of 6,
FrameMarkerSingleton 0 of 3, GlyphRunWidget1498 8 of 16, LegacyPs2GsTextureContext 4 of 16.
So those negatives SURVIVED the hardening, and that is a measurement, not a hope.

RE-VERIFIED AFTER THE TOOL CHANGED, 2026-09-21. Four tracker rules and the cap lesson
landed AFTER most of the sweep was published, so every cell-seeded type was re-run at
CAP=3000 with the final tool and the reached/not-reached status of every span compared
against what was written. NOT ONE SPAN FLIPPED: Manager0209AC60 4 of 4, ManagerSingleton
0209BE80 2 of 29, GlyphRunWidget1498 8 of 16, SavePayload 0 of 6. Displacement totals
moved slightly - the rules do find a little more - but no recorded result changed, and
none of these truncated. A tool that changes under published results owes them a re-run;
this is that re-run.

Authored 2026-09-21 (OPUS) from the session scratchpad, after it corrected four types.
"""

import struct, collections, sys, os, json, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import (X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP,
                          X86_REG_RCX, X86_REG_RAX, X86_REG_RSP, X86_REG_RBP,
                          X86_REG_RDX, X86_REG_R8, X86_REG_R9, X86_REG_R10,
                          X86_REG_R11)

if "--self-test" in sys.argv:
    import subprocess
    r = subprocess.run([sys.executable, __file__, "0x0209AC30", "0", "0xE00"],
                       capture_output=True, text=True)
    m = re.search(r"distinct displacements: (\d+)", r.stdout)
    n = int(m.group(1)) if m else 0
    print(r.stdout.strip())
    # Threshold recalibrated 2026-09-22 after the CFG walk + call-clobber fix: the
    # control measures 147 distinct displacements under the corrected walker. The old
    # 150 was calibrated on output inflated by volatile registers surviving `call`
    # (161 -> 134 from the clobber alone), so it could never be a fair gate. 130 is a
    # margin below the corrected measurement; a drop under it means lost coverage.
    print("SELF-TEST control Manager0209AC60: %d distinct displacements, need >= 130 -> %s"
          % (n, "PASS" if n >= 130 else "FAIL"))
    sys.exit(0 if n >= 130 else 1)

CELL   = int(sys.argv[1], 16)
EMBED  = int(sys.argv[2], 16)
EXTENT = int(sys.argv[3], 16)
CAP    = int(os.environ.get("CAP", "400"))
# MODE picks how the FIRST receiver is obtained. Getting this wrong does not give a wrong
# answer, it gives ZERO FUNCTIONS - and a zero from the wrong seed must never be written
# onto a type's rows as a negative. See the MessageWindowRecord note.
#   cell  (default) CELL is a .data slot holding the object pointer
#   slots           CELL is the BASE of a pointer ARRAY; an indexed load off it is an element
#   call            CELL is a GETTER's address; its return value in rax is the object
MODE = os.environ.get("SEED", "cell")
if MODE not in ("cell", "slots", "call", "static", "vtable", "ctor"):
    print("SEED must be cell, slots, call, static, vtable or ctor"); sys.exit(2)
# ARGREGS=1 widens the call-enqueue rule from rcx to all four integer argument
# registers (rcx/rdx/r8/r9). Pair identity gains the ENTRY register - a callee
# reached with the object in rdx is scanned with rdx, not rcx, as its seeded
# receiver, so (fn, base, rdx) and (fn, base, rcx) are distinct pairs. Default is
# off because the measured residue is small (22 of 1,740 direct call sites of
# object/member-returning getters, 2026-09-30 enumeration) and every extra arg
# register multiplies pairs against CAP.
ARGREGS = os.environ.get("ARGREGS") == "1"
_ARGLIST = ((X86_REG_RCX, X86_REG_RDX, X86_REG_R8, X86_REG_R9)
            if ARGREGS else (X86_REG_RCX,))
ARRAY = -1 << 40      # sentinel base: "this register holds the slot-array base, not an object"
import kit_paths as KP
import reg_tracking as RT
EXE = os.path.join(KP.ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FNS = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
BASE = 0x120000
d = open(EXE, "rb").read(); pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe+6)[0]; optsz = struct.unpack_from("<H", d, pe+20)[0]
secs = []
for i in range(nsec):
    o = pe+24+optsz+i*40; vsz, va, rawsz, raw = struct.unpack_from("<IIII", d, o+8)
    secs.append((va, vsz, raw, rawsz))
def fo(v):
    r = v-BASE
    for va, vsz, raw, rawsz in secs:
        if va <= r < va+vsz and r-va < rawsz: return raw+(r-va)
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
sizes = {}; names = {}
allfns = []
for ln in open(FNS, encoding="utf-8", errors="replace"):
    c = ln.rstrip("\n").split("\t")
    if len(c) > 2 and len(c[0]) == 8 and c[2].isdigit():
        a = int(c[0], 16); sizes[a] = int(c[2]); names[a] = c[1]; allfns.append(a)
SKIP = lambda a: (sizes.get(a, 0) < 8 or sizes.get(a, 0) > 60000
                  or "guard_check" in names.get(a, "") or "guard_dispatch" in names.get(a, "")
                  or names.get(a, "").startswith("thunk_"))

acc = collections.Counter(); sites = collections.defaultdict(set)
rd = collections.Counter(); wr = collections.Counter()
indexed_skips = set()              # site VAs skipped because the access was indexed
siterw = {}                             # (disp, width, siteVA) -> [isRead, isWrite]
vtinstall = []   # sites that store an .rdata address into +0x00 - the vtable install
_recorded = set()   # (site, disp, width) already counted - the CFG fixpoint revisits
# ENUMERATED SITES (OPUS, 2026-09-28). The generous join enumerates a loop's induction values up to BASECAP, so
# `add rbx, 0x68` around a call reaches the callee at every base the extent allows - including elements the loop's
# trip count never produces (LegacyPs2GsTextureContext: a two-iteration clear reported at +0x110 / +0x178 / +0x1E0).
# That over-report is the design (negatives are published), but a POSITIVE reached only that way is not proof of an
# access. Each recording notes its context - the (function, base) pair being scanned and whether the base register held
# more than one candidate - and each enqueue notes the same; EMIT_JSON's `enumerated_sites` lists the sites with no
# recording traceable to a seed through single-candidate steps. Their trip count is not established by this census.
_CUR = [None]                                   # the (function, base) pair being scanned; None = a cell-mode seed scan
_SITECTX = collections.defaultdict(set)         # (disp, width, siteVA) -> {(pair, multi)}
_EDGES = set()                                  # (parent pair, child pair, multi)
                    # instructions, so every access is recorded once per site, matching
                    # the linear pass's semantics (acc ~= number of sites, not visits)
TOP = object()      # a tracked register whose base set overflowed - still "the object",
                    # but no displacement can be computed off it and nothing enqueues
BASECAP = 16        # join/loop bound: a register holding >16 candidate bases saturates
VOLATILE = frozenset((X86_REG_RAX, X86_REG_RCX, X86_REG_RDX,
                      X86_REG_R8, X86_REG_R9, X86_REG_R10, X86_REG_R11))
EMPTY_ST = ({}, {}, frozenset())     # (tracked, spill, rdata_regs)

def _joinv(a, b):
    if a is TOP or b is TOP: return TOP
    u = a | b
    return u if len(u) <= BASECAP else TOP

def _joinst(A, B):
    t, sp, rr = dict(A[0]), dict(A[1]), A[2] | B[2]
    for k, v in B[0].items():
        t[k] = _joinv(t[k], v) if k in t else v
    for k, v in B[1].items():
        sp[k] = _joinv(sp[k], v) if k in sp else v
    return (t, sp, rr)

def scan(addr, entry_base, seed_cell, entry_reg=X86_REG_RCX):
    """Walk one function's control-flow graph to a fixpoint; return (callee, base) calls.

    The old pass ran md.disasm once in address order, which made every negative it
    produced unsound: a receiver killed on one arm (`xor ebx,ebx` in MSVC's inline
    out-of-range stub) stayed dead for the rest of the body even though the live path
    re-merged with the receiver intact. Measured on one type, 2026-09-22 (OPUS): the
    same enumeration gives 41 accesses/19 functions linearly and 173/33 over the CFG.

    State is a per-register SET of candidate bases; the join is the union (generous -
    the census's failure direction must stay over-report, since its negatives are
    published). Sets cap at BASECAP and saturate to TOP so loops like `add rax,8`
    still terminate. Instructions unreachable by resolved edges - jump-table arms -
    are seeded from the union of dispatch-site exits, preserving the flat pass's
    whole-extent coverage. `call` drops the volatile registers from tracking: a
    callee may clobber them, and capstone's regs_access does not report it.
    """
    o = fo(addr); out = set()
    if o is None: return []
    insns = {}
    for ins in md.disasm(d[o:o+sizes[addr]], addr):
        insns[ins.address] = ins
    order = sorted(insns)
    if not order: return []
    nxt = {order[i]: order[i+1] for i in range(len(order)-1)}
    succ = {}; ind = []
    for a in order:
        ins = insns[a]; ops = ins.operands; m = ins.mnemonic; s = []
        fall = nxt.get(a)
        if m == "jmp" and len(ops) == 1 and ops[0].type == X86_OP_IMM:
            if ops[0].imm in insns: s = [ops[0].imm]
            # an out-of-function jmp imm is a tail call - the callee enqueues below
        elif m == "jmp":
            ind.append(a)     # jmp reg/mem: jump-table dispatch, no resolved edge
        elif (m.startswith("j") or m in ("loop", "loope", "loopne")) \
             and len(ops) == 1 and ops[0].type == X86_OP_IMM:
            if ops[0].imm in insns: s.append(ops[0].imm)
            if fall: s.append(fall)
        elif m.startswith("ret") or m in ("ud2", "int3", "iret", "iretq", "iretd"):
            pass
        elif fall:
            s = [fall]
        succ[a] = s

    def xfer(ins, st):
        """One instruction: (new state, enqueued calls). Recording is a side effect."""
        tracked = dict(st[0]); spill = dict(st[1]); rdata_regs = set(st[2])
        # the shared kill set (reg_tracking.written): sub-registers fold to their 64-bit parent, so
        # `mov ecx, 1` now kills a tracked rcx, and capstone's cmpxchg / cdq / test implicit-write
        # tables are corrected (FRONTIER-REQ-OPUS-ACCESS-FLAG-PRODUCER-REPAIR)
        _wn = RT.written(ins)
        written = {r for r in set(st[0]) | set(st[2]) if RT.canon(ins.reg_name(r)) in _wn}
        ops = ins.operands; newt = None
        if seed_cell and MODE == "call" and ins.mnemonic == "call" and len(ops) == 1 \
           and ops[0].type == X86_OP_IMM and ops[0].imm == CELL:
            # MODE=call: the object arrives as a GETTER'S RETURN VALUE, not from a cell.
            # PersistentFlagPayload is SaveImage_GetActiveBuffer() + 0x200 and has no cell
            # at all; without this the census cannot start on such a type.
            newt = (X86_REG_RAX, frozenset((0,)))
        elif seed_cell and MODE == "static" and ins.mnemonic == "lea" and len(ops) == 2 \
             and ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP \
             and ops[0].type == X86_OP_REG \
             and ins.address+ins.size+ops[1].mem.disp == CELL:
            # MODE=static: CELL IS THE OBJECT, not a pointer to it. A STATIC route names the
            # object's own address, so code leas it and that register IS the receiver at base 0.
            # Using SEED=cell here reads the object's first 8 bytes as if they were a pointer
            # and censuses whatever that garbage addresses - it does not merely find nothing.
            newt = (ops[0].reg, frozenset((0,)))
        elif seed_cell and MODE == "slots" and ins.mnemonic == "lea" and len(ops) == 2 \
             and ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP \
             and ops[0].type == X86_OP_REG \
             and ins.address+ins.size+ops[1].mem.disp == CELL:
            # MODE=slots: CELL is the BASE OF A POINTER ARRAY, not a pointer to the object.
            # Code leas the base and indexes it, so the base register is marked ARRAY (a
            # sentinel base) and only an indexed load off it seeds a real receiver. Without
            # this a SLOTPTR type censuses as zero FUNCTIONS, which is not a negative about
            # the type - it is the tool failing to start. See MessageWindowRecord.
            newt = (ops[0].reg, frozenset((ARRAY,)))
        elif seed_cell and MODE == "cell" and ins.mnemonic == "mov" and len(ops) == 2 \
           and ops[1].type == X86_OP_MEM \
           and ops[1].mem.base == X86_REG_RIP and ops[0].type == X86_OP_REG \
           and ins.address+ins.size+ops[1].mem.disp == CELL:
            newt = (ops[0].reg, frozenset((0,)))
        elif ins.mnemonic == "mov" and len(ops) == 2 and ops[1].type == X86_OP_MEM \
             and tracked.get(ops[1].mem.base) is not TOP \
             and ARRAY in tracked.get(ops[1].mem.base, ()) \
             and ops[0].type == X86_OP_REG:
            # loading an ELEMENT POINTER out of the slot array: the destination now holds a
            # real receiver at base 0. The element index is dynamic and is not recovered.
            newt = (ops[0].reg, frozenset((0,)))
        elif ins.mnemonic == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM \
             and ops[1].mem.base in tracked and ops[1].mem.index == 0 \
             and ops[0].type == X86_OP_REG:
            _v = tracked[ops[1].mem.base]
            if _v is TOP:
                newt = (ops[0].reg, TOP)
            else:
                _nb = frozenset(b + ops[1].mem.disp for b in _v if b != ARRAY)
                if _nb: newt = (ops[0].reg, _nb)
        elif ins.mnemonic == "mov" and len(ops) == 2 and ops[1].type == X86_OP_REG \
             and ops[1].reg in tracked and ops[0].type == X86_OP_REG:
            newt = (ops[0].reg, tracked[ops[1].reg])
        elif ins.mnemonic in ("add","sub") and len(ops) == 2 and ops[0].type == X86_OP_REG \
             and ops[0].reg in tracked and ops[1].type == X86_OP_IMM:
            _v = tracked[ops[0].reg]
            _sgn = 1 if ins.mnemonic == "add" else -1
            if _v is TOP:
                newt = (ops[0].reg, TOP)
            else:
                _nb = frozenset(b + _sgn*ops[1].imm for b in _v if b != ARRAY)
                if _nb: newt = (ops[0].reg, _nb)
        elif ins.mnemonic == "add" and len(ops) == 2 and ops[0].type == X86_OP_REG \
             and ops[0].reg in tracked and tracked[ops[0].reg] is not TOP \
             and tracked[ops[0].reg] != frozenset((ARRAY,)) \
             and ops[1].type == X86_OP_REG:
            # COMPUTED BASE. `add rbx, rcx` where rcx is selector*stride SELECTS AN ARRAY
            # ELEMENT, so the register still points at an object of this type and the base
            # stays where it was - element-relative. Dropping the receiver here is what made
            # receiver_census.py's blind spot 2, and this file had the same hole until now.
            # The added term is unknown, so the base is NOT advanced; displacements stay
            # element-relative, which is what a per-element census wants.
            newt = (ops[0].reg, tracked[ops[0].reg])
        elif ins.mnemonic == "add" and len(ops) == 2 and ops[0].type == X86_OP_REG \
             and ops[1].type == X86_OP_REG and ops[1].reg in tracked \
             and tracked[ops[1].reg] is not TOP \
             and tracked[ops[1].reg] != frozenset((ARRAY,)) \
             and ops[0].reg not in tracked:
            # THE MIRROR CASE, and the one that matters for an INLINE array. When the stride
            # is too large for an x86 scaled index (they stop at 8), the compiler computes
            # `imul rax, slot, STRIDE` and then `add rax, base` - the INDEX is the destination
            # and the BASE is the source, the opposite way round from the rule above. Without
            # this, BattleUnit (PARRAY stride 0xF50) censused 3 displacements where its
            # elements are plainly worked on, and that thinness could have been read as
            # absence. The result is an element pointer, so it inherits the array base.
            newt = (ops[0].reg, tracked[ops[1].reg])
        elif seed_cell and MODE in ("cell", "static") and ins.mnemonic == "add" \
             and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM \
             and ops[1].mem.base == X86_REG_RIP \
             and ins.address+ins.size+ops[1].mem.disp == CELL:
            # `add rax, qword ptr [rip -> CELL]` - the base is added STRAIGHT FROM MEMORY,
            # never loaded into a register first. READ OUT OF 0023683A, not guessed: two
            # earlier guesses at BattleUnit's idiom (a scaled index, then add of a register)
            # both left it at 3 displacements. rax already holds slot*stride, so the sum is
            # an element pointer and the base is element-relative 0.
            newt = (ops[0].reg, frozenset((0,)))
        elif ins.mnemonic in ("call","jmp") and len(ops) == 1 and ops[0].type == X86_OP_IMM:
            for _ar in _ARGLIST:
                if _ar not in tracked: continue
                _v = tracked[_ar]
                if _v is TOP: continue
                _nb = len([x for x in _v if x != ARRAY])
                for _b in _v:
                    if _b != ARRAY:
                        out.add((ops[0].imm, _b, _ar))
                        _EDGES.add((_CUR[0], (ops[0].imm, _b, _ar), _nb > 1))
            # a TOP arg register = "still the object, base unknown": the callee cannot be
            # enqueued because a (function, base, register) pair needs a number.
            # Under-enqueues, never lies.
        # `nop dword ptr [rax]` and `nop word ptr [rax+rax]` are multi-byte ALIGNMENT
        # PADDING. capstone gives them a memory operand, but they access nothing, and
        # counting them invents an access at whatever offset the padding happens to
        # encode - found at 0028F3B4, which was reported as a 4-byte access at +0x00
        # of ManagerSingleton0209BE80 and is not an access at all.
        if ins.mnemonic not in ("lea", "nop") and not ins.mnemonic.startswith("prefetch"):
            for oi, op in enumerate(ops):
                if op.type == X86_OP_MEM and op.mem.base in tracked \
                        and op.mem.index != 0:
                    # INDEXED-ACCESS bound, made visible: [tracked + idx*scale + d]
                    # is an element-relative access the instrument cannot place, so it
                    # is skipped - but it is COUNTED, deduped per site, so a run's
                    # negative can say how much sits outside the envelope rather than
                    # the limit existing only in this docstring. Only sites whose
                    # displacement could land inside the extent are counted - an
                    # indexed access outside it cannot be this object's field anyway.
                    _v = tracked[op.mem.base]
                    if _v is TOP or any(_b != ARRAY
                                        and 0 <= _b + op.mem.disp - EMBED < EXTENT
                                        for _b in _v):
                        indexed_skips.add("%08X" % ins.address)
                if op.type == X86_OP_MEM and op.mem.base in tracked and op.mem.index == 0:
                    _v = tracked[op.mem.base]
                    if _v is TOP: continue
                    _nb = len([x for x in _v if x != ARRAY])
                    for _b in _v:
                        # the ARRAY sentinel is a registry base, NOT an object: counting a
                        # displacement off it would invent fields out of slot indices
                        if _b == ARRAY: continue
                        dp = _b+op.mem.disp-EMBED
                        if not (0 <= dp < EXTENT): continue
                        _SITECTX[(dp, op.size, "%08X" % ins.address)].add((_CUR[0], _nb > 1))
                        _dk = (ins.address, dp, op.size)
                        if _dk in _recorded: continue
                        _recorded.add(_dk)
                        acc[(dp, op.size)] += 1; sites[(dp, op.size)].add("%08X" % ins.address)
                        # READ vs WRITE. Counting "any access" let a BUILDER writing defaults
                        # be reported as a consumer on UQ-5 - the who-reads-this question the
                        # census exists to answer. capstone marks each operand's access, so
                        # the two are separated here rather than by hand afterwards.
                        try:
                            # shared policy, not raw capstone flags. Kept in its own name: the per-site
                            # key below was also called _k, which silently zeroed every EMIT_JSON
                            # [read, write] flag from 6b6a423db until 2026-09-28 (OPUS)
                            _ak = RT.op_kind(ins, op, oi)
                            if _ak in ("w", "rw"): wr[(dp, op.size)] += 1
                            if _ak in ("r", "rw"): rd[(dp, op.size)] += 1
                            # PER-SITE, not just per-(displacement,width). Two SEEDS reach
                            # overlapping call graphs, so unioning their results by ADDING
                            # access counts double-counts every instruction both of them
                            # found. Only a set of site addresses unions correctly, so the
                            # r/w decision is recorded against the site that made it.
                            _k = (dp, op.size, "%08X" % ins.address)
                            _v2 = siterw.setdefault(_k, [0, 0])
                            if _ak in ("r", "rw"): _v2[0] = 1
                            if _ak in ("w", "rw"): _v2[1] = 1
                        except Exception:
                            pass
                        # A vtable install is an 8-byte store at +0x00 of a value the
                        # function just lea'd out of .rdata. Recording it is what lets the
                        # contamination canary tell a POLYMORPHIC type from one whose +0x00
                        # is an ordinary field - Manager0209AC60 is memset at init and its
                        # +0x00 is a flags dword, so the canary must stay quiet there.
                        if dp == 0 and op.size == 8 and ins.mnemonic == "mov"                            and len(ops) == 2 and ops[1].type == X86_OP_REG                            and ops[1].reg in rdata_regs:
                            vtinstall.append("%08X" % ins.address)
        # FRAME RESTORE versus GENUINE RELOAD. A flat pass walks every arm's epilogue, so a
        # `mov rbx, [rsp+0x50]` there would kill the receiver for the whole remainder of the
        # body - receiver_census.py measured 3 offsets against 20 found by hand on one proc.
        # But a reload from an OBJECT field is a different object and must kill. The two are
        # told apart exactly, not by guessing: a store of a tracked register to a stack slot
        # remembers that slot's base, and only a load from a remembered slot restores it.
        if ins.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM \
           and ops[0].mem.base in (X86_REG_RSP, X86_REG_RBP) and ops[0].mem.index == 0 \
           and ops[1].type == X86_OP_REG and ops[1].reg in tracked:
            spill[(ops[0].mem.base, ops[0].mem.disp)] = tracked[ops[1].reg]
        restored = None
        if ins.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
           and ops[1].type == X86_OP_MEM and ops[1].mem.base in (X86_REG_RSP, X86_REG_RBP) \
           and ops[1].mem.index == 0 and (ops[1].mem.base, ops[1].mem.disp) in spill:
            restored = (ops[0].reg, spill[(ops[1].mem.base, ops[1].mem.disp)])
        if (ins.mnemonic == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM
                and ops[1].mem.base == X86_REG_RIP and ops[0].type == X86_OP_REG):
            t_ = ins.address + ins.size + ops[1].mem.disp
            (rdata_regs.add if 0x800000 <= t_ < 0x1F00000 else rdata_regs.discard)(ops[0].reg)
        for w in written:
            if ins.mnemonic != "lea": rdata_regs.discard(w)
        for w in written: tracked.pop(w, None)
        if ins.mnemonic == "call":
            # A callee may clobber every volatile register; capstone's regs_access does
            # not report it, so without this a receiver in rax/rcx/rdx/r8-r11 survived
            # the call and everything after it was attributed to the wrong object -
            # the measured inflation on the control was 161 -> 134 displacements.
            # Applied BEFORE newt so MODE=call's rax seed (the getter's return value)
            # still lands, and before `restored` so a post-call reload can win.
            for v in VOLATILE:
                tracked.pop(v, None); rdata_regs.discard(v)
        if restored: tracked[restored[0]] = restored[1]
        if newt: tracked[newt[0]] = newt[1]
        return (tracked, spill, frozenset(rdata_regs))

    IN = {}
    OUT = {}
    IN[addr] = EMPTY_ST if seed_cell else ({entry_reg: frozenset((entry_base,))},
                                           {}, frozenset())
    wl = collections.deque([addr]); onwl = {addr}; visited = set()
    while True:
        while wl:
            a = wl.popleft(); onwl.discard(a)
            st = IN.get(a)
            if st is None: continue
            visited.add(a)
            ns = xfer(insns[a], st)
            OUT[a] = ns
            for s in succ[a]:
                j = _joinst(IN.get(s, EMPTY_ST), ns)
                if IN.get(s) != j:
                    IN[s] = j
                    if s not in onwl: wl.append(s); onwl.add(s)
        # Orphan blocks: instruction ranges no resolved edge reaches - jump-table
        # arms above all. The flat pass covered them by walking bytes; here they are
        # seeded from the union of dispatch-site (jmp reg/mem) exit states, which is
        # the generous-and-honest approximation of "entered however the table sent
        # us". With no dispatch site, the union of every exit state stands in.
        heads = []
        prev = True
        for a in order:
            if a not in visited:
                if prev: heads.append(a)
                prev = False
            else:
                prev = True
        if not heads: break
        base_st = EMPTY_ST
        srcs = [a for a in ind if a in OUT] or list(OUT)
        for a in srcs: base_st = _joinst(base_st, OUT[a])
        for h in heads:
            IN[h] = _joinst(IN.get(h, EMPTY_ST), base_st)
            if h not in onwl: wl.append(h); onwl.add(h)
    return list(out)

seeds = []
if MODE == "vtable":
    # SEED=vtable: CELL is the class's VTABLE. Every slot is entered with `this` in rcx by
    # definition, so each slot is a seed at base 0 and the fixpoint then follows the call
    # edges out of them. This is for a type the cluster system creates - no cell, no getter,
    # nothing to track from. The vtable is the only receiver-proven way in.
    # It covers VIRTUAL methods and whatever they call; a non-virtual member reached by a
    # direct call from outside the class is still invisible, and a zero must say so.
    o = fo(CELL)
    if o is None:
        print("vtable address not in the image"); sys.exit(2)
    for i in range(200):
        p = struct.unpack_from("<Q", d, o + i * 8)[0]
        if not (0x120000 <= p < 0x900000): break
        seeds.append((p, 0, X86_REG_RCX))
elif MODE == "ctor":
    # SEED=ctor: CELL is a FUNCTION that is entered with `this` in rcx - a constructor, or any
    # member whose receiver is the first argument. Same receiver proof as a vtable slot, and it
    # is the only way into the 107 debt-carrying types that have no cell, no getter, no array and
    # no MSVC class RTTI to hang a vtable on. Their ctor address is often the one thing the store
    # already records about them.
    #
    # THE LIMIT THAT MAKES OR BREAKS IT: this is sound only if the function constructs THIS type
    # and nothing else. Constructors ARE shared in this image - 00245000 is recorded as the ctor
    # of both BattleMenuChildWidget1620 and HelpMessageWidget0500, and 00244F50 of two
    # ManagerSub0209AC60 types - and seeding a shared ctor would credit one type with another's
    # fields, which is how a census invents a merged layout. The caller must establish exclusive
    # ownership before using this mode; the tool cannot see the store and will not check it.
    if fo(CELL) is None:
        print("ctor address not in the image"); sys.exit(2)
    seeds.append((CELL, 0, X86_REG_RCX))
else:
    for a in allfns:
        if SKIP(a): continue
        _CUR[0] = None
        seeds += list(scan(a, 0, True))
seen = set(); work = [(c, b, r) for c, b, r in seeds if c in sizes and not SKIP(c)]
rounds = 0; truncated = False
while work:
    rounds += 1
    nxt = []
    for fn, b, rg in work:
        if (fn, b, rg) in seen: continue
        seen.add((fn, b, rg))
        if len(seen) > CAP: truncated = True; break
        _CUR[0] = (fn, b, rg)
        nxt += [(c, nb, nr) for c, nb, nr in scan(fn, b, False, rg)
                if c in sizes and not SKIP(c)]
    if truncated: break
    work = nxt
print("methods reached at a fixpoint: %d (function,base,arg) pairs, %d distinct functions, %d rounds%s"
      % (len(seen), len({f for f, _, _ in seen}), rounds, "  [TRUNCATED AT CAP]" if truncated else "  [CONVERGED]"))
# CONTAMINATION CANARY, run automatically because I only caught it by hand once.
# On a polymorphic type +0x00 holds an 8-byte vtable pointer, so ANY access there of a
# different width cannot coherently be touching this object - it is a generic callee's
# access credited to the seed. Reported, never silently dropped: the run may still be
# useful, but its displacement count is an upper bound.
# Fires only on MIXED widths at +0x00 that INCLUDE 8. A non-polymorphic type may
# legitimately have a 4-byte field at offset 0 - that is not contamination, and an
# earlier version of this check fired on the control for exactly that reason. What
# cannot be true is an 8-byte pointer AND a narrower or wider access at the same
# offset: one of them is not this object.
# GATED ON ACTUAL POLYMORPHISM. The canary's premise is that +0x00 holds a vtable
# pointer that nothing may overwrite. That is false for a type without a vtable:
# Manager0209AC60 is memset at init and its +0x00 is a FLAGS DWORD - 00249425 does
# `or dword ptr [rcx], 2` and 0024942B `test byte ptr [rcx], 2`, both perfectly
# legitimate. So the canary only speaks when a VTABLE INSTALL was actually seen.
_poly = os.environ.get("POLY")          # "1" / "0" to assert; unset = undetermined
_is_poly = (_poly == "1") or (vtinstall and _poly != "0")
_w_all = {w for (dp, w) in acc if dp == 0} if _is_poly else set()
_w0 = sorted(w for w in _w_all if w != 8) if 8 in _w_all else []
if vtinstall and not _w0:
    print("polymorphic (vtable installed at %s); no width conflict at +0x00."
          % ", ".join(sorted(set(vtinstall))[:3]))
if not _is_poly and _poly != "0":
    _mix = sorted({w for (dp, w) in acc if dp == 0})
    print("POLYMORPHISM UNDETERMINED: no vtable install was seen in THIS run, which is not")
    print("  evidence of absence - a getter-seeded closure never reaches the constructor,")
    print("  and PApplication is exactly that case. The offset-0 canary is therefore NOT")
    print("  evaluated. Widths seen at +0x00: %s. Pass POLY=1 if the type has a vtable"
          % (", ".join("%dB" % w for w in _mix) or "none"))
    print("  (then the canary runs) or POLY=0 if it does not (then it stays quiet).")
elif _poly == "0":
    print("POLY=0 asserted: type has no vtable, offset-0 canary not applicable.")
if _w0:
    _n = sum(c for (dp, w), c in acc.items() if dp == 0 and w != 8)
    print("CONTAMINATION CANARY: %d access(es) at +0x00 with width(s) %s alongside an"
          % (_n, ", ".join("%dB" % w for w in _w0)))
    print("  8-byte one. THIS IS A FLAG FOR REVIEW, NOT A PROOF - a 1-byte read of a")
    print("  pointer's low byte is ordinary code, and so is a 16-byte copy of an object's")
    print("  head. What it reliably means is that this closure MIGHT include generic")
    print("  callees whose accesses are credited here. VERIFY BY READING THE SITES: on")
    print("  PApplication, 0018E223 and 001EB3D4 turned out to sit in unrelated bodies.")
    print("  Until verified, treat the displacement count as an UPPER BOUND.")
print("distinct displacements: %d ; pairs: %d ; accesses: %d  (READS %d, WRITES %d)"
      % (len({k[0] for k in acc}), len(acc), sum(acc.values()), sum(rd.values()), sum(wr.values())))
if indexed_skips:
    print("indexed accesses on a tracked base, skipped (not resolvable): %d site(s): %s"
          % (len(indexed_skips), " ".join(sorted(indexed_skips)[:20])
             + (" ..." if len(indexed_skips) > 20 else "")))
for lo, ln in json.loads(os.environ.get("DEBT","[]")):
    ins_ = sorted((dp,w,acc[(dp,w)]) for (dp,w) in acc if lo <= dp < lo+ln)
    sr = sum(rd[(dp, w)] for dp, w, _ in ins_); sw = sum(wr[(dp, w)] for dp, w, _ in ins_)
    print("\nSPAN +0x%04X len %-5d : %d pairs, %d accesses (READS %d, WRITES %d)"
          % (lo, ln, len(ins_), sum(c for _, _, c in ins_), sr, sw))
    if ins_ and sr == 0 and sw:
        print("      WRITE-ONLY: every access here is a write, so nothing CONSUMES this span.")
    for dp,w,c in ins_[:12]:
        print("      +0x%04X %dB x%-3d r%-2d w%-2d %s"
              % (dp, w, c, rd[(dp,w)], wr[(dp,w)], ", ".join(sorted(sites[(dp,w)])[:2])))
    if len(ins_) > 12: print("      ... %d more" % (len(ins_)-12))

# EMIT_JSON=<path> writes the full per-site result so a caller can UNION SEEDS EXACTLY.
# stdout is not sufficient for that: its detail lines print at most 2 sites per pair and
# stop after 12 pairs, so a driver that parsed them would silently under-report, and one
# that added the printed access counts across seeds would double-count every instruction
# two seeds both reached. The convergence flag travels with the data because a caller must
# never annotate from a TRUNCATED run.
_emit = os.environ.get("EMIT_JSON")
if _emit:
    _by = collections.defaultdict(dict)
    for (dp, w, site), (r, w_) in siterw.items():
        _by["%d:%d" % (dp, w)][site] = [r, w_]
    # a pair is PLAIN when a seed reaches it through single-candidate enqueues only; a site is ENUMERATED when no
    # recording of it is a single-candidate one inside a plain pair (or a cell-mode seed scan)
    _plain = set(p for p in seeds) if MODE in ("ctor", "vtable") else set()
    _grow = True
    while _grow:
        _grow = False
        for _par, _ch, _m in _EDGES:
            if not _m and _ch not in _plain and (_par is None or _par in _plain):
                _plain.add(_ch); _grow = True
    _enum = sorted("%d:%d:%s" % k for k, ctx in _SITECTX.items()
                   if not any(not _m and (_pr is None or _pr in _plain) for _pr, _m in ctx))
    json.dump({"seed": MODE, "cell": "%08X" % CELL, "embed": EMBED, "extent": EXTENT,
               "enumerated_sites": _enum,
               "converged": not truncated, "rounds": rounds,
               "functions": len({f for f, _, _ in seen}), "pairs": len(seen),
               "vtinstall": sorted(set(vtinstall)), "poly_asserted": _poly,
               "canary_widths": _w0, "indexed_skips": sorted(indexed_skips),
               "sites": _by},
              open(_emit, "w", encoding="utf-8"), indent=0)
