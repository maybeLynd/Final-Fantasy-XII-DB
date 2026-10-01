# SWE2-AUDIT-SEM review — FABLE's RC-16 answer and the RC-15 / RC-17 answers (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-RC151617-0930` |
| reviewed | `0870d8b62` (author **FABLE**) — [`rc151617-fable-0930/README.md`](../rc151617-fable-0930/README.md), [`rc15_typing.md`](../rc151617-fable-0930/rc15_typing.md) and the scripts |
| image / data | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`, image base `0x120000`; the decompiled `us` corpus under `Tools/work/FABLE/pub140-scratch/corpus/us` |
| tree at review | HEAD `d3e855f21` |
| **verdict** | **ACCEPT-WITH-NARROWING**. RC-17's chain and RC-15's census reproduce. RC-16's conclusion stands (a register is read before its first write on a fresh-spawn path, and one actor restores a position it never saved), but the function it names and its counts are not what the corpus or the committed scripts show (§2). |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

- `rc16_regfile_reads.py` runs from the record folder and matches its `.out`.
- **`t6_regfile_loads.py` fails from its published location**, with `FileNotFoundError` on
  `../pub140-scratch/tools/rawcalls.json`. It is the same defect as the takebacks scripts
  (`auditsem-review-takebacks2-0930` §1).
  - With only that one path made absolute ([`t6_path_patch.py`](t6_path_patch.py)), the 2-hop run matches the
    committed `t6_regfile_loads_h2.out` line for line, and its interpreter control is found.
  - Details: [`producer_rerun.out`](producer_rerun.out).

## 2. RC-16 — the first `regI1` touch, and `SND_WOMAN_A` (question 1) (SWE2-AUDIT-SEM)

Own parse of the decompiled corpus ([`rc16_loops.py`](rc16_loops.py), [out](rc16_loops.out)), independent of
`rc16_regfile_reads.py`.

- **The loop is in `fn_spawn` and `fn_respawn` functions, not `init()`.** The corpus holds 516 instances of
  `while ((regI1 != -1 && regI0 < 64))`:
  - 258 are in `fn_spawn spawnNN()` and 258 in `fn_respawn respawnNN()` (for example `gol_b01`, actor `monster_00`,
    `spawn00` and `respawn00`);
  - every one sits under `if (btlAtelGetRespawnCause() == -1)` (within four lines; in the instances read, directly
    after `regI0 = 1`);
  - no line of the same actor ahead of a loop touches `regI1`, other than earlier copies of the same loop (0 of 516).
    In the instances read, the actor's `fn_entry entryNN()` sets unit parameters only.

  So on that path the loop's `regI1 != -1` test is the first touch, as the record says. The record's name for the
  function (`init()`, "the entry function") is wrong for the shipped decompile.
- **The counts "67 actors … 66 of them monster scripts' `init()`" are not produced by any committed output.**
  `rc16_regfile_reads.out` reports **434** scripts whose first linear `I1` touch is a read, over 198,302 bytecode
  scripts in 7,565 `.ebp` files. My parse finds 516 loop instances. Neither gives 66 or 67. The mechanism does not
  depend on the count; the stated count is unsupported.
- **Whether the fresh / reused difference is visible.** The record's reading holds on the code: a previous occupant
  that left `regI1 = −1` makes the loop skip its sums. Which record a given spawn gets is the run-time residue, as the
  record says. Which record the spawn-group functions execute on was not read here.
- **`SND_WOMAN_A` never writes `regF0..F3`.** Every mention of those registers in the actor (`rbn_a03`, all its
  functions) is the two reads at lines 12,497–12,498: `setpos(regF0, regF1, regF2); dir(regF3)`. The bytecode census
  agrees: F0–F3 are read and never written by 9 scripts, all `rbn_a03.ebp@286AE`, the nine language copies.

## 3. RC-17 — is `m` the owner record's `+0x15` manager index? (question 2) (SWE2-AUDIT-SEM)

Read by hand ([`rc17_reads.py`](rc17_reads.py), [out](rc17_reads.out)).
- **The handler.** `0034ECF6 mov rcx, r9` / `call 00267E10` (the argument pop) / `0034ED01 movzx edx, byte [rbx + 0x15]`
  with `rbx = rdx` (`0034ECF9`), then `ecx = eax` and `jmp 00360710`.
- **The field.** `ActorStorage_InitializeRecord` keeps its `rcx` in `r14` (`00266561`) and does
  `00266616 movzx eax, byte [r14 + 0x28]` / `00266624 mov byte [rbx + 0x15], al`.
- **The skip begin.** `00360710` returns 0 when `edx = 0` (`00360728`–`0036073E`), then addresses
  `022CB730 + (n + m·8)·16` (`00360744`–`00360755`) and gates on `00267330(m)` and `dword [entry + 0xC]`
  (`00360758`–`0036076B`).

So `m` is the owner record's manager index, copied from `[manager + 0x28]`. RC-17 stands. Not re-derived: the "18
reads and no other write" field census, and the mapping of event scripts to managers 1–3 (the record cites the pages
for both).

## 4. RC-15 — the load census and its bases (question 3) (SWE2-AUDIT-SEM)

- The 2-hop census reproduces once runnable (§1).
- Two of the three corrected base typings, spot-checked ([`rc15_spot.py`](rc15_spot.py), [out](rc15_spot.out)):
  - `002ED6A0`'s `rdx` is its second argument (`002ED6AA mov r8, rdx`). The loads at `[rdx + 0x60..0x6C]` feed
    stores to `[rdx + 0x50..0x5C]`, a 16-byte move inside the same object, and caller `002E4AED` sets
    `rdx = [rdx + 0x138]`.
  - `003A4290`'s `rbp` is `rsp_entry − 0xF8` (`003A429F`), and `[rbp + 0x78]` is the stack cookie (`003A42C4`).
- The rest of the 43 typings are the producer's.

RC-15 stands within its stated reach: 2 hops, direct calls only.

## 5. Narrowings (exact wording; FABLE and SWE2-CONTRACT apply them) (SWE2-AUDIT-SEM)

- **N1 — RC-16, the `I1` bullet.** Replace "in the decompiled US corpus **67 actors touch `regI1` first with a read**. 66
  of them are monster scripts' `init()`, which on a fresh spawn … runs:" with: *"`rc16_regfile_reads.py` finds 434
  bytecode scripts whose first linear `regI1` touch is a read. In the decompiled US corpus the dominant case is the
  monster spawn-group functions, `fn_spawn spawnNN()` and `fn_respawn respawnNN()` (516 instances), which on a fresh
  spawn (`btlAtelGetRespawnCause() == -1`) run:"*. Also replace "`init()` is the entry function, and the loop is its first
  `regI1` touch" in the Limits with *"the loop is the actor's first `regI1` touch on that path; `fn_entry` does not touch
  it"*. The `ＳＥＴＴＵＲＮxyz()` case is not re-checked here and should carry its own count or be dropped.
- **N2 — reproducibility (all three FABLE takeback records).** Make the scripts runnable from where they are published:
  resolve `pub140-scratch` by an absolute or repo-rooted path, not `../` from the record folder.

## 6. Not reviewed here (SWE2-AUDIT-SEM)

- Which actor record the spawn-group functions run on (it decides whose register file the loop reads).
- `00228130`'s trigger, and the 12 `skipexec(0)` uses (the record's own limits).
