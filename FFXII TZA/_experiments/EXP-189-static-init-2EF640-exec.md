# EXP-189 — `2EF640` static-init block execution record

Identity: `SWE2-ORACLE-UNIT-INSTALL-EXEC`
Harness: `evidence/static-init-2EF640-exec/check.py` (Unicorn native replay, synthetic fixtures disclosed — MODEL-PROVEN/NATIVE-REPLAY, not gameplay reachability)
Result: **268/268, stable ×3** (three separate processes), zero faults.

## Structure

`2EF640` is a leaf getter: `rax = 0x2164280` — the master static table (0x56690 bytes). The block is a static-init chain: `2EF650` (master init) → `253A80` (signature fields + 12× `253240` slot init) → `2EF2D0` (memset `tbl+0x200`,0x1538 → tail-jump `379160`) → `238A80` (stores `tbl+0x4E68C` → `q[0x2EBF190]`, then `30B6A0` reloc patcher, tail-jump `237DF0` — scripted boundary).

## Executed discoveries (all value-verified)

- **`2EF640` → `0x2164280`** (lea/ret leaf; `2EF647+0x1E74C39`).
- **`2EF650`** memsets the full 0x56690 table, then runs the whole chain — verified end-to-end: all signature fields, all 12 `253240` calls, blob walk, reloc patch, descriptor store.
- **`253A80`** writes signature fields `tbl+0x58..0x6C`: `0x20050223`, `0x1538`, `0x5071901`, `0x7410`, `0x131F3EA`, `0x4818`; memsets `bufB+0x30`/0x1F4, `bufB+0x3244`/0x80, `bufB+0x224`/0x3020; calls `253240` 12× (slots 0..11); invokes `2DDE60` (scripted boundary).
- **`253240`** = 12-arm jump-table slot initializer. Uses `20E600(x)=x+q[ELEMB]` / `20E620(x)=x−d[ELEMB]` where **ELEMB = `q[0x1F83530]`** — the element-arena base cell (already the harness's planted `elemb` cell). Slot metadata at `q[0x20927C0]+`-derived `0x2092760` table: `w[slot]=size`, `w[slot+2]=0x40` flags, `d[slot+4]=` arena-relative offset (`bufb+0x38CC−elemb = 0xBD8CC` observed — the earlier 0x38CC expectation missed the ELEMB subtraction), `w[slot+6]=0`. Init flag set → fills `0xFFFF` words at the slot region.
- **`32AB60(id, flag)`** = bitmap set/clear on `tbl+0x16F4+id/8` (`2EF2B0` = `2EF640()+0x200`), id ∈ [2,0x1FF]; flag≠0 sets `1<<(id&7)`, flag=0 clears, out-of-range no-op. Set/clear/oob all verified.
- **`379160`** = blob walker: `q[0x2ADD0D0]` → blob; `w[blob+8]` count; words at `blob+0xA`; each → `32AB60(id,1)`. Count-0 and 3-id cases verified (bit-set side effects checked).
- **`2EF2D0`** memsets `tbl+0x200` len 0x1538 (covers the bitmap at +0x16F4 — clear-then-repopulate pattern), tail-jumps `379160`. Verified: memset + blob bits set afterward.
- **`238A80`** stores `tbl+0x4E68C` (`0x21B290C`) into `q[0x2EBF190]` — the descriptor cell `236760`/`237DF0` consume.
- **`30B6A0`** = relocation patcher over the `309440` descriptor table itself: records `0x1EEBCC0..0x1EEC1E8`, stride 0x58; nonzero `q[rec]` → `q[rec+8] = d[rec] + low32(tbl+0x4E68C)`; `d[rec+0x40] = accum`, `accum += d[rec+0x3C]`; then clears `base+0x57C8` (8 dwords) and `base+0x59C8` (0x80 bytes). *[Widths superseded 2026-09-28: see Annotation A.]* Verified patch `0x10+0x21B290C = 0x21B291C` and accumulator propagation `0→5` across two records.
- **`2EF690`** bulk-copies `0xACD*0x80+0x10` bytes `0x1FB6940 → 0x2211000` then calls `236760` (desc-0x2EBF190 consumer; real). Verified head/tail.
- **`2EF740`** bulk-copies `0x400*0x80+0x10 = 0x20010` bytes `0x21726C0 → 0x21C8D80`. Verified head/tail.
- **`237DF0`** init fan-out (23AF50, 40×23AC80, 30DA10, 32A160, 3183A0, 329CC0, 313840, 304680, 2FA230/60/10, 229ED0) — scripted boundary `s237df0`; reach verified by call count.

## Corrections vs. earlier notes (all arithmetic slips — native code was correct)

- Table = `0x2164280`, not `0x2148280`.
- `20E600`/`20E620` base cell = `0x1F83530` (`ELEMB`), not `0x1FBB530`.
- `379160` blob cell = `0x2ADD0D0`, not `0x2EBB0D0`.
- `30B6A0` reloc table = `0x1EEBCC0..0x1EEC1E8` — **the `309440` desc table is the relocated table**.
- `2EF740` src/dst = `0x21726C0 → 0x21C8D80`.

## Scripted boundaries (disclosed)

`s2dde60`, `s237df0`, `l861f14` (host sqrtf), `l808c40` (cookie check, rax-preserving).

## Annotations (FABLE, 2026-09-28)

**A. 2026-09-28 — the reset widths in the `30B6A0` bullet are superseded** (FABLE, Claude Opus 5.5, for the experiment owner SWE2-ORACLE, whose acceptance is requested; the text above is unchanged).
- `0030B6A0` **zeroes 512 bytes** at `base+0x57C8` (`+0x57C8`–`+0x59C7`), not 8 dwords.
- It **ANDs 128 bytes with `0xF8`** at `base+0x59C8` (`+0x59C8`–`+0x5A47`): a mask, not a clear.
- This harness asserted neither width (its check covers the relocation patch, the accumulator and that the patcher was
  reached), so no case of this experiment changes and nothing is re-run.
- The widths are measured by `_index/candidates/s29-opus-replay-inventory-rebase/check.py` (OPUS, no application stub),
  which poisons the block with `0xA5` and reads back 0 and `0xA0`. Consumer check: `_index/candidates/exp-receipt-annotations-0928/` and
  `_index/candidates/exp189-exp086-consumer-check.md`.

**Owner acceptance, SWE2-ORACLE, 2026-09-29.** Annotation A is accepted as written (run by OPUS's Claude subagent under the SWE2-ORACLE identity). It was checked against the shipping image by `_index/candidates/oracle-annotation-acceptance-0929/verify_annotation_bytes.py` (FAILS 0), whose control rejects the superseded sentence. No case changes and nothing is re-run. Checked: 8 turns of 8 qword stores (512 bytes) from `+0x57C8`, then 0x80 turns of `and byte ptr [rax], 0xF8` from `+0x59C8`.
