# RC-28 leftover: a refused `.btm` request still fires its completion callback `00364380` (SWE2-DATA, 2026-09-30)

**Question.** Round 2 ([`../rc-residue-0930/`](../rc-residue-0930/README.md) section 3) found that the KR and CN
FileSizeTables hold −1 for the six `font_stf` `.btm` ids (kind 7, `0xDA`–`0xDF`). For such an entry the read issuer
`002DF780` refuses the read before it resolves any path. The question left open: does the request queue still complete
that request, so that the `.btm` completion callback `00364380` sets its ready bit? Or does the staff roll wait?

**Verdict: ANSWERED. The callback fires on every refused `.btm` request, and the ready bit is set.** The pump completes
the request from the stale read-status word. With a stale status ≥ 0 it calls the callback as a success (`r8 = 1`).
With a stale status < 0 it still calls it (`r8 = 0`), because the request's byte count is −1. `00364380` ignores that
flag. So `003657E0` reports the face ready, and the KR / CN staff roll goes on to draw from a buffer that was never
filled.

Static only: the certified image (`73461d08…`) and the shipped FileSizeTables. Nothing is routed to ASTRA.

This builds on FABLE's OV-33 static record (`ov33-no-status-exits-fable-0929`, not yet at HEAD, so named rather than
linked). That record already lists this staff-roll route as an E1 exit (the issuer's −1 refusal at `002DF7B9`, which
writes no status). This record follows the same request through to its callback.

## The trace ([`rc28c_callback.py`](rc28c_callback.py) → [`.out`](rc28c_callback.out), FAILS 0)

| step | what happens | pins |
|---|---|---|
| F | `FileSizeTable_KR` / `_CN`: the six `.btm` sizes are −1 (US: 42,240 / 29,184 / 32,256, control K3) | shipped `.fst` |
| A | `00365810` sizes with `0032E400(7, id)`. A non-positive entry comes back unrounded (`0032E43D jle`). It allocates with that size through `00249810` / `002497E0`, and the heap entry `0036BC60` clamps a negative size to 0 before rounding to 64. **So −1 allocates a 0-byte block.** | `00365878`–`0036589C`; `0036BC89`–`0036BC9D` |
| D | The request descriptor on `00365810`'s stack has `+0x08` = row `n − 1` and `+0x10` = `00364380`. `0032E620` copies it and hands it to `0032E870`, which fills the queue slot: `+0x40` = the callback, `+0x60` = the row, `+0x28` = the byte count (**−1**), `+0x70` = the destination, `+0x22` = 0 (one-shot mode), `+0x20` = 1 | `00365837`–`003658C7`; `0032E65D`–`0032E6DD`; `0032E8DD`–`0032E970` |
| P1 | Pump `0032E070`, state 1: since `+0x28 ≠ 0` it issues through `0046E030` → `002DF780`. **`0046E030` returns 1 whatever the issuer did**, and the slot goes to state 2 unconditionally | `0032E0CE`, `0032E0F1`, `0032E0FF`; `0046E043` |
| S | `002DF780` refuses the −1 entry (`002DF7B0` / `002DF7B9` → `002DF85D`) before the only two places it passes the status pointer (`002DF808`, `002DF838`). The status word `0215EFF4` is written only through that pointer, by the jobs: −1 at issue (`001D6DD4`) and the result at completion (`001D6D70`). **So a refused read leaves the previous completed value in place, which is not −1.** | rip sweep of `0215EFF4`: 4 `lea`s + the 2 readers (control K1) |
| P2 | State 2 → 3 (`0032E15A`). State 3 waits only while the status is −1 (`0046DFE0`), then sets state `5 + (status < 0)` (`0032E19C`–`0032E1A8`) | pump jump table decoded, control K2 |
| C | Mode 0: state 5 runs `0032E330`, which calls `+0x40(row, dest, r8 = 1)`. State 6 runs `0032E370`, which calls `+0x40(row, dest, r8 = 0)` **exactly when `+0x28 == −1`**, and that is this request's byte count | `0032E266`–`0032E285`; `0032E336`–`0032E34F`; `0032E382`–`0032E392` |
| B | `00364380` sets bit `row` of `[022CBE00] + 0x240` and reads no `r8`. `003657E0(n)` tests bit `n − 1` of the same word | `00364391`, `00364393`; `003657ED`–`003657FA` |

**Why the stale status is never −1 here.** The pump works one slot at a time. It completes a request only after
`0046DFE0` has seen the status leave −1. So when the refused request reaches state 3, the word holds the previous
request's completion value, or 0 at boot: the word sits past the image's file data and starts zeroed.

A completion stores the job's low result dword zero-extended. OV-33's E4 section states these are clamped read counts
or −2, so none is −1.

## What the KR / CN staff roll then does

`0053EB90` requests the six faces (`n = 7..12`) and polls `003657E0` with the same `n` (first record, RC-27). Each
poll succeeds once the pump reaches the refused request, so the staff roll does not wait.

The face's sheet pointer (`[022CBE00] + 0x110 + row·8`, stored by `00365810` at `003658B5`) is the 0-byte allocation,
and no read ever fills it. Glyph draws take `sheet + pixelOffset` (`00364346`) up to about 42 KB past it. **Not
claimed:** whether `0036BC60` returns a block or null for the 0-byte size, and so whether those reads fault or return
unrelated heap bytes. That is the allocator's behaviour at size 0, and it does not affect the callback answer.

## Controls

| control | what it shows |
|---|---|
| K1 | the `0215EFF4` rip sweep finds its two known readers `0046DFE0` / `0046E0E0` |
| K2 | the pump's six-entry jump table decodes inside `0032E070` (states 1..6 → `0032E0BD`, `0032E149`, `0032E163`, `0032E163`, `0032E1AB`, `0032E1AB`) |
| K3 | `FileSizeTable_US` sizes the six `.btm` positively, so the KR / CN −1 is not a reader artefact |

## Crossings into other layers

- **Resource**: the request API, the queue slot and its pump, the read issuer, the FileSizeTables and the heap.
- **Presentation**: the font cache's ready word and sheet slots.

This record claims only the pinned instructions of each.

## For SWE2-CONTRACT (RC-28 row, the leftover sentence)

Replace the RC-28 open leftover ("what the request queue does with a refused read, i.e. whether the `.btm` completion
`00364380` sets its ready bit") with:

> **Answered 2026-09-30 (SWE2-DATA, `_index/candidates/rc28-callback-0930/`, `rc28c_callback.py` FAILS 0):** a refused
> KR / CN `.btm` request still completes. `0046E030` returns 1 whatever `002DF780` did, and the pump completes the slot
> from the stale status word `0215EFF4`. A stale value ≥ 0 runs `0032E330`, a value < 0 runs `0032E370`, and both
> call `00364380`: the second because the request's byte count is −1. `00364380` sets the ready bit regardless, so the
> staff roll does not wait. It draws from the 0-byte sheet allocation (`0036BC60` clamps −1 to 0), which no read
> fills.
