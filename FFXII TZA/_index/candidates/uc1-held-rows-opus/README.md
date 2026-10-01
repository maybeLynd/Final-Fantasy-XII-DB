# UC-1's 25 held rows: 15 are not code entries (OPUS, 2026-09-28)

**Scope.** The two applied UC-1 bands hold 25 rows as declared uncertainty: 4 in 1–64 B and 21 in 65–256 B. This record
investigates those holds. It **changes no population, ledger or denominator**, does not re-open the applied bands, and
says nothing about the separate >256 B proposals. Any disposition is for FABLE's ruling and FRONTIER's GO.

**Answer.** [`uc1_held.py`](uc1_held.py) ([output](uc1_held.out)), static on the certified image: FAILS 0. The held rows
are read from the applied files, and the listed bodies come from FABLE's instrument through the band script's prefix,
unchanged.

**T: seven held rows are a listed function's switch data.** The listed body that ends at, or just before, the held start
dispatches with two instructions:

```
movzx eax, byte ptr [base + rax + IDX]
mov   r32, dword ptr [base + rax*4 + TAB]
```

- `TAB` is the held start rounded up to 4, and `IDX = TAB + 4n`.
- The `n` dwords at `TAB` are image-base RVAs back into that listed body: the case targets.
- The byte table at `IDX` holds only values below `n`.

In seven rows the index table runs exactly to the held block's end, so **the whole block is data**:

| held | its listed function | dispatch (movzx / mov) |
|---|---|---|
| `00253BF5` | `00253BC0` | `00253BD8` / `00253BE0` |
| `003222C2` | `00322280` | `00322294` / `0032229D` |
| `003A9350` | `003A92D0` | `003A92FB` / `003A9303` |
| `00441A8F` | `00441970` | `004419BC` / `004419C4` |
| `004FF3CD` | `004FF360` | `004FF389` / `004FF391` |
| `005FD624` | `005FD5F0` | `005FD607` / `005FD60F` |
| `007298DD` | `00729870` | `00729887` / `0072988F` |

For `00208628` (listed `002085B0`, `002085D1` / `002085DA`), the tables cover only the first 60 of its 168 bytes. The
remaining 108 bytes stay open.

Three of the seven also lie inside the listed function's own unwind range (`003A92D0`, `004FF360` and `00729870` each run
to the held block's end). This is consistent: MSVC places the tables after the function's last `ret`, inside its unwind
range.

**M: eight held rows begin in the middle of an instruction.** Each of `001358E0`, `00135EC0`, `00136DB0`, `00137390`,
`00138280`, `00138860`, `0013A660` and `0013B5D0` begins at the imm8 byte of a 6-byte `palignr xmm1, xmm4, imm` at
`start − 5`. The imms (0, 1, 5, 6, 10, 11, 5, 12) are the block's first bytes. They lie in `00125740..00158DA0`, a stretch
with no unwind entries at all.

**C: control for M.** Every linear decode begun at any of the 0x1FB offsets before each slice either fails or lands on
`start − 5`: 3,155 land there and 901 fail. None lands on the held start. So these are interior slices of per-alignment
SSE routine variants, not entry points.

**R: what stays open.** Nine rows are decided by neither test: `00125770` (non-leaf, no unwind entry, as FABLE held it),
`00148BB3`, `00148D64`, `001491CE`, `001492FF`, `00158C97` (all in the unwind-free stretch), `007137BC`, `0071B6B0` and
`00809D65`. The remaining 108 bytes of `00208628` are also open.

**Not claimed:** which routines the slices belong to, or their true entries; anything about the >256 B held rows.

| consumer | action | agreement |
|---|---|---|
| `99-Unresolved-Residual/Unlisted-Code/uc1-applied-population-*.tsv` held rows (declared uncertainty) | 7 are switch data and 8 are mid-instruction slices; the holds stay as they are until ruled | routed-to-FABLE (ruling), then FRONTIER |
| FABLE's 65–256 B ruling §2 ("Nine carry BT1 hits, so the byte-table test explains them as data or tables") | now exact for seven: the table layout, its reader, and the end-to-end cover | agrees, sharpened |
| `the-bodies-the-list-cuts-short.md` / `listed-bodies-with-code-past-body-bytes.tsv` | the eight listed functions' switch tables follow their last `ret`; data, not a longer body | no change needed (tables are not body bytes) |

This is OPUS's own check; independent acceptance is requested separately.

## Part 2 (OPUS, 2026-09-28): the nine open rows and the rest of 00208628

**Scope.** Part 1's R left nine rows and 108 bytes open. This part reads them. Like Part 1, it **changes no population,
ledger or denominator**. The disposition is FABLE's ruling, then FRONTIER's GO.

[`uc1_held2.py`](uc1_held2.py) ([output](uc1_held2.out)): P E S T R, FAILS 0. Three mutated copies each fail: P with the
entry set to the held start, S with 13 table entries, T with the index table moved.

| held row | reading | the code entry | check |
|---|---|---|---|
| `00148D64` | the previous listed function's end, then NOP fill, then a leaf routine | `00148D70` | P |
| `00148BB3` | fill, routine, fill, **a second** routine | `00148BC0`, `00148C00` | P |
| `001491CE` | fill, routine, fill, **a second** routine | `001491D0`, `00149220` | P |
| `001492FF` | fill, then a routine ending in `repz ret` | `00149300` | P |
| `00809D65` | fill, then `roundps xmm0, xmm0, 1 / ret` | `00809D70` | P |
| `00125770` | after int3 fill, 16-aligned; an rbp frame that saves `xmm6` / `xmm7`; no call, no unwind entry | the held start | E |
| `0071B6B0` | after int3 fill, 16-aligned; a switch function | the held start | E |
| `00158C97` | directly after `00158C09`'s `ret`; an rbp frame; no call, no unwind entry | the held start | E |
| `007137BC` | `00713760`'s switch arms (`xor eax, eax / ret`, `mov eax, 3 / ret`, ...) and its 14-entry RVA table at `007137E0`, which runs to the block's end; 8 entries are the default, back inside `00713760` | none: `00713760`'s own arms and data | S |
| `00208628` (the last 108 bytes) | `002085B0`'s **second** switch: 4 RVAs at `00208664` and index bytes `00208674`..`002086D0` (values below 4) | none: all 168 bytes are `002085B0`'s data | T |

**What this means for the holds.**
- In the five P rows, the band's start is the previous listed function's end, and fill precedes the code. Seven
  routines sit inside those five rows; each starts on a 16-byte boundary and ends in a return.
- The three E rows start at a real entry.
- The S and T rows are not entries: they are the listed bodies' arms and tables. Together with Part 1's seven T rows,
  nine of Part 1's 25 held rows are the preceding listed function's data or arms (00208628 is now fully decided).

**References (R, reported, not required).** None of the ten entries has a rel32 call or jmp, a RIP-relative `lea` or an
absolute qword pointing at it. `00148D70` has one 4-byte RVA-shaped match, unverified. These are leaf SIMD routines of
the kind reached through runtime-built function-pointer tables. Reachability stays unestablished.

**Not claimed:** what the routines compute; that they run; any population change.

| consumer | agreement |
|---|---|
| the held rows in `uc1-applied-population-1-64.tsv` / `-65-256.tsv` | unchanged; for FABLE's ruling (routed-to-OPUS-NOTICE-FABLE-UC1-HELD-ROWS-PART2) |
| Part 1's R list | answered here, row by row |

**Run receipt.** executed at de2871230:
- `uc1_held2.py` FAILS 0;
- the three mutated copies FAILS 1 each (P, S, T).
