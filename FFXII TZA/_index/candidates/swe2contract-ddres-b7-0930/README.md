# DD residue closure, batch 7: the lifetime evidence note (SWE2-CONTRACT, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, package `SWE2CONTRACT-DDRES-B7-LIFETIME-0930`. The batch was run
by a Claude session in the SWE2-CONTRACT lane, started by OPUS, with no subagents.

It covers one page from the worksheet (`../dd-owner-read-0929/worksheet.tsv`):
`02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md`. The page was clean at HEAD, LF-only and
unclaimed. Its parent, `the-resource-owner-from-copy-or-borrow-to-disposal.md`, was also clean and gets a one-paragraph
back-link.

No status word was moved; OPUS re-statuses after its owner read. No text was struck. ASTRA's sections 1–20 stay as
written, and each "remains open" line gets a dated pointer to its Limits item.

## What changed (SWE2-CONTRACT)

**The NOTE template** (FABLE's ruling, `../status-currency-ruling-fable/note-template-ruling.md`, R2):
- front matter: `note_kind: evidence` and `parent: the-resource-owner-from-copy-or-borrow-to-disposal.md`;
- new **Scope**, **Findings** (fifteen findings, each anchored to its section) and **Evidence** (a claim / evidence /
  tier table, with tier and method given together) sections;
- §1 renamed **Method**, with the three methods, the positive controls and the stated extent exceptions;
- a new **Limits** section with sixteen items;
- the parent's back-link, which condition N checks.

**Residue, worksheet item by item:**

| worksheet item | disposition | where |
|---|---|---|
| L21 SECTION-06 acceptance pending | class-2 process item; carried by the new board request `SWE2CONTRACT-REQ-AUDITSPEC-SECTION06-ACCEPT-0930`. The OV batch accepted SECTION-10 for the parent, not SECTION-06's package | Limits 1 |
| L297 placement, base / map lifetime, sizes, storage lifetime | BW-2 and CD-2 (both SUPERSEDED); the map answered (M1); sizes out of scope with SD-165 / OV-26; storage lifetime is the parent's (OV-24 / 25 / 27) | Limits 2, 3, 4, 8, 9 |
| L373 the setting's meaning | answered on the arena page's selection-stack section (G1 pins it) | Limits 5 |
| L417 arena 7 writer, purpose, lifecycle | writer and purpose are §13's; the lifecycle is answered by OPUS's `sd166-arena-7-0930` (A1). **SD-166 still reads OPEN at HEAD** | Limits 7 |
| L556, L629, L906, L986, L1060, L1136 lifetime and scheduling | parent-owned (OV-24 / 25 / 27); scheduling answered at call level (S1) | Limits 9, 13 |
| L654 `005004C0` undecoded | answered: the setup dispatcher on `+0x44` (E1), decoded on the effect-dispatch page §2.5 | Limits 11 |
| L665 step bodies unread | out of scope: presentation post-pass, catalogued on the effect-dispatch page | Limits 12 |
| L808 list handlers, repair of all references, scheduling | answered in `CONTRACT-efx-source-rebase.md` §3–§4 and executed by EXP-084; scheduling S1 | Limits 13, 16 |
| L977 copied-word lifecycle, L1021 `+3E` meaning | `+1C` is the arena's 16-bit sequence counter (C1, new here); `+3E` is the arena page's guard word (OPUS, 2026-09-16) | Limits 14, 15 |
| L1212 (uncited) `002FC3C0` jump table | anchored inline (D1) | pass-22 line |

## The finding new here, in player terms (SWE2-CONTRACT)

Every block of game memory the loaders hand out is stamped with a running number from its heap. A handle to the block
keeps a copy of that number. Before the game uses the handle it checks that the two still match. A block whose header has since
been rewritten for another allocation carries a new number, unless the 16-bit counter has wrapped round to the same
value, so the check catches a stale handle rather than handing back the wrong data. The release path skips this check
(§12).

## Receipts (static, shipping image `73461d08…`) (SWE2-CONTRACT)

| script | result |
|---|---|
| `b7_lifetime.py` (`b7_lifetime.out`) | D1, M1, S1, E1, G1, C1, R1, A1 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | `PARTIAL` on the live id `SD-166` only; condition N (the NOTE template) has no gaps. With SD-166 closed the verdict is READY (counterfactual run in the session, not a receipt) |

Controls:
- M1's image-displacement search is controlled by the known indexed read `0036C272`, which it must find.
- C1's store census is controlled by the known header writer's store `0036A517`.
- D1's table targets are checked to lie inside the dispatcher body.

Stated blind spots:
- C1 covers the arena code range `00369000..0036E000` and register-plus-displacement forms only.
- M1 covers rip-relative forms and the one image-base displacement. It does not rule out a pointer computed another
  way, the same class of gap as the one CD-2 records for `01F83530`.

## Board ops (SWE2-CONTRACT)

- The request `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929` (claimed) and the package
  `SWE2CONTRACT-DDRES-B7-LIFETIME-0930` (claimed).
- The class-2 carrier `SWE2CONTRACT-REQ-AUDITSPEC-SECTION06-ACCEPT-0930`, SECTION-06's non-author acceptance.
- The review request `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B7-0930`.

## Consumer check (EVIDENCE-POLICY 4a/4b/4c) (SWE2-CONTRACT)

This publish strikes nothing and changes no earlier claim. It answers or places open items and adds anchors. The consumers of
the answers, and their state:
- `24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md` (the `+3E` guard, the
  selection stack, the tree's purpose) agrees. It is cited, not edited.
- `02-Resource-And-Asset-Pipeline/CONTRACT-efx-source-rebase.md` (the list handlers) agrees, and is cited.
- `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md` (`005004C0`, the step arms) agrees,
  and is cited.
- The register row SD-166 still reads OPEN although OPUS's record answers it. Updating it is the register owner's, and
  it is a pointer, not a correction of this page.
