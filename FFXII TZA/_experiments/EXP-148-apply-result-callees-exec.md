---
experiment: EXP-148
title: Apply-result-to-target — the five previously-undecoded callees
  0030E130/0030FED0/0030C650/003008A0/00316A50 executed on shipped
  bytes (status-bit modes, recompute bitmap dispatch, level growth,
  item-write unlock flags, descriptor-driven field writer)
contract: ../07-Combat-Action/CONTRACT-apply-result-to-target.md
method: B
live_game: false
tool: evidence/apply-result-callees-exec/check.py
---
# EXP-148 — apply-result-to-target: the five undecoded callees

> **SECTION-01 consumption (2026-09-22):** the 43 stored case assertions replay
> successfully. This is retained-result checking, not a new Unicorn or live run.
> The [current contract](../07-Combat-Action/CONTRACT-apply-result-to-target.md) and
> [review](evidence/continuation-section01-result-install/REVIEW.md) preserve scripted
> boundaries and separate stats-record arguments from their owning BattleUnit objects.

**Contract:** `../07-Combat-Action/CONTRACT-apply-result-to-target.md`
**Scope:** §14's five callees "cited by name and argument, not decoded":
`00316A50`, `0030FED0`, `0030C650`, `003008A0`, `0030E130`.
**Method:** NATIVE-REPLAY — shipped bytes under Unicorn, fixtures are
disclosed MODEL-PROVEN plantings of BSS/descriptor state. No EXE bytes
modified.
**Harness:** `evidence/apply-result-callees-exec/check.py`
**Result:** `evidence/apply-result-callees-exec/result.json` —
43/43 cases, 0 failures, stable across 3 processes.

All five callees execute as shipped bytes. Real helpers under
emulation: `002536A0`, `0020E600`, `002F9A60`, `002F9B20`, `002F9BD0`,
`003166F0`, `00322C50` (+ its cls-6/cls-0x1D arms). Scripted
boundaries (entry-intercepted, args recorded, disclosed):
`0031B860`, `003165C0`, `00315E90`, `00316BF0`, `008632B0`,
`00309F30`, `0030EA40`, `003112F0`, `003279B0`, `00808C40` (canary),
`00386A50`, `00386AE0`, `0046A720`, `0046A790`, `0046A690`,
`0035D8C0`, `002EACD0`, `003A1180`, `002DF220`, `00329210`,
`0031E9A0`, `00323890`, `002FEF30`, `0030E060`, the `q[desc+0x48]`
item callback, and `0030FED0`/`0030E130`/`0030E360` when reached
*nested* from another subject (each is also exercised standalone).
`00861EC0` (memset) is implemented in the hook.

Planted runtime state (all BSS/heap cells the EXE would initialise at
boot — disclosed fixtures, not shipped data): `q[01F83530]` element
array base (20E600), `q[020927C0]` unit base (2536A0), the
`q[02EBF***]` descriptor cells (`{d+4 count, w+8 stride, d+0xC elem
off}`), `q[02EBF190]` flag-record pointer, `q[01F44830]` canary, the
`00D10460`/`00D10550` field tables, and the `01EEBCC0` category table.

## 00316A50 — field writer `(cl=field, edx=delta)`

Field descriptor at `00D10460 + f*8`: `b[+0]` path-select, `b[+1]`
storage offset for the getter, `b[+2]` mode, `d[+4]` bound/expected.
Second table `00D10550 + f*4` supplies the `008632B0` argument.
`field >= 0x1E` returns immediately with no reads.

- **Path 0** (`b[+0]==0`), mode 0: gate = `003165C0(f)` if nonzero
  else `d[+4]`; `delta < gate` exits silently; otherwise `bts` into
  the bitfield at `002536A0()+0x3844 + f>>3` bit `f&7`, then
  `008632B0(d[00D10550+f*4])`. Mode 1: requires `delta == d[+4]`
  exactly. Other modes exit.
- **Path 1** (`b[+0]!=0`): `ebx = 003166F0(f)` — the real getter
  reads `movsx w` / `movzx d` at `unit+0x384C+b[+1]` when `b[+0]` is
  2/4, else returns −1. Then `b[+2]` mode: 0 → dispatch on `b[+0]`:
  2 → signed add clamped to `0x7FFF` with floor 0; 4 → clamped to
  `0x7FFFFFFF`; other → **plain unclamped add** (observed: b0=1,
  getter −1, delta 0x10 → wrote back 0xF). Mode 3 → `bts ebx,
  delta−0xE2` (bit-set by delta). Mode 8 → exit. Other modes →
  write back the unmodified getter value. Write-back pair is
  `00315E90(f)` then `00316BF0(f, ebx)` (scripted; arg recorded).

## 0030C650 — level set / growth `(rcx=unit, edx=target, r8d=flags)`

`r14d = min(target, 0x63)`; loop over `esi = b[unit+0x1C2]` → r14d.
Zero iterations makes zero calls. Per iteration:

1. `0031B860(unit)` → record (scripted).
2. If `b[unit+5]==0`: growth record = `0020E600(d[desc130+0xC]) +
   w[desc130+8]*b[unit+4]`; `002F9A60(level, d[unit+8])` rewrites
   `d[unit+8]`; `002F9B20` rewrites `w[unit+0xC]`; four `002F9BD0`
   calls fold `b[rec+0x1F/0x22/0x25/0x28]` into `f[unit+0x10..0x1C]`.
   `b[unit+5]!=0` skips all growth — level increments only.
