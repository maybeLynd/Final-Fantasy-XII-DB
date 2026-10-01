# HP clamp needs an ordered-bounds precondition

The current contract's universal `floor <= hp <= cap` invariant does not follow
from the original clamp for inconsistent bounds. The implementing page's matching
player summary and its "only bottom value" explanation need the same qualification.
This package derives the branch structure from shipping code, without a fresh run.

Question, hypotheses, method choice and limits are in PLAN.md. source.json retains
the whole 880-byte HP body through RET at0030089F, the27-byte floor setter through
RET at0023983A, exact bytes/hashes/disassembly, reader/tool identity and consumer
preimages. The full HP hash matches the retained EXP093 body record. check.py
checks precise instructions and five historical original-code positive controls;
it does not rerun EXP093 or its mutations. validation.json is a producer check,
not independent acceptance. observation.json contains **symbolic**, unexecuted
branch illustrations and the source-derived conclusion.

The original local clamp reads old HP, adds the signed32 delta, then does:

```text
candidate = signed32(old + delta)
if candidate < floor:
    localResult = floor       # 00300651
    goto convergence         # 00300654 -> 003006A7; skips all cap tests
else:
    localResult = min(candidate, effectiveCap)  # signed comparison
# no second floor comparison before this body's HP store at00300749
```

The effective cap has the existing freeze/Bubble status rules. These witnesses
use both status layers0, so it is simply max HP; additions stay within signed32.

| old | delta | floor | max HP | local result | path |
|---:|---:|---:|---:|---:|---|
| 50 | -40 | 20 | 50 | 20 | ordered lower control |
| 50 | 100 | 20 | 50 | 50 | ordered upper control |
| 50 | 0 | 80 | 50 | **80** | floor selected, cap not consulted |
| 50 | 100 | 80 | 50 | **50** | cap selected, floor not rechecked |

The last two cannot satisfy both bounds. There is no source correction needed to
the published clamp formula; its **unqualified invariant** is what fails. For
this local algorithm, ordered floor/cap is required before promising both bounds.
Preserve the original branch order; an extra second clamp would change behavior.

The floor setter00239820 saves the supplied EDX in EBX, calls0031B760's unit
lookup, and, if that returns nonnull, writes EBX unchanged to unit+48. This27B
body has no cap comparison or clamp. That statement does not prove every caller
can create inconsistent bounds or that a shipped script does so. HP's own target
lookup reads unit+48 into the stack floor slot; no floor/max ordering test occurs
in the local clamp. The contract's separate downstream second-store qualification
still stands, but its assertion that the two-sided bound survives also needs an
actual ordered-bounds/callee proof; this package does not supply that proof.

Five retained EXP093 cases establish ordinary ordered-bound controls at the
isolated original-code class with the original deep stubs disclosed. They remain
valid. No prior raw result/mutation was changed or invalidated. The new finite
witnesses lie outside that listed boundary coverage and are not execution receipts.

Limits: admitted local write, finite no-overflow values and statuses0. Source/callee
side effects, ordinary command reachability, normal script occurrence, death/KO/
revival, final post-recompute HP, other status combinations and integer-wrap domains
are untested. A source branch illustration is not evidence that normal gameplay
reaches it. FABLE/OPUS qualification and independent SPEC review remain pending.

Cleanup: binary/artifacts read-only. No game, PC control, native attachment/input,
save/config/reference changes or fresh live restoration receipt. L1+L2 NOT_MET.

Player version: a scripted minimum higher than maximum HP creates contradictory
limits. The original code may choose either limit depending on the requested
change, rather than reconciling them. Modders need that precondition stated.
