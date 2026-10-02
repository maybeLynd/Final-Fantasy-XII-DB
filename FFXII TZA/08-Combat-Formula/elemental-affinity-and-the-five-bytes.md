---
system: Elemental affinity and the five bytes
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN159 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN159 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: true
  reopened_count: 0
---

# Elemental affinity and the five bytes

`BattleFormula_ApplyActionElementAffinity` at **`0038B6A0`**, 686 bytes. Four documents cited it; none
had opened it.

## What the player sees

**Whether an attack is weak, resisted, absorbed or does nothing at all is decided by five bytes and a
bitwise AND.** The action carries an **element mask** — one bit per element — and the target carries
**four consecutive bytes at `+0x40`, `+0x41`, `+0x42`, `+0x43`, one per behaviour**, each a mask over
the same elements. The attacker carries a **fifth** at `+0x44`.

| test | outcome | recorded as |
|---|---|---|
| `target[+0x43] & element` | **immune — nothing else runs at all** | a global set to 1 |
| `target[+0x40] & element` | **× 2.0** | result flag `0x02` |
| `target[+0x42] & element` | **× 0.5** | result flag `0x04` |
| `target[+0x41] & element` | **absorb** | a separate global set to 1 |
| **source**`[+0x44] & element` | **× 1.5** | result flag `0x08` |

> **Immunity is not a multiplier of zero — it is a branch taken before any multiplier exists.** The
> nullify test is first, and everything else, including the attacker's own bonus, lives in its `else`.

**And the multipliers compose, because none of them is exclusive.** A target that is both weak and
resistant to the same element gets `2.0 × 0.5` — **exactly 1.0**, reached by two multiplications
rather than by a rule saying they cancel. Add the attacker's affinity and it is `× 1.5`.

> **Nothing here decides between the four; each is asked separately and each applies if its bit is
> set.** *Weakness and resistance are not opposite ends of one scale — they are two independent
> masks.*

**Absorb is a flag, not a factor.** It sets a global and does **not** touch the multiplier, so whatever
inverts the result reads that flag downstream — and **a target can be marked absorbing while the
multiplier is still 2.0 from a weakness bit.**

## The evidence

```asm
0038B765  movzx eax, byte ptr [rcx + 0x13]     ; the action's element mask
0038B769  test  byte ptr [rdi + 0x40], al      ; target's WEAK mask
0038B76C  jz    0x0038B803
0038B772  movss xmm0, dword ptr [0x02AEE054]   ; the running damage multiplier
0038B77E  mulss xmm0, dword ptr [0x01CEBC08]   ; x 2.0, from a constant pool
```

**The multiplier is a global, accumulated across the whole formula** — this function multiplies into
`02AEE054` four separate times rather than computing a factor and returning it. **It has no return
value; its entire output is three globals and four bits.**

**The factors are loaded from memory, not encoded as immediates** (`mulss xmm0, [0x01CEBC08]`), so a
modder changing 2.0 to 3.0 is editing a constant pool entry that **other code may share** — the
address is the thing to check, not the instruction.

## Where the answer goes

The three flags are OR-ed into **`*(uint*)(param_3[+0x10] + 0x140)`** — and **`+0x140` is the same
field the result applier reads** when it decides which presentation path a hit takes. Two functions,
read independently, meeting on one dword: **the formula writes the outcome bits and the applier
consumes them.**

**A fourth bit, `0x400`, is set only in one place:** inside the weakness branch, when the target
carries status bit `0x10` in **either** status layer (`+0x6E` or `+0x7E`), the engine calls
`00384B10(element, ctx)` first. **A status that reacts specifically to being hit by an element the
target is weak to** — and it is the only nested condition in the function.

> **That status is id 52**, and this document could not have said so on its own. `+0x6E` and `+0x7E`
> are **byte 6 of the two status layers**, and the layer document's own rule — `byteIndex = n >> 3`,
> `bit = 1 << (n & 7)` — makes bit `0x10` of byte 6 **status id 52**. So the nested condition reads:
> *does the target have status 52, in either layer.*

**And the "three pairs at a stride of `0x10`" reading this document first carried was wrong.** There
are not three offset pairs sharing a stride; **there is one pair of 16-byte layers, and every byte
inside them is `0x10` apart by construction.**

| offsets | byte of each layer | status ids |
|---|---:|---|
| `+0x68` / `+0x78` | 0 | 0–7 |
| `+0x6B` / `+0x7B` | 3 | 24–31 |
| `+0x6E` / `+0x7E` | 6 | 48–55 |

> **One structure, three windows — not three structures sharing a stride.** Three true observations
> that were cheaper and sharper as one, and consolidating them paid out a status id that none of them
> could produce alone.

## The record lookup, repeated five times verbatim

Every test re-derives the element record with the same six-instruction sequence — a global at
`02EBF138`, a call to `0020E600`, a `u16` at `+0x08` scaled by `02AEDFD4`, plus the call's result —
**and then reads the same byte `+0x13`.**

> **Five identical derivations of one value is a non-inlined accessor, not five different lookups.**
> A reader counting "five element reads" would be counting the compiler's work, not the engine's —
> the same species as *a count of call sites is not a count of calls.*

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Are `+0x40 … +0x43` really four fields, or one field read at four offsets? | **Four distinct `test` sites against four distinct displacements on the same base**, each guarding a different consequence. |
| Is `+0x44` on the target too? | **No — it is on `param_1`**, a different base register (`rbp` vs `rdi`), which is what makes it the attacker's affinity rather than a fifth target mask. |
| Is immunity really a short-circuit? | The nullify test wraps **everything else in its `else`** — a single `jz` at the top of the body over the whole remainder. |
| Are the multipliers immediates? | **No** — `mulss xmm0, dword ptr [0x01CEBC08]`. Loaded from a shared constant pool. |
| Does absorb multiply by `-1` here? | **It does not multiply at all.** It sets `02AEDFD0 = 1` and nothing else; the inversion, if any, is downstream and is **not** established by this function. |

**What this document does not claim:** ~~which bit is which element,~~ what `00384B10` does~~, where the~~
~~absorb and nullify globals are consumed, or what the running multiplier at `02AEE054` is initialised~~
~~to and by whom~~. *(answered: the element bits are CONTRACT-environmental-element-scaling.md §3's mask; the absorb and nullify globals are consumed by the finaliser `0038D280`, and `02AEE054` is reset to 0 by `003849B0` at `00384A29` — Scratch-Block/the-formula-scratch-block.md §2.2; 2026-10-02, OPUS)*

## SWE2-EC7-24 update (2026-09-18) — `00384B10` mask-popcount divisor

`00384B10` (273 B) rotates `cl`'s byte mask through `r8d` one bit per step,
`cmovne`-accumulating a popcount with a `cmove` floor of 1, then `idiv` — a
`rand() % popcount(mask)` selector — and re-tests `bt r14d, ebx` per arm for
the element pick. Interior anchor `00384B46` (the first `test r8d, r14d`).