3. `b[unit+0x1C2] = min(level+1, 0x63)`.
4. On the last iteration (`esi == r14d-1`): `0030FED0(unit, 0)`
   **always** runs; then if `~(flags>>1)&1` (flags bit1 clear) and
   `b[unit+5]==0` → `0046A690(unit)`; then if also `r15` nonzero and
   `b[q[r15+0x698]+5]==0` → license-notify chain `0035D8C0`,
   `002EACD0(r15+8,1,0x71)`, `003A1180(7)`, `002DF220`, `00329210`.

Executed: single level-up ran the full chain; multi-level repeated the
growth block per level; `flags&2` suppressed `0046A690`+license but
not `0030FED0`; `b[unit+5]!=0` suppressed growth but not the license
chain; target>99 clamped to 99.

## 003008A0 — item write `(cx=id, edx, r8d, r9d, [arg5])`

Rejects (32-bit `0xFFFFFFFF`): `id==0xFFFF`, `id==0x1000`,
`(id&0xF000)>0xE000`, `(id&0xFFF) > d[cat+0x3C]-1`. Category
descriptor = `01EEBCC0 + (id>>12)*0x58`. `00309F30(id, r9d)` resolves;
`q[cat+0x48]` callback overrides and supplies `esi` (the return).

The unlock-flag block runs only when `r9d==1 && resolve<=0 &&
esi>0` — i.e. a callback/secondary path returned a positive count on
an id the raw resolver declined. Executed masks into
`d[q[02EBF190]+4]`: cat 3 → `|1` plus the chain `02EBF0F0` desc →
`recA = base+stride*(id-0x3000)` → `02EBF138` desc → `recB =
base+stride*b[recA+2]` → `w[recB+0x2C]&7` (≤4) indexes the mask table
`01EECF98` → second OR (observed `flags=1|d[01EECF98]=3`); cat 4 →
`|0x40` (`003009E7`); cat 0xC → `id≤0xC011` `|0x80` (`003009D4`),
`0xC012..0xC01E` `|0x100` (`003009C1`) (sites: owner verdict,
EXP-148 consumption). Return = `esi` verbatim.

## 0030E130 — status-bit modifier `(rcx=tgt, dl=bit, r8d, r9d=flags, [arg5]=mode)`

`bit` validated by `00322C50(0x1D, bit)` (real — cls-0x1D desc
`q[02EBF040]`, bound `d[desc+4]`). Modes: 0 clear `b[tgt+bit>>3+0x68]`
(require set); 1 clear `+0x78` (require set); 2 set `+0x68` (require
clear); 3 set `+0x78` (require clear). Mode outside 0–3 exits.

On an actual state change: `memset` a 0x148-byte stack struct, call
notify thunk `00386A50` (modes 0,1) or `00386AE0` (modes 2,3) with
`(tgt, bit, &struct)`; if `b[struct+0x2C]&1` → `003112F0`; if flags
bit1 clear → `0046A720`/`0046A790` (same mode split); if bit ∈
`0x68..0x71` → `003279B0(tgt, sel*2-1)` (`sel`=1 for modes 2,3); then
`0030FED0(tgt, r9d)` **only when flags bit9 is clear** — bit9 is the
anti-recursion suppressor, which is why `0030FED0` passes `flags|0x202`
down. No change → none of the notify chain runs.

## 0030FED0 — recompute `(rcx=unit, edx=flags)` — internally `flags|0x202`

- **Null unit is not fully guarded**: `test rcx,rcx` jumps *into* the
  equipment loop, which dereferences `unit+0x50` — observed read fault
  at `0x310080` on `[0x50]`.
- `b[unit+5]==0`: record via the `02EBF130` double-hop; stack bitmap
  bits 0–31 = `d[rec+0x50]`, bits 32–63 = `d[rec+0x54]`.
- `b[unit+5]==1`: `0031B860(unit)` → member; bitmap bits 0–0x7F OR in
  the member's `+0xE80` bitfield.
- Equipment: five words at `unit+0x50`, each cls-6 validated
  (`[0x1000, 0x1000+d[descF8+4])`); item record via `02EBF0F8`
  double-hop; `0031E9A0(rec)==3` and `b[rec+0x1A]!=0xFF` → `bts`.
  A second loop (`edi<0x169`) per set bit consults `q[02EBF038]`
  records gated by `00323890(rec)==2`, folding `w[rec+0xA..0x16]`
  (≠0xFFFF) into the bitmap.
- Dispatch: each set bitmap bit `edi<0x80` → `0030E130(unit, edi, 0,
  flags|0x202, mode=3)` — the bitmap drives the `+0x78` status array,
  and the pre-OR'd bit9 prevents `0030E130`'s own recompute recursion.
- Member tail (`b[unit+5]==1` only): each set bit of `d[member+0xE90]`
  (`edi<0x20`) → `0030E360(unit, 0, edi, 0, …, mode=5)` — the
  contract's own apply/remove entry, exercised here as a scripted
  boundary. Then `b[q[member+0x6A0]]&0x80` selects copy direction
  between `member+0x78..0x7C` and `unit+0x40..0x44` (clear → unit→
  member, executed; set → member→unit).
- Final gated updates of `d[unit+0x48]` (vs `d[+0x24]`, `flags&0x10000`
  clamp to `r13d=1`, `bt edx,0x1C` doubling), `w[unit+0x4C]`, `w[unit+6]`
  under the `b[+0x6C]`-sign/`b[+0x7C]`/`b[+0x37]` gates; tail call
  `0030E060(unit, flags|0x202)`.

## Boundary honesty

This is replay evidence over synthetic fixtures: the descriptor cells,
unit/member blocks, and record rows are planted. It proves the five
callees' executed semantics — dispatch tables, clamps, bit semantics,
notify chains, recursion suppression — at their real shipped bytes. It
does not prove the in-engine call sites initialise the same fixture
state, and the scripted helpers' own bodies remain their own scopes.
