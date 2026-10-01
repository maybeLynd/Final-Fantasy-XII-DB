---
system: The basis-column helpers
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: CodeDomain — no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 3 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: false
  reopened_count: 0
---

# The basis-column helpers

`0062DDE0` (458 B) and `0062DFB0` (517 B). **Cited by no document in this database.** They are the top
two entries of the SSE-density ranking — **72 % and 69 % SSE moves, zero backward jumps** — and they
are the purest instance of the shape that ranking was built to find.

## The whole semantic content is one line

**`0062DDE0` does this and nothing else:**

```
C -= B * t
```

**`0062DFB0` does this and nothing else:**

```
C += A * b  +  T * a
```

**Everything else in both bodies — well over four fifths of the instructions — is a copy of the
structure into scratch fields and a copy back.**

> **That is why the SSE column found them before anyone opened them.** A function that is almost all
> `movss` with no loop is not doing work; **it is moving a structure around one line of arithmetic.**

## The layout the two functions agree on

Twelve floats at `+0x08 … +0x34`, in **three groups of four**, and **the fourth element of each group
is not part of that group**:

| | x | y | z | fourth |
|---|---|---|---|---|
| `+0x08` | `A.x` | `A.y` | `A.z` | `T.x` |
| `+0x18` | `B.x` | `B.y` | `B.z` | `T.y` |
| `+0x28` | `C.x` | `C.y` | `C.z` | `T.z` |

**`0062DFB0` proves the fourth column is a vector rather than three per-row scalars**: it multiplies
`+0x14`, `+0x24` and `+0x34` by **one** parameter and adds them to `C.x`, `C.y` and `C.z`
**respectively** — *they are used as a coherent triple.*

**Both functions save those three fields to scratch first and restore them last**, unchanged — because
the scratch copy writes **zero** into the fourth slot of each group and the write-back would otherwise
destroy them.

```asm
0062DE6E  mov   dword ptr [rcx + 0x44], eax   ; the scratch fourth slots are zeroed
0062DE80  mov   dword ptr [rcx + 0x54], eax
0062DE94  mov   dword ptr [rcx + 0x64], eax
```

> **The save/restore exists because the copy is destructive, not because the values change.** A reader
> who assumed those three writes meant the fourth column was being *modified* would have it exactly
> backwards.

**And `0062DFB0` reads the saved fourth column back as a `movups` of all four slots at once**, then
broadcasts components out of it with `shufps` — which is the clearest evidence in either body that the
three fourths are one vector:

```asm
0062E07C  movups xmm6, xmmword ptr [rcx + 0x38]   ; the saved fourth column, as a unit
0062E080  movups xmm5, xmmword ptr [rcx + 0x48]   ; column A, as a unit
0062E08C  mulss  xmm1, xmm12                      ; x the first parameter
0062E094  shufps xmm3, xmm5, 0x55                 ; broadcast .y
0062E09E  shufps xmm5, xmm5, 0xAA                 ; broadcast .z
```

**Three separate scalars would never be loaded with one `movups` and then shuffled apart.**

**And the negation is free:** `0062DDE0` computes `C − B·t` by negating the parameter through
`xorps xmm12, [01CEBDA0]` — a sign-mask constant — and then **adding**, so the body contains no
subtract at all.

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the fourth column really one vector, or three unrelated scalars? | **`0062DFB0` scales all three by the same parameter and adds them to the three components of one column.** Three scalars would not be used that way. |
| Are the scratch fields part of the structure or a caller's buffer? | They are **at fixed offsets on the same pointer** (`+0x38 … +0x74`), written and read within the body — **the structure carries its own scratch.** |
| Could the save/restore mean the fourth column is modified? | **No** — it is written back **byte-identical**, from the same scratch slots, with nothing between. **The zeroing of the scratch fourths is what makes the restore necessary.** |
| Is `xorps` against a constant really a negation? | It is applied to the scalar parameter, and the subsequent arithmetic is an **add** whose result the decompiler renders as a subtract. **Two representations of one operation.** |
| Do the two functions share a layout, or is that an assumption? | **Both save exactly `+0x14`, `+0x24`, `+0x34` and both use `+0x48 … +0x70` as scratch** — the same offsets in the same roles, in two independently compiled bodies. |

