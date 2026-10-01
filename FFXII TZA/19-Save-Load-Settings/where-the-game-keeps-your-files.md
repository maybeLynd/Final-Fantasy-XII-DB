---
system: Where the game keeps your files
category: 19-Save-Load-Settings
status: AUDITED
owner_layer: CodeDomain — mixed (Input and Save_Load_Settings each build the path independently); no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 2 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: pair-frontier-repos-55
  crossref_clean: true
  reopened_count: 0
---

# Where the game keeps your files

**The pair frontier's fourth candidate**, and the tightest one yet: **two functions, both documented,
sharing one address, with no document citing both.**

## The path, read from the image

```
008F3848   L"\My Games\"
008F3860   L"FINAL FANTASY XII THE ZODIAC AGE\"
008F38C0   L"%s%s"        (then L"%s\%s" and L"%s" alongside)
008F3888   L"keym..."     (the keymap file name begins here)
```

**The per-user directory is `…\My Games\FINAL FANTASY XII THE ZODIAC AGE\`**, assembled at run time
from a base path the engine obtains first.

## Both builders do it identically, and neither calls the other

```asm
; InputManager_BuildKeymapPath
00197F22  call 0x001F3EA0                ; obtain the base path into a buffer
00197F27  lea  r9,  [0x8F3848]           ; L"\My Games\"
00197F2E  lea  r8,  <the same buffer>
00197F33  lea  rdx, [0x8F38C0]           ; L"%s%s"
00197F3A  lea  rcx, <the same buffer>
00197F3F  call 0x00194EF0                ; format in place

; the settings/locale side
0079818B  call 0x001F3EA0
00798190  lea  r9,  [0x8F3848]
00798197  lea  r8,  <its buffer>
0079819E  lea  rdx, [0x8F38C0]
007981A5  lea  rcx, <its buffer>
```

> **Five instructions, same order, same two constants, same two callees — in two functions in different
> subsystems, and neither is a helper the other calls.** The construction is **duplicated, not
> shared.**

**That is the fact a modder needs:** the directory is not read from one place. **Anything that changes
where the game looks must change it in at least two, and this pair census found two — it does not
prove there are only two.**

**The format string is `%s%s` — a plain append**, with `%s\%s` and `%s` sitting beside it in the same
constant pool for the other joins. **The buffer is passed as both the destination and the first
source**, so each step appends to what is already there.

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Are the two sequences really identical, or similar? | **Same two callees, same two constants, same argument registers, same order** — five instructions each, differing only in which buffer they name. |
| Is `008F3848` a directory fragment or a filename? | It is `L"\My Games\"`, **with separators at both ends**, and the game-folder string follows it in the same pool with a trailing separator. **A fragment.** |
| Could one of the two be calling the other? | **No** — both call the same two helpers directly, and neither address appears in the other's body. |
| Does this prove there are exactly two builders? | **It does now — and by a different question.** Censusing the path *components* rather than the one address gives **four references from exactly two functions.** *A census of one address is a census of one question.* |
| Is the encoding really UTF-16? | Every second byte is zero across all four strings. |

**What this document does not claim:** what `001F3EA0` returns as a base path, what the file names are
beyond the keymap's first characters, whether the directory is created or only read, or whether any
other subsystem builds the same path by another route.

## And there is a second, dead copy of the strings

**The same strings exist twice.**

| block | contents | references |
|---|---|---|
| `008F384x` | `\My Games\`, `FINAL FANTASY XII THE ZODIAC AGE` | **4 references from exactly 2 functions** |
| `008F316x` | **the same strings again** | **zero references** |

> **The duplication is deeper than two functions with identical instructions — the string data is
> duplicated too, and one copy has fallen out of use entirely.** Whatever produced the second builder
> produced a second copy of its constants with it.

**Bounded the same way as the rest:** this is a census over the function list, so it establishes that
**no *listed* function references the dead copy**, and it cannot see a builder that constructs the path
without using any of these constants.

## Why this document exists

**`008F3848` is touched by exactly two functions.** Both are documented — one in the keymap work, one
across four documents including settings and locale — **and no document cites both.** The duplication
is only visible from the address; **from inside either function it looks like the only builder.**

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Input — CLIENT.** `InputManager_BuildKeymapPath` calls a 43-byte helper this page cites; the keymap path is built with the same helper as the file locations described here.
