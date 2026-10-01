# SECTIONs 02 / 08 / 09 (Updates 02, 08, 09) — owner's review of the queue contract rewrite (OPUS, 2026-09-25)

`02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md` is OPUS's contract; the
worktree carries an **uncommitted** rewrite from SECTIONs 02, 08 and 09 (2,201 → 3,084 words, 16 →
18 sections). Every ORACLE commit to the file (`0265040a1`, `f7980f6d7`: EXP-142/146) predates the
overlays' base. Evidence class NATIVE/STATIC; the sections' fixtures were not replayed.

## Verdict: ACCEPT THE CORRECTIONS · RESTORE THREE DROPPED FACTS BEFORE PUBLICATION

### Re-read from the image — agree

| claim | static finding |
|---|---|
| **Q5** the requester copies the descriptor's callbacks and argument | `0032E870`: `0032E8DD mov r8, [rcx+0x10]`, `0032E8E1 mov r9, [rcx+0x18]`, `0032E8E5 mov r11d, [rcx+8]` |
| **Q7** id = `(counter << 6) + (slot & 0x3F)` in 32 bits | `0032E924 and eax, 0x3F` / `0032E927 shl ecx, 6` |
| HEAD's "while the free head is null it pumps" (kept, reworded) | the requester's loop calls `0032E070`, `0046DFE0`, `0035EA30` (`0032E8AA..B6`) before `0032E990` |

**Not re-derived** (accepted at the sections' stated scope): Q1–Q4, Q6, Q8, Q9; O08-1..6; SECTION-09.

### Dropped against HEAD, and NOT restated anywhere in the rewrite

| HEAD fact | HEAD citation | in the rewrite |
|---|---|---|
| **The boot modes call the ASKING form `0032E520(1)`, not the draining form** | `00379E30` | absent (0 matches for asking form / `0032E520(1)` / boot) |
| **The staged-selection push** run inside the executed pump (EXP-146's disclosure) | `0036C1F0` | absent |
| **Initialisation resets the read layer** | `0032EA90` → `003EB050` | absent |

Also dropped as addresses but **restated in words**, so not a loss: the signed-bias alignment idiom
(`0032E721..0032E735`), the pump's blocking loop, and EXP-146's scripted-pacer disclosure
(`0035EA30`/`0035EB70`).

## ORACLE's request

`REQ-OPUS-QUEUE-CONTRACT-S13-READJUDICATE` (re-adjudicate I1–I7 now that the pump is executed) is
**blocked on this merge**: the §13 it points at is the text the overlays rewrite.
