---
experiment: EXP-091
title: Commit-action callees under isolated original execution
contract: ../07-Combat-Action/CONTRACT-commit-action.md
method: B
live_game: false
tool: evidence/commit-callees-exec/check.py
---
# EXP-091 — the scripted commit-action callees, executed real, and `0030F760` re-driven

**Date:** 2026-09-17 · **Worker:** SWE2-ORACLE · **Method:** B (isolated original-code execution, Unicorn)
**Subject:** every callee `diff_commit_action.py` supplies as a scripted oracle — `003105D0`,
`00310780`, `0031B7E0`, `003588B0`, `00316CF0`, `00316CD0`, `0030AB40`, `0030C970`, `00313B30` —
plus their bounded transitive closure (`bodies.json` lists 54 bodies; the retained fixtures execute 47 — see `evidence/exp091-resolver-base-repair-1003/`), then `0030F760` re-driven end-to-end
with the real callees wired in.
**Contract:** `Database/FFXII TZA/07-Combat-Action/CONTRACT-commit-action.md`
**Board task:** `SWE2-ORACLE-COMMIT-CALLEES-EXEC`
**Evidence:** `evidence/commit-callees-exec/` (`check.py`, `result.json`, `bodies.json`,
`run1.log`, `run2.log`)

## Result

**87/87 cases pass; 10/10 byte-level mutants detected.** Stable across two full processes. (85→87 on 2026-10-02: additive `cpys-dest-6b0`/`cpys-nohit` regression cases per `ASTRA-REQ-ORACLE-SUSPEND-COPY-REGRESSION-1001`; the historical 85-case/10-mutant set is unmodified.)

## What each body decides (all measured, none asserted)

- **`0030F760` commit** — stack arg `[rsp+0x70]` is `cancelFirst` (`com-cancel-first` orders
  `commit→cancel→resolv` before anything else). `0031B7E0` resolves the packed param once, before
  the band test. Band 1 (`id <= 0x21E`): `00316CF0` resets the `+0x778` buffer (byte `+0` bit1 →
  `memset` 208 B, count→1 or 0) then `00316CD0` appends **`[resolved+0x10]`** — a field of the
  resolved unit, not the unit pointer. Band 2 (`0x4000–0x4166` window, `id-0x4000 <= 0x166`):
  skips reset/append entirely. Anything else → return 0.
  - Then unconditionally: `+0x700 &= ~3`, `+0x708 = rdx arg`, `+0x710 = param`, `+0x714 = id`,
    `+0x718 ← +0x700` copy, `+0x728 ← +0x710` copy, `+0x6B4 = 0`.
  - `+0x770` latch: cleared unless it is nonzero **and** stats byte `+5 == 0` with committed id
    `+0x744 == id` and committed param `+0x740 == param` (`com-770-same`/`com-770-diff`).
  - `+0x6B0` bit1 consumed → posture byte `+0x6B9 = [0x22C1DB8 + ea9*12]`, `+0x6B6 = 1`.
  - `+0x24 != +8` → `+0x750` zeroed early; relation runs anyway. `relat >= 2` → `+0x754 = param`;
    `relat >= 2` **and** `+0x24 == +8` → the propagation loop re-reads `00236850()` every pass and
    writes `+0x754 = param` to every unit whose `+0x24` matches, then `+0x750 = param`
    (`com-b1-basic` vs `com-noprop`).
  - Target mask: actor flag bit 22 vetoes it (`bt [rbx], 0x16; jb`). Otherwise
    `1 << actor+0xEA9` not in `target+0xEA4` → `inc +0xEA8`, `or` into `+0xEA4`,
    `notify(actor, target, r8=1)` (`com-masked`).
- **`003105D0` cancel** — null unit / null stats early-out. `cfix` → `+0x6B6 = 0` →
  `unlink(+0x695)` → `+0x695 = 0xFF` → `unlink(+0x696)` → `+0x696 = 0xFF` → `postc` → flag clears
  `&= 0xFFFFBFF75FFFCFFF`, `+4 &= 0xFFDFFF7F`, `+0x690 = 0` → `0016D6A0` (a `ret` leaf) →
  `&= 0xFFF3FFFFFEFFFFFF` → unit loop (`ucount` re-read per pass) → `treset(+0x778)` →
  `vreset(+0x80)` → `ffill` writes 0x80 bytes of `0xFF` at `unit+0x210` → `mreset` (stub).
- **`00310780` cfix** — null stats → skip. `resolv(+0x710)`; resolved null → postf only.
  **Bit 22 set skips the committed-target fixup** (direction confirmed against `00308270`):
  bit22 clear + target `+0xEA4` has actor's `+0xEA9` bit → `dec +0xEA8`, clear the `+0xEA4` bit,
  `notify(actor, target, r8=0)`, `tfix` (`002FEAD0`). Always ends with postf, then
  `flags0 &= ~0x100020` and `unlink(+0x694)`.
