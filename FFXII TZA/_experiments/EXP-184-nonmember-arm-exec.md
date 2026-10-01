# EXP-184 — `2FEF30` non-member arm; `2F8E50`/`2F9180` un-stubbed

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the
exact shipping EXE, SHA256 73461D08…97f8). `2F8E50`/`2F9180` were pure
leaf arithmetic — removed from the SCR boundary and now execute real.

Harness: `Temp\exp166_check.py` — **243/243, stable ×3**.

## `2FEF30` non-member arm (`b[rec+5]==0`, `0x2FF02E`)

Resolves ONE row: desc `q[0x2EBF130]`, idx `b[rec+4]` →
`elemb + d[desc+0xC] + w[desc+8]*idx` (same desc read thrice:
null-gate, base, stride).

- **HP** = `2F8E50(d[rec+8], b[row+0x19], b[row+0x18])`
  = `(b18+1) · d[rec+8] · b19 / 100` — magic-multiply
  (`0x51EB851F`, sar 37) — verified 8·100·9/100 = **72**.
- **MP** = `2F9180(w[rec+0xC], b[row+0x1D])` = `ecx·edx/100`
  — verified 80·11/100 = **8** (floor).
- `b[out+6..9]` = `cvttss2si` of `f[rec+0x10/+0x14/+0x18/+0x1C]`
  — rec holds **float** stats for non-members (trunc toward zero):
  12.7→12, 34.9→34, 56.5→56, 78.1→78.
- `b[out+0xD]` = `b[out+0x11]` = `b[row+0x2A]` (cap 100).
- `d[out+0x14] |= d[row+0x4C]`, `d[out+0x18] |= d[row+0x48]` —
  status-immunity bitmask ORs from the row.
- `b[out+0x13]` = min(`b[rec+0x20]`, 3) — verified 5→3.
- `b[out+0xA..0xC]`, `+0xE..0x10`, `+0x12`, `+0x1C..0x20` = 0
  (scratch slots zeroed pre-arm; no member tables).

## HP cap semantics (corrected)

`d[rsp+0x3C] = b[rec+5]` → `edi`: **non-member → cap 9999**;
**member → cap 999,999,999** (0x3B9ACA00 — break-HP-limit class).
Separately `b[rec+4]−0x1B ∈ [0,0xC]` sets `d[rsp+0x5C]` → a second
write clamps HP to **0x7FFF (32767)** — and can *raise* it past the
first clamp since it re-reads the raw pre-clamp value. Verified:
- `b4=2` → `d[out]` = min(3,264,000, 9999) = **9999**.
- `b4=0x1B` → second clamp → `d[out]` = **32767**.

## Fixture collision found

`nmdesc` off `0x20000` overlapped `O_FOE` — the foe-row defaults
(`w[+0xA]=0x501`, `w[+0xC]=0x502`, `w[+0xE]=0xFFFF`) clobbered the
planted `+0x48/+0x4C` dwords. Moved to `0x60000`. Symptom was
visible in-memory (`d[row+0x4C]` = `0xFFFF0502`) — the read-trace
plus memory dump located it in one pass.

## Notes

- `w[rec+8]` is a **word** stat on the member arm but `d[rec+8]` a
  **dword** on this arm — same bytes, different interpretation.
- The member arm writes `out+0x1C..0x20` from the r11 row; this arm
  leaves them zero.
