# EXP-234 — entity node clear `2E42D0` + `427280` fold leaf real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `07c5f87a` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..233; no new cases — the `r2e42d0` scripted sink now
executes the shipped body; asserts retargeted to real tags; one new
scripted boundary `v422c20` declared).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

`002E42D0` — the per-release entity-node clear called from `3243F0`
(twice, at `0x324433`/`0x3244CA`, gate-arm selected) plus the `2E3xxx`/
`32xxxx`/`34xxxx`/`37xxxx` teardown family (nine image call sites;
only the `3243F0` pair is harness-reached today). Signature
`(rcx=ent)`; `rdx` is carried but unread:

| body | semantics | hits |
|------|-----------|------|
| `002E42D0` (`l2e42d0`) | `rcx` null → ret; `rax = q[ent+0xC0]` link node — null → skip (`+0xEC` write included) → ret. Live node: `d[node]==-1` → skip; `w[node]` sign → `row = q[0x22C6F28] + w*0x740` — null base → skip; `d[row+0x284]!=0` → `427280(row)`; `d[ent+0xEC] = 0`; ret. | ×18 |
| `00427280` (`l427280`) | `d[row+0x294] &= 0xFFFDFA5F \|= 4` — clears the 0x205A0 visual-state bits, latches bit2 — then `jmp 422C20` tail (scripted, below). | ×1 |

## `422C20` — the disclosed scripted boundary (`v422c20`, ×1)

`00422C20` is the deregistration sweep `427280` tail-jumps to:
`d[rbx+0xC4]`/`+0xC8`/`+0xCC`-family sentinel loop — each `!=-1` field
routes `ecx=d[rbx+0x10]` through `20E600` (table-index resolver) →
`q[rax+0xDA8]` → `51BA40` (dereg call) → sentinel reset. Never
harness-reached before this round — every path to it was gated behind
the scripted `2E42D0` — so intercepting at entry records the call
(`v422c20(elem2)` on `u43f0-ec`) and `_ret()` models `427280`'s tail
return to `0x2E4319` exactly. Needs the `20E600`/`51BA40` resolver
classified plus planted `+0xC4..` sentinel fields before promotion.

## Execution split across the 18 calls

17 of 18 calls resolve `q[ent+0xC0]=0` → early-out (observably
identical to the former stub). `u43f0-ec` — the only case with
`objc0` + `ecarr` planted — executes the full arm: `w[node]=2` →
`ecarr[2]` (`d[+0x284]=1`) → real `427280` fold → `v422c20` boundary
→ `d[ent+0xEC]=0`.

## Shipped-value pins added/changed

`u43f0-ec`: elem2 `d[+0x294]` **`0x401080` → `0x401084`** — EXP-234's
`2E42D0` runs *before* `2EB0D0` in `3243F0`'s flow (`0x3244CA` precedes
the `2ECEC0`→`2EB0D0` arm at `0x3244DC`), so `427280`'s `|=4` lands
first and its `&=0xFFFDFA5F` acts on a zeroed row (no-op); EXP-233's
`4278B0`/`427860`/`4272A0` fold ORs on top. New `v422c20(elem2)`
boundary record pinned. `d[objent+0xEC]=0` confirms an existing `dEC`
assert now reads a real write.

## Corrections of record

Assert retargets only: two `by("r2e42d0")` sites → `byr("l2e42d0")`
(`a630r9-swap` shared block, `w4450-set` block; `rcx==w.objent` pins
hold verbatim). Zero regression failures — **542/542 first run**.

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `290B90` (`s290b90` ×34), `317E50` (`b7e50`
×0), `20CE60` (`v20ce60` ×0), `427320` (`v427320` ×1), `422C20`
(`v422c20` ×1 — new), `319490` (`s9490` ×19), `46AB10`, `426130`
remain scripted. `422C20`'s other five image callers (`0x41E8B4`,
`0x429378`, `0x42A0E1`, `0x42A116`, `0x42E03E`) are unreached under
fixtures — interception at `422C20` is exactly scoped. `427280`'s
other image callers (`0x2E30B3`, `0x2E4364`, `0x2E6C2E`) are
unreached; if a future fixture reaches them it now executes shipped
bytes rather than silent code. `live_game: false`.

## Deferred package note — `319490`/`s9490` (×19)

Triage spent on `319490` (the `3377C0` entity-context chain) before
selecting `2E42D0`. Mapped but unapplied: `319490` = `3590D0()` ctx-id
→ `b[0x2089340]&0x10` gate → `3588B0`/`263E30` class-table resolution
→ `b[node]&8` → `3377C0(ctx-or-0, &vec4)` position broadcast. Promoting
its head is feasible (`3590D0`/`3588B0`/`263E30` fixtures exist via
`g272f0`/`mctxid`/`clstab`/`ctx4`) but the honest ctx path needs a
`q[ctx+0x30]` node wiring the `ctx4` fixture doesn't expose, and
`3377C0`'s spatial broadcast (`265090`/`236820`/`31ABE0`/`2EA7F0` →
`391D10`/`3920F0` query → per-entity `263E30`/`314EB0`/`313F80`
classification, five image callers) stays scripted either way. It
remains the census leader at ×19 for the next deep-ctx round.
