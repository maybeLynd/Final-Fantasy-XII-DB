---
id: EXP-156
title: "Broadcast wrappers 30F3F0/30F4B0 + slot resolvers 320AB0/31B9F0/320A40/30B0E0"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp156_check.py
result: 77/77 (stable x3)
---

# EXP-156 — per-slot broadcast wrappers, executed

`0030F3F0` / `0030F4B0` are the sibling wrappers that fan the stat cluster
(`30F690`/`30F340`/`30F5A0`, all real since EXP-153) out across the spawn
record table. The whole resolver chain ran real: `320AB0`, `31B9F0`,
`322C50` (its `0x17` arm), `30B0E0`, `320A40`, and the shipped cls-`0xC`
validator `2FD970`.

## `30F3F0(flags)` — member broadcast (0xBE bytes)

Loops `ebx = 0..8` (nine member slots):

```
rec  = 320AB0(ebx, 3)                    # slot -> rec resolver
mask = (flags & 4  ? d[0x208D320] : 0)
     | (flags & 8  ? d[0x208D324] : 0)
     | (flags & 0x10 ? 0x544 : 0)        # default set gated ON by bit4
if mask:        30F690(rec, mask)
if flags & 1:   30F340(rec)
if flags & 2:   30F5A0(rec)
```

Byte-verified correction to the earlier static read: `cmove edx,ecx` at
`0x30F461` *reverts* to globals-only when `flags&0x10` is **clear** — the
`0x544` default mask applies only when bit `0x10` is **set**. The gate cells
are `0x208D320`/`0x208D324` — the same dirty-mask pair `30C470` reads
(earlier `0x1E8D3xx` addresses were a hex slip).

No null check on `rec` in the wrapper — but `30F690` opens with
`test rcx,rcx; je` so unmapped slots are silent no-ops. Verified: slot map
byte `0xFF` → `320AB0` returns 0 → `f690` entry tagged but skips → `e360`
call count drops 36→32, `fed0` 9→8, no fault.

## `30F4B0(x, flags)` — member + foe broadcast

```
30F3F0(flags)          # ecx = edx = flags
jmp 30F4D0             # tail: ecx = ebx = flags
```

## `30F4D0(flags)` — foe broadcast (13 slots)

Loops `ebx = 0..12`:

```
id  = ((ebx + 0x12) & 0xFFF) | 0xC000    # 0xC012 .. 0xC01E
if !30B0E0(id): continue                 # class-descriptor validity
rec = 320A40(ebx + 0x1B)                 # glob+8+(0x1B+i)*0x1C8
<same mask construction + dispatch as 30F3F0>
```

## Resolver chain (all real)

- `320AB0(slot, cls)` → `31B9F0(slot, cls)`; `al > 0x27` → 0, else
  `q[GLOB] + 8 + al*0x1C8`.
- `31B9F0(slot, 3)` → `322C50(0x17, slot)` gate — its `0x17` jump-table arm
  is the constant bound **9** — then `b[q[GLOB] + slot*2 + 0x5A7E]`
  (slot→rec-index map; cls 0/1/2/4 use `+0x5A5A`/`+0x5A6C`/`+0x5A90` maps).
- `320A40(idx)` → `idx > 0x27` → 0, else `q[GLOB] + 8 + idx*0x1C8`.
- `30B0E0(id)` → `id==0xFFFF` or `(id&0xF000)>0xE000` → 0; else class
  descriptor row `0x1EEBCC0 + (id>>12)*0x58`; `(id&0xFFF) > d[row+0x3C]-1`
  → 0; else `call q[row+0x50](id)` — a per-class validator pointer.
- cls-`0xC` row ships `q[+0x50] = 2FD970` (in-file, not fixture):
  `2FD970(id, mode)` mode-0 arm = spawned-bitmap test
  `bt w[q[row+8] + (idx>>4)*2], idx&0xF`. `q[row+8]` is null in the shipped
  table — runtime-populated; planted in the fixture (disclosed MODEL-PROVEN
  state, the only one needed).
- cls-`0xC` `d[row+0x3C]` ships = 32 → ids `0xC012..0xC01E` (idx 0x12..0x1E)
  all pass the count check; validity reduces to the bitmap.

## Executed results

| case | flags | observed |
|---|---|---|
| f3f0-none | 0 | 9 resolves, mask=0 → no f690 |
| f3f0-bit10 | 0x10 | mask 0x544 → f690×9, e360×36 (bits 2,6,8,10) |
| f3f0-gates | 0x1C | mask 0x5C4 → e360×45 (5 bits) |
| f3f0-trio | 3 | f340×9 + f5a0×9, mask=0 → no f690 |
| f3f0-emptymap | 0x10, slot3→0xFF | silent skip, e360=32 |
| f4b0-foes | 0 | 9 member + 13 foe resolves, no dispatch |
| f4b0-mask | 0x10 | f690×22, e360×88 |
| f4b0-trio | 0x13 | f340×22 + f5a0×22 + f690×22 |
| f4b0-skip | 0x10, bmp=0x000C | only ids 0x12/0x13 valid → 2/13 foes |

## Boundary disclosure

Fixture-only state: the cls-`0xC` `+8` bitmap pointer and its bits — real
`30B0E0`/`2FD970` semantics are executed, but which ids are "spawned" is
planted, not live-game evidence. Member `+0x5A7E` map bytes are planted
(identity map). Everything else — resolvers, wrappers, mask construction,
dispatch, the stat cluster underneath — is shipped-code execution.