- **`00308270` postf** — runs its body only when bit22 is **set**: `+0x28 = 0`,
  `unlink(+0x695)`, `+0x695 = 0xFF`, posture row `0x22C1DB0 + ea9*12` → word→`+0xDC8`,
  dword→`+0xE58`, then `0030EDA0`.
- **`0030EDA0` cpys** — copies `0x4F0` bytes from `[unit+0xB88]` to **`unit+0x6B0`**
  covering `[unit+0x6B0, unit+0xBA0)` — **CORRECTED 2026-10-02** (was recorded as
  `unit+0x730`, copying the loop cursor's pre-advance as the origin: `rcx = unit+0x6B0`
  at `0030EDA7`, `lea rcx,[rcx+0x80]` at `0030EDB6` runs before the first store at
  `[rcx-0x80]` (`0030EDC7`), so the first byte written is `unit+0x6B0`; nine `0x80`
  rounds end at `+0xB30` and the seven-movups tail ends at `+0xBA0` exclusive). Null
  `+0xB88` faults at `0x30EDBD` — real precondition. Then scans the eight `0x4F0` slots
  at `0x22BEFC0` for an entry **address** equal to the source pointer; hit → `btr` bit
  `i&7` of `0x22BEFB0[i>>3]` (`canc-cpyhit` → `0xFF→0xFB`); miss → return 1. The bitmap
  comparison uses **incoming `r8`** — the source pointer loaded at `0030EDA0` *before*
  the copy overwrites `+0xB88` (which lies inside the copied range at offset `0x4D8`).
  **Additive regression `cpys-dest-6b0`/`cpys-nohit` (2026-10-02,
  `ASTRA-REQ-ORACLE-SUSPEND-COPY-REGRESSION-1001`):** direct `0030EDA0` entry,
  patterned disjoint source, poisoned destination, `0xCC` canaries at `+0x6A8..6AF` and
  `+0xBA0..BA7`; asserts all `0x4F0` destination bytes (incl. `+0x714`, `+0xB88`),
  canaries intact, `+0xB88` post-copy = source's embedded slot-5 pointer while the
  bitmap still clears bit **2** (the incoming r8), ret 1 both paths, bitmap untouched
  on a non-table source. (Also corrects the earlier noted `0x20BEFB0`.)
- **`0030C970` unlink** — **two** `cmp cl,0x1F` gates: `0x30C983` selects the entry for the tail
  (oob → rbx=0), `0x30C9A1` gates the unlink itself; `cl==0xFF` skips unlink but still runs the
  tail. Unlink splices neighbours + head0/head1 globals. Tail on the selected entry:
  `00325A00(+0x28)`, `00317EC0(+0x24)`, and if `+0x18 != 0` → `resolv(+0x20)` → `00306570`.
  Slot reset: `+0x2C &= ~0x1F`, `+0x1C = 0xFFFF`, links zeroed, `+0x28 = 0x80000000`,
  `+0x24 = -1`, `+0x14/+0x10/+0x20 = 0` (`unlink-mid`/`unlink-own`).
