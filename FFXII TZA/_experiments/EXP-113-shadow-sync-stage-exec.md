---
experiment: EXP-113
title: Character-shadow stage — shipped gate/walk/sync bodies 00428E40/00426420/00426340 plus the four shadow-object verbs, isolated under Unicorn
contract: ../17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md
method: B
live_game: false
tool: evidence/shadow-sync-stage-exec/check.py
---
# EXP-113 — shadow-sync-stage-exec

**Status:** complete · **25/25 functional cases, 38/38 mutants, stable
across three processes**
**Evidence:** `evidence/shadow-sync-stage-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`, `run2.log`, `run3.log`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-authored-command-ramp-channels`'s last open row: *"the
shadow draw that consumes the floats is unread on both pages."* The
draw is the `display character : shadow` stage (`00332440` stage 1 →
`00428E40`), whose per-record body `00426340` was statically read as
`CharacterRenderRecord_SyncShadowObjects` in
`the-character-render-record-array.md` §13 but never executed. This
experiment executes the full stage under Unicorn — gate, record walk,
per-record sync, and all four shadow-object verbs — and diffs slot
bytes in both shadow pools and the complete call trace against a
Python model.

| VA | role | execution |
|---|---|---|
| `00428E40` | GATE — stage gate + tail jmp to PASS | **real** (48 B, 11 insns) |
| `00426420` | WALK — record chain walk, stride `0x740` | **real** (94 B, 22 insns) |
| `00426340` | SYNC — per-record shadow sync | **real** (211 B, 56 insns) |
| `003B6900` | V1 — `0xE0`-pool mode bits | **real** (43 B, 12 insns) |
| `003AFD00` | V2 — `0x70`-pool mode bits | **real** (44 B, 13 insns) |
| `003B6B80` | LODS — shadow LOD setter | **real** (28 B, 7 insns) |
| `00521440` | THUNK — `jmp 003B6020` | **real** (5 B, 1 insn) |
| `003B5980` | LODC — computed shadow LOD (~16 KB, 130+ calls) | scripted |
| `003B6020` | PASS — the ramp-channel pass itself | scripted |

PASS is scripted at the thunk boundary — it was already executed real
in EXP-108; the stage's own writes all land before the `jmp`. LODC is
scripted with a planted `xmm0` return plus trace — its internals are a
deep geometry pipeline of its own; the sync's *choice* between
computed and constant LOD is what this package measures.

## Measured semantics (native execution, not static reading)

**GATE `00428E40`:** `rax = q[0x022C6F28]` (the character render
record array); pass iff `b[rax+0x48842] == 1 && b[rax+0x48843] == 0`
→ `call WALK` then `jmp THUNK`. Either gate failing → bare `ret`.

**WALK `00426420`:** re-tests the same two gate bytes (it is callable
standalone), then `ecx = d[rax+0x48800]` — head record index. Loop:
`rec = rax + movsxd(ecx)*0x740`; `call SYNC(rec)`;
`ecx = sx w[rec+4]`; until `ecx == -1`.

**SYNC `00426340(rec)`:** unconditional handle maintenance —
`d[rec+0x114] != 0` → `V1(h114, 6)`; `d[rec+0x118] != 0` → `V2(h118, 0)`.
Then the flag gate, all on `eax = d[rec+0x284]` plus two record bytes:
`test al,4` (bit2) `&& w[rec+6] == -1 && !(b[rec+0x2AE] & 2) &&
test al,al` sign (bit7) `&& test al,0x40` (bit6) `&& bt eax,0xC`
(bit12) — i.e. `d[+0x284] & 0x10C4 == 0x10C4`. Under the gate:

- `h114 != 0 && !(b[rec+0xC0] & 0x18)` → `V1(h114, 4)`, then
  `lod = !(b[+0xC0] & 2) ? LODC(h114) : f[rec+0x27C]`, `LODS(h114, lod)`
- `h118 != 0 && (b[+0xC0] & 0x18) == 8` → tail `V2(h118, 1)`

**V1 `003B6900(h, edx)`:** slot = `q[0x02B40528] + (h & 0xFF)*0xE0`;
generation check `d[slot+0x10] == h` →
`b[slot+0x41] = (b[slot+0x41] & (edx >> 2)) | (edx & 3)`.

**V2 `003AFD00(h, edx)`:** slot = `0x02B3F570 + (h & 0xFF)*0x70`
(second pool is an in-image table, not a pointer); `d[slot+4] == h`
→ `b[slot+0x20] = (b[slot+0x20] & 0xF0) | (edx & 0xF)`.

**LODS `003B6B80(h, xmm1)`:** slot = `q[0x02B40528] + (h & 0xFF)*0xE0`;
`d[slot+0x10] == h` → `f[slot+0x14] = xmm1`.

**THUNK `00521440`:** `jmp 003B6020` — the stage tail-falls into PASS.

## Execution findings (beyond the static reading)

1. **The stage gate is two bytes, not one** — `+0x48842` must equal 1
   AND `+0x48843` must equal 0, tested in both GATE and WALK (WALK
   re-tests because it is callable independently of the stage
   dispatcher).
2. **The `+0x284` flag gate is a four-bit mask** — bits 2, 6, 7 of the
   low byte plus bit 12 of the dword (`& 0x10C4`), plus `w[+6] == -1`
   and `!(b[+0x2AE] & 2)`. The earlier §13 reading grouped these as
   kind/subtype checks; execution shows the exact mask.
3. **`b[+0xC0] & 0x18` selects the shadow verb set** — nonzero skips
   the h114 mode/LOD update entirely; `== 8` alone arms the h118
   second verb. `b[+0xC0] & 2` selects constant `f[+0x27C]` over
   computed LOD.
4. **Both pools generation-check before writing** — handle = `gen<<8
   | slot`; V1/LODS compare `d[+0x10]`, V2 compares `d[+4]` (different
   layout — the `0x70` pool stores the generation earlier in the
   slot). A stale handle silently no-ops.
5. **The second pool is an in-image table** at `0x02B3F570`, not a
   pointer — `lea r8,[rip+disp]`, `0x70` stride, gen at `+4`, mode
   nibble at `+0x20`.
6. **The unconditional verbs run before the flag gate** — `V1(h,6)`
   and `V2(h,0)` fire on every synced record with a handle; the
   gated `V1(h,4)` + LOD + `V2(h,1)` updates only apply to records
   passing the full flag gate.

## Mutation campaign

38 byte-precise mutations across: gate immediates and JCC; walk head
field disp, `-1` compares, `0x740` stride, `+4` next field; sync
`+0x114`/`+0x118` disps, verb arg immediates (6/4/0/1), `d[+0x284]`
disp and each flag-gate bit test (`4`, `al` sign, `0x40`, `bt 0xC`),
`w[+6]` disp and `-1`, `b[+0x2AE]` bit, `b[+0xC0]` masks `0x18`/`2`
and `cmp 8`, `f[+0x27C]` disp; verbs' strides `0xE0`/`0x70`, gen
fields `+0x10`/`+4`, mode fields `+0x41`/`+0x20`, masks `3`/`0xF0`,
`shr 2`, `cmovne` inversion, `f[+0x14]`; thunk rel32. **38/38 killed.**

Five initial survivors were coverage gaps, not equivalent mutants:

- `m-w-head` — disp byte0 `+0`→`+2` identical at head=0; repointed to
  disp byte2 (`0x48800`→`0x58800`) on a head=2 case. Killed.
- `m-w-hcmp` — `cmp -1`→`-2` only differs at head=-1; needed `empty`.
  Killed.
- `m-s-2ae` — `test 2`→`4` needed `b2ae=4` (`flag-2ae4`). Killed.
- `m-s-c0m` — `test 0x18`→`0x10` needed `bc0=8` (`flag-b8`). Killed.
- `m-v2-f` — `and dl,0xF`→`7` unreachable: edx is only ever 0 or 1.
  Replaced with the `cmovne`→`cmove` gen-check inversion. Killed.

## Limitations

- LODC `003B5980` is scripted — its gen-match arm is a ~16 KB
  geometry pipeline (130+ calls) that merits its own package; here it
  returns a planted `xmm0` and the call is traced.
- PASS `003B6020` is scripted at the tail — executed real in EXP-108;
  the thunk boundary means no stage semantics depend on it.
- The `+0x48842`/`+0x48843` gate bytes and the `+0x48800` head index
  are planted; their producers (frame driver `00332510` and the
  lifecycle) are outside this package.
- `bodies.json` holds body span + sha256 over shipped bytes;
  instruction-start coverage convention matches EXP-107–112.
