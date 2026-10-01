# EXP-249 — `0046AB10` dedup-ring scan arm (hit / stale / miss)

**Status:** complete — **545/545 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `9423b774` prefix; 545
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn over a seeded dedup-ring fixture on three new
direct-entry cases only; nothing claims initialized-gameplay
reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..248; three new cases `q6dup-hit`/`q6dup-miss`/
`q6dup-stale` — pure additions, no existing assert touched).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## What a player sees

When a stat change lands (EXP/LP gain, level up, flag change), the
notifier first asks the dedup ring "did I already report this exact
`{tag, payload}` recently?" EXP-246 executed the insert arm — a fresh
notification writes a ring row, advances the cursor mod 10, and posts
the notify. This package exercises the other half: the **scan arm**
that decides whether a repeat is still inside the dedup window.

## Mechanism exercised (all shipped bytes)

Entry `0046AB10` directly (`rcx`=payload, `edx`=tag, `r8`=struct —
`d[r8+0x28]=0` under the `0x1FF` cap, `q[r8]`/`q[r8+8]` null so
`00469570`'s owner lookups miss → ret 1 → proceed). The `q6desc`
fixture's new `elf` field sets `b[elemb+4]&1`, so the flag test at
`0046ABB3` takes the **scan** branch instead of the insert fast-path.

The scan walks all ten ring rows `02EBB560..02EBB6A0` (stride
`0x20`): a row matches iff `q[row+8] == payload` and `w[row] == tag`.
On a match, `ecx = d[01DFE0B4]*0x1C2 + d[row+4]` — the shipped
constant `d[01DFE0B4]` is `1`, so the predicate is
`stored_ts + 0x1C2 > now` where `now = 0032A150() = d[0208D45C]`:

- **`q6dup-hit`** — matching row, `0x1C2 > 0` → `ja 0046AC6B` →
  epilogue → **ret 0: no row write, no cursor move, no `s5369c0`**.
  The repeat is inside the `0x1C2`-tick window and is swallowed.
- **`q6dup-stale`** — matching row but `now=0x1000` expires it
  (`0x1C2+0 ≤ 0x1000`) → scan continues over the remaining rows →
  falls into the real insert arm at pre-seeded cursor 5: writes
  `w=0x1234`, `q+8=payload`, `d+4=0x1000`, cursor→6, `s5369c0` fires.
  The seeded stale row at slot 2 is left **untouched** — pinned.
- **`q6dup-miss`** — seeded row carries tag `0x9999` vs `0x1234` →
  the `w[+0]` compare fails on all ten rows → insert arm at cursor 0
  overwrites the seeded slot, cursor→1, `s5369c0` fires.

New case keys: `q6desc.elf` (element flag byte), `q6ring` (seeded
rows `{slot, w, ts, q8}`, `"q8":"self"` resolves to the case's own
payload alloc), `q6now` (`d[0208D45C]` "now"), `q6cur` (insert
cursor `d[02EBB54C]`). Fixture allocs are lazy — only the three new
cases shift pool layout; all 542 prior cases are byte-identical.

## Harness note

`on_code` skips `addr == self.entry`, so a direct-entry case never
records its own REAL tag — execution is proven by the shipped side
effects (ring writes, cursor, scripted-notify args `s5369c0 =
[q6pay, 0x1234, q6s]`) plus the `l69570` callee record — the same
convention `k99b0-*`, `d3d0-*` and the other direct-entry families
already use.

## Not claimed

- The `d[r8+0x28] ≥ 0x1FF` cap early-out (`0046AB21 jge`) — needs
  a struct over the cap; trivially reachable, left unexercised.
- The `b[rax+4]&0x20` mid-gate (`0046AB52`) — needs a `0031B860`
  owner-scan hit; scripted boundary today.
- `005369C0` real body — remains the scripted `s5369c0` notify sink
  (0x240-frame broadcast builder, unread stack arg — deferred).
- Live-game reachability — `NATIVE-REPLAY`, `live_game: false`.
- `e130`/`0030E130` still ×0.