- **`0030AB40` relat** — `ebp=1` base; `esi = r8&1`; faction-5 and faction-3 rules plus
  action-block byte `+5` resolve the expected-side flag; result = equality + 1 ∈ {1, 2}.
  `rel-diff` measured 2 (faction 1 vs 2 differ but don't hit the special rules).
  **Null stats + `r8&1 == 0` faults at `0x30AC14`** — a genuine crash input, kept as
  `rel-ablk0-fault`; `r8&1 == 1` skips the deref (`rel-ablk0-r8` → 2).
- **`00313B30` notify** — stack-cookie prologue (`0x1F44830`, `00808C40` rol-16 check — fixture
  cookie `0x0000C0FFEE00C0FE`). Target stats null → `r8` decides directly. Stats mask
  `([+0x64]|[+0x3C]) & 0x80000003` **clear** → collect unconditionally (r8 ignored). Mask set →
  `00377C20` flag77; pass → collect; fail → `r8 != 0` suppresses (`ntf-suppress`), `r8 == 0`
  collects. Collect: actor stats `+5 == 0` → `0031B810(i)` for i=0..3, per-member mask+flag77,
  capped 4 → `0x22C1788`; else single self-record (`ntf-actorbusy`). Dispatch record
  `{+0 kind (self=1/other=2), +1 flag (r8==0), +4 uid, +8 aid, +0xC tid}` → `002ED2A0(uid, &rec)`
  per unit. `rdx=0` faults at `0x313B4F` (`ntf-nulltgt`).
- **`002ED2A0` edisp** — `003588B0(uid)` → `[elem+0xC0]` block; dword `-1` → out; word →
  `RENDT + word*0x740`; `+0x284 == 0` → out; else tail `jmp 0x3E6B50` (esink) → deep chain to the
  stubbed `0x512F30`.
- **`003008A0` idres2** — `cx ∈ {0xFFFF, 0x1000}` → -1; `(cx & 0xF000) > 0xE000` → -1;
  `idx = cx&0xFFF > fam[cx>>12].count-1` → -1 (fam3 count 0x51 → `ir2-fam3-oob` -1).
  `0xE000` is **in** bounds: fam14 (`count 0xFFF`) passes, `famd` returns 0 (`+0x50` null),
  resolver `002FD880` returns 0 for `r9 != 1` → `ir2-e000` = 0 (corrects the boundary guess).
  `r9==1 && famd<=0 && res>0` enters family-specific range checks.
- **`00309F30` famd** — same sentinel/nibble/count bounds (fail → 0, not -1); `edx==4` tail-jumps
  `002FD970` unconditionally; else `jmp [fam+0x50]` or 0.
- **`0031B7E0` resolv** — gate byte `0x2089340` bit `0x10` → `003588B0` → `00263E30` tail;
  else 0 (`com-gateoff` traces resolv but no idres).
- **`003588B0` idres** — nibble `> 5` → -1; `00263FF0` table base; idxt entry `mark`, `bit10`,
  `list`, `bound`, version `+0x16` match gates measured per-field (`idr-*`).
- **`00316CD0` append** — bound `count < 0x20`; slot layout `+8 + count*16`;
  **negative count is unguarded** — `app-neg` writes 8 bytes at `buf-8` and increments `-1→0`.
- **`0031B810` party** — `bound(0x17, i)` fixed `0..8` → byte `[0x2EBF190]+2i+0x5A5A` →
  `002367A0` unit scan (`stats+4` word; `0xFF`→`0xFFFF`).

## Mutation campaign (10/10 detected)

| mutant | site | effect measured |
|---|---|---|
| append bound `0x20`→`0x1F` | 00316CD6 | count 0x1F rejected |
| unlink gate2 `0x1F`→`0x1E` | 0030C9A3 | slot 0x1F skipped (neighbour links survive) |
| idr nibble `5`→`4` | 003588E1 | nibble-5 id now resolves |
| resolv gate `0x10`→`0x20` | 0031B7EA | gate byte 0x10 no longer passes |
| relat fact `5`→`4` | 0030AB96 | faction-4 enters the fact-5 rule |
| cancel `je`→`jne` | 003105EA | null-stats unit runs the full cancel body |
| commit band1 `0x21E`→`0x21D` | 0030F79A | id 0x21E falls to band-2 test |
| commit band2 `0x166`→`0x165` | 0030F7E5 | id 0x4166 rejected |
| notify mask `0x80000003`→`0x80000002` | 00313B68 | masked target collected → dispatch fires |
| edisp `+0x284`→`+0x285` | 002ED2E4 | live render entry fails the gate |

## Deviations and limits (disclosed)

- **Four stubbed entries** (entry byte patched to `ret`, calls logged): `0x512F30` SINK (deep
  render/event sink), `0x33C9B0` MRESET, `0x2FC9D0`/`0x2FCBA0` FAMH0/FAMH3 (family-table handlers
  invoked with the raw id — signature not established). Two host helpers: IAT `memset`/`tick`.
  *(2026-10-03, OPUS: this record did not execute `0x512F30`. Its local effects are now established separately by Method A - ASTRA's `uq147-native-relation-invariant`, ACCEPTED by SWE2-AUDIT-SPEC (`b9502c733`): 26 + 11 persistent write sites, the only transfers `00513005`/`00513022` to `00512CD0`, no import or heap call; see the relation types consumed in `_index/candidates/opus-native-relation-cache-1003/`. That static result is not one of this record's Method B samples, and no case here changes.)*
- Fixture content only: unit array, stats records, `0x2EBF190` struct tables, idxt lists, link
  table, posture table `0x22C1DB0`, render table `0x22C6F28` gate words, `0x22BEFC0`/`0x22BEFB0`,
  cookie `0x1F44830`, fam3 `+8` bitset pointer (runtime-initialized, 0 in the shipped image).
- The `003008A0` 5th argument is read from the caller's stack slot; `ir2-*` cases leave it 0.
- `bodies.json` spans are computed by linear scan with forward-branch reachability — approximate
  on jump-table dispatchers (e.g. `0x322C50` arm tails); 47 of the 54 listed VAs execute under the retained 87 cases and 10 mutants. `0020E600`, `0025AAD0`, `002F1710`, `00316A50`, `00317E50`, `003BBC80` and `003DC780` do not. This is a coverage gap of these fixtures, not a reachability result. The harness planted the resolver base at `0x1F85D30`, not the `0x1F83530` that `0020E602` reads. No retained case reaches `0020E600` or reads either cell, so no retained result changes. The repair and the action-row control are in `evidence/exp091-resolver-base-repair-1003/`.
- Isolated original-code evidence under Unicorn; no NATIVE-REPLAY or live claims.
