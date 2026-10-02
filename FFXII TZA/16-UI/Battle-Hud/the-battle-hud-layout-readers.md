---
id: ui-battle-hud-layout-readers
title: The battle-HUD layout-key readers — command menu, mist, gauges, overhead, number effects
status: DOCUMENTED — the command-menu procedure 00276D30's arms are decoded on the selection page; the other procedures' arms (SD-126, OPUS), the base-pointer key reads (SD-127, OPUS) and the 002C7660 parent (SD-128, FABLE; reviewed ACCEPT-WITH-NARROWING by SWE2-AUDIT-SEM) are answered (owner re-status 2026-10-01, OPUS; documented_rule READY)
evidence_tier: 1
tags: [ui, battle-hud, layout-keys]
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  snapshot_basis: GN160's snapshot by pairing, not by a separate verification - the document already names GN160 as its gzf_sha256 and b57264ba IS GN160's annotation snapshot, recorded in GfzEnv.ps1's lineage and in every other GN160-stamped document. Added 2026-09-15 (OPUS) to complete the block, not to assert a check nobody ran. This page's 2026-09-14 falsification pass is separately image-derived: every cited instruction was read from the authorized EXE.
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `0028B140`, `002A86A0`, `002C7660`, `002C7B10`, `002C84E0`, `003FDFE0`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-14
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: OPUS-thirteen-instructions-hold-nine-installations-found-one-finding-withdrawn
  last_pass_kind: attack
  crossref_clean: false
  reopened_count: 0
addresses:
  - "00276D30"
  - "002778C0"
  - "00298250"
  - "0027AD70"
  - "00299D10"
  - "0029E110"
  - "002C0870"
  - "002C1E20"
  - "002CF440"
  - "00405310"
---

# The battle-HUD layout-key readers

**Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, owner re-status 2026-10-01)* — this page documents where each `uisize.json` key of the battle-HUD families
lands at its native use site (the LAYOUT-KEY-READERS package). The widget procedures themselves
(`00276D30`/`002778C0` battle command menu, `00405310` boss gauge, `003FDFE0`/`003FF360` status
window) are atlas-labelled but their dispatch arms are not decoded here. *(2026-09-30, SWE2-DATA: `00276D30`'s are decoded on [the selection page](../the-selection-the-menu-publishes.md), a 53-id procedure with ten handled ids; the rest are `SD-126`.)*

## What the player sees (SWE2-DATA, 2026-09-30)

Each key below places or tints one element of the battle screen: the command menu's tags, scroll bar and mist-count icons, the gambit indicator, the enemy / other / side HP-gauge colours (a lerp between a Min and a Max RGBA by HP fraction), the boss gauge's extended colour, the status window's top and bottom elements, the overhead status numbers and the "N/A" text, the EXP / LP numbers, the level-up blink, the "NG" signal and the silhouette window. The values are loaded from `uisize.json` by the layout loader ([the layout-parameter page](../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md)).

## Key addresses (SWE2-DATA, 2026-09-30)

| address | what |
|---|---|
| `00276D30` | the command-menu widget's message procedure |
| `002778C0` | the command dispatcher widget's procedure |
| `00405310` | the boss gauge's procedure |
| `003FDFE0`, `003FF360` | the status window's procedures |
| `002C7660` | ~~the unlabelled parent of the HP-gauge and overhead-status paths~~ the per-unit overhead-display evaluation (one call per `[hud+0x1D70]` node from `002C62B0`): ~~fade level, anchor,~~ a level (a per-unit render channel, read as fade: `00272DE0` forwards to `002E7E90`, the character render record's channel 11, which is named nowhere), an offset labelled anchor *(Corrected 2026-10-02, FABLE, on SWE2-AUDIT-SEM's review [`auditsem-review-sd125-128-0930`](../../_index/candidates/auditsem-review-sd125-128-0930/REVIEW.md) N3)*, gauge kind, then the HP-gauge and overhead-status paths and the name-label layout (SD-128) |
| `002C1DDC`, `002CF41C`, `0029E0FA` | the rip-relative `lea` installers of `002C1E20`, `002CF440`, `0029E110` |

## The command menu and mist layer

| reader (→ owner) | keys | what the values do at the use site |
|---|---|---|
| `00273E30` (←`0035C620`) | `BattleCommandNumTagWidth`, `BattleCommandMistTagWidth`, `BattleCommandScrollBarWidth`, `BattleCommandScrollTableOffsetX`, `mBattleCommandItalicRevJp/Us` | tag widths `cmovne`-selected and `add`ed into the tag layout (`00274554`, `00274560`); `ScrollBarWidth`+`ScrollTableOffsetX` `add`ed into `edx` — the scroll region's X (`00274015`, `0027401B`); the `ItalicRev` pair is the per-locale italic reverse offset — `cmove ebx` picks US vs JP (`00274627`, `00274642`) |
| `0027CE70` (inside the `002778C0` battle-command subtree; reached indirectly — no direct call edge) | `BattleCommandMistPosX/Y`, `BattleCommandNumPosX`, `BattleMistCount0–3Offset`, `BattleMistIconWidth` | `MistPosX` `sub`ed into `r9d` → `002D8CB0` draw (`0027D0E4`); `MistPosY`/`NumPosX` → `r14d`/`r12d` position registers (`0027D094`, `0027CF37`); the four `Count` offsets → `[rsp+0x44]`/`[rsp+0x4C]`-family args — the mist-count digits' slots (`0027CFE5`–`0027D001`); `MistIconWidth` `imul`ed into `r9d` — per-icon stride (`0027D0C7`) |
| `0027DED0` (←`002778C0` P, battle command menu + help message) | `BattleCommandGillTagOffset`, `BattleCommandNumTagWidth`, `BattleCommandScrollTableOffsetX`, `mBtlCommandScrollTableOffsetY` | `GillTagOffset − NumTagWidth` — the gil tag sits left of the number tag by its width (`0027DF31`/`0027DF37`); `ScrollTableOffsetX` word → `[rcx+0x98]` (`0027DFAA`); `ScrollTableOffsetY` → `r9d` with a `cmovbe` bound (`0027DF7F`) |
| `00298250` P (battle command menu child, installed by `002985D0`) | `mBattleCommandItalicRevJp/Us`, `mCPCWindowHeight` | italic-reverse pair `add`ed into `ecx`/`edx` (`002984FB`, `00298501`); `CPCWindowHeight` → `r9d` + `cmovg` — the charge/command window's height clamp (`00298549`) |
| `0027AD70` P (scroll list, installed by `BattleMenu_UpdateCommandSelectionAndDispatch`) | `mScrollListHeight` | `eax` → `[rsp+0x4C]` — the visible list height fed to the scroll calc (`0027AE79`) |
| `00276BE0` (battle-menu region; no direct call edge) | `mGambitPositionOffsetX`, `mGambitPositionOffsetY` | `OffsetX` `add`ed into `edx` → `00242600` (`00276D19`); `OffsetY` → `r8d` → `[rsp+0x20]` (`00276D04`) — the gambit indicator's draw position |

## Gauges and status

| reader (→ owner) | keys | what the values do at the use site |
|---|---|---|
| `002C5F90` (←`002C8310`←`002C7660`, the HP-gauge path) | all 24 `HpGauge{Enmey,Other,Side}{Min,Max}_{R,G,B,A}` | per-channel `Max − Min` deltas → `cvtdq2ps`/`mulss` — a color lerp: each gauge (enemy/other/side) interpolates between its Min and Max RGBA by HP fraction (e.g. `002C6048`/`002C604E` for Enmey A, `002C6030`/`002C5FBC` for Other, `002C6154`/`002C60E0` for Side) |
| `0029E840` (←`00405C20`←`00405310` P, the boss gauge) | `BossGaugeExColorR/G/B/A` | four `movzx` byte loads assembled into the extended-gauge color state (`0029EA58`–`0029EA6F`) |
| `002C1CC0` (←`003FD2C0`←`003FDFE0` P, status window) | `StatusAloneBottomX`, `StatusAloneBottomY` | `edx`/`r8d` + `r9d`=1 + `[rsp+0x20]`=`0xC8` — the draw call's position args for the bottom status element (`002C1CE4`, `002C1CD7`) |
| `002C1D30` (←`003FDA20`←`003FF040`→`003FF360` P, status window + action list) | `StatusAloneTopX`, `StatusAloneTopY` | same arg shape for the top element (`002C1D54`, `002C1D47`) |
| `002C1E20` P (status-window leaf, ids 1/18) | `StatusAloneBottomX`, `StatusAloneBottomY` | `BottomX` word → `[rbx+0x98]` (`002C1E9E`); `BottomY` → `r8d` (`002C1E8A`) — the leaf's stored rect |
| `002C4720` (←`002C12B0`/`002C1320`/`002C4460`←`002C1A80`→`002C2320`) | `ActionListMistLineOffset`, `ActionListMistNameOffset`, `ActionListMistTableOffset` | each `add`ed to the anchor widget's `+0x9A`/`+0x9E` pair and stored as a **Y** — the mist column's line/name/table Y offsets in the action list (`002C530B`, `002C532E`, `002C5350`) |
| `002C0870` P (target info) | `TargetInfoMoveY` | `ebx` = key — the target-info window's Y (`002C097B`) |

## Overhead, effects and indicators

| reader (→ owner) | keys | what the values do at the use site |
|---|---|---|
| `002C84E0` (←`002C7B10`←`002C7660`) | `OverHeadStatusNumXSpace`, `OverHeadStatusOffsetX`, `OverHeadStatusOffsetY` | `NumXSpace` → `r14d` — the digit stride for overhead status numbers (`002C8579`); `OffsetX/Y` `add`ed into `eax` — the icon origin (`002C8756`, `002C877A`) |
| `002C64C0` (←`002900C0`, the N/A overhead proc) | `NAOverHeadTextOffsetY` | `ecx` = key — the "N/A" overhead text's Y (`002C67EE`) |
| `0028B140` (←`00289A10`←`0028EE10`, the EXP/LP effect path) | `ExpLpPositionOffsetX/Y`, `EXPLPNumOffsetX/Y`, `ExpNumOffsetX`, `LpNumOffsetX`, `NumEffectLPOffsetY`, `mExpEffectOffsetY` | the position pair word-`add`ed into the effect origin (`0028B38E`, `0028B39A`); the `*NumOffset*`/`mExpEffectOffsetY` values loaded to `eax` and stored into the `0209BA60`–`0209BA78` effect globals; `NumEffectLPOffsetY` `add`ed on top (`0028B214`, `0028B60B`) — the EXP/LP number-effect's complete placement block. Caveat (Y-1, 2026-09-27): `0028B24A` overwrites `EXPLPNumOffsetX`'s global with `ExpNumOffsetX` or `LpNumOffsetX` before the read at `0028B5F1`, so the authored key never reaches the digits |
| `00299D10` P (level-up blink) | `LevelupBlinkSpeed` | `r8d` = key beside `xorps xmm0` — the blink timer's speed arg (`00299E7D`) |
| `0029E110` P (the NG signal — tail-jump installed per the protocol page's DL-2 list) | `NgSignalOffsetBaseX`, `NgSignalOffsetBaseY` | `BaseX` `movzx` word → ~~the `+0x160` record~~ `+0xC0` *(corrected 2026-10-02, OPUS: `0029E110+0x151` `mov word ptr [rbx+0xc0], ax`; the `lea rcx, [rbx+0x160]` between them only forms an argument)* (`0029E251`); `ax − BaseY` (`0029E271`) — the "NG" signal sprite's base position |
| `002CF440` P (silhouette) | `SilhouettePosX`, `SilhouettePosY`, `SilhouetteWidth` | `PosX` word → `[rsp+0x40]`, `PosY` `add`ed → `[rsp+0x42]` — the silhouette window's rect origin (`002CF4FA`, `002CF50D`); `Width` → `eax`/`xmm1` (`002CF660`) |

## Call chain (SWE2-DATA, 2026-09-30)

From the reader tables' owner columns:

```
0035C620 -> 00273E30                          command-menu tags
002778C0 -> 0027DED0                          gil and number tags; installs 0027AD70 (002779DB, 00277A08)
002C7660 -> 002C8310 -> 002C5F90              HP-gauge colour lerp
002C7660 -> 002C7B10 -> 002C84E0              overhead status numbers
00405310 -> 00405C20 -> 0029E840              boss gauge colour
003FDFE0 -> 003FD2C0 -> 002C1CC0              status window, bottom element
0028EE10 -> 00289A10 -> 0028B140              EXP / LP numbers
002900C0 -> 002C64C0                          the N/A overhead text
```

## Modding notes (SWE2-DATA, 2026-09-30)

- Each reader loads its key from a fixed global (the falsification table quotes the `01E0C3xx`–`01E0CFxx` cells and `0209E628`), so an element moves by changing that value or the use-site instruction the table names.
- The HP-gauge colour is a per-channel lerp from Min to Max, so equal Min and Max make a gauge one colour.

## What is not known

- [x] Which keys among these are also read through base pointers — this page covers the rip-relative
  readers only; `0027CE70` and `00276BE0` in particular may gain direct callers through the
  `002778C0` subtree's jump tables. **SD-127** (SWE2-DATA, 2026-09-30). *(SD-127 answered 2026-09-30 by OPUS `23a99db40`, [record](../../_index/candidates/sd127-hud-key-base-reads-0930/README.md).)*
- [x] The `002C7660` parent that owns both the HP-gauge and overhead-status helper paths is not yet
  labelled in the atlas. **SD-128** (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30, FABLE, [record](../../_index/candidates/sd125-sd128-fable-0930/README.md): `002C7660` is the per-unit overhead-display evaluation: one call per node of the `[hud+0x1D70]` list from `002C62B0`; per unit it computes ~~the fade level, anchor offset~~ a level (a per-unit render channel, read as fade: `00272DE0` forwards to `002E7E90`, the character render record's channel 11, which is named nowhere), an anchor offset (also a label) and the gauge kind *(narrowed 2026-10-01, OPUS, on SWE2-AUDIT-SEM's N3, [review](../../_index/candidates/auditsem-review-sd125-128-0930/REVIEW.md))*, calls the HP-gauge (`002C8310`), overhead-status (`002C7B10`) and element (`002C8920`, `002C8820`) paths, and lays out the unit's name label.)*
- [x] The dispatch arms of `002778C0`, the boss gauge `00405310` and the status window `003FDFE0` / `003FF360`
  are not decoded. **SD-126** (SWE2-DATA, 2026-09-30). *(SD-126 answered 2026-09-30 by OPUS `c3570bf4b`, [record](../../_index/candidates/sd126-hud-proc-arms-0930/README.md).)*

## Falsification pass — 2026-09-14 (OPUS)

This page had no falsification pass. Its claims are unusually checkable — each row names a reader, a
`uisize.json` key, and the exact address of the instruction that consumes the value — so the attack
was to go to those addresses in the shipping bytes and see whether the instruction is the one
claimed, and then to ask the harder question the page does not: **can these readers be reached at
all?**

### Thirteen cited instructions, thirteen survivals

| cited | claimed | at that address |
|---|---|---|
| `00274554` | tag widths `cmovne`-selected | `cmovne ecx, [01E0C354]` |
| `00274015` / `0027401B` | both `add`ed into `edx` | `add edx, [01E0C35C]` then `add edx, [01E0C360]` |
| `00274627` / `00274642` | `cmove ebx` picks US vs JP | `mov ebx, [01E0C34C]` then `cmove ebx, [01E0C350]` |
| `0027D0C7` | `MistIconWidth` `imul`ed into `r9d` | `imul r9d, [01E0C390]` |
| `0027DF31` / `0027DF37` | `GillTagOffset − NumTagWidth` | `mov eax, [01E0C364]` then `sub eax, [01E0C354]` |
| `00298549` | `CPCWindowHeight` → `r9d` + `cmovg` | `mov r9d, [01E0C554]`, `cmovg ecx, eax` at `00298550` |
| `0027AE79` | `eax` → `[rsp+0x4C]` | `mov eax, [01E0C348]`, `mov [rsp+0x4c], eax` |
| `00276D19` | `OffsetX` `add`ed into `edx` → `00242600` | `add edx, [01E0C36C]`, `call 00242600` |
| `002C6048` / `002C5FBC` | a colour lerp, `Max − Min` then `cvtdq2ps` | ~~`mov eax, [01E0CEF4]`; `sub eax, [01E0CF24]`~~ two lerps, one per gauge: `002C5F90+0xB8`/`002C5F90+0xBE` `mov eax, [01E0CEF4]` / `sub eax, [01E0CEE4]` (enemy Max − Min) and `002C5F90+0x26`/`002C5F90+0x2C` `mov eax, [01E0CF34]` / `sub eax, [01E0CF24]` (other Max − Min) *(corrected 2026-10-02, OPUS: the row joined one gauge's Max with the other's Min)*, `cvtdq2ps xmm1, xmm1` |
| `0029EA58` | four `movzx` byte loads | `movzx edx, byte [01E0C5B4]` |
| `002CF4FA` | `PosX` word → `[rsp+0x40]` | `movzx eax, word [0209E628]` |

Every one is the instruction the page says it is, against the register the page names. The
`ItalicRev` row is worth singling out because it is the one that could most easily have been
loose prose: `00274627` is the `mov` and `00274642` is the `cmove`, exactly as written.

### How the readers are reached — three mechanisms, and a finding this pass withdrew

Nine readers on this page are marked `P` or "no direct call edge", and none of the nine has a caller
in `edges.tsv`. That is not surprising on its own — a widget procedure is installed, not called. So
the attack was to find the installation.

**The image stores code pointers as 32-bit RVAs**, `VA − 0x120000`, which is the same form the
engine's `ImageAddress_ResolveRuntimePointer` (`0020E600`) exists to add the base back onto. Scanning
for that, and for every `E8`/`E9 rel32` in `.text` whose target is the reader, six of the nine came
back installed and **three came back with no reference of either kind**: `002C1E20`, `002CF440` and
`0029E110`. That was written up here as a finding.

**It was wrong, and the way it was wrong is the useful part.** There is a third mechanism, and the
sibling page names it in plain sight — *"`lea rdx, 002A86A0` at `002A837B`"*. An installer that forms
the procedure's address with a **rip-relative `lea`** stores no RVA and emits no `rel32`, so a scan
that looks only for those two reports a live procedure as unreferenced. Adding
`REX.W 8D /r mod=00 rm=101` to the scan finds all three immediately:

| reader | stored RVA (excl. **all** unwind data) | `E8`/`E9 rel32` | rip-relative `lea` |
|---|---:|---:|---|
| `0027CE70` | **1** — `0x008C3340` ~~3~~ | 0 | — |
| `00276BE0` | **0** ~~2~~ | 0 | — |
| `0027AD70` | **0** ~~2~~ | 0 | 2 — `002779DB`, `00277A08` |
| `00299D10` | **0** ~~2~~ | 0 | — |
| `002C0870` | **0** ~~2~~ | 0 | — |
| `00298250` | **0** ~~4~~ | 0 | — |
| `002C1E20` | 0 | 0 | **1 — `002C1DDC`** |
| `002CF440` | 0 | 0 | **1 — `002CF41C`** |
| `0029E110` | 0 | 0 | **1 — `0029E0FA`** |

*(The last three rows were moved back into their table 2026-09-30, SWE2-DATA; the correction below had split it.)*

> **Corrected 2026-09-16 (FABLE) — `FINAL-AUDIT-PROTOCOL` pass 6, and the correction makes the
> section's own argument stronger.** The column header said *"excl. `.pdata`"*, and that exclusion is
> **true and incomplete**. `.pdata` holds one copy of a function's unwind records; a second copy lives
> in `.rdata`, **chained**, behind an `UNWIND_INFO` whose flags carry `UNW_FLAG_CHAININFO` — a 12-byte
> `RUNTIME_FUNCTION` sitting immediately after the unwind codes. **Twelve of the thirteen addresses
> this column listed were fields of those records**, and the thirteenth (`0x008C3340`) is not.
>
> **They were not references to these functions. They were these functions' own unwind metadata.**
> Every one of the twelve belongs to a record whose `Begin` field is **the reader in its own row** —
> `0027CE70`'s two belong to a record beginning at `0027CE70`, and so on down the table. A function's
> own unwind chain counted as something pointing at it is the purest form of the error the evidence
> standard bans by name.
>
> **The addresses are removed rather than struck through.** The sibling residual page worked out why:
> the checker cannot distinguish an address cited *as* evidence from one cited as an example of what
> does not count, so discussing a banned address must not look like using one. The counts keep their
> old values struck so the correction is visible without the operands being.
>
> **What this does to the section's claim: it confirms it.** The argument here is that a scan for
> stored RVAs and `rel32` misses a rip-relative `lea` installer. With the unwind rows gone, **five of
> the six readers that looked referenced have zero admissible stored RVAs and zero `rel32`** — so they
> need the third mechanism as much as the last three rows do, and only `0027CE70` retains a single
> genuine stored RVA. The inflated counts were hiding the finding this section exists to make.
>
> **Test, with controls both ways.** No table parse and no count field: `UNWIND_INFO` is
> `[version:3 | flags:5]` with the code count at byte 2 and a body of `4 + 2 * ((codes + 1) & ~1)`;
> when `UNW_FLAG_CHAININFO` is set a `RUNTIME_FUNCTION` follows the codes, and its three fields must
> name a `Begin < End` inside `.text` and an unwind block in `.rdata`. Six controls, all as expected —
> three known-positive and three known-negative, the negatives drawn from the same `.rdata`
> neighbourhood so proximity alone cannot pass them.

**Each of those three `lea`s sits a few bytes above the procedure it installs** — `002C1DDC` for
`002C1E20`, `002CF41C` for `002CF440`, `0029E0FA` for `0029E110`. The installer is the function
immediately preceding its procedure in the image, which is why nothing anywhere else refers to them.

**Positive control, because a null result is only as good as the scan that produced it.** The five
readers this page says have a caller — `00273E30`, `002C5F90`, `0029E840`, `002C1CC0`, `0027DED0` —
return 1, 2, 2, 1 and 2 `rel32` references. The scan finds what is there. The control is exactly what
the withdrawn finding lacked: it proved the scan could see calls, and nothing proved it could see
installations.

**What survives.** Every `P` marking on this page is correct, and the page's reachability claims hold
in all nine cases. ~~The six that carry stored RVAs cluster in one `.rdata` region, in pairs — the
shape of a table of `(procedure, something)` entries, and worth a page of its own.~~
**Withdrawn 2026-09-16 (FABLE) with the table above: five of those six carry no stored RVA at all.**
The `.rdata` region is real and so is the pairing, but it is **not a table of `(procedure, something)`
entries** — it is the run of **chained `RUNTIME_FUNCTION` records**, and the pairing is simply that
each of these functions has two of them. **Recommending a page of its own would have sent someone to
document unwind metadata as an engine structure**, which is the failure the evidence standard names.
The addresses that bounded the region are removed for the reason given above.

**What this still does not establish.** Three mechanisms now account for all nine, but a target
computed by arithmetic from a base, or an entry held as an offset rather than an RVA, would still be
invisible. A fourth mechanism cannot be ruled out by this scan; it simply is not needed to explain
anything on this page.

## Evidence (SWE2-DATA, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| each reader row's use-site instruction | the falsification pass above: thirteen cited instructions, thirteen survivals | 1 |
| every `P` reader is installed | the three-mechanism scan and its positive control, above | 1 |
| `00276D30`'s arms | [the selection page](../the-selection-the-menu-publishes.md), the reader decode | 1 |

## Related (SWE2-DATA, 2026-09-30)

- [The selection the menu publishes](../the-selection-the-menu-publishes.md) — the command-menu widget and its `+0x2FE0` handle.
- [The layout parameters](../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md) — where the keys are loaded.
- [The widget message protocol](../Widget-Object-Model/the-widget-message-protocol.md) — the message ids the procedures handle.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

- **Presentation — SERVICE (16 edges).** The readers on this page draw through the shared render layer: `0028B140`/`002C7B10`/`002C8310`/`002C84E0` each call `003F0040` and `003F1290` (the quad/text emission pair, 8 edges), `0028EE10` reaches `003BBB60`/`003F0170`, `002C7B10` reaches `003F12E0`, and `00405C20` chains to the shader-material (`0029E840`), textured-quad (`002D9DB0`) and screen-capture (`002DB080`) helpers. The readers consume the draw path; the crossing is the emission, not a second owner.
- **CoreRuntimeScheduling — MECHANICAL (10 edges).** `RuntimePointer_EncodeImageAddress` (`0020E620`, 4), `ImageAddress_ResolveRuntimePointer` (`0020E600`, 2), `001EDEC0` (2), `00229DF0` and `00229E70` are the pointer/address helpers every UI body shares. Shared-helper fan-in, not a scheduling relationship.
- **Audio — MECHANICAL (7 edges).** All seven edges are readers calling `00249C60`, the shared Audio helper the shared-neighbours page measures at 99 callers. One accessor, not seven relationships.
- **Items_Equipment_Shops_License — SERVICE (5 edges).** `003FF360` and `002C2320` consult `Equipment_CheckPrimarySecondaryPairReasonByStatsIndex` (2), `Equipment_BuildRecommendedLoadoutForMappedStats`, `BattleStats_ClearAllEquipmentSlotsByMappedId` and `BattleStats_SetEquipmentSlotsByMappedId` — the HUD's equipment-indicator path reads the item layer's answers. The crossing is those calls, not shared ownership.
- **ActorEntity — SERVICE (3 edges).** `002C0870`, `002C64C0` and `002C7660` call `00273A00`, `003DF6F0` and `ActorRuntime_GetClassNibble` — actor class/context reads behind the overhead-status and HP-gauge paths.
- **CombatAction — SERVICE+CLIENT (3 edges).** `002778C0` calls `BattleUnit_IssueCommandByFocusHandles` and `…WithOptionalPartyFanout` — the HUD command issue path reaches into the action layer; and `BattleAction_UpdateSpecialPresentationSequence` calls `0035C620`, one reader on this page, as a client of it.
- **Party — SERVICE (2 edges).** `002C64C0` and `002C7660` call `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) — the focus-handle lookup behind the overhead-status read.
- **Gameplay — SERVICE (1 edge).** `00273E30` calls `0031C5D0` (BattleEncodedId definition-resolution validation) — a single shared-helper call.
- **Movement — MECHANICAL (11 edges).** All 11 edges are Movement bodies (`Movement_SetRequestedSpeed`, `Movement_UpdateSteeringTowardTarget`, `BattleUnit_CanAdvanceCombatNavigation`, `00326BB0` and seven more) calling `003590D0` — the same `PartyFocus_GetCurrentPackedActorHandle` cited above. One accessor's caller set, not a Movement relationship.
- **Input — MECHANICAL (4 edges).** Three `InputGameplay_Test*WithTemporalGate` bodies call `00229DF0` and `00226BE0` calls `003590D0` — Input consumers of the same shared helpers. Fan-in only.

*(SWE2-CONTRACT 2026-09-15 — edge counts from `edges.tsv`; helper identities from `functions.tsv`.)*
- **World - CLIENT (3 edges).** `00226BE0`, `003590D0` are called by bodies filed to World: `0025E400`, `002623A0`, `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - MECHANICAL and SERVICE (15 edges).** Fourteen script-VM bodies call `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) - accessor fan-in - and `00266D10` reaches `VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2D0`).

