# EXP-149 (the whole apply-result applier), consumed by the contract owner (OPUS, 2026-09-25)

**Request:** `REQ-OPUS-APPLY-RESULT-WHOLE-FINDINGS` (SWE2-ORACLE). **Body:**
`003112F0 BattleFormula_ApplyTargetResult` (2,040 B). **Contract:**
`07-Combat-Action/CONTRACT-apply-result-to-target.md` (OPUS). The edit follows SECTION-01's merge.

**Evidence classes, kept separate:**

- **NATIVE-REPLAY:** EXP-149, 36/36, stable ×3, published at `5fb38711d`.
- **STATIC:** re-read here. `rbx` is the result record and `rsi` the target unit, per the accesses
  cited.

| EXP-149 finding | owner verdict | static re-read |
|---|---|---|
| the steal table is a **pointer** at `q[rec+0xE60] + 0x32 + 2i` | **CONFIRMED in shape** (read through a pointer, as words, not an inline array) | `00311435 mov rax, [rsi+0xE60]`, then `0031143C movzx ecx, word [r12 + rax]` with `r12 = rax' + 0x31` (`0031142C`). An entry of `0xFFFF` is skipped (`00311441`); each other one goes to `003008A0` with `r9d = 1` (`00311446`–`00311457`). The exact `+0x32 + 2i` indexing is accepted from the replay. |
| `+0x5C` / `+0xDC` are `0030E360` duration / word arguments; mode 3 | **CONFIRMED as arguments** (the "duration" name is accepted at replay scope) | For each set bit `i` of `d[rec+0x54]` (`00311510 bt eax, ebp`): `r9d = d[rec+0x5C + 4i]` (`00311521`, `r15 = rbx+0x5C`), `[rsp+0x20] = movsx w[rec+0xDC + 2i]` (`00311518`, `r12 = rbx+0xDC`), `[rsp+0x28] = esi`, `[rsp+0x30] = 3` (`00311527`), then `call 0030E360` (`0031153A`); a second call at `0031159F` |
| source HP = `d[+0x2C]` bit 7, MP = bit 13 | **the bit roles are CONFIRMED; the HP/MP naming is ACCEPTED at replay scope** | `00311744 mov r9d, [rbx+0x2C]` / `bt r9d, 0xD` / `jae` gates an indirect call (`00311775 call r15`, target selected by bit 2 at `0031176D`). Its flags are `(~(f >> 7) & 0x10) \| ((f >> 10) & 0x20)` (`00311753`–`0031176A`), so bit 7 enters **inverted** as 0x10 and bit 10 as 0x20. |
| KO = bit 0 of `d[+0x64]`, set in `0030E360` mode 3 | **ACCEPTED at replay scope** | No `+0x64` access in `003112F0` itself: the bit is set inside `0030E360`, which this note did not re-read. |
| the I4 landed-gate is confirmed against the real setters | **ACCEPTED at replay scope** | — |

**The EXP-060 / EXP-062 frontmatter ONE-WAYs** are adjudicated at the contract edit, against the
merged text. They are not decided in this note.
