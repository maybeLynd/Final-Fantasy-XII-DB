# Wave A of SWE2-AUDIT-SPEC's narrowings on OPUS-lane records (SWE2-CONTRACT for OPUS, 2026-10-01)

Request: `SWE2AUDITSPEC-REQ-OPUS-0930-WAVE-NARROWINGS` (SWE2-AUDIT-SPEC to OPUS). It asks the owner to apply the
correction wording of each ACCEPT-WITH-NARROWING review, or to record why not. FABLE is inactive, and the user
authorized the OPUS lanes to do this. A Claude session ran wave A in the SWE2-CONTRACT lane, started by OPUS, with no
subagents and no commits (OPUS publishes). SWE2-STRUCT runs wave B (dd-mixed .. dd-02-b2) at the same time; none of
its reviews is touched here. Board task `SWE2CONTRACT-AWN-WAVE-A-1001`.

**Method.** For each review, the correction wording was read, then the reviewed record and every page that cites the
record were searched for the text it replaces. None of the 15 had been applied before this wave: no target file had
changed since its reviewed commit, and no page or record outside the reviews cited them. The replaced text is kept
struck (`~~...~~`). Each edit carries a dated note, "(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's
review link, item N)". Every target was clean in `git status` immediately before the edit. The edits are line-exact
and keep each file's line endings. They were made by one idempotent script, `Database/Tools/work/SWE2-CONTRACT/awn_a_edit.py`
(37 edits; a second run applies 0). No status line and no register cell was edited.

**Checker.** `awn_a_checks.py` (output `awn_a_checks.out`, 95 PASS, `FAILS 0`):
- A: each applied wording is present on its target, the replaced original is struck, the target has exactly one
  unstruck copy fewer than at HEAD, and the dated note is beside it.
- X: each replaced original was present at HEAD and the new wording absent, so the A checks can fail.
- K: the two checker texts.
- T: no edited table row changed its column count.
- L: every review link in the notes resolves.
- B1: the blocked `_types` cell is untouched.

## Outcome per review (SWE2-CONTRACT for OPUS)

Counts: 11 applied in full, 2 applied with one part blocked or routed, 2 declined with a reason, 0 already applied.

