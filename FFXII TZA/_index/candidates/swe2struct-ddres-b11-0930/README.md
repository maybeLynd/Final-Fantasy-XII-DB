# DD residue closure, batch 11: four pages with closed registers and open prose (SWE2-STRUCT for OPUS, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, batch 11. The batch was run by a Claude session in the
SWE2-STRUCT lane, started by OPUS, with no subagents, no board tasks and no commits.

FABLE's ruling (`status-currency-ruling-fable/README.md`, "What the check cannot do") lets a page read DOCUMENTED only
when no sentence such as "still open", "not read" or "unknown" is left without a register id. Every register row these
four pages name is closed, but their prose still carried such sentences. All four were clean at HEAD when the batch
started (`git status --short` empty for each):

- `07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md` (CRLF)
- `07-Combat-Action/Action-Definition-Row/the-action-definition-row.md` (CRLF)
- `12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md` (CRLF)
- `18-Audio/Sound-Selection/sound-variant-selection.md` (LF)

The sentences were found with `grep -n -i` for *not read, unread, not yet, not established, still open, remains open,
unknown, not settled, not proven*, plus a wider pass (*not followed, not re-examined, has not been run, is the
residue, what remains*). Text inside `~~strikes~~` and lines that already carry a later answer note were set aside.
No status word was moved: OPUS re-statuses after its owner read. Nothing was struck, so this batch has no
`consumer-check.md`. Every edit is an added note or an added evidence row, and each line keeps its own ending
(`git diff --numstat`: 3/2, 10/10, 8/7 and 3/3).

## Dispositions (SWE2-STRUCT for OPUS)

Legend: **STALE** = already answered, so a dated note was added pointing to the answer. **BOUNDARY** = another page
owns the fact. **RESIDUE** = open and in scope. **carried** = the line already names its register id and answer, so it
was not edited.

### how-a-combo-continues-and-what-it-blocks.md: STALE 3, BOUNDARY 0, RESIDUE 1 (answered) (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 4 (status) | "what the battle HUD's per-frame walk draws … is not read (GR-3 …)" | STALE; GR-3 is ANSWERED. Left for OPUS's re-status, because the front matter is not edited |
| 375 | "What that routine puts on screen is not read (`GR-3`)." | STALE; note added pointing to the GR-3 item |
| 423 | "the per-entry draw routine reached from the list walk is not read" | carried (the GR-3 answer note follows it on 425) |
| 425 | "Which glyph the label is stays unread." | **RESIDUE, answered in place** (C1–C6, D1–D4). The label is the atlas `battle_4_c`, sub-image code `0x0001` frame 14, and it is the word "Hits", localised per pack. An evidence row was added to §9 |

### the-action-definition-row.md: STALE 10, BOUNDARY 0, RESIDUE 0 (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 27 | "which bytes no reader has been found for … leaves the rest as shape" | STALE: AY-2 ANSWERED (every byte placed) |
| 66 | `+0x0C`: "the other bits are read by the two gates, not yet decoded" | STALE: UQ-107 ANSWERED, record `uq107-action-flag-bits` |
| 186 | "Still no reader at hop 0 or 1: `+0x02`, `+0x03`, `+0x21`, `+0x30`, `+0x38`" | STALE: AY-2 and the §2.2 readers `00320D70`, `0030A370`, `00237FC0`; `+0x21` has none |
| 187 | "a reader of those five bytes, if one exists …" | STALE: as 186 |
| 188 | "Still without a reader or a reading: `+0x02`..`+0x03` … and `+0x21`" | STALE: as 186 |
| 189 | "those bytes are not read; if they are consumed at all …" | STALE: AY-2's second instrument |
| 196 | "the bit meanings are not read" | STALE: the ANSWERED line at the head of UQ-107 |
| 197 | "`+0x0C`'s bits stay open … it has not been run over these sites" | STALE: the 2026-09-18 census and UQ-107 |
| 198 | "The others in the list were not re-examined." | STALE: the 2026-09-27 correction in the same paragraph |
| 199 | "bit 5's meaning … is the status-mask pages' to read" | STALE, although it is worded as a boundary: UQ-107 finds `+0x2C` bit 5 read by nothing |
| 45, 77, 79, 89, 103, 136/148, 151, 183, 206 | "not followed", "`+0x21` … unread (AY-2 …)", "not read here … (GR-6)", "is open (GR-7)", "(unread: AY-2)", "reader not found", "`+0x0B` stays unread, GR-5", UQ-106's "unread bytes", GR-6 | carried |

