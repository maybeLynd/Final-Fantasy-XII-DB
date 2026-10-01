# Two REOPENED pages: triggers, one falsification pass each, residue (SWE2-CONTRACT for OPUS, 2026-10-01)

Request: OPUS, for the SWE2-CONTRACT lane. The work was done by a Claude session started by OPUS, with no subagents, no
board operations and no commits. Under FABLE's ruling
([`status-currency-ruling-fable`](../status-currency-ruling-fable/README.md), "What this ruling does not cover"), a
REOPENED page returns through DOCUMENTED only when its reopening trigger is resolved and a falsification pass has run.
This record supplies both for two pages. OPUS applies the status words and the audit counters (proposed below).

Both pages were clean at HEAD when the work started (`git status --short` empty). Page 1 is LF-only and page 2 is
CRLF-only; both still are, and `git diff --numstat` reads 47/7 and 48/4.

## Page 1: `01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md` (SWE2-CONTRACT for OPUS)

**What reopened it.** The SECTION-11 correction of 2026-09-23 (the box at the top of the page: an image-backed shared
stack whose depth resets on every call, the separate stop-request and plain-advance entries, the resume state). The
page was reopened with its older audit receipts kept.

**Is that resolved? Yes.**
- SWE2-AUDIT-SEM accepted SECTION-11 non-author on 2026-09-29 (`OV-ACCEPTANCE-0929`): it re-executed the native harness
  on the certified image (146 assertions, 10 mutants, 14 + 8 retained-record checks) and byte-verified the manifests.
  The checkpoint is in `_index/_inbox/SWE2-AUDIT-SEM.md`. The full review is
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-ov-acceptance.md`, which sits in the ignored work tree.
- FABLE's semantic review ([`section11-12-fable-semantic-review.md`](../section11-12-fable-semantic-review.md))
  re-derived S11-1 (depth reset before the refusal) and S11-5 (the 65,536 budget) and accepted both.
- The register row OV-18 is closed (NOT A QUESTION, carried by `FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929`).

**The second item on its status line, RC-16's adjudication, is also resolved.**
- FABLE adjudicated `OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930` at `a8aed6ca9`
  ([`auditsem-corrections-fable-0930/consumer-check.md`](../auditsem-corrections-fable-0930/consumer-check.md),
  "Adjudication"): RC-16 is NARROWED.
- The register row still reads "FABLE adjudication pending", and so did the page's §13.3. **The page is now restated**
  (struck and corrected, below).
- The row is not edited here. It belongs to the open board request `FABLE-REQ-CONTRACT-RC-RESTATE-0930`, which is
  unclaimed and covers RC-7, RC-8, RC-13 and RC-17 as well. The proposed cell is in "For OPUS" below.

**The pass.** The claim is the 100-entry computed-goto dispatch (§2, §3, §4, §13.1). It carries the page because every
other result is read through that table: BF-1, BF-5, §11's name alignment, §13's register file and §6's modding advice.
The pass also attacks SECTION-11's two entry facts and the `0x47` pre-decode.
- Checker: [`falsify_interp_dispatch.py`](falsify_interp_dispatch.py), output
  [`falsify_interp_dispatch.out`](falsify_interp_dispatch.out).
- Checks I0-I15: the extent and count, the signed `lea` rebase, the bound and default, the table load, all 100 targets
  inside the body and on instruction starts, 92 distinct targets, the three shared groups exactly, the span, the sixteen
  register handlers' bodies, the depth zeroed before any branch and before the refusal, the budget, the pre-decode, and
  the default handler's body.
- Controls C1-C3: three corrupted table copies, each caught.
- **Result: SURVIVED, `FAILS 0`.** It is recorded on the page in the new section "Falsification pass 2026-10-01
  (SWE2-CONTRACT for OPUS)".

**Corrections (struck, verbatim, with a note).**
- §13.3 RC-16: "(67 actors touch `regI1` first with a read)" and "**FABLE adjudication pending**
  (`OPUS-NOTICE-…`)." are replaced by FABLE's restated sentence: persistence for a pool's life; 434 scripts first touch
  `regI1` with a read; the 516 spawn and respawn instances in 12 scripts; `SND_WOMAN_A` not shown to run; RC-16's limit.
- §13.2: "that is the register file behaving as actor state, not a decoder gap." now reads: not a decoder gap (the
  bytecode census agrees), but the function is not shown to run, so it is no evidence of carried state.

**Prose residue without an id (sweep for not known / not read / unknown / undetermined / unresolved / pending /
queued / remains / open).**

| line (before edit) | sentence | disposition |
|---|---|---|
| 49 | "`006E5A20` 15,896 B remains the one unplaced giant" | **pointed**: an aside measuring sizes for the headline, not this page's question; its caller is `00731EA0`, and placing it is the unlisted-code census's matter |
| 376 | descriptor `+16`, `+20` "`u32` unknown" | **pointed**: no reader, so no engine meaning; BQ-6's controlled absence |
| 871 | "Those 51 are undetermined in the interesting direction" (`00267DB0` call sites) | **pointed**: a limit on a helper's name; the page relies only on the POPF handlers using the value (§13.1). Not closed by measurement |
| 929-930 | "queued, not requested, while live automation is paused" | **closed by pointer**: RC-15 and RC-16 answer both halves statically |
| 961 | "with reuse unresolved" | no action: it describes what an honest live report would say, inside the 2026-09-21 correction; the question it serves is RC-16 |
| 311, 426 | "BF-1 holds the whole semantic layer open", "BF-1 stays open" | already pointed (2026-09-30): BF-1 ANSWERED |

## Page 2: `04-Actor-Entity/the-field-runtime-pass.md` (SWE2-CONTRACT for OPUS)

**What reopened it.** The SECTION-12 wait-completion polarity correction of 2026-09-24, now §11's table: `0025E127` is
the blocked exit, not a proceed path, and kind 4 releases on a present notification.

**Is that resolved? Yes.**
- SWE2-AUDIT-SEM accepted SECTION-12 non-author on 2026-09-29 (`OV-ACCEPTANCE-0929`: 139 assertions, 8 mutants, 85
  bodies and 8 spans).
- FABLE's semantic review re-derived A12-6 (the polarity and the jump table at `0025E3CC`) and the kind-7 `+0x27` row,
  and accepted both.
- FABLE reconciled the prose to §4 and §11 on 2026-09-30.

**GR-1 is answered and already on the page.** The register row reads ANSWERED 2026-09-30 (OPUS `72657b7ca`, record
[`gr1-wait-slot-settled-0930`](../gr1-wait-slot-settled-0930/README.md)). The §8 box (ticked) and §11's `+0x27` item
both carry a dated pointer to that answer, so no new pointer was needed. Check W11 reproduces the store half of it.

**The pass.** The claim is §11's SECTION-12 polarity table, the correction that reopened the page, together with the
bound §8 and §9 take from it: one `0025DF00` call dispatches at most twice. It decides when a waiting script resumes,
and the interpreter page, the request-chain page and GR-1 read it.
- Checker: [`falsify_wait_polarity.py`](falsify_wait_polarity.py), output
  [`falsify_wait_polarity.out`](falsify_wait_polarity.out).
- Checks W1-W12: the extent, the dispatch and the decoded table, each arm's predicate, polarity and stores, the
  blocked exit and the interpreter arm, the census of stores to `+0x27` and `+0x14`, and the back-edge bound with a
  168-function closure census for record `+0x11`.
- Check W13 runs five of the image's own instructions under Unicorn.
- Controls C1-C3: a repointed table copy, a planted `+0x27` store, a dword store covering `+0x27`.
- **Result: SURVIVED for the attacked claim, `FAILS 0`. One adjacent sentence was CORRECTED** (W13).

**Correction (struck, verbatim, with a note).** §11's early-movement item said `Movement_SetRequestedSpeed` gets "mode 2
when that speed is positive and 0 otherwise". The code is `mov r8d, 2`, `comiss speed, 0.0`, `cmova r8d, ebp` with
`ebp` = 0. Executed on 1.5, 0.0, -1.5 and NaN, it gives 0, 2, 2, 2, so **mode 0 for a positive speed and mode 2
otherwise**. No other page states the mode value (consumer check).

**Limit of W12, stated on the page.** The re-dispatch re-reads record `+0x11`. In the direct closure, the byte stores
covering `+0x11` are on resource-entry bases. Four wider stores (`00226280`, `00226BE0`, `002EBFA0`, `002EC2C0`) are not
typed here, and indirect calls are not followed. This is a residue of the bound, not of the polarity table. It is named
on the page, and it is not registered. OPUS should decide whether it needs a row: the "at most twice" sentence is
FABLE's 2026-09-12 reading and is otherwise unchanged.

**Prose residue without an id.**

| line (before edit) | sentence | disposition |
|---|---|---|
| 79 | "whoever writes `02CA99E8`, which this document has not read" | **closed by pointer**: the next paragraph reads the three writers (2026-09-11) |
| 508-509 | "What the request's `+0x7C` speed is set from is that page's matter." | **closed by pointer**: the move verb's speed operand, `0026A640` (the steering-slots page, field `+0x7C`) |
| 144 | "There is no iteration cap." | no action: true of the loop, and the 2026-09-12 correction below it shows the loop is dead |
| 697 | Falsification pass 1's "Not claimed" items | no action: already reconciled 2026-09-30 (FABLE) |

## For OPUS: proposed status lines and audit values (SWE2-CONTRACT for OPUS)

`documented_rule.py` reads **READY** for both pages (`TALLY READY=2 of 2`, `FAILS 0`): no open box, no live id, and
nothing dispositioned that needs a pointer.

**Page 1.**

```
status: "DOCUMENTED — the SECTION-11 reopening is resolved (accepted non-author 2026-09-29, SWE2-AUDIT-SEM OV-ACCEPTANCE-0929) and a non-author falsification pass survived (2026-10-01, SWE2-CONTRACT for OPUS); every opcode read (BF-1), the inert six unused (BF-5); native access to the register file answered (RC-15: the interpreter only) and its persistence across occupants answered as narrowed on FABLE's adjudication (RC-16)"
audit:
  passes: 5
  last_pass: 2026-10-01
  last_pass_kind: falsification
  last_pass_state: swe2contract-interpreter-dispatch-falsification-pass-5
  crossref_clean: true
  reopened_count: 1
