# HM-1: how hc1006_03 gets a parent (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**Question.** HM-1 was left with "what attaches hc1006_03's actor in those four maps". The candidates were the attach
setters' untraced callers (`002EDAA0` via `002E3110`, `00426C90`, `00427320`, `0042DC10`, `0042F4C0`).

**Discriminator.** Which caller both parents an element and sets the binding state `003703A0` needs (2)? Does its
model choice reach hc1006_03?

**Negative results, which narrowed the question:**
- `00426C90`, `00427320`, `0042DC10` and `0042F4C0` all pass the fixed code `0x10A`, the mount pattern.
- `0041EDE0` / `0041F010` → `004211B0` is the equipment attach (weapon / shield slots `+0x2C8` / `+0x2CA`).
- None of these sets `+0x6C8`.

**Result** (`hm1_body_bind.py`, B1–B8).

*B1, the data.* `highmodelreplace.bin` record `c:3` has key (-1,-1) and one pair: `C:22` at threshold 0.
- `c:3` is c1006; `C:22` is `hc1006_03` (kind 15 entry 22).
- So `0037CB90(c1006, b, c)` returns hc1006_03 for every b and c, and for every non-negative story progress.

*B2, the poll.* The bind poll is `003409F0`. It serves `bindp` 0x0C, and the `bindp2` family through `00342330 jmp`.
- It binds the requested model to the unit's own record, then asks `0037CB90` (`00340A7F`).
- With no replacement, the request stays at mode 1.
- With a replacement, the poll loads it: mode 2, then mode 3 (`00340B03`).

*B3, the result.* The result handler is `00342640`, which the `bindp2` family reaches through `00343760 jmp`. At mode 3 it
calls `002E3110` with k = 4 (`003426B5`). `bindhoff` (`003460F0`) does the same after its own `0037CB90` call.

*B4, the attach.* With k = 4, `002E3110` does three things:
- It binds the model into the unit's `+0x90` body element.
- It passes `(own record, 0x7FFF, body record)` to `002EDAA0`. That function swaps them into `0042F310(child = body,
  parent = own, code)`, which stores `+0x3CE` / `+0x3CC`.
- It sets binding state 1 on the own record and 2 on the body (`002E3466`; `002E3484` → `002E34D2`).

*B5, the state machine.* `002EDF90` is `+0x6C8`'s only writer besides the reset, and it is called only from `002E3110`.
- State 0 stores the request.
- Release: 1 → 3 and 2 → 4.
- Re-bind: 3 → 1 and 4 → 2.
- The store row's "1 and 2 are the two states" missed the four literal stores.

*B6, the dirty pass.* `004215A0` turns code `0x7FFF` into `004219C0(parent, -1, child)`, which reaches `0046E640`, the
element's `+0x08` / `+0x0C` writers.

*B7, the pose path.* `003703A0` maps only when the record's state is 2 (`00370634`) and `+0xB0 != -1`. It reaches the
second skeleton through the element's `+0x0C`.

*B8, the reset.* The reset value is 0.

**So:** hc1006_03 is c1006's high-detail replacement body. It becomes a child of the bound c1006 model's own record, and
its 39 SkeletonMapping values map its joints onto that model's skeleton. "Pose mode 2" means *the replacement body of a
bound model*. All four manifests that load `C:22` also load `c:3`.

**Supporting census.** `hm1-parent-writer/c22_bind.py` lists every bind-family call in the four maps: dgl_g0102 66,
gol_a0200 25, hne_b0102 88, rsn_z0200 92. Party scripts there call `bindp2` / `bindp2_d4`, `bindh` and `bindhoff`.

**The requests that name c1006 (BIND REQUESTS NAMED 2026-09-27, B9 + `c22_bind.py`).** In each of the four maps exactly one script binds c:3, with a bindp-family verb, and the same script also calls bindh on C:22: dgl_g0102 bindp2_d4 (script 'フラン'), gol_a0200 bindp2 ('Fran'), hne_b0102 bindp2 ('フラン'), rsn_z0200 bindp2 ('FRAN') - script names are the files' own labels. The argument route is read, not assumed: PUSHI reads the int constant pool, and the pool value 0x3000000 + k goes through 002E9A60 -> 00263F80, which indexes EBP section 12 (the manifest) by k (0033F378, 00263F87, 00263F97). So in shipped scenes c1006 is bound through the replacement poll, and hc1006_03 arrives as its mapped body; bindh C:22 binds the same file through k = 2, which requests state 0 and so does not map. 

**Still open:**
- The run-time order of the `bindp2` / `bindh` calls.
- What is drawn. *LIP FLAP 2026-09-27:* the +0x304 bit 6 that the k = 4 bind sets on the unit's own record (002E31DB) is not a hide flag but the LIP FLAP - setkutipakustatus's bit (002E8570), mirrored into +0x40B bit 5 by 00429C40, which switches rig controller 9 on through 0042DD90 for the record and the records linked under it, the replacement body included; k = 4 stores a timer of 0, which the countdown 0042EE90 never counts, so the mouth stays on until k = 2 clears it (LIP FLAP 2026-09-27, _index/candidates/hm1-body-bind/hm1_lipflap.py L1-L5). So nothing found hides the base model.

**Run receipt:** `hm1_body_bind.py`: PASS B1–B8; all 10 mutants rejected; FAILS 0 (2026-09-27, before publish of 7703e21cf). Part 2: PASS B1–B9, 11 mutants rejected, FAILS 0; `hm1-parent-writer/c22_bind.py` PASS in 4 of 4 maps, FAILS 0 (2026-09-27).

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` CharacterRenderRecord `+0x6C8` | corrected (five-state machine, reset 0; old text kept in the evidence cell) | revised-here |
| `_types/fields.tsv` CharacterRenderRecord `+0x3CC` | extended (code `0x7FFF` = the body bind) | revised-here |
| `_index/OPEN-QUESTIONS.md` HM-1 | narrowing prepended; row stays PARTIAL | revised-here |
| `17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md` "Not claimed: which actor…" bullet | struck and narrowed in place; a new "Not claimed" | revised-here |
| same page §3 (`002EDF90` as a state machine) | already reads it this way | agrees |
| `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md` (k-enum, `+0x90` = body model) | agrees; the k = 4 attach and binding state are this record's addition | agrees |
