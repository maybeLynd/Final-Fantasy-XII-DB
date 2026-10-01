# Selected rendering flag stores: exact actor-kind overlap condition

Producer checked Method A; independent review/canonical adoption pending.
No machine code, native harness or game was executed. Retained shipping
21B/19B snippets retain **UNPROVED_CATALOGUE_ONLY** extent labels. The
129B2E6000 body binds the actor gate to byte3 maskE0. No all-functions,
all-entry, initialized-pointer or full class-stability proof is awarded.

Original3E33E0 updates bit23 and raises dirty bit1. Original3E3440 updates
bit24 and raises dirty bit2. The original two DWORD reads are **independent**
d0/d1. In `(((shifted_input ^ d0) & mask) ^ d1) | dirty`, every bit outside
mask|dirty copies d1. This holds even when d0 differs from d1; it does not
make the complete operation atomic or force the requested bit's value.

Let actor base beA, flag-word addressF, actor class byteA+3, and assume
nonwrapping valid memory. A DWORD store covering that byte must have
F=A+q, q0..3. The class mask in that DWORD isE0 shifted by8*(3-q).

- **3E3440:** bits24/2 never intersect class bits at any of these four
  placements. Its computed store retains the class bits sampled in d1
  even for unaligned/overlapping storage. No alignment premise is needed.
- **3E33E0:** only F=A+1 intersects them: bit23 reaches actor byte3 bit7.
  All other covering placements retain class bits from d1. An algebraic
  counterexample usesDX1/d00/d10, computed00800002 atF=A+1, changing actor
  class-byte mask from0 to80. It is not an observed initialized alias.
- If both bases are4-aligned, F=A+1 is excluded. Alignment remains a
  condition requiring separate initialized-layout evidence. Nonaliasing
  is sufficient but stronger than these exact source-derived conditions.

Actual preservation in memory also requires no interfering write between
d1 and this store, and comparison with an earlier class gate requires the
corresponding longer no-interference premise. The invariant describes the
computed value, not scheduling/lifetime/concurrency or other native stores.

The reducer validates the retained successful original checker receipt,
exact helper/EXE identities, selected byte/hash/annotation agreement, and
actually calls the reviewed shared adapter with store/LEA/RMW controls.
It then checks256 Boolean triples over32 independent bit columns per
snippet (512 algebraic cases). Arbitrary shifted input bits overapproximate
legal MOVZX/SHL outputs for this preservation lemma. These are not512 FF12
samples or native runs and are not an exact model of omitted operations.

The single actual positive and four synthetic actual CLI refusals are
retained: upstream checker exit1, wrong memory-store role, coherent changed
mask bytes, missing original class gate. Every refusal emits no result.
Existing6B/R13/SPEC/OPUS work is consumed as already delivered, not rerun.
No peer page or claim was edited. Other native delegates and full CON-172
remain open. Source shape/published original evidence is not self-acceptance.

Reproduce using a fresh output and the included selected retained input
directory: `python -B prove-flag-class-mask.py flag-class-mask-input-01 FRESH_RESULT`.
Control CLI requires a fresh directory. Original raw files retain links
to their full parent package; this supplement validates only selected
two snippets and class-gate body, not a fake complete parent export.

FABLE/OPUS should consume the precise bit/geometry condition after review,
and keep actual initialized alignment/alias/no-interference obligations
separate. No whole runtime/OV row closes. Full L1+L2/M0-M5 goal ACTIVE/NOT_MET;
menu branch spent/unapproved, EXP127 invalid. Offline reference unchanged,
all own bounded children terminal, no game/PC/instrument/save/config writes.
