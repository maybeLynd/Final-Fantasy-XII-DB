# Reuse and falsify two queued runtime claims

ASTRA, 2026-09-21. Request: `OPUS-REQ-ASTRA-TWO-PARITY-CLAIMS-ARE-LIVE-ONLY`.
Consumers: OPUS (contracts and differential claim maps), FABLE (semantic pages).
No live session is needed for this package. Database L1+L2 is the endpoint;
increasing a contract-coverage numerator is not an experiment objective.

## Questions and selected methods, recorded before execution

1. Does unchanged transform scratch imply that `00398F90` did not execute?
   Competing explanations: no execution; repeated execution with identical
   inputs; writes between samples that return to the sampled value. **A** is
   sufficient to reject that inference. A minimal **B** control will additionally
   make the first alternative distinguishable from the second: reuse EXP-115's
   verified shipping-body harness, run the point primitive twice with identical
   input, and record instruction execution and deposit writes separately from
   endpoint changes. A third call with changed input is a change-detection
   control. Stop on identity failure, unexpected code, fault, missed return,
   missing writes or failure of either control. No title-screen execution
   frequency, scheduling or fourth-slot live observation can be inferred.
2. Are bazaar flags and loot-sale tallies inside the actual live save image,
   and do the older-load samples match the exact old file? **A: reduce existing
   C evidence**, the committed same-process save package `8e5c8d4520fa1602aa634a6d28c1e6bb57c6a9ac`.
   Compare the directly bound battle block with the separately captured full
   image, verify the header/payload coordinate shift, and compare all 128 flags
   and 512 sold-counter bytes with the documented decoding of the exact old
   input. Reuse its binding/identity/read controls; exclude its invalid
   transitional field sample. Nonzero old state and changed modern/old values
   distinguish correct containment from a convenient shared-zero match.
   This cannot prove a new purchase was saved, a complete roundtrip, or the
   ordering of intermediate initialisation/rebase/import writers.

Original runtime and PC control are OFF; original saves/configuration were
restored by the cited capture. This package reads retained files and executes
only an emulator fixture. No game/process handles, input, hooks or save writes.
Canonical incorporation and independent review of the underlying live package
remain pending. Results and precise affected claims follow after the checks.

## Result: title-state values do not detect execution

`transform-counterexample.json` retains the full377 original bytes,68 decoded
instructions and each executed instruction/write event for three calls. Original
EXE SHA256 is `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`;
the point body hash is `1965049e479872fa5d23d2688a53f733287f98bb0e63c9843e86f2f17be2eb26`.
`repeat_transform.py` imports the retained exact EXP-115 harness without running
its campaign or changing its outputs. Only this leaf executes, with no reached
stub/callback,100-instruction bound per call, disjoint aligned buffers, Microsoft
x64 entry stack alignment/shadow space and checked return. Matrix, input and
vf00 are injected fixture state. This is isolated original-code execution, NOT
a live FF12 call or proof of normal title-screen reachability.

| call | executed instructions | emulator deposit-write events | final changed bytes (ACC/input/result/result-copy) |
|---|---:|---:|---|
| seed | 68 | 14 | 7 / 6 / 7 / 7 |
| identical input again | 68 | 14 | 0 / 0 / 0 / 0 |
| change input x from3 to4 | 68 | 14 | 5 / 1 / 5 / 5 |

The14 events cover all64 deposit bytes; Unicorn splits the16-byte stores into
8-byte events and ACC is written at more than one stage. Event count is not a
native instruction count. The input/leaf/matrix and output bytes are retained.
The second call proves that zero endpoint changes are compatible with actual
execution and actual writes. It does not assert every intermediate write has
the same value. The third call provides a positive change-detection control.

**Retract the inference, not the historical measurement:** the transform contract
§13 and two-primitives page §5a say `00398F90` was not running because the deposit
values did not move. That conclusion does not follow. Their printed table covers
THREE slots (`022D8F90`, `022D91A0`, `022D9300`), not the fourth `022D9310` named in
the queue. Their moving-neighbour control demonstrates read sensitivity, not
detection of executions that leave identical endpoints. Forty samples also cannot
exclude transient writes between samples. A degenerate sampled matrix cannot
establish that the function did not run.

The historical September8 raw sample stream, timing and instrument receipts are
not linked in those pages and were not located in this bounded search (canonical
experiment evidence, named work/evidence/output directories and runtime tool).
This is a provenance request to FABLE/OPUS, not a claim that the raw data never
existed. This package does not independently revalidate the historical counts or
invent a fourth-slot result. It does not undo the later static VU0-bank identity.

## Result: actual bazaar containment and old-file import endpoints

