# EXP-239 — entity-node bit-3 writer `2EBB80` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `9af86e31` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..238; no new cases — the `bbb80` scripted sink now
executes the shipped body; asserts retargeted to the real tag).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Body promoted real this round

`002EBB80` (`l2ebb80`, ×7) — the bit-3 writer `301140`'s teardown
reaches through the one-instruction `26DC60` trampoline
(`jmp 0x2EBB80`, already real as `l26dc60`):

```text
if b[rcx+3] & 0xE0 != 0x60:            ret        ; eax clobbered
node = q[rcx+0xC0];  if !node:         ret
b[node+0x10] = (b[node+0x10] & 0xF7) | ((dl & 1) << 3)
jmp 0x2E8FD0                                     ; tail — scripted
```

Same `b[+3]&0xE0==0x60` gate family as EXP-237's `2E9780`/`26D6F0`.

## Why all 7 calls are the early-out arm

The calls come from `301140` (`l01140-*` family) with
`(rcx=ent, edx=0|1, r8, r9=1)` — `ent` is the zeroed fixture buffer
(`ent_b`/`ent_q` never planted on l01140 cases), so `b[ent+3]`=0 →
`&0xE0`≠`0x60` → the early `ret`. Observable behavior identical to
the stub: the caller at `0x3012F6` discards `eax`
(`d[rbx+0x30]=edi` + restore + ret), so the stub-vs-real rax
difference (`movzx`/`and` clobber) is unobservable. What changed is
authority — the shipped gate computes the decision, and a fixture
planting `b[ent+3]=0x60` + `q[ent+0xC0]` would now reach the real
bit-3 fold and the `2E8FD0` boundary instead of unmapped bytes.

## Newly surfaced boundary

`002E8FD0` (`v2e8fd0`, ×0) — `2EBB80`'s pass-arm `jmp` tail:
`q[rcx+0xC0]` second-level node walk (`+0x30/+0x60/+0x90` rows,
`d[node+0x164]`/`b[+0x10]/b[+0x11]` mask checks, `d[node]==-1`/`w[node]`
sentinels) into `3E6A60`/`2E8CE0`/`2EE190`/`2E8AC0`/`2E8A70` subtree.
Only image reference is the `26DC60` trampoline — no other harness
caller can reach it. Scripted eagerly so a future `ent_b={3:0x60}` +
`ent_q={0xC0:…}` fixture surfaces it as a recorded boundary rather
than silent real execution. jmp-tail `_ret` mechanics identical to
`v422c20` (pops the `call 26DC60` return address).

## Shipped-value pins

`byr("l2ebb80")` args on `l01140-rel` (rcx==`ent`, edx==0) and
`l01140-bbb1` (edx==1) — same slots the stub era pinned, now
recorded off the real call. No state pins: the early-out writes
nothing.

## Corrections of record

Assert retargets only: `by("bbb80")` → `byr("l2ebb80")` (two sites,
`l01140-rel`/`l01140-bbb1`). The `bbb80` SCR entry removed;
`l01140-bbb1`'s name now refers to the planted `edx=1` arm value,
not the routine's scripted tag. Zero regression failures —
**542/542 first run**. Census: `l2ebb80` ×7, stale `bbb80` ×0,
`v2e8fd0` ×0 disclosed.

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `290B90` (`s290b90` ×34), `317E50` (`b7e50`
×0), `20CE60` (`v20ce60` ×0), `427320` (`v427320` ×1), `422C20`
(`v422c20` ×1), `3377C0` (`v3377c0` ×19), `28EF70`/`28EF00`
(×1/×0), `2E9BB0`/`2EC5B0` (×0), `2E8FD0` (this round, ×0),
`3B02A0`, `46AB10`, `210EC0`, `1CCB20`, `3180F0`, `319CA0`,
`426130` remain scripted. `live_game: false`.