| review | outcome | files touched | notes / proposed text |
|---|---|---|---|
| [links-scope](../auditspec-review-links-scope-0930/REVIEW.md) | declined (routed to OPUS) | none | The three items are code repairs to the shared gate `check_links.py` and its tests (CommonMark code-span pairing with two new tests; judge or rule out authored files in package subdirectories; refuse a decoded `%2F` / `%5C` separator). A wording pass cannot apply them, and the gate needs its own claim and a test run. Proposed: an OPUS tool package on `check_links.py` + `test_check_links.py` with the review's tests B1 and A1 as the regressions. |
| [sd1](../auditspec-review-sd1-0930/REVIEW.md) | applied | `sd1-force-fight-enemy-consumers-0930/README.md` | Items 1 and 2. The checker docstring (`sd1_consumers.py`, "has two readers") is not re-issued. The force-fight page's "only two readers" (§7, the `FLEEING`-label box) is routed in the consumer check. |
| [pass6-opus-rows](../auditspec-review-pass6-opus-rows-0930/REVIEW.md) | applied, re-sign routed | `text-gap-append-0930/README.md` | L21 is reworded as quoted. As the review predicted, this lapses disposition row 76 of `false-positive-dispositions.tsv` (evidence `940533025da6baf4`, now `dd112027c34e0da2`; `check_banned_evidence.py` lists it under LAPSED). SWE2-AUDIT-SPEC must re-sign the page. `textgap_rule13.py`'s reasons for `00121E11` / `0036F22E` were not changed: the review gives no exact text for them, the script only fills empty cells, and the reasons live in `text-gap-citations-250.tsv`. Proposed cells: `00121E11` "the second byte of `jmp $` (EB FE) at 00121E10, after the `ret` at 00121E0E, inside the body 00121DB0 the list cuts short; code, not data"; `0036F22E` "`mov eax, edi` in the epilogue of the body 0036F0F0 lists, ending `ret` at 0036F23A; code, not data". |
| [extent-v4](../auditspec-review-extent-v4-0930/REVIEW.md) | declined (routed) | none | (1) The B11 attribution is in commit `d20226c17`'s message, and no record README exists for that commit, so there is no record text to amend. Proposed for the next record or commit that cites B11, and for `test_build_views.py`'s B11 docstring: the review's item 1 sentence as quoted. (2) is a string in `program_coverage.py` and (3) is a required code repair of `field_disp_scan.py` (skip table-indexed tail bytes, or decode past the listed end only from branch targets; then `consumer_sensitivity.py fds` must lose the `0023B6D3` site and keep the control). Both are OPUS tool packages. (4) is routed to the FRONTIER / UC-1 owners, as the review directs. |
| [gr1](../auditspec-review-gr1-0930/REVIEW.md) | applied | `gr1-wait-slot-settled-0930/README.md` | Items 1-3. Proposed GR-1 register cell for OPUS (its Limits sentence is now narrower than the record), replacing "Limits: begin-before-poll is the lifecycle contract's order, and same-handler writes are ordered by address, not by path.": "Limits: every handler read is preceded by the same command's own write, on every path for 24 of the 38 command-reads and through a guard the begin always sets for the other 14; the phase byte `+0x15` is written only by the interpreter, the slot reset `0025D460`, `002621D0` and the VMResult writers, so a command starts at phase 0 unless an opcode is abandoned mid-execution, which is not traced." |
| [gr7](../auditspec-review-gr7-0930/REVIEW.md) | applied | `gr7-kind10-reader-0930/README.md` | Items 1-3. The review did not re-read the release clear, so nothing is said about it. |
| [gr45](../auditspec-review-gr45-0930/REVIEW.md) | applied | `gr4-gr5-action-row-readers-0930/README.md` | Items 1-4. The checker's S0 message is not re-issued (the review asks for it only "if it is re-issued"). |
| [gr13-15](../auditspec-review-gr13-15-0930/REVIEW.md) | applied | `gr13-15-shop-list-widget-0930/README.md`, `gr13_15_shop_list_check.py`, `gr13_15_shop_list_check.out` | GR-14's last bullet reworded. The README's B6 table row never carried the replaced sentence. The checker's B6 text now reads as the review asks. The checker was re-run before and after the edit (31 s each): the only change in the output is that line, and it still ends `FAILS 0`. |
| [gr17](../auditspec-review-gr17-0930/REVIEW.md) | applied | `gr17-reward-table-lifetime-0930/README.md` | The 382 / 383 count, plus the optional jcc sentence. |
| [dd-crt](../auditspec-review-dd-crt-0930/REVIEW.md) | applied in the record; `_types` cell blocked | `opus-dd-crt-0930/README.md` | A2 reworded, with the optional `0071E3A2 call 0x1a4c90` pin. `_types/types.tsv` is held by SWE2-STRUCT's `SWE2STRUCT-AWN-WAVE-B-1001` (a file claim), so the `MsvcTreeNodeHeader` ctor cell was not edited. Proposed cell text: in "0071E340 (for the 0x60 node) does the same and constructs two empty MSVC strings at +0x20 and +0x40 (capacity 15, size 0)", strike the clause from "constructs" to the closing parenthesis and write "initialises two MSVC strings and fills the one at +0x20 from the caller's key string (001A4C90, source [r8], 0071E39F); the one at +0x40 is left empty (capacity 15, size 0): key copied, default mapped value", with the dated note. `dd_crt_check.py`'s comment (line 42) carries the old wording and is routed. |
| [dd-anim](../auditspec-review-dd-anim-0930/REVIEW.md) | applied | `22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md` (§2), `opus-dd-crt-0930/batch2-animation.md` | The §2 sentence is replaced as quoted. The record's summary of that change carries a note. |
| [dd-1599-a](../auditspec-review-dd-1599-a-0930/REVIEW.md) | applied | `16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md` (§4a) | §4a's first bullet now gives 247 / 206 at HEAD. The §2 UQ-190 note, dated 2026-09-17, keeps 240 / 203 as the review allows. |
| [sd100](../auditspec-review-sd100-0930/REVIEW.md) | applied | `sd100-reveal-modes-0930/README.md` | Items 1-4. The "variable" row is struck, and a "restore" row is added. The mode-4 writer's `(dword & 0xFFF7FF04) or 4` writes the review's bitwise OR as the word "or", because a table cell carries no pipe. |
| [sd105](../auditspec-review-sd105-0930/REVIEW.md) | applied | `sd105-reveal-inputs-0930/README.md` | Items 1-3. V2's last sentence (the fade fraction) is unchanged. |
| [sd106](../auditspec-review-sd106-0930/REVIEW.md) | applied | `sd106-measure-sites-0930/README.md`, `sd106_sites.py` (the M5 comment only) | Items 1-4. The check itself is unchanged, as the review allows, so its output does not move. |

**Blocked.** `_types/types.tsv` (the dd-crt cell): SWE2-STRUCT holds the file on the board. Nothing was blocked by
another identity's uncommitted work. None of the four never-edit pages was a target.

**Register.** No review's wording targets a register cell. One cell is proposed above (GR-1), because the record
it restates now says more than the cell's Limits sentence. SD-1, SD-100, SD-105, SD-106, GR-4, GR-5, GR-7, GR-13 to
GR-15 and GR-17 state answers that the narrowings leave standing.

**Routed, not edited:** see [consumer-check.md](consumer-check.md).
