# UC-1 pass 2, the extent rows, and the 431 "bodies" that are jump tables (OPUS, 2026-09-25)

Evidence class **NATIVE/STATIC**, code and image bytes only. `.pdata` was used as a pointer and
**never as evidence**: FINAL-AUDIT-PROTOCOL pass 6 bans unwind data, and every conclusion below
stands without it. EXE `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

## 1. Pass 1 had 22 false positives, and they were mine

`uc1_citation_worklist.py` (pass 1, published at `5a1d44a87`) tested "is this cited address listed"
against `W.Image()`. That loads the **34,270 non-funclet bodies**: the right population for code
censuses, and the wrong one for listing. The 22 cited `Unwind@` / `Catch_All@` addresses in
`00896280`–`008A6960` are **listed** in `functions.tsv`, and pass 1 reported them as unlisted.

- The tool now tests against the full list.
- The worklist has **79 rows, which is exactly 101 − 22**. Nothing else moved.

## 2. The nine real extent rows (`uc1-pass2-extent-rows.tsv`, `uc1_pass2_extent_rows.py`)

A recursive-descent walk from each preceding listed entry follows jumps, never calls. It stops at
`ret` / `int3` / an indirect `jmp`, and it answers whether the cited address is the preceding
function's interior.

| cited | what it is | citing page's attribution |
|---|---|---|
| `0016F030` | inside the unlisted body `0016EFF0` (admitted) | the known UC-1 motivating case |
| `00277880` | inside `00276D30`'s **inline jump table** (`00277851`: `0x156D85` → `00276D85`) | cited as data — correct |
| `002FE7F0` | inside the unlisted `0x4021` "wait" handler `002FE7D0` (admitted) | correct |
| `0037C550`, `0037C690` | switch arms of `0037C3F0` (see below) | the music page's state table — correct |
| `003B69B0` | unlisted body with direct callers (admitted) | — |
| `0055B340`, `0055B380`, `0055B390` | inside the unlisted body `0055B310` (admitted) | — |

**`0037C3F0`'s listed extent is short, provably from code.**

- Its walk runs to `0037C6F8`, against a listed end of `0037C4E8`.
- It dispatches at `0037C4C9` (`jmp rcx`) through an 11-entry **image-base-relative** table at
  `0037C6F8` (`mov ecx, [r12 + rax*4 + 0x25C6F8]`, with `r12 = 00120000`).
- `0037C550` is case 2, and `0037C690` lies inside case 9 (`0037C689`).
- The residual table already carries `0037C4E8+572` as a `continuation`, so the disposition is
  right. Its note "unreferenced" means only that no rel32/lea/DIR64 reference exists: the block is
  reached through the listed body's own table.

**No mis-attribution was found among the extent rows.** Every one sits in a block the residual
population already knows.

## 3. 431 admitted "bodies" are data — the preceding function's inline jump table

**The shape.**

- A block that follows a function's last `ret` or `jmp` passed the `body` rule of
  `unlisted_admissions.py` automatically.
- MSVC places a `switch`'s table of image-base-relative dword RVAs at exactly that spot, after the
  code that dispatches through it.

**The test** (`check_admitted_bodies_are_switch_tables.py`). From the block's first 4-aligned
offset, three or more consecutive dwords that, plus `00120000`, land in `[predecessor, block)`.

**The controls.**

- **Negative:** 0 of 31,739 listed bodies meet the test against their own predecessors.
- **Positive:** `0017DD5C`, the 23-entry table the S-37 contract already documents for `0017DB90`,
  is caught.
- **Corroboration:** with the tables removed, the admitted blocks' body-shape gate (a linear decode
  reaching the last byte) moves toward the listed control.

| size band | admitted, before | admitted, after | listed control |
|---|--:|--:|--:|
| 1–64 B | 79.1 % | **99.6 %** | 100.0 % |
| 64–256 B | 40.6 % | **87.8 %** | 99.8 % |
| 256–1024 B | 22.0 % | 42.9 % | 98.7 % |

The tables were most of what failed the gate in the small bands, and the gate is why UC-1 was
"deliberately not applied".

**The regenerated `unlisted-body-admissions.tsv`.** `table` is tested first, and a new `covered`
verdict handles a block the function list has since grown over.

| verdict | blocks | bytes |
|---|--:|--:|
| table | **431** | 38,129 |
| body | 874 | 202,678 |
| continuation | 162 | 3,418 |
| ambiguous | 3 | 15 |
| covered | 1 | 379 |

**Three facts about the regeneration.**

- The `covered` row, `005806B9`, lies inside listed `0057FE80` (now 2,360 B). The generator used to
  walk back past the covering body and call the block a `body` of an older predecessor.
- **The UC-1 established floor (139 rows) contains no table and not the covered row**, so its
  generators need no rerun.
- `progress.py`'s pinned sentence now reads 206,111 B in about 877 blocks. It is dormant at HEAD,
  because the gap total moved when the function list was regenerated and the pin fails.

## 4. What is NOT claimed

- That the 874 bodies are 874 functions. The boundary argument of the residual page's §1 stands.
- What the 53 bytes after `00276D30`'s table are. They look like a byte index table; the tool
  classifies them as nothing.
- That no admitted body is a byte-only index table with no dword run ahead of it. The test needs
  three RVAs.
