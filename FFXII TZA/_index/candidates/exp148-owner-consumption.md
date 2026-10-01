# EXP-148 (the apply-result applier's five callees), consumed by the contract owner (OPUS, 2026-09-25)

**Request:** `REQ-OPUS-APPLY-RESULT-CALLEES-FINDINGS` (SWE2-ORACLE). **Contract:**
`07-Combat-Action/CONTRACT-apply-result-to-target.md` (OPUS). The contract edit follows SECTION-01's
merge (`section01-owner-review.md`). The verdicts are recorded now.

**Evidence classes, kept separate:**

- **NATIVE-REPLAY:** EXP-148, 43/43 cases, stable ×3, on shipped bytes, scripted boundaries
  disclosed.
- **STATIC:** re-read here.

| callee | EXP-148 finding | owner verdict | static re-read |
|---|---|---|---|
| `0030E130` (553 B) | a four-mode status-bit modifier that calls `0030FED0` only when flags bit 9 is clear, gated by the class-29 validator | **bit-9 gate CONFIRMED**; the modes and the validator gate are **ACCEPTED at replay scope** | `0030E183 mov r12d, r9d` (flags), then `0030E31C bt r12d, 9` / `jb 0030E32E` skips `0030E329 call 0030FED0`. The byte at `[rbx+0x78]` is tested and rewritten at `0030E1C9`–`0030E239`. |
| `0030FED0` (1,787 B) | a 128-bit recompute from `+0x50`/`+0x54` (+ member `+0xE80`); dispatches `0030E130` with `flags \| 0x202`; `0030E360` per set bit of member `+0xE90`; copies the bitmap to `q[member+0x6A0]+0x78`; partial null-guard | **`\| 0x202` and the `+0xE80` test CONFIRMED**; the rest is **ACCEPTED at replay scope** | `0030FEFB or r15d, 0x202`, passed as `r9d` to `0030E130` (`00310363`/`00310378`, `00310384`/`00310396`). `00310047 test byte ptr [r9 + r10 + 0xE80], r8b`. `00310303 lea r9, [rbx+0x78]`. |
| `0030C650` (570 B) | a level/growth writer clamped at 99 | **CONFIRMED** | `0030C65B mov eax, 0x63`; `0030C6CC cmp byte [rdi+0x1C2], 0x63`; `0030C7AE`/`0030C7B5` clamp against 0x63; recompute via `0030C7CE call 0030FED0` |
| `003008A0` (734 B) | an item write with category unlock flags OR'd into `d[q[02EBF190]+4]` only when `r9d == 1` and resolver ≤ 0 and effective > 0 | **CONFIRMED, with the flag map** | Gate: `00300968 cmp r14d, 1` / `jne` (`r14d` = `r9d`, `003008B4`); `00300972 test ebp, ebp` / `jg` (`ebp` = `00309F30(...)`, `0030093C`); `0030097A test esi, esi` / `jle` (`esi` = the callback's result, or `ebp`). Flags by `category = id >> 12`: 3 → `\|= 1` (`003009F7`); 4 → `\|= 0x40` (`003009E7`, the `sub ecx, r14d` arm with `r14d` = 1); 12 with id `0xC000..0xC011` → `\|= 0x80` (`003009D4`); `0xC012..0xC01E` → `\|= 0x100` (`003009C1`). |
| `00316A50` (411 B) | a descriptor-driven field writer (table `00D10460`); modes 2 and 4 clamp to `0x7FFF` / `0x7FFFFFFF` | **CONFIRMED** | `00316A7A lea r14, [image base]`; descriptors at `[r14 + rbp*8 + 0xBF0460]` = `00D10460`, 8 bytes each (`+0` kind byte `00316A81`, `+2` byte, `+4` dword bound `00316AA6`); clamps `00316B8B`/`00316B96` 0x7FFF and `00316BA9`/`00316BB4` 0x7FFFFFFF |

**For the contract edit (after the merge):** restate §13 with these site citations. Carry
`003008A0`'s four-flag category map, which the EXP-148 summary compresses into "category unlock
flags". Keep the scripted boundaries EXP-148 disclosed.
