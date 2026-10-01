# GA-1 — the rest of the `status_data.bin` row, closed

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC plus authored data. Nothing was executed.**
Control: `ga1_open_bytes.py` (5 checks, FAILS 0). It runs `ga1_row_follower.py`, a may-taint follower of status-row
pointers. Detail: [`findings.md`](findings.md) for the bytes, [`kinds.md`](kinds.md) for the lists. Correction
record: [`consumer-check.md`](consumer-check.md).

GA-1's last status left three things open. All three, and one older residue, are answered here.

**1. `+0x11`, `+0x12` and `+0x14`–`+0x1D`: no code reads them.**
- **The follower.** It starts from all 130 references to the registry slot `02EBF118`, in the 18 functions that hold
  one. It follows row pointers through copies, stack spills, jump-table arms, callee arguments (depth 7) and
  row-returning accessors. It reaches 13 row offsets, none of them in the open range (G2). No row pointer is passed
  to a callee or stored outside the stack (G3).
- **The control (G1).** The follower finds the established reads: `+0x20` in `00387CB0`, `003908A0` and `0038FCE0`;
  `+0x08` in `00387730`; and `+0x13` at `0031E241`, which sits in the query filler's jump-table arm that the
  2026-09-15 census missed.
- **The three earlier candidate reads are other records.**
  - `00387D0D` reads the evaluation context.
  - `0031C981` reads an equipment row.
  - `003860DF` reads a 64-byte slot record.
- **No wider access covers the open bytes.** The only multi-byte row reads are dword `+0x0C`, dword `+0x20`, and
  words at `+0x00`, `+0x06` and `+0x0A`.
- **The data.** The twelve columns carry values `{32-n .. 31}` for the *n* statuses each lists (findings, per-offset
  table). They are authored in this build and read by nothing.

**2. Which reader turns `+0x08` into the running timer.** This is already on the
[stats-record field map](../../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md), in
its `+0x0BC` row:
- `00387730` computes the default duration from `status_data` `+0x08`, times the Vitality factor, times the frame
  base (`003877A6` onward);
- the tick's stage 2, `00386C70`, spends it.

**3. Which on-screen list each key feeds** (kinds.md; G4 and G5 re-check it from the bytes).
- **Two index spaces.** `002D02C0`'s kind is `+0x20 + kind`. The cached tables use a listing index L of their own:
  L0 `+0x1500` / key `+0x21`, L1 `+0x1700` / `+0x23`, L2 `+0x1600` / `+0x22`, L3 `+0x1800` / `+0x24`. Citing one as
  the other swaps kinds 3 and 4.

| row key | record | list |
|---|---|---|
| `+0x10` | `+0x20` (kind 0) | the party-member panel's status icons on the menu screens, built by `002D02C0` from `00283E40` (up to 11 icons) |
| `+0x26` | `+0x21` (L0) | a four-slot HUD panel that cycles each slot's status name and icon (`0029A0A0`, `00297D10` pass L0); no page names the panel |
| `+0x27` | `+0x22` (L2) | the target-info window (`002BFD20` passes L2 at `002C01D6`; layout key `TargetInfo`) |
| `+0x13` | `+0x23` (L1) | the status icon above each unit, with its two-digit Petrify / Doom count (`002C6F70` → `00273160`, `+0x1700`) |
| `+0x02` | `+0x24` (L3) | **no on-screen list**. No caller selects L3. Only the battle reaction queue `003BBD00` reads it: `0xFF` means no reaction |

**4. The `+0x0A` word's consumer** (open since the 2026-09-18 narrowing). The status arm of the query filler reads
the word at `0031E288` and passes it to `002F9860`, the text-id lookup (id / 1000 → group). It stores the result
in the query record's `+0x10`. So `0x2EE0 + id` is used as a text id. The 2026-09-18 text cited `0031C81A` as the
reader and said "not a string-pool key"; both are corrected in the consumer check. Which string each id resolves to
was not resolved here.

**Also from the data:** the runtime table is not only the four loose `status_data.bin` copies. All nine
`test_battle/*/binaryfile/battle_pack.bin` copies embed it byte for byte, at the header's `+0x40` offset, which
`00236D91` binds to the slot.

**Not established:**
- the name the game gives the four-slot HUD panel;
- the text each `0x2EE0 + id` resolves to.

Neither is part of GA-1's question.
