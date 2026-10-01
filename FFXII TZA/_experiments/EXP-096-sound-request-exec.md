---
experiment: EXP-096
title: Sound request path under isolated original execution
contract: ../18-Audio/Audio-Boundary/CONTRACT-sound-request.md
method: B
live_game: false
tool: evidence/sound-request-exec/check.py
---
# EXP-096 — sound-request-exec

**Status:** complete · **39/39 cases, 14/14 mutants, stable across three processes**
**Evidence:** `evidence/sound-request-exec/` (`check.py`, `result.json`,
`bodies.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-sound-request.md` describes the sound-request path — the script verb
`00357040` (`sebsoundplay_2c1`), four request wrappers, four resolvers over
three handle dwords, two independent gates, and the masking play call
`002DF220` that ends in dispatcher `001DBDB0`. The contract's own pilot
(`diff_sound_request.py`, 326 comparisons / 0 mismatches) established
model-level parity with **six leaf callees scripted**. This experiment executes
five of those six — and everything around them — as real shipped bytes:

| VA | role | execution |
|---|---|---|
| `00357040` | `sebsoundplay_2c1` verb | **real** |
| `00267E10` | typed VM stack pop | **real** |
| `0026B4E0` | VM result push (command-state write) | **real** |
| `00249C60` / `00249CA0` / `00271500` / `0024A1A0` | wrappers | **real** |
| `003A1180` / `003A11F0` / `003A1070` / `003A1100` | resolvers | **real** |
| `00267330` / `00267310` | liveness / mute slot predicates | **real** |
| `002DF220` | play call — gate2 + argument masking | **real** |
| `003603C0` | gate2 byte reader | **real** |
| `002DF0F0` | `0024A1A0`'s reshape tail | **real** |
| `001DBDB0` | dispatcher | **scripted at entry** — 174-body closure; logged entry args are the contract's central observable |
| `001DBE90` | dispatcher-B | **scripted at entry**, args logged |
| `002DEE80` | readiness test | **scripted** — its `ecx≠0` arm tail-jumps into dispatcher-B machinery |
| `008620C0` | vmpop type>2 error path | **scripted** ret 0 |

The observable is the call trace plus captured dispatch arguments: `o<n>` =
vmpop seeing count *n* (pop order), `res*` = resolver + arg, `l`/`m` =
liveness/mute predicate calls, `Y` = play-call entry args, `gate2`, `D` =
dispatcher entry args `(sel, id, pan, vol)`, `W` = vmpush value, `DB`/`Rd` =
dispatcher-B / readiness stubs.

## Executed bodies (real shipping bytes)

16 bodies, spans + sha256 in `bodies.json` (`real` array); the four scripted
boundaries are listed separately in `bodies.json` (`scripted`).

| VA | role |
|---|---|
| `00357040` | verb — 4 typed pops, selector dispatch, mute gate, play, push |
| `00249C60` | gated wrapper → `003A1180` → `(0x40, 0x7F)` → play |
| `00249CA0` | gated wrapper → `003A11F0` (no liveness) → play |
| `00271500` | gateless wrapper → `003A1180` → play |
| `0024A1A0` | control entry — gate1, readiness, reshape tail |
| `00267330` | liveness — byte `0x2098E20 + slot*0x288` |
| `00267310` | mute — byte `0x2099011 + slot*0x288` |
| `00267E10` | vmpop — count/type/value stack shape, `cvttss2si` on type 2 |
| `0026B4E0` | vmpush — slot `byte[ctx+0x11]`, buffer `[ctx+0xA8]`, 40B stride |
| `002DF220` | play call — id −1 refusal, gate2, masks, `btr 31` |
| `003603C0` | gate2 — `movsx` byte `0x22CB726` |
| `002DF0F0` | reshape — `id`/`flag` → `(flag≥0, id, flag&~bit31)` → `001DBE90` |
| `003A1070` | resolver — gate `0x2AEF400`, liveness, handle `0x2AEF404` |
| `003A1100` | resolver — gate + handle both `0x2AEF400`, liveness |
| `003A1180` | resolver — liveness, handle `0x2AEF3FC` |
| `003A11F0` | resolver — handle `0x2AEF3FC`, **no liveness** |

## Fixture surface

- Gates: `0x2091098` dword (gate1), `0x22CB726` byte (gate2).
- ActorManager slots `0x2098E20` stride `0x288`: liveness byte at `+0`
  (effective `0x2098E10 + slot*0x288 + 0x10`); mute byte at `+0x1F1`
  (effective `0x2099011 + slot*0x288`).
- Handle dwords `0x2AEF3FC` / `0x2AEF400` / `0x2AEF404`; handle table
  `0x2AEEDC0`, 64 × 24 B, entry `{+8 lo16, +0xA hi16}`.
- VM stack ctx: count dword `+0`, type bytes `+4+i`, value dwords
  `+0x184+4i`. Push order arg1..arg4 = selector, index, pan, volume.
- Command record `+0x15` = mute slot index; outer ctx `+0x11` = push slot,
  `+0xA8` = result buffer (40 B slots: `+0xC` value, `+0x15` type 2).
- Cookie `0x1F44830` planted; all IAT slots nulled.

## Findings (native-verified)

1. **The four wrappers are exactly as contracted.** `00249C60`/`00249CA0` gate
   on `0x2091098` and refuse −1; `00271500` is `00249C60` with the gate check
   absent (proceeds with the gate set — `w-1500-gate1`); `0024A1A0` gates,
   readiness-tests, reshapes `(id,0)` → `(1, id, 0)` and tail-calls
   `001DBE90` — never the play path.
2. **Resolver selection is real.** Verb selector `1` → `003A1100`,
   `2` → `003A1070`, anything else → `003A1180` (`sub eax,1; je; cmp eax,1; je`
   — selector 0 and ≥3 share the default arm).
3. **`003A11F0` really has no liveness call.** `w-ca0-dead` resolves with the
   liveness byte `0x00` where `003A1180` refuses (`resA-dead`/`verb-held`).
4. **Handle arithmetic verified end to end.** `slot = handle & 0xFFFF` indexes
   the table; `entry.w8 | entry.wA<<16` must equal `handle & 0x7FFFFFFF`
   (`resA-mismatch` refuses; `resA-flag31` resolves with bit 31 set);
   resolved id = `slot<<9 + index`; handle `−1` refuses.
5. **Liveness byte semantics verified.** Bit 0 clear → refuse(1); bit 0 set →
   returns bit 7 (`resA-bit7` with `0x81` refuses).
6. **Play-call masking verified at the dispatcher boundary.** With
   `pan=0x2FF, vol=0x1FF`, dispatch receives `(0, 0x605, 0xFF, 0x7F)`: pan
   truncated to 8 bits (`sil`), volume masked to 7 bits (`&0x7F`), id bit 31
   cleared (`play-mask` sends `0x80000605`, dispatch sees `0x605`).
7. **Refusal returns differ and are verified.** Resolver failure → wrapper
   returns −1 (its own `or eax,-1`), while `002DF220` returns **0** on id −1
   and on gate2 (`play-idm1`, `play-gate2`). A scripted dispatch return
   (`0x5A`) propagates through play → wrapper → verb push unchanged.
8. **VM stack contract verified.** Typed pops in reverse order
   (`o4 o3 o2 o1`); type 2 converts via `cvttss2si` (`vpop-float`); empty
   stack returns 0 without popping; type 3 enters the `008620C0` arm. The
   push writes `{type=2 @ +0x15, value @ +0xC}` into slot `byte[ctx+0x11]` of
   the 40 B-strided buffer at `[ctx+0xA8]` — asserted by memory inspection,
   not just trace.
9. **Mute is a separate predicate from liveness.** `00267310` reads
   `+0x1F1` of the same slot record the verb names via `cmdrec+0x15`; nonzero
   skips the play call entirely and pushes 0 (`verb-muted`), distinct from
   `00267330`'s liveness byte at `+0`.

## Mutants (14/14 killed)

Pan truncate (`movzx r8d,sil`→`si`), volume mask (`&0x7F`→`0xFF`), `btr 31`
removal, `cmp ecx,-1`→0, gate2 forced 0, wrapper gate inversion, wrapper
refusal value, resolver `btr`/`shl 9`, verb selector arm shift, verb mute
inversion, liveness bit select, vmpop `dec`, vmpush field offset. Every
mutation produced an observable divergence in trace, return, or pushed
memory.

## Not exercised (disclosed, not claimed)

- `001DBDB0` past its entry — the Seb/Sep fork `00210C00`, controllers,
  bank managers, voice machinery (174-body closure).
- `001DBE90` past its entry — dispatcher-B.
- `002DEE80`'s `ecx≠0` arm (`001DBCE0`) — part of the same boundary.
- `008620C0` — vmpop error path internals.
- No live process, no audible result, no bank data — this is isolated
  original-code execution.

## Harness notes

- `00267330`'s effective liveness address is `slot*0x288 + 0x2098E20` — the
  `+0x10` lands on a `0x2098E10` base, not `0x2098E20`. First run planted the
  byte one stride field off; every liveness-gated case refused.
- Stack-arg discipline unchanged: `emu_start` pushes no return address, so
  the callee sees `rsp` at entry state (fixture stack sits at `sp+0x28..`).

## Reproduce

`python check.py` in `evidence/sound-request-exec/` — requires the exact
shipped EXE (sha256 asserted at load). Exit 0 ⇔ all cases pass and all
mutants die.
