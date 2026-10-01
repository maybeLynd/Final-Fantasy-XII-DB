---
system: The five-slot array the console reads
category: 18-Audio
status: AUDITED
owner_layer: PrimaryOwner:Audio
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0020AC30, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: 1 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
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
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# The five-slot array the console reads

**The only candidate the image-base RVA census produced**, and it joins two subsystems that have no
other connection: **the developer console's row renderer and the audio bank-name classifier index the
same array.**

## One array, two readers

```asm
; the console's row renderer
001CD262  movsxd rax, dword ptr [0x01DFE40C]        ; the "currently being set" slot index
001CD269  cmp    eax, 0x4
001CD26C  ja     0x001CD277                         ; out of range -> a fallback value
001CD26E  mov    ebx, dword ptr [rsi + rax*4 + 0x1E632B0]

; the audio bank-name classifier
0020ACD8  cmp    dword ptr [r15 + rsi*4 + 0x1E632B0], 0
0020ACE1  jz     0x0020ACF4                         ; zero entry -> skip
0020ACE5  call   0x0020A760                         ; non-zero -> act on slot rsi
```

**Both address `01F832B0` — the displacement is an RVA and the base register holds the image base** —
**as a dword array indexed by a small integer.** The console bounds-checks at **4**; the classifier
manages **five named bank slots.** *Five entries, one per slot.*

## The console is only safe because of a property established elsewhere

**`01DFE40C` is `−1` at rest.** It holds a slot index **only during a bank-name call** and is reset on
**every** exit path, including the early ones — established independently, from the classifier's side,
before this pairing was found.

**The console reads it with `movsxd` and then compares unsigned against 4.** Sign-extended `−1` is
`0xFFFFFFFFFFFFFFFF`, so **`ja` is taken and the fallback runs.**

> **The console's bounds check is exactly what makes the at-rest `−1` harmless.** Neither function
> knows about the other, and **one of them is safe only because of a property the other establishes.**
> A reader who found the console's `cmp eax, 4` alone would call it defensive; a reader who found the
> `−1` alone would call it a hazard. **It is the pair that makes it a design.**

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Are the two really the same array? | **Same displacement `0x1E632B0` on a register-held image base**, same 4-byte scaling, in both bodies. |
| Is the array five entries or more? | The console bounds-checks **`<= 4`**, and the classifier manages **five** named slots. **Two independent reasons for five; neither alone would fix the count.** |
| Is `01DFE40C` really the index? | It is the operand of the `movsxd` immediately before the bounds check, three instructions above the indexed load. |
| Could the console's fallback mean the array is optional? | The fallback substitutes a register value for the array read; **what that value is is not established here.** |
| Is the base register really the image base? | The census flags this row `base_proven` — **a `lea reg, [rip] -> 00120000` is present in both bodies.** |

**What this document does not claim:** what a slot's dword holds, what `0020A760` does with a non-zero
entry, what the console's fallback value is, or why a debug row renderer reads audio slot state at all.

## Why this document exists

**The image-base RVA census is the one whose addresses the rip-relative census could not see** — the
base sits in a register rather than in `rip` — and **1,023 of its 1,209 addresses were new.** This is
its only pair candidate, and it produced a cross-subsystem safety relationship **that neither function
states and no document had.**

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Resource — SERVICE.** `0020AC30`, owned by that layer, calls this page's `0020A760` at
**`0020ACE5`**. That entry is the slot setter, and its own shape is the page's subject: it stores
the argument into a global immediately (`0020A760`) and then **bounds it at 4**
(`0020A768 cmp ecx, 4` / `ja`), which is the five-slot range this page is about. **The resource
layer selects a slot; it owns nothing here.**

