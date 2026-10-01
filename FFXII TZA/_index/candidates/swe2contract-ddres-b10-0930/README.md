# DD residue closure, batch 10: six pages, from the widget protocol to the unit-shape toolbox (SWE2-CONTRACT for OPUS)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, batch 10. A Claude session ran the batch in the SWE2-CONTRACT
lane, started by OPUS. It used no subagents, no board tasks and no commits.

Each of the six pages passes the mechanical documented rule. Each status line still named content residue with no
register id, or was a bare `PARTIAL`. All six were clean at HEAD, LF-only and unclaimed when the batch started:

1. `16-UI/Widget-Object-Model/the-widget-message-protocol.md`, whose status read "24 handlers UNPARSED and several
   ids UNRESOLVED in the census".
2. `17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md`, whose status read "no .efx/.efb
   file was opened and the EFB buffer lifetime is not read; … binders 00333C80 and 004FF270 unread".
3. `17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md`, a bare `PARTIAL`.
4. `17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md`, a bare `PARTIAL`.
5. `17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md`, a bare `PARTIAL`.
6. `06-Movement-And-Navigation/the-unit-shape-distance-primitives.md`, whose status read "home page filed so the
   executed contract has somewhere to land; the full adoption is in flight".

No status word was moved; OPUS re-statuses after its owner read. Where a status line named residue, its clause now
says what is answered, and the old text is kept after "was —". The three bare `PARTIAL` lines are unchanged. Every
correction keeps the removed text under a strike, with a *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10)* note.
The work is static only:
- the certified image (`73461d08…`), through `retool.py`;
- the game extract `D:/FFXII_TZA_extract`: all 3,288 `.efx`, 410 `.efb` and 1,066 `.cm` files, plus the 531
  embedded EFX streams listed by the effect folder's `type_census.py`;
- the installed `FFXII_TZA.vbf`, for control X1, which re-decodes sample extract files from the archive byte for
  byte.

## What changed, page by page (SWE2-CONTRACT for OPUS)

**1. the-widget-message-protocol.md**

| residue | disposition |
|---|---|
| status: 24 handlers UNPARSED | **answered (W1–W3).** The table now holds 264 exact rows, 0 upper-bound rows and 3 unparsed rows. All three are read: `005C5230` is the no-op, `0017CDE0` jumps to it, and `002985C0` jumps to `003EE420`, which answers 1, 2 and 4 |
| status: ids UNRESOLVED | **answered.** Every id of the 56-id recount was already named or dispositioned in §10 (`DL-1`, 2026-09-25). The status line had not caught up |
| §7: three stale "does not claim" bullets (ids 8–289, the 11 upper bounds, the 24 unparsed) | **corrected** (struck) |
| §10: whether `002D2DB0` / `005691E0` return non-zero for 26 | **answered (W4).** `005691E0` returns 0. `002D2DB0` returns its `+0xC8` delegate's answer, or 0 without one |
| §3: the 232 / 11 / 24 table | dated note added, giving the current counts |

**2. efx-and-efb-effect-containers.md** (new §2b)

| residue | disposition |
|---|---|
| status: no file opened | **answered (E1–E4).** In every `.efx`, `+0x08` is `1.0` and `+0x0C` is the file size. The walk ends exactly there, and every chunk has `+4 = 0x100`. In every `.efb`, `+0x0C` is 0 and the blob sizes equal the EFX `+0x0C` |
| status: EFB buffer lifetime | **answered (E10–E11).** The buffer is one fixed block of `0x43D170` bytes (the largest `.efb`) from `00377DC0`. The mode-1 completion parses it and the mode-0 completion hands it to a stub. Only the map teardown `00378230` frees it, and only after `0026FF50` has disposed of every type-2 context. What mode 0 is for is proposed row P7 |
| status: binders `00333C80`, `004FF270` unread | **answered (E5–E9).** `004FF270` relocates offsets for four subtypes of fixed size `0x160`–`0x300`. In every `0x700` chunk the `+8` dword equals that size, and all 212,896 relocated offsets land inside their chunk. `00333C80` is the `EFX0009` / `EFX0008` → `EFX0010` rewrite plus the lane-count nibble |
| §2: the handlers' own retention | **answered (E12).** The handlers keep their records in the context tables `+0x38` and `+0x840`, which `0024F410` releases |
| §7: `+0x08..+0x0F` engine-wide inert | **corrected.** Four of the six loader callers pass `+0x0C` as the size |
| §7: callers not read; EFB body past `0026FC4E`; the handlers "neither read"; the version split | **corrected** (struck; each is answered elsewhere on the page or here) |

**3. fte-fct-texture-colour-tables.md**