**What this document does not claim:** what the structure is, what `A`, `B`, `C` and `T` mean, who
calls either function, or what the two parameters of `0062DFB0` represent. **Nothing in the database
cites either address**, so `0062DDE0` and `0062DFB0` have no caller context to draw on — this is a description of an
operation and a layout, not of a purpose.

## Where the layout comes from

**`00189130`** (642 B, **68 % SSE, zero loops**) **writes into exactly this layout**, and the reshuffle
in its epilogue is the proof:

```asm
00189340  movss  xmm12, dword ptr [rax]        ; the product's first three floats...
00189345  movss  xmm13, dword ptr [rax + 0x4]
0018934B  movss  xmm14, dword ptr [rax + 0x8]
00189351  movups xmm8,  xmmword ptr [rax + 0x30]
0018935E  mov    rax,   qword ptr [rbx + 0xb8] ; ...into the destination matrix
```

**The product it computes keeps its translation in the first three floats.** The destination does not:
those three are written **individually into `+0x0C`, `+0x1C` and `+0x2C`** — **the fourth slot of each
of the three rows** — while the twelve remaining floats go in as three contiguous rows.

> **That is the interleave this document describes, performed.** A translation vector taken from one
> place and scattered into the fourth component of three rows is **the layout being constructed**, and
> it independently confirms the reading taken from the two helpers.

**What it builds:** a fixed base with **`1, −1, −1`** on the diagonal, composed with **three
axis-angle rotations in a fixed order** — two about one axis, one about another, from three separate
angle parameters — through a shared 4×4 multiply. **Two of the three rotations are built by a helper
from an axis vector; the middle one is written out by hand** from `sinf`/`cosf`, with the sine negated
by an XOR against the sign bit rather than a subtract.

**Two components of the previous matrix are read at entry and carried into the base**, so the result is
**not built entirely from the three angles** — a caller cannot reproduce it from the parameters alone.

## Why it is here

**The SSE-density ranking was added to find functions the database had *mis-typed*.** Its top two
entries turned out to be functions the database had **never mentioned**, and both are the predicted
shape exactly: **a structure snapshotted, one line changed, written back.**

> **A ranking whose first two picks match its own stated prediction, on functions nobody had looked
> at, is a ranking that can be pointed at the rest of the list.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Presentation — CLIENT (1 edges, one fan-in).** All 1 edges are Presentation bodies reaching `00189130` on this page. `FUN_00187950` is the worked example - it is a 3,311-byte routine in a `0x70`-byte frame with a stack cookie, an unwind marker and one preserved SSE register. The crossing is **one shared subject with 1 callers on that layer**, not 1 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-36 update (2026-09-19) - `00189130`

`00189130` (642 B) is a basis-column helper - `008C5F80`-`008C5FC0`/`01CEBC9C` rdata run, `00185100` triple plus `00188E60`/`00861F0E`/`00861F08`. Interior anchor `001891F1` (an `00185100` call).

## SWE2-EC7-52 update (2026-09-19) - `00185100`

`00185100` (951 B) is a call-free 4x4 matrix product - `out[rdx] = [rcx] x [r8]`, sixteen `shufps`-broadcast `mulss`/`addss` chains, four `movups` rows out (the `00189130` basis-column helper calls it triple). Interior anchor `00185208` (the second-operand row load).

## SWE2-EC7-53 update (2026-09-19) - `00188E60`

`00188E60` (413 B) is a basis-column helper - `00861F08`/`00861F0E` plus `008C5FD0`/`01CEBBA8`. Interior anchor `00188E97` (a `00861F0E` call).


## SWE2-EC7-111 update (2026-09-20) - `0018D320` measured

`0018D320` (28 B) is the
paired out-param getter
`00187950` and `001CD0E0`
run: a non-null `rdx`
receives `dword[+0x168]`, a
non-null `r8` receives
`dword[+0x16C]` - either
output may be declined
independently.
Interior anchor `0018D325`
(the `+0x168` read).
The two callers' own fan-out
is mechanical and recorded
here: `00187950` reaches the
Audio domain, `001CD0E0`
reaches the
PlatformOnlineAchievements,
Resource and WorldAreaField
domains - shared-service
edges, not basis-column
subjects.
