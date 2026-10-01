# EXP-150 (battle-unit installer), consumed by the contract owner (OPUS, 2026-09-25)

**Request:** `REQ-OPUS-UNIT-INSTALL-FINDINGS` (SWE2-ORACLE). **Contract:**
`04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md` (OPUS).

**What this note does.** It records the owner's verdicts now. The contract text itself is edited
after SECTION-01's overlay of the file is merged (see `section01-owner-review.md`). The request's
block reason covers the edit, not the consumption.

**Evidence classes, kept separate:**

- **NATIVE-REPLAY:** EXP-150, 39/39 cases, stable ×3, on disclosed planted fixtures.
- **STATIC:** re-read here from the shipping image.

## Verdicts

| EXP-150 finding | owner verdict | static re-read |
|---|---|---|
| The spawn-init / flag / tracked block runs only when `b[spawn] & 5 == 0` | **CONFIRMED** | `0023A77B` `rbp` = `00236100(...)`, the spawn record (null → `0023A63A`). Then `0023A791 test byte ptr [rbp], 5` / `jne 0023A84A` skips the block that begins `call 0023AC80` (`0023A7A9`). |
| Count-0 guards: unsigned underflow admits, signed `jg` rejects | **CONFIRMED, with sites** | `+0x50`: `0023A71E movzx eax, word [rsi+0x50]`, `dec ecx` (count−1), `0023A726 jg` → reject, so a zero count (−1) rejects every order. `+0x22` / `+0x24`: `0023A747` / `0023A768 ja`, unsigned, so a zero count (0xFFFFFFFF) admits every value. |
| `00328FF0` writes only when kind ≠ 0 | **CONFIRMED AT THIS CALL SITE; the function's rule is wider** | `00328FF0(i, kind, value)` stores `{value, kind}` to `02EC1380 + i*24` when **(kind ≠ 0 or value < 0) and i < 2** (`00328FFE`–`00329011`). The installer passes i = 0 (`0023A9FB xor ecx, ecx`), kind = `[rsi+3] & 3` (`0023A9FD`/`0023AA01`) and value = `movzx byte [rdi+0xEA9]` (`0023A9EC`, never negative). So **here** kind alone decides. The contract must not state the site's rule as the function's. |
| `002B58B0` is a string/blob walker, not a resolver | **CONFIRMED** | 62 bytes. Null → 0. If byte 0 or 1 is non-zero it returns the pointer unchanged (`002B58B8`–`002B58C1`, `002B58EA`). Otherwise it skips the 2-byte zero header and `edx` NUL-terminated strings, returning the next (`002B58C3`–`002B58E9`). Called at `0023A8E1` and `0023AB5A`. |
| The reset `00236A60` gives combined q0 mask `0xFFEF7FB9FFE7B0E1` on all-ones input | **ACCEPTED at replay scope** | The call is at `0023A5B0`. The mask is an execution result over a planted all-ones image; it was not re-derived statically here. |
| The engaged arms `002FED60` / `002FEDC0` are real, and the stub model is corrected | **ACCEPTED at replay scope** | Not re-derived here. |

## For the contract edit (after the merge)

- §14's three named gaps close as EXP-150 states, with the site citations above.
- The `00328FF0` sentence must carry the function's own rule and the call-site specialisation, as
  in the table.
- Scripted boundaries stay disclosed as EXP-150 lists them: `003220E0`, `00377C20`, `00308010`,
  `003271D0`, `003105D0`, `0023AC80`.
