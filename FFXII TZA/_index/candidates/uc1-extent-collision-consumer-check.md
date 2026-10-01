# Affected-consumer check: listed `007EE7F0` is a false entry inside `007EE7C0` (OPUS, 2026-09-27)

**State: PENDING REVIEW → PENDING PROPAGATION.** This record is an owner adjudication, not an
accepted correction. Independent review is routed to SWE2-AUDIT-SPEC. Until it returns:
- no function-list row, generated table or denominator moves;
- the UC-1 row stays BLOCKED on this item.

**The ruling** (evidence: `_experiments/evidence/uc1-extent-collision-opus/`):
- **The false entry.** The listed `FUN_007ee7f0` (9 B) begins at byte 2 of the reachable 7-B
  store `007EE7EF 41 89 89 38 01 00 00`.
- **No producer.** Nothing in the image produces its address: no branch, call, RIP-relative
  operand, DIR64, absolute qword, image-relative dword, `.pdata` begin or export.
- **The real body.** It is the unlisted leaf `007EE7C0`, **57 B, ending at `007EE7F9`**.
- **One defect, not two.** The candidate's 48 B was the gap up to the false entry.

**The 007C2A29 extent convention:**
- The predecessor `007C23C0` is extended, and no body is added.
- Its **instruction extent** is `[007C23C0, 007C2A2F)`.
- Its **native (unwind) extent** is `[007C23C0, 007C2A58)`. The `.pdata` chain ends there.
- The last 41 B of the native extent are a 1-B `nop` pad plus the 40-B jump table that
  `007C27F2` reads. They are owned data, not instructions.

**Regression:** `_experiments/evidence/uc1-extent-collision-opus/check.py`. It is an executed
control, not a word match. It rejects three interpretations:
- **W1**, the 48-B extent;
- **W2**, `007EE7F0` as an independent or alternate entry;
- **W3**, all 47 B at `007C2A29` counted as instructions.

It also carries live controls: the `007EC4F1` LEA, the `007EE730` and `007EE800` `.pdata`
begins, and a planted-call mutant.

| Consumer | State |
|---|---|
| `Tools/work/graph/functions.tsv` row `007EE7F0` (GZF-derived listed population, 34,270) | **routed; not applied.** Retiring a listed row is a GZF mutation under the serialized fence, applied only after acceptance. Until then, readers use the errata row below. |
| `_index/FUNCTION-EXTENT-ERRATA.tsv` | **pending.** After acceptance, one row goes in: `007EE7F0`, verdict *false entry (inside a reachable instruction of an unlisted body)*, `covered_by 007EE7C0`. `unlisted_admissions.py` must then treat the row as absent when it measures gaps. The mechanism is the one its `merge` rows already use. |
| `99-Unresolved-Residual/Unlisted-Code/unlisted-body-admissions.tsv` row `007EE7C0` (48, `decodes_to_end=no`) | **pending regeneration.** It becomes 57 and decodes to its end. |
| same directory: `unlisted-code-blocks.tsv`, `unlisted-entry-points.tsv`, `referenced-unlisted-blocks.tsv` (each `007EE7C0 48`) | **pending regeneration** (57). |
| `_index/candidates/uc1-band-1-64-fable-2026-09-25.tsv` row `007EE7C0` (48, `admit`) | **routed to FABLE** (`ASTRA-RETURN-FABLE-UC1-QUALIFIED-BAND`). The admit stands at 57 B, and 57 is still inside the 1–64 B band. |
| `18-Audio/members/sead-library-span.tsv` member `007EE7F0` | **routed to the Audio owner.** The member is `007EE7C0`. The span generator `select_audio_libraries.py` takes listed entries, so it follows the function list. |
| GZF comment on `FUN_007ee7f0` (1,583 chars, `GFZ.V120.PrimaryOwner.Audio`) | **routed with the GZF row;** not read here. |
| `_index/ADDRESS-INDEX.md` `007EE7F0` | generated. It follows the span TSV. |
| `99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md` line 725 (`007EE7F0` among the "phantoms", correctly emitting no row) | **agrees.** |
| `_index/_inbox/SWE2-AUDIT-SPEC.md` shadow audit, 2026-09-14 ("lands mid-instruction … no callers, no .pdata, no pointer refs") | **agrees.** It is an independent prior observation. This package widens the producer classes and adds controls. |
| `_experiments/evidence/uc1-band-ruling/README.md` (ASTRA): the 48-B truncation, and the 57-B extent ending `007EE7F9` | **agrees.** Its open alternative, "a deliberate alternate entry", is rejected here by D1+D2. |
| `_index/OPEN-QUESTIONS.md` UC-1 row | **revised here.** A dated annotation is added, and the row stays BLOCKED pending review. |
| Population figures: listed 34,270; floor 34,409 = 34,270 + 139 | **pending, not restated.** `007EE7C0` is not among the 139. The false entry sits inside the *listed* term, so on acceptance the listed term is 34,269, and the floor is 34,408 with a recorded series break. The historical figures keep their populations. |
| `99-Unresolved-Residual/Unlisted-Code/unlisted-blocks-reached-from-the-listed-body.tsv` row `007C2A29` and `the-bodies-the-list-cuts-short.md` | **pending.** The tail extension carries the two extents above. Its instruction census uses the instruction extent. |