| residue | disposition |
|---|---|
| `@FTE` `+0x10` unread | **answered (T1, T3).** It is 0 in all 2,127 records. The pointer-forming bodies are exactly `005044D0`, `00504D30` and `0053AB50`. `0053AB50` reads the record at `+0` and `+0x1C`, and `00504520` copies every field but `+0x10` |
| cache-key collision semantics | **answered (T4–T5).** A key that is already live shares the slot (`005210F0` raises its count). The slot carries the last binder's descriptor. Of 87 shared keys, 80 have identical pixels, 85 an identical descriptor, and 15 an identical descriptor and offset. The seven pixel-differing keys are variant sets and one weapon pair. What a co-drawn second model then shows is **runtime-only** |
| `@FCT` `+0x08` use | **answered (T2).** None of the three pointer-forming bodies reads it |
| page 1's setter value | **answered (T6–T7).** None exists. The 23 `00428CD0` sites pass 0, 2 or 3, and the one variable site passes `0xD0` definition `+0x146`, which is 2 or 3 in every shipped definition with the gate set (1,437 definitions, matching the type census) |
| how `@FCT` sub-indices are chosen (front matter) | **answered (T8).** `003E7210` takes them from `+0x3D3` / `+0x3F8`, and `0xFFFF` binds every sub. Only command `0x16`'s handler writes these fields, and every shipped `0x16` passes `0xFFFF` |
| "UQ-218 stays PARTIAL" bullet | **corrected.** UQ-218 is ANSWERED, and those entries have their own pages |

**4. fef-and-motion-entries.md**

| residue | disposition |
|---|---|
| op `0x12` "beyond name/callees" | **answered (M1).** The handler sets bit 7 of the look record's `+0x1C` through `003E29F0`'s kind-4 arm. The bit's reader is proposed row P2 |
| the `+0x44` bullet: "`02B64380` row meaning stays open" | **corrected** (stale; resolved by the first bullet and pass 18) |
| falsification pass: `001D6EC0` not re-read | annotated as answered by pass 18 |
| falsification pass: reachability not observed | **runtime-only.** Every `@FEF` model's load completion reaches the arm, and which models a session loads is content |
| the embedded payload's remainder (copied pointer, or a `003EDAD0` use) | proposed row P1 |
| the target-bearing arm "against the target" | **runtime-only** (a visual question) |

**5. ftr-node-table.md**

| residue | disposition |
|---|---|
| bits 31 / 22: "whether shipped records set them" | **answered (R2).** 11,243 and 23,694 records set them |
| bit 21's "~16" | **corrected (R1).** Exactly sixteen `u16` become sixteen dwords |
| front matter: flag vocabulary not established | **narrowed (R1–R2).** The bind path tests bits 8, 21–28, 30 and 31. Bit 29 carries a `u16` that nothing reads. Bits 0–2 and 9–19 carry no stream data, and nothing tests them. Bits 3–7 and 20 are never set. The length rule holds for all 27,561 records |
| §4: runtime consumers of the `0x290` records | **located (R3)**: `0041C260`, `00373860` → `00372610`, plus the fef page's readers. Their field use, and the `+0x94` tail readers, are proposed row P6 |
| §4: bone semantics, aux values, FCP section-2 | proposed rows P3, P4 and P5 |

**6. the-unit-shape-distance-primitives.md**

| residue | disposition |
|---|---|
| status: adoption "in flight" | **answered.** The adoption landed (SWE2-DATA, 2026-09-30) and the request closed as `CON-129`. The status line had not caught up |
| §3: the authored-or-per-query question | **corrected** (struck). The SD-182 box below it answers the question |
| §3: the constants "not reproduced here" | **answered (S1–S2).** The face table is six unit planes with `w = 1` and a margin of `1.001`. The sign mask is four `0x80000000` dwords |
| missing content: the planted siblings and D2020 | **supplied (S3).** Sizes, plant sites and callees. One plant of `0022DE60` is new (`0023126A`). All of this is call level, not executed |

## The findings, in player terms (SWE2-CONTRACT for OPUS)

- **The game converts older effect files as they load,** and fixes up each effect's internal offsets once. A modded
  effect that keeps the `0x700` chunk's `+8` equal to its fixed size, and its offsets inside the chunk, loads like a
  shipped one.
- **A map's weather effects stay in memory until the map is unloaded,** and they are released only after every effect
  built from them has been torn down.
- **Page 1 of every character palette ships but is never shown.** Stone and Petrify use page 3. HP Critical, Doom and
  two effect definitions use page 2.
- **Every shipped bone record's size follows from its flag word,** and bit 29 adds a value the game never reads.
- **Every menu object's answer to every message is now read.** No list lifts its clipping by its own answer to
  message 26.

## Proposed register rows, id-less, proposed for SWE2-DATA (SWE2-CONTRACT for OPUS)

