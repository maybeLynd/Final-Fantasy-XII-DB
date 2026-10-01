---
experiment: EXP-112
title: Actor record per-record init — shipped ctor 00266530 plus its real callees, isolated under Unicorn
contract: ../04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md
method: B
live_game: false
tool: evidence/actor-record-init-exec/check.py
---
# EXP-112 — actor-record-init-exec

**Status:** complete · **39/39 functional cases, 46/46 mutants, stable
across three processes**
**Evidence:** `evidence/actor-record-init-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`, `run2.log`, `run3.log`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-actor-record-pool-and-region-map`'s last unexecuted closure:
EXP-107 executed the allocator `002679F0` and the region-map
dispatcher `00266AD0`, but scripted the per-record initializer
`00266530` as a boundary. This experiment executes that ctor plus its
real callees under Unicorn and diffs the complete record image, the
RMAP-derived in-record regions, all external buffers, the kind-link
table, the registration cell, and the scripted-boundary call trace
against a Python model of the decoded semantics.

| VA | role | execution |
|---|---|---|
| `00266530` | CTOR — per-record init (mgr, ptab, idx) | **real** (1439 B, 381 insns) |
| `00266AD0` | RMAP — kind jump-table: `+0xA0/+0xA8/+0xB8/+0xC0` | **real** (211 B, 43 insns) |
| `00266BD0` | KINIT — kind leaf: `d[+0x1C]`, `b[+0x14]|0x80` | **real** (95 B, 24 insns) |
| `003DB580` | SINIT — slot-array init on `q[+0xA0]` | **real** (183 B, 44 insns) |
| `003DB280` | TAIL — `call QWALK; shr b[+0x63],1` | **real** (23 B, 8 insns) |
| `003DB6E0` | QWALK — queue walk + `b[+0x14]&0x40` fixup | **real** (158 B, 41 insns) |
| `0020E600` | BASE — `eax=ecx + q[0x1F83530]` resolver | **real** (10 B, 3 insns) |
| `00265FF0` | boundary (rdx = `q[+0xB8]`) | scripted |
| `00265B60` | boundary | scripted |
| `00268380` | boundary ×2 (c0 block) | scripted |
| `002681E0` | boundary (link + c0 gate) | scripted |
| `003DBB60` | boundary ×4 sites (args captured) | scripted |
| `00268EA0` | boundary — **dead**: `b[+0xB]&8` masked off | scripted |
| `003DBDC0` | boundary — **dead**: `b[+0x63]==0` skips walk | scripted |

## Measured semantics (native execution, not static reading)

Head: `rsi = q[mgr]` (descriptor), `r11 = 0x120000`, `rbx = q[ptab + 8
+ idx*8]`, `r10 = idx`. `kind = b[rbx+3] & 0x1F`; `subf = b[0x01E0C329
+ kind*4]`; `subf==1` (kinds **2,4,7**) → `r15=6, ebp=8`, else
`r15=8, ebp=0xA`. `b[+0x14]&=0x7F`, `q[+0xEC]=0`, `b[+0xF5]=0xFF`.

RMAP jt `{0:A,1:B,2:B,3:C,4:C,5:D,6:D,7:D}`: A `+0xB8=+0xC0=0,
r8=REC+0x120`; B `+0xC0=0, +0xB8=REC+0x120, r8=+0x1A0`; C `+0xC0=0,
+0xB8=REC+0x120, r8=+0x140`; D `+0xB8=REC+0x120, +0xC0=REC+0x350,
r8=+0x4D8`. All arms `+0xA0=r8`, `+0xA8=r8+(0xA0 if subf==1 else
0xC8)`. Kind>7 → no writes (planted pointers kept).

KINIT jt `{0:0,1:0x38,2:0x38,3:0x40,4:0x40,5:0x30004,6:0x30004,
7:0x34C85}` → `d[+0x1C]`; kinds 5,7 also `b[+0x14]|=0x80`.

Flag chain (net effects on planted byte X): `b[+0xD] =
(X&0xA2|0x02)` then `mgr+0x28==0 → |0x80, else &0x7F`, then `&0xDF`;
`b[+8] = (X&0x9F|0x01)` then gate `|0x10/&0xEF`, then `&0x7F`;
`b[+0xC]=0x08` always; `b[+0xB]&=0xC0`; `b[+0x9]&=0x5F`;
`b[+0x13]&=0x3C`; `b[+0xE]=0xF0`; `b[+0x14]=(X&0xB0)|0x30`;
`b[+0xF]=0`; `b[+0x12]=0xFF`; `b[+0x15]=b[mgr+0x28]`; `b[+0xA]=0`;
`b[+0x20]=0xFF`; `w[+0]=idx`; `w[+4]=0xFF00`; `w[+0x10]=0`;
`w[+0x16]=1`; `w[+0x21]=0`; `w[+0xF6]=0`; `w[+0x100]=0`;
`w[+0x102]=w[+0x104]=0xFFFF`; `w[+0x106]=0`; `q[+0x28/0x30/0x38/
0x10C]=0`; `d[+0x18]=0xFFFF0000`; `d[+0x114]=0`; `d[+0x118]=0x3C0000`;
`q[+0xF8]=0x02F8F2A0`; `d[0x02F8F2A0]=0`. cls60 → `d[+0x1C]&=
0xFFFFDEFF` (applied to the KINIT value).

`b[+2] = (idx < w[desc + d[desc+0x14] + 2]) + 1` (signed setl).
`ent = desc + d[desc+0x18] + idx*(0x30 if w[desc]>=8 else 0x20) + 4`
→ `q[+0x40]`. Link block on `b[ent+6]`: bit7 set and `!=0xFF` →
`link = b&0x7F`; swap-out gated on `u32(s8(b[+0x12])) <= 3` (**dead** —
b12 was just set to 0xFF → -1); write-in unconditional →
`q[0x0209A1F0 + link*8] = rbx`, `b[+0x12]=link`,
`b[+0xF]=(link>3)+2`.

`q[+0x48] = resolve(d[ent+0x10]) + rsi`; `q[+0x50] =
resolve(d[ent+0x14]) + rsi`; `q[+0x58] = d[ent+8] + rsi` (zero-extend,
no resolve). `resolve(x) = x + q[0x1F83530]` = identity under zero
BSS.

SINIT(rbx, r15, ebp): `b[+0x88]=r15`, `d[+0x24]=0`, `b[+0x89]=ebp`;
ebp slots at `q[+0xA0]` stride 0x14 `{b[0]=i+1, b[1]=i-1,
d[+4]=0x80000000, w[+0x10]=0}`; first/last sentinels 0xFF; r15 bytes
of 0xFF at `+0x8C` and `+0x94`; `w[+6]=0`; `b[+0x63]=0`;
`w[+0x60]=0xFF00`. Then the A8 clear loop: `b[+0x88]` slots at
`q[+0xA8]` stride **0x28**, zeroing `q+0,q+8,d+0x10,w+0x14,b+0x16`
(0x17 bytes).

Boundary calls: `CFF0(rbx, q[+0xB8])`; `CB60(rbx)`; c0 block (if
`q[+0xC0]`): `q[c0+0x138]=0`, `d[c0+0x148]=1.0f`, `b[c0+0x14E]=1`,
`d[c0+0x140]=0`, `C8380`, `d[c0+0x144]=0`, `C8380`. Rep stosw
`w[+0xC8..+0xEC) = 0xFFFF` (0x12 words — **covers every site word**).
Link-valid + c0 → `b[c0+0x152]=0`, `C81E0`.

DBB60 sites (r9=2, stk0=0): `w[desc]>=0xA` gates **only site 1**
(`w[+0xE6]`; if `!=0xFFFF` literal u16 — dead under stosw; else
`bound< s16(w[tab])` where `tab = desc + resolve(d[ent+0x18])`, arg
`s16(w[tab+0x20])`; `edx=r15-1`; inc `b[+0x10]`). Site 2
unconditional (`edx=b88-1`, arg 0, inc). Site 3 unconditional
(`w[+0xDA]`, bound 9, arg `+0x14`, `edx=b88-1`, inc). Site 4
unconditional (`w[+0xCA]`, bound 1, arg `+4`, `edx=0`, **no inc**).

cls60 sites (`or`/`and` on `d[+0x1C]`, not calls): site 5 `w[+0xCC]`
bound 2 arg `+6` → ok `|4` else `&~4`; site 6 `w[+0xDC]` bound 0xA arg
`+0x16` → ok `|0x400` then `&~4` (clears site 5's bit) else `&~0x400`.
The `test b[+0xB],8` → `00268EA0` arm is **dead** — `b[+0xB]` was
masked `&0xC0` (bit3 always clear).

Tail `jmp 003DB280` → `QWALK` (`b[+0x63]==0` under ctor → immediate
return, `b[+0x14]` untouched, `003DBDC0` unreachable) → `shr
b[+0x63],1`.

## Execution findings (beyond the static reading)

1. **The ctor's `&0x1F` only bounds the subflag-table index** —
   RMAP/KINIT re-read `b[+0x3]` and apply their own `&0x1F`. Mutating
   it (`m-kind1f`) is observable only through which subflag byte is
   fetched — discriminated via kind `0x12` (table `!=1`) vs masked
   kind `0x02` (table `==1`).
2. **`w[desc]>=0xA` gates only site 1** — sites 2–4 are unconditional
   (site 4 uses `edx=0` and does not inc `b[+0x10]`). The earlier
   group-count reading was wrong: the gate is the descriptor field
   count.
3. **The cls60 "call sites" are flag ops** — `or`/`and` on `d[+0x1C]`
   gated by the same resolve+table compare; the arg word only feeds a
   sign check. Site 6's success path clears site 5's bit2
   (`|0x400` then `&~4`).
4. **The literal-word arms are dead** — the `rep stosw` writes
   0xFFFF over `+0xC8..+0xEB` before any site reads them, so every
   site's `w[+0xE6/0xDA/0xCA/0xCC/0xDC]` is always 0xFFFF and the
   `movzx` literal arm is unreachable under the ctor.
5. **Two scripted boundaries are unreachable from this ctor** —
   `00268EA0` (`b[+0xB]&8` is masked off earlier) and `003DBDC0`
   (`b[+0x63]==0` skips the queue walk before its call site).
6. **The link swap-out is dead; the write-in is not** —
   `b[+0x12]=0xFF` precedes the link block, so the old-record
   eviction (`u32(s8(b12)) <= 3`) never fires, but
   `q[0x0209A1F0 + link*8] = rbx` runs for every link `0..0x7F`.
7. **Registration cell** — `q[+0xF8] = 0x02F8F2A0` and
   `d[0x02F8F2A0] = 0`; the cell is BSS and stays zeroed.
8. **Subflag==1 kinds are exactly {2,4,7}** (shipped table read at
   `0x01E0C329 + kind*4`) → `r15=6, ebp=8` — smaller SINIT/A8 init.
9. **A8 clear stride is 0x28** over `b[+0x88]` (=r15) slots.

## Mutation campaign

46 byte-precise mutations across: flag masks (`&0x7F/&0x8F/&0xF0/
&0xFFFFDEFF`), kind/subflag (`&0x1F` index mask, `cmp 1`, `jne`),
manager gate (`+0x28` field, setl), entry (`shl4` stride, `+0x10/
+0x14/+8` fields, `+0x18` resolve base), pointer stores (`+0xEC`,
`+0xF5`, `+0x18`, `+0x118`, `+0xA8` stride `0x28`, `+0x148` field),
link (`js` write-in skip), stosw count, site1 gate bound, site words
and bound immediates (0xF/9/1/2/0xA), site arg displacements,
`inc b[+0x10]` field, cls60 `cmp 0x60` and `or4/or0x400` immediates,
RMAP arm-A `r8` displacement, KINIT kind0 value, SINIT `+0x88` field,
`0x80000000` tag, slot link value, QWALK `b63` compare, TAIL `shr`
field. **46/46 killed.**

Four initial survivors were fixture-coverage gaps, not equivalent
mutants:

- `m-kind1f` — needs a kind whose `&0x1F` vs `&0x0F` differ in
  subflag membership (kind `0x12` → masked `0x02`, which is a
  subflag==1 kind). Killed.
- `m-dc-arg` — the cls60 arg feeds only a sign check; needed the
  mutated displacement to land on a negative planted word
  (`tabw[0x18]=0x8000`). Killed.
- `m-b8-test` — `b[+0xB]&8` is provably dead; replaced with the live
  `js` write-in skip (`m-link-js`). Killed.
- `m-t*-cmp`/`m-dc-bound` bound mutations — share one compare word
  `w[tab]`; each needed a dedicated case where the planted compare
  word sits between the original and mutated bound. All killed.

## Limitations

- Deep boundary internals (`00265FF0`, `00265B60`, `00268380`,
  `002681E0`, `003DBB60`) are scripted — their argument values are
  captured in the trace, not their effects. `00268EA0`/`003DBDC0` are
  additionally unreachable from this entry point.
- `q[0x1F83530]` is planted zero → `resolve` is identity; a nonzero
  live-game base would offset the site compare/arg reads uniformly.
- `b[+0x63]` is always 0 under this ctor (SINIT clears it) → the
  QWALK body and `003DBDC0` are executed only to their early-exit;
  the walk itself is for a later package when a caller can plant a
  live queue.
- `bodies.json` holds body span + sha256 over shipped bytes;
  instruction-start coverage convention matches EXP-107–111.
