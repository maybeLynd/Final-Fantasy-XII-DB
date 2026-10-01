# SWE2-AUDIT-SEM review — FRONTIER's pass-22 crossing section on CONTRACT-defeat-rewards-sequence.md (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FRONTIER-REQ-AUDITSEM-REVIEW-DEFEAT-CROSSING-0930` |
| reviewed | `4032e34d4` (author **SWE2-FRONTIER**) — the section "Cross-subsystem neighbours - FINAL-AUDIT pass 22, the falsification pass's new cites"; OPUS's falsification table above it is not in scope |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** |

## 1. Audio — SERVICE (SWE2-AUDIT-SEM)

[`defeat_own.py`](defeat_own.py), [out](defeat_own.out).

- **The call chain.** The recipient walk calls `0030C650` at `003124A3`. Then:
  - `0030C831` `mov ecx, 7` and `0030C836` `call 003A1180`;
  - `0030C83B`–`0030C83E` skip when the result is −1;
  - `0030C840`–`0030C84B` call `002DF220(id, 0x40, 0x7F)` (`r8d = rdx + 0x3F`).
- **`003A1180`.** It returns −1 when `00267330(0)` is non-zero. Otherwise it validates the packed handle it loads
  against its table entry and returns `(bankWord << 9) + 7` (`003A11D7`–`003A11DC`). "Resolves the current packed
  sound-bank handle to a sound id" is right.
- **The level-up attribution.** It is properly attributed. `CONTRACT-battle-unit-construction.md` line 383 says "The
  level-set plays the level-up sound when it finishes", and `what-happens-when-a-character-levels-up.md` §6 calls it
  the fanfare. The paragraph does not assert this itself.
- **"No audio state feeds back into the award."** The one value that comes back is `002DF220`'s return. `0030C850`–`0030C857`
  hand it to `00329210(1, h)`, which stores it in slot 1 of the array at `0208D328`. That array is referenced from
  `002339CC`, `0031B4F8`, `0031EB13`, `00328D98`, the stores at `00322192`–`003221A7`, and `00329213`. None of those is
  in the award body `00312280`. So the sentence holds.

  The paragraph does not mention this handle store. That is an omission, not an overstatement.

**SERVICE** is right: the sequence calls into Audio, and Audio returns nothing the award reads.

## 2. Save_Load_Settings — CLIENT (SWE2-AUDIT-SEM)

- **The getter.** `00236780` is `mov rax, [02EBF190]; mov eax, [rax+4]; shr eax, 0xE; and eax, 1; ret`, which is
  17 bytes and bit 14 of the dword at `+4`, as stated.
- **Its callers.** It has three: `00312429` and `00312505` in the award body (DR-2's test at `00312505`–`00312513`,
  `cmovne edi, ebp`), and `00583F67` in `00583D60`.
- **The header write.** `00583F67`–`00583F70`: when the bit is set, `or byte [rdi+0x57], 4`. Beside it, `00236760` and
  `00236740` set bits 0 and 1 of the same byte (`00583F5A`–`00583F7D`).

**CLIENT** is right. The save finaliser reads the flag and writes only its own header.

## 3. Strongest counterexample tried (SWE2-AUDIT-SEM)

I looked for a path by which audio could influence the award. The one returned value, the play handle, goes to a global
slot that the award body never references. None was found.
