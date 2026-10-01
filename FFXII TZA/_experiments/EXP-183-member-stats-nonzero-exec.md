# EXP-183 — `2FEF30` member stat computation, nonzero verified

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixture on the exact
shipping EXE, SHA256 73461D08…97f8). Closes the EXP-171 disclosure: the
member-arm stat math is now proven with **nonzero** planted tables —
every output field asserted against a hand-computed expected value.

Harness: `Temp\exp166_check.py` — **240/240, stable ×3**
(`t2fef30-nz`, direct entry `0x2FEF30`).

## `2FEF30(rec, out, slotlist)` — member stat computation

Head: rdi=rec, rsi=out (null → `rec+0x24`), rbx=slotlist (null →
`rec+0x50`). `d[rsp+0x3C] = b[rec+5]` selects the HP cap; `b[rec+5]!=0`
(member) → the four-desc arm at `0x2FF0E1`.

### Row resolution (EXP-171 structure, now value-verified)

| reg | desc | index field | role |
|-----|------|-------------|------|
| r13 | `q[0x2EBF120]` | `b[rec+4]` | member row |
| rbp | `q[0x2EBF148]` | `w[r13+0x22]` | **base stats** |
| rbx | `q[0x2EBF140]` | `w[r13+0x24]` | **per-level growth** |
| r11 | `q[0x2EBF150]` | `w[r13+0]` | resist/aux bytes |

### Stat formula (delta = `b[rec+0x1C2] − b[rec+0x88]`)

Per stat: `growth[k]*delta + base[k] + w[rec+field]`, then clamped.

- `d[out+0]` HP = `d[rbx+0x20]*delta + d[rbp+0x20]` + license adds,
  clamped `[1, 9999]` for members (`d[rsp+0x3C]!=0` → 0x270F; else
  0x3B9ACA00 = break-HP-limit). Verified 50*5+1000 = **1250**.
- `w[out+4]` MP = `w[rbx+0x24]*delta + w[rbp+0x24]`, cap 999.
  Verified 4*5+100 = **120**.
- `b[out+6..9]` = stats (+0x26..+0x29 pairs vs rec `w+8/+0xA/+0xC/+0xE`),
  cap 99. Verified 45/52/59/66.
- `b[out+0xB]` = stat +0x2B vs `w[rec+0x12]`, cap 255 → 80.
- `b[out+0xC]` = stat +0x2C vs `w[rec+0x14]`, cap 255 → 87.
- `b[out+0xD]` = stat +0x2A vs `w[rec+0x16]`, cap 100 → 73.
- `b[out+0xA]` = `w[rec+0x10]` + (member-row `b[r13+0x15]` **bit0** arm:
  `b[rbx+0x2D]*delta + b[rbp+0x2D]`), cap 255 → 89.
- `b[out+0xE]` = `w[rec+0x18]` + (bit1 arm: `b[rbx+0x2E]*delta +
  b[rbp+0x2E]`), cap 100 → 86. `b[out+0xF]` = `w[rec+0x1A]` +
  (`b[rbx+2]*delta + b[rbp+2]`) → 63. `b[out+0x10]` = `w[rec+0x1C]` +
  (`b[rbx+3]*delta + b[rbp+3]`) → 70.
- `b[out+0x11]` = `w[rec+0x1E]` + out+0xF + out+0xE + out+0xD
  intermediates (s20+s24+s50), cap 100 — verified **clamp**: 243→100.
- `b[out+0x12]` = `w[rec+0x20]` + out+0x10 intermediate, cap 100 → 92.
- `b[out+0x13]` = min(`d[rsp+0x60]`, 3); `rsp+0x60` only written on the
  non-member path → members get 0.
- `b[out+0x1C..0x20]` = `b[r11+0x2C,+0x29,+0x2A,+0x2B,+0x2D]` —
  **non-sequential order** (0x2C first, 0x2D last). Verified
  0x44/0x11/0x22/0x33/0x55.

### Loops (skipped cleanly with zeroed lists — disclosed)

- Equipment loop ×5 over `w[slotlist+i*2]`: `322C50(slot,6)` —
  `slot==0` → ret 0 (`slot-1 > 0x1F` unsigned) → skip. Body resolves
  `q[0x2EBF130]`-family elem `(slot−0x1000)*stride`, `31E9A0` kind
  dispatch (1/2/3 arms add to HP/stat slots), then 8× `e600` ORs into
  `out+0x14/+0x18` and `b[out+0x1C..0x20]`.
- License loops ×3 over static bit tables `0x1DF0290/0x1DF02A0/
  0x1DF02B0` (0x10/0x10/0xC entries): bit set in `rec+0x68` or
  `rec+0x78` bitmap → resolve desc → `w[elem+4]` added to r12/r13/r14
  (stat1/stat2/HP). Zero bitmaps → all skipped.
- `322C50` itself: jump-table on `ecx-1` (≤0x1F) — slot-0 returns 0.

### Corrections vs the read

- My first expected values had arithmetic slips (native was correct).
- `rsp+0xD0` in the license loops = the entry-frame saved `rcx` = rec —
  not garbage.
- Non-member arm (`b[rec+5]==0`, `b[rec+4]−0x1B ≤ 0xC`) uses a
  different path (`2F8E50`/`2F9180` HP/MP formulas, floats at
  `rec+0x10..0x20`) — not covered here.