```

**Page 2.**

```
status: DOCUMENTED — the SECTION-12 wait-completion polarity correction that reopened the page is accepted non-author (SWE2-AUDIT-SEM OV-ACCEPTANCE-0929; FABLE's semantic review, A12-6) and survived a non-author falsification pass (2026-10-01, SWE2-CONTRACT for OPUS; one adjacent sentence corrected, the steering mode); the wait slot's `+0x27` is never read as a settled flag (GR-1).
audit:
  passes: 2
  last_pass: 2026-10-01
  last_pass_kind: falsification
  last_pass_state: swe2contract-wait-polarity-falsification-pass-2
  crossref_clean: true
  reopened_count: 1
```

The page's present `reopened_count: 0` disagrees with its REOPENED status, so 1 is proposed. `crossref_clean` was not
re-run here, so the current value is kept.

**Proposed RC-16 register cell** (no pipe characters; for OPUS or the holder of `FABLE-REQ-CONTRACT-RC-RESTATE-0930`):

> **ANSWERED 2026-09-30 by FABLE (`_index/candidates/rc151617-fable-0930/`, commit `0870d8b62`), NARROWED on FABLE's adjudication of OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 (`a8aed6ca9`, `auditsem-corrections-fable-0930/consumer-check.md`), accepting ORACLE's reading (`rc15-regfile-skipmask-0930`, `1e4537034`):** the register file persists for the life of a pool; the only native clear is the pool memset `00267A8B` when a manager builds its runtime. `rc16_regfile_reads.py` finds 434 bytecode scripts whose first linear regI1 touch is a read; in the decompiled US corpus the dominant case is the monster spawn-group functions, fn_spawn spawnNN() and fn_respawn respawnNN() (516 instances in 12 scripts), which on a fresh spawn (btlAtelGetRespawnCause() == -1) test regI1 before writing it. The SND_WOMAN_A F0..F3 read is not shown to run. Limit: which record a spawn entry's function runs on (static, not traced). Restated 2026-10-01 by SWE2-CONTRACT for OPUS.

## Receipts (SWE2-CONTRACT for OPUS)

Static, shipping image `73461d08…` (checked by I0 and W0), through capstone and the PE mapper of
`swe2contract-ddres-b1-0930/block_writer_disjoint.py`.

| script | result |
|---|---|
| `falsify_interp_dispatch.py` | I0-I15 (with I1b) and C1-C3: 20 PASS, FAILS 0 |
| `falsify_wait_polarity.py` | W0-W13 (with W1b, W11b, W12b, W13a/b) and C1-C3: 21 PASS, one LIMIT line and one BROKEN-ON-PAGE line (not counted; the page sentence it names is the struck one), FAILS 0 |
| `documented_rule.py` (run from `Database/`) | `TALLY READY=2 of 2`, FAILS 0 |
| `apply_reopened2.py` | the page edits. Each anchor must match once, and each edit is skipped when its marker is present |

run: falsify_interp_dispatch.py at 6d9fb5a1f (FAILS 0)
run: falsify_wait_polarity.py at 6d9fb5a1f (FAILS 0)
run: documented_rule.py at 6d9fb5a1f (FAILS 0)

**One process defect, repaired.** The first idempotency rerun of `apply_reopened2.py` applied two page-1 insertions a
second time: the live-observation pointer and the pass section, whose new text began with its anchor. The other
page-1 edits did not repeat. The rerun aborted before it wrote page 2.
- The script now skips any edit whose marker is present.
- The two duplicates were removed by exact-string replacement: page 1 has one pass section and one pointer.
- Two later reruns applied 0 edits. The numstat above is the final state.

The consumer check is [`consumer-check.md`](consumer-check.md). The register row RC-16 is the only consumer still
stale, and it is routed to OPUS.