| # | page | question |
|---|---|---|
| P1 | fef-and-motion-entries.md | Does any shipped code read the embedded `EFX0010` payload at `@FEF + 0x30` through a pointer copied in memory, or hand it to `003EDAD0`? The six direct callers of `003EDAD0` and the image-wide edge sweep exclude every other route |
| P2 | fef-and-motion-entries.md | Which code reads bit 7 of the look record's byte `+0x1C`, written by op `0x12` at `003E2A4E`–`003E2A56`, and what does it gate? |
| P3 | ftr-node-table.md | Which `@FTR` bones carry attachments or effect markers rather than pure transforms? |
| P4 | ftr-node-table.md | What the aux-pool values mean for each reading bit (bits 23–25 to runtime `+0x30` / `+0x34` / `+0x38`, bits 26–28 to `0046D560`, bit 21's sixteen dwords), and what bit 29's unread `u16` index names |
| P5 | ftr-node-table.md / fcp-character-parameter-block.md | The FCP section-2 blob's field semantics after the `003E1C50` fixups |
| P6 | ftr-node-table.md | Which fields of the `0x290` runtime bone record each located consumer reads (`0041C260`; `00373860` with `00372610`; the `@FMW` apply path; the skinning palette), and which code reads the render record's `+0x94` tail pointer |
| P7 | efx-and-efb-effect-containers.md | What the mode-0 `.efb` request is for (`003789A0` hands the block to the stub `0053DD10`), and whether a mode-0 and a mode-1 request can both be pending for one map (both publish at `02ADD088`) |

## Runtime-only (SWE2-CONTRACT for OPUS)

- **`@FTE` shared keys:** whether two models that share a texture key are ever drawn while both are bound, and what
  the second one shows. This depends on the scene's models and the upload order.
- **`@FEF` reachability:** which of the 144 `@FEF` models a session loads.
- **The target-bearing locomotion arm:** what `run_r_*` looks like against the target. This is a visual question.
- **The `0x700` relocation:** whether `[01F83530]`'s low 32 bits are zero at run time, so that the relocated value
  names `record + bias + stored`. The global is a zero-filled `.data` slot set at run time, and the image holds only
  its two reads.

## Receipts (SWE2-CONTRACT for OPUS)

| script | result |
|---|---|
| `b10_checks.py` (`b10_checks.out`) | W1–W4, E1–E12, T1–T8, M1, R1–R3, S1–S3, X1: 245 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | READY for all six (`TALLY READY=6 of 6`), FAILS 0 |

Controls and blind spots:
- **The W3 chain decoder** reproduces the table's ids for `002D2DB0` and `0027AD70` before it is trusted on
  `003EE420`.
- **The corpus walks** are anchored three ways. E1 reproduces §6b's magic split. T5 reproduces the page's 87 / 80.
  T7's `0xD0` count equals the published type census (1,437). Control X1 equals the extract to the archive for
  `h0026.efx`, `alc0201.efb` and `m1132.cm`.
- **T1 filters on its address range.** It is a census of the render-record code band `00500000`–`0053FFFF` for
  bodies that read `+0x218` / `+0x21C` beside `+0x1F8`. A body outside the band, or one that receives the entry
  pointer already formed, would escape. The two pointer hand-offs actually seen (to `00504520`, and none from the
  `@FCT` record) are followed.
- **The T8 store census** is image-wide and finds the `+0xBA` setter as its control. It sees only immediate-base
  stores (`mov` / `or` / `and` / … to `[reg + disp]`).
- **E3 is a direct-call and rip-reference census,** and its control finds `003788F0`'s plant. A pointer stored to
  memory and called later is outside it.
- **S3 is call level.** None of the sibling bodies was executed or read whole.

## Consumer check (EVIDENCE-POLICY 4a/4b/4c) (SWE2-CONTRACT for OPUS)

See [`consumer-check.md`](consumer-check.md). Two consumers disagree with this batch, and both are routed, not
edited:
- `06-Movement-And-Navigation/heading-speed-to-position-delta.md` calls `00381450` "the heading delta's length arm".
  This page and its falsification pass (U1, U2) read it as the box primitive over `00D11200`.
- `03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md` gives `00378230` as 114 B, but the v4 extent is 619 B. The
  page's own claims about it (teardown, `003697F0` calls) agree.

The handler table `widget-message-handlers.tsv` still calls `002985C0` "a genuine open edge" in its note. The TSV
is left to its owner, and the page now answers that edge (W3).

## Not touched (SWE2-CONTRACT for OPUS)

- **The front-matter `audit.note` blocks** of the fte-fct and ftr pages still list as "not read" items this batch
  answers or narrows. They are left for the owner's re-status, to avoid editing multi-line YAML.
- **Other pages modified in the shared tree during the batch** (peers' uncommitted work) were not opened for
  editing. None of the six pages was modified by anyone else.
