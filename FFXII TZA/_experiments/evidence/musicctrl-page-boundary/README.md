# Music-control rebase/reader page boundary — pending independent acceptance

Method A: original static instructions plus retained original-code EXP099 observations, kept separate. No fresh isolated/native/live run, no historical22-case/20-mutation campaign replay. Question/method/control/limits are in PLAN.md.

Reference EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, canonical image base00120000. Complete original callback003EAB9071B and reader003EAA70229B retained as raw bytes, disassembly and hashes in primary.json. Existing image reader unchanged/pinned. Canonical mechanism/two contracts and EXP099 driver/result preimages retained with hashes. Do not treat the arithmetic witnesses below as measured native writes.

The rebase callback loads dword table+4, performs wrapped32-bit +127 followed by signed biased divide128, and visits that many header words starting table+8, stride4. A nonzero visited word gets low32(table base) added; zero is skipped. For the small nonnegative witness domain without overflow, its count is `(maxFieldId+127)//128`.

The reader rejects only `fieldId > maxFieldId` (signedJL at003EAA8C); equality passes. It then selects page by biased signed divide128, loads/sign-extends that page word and, if nonzero, dereferences it immediately. The current field-selection contract rightly calls this an inclusive maximum.

| Inclusive maximum | Callback visits page indexes | Reader page for field==maximum | Covered? |
|---|---|---|---|
| 0 | none | 0 | no |
| 127 | 0 | 0 | yes |
| 128 | 0 | 1 | no |
| 129 | 0,1 | 1 | yes |
| shipped1311 | 0..10 | 10 | yes |

Thus at the exact positive128 boundary, a nonzero final file-relative page word remains unrebased, although the inclusive reader admits that field and consumes the word as an absolute address. If that word is zero, the reader returns−1 instead; the boundary is not a universal fault. No actual exception or invalid game table is asserted. The shipped maximum1311 and its11 pages/291 runs remain consistent; this does not invalidate that corpus walk.

Retained EXP099 supports equality admission and normal page/null-page behavior under its supplied state: arg-eq-bound returns7, arg-over-bound returns−1, page1 returns18, page-null returns−1, each with real subject/getter trace and no recorded fault. Its actual driver explicitly excludes loader production and plants every page as `PAGE+pi*0x1000`. Consequently its successful reader result cannot certify callback production of those absolute page words. Keep the original accepted finite reader/threshold claims; qualify only the producer-consumer coverage. No scripted callee is upgraded to a native effect, and no old mutant kill erased.

check.py derives the seam from exact operand/branch/update anchors, validates the retained receipts/preimages and distinguishes adjacent/shipped static witnesses. Five corrupted-derivation controls reject an exclusive bound, corrected rounding, changed visit count, changed reader granularity and a rebasing reader. These are receipt/analysis controls, not executed binary mutations. Source qualification and independent original-byte review are still required; PASS is not canonical closure.

L1/L2 implication: the database's header extent/preconditions must distinguish the inclusive reader's required final slot from the callback's rounded visit count. A modder changing the highest field to an exact multiple128 needs to account for this producer-consumer seam when supplying a nonzero tail page. A reconstruction following a universal “all pages rebased” rule would change original boundary behavior. No replacement implementation, L3 parity requirement or authored-data census takeover.

Affected owned consumers: FABLE `the-music-control-file-and-the-bgm-stream.md` §2.2/format explanation, OPUS `CONTRACT-music-control-file-and-bgm-stream.md` MC-5/edge conditions and `CONTRACT-field-music-selection.md` inclusive-bound/page-production interpretation. Independent SWE2-AUDIT-SPEC must re-derive the original arithmetic and retained fixture scope; FABLE/OPUS adjudicate and incorporate. PENDING PROPAGATION. Normal delivery order, allocation placement, table lifetime and actual authored occurrence are separate and unchanged.

Cleanup/state: EXE read-only and exact hash verified. No guest/native/game/PC/instrument or save/config changes; no fresh restoration receipt. Existing runtime authorization/extra-input setup budget unchanged. Full database goal ACTIVE / DB_GOAL=NOT_MET.