### the-shop-table-and-its-stock-gates.md: STALE 6, BOUNDARY 0, RESIDUE 1 (answered) (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 336 | "Still open: where the Vendor of Goods stands … is not established." | STALE: the next two paragraphs (`fon_b01`; UQ-133 ANSWERED) |
| 629 | "The half-price sell rule is not read here from lore" | STALE (not open): "from lore" names the source, and the rule is read from the code |
| 775–776 | "'nothing reads the price' is *not* established … What also remains unread is whether the selector … routes to `0057DED0`" | STALE: the price reader `0056D370` (the paragraph below), and GR-15 (family A = the inventory menu, selectors 0–7, whose equipment kind is filled by `0057DED0`) |
| 782–783 | "Narrowing it needs the object's identity, which is exactly what is not established here" | STALE: the GR-14 record (`005651E0` belongs to family A's four list procedures) |
| 796 | "that the object at the widget's `+0xC0` is the driver is … not proven separately" | STALE: `gr13-15-shop-list-widget-0930`, consumer item 6 (`0056C9BC`–`0056C9CB`) |
| 858–860 | "Stated as **unread by these two builders**, not as unused …" | STALE: the same record's item 3 / D1. Three more sites read the second word; the note also says that "nine reference sites in the entire image" undercounts |
| 991 | "this page does not read what it counts" | **RESIDUE, answered in place** (S1–S5): counters 19 (*Collector*) and 14 (*Privateer*). An evidence row was added to §8 |
| 797 | "What stays open … That is GR-14" | carried (GR-14 is answered in §7) |

### sound-variant-selection.md: STALE 3, BOUNDARY 0, RESIDUE 0 (SWE2-STRUCT for OPUS)

| line | sentence | disposition |
|---|---|---|
| 321 | "naming those fields is the residue" | STALE: registered as G-2, whose SUPERSEDED disposition names the finite residue `+0x24`, `+0x28`, `+0x2C`, `+0x30` |
| 344 | "What remains is an indexed walk … Those candidates are the next step." | STALE: closed by the walk-routes narrowing above it (`g2_walk_routes.py` W1–W3), read with the SD-24 note |
| 536–537 | "whether they share state depends on threading, which is not established here — `SD-25`" | STALE: SD-25 ANSWERED (the audio thread has its own `rand()` state) |
| 4 (status) | "SD-23 … and SD-25 … are open" | STALE; both are ANSWERED. Left for OPUS's re-status |
| 110 (heading) | "shape read, rule not yet proven" | carried: the next line says "Superseded by §12". The heading was not edited, so its anchor is kept |
| 163, 340, 343, 549, 718 | SD-23; G-2's "is the residue" and "what remains is a copy by code outside those consumers"; the modulus note; G-2's §12 residue | carried (SD-23 answered in place; G-2 SUPERSEDED with its named residue; 549 already corrected) |

No register row is proposed and nothing is marked runtime-only: every sentence was either stale or answered statically.

## The two answers, in player terms (SWE2-STRUCT for OPUS)

- **The combo popup reads "N Hits".** From the second hit of an Attack combo, the counter over the unit is the hit
  count beside a word drawn from the UI atlas `battle_4_c`. The word is "Hits" in the English pack, "Treffer!" in
  German, "coups" in French, "golpes" in Spanish, "colpi!" in Italian, and "Hits!" in the `in`, `kr`, `ch` and `cn`
  packs. At 12 the digits switch from the small style (28 × 38) to the large one (36 × 50). A modder who edits
  `battle_4_c`'s 130 × 60 cell at (120, 0) in `tex2pack_ys.bin` changes the word.
- **Shopping feeds two achievements.** Every purchase reports the bought id to counter 19, and *Collector*
  (`ACH_SPECIAL_HORIDASHI`) unlocks when that id is `0xD07F`, the last bazaar good. A sale adds the quantity sold to
  *Privateer*'s counter (`ACH_COUNT_SELL_EVITEM`), but only when the driver's `+0xE4` bits 6–13 read 7.

## Receipts (SWE2-STRUCT for OPUS)

Static work on the certified shipping image (`73461d08…`) through `retool.py`. The data is the installed
`FFXII_TZA.vbf`: the ten `ps2data/image/ff12/myoshiok/<lang>/packfiles/tex2pack_ys.bin` packs, read by the checker's
own SRYK reader.

| script | result |
|---|---|
| `b11_struct.py` (`b11_struct.out`) | C1–C6, D1–D4, S1–S5: 127 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | `TALLY READY=2 READY-WITH-POINTER=2 of 4`, FAILS 0 |

- **C1** reads `00280750`'s stack name array. Slot `+0x338` is `battle_4_c`, `+0x360` is `partytop_4_c`, and all ten
  slots are named. *Positive control:* `+0x368` is `partytop_8_c`, which is the `_00A0` texture of the
  `hud-blocks-identified-0930` record, and the ten names are exactly the loader-bound page's set.
- **C2** pins the lockstep bind, directory entry *i* to slot *i* (`00280670`). **C3** pins the three getters.
- **C4 / C5** pin `0028AAA0`'s two lookups: the label is code 1 frame 14 (`lea rdx, [rsi + 0x70]`), and the digits are
  code 1 at the cap or code 2 below it, with the digit as the frame. **C6** is the control: the types 2/9 constructor
  uses the same lookup.
- **D2** finds the label cell (120, 0, 130 × 60) in all nine full-size packs, and (126, 38, 37 × 17) in `in_sdver`.
  *Positive controls (D3):* the digit codes decode to ten equal cells in a row, 36 × 50 at y 273 and 28 × 38 at y 331,
  which only a correct lookup produces. Frame 13, one short, is a 16 × 16 placeholder at (0, 0).
- **D4** shows that the label pixels form six distinct pictures by language. The words themselves were read visually
  from crops written by `b11_struct.py --png DIR` (palette 0, CSM1 order). The colours are not claimed, only the
  shapes.
- **S1–S2** pin both arms of `0056D370` after the commit. **S3** pins `00316A50`'s kind-0 / mode-1 path. **S4** reads
  descriptors 19 and 14 from `00D10460`. **S5** reads the achievement records at `01DFE410`. *Positive control:* slot
  19 is `{13, ACH_COMPLETE_YUGOU, "Mist Walker"}`, as the catalogue page records.
- **Blind spots.** The label's word is data read from the shipped packs; a repacked archive can change it. Which
  language pack a given install loads is not examined here. What bits 6–13 of the driver's `+0xE4` denote is not
  named; the condition is stated as the code tests it. The callee names `Shop_CommitPurchaseItemAndGil`,
  `Shop_CommitSaleItemAndGil` and `AchievementCounter_UpdateAndMaybeFire` are the database's, and the checker does
  not verify them.

## For OPUS: consumers and things left untouched (SWE2-STRUCT for OPUS)

- **The achievement catalogue page is stale on two points** (routed, not edited):
  `20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md` line 331 says `0056D370` passes 19
  "gated on `[+0xE4] & 0x3FC0 == 0x2C0`". S2 shows that the `0x2C0` test guards only the `0030B630` call, and that
  counter 19 is reported on every purchase. Its census of direct feeders (lines 319 and 331) also misses counter 14.
  The sale arm loads `cl = 0xE` at `0056D496` and jumps to the shared call at `0056D4D2`, so a raw-index read at the
  call sees only the purchase arm's `0x13`. `the-bazaar-recipe-unlock-and-purchase.md` line 374 names counter 19 only.
- **The shop page still carries `gr13-15-shop-list-widget-0930`'s consumer items 1–5**, which that record routed to
  FABLE: "layout B", the cursor-relative table for `0057DAD0`, "`+0x10` is not a stable price field" applied to shop
  lists, "nine reference sites in the entire image", "1, 1, 2, 3", and "bit 5 set by tail arm 3". Those are claim
  corrections, not residue prose, so they were left for their owner. The line-860 note only points at item 3.
- **Status lines.** The combo page's status still says GR-3 "is not read". The shop page's says GR-13 / GR-14 / GR-15
  "stay open". The sound page's says SD-23 / SD-25 "are open". All five rows are ANSWERED, so this is left for OPUS's
  re-status.
- **Bounds outside the grep set, not edited:** combo line 188 ("a whole-qword store to the flag word is not covered
  by this sweep") and shop line 338 ("native writes of the counter are not censused"). Each is a stated scope bound on
  an answered claim, not an open question the page asks.
