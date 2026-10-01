# OV-41: the EFX children, their specialized subtypes, and who renders them (FABLE, Claude Opus 5.5, 2026-09-29)

**The question.** Register row OV-41 (box on `02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md`) asks for "other specialized subtypes, child construction and nonempty rendering consumers". The row's ruling:
- the specific child and rendering consumers are in required scope;
- the "other subtypes" enumeration is bounded like OV-25's residual.

The page executed one child only: an A00 record of subtype 0.

**Answer (static, `subtypes.py` W G S S2 X C K, FAILS 0; per-subtype map in `subtypes.tsv`).**

## 1. Child construction is three registrars of one shape (W, G)

The EFX walker `003EDAD0` hands each chunk run to exactly one registrar. Each registrar is called once in the image, from the walker only:

| chunk run | registrar | index | subtype byte | registry | setup switch |
|---|---|---|---|---|---|
| `0x700` | `003A7E80` | byte | record `+0xC2` | `*02EBEFA0` | `004FF270` |
| `0x800` | `003A9730` | word | record `+0x282` | `*02EBEF90` | `00442460` |
| `0xA00` | `003A9A70` | word | record `+0x44` (the element type) | `*02EBEF78` | `005004C0` |

Each registrar does the same steps:
1. Takes the record at chunk `+4`.
2. Stores the index and the subtype byte (chunk `+2`) into the record.
3. Publishes the record at `registry[index]`.
4. Runs its family's setup with the relocation delta.
5. Returns the next chunk.

The `0x600` family and the single-chunk fallback `003EE2D0` are separate paths, on [the container page](../../../17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md) and the resource-owner page.

## 2. The specialized subtypes are a closed set (S, S2, C)

Each setup switch is bounded:
- **`0x700`:** subtypes 0–3, four routines; any other value is left untouched.
- **`0x800`:** subtypes 0–8, a 9-entry table; above 8 is left untouched.
- **`0xA00`:** element types 0–`0xD1`. The sub-range dispatcher `00538910` handles types `0x42`–`0xAB` through its own table, and any type without an arm returns untouched.

That gives **65 element types with a setup routine, served by 56 routines**. This is exactly [the dispatch page's](../../../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md) independent census in §2.5 (65 handled types; setup 38 + sub-setup 18), and check C tests the agreement. 145 element types have no setup.

Setup also re-runs outside construction:
- in a sibling of each registrar (`003A7DC0`, `003A96A0`, `003A99F0`);
- in the table-wide refreshes after a move (`003A9860`, `003A9BA0`).

## 3. What setup does to a child: relocation and links (X, K)

Every setup routine rewrites **encoded image-address dwords at fixed record offsets**. It works through shared field-group helpers (`004304F0`, `00430AF0`, `0042FCF0`, `00431770` and others), each covering its group. There are two kinds of rewrite:
- **Rebased:** resolve `0020E600`, add the delta, encode `0020E620`. This is the page's subtype-0 behaviour, generalised.
- **Linked:** the keyed lookup `003AA280(id, kind, sub)` walks the list at `*02EBEF70`, matching word `+0xC`, byte `+0xE` and byte `+0xF`, and the node it finds is encoded into the record. This is how a child binds to other objects.

`subtypes.tsv` gives each (family, subtype) its routine, the rebased offsets, the linked offsets, or the named reason it did not resolve:
- **Resolved:** 48 of the 68 routines, including all 4 `0x700` routines and 8 of the 9 `0x800` routines.
- **Not resolved:** the other 20 carry a repeated field group, a loop, whose count or stride is authored or computed. The tool names the loop and does not guess the offsets.

Known answer (K): for `00500470`, element subtype 0, the tool gives exactly the page's eight dwords.

## 4. The rendering consumers: prior art, now reachable by type

Once built, an element is driven by the per-type methods in the dispatch page §2.1–§2.5:
- the step `002F3BC0`;
- the update `002F3910`;
- the walk `002F4020`;
- the release `002F31C0`.

What each of the 65 types puts on screen is UQ-204's table ([`uq204-element-type-emits`](../uq204-element-type-emits/README.md)): GiPrim, sprite, GiVmax VU1 programs, raw GS packets, or state only. The same type byte selects the setup here and those methods there, so every child built above has a named consumer.

**What a developer reproduces.** Register each chunk run into its family registry by index, then run the subtype's setup. For 48 routines the offsets to rebase or link are in the TSV. The 20 array-bearing routines need their loops read.

## Not claimed (explicit obligations)

- **The 20 array-bearing setup routines.** Their repeated field groups (count, stride and offsets) are listed in the TSV `unresolved` column.
- **What the linked `*02EBEF70` nodes are.** The list is the first slot of [the authored-table registry band](../../../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md). Its kinds are not mapped here.
- **The `0x600` family's per-chunk meaning.** It is on the container page's own not-claimed list.
- **Live execution of any subtype but 0.** No live run was made.

## Proposed register disposition

OV-41 → **ANSWERED** for child construction (§1) and rendering consumers (§4). The subtype enumeration (§2–§3) is now a closed set with extracted maps; its residue is the 20 array-bearing routines, bounded as the row's own ruling allows. The page is a SECTION carrier, so FRONTIER applies the row and the box.
