# SWE2-AUDIT-SPEC review of SD-168 (sd168-arena-tail-bytes-0930, OPUS, d9806dfff): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed: OPUS's
`d9806dfff`, the [README](../sd168-arena-tail-bytes-0930/README.md) and `sd168_tail.py`. First half measured at HEAD
`9b6c5bc93`, resumed and finished at HEAD `b58c633f7`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD168-0930 | sd168-arena-tail-bytes-0930 | `d9806dfff` | ACCEPT |

**Re-run.** [rerun_sd168_tail.out](rerun_sd168_tail.out) is identical to the committed `sd168_tail.out` (CR ignored),
T1/T2 PASS, `FAILS 0`. The package dir is clean.

**Re-derived independently** ([sd168_pair.py](sd168_pair.py) / [.out](sd168_pair.out); the boot routine's linear dump is
[boot_0022A0B0.dump](boot_0022A0B0.dump)). Tools: arena_ix and adump only.
- **T1, pairing rather than set membership.** T1 tests `size + count in allocs`, so on its own it could pair the wrong
  allocation with an initializer. I paired the two exactly instead:
  - Each `0036D240` result in `0022A0B0` is stored to its own global (`01FD49F0..01FD4A40`, `01FD4A90`). Each
    `00369D30` call loads its `rdx` from one of those globals.
  - The code between the stores and the loads is straight-line, and its only calls are `0036D240` and `00369D30`.
  - All **9 of 9** initializer calls get the allocation of exactly `size + count` for their own heap (2, 3, 4, 5, 6,
    7, 8, 9, 0xB), with the sizes and counts in the README's table.
  - The two extra allocations are not backings in this routine: `0x80000` goes to `01FD4A20` and `0x100000` to
    `01FD4A90`.
  - `0036D240` is `movsxd rcx, ecx; or r8d, -1; xor edx, edx; jmp 0x85e730`.
- **T2, the layout** (`00369D30`, read in full).
  - The header is the 8 qwords cleared at the backing.
  - `+0x20 = align64(base + 0x7F)` (`00369E73..7E`). Then `+0x28 = align64(+0x20 + pages/32·8)`. Then
    `r10 = align64(+0x28 + pages·8)`, where `pages` = ⌈size / 64 KiB⌉ rounded up to 32.
  - If `count` ≠ 0: `+0x30 = +0x40 = r10` and `+0x38 = r10 + count·16` (`00369EB7 shl rax, 4`), then r10 is aligned
    again.
  - The data start is `+0x10 = r10`. The length is `+0x5C = (size − (r10 − base))` rounded down to 64
    (`00369F5D..88`). So the data end is at or below `base + size`.
  - The one initial free block is written by `0036A490` at the data start (header at `+0x00..+0x3F`), with payload
    length `+0x5C − 0x40` (`00369FD0`, `0036A50F`). It ends exactly at the data end.
  - Nothing in the initializer records `size + count`, and no field points past `base + size`.
- **Independent corroboration** (the other four callers of `00369D30`):
  - `0037B3D0` re-creates heap 0xB with count **0x100**. Its backing is allocated at exactly `size`, not `size + count`
    (`0037B41E mov ecx, ebx; call 0x36d240`, then `r8d = ebx`, `r9d = 0x100`).
  - `0025A990` (heap 0xD, 0x100000) and `0025AA30` (heap 0xE, 0x19000) initialise their backings at exactly `size`.
    So does `003E9AA0` (heap 0xC, `edi`). All three pass count 0.
  - A heap with a 256-slot handle table therefore runs with no tail at all. That supports the README's point that the
    `+ count` bytes are not needed by the arena's layout.

**Controls.** The defect the pairing check is sensitive to is an initializer given a backing of a different size. That
would show as `False` in P1, and the `0x80000` / `0x100000` allocations, which do not match any pair, are the negative
examples. T2's nine instruction texts all re-read the same in my dump.

**Citations checked.** `0036D249`, `00369EB7`, `00369EBE`, `00369F5D`, `00369F65`, `00369F6C`, `00369F85`, `00369F88`,
`00369D3E` and `00369D41` each say what the T2 sentence says.

**Runtime routing.** None. The README's two limits are correctly stated as limits:
- A foreign pointer into the tail is a dynamic address, which no static census can exclude.
- The page rounding of `0085E730` is unread.

**Correction wording:** none needed. Optionally add the `0037B3D0` corroboration: heap 0xB re-created with count 0x100 on
a backing of exactly `size`.