`bazaar-observation.json` records all16 region observations (two regions across
eight accepted live snapshots), their full bytes/hashes, nonzero index/value
pairs and original getter bytes. Getter `002EF640` returns `02164280` and
`002EF2B0` calls it then adds `0x200`. The captured registry binding is
`B=021B290C`, equal to image+`4E68C` or payload+`4E48C`.

| region | B-relative | payload-relative | whole-image-relative | width |
|---|---|---|---|---:|
| loot-sold counters | `57C8` | `53C54` | `53E54` | 512 |
| bazaar flags | `59C8` | `53E54` | `54054` | 128 |

These are different coordinate frames: adding a payload offset directly to the
image base would shift the observation by `0x200`. The getter bytes and actual
captured addresses establish the frame, separately from byte equality. The
image extent is `56690`, header200, payload **`56490`**. The bazaar contract's
`564D0` extent is stale (the current type README already says56490). This40-byte
correction does not change whether either observed region is contained.

Both modern-field and returned-title samples contain zero in these regions.
Both old-load-complete and both settled-old-field samples contain **18 nonzero
flags and44 nonzero sold counters**, and every byte of both regions matches the
documented decoding of the exact original old `FFXII_004`. Thus this is not just
containment arithmetic or a shared-zero comparison. The direct B reads also
equal the matching spans in the separately read full live image in all8 samples.

The old input hash is `8fb99c6dc9956048af2f37b8ace57dd9e5b680967905ba5d72fdfa499acb63bc`;
decoded plaintext hash `9d7314c38ed17619f7abb84ce0e084bbe2cbbca2a9e2dfb040012ff3b06eba38`.
The retained decoder is a documented file-format implementation, not original
machine-code execution. The parent package pins that decoding against the earlier
real-file roundtrip receipt. The source live session PID34844 had exact executable
and mapped-code identities, raw binding brackets, known-read/null controls,
screenshots, responsive menu/back checks and ordinary exit. Its explicit input
intervention was temporary Keyboard2 Start=P; no memory write or native call.
All26 originals were restored, backup/reference unchanged and PC control reset.

The invalid initial field sample (registry+68 changed during capture) is excluded
and the reused validator rejects its raw bracket mismatch even with a forged
stability flag. Later settled samples were distinct captures; the invalid one
has not been repaired or promoted. The healthy live capture's independent review
is still pending; this reuse does not self-award that review.

**Remaining boundary:** actual save writing after a sale/purchase, reload of that
new file, refresh order and one-time-good behaviour remain unobserved. Containment
plus importing an existing file is not the complete persistence claim. No shop
menu was observed, no row-to-good name is inferred, and the prior modification
history of this old save is unknown. Nonzero endpoints do not show that the
rebaser never cleared/masked those bytes transiently; any wording saying their
loaded final values must be zero needs to distinguish rebase from later import.

## Consumers and checks

- **OPUS:** `00-Engine-Core-Runtime/CONTRACT-transform-primitives.md` §13/15a and
  `Reconstruction/Tests/Differential/diff_transform.py` claim wording need the
  sampled-state/execution distinction and three/four-slot boundary. The offline
  harness itself still does not exercise a live title-screen claim; external
  evidence must not silently become its own coverage.
- **OPUS:** `12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md`
  §3/7/13/15 can consume actual observed binding/containment/import endpoints and
  correct564D0 to56490. Preserve the unobserved new-save/purchase roundtrip.
  `Reconstruction/Tests/Differential/diff_bazaar.py` describes its own offline run;
  attach external evidence separately instead of relabelling it live.
- **FABLE:** two-primitives §5a, `PROGRAM-STATE.md`'s historical title inference and
  `OPEN-QUESTIONS.md` BI-9 carry the same unsupported no-execution reasoning. Add
  a correction while preserving the historical observations and later static
  identity. Locate the original raw samples if retained. Review any universal
  load-clears wording in the battle-state/encoded-id pages against old-load
  endpoints, without claiming the earlier clearing routine did not execute.
- **FRONTIER:** the queue's "only observations missing / neither disputed"
  description is superseded by these results. No duplicate live capture for a
  coverage count. Any new title execution/timing question needs a named consumer,
  exact state/trigger and detection control, not just unchanged scratch values.

Run `reduce.py`, `repeat_transform.py`, then `check.py` using the existing analysis
venv. `validation.txt` records the bounded run. Five focused rejection controls
cover empty execution, missing execution detection, missing write detection,
empty live reduction and omission of the header coordinate shift. Historical
mutation campaigns are preserved; no broad campaign is needed for these scoped
evidence additions. Sources and dependencies are hash-pinned by the manifest.

Player version: the older save brought back its recorded bazaar flags and sold
loot totals. We have not yet demonstrated saving a new bazaar purchase. Separately,
a game calculation can run and write the same answer again; a motionless memory
value is not proof that the game skipped that calculation.
