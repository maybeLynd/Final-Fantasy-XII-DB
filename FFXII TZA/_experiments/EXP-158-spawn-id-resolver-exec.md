---
id: EXP-158
title: "ID resolver 3008A0 — spawn-bitmap update + active-set registration"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp158_check.py
result: 102/102 (stable x3)
---

# EXP-158 — `3008A0` id resolver, executed

`003008A0` is the sibling immediately after `300530` (which ends at
`0x30089F`). It resolves a 16-bit entity id through the class-descriptor
table `0x1EEBCC0` (stride `0x58`), invokes the row's `+0x48` callback —
for class `0xC`, the spawn-bitmap **mutator** `2FD420` — and, when the
dispatch gate is armed, ORs spawn-state flags into a shared state object.

## Signature and flow

`3008A0(cx=id, edx=delta, r8d=mode, r9d=dispatch, a5=flag)`:

```
id==0xFFFF || id==0x1000 || (id&0xF000) > 0xE000 -> ret -1
row = 0x1EEBCC0 + (id>>12)*0x58
if (id&0xFFF) > d[row+0x3C]-1 -> ret -1
ebp = 309F30(id, dispatch)                    # validator dispatch
esi = q[row+0x48](id, delta, mode, flag)      # mutator callback
if dispatch==1 && ebp<=0 && esi>0:
    cls = id>>12
    cls==3   -> q[0x2EBF190]+4 |= 1 + 20E600-walked tbl mask
    cls==4   -> q[0x2EBF190]+4 |= 0x40
    cls==0xC: id<=0xC011 -> |=0x80 ; 0xC012..0xC01E -> |=0x100
ret esi
```

`309F30(id, mode)` is the **shared validator dispatcher** — the same
validator path `30B0E0` inlines: `mode==4` jumps straight to `2FD970`,
otherwise `jmp q[row+0x50]` (cls-0xC ships `0x2FD970`, the spawned-bitmap
query).

## `2FD420` — cls-0xC spawn-bitmap mutator (executed)

`2FD420(id, delta=edi, mode=esi, flag=stack)`:

```
bmp   = q[row+8]                       # runtime bitmap, planted
old   = bt w[bmp + (id&0xFFF >>4)*2], id&0xF
ecx   = mode==0 ? old+delta : delta
ecx < 0   -> btr ; ecx > 1 -> bts
else ebx = mode==0 ? old+delta : delta ; ebx==0 -> btr else bts
w[bmp word] updated; 325F40(id, old, ebx)   # change notify
mode==0 && flag&1 -> 46A630(id, delta)      # -> scripted 46AB10
ret ebx
```

Proven live: `foe` (bit set, delta 0) stays `0x7FFC` ret 1; `clear`
(delta −1) → `0x7FF8` ret 0; `set` (bitmap 0, delta 1) → `0x0004` ret 1;
`neg2` (delta −2 → ecx<0 direct-clear) → `0x7FF8`; `mode`/`mode0`
isolate the mode≠0 absolute-write path; `flag4`/`flag4clr` prove the
`46A630` → `46AB10` post-notify (edx selects `0x24`/`0x25`).

## `325F40` — change-notify router (executed, early-ret path)

Validates via `322C50(1, id)` — cls-0xC foe ids fail the cls-1 bound and
return early (no notify) — proven by trace: `n325f40` runs, `v309440`
bound resolver executes, no `call rsi` arm reached. The notify arms
(`rsi ∈ {0x252E60, 0x252FD0}`) are exercised only for classes the gate
accepts; `252E60` stays scripted (it contains the 19-call `2CD650`
batcher), `252FD0` is a real 5-insn leaf in the real map.

## Dispatch arm — active-set registration (executed)

Gate: `dispatch==1 && validator(id,1)<=0` (not already spawned) `&&
mutator ret>0` (bit now set). Then `q[0x2EBF190]` is a state object
whose `+4` dword accumulates class flags:

- cls 3 (member): `|=1`, then a `20E600` descriptor chain computes
  `tbl[0x1EECF98 + (w[row+0x2C]&7)*4]` and ORs it in too.
- cls 4: `|=0x40`.
- cls `0xC` id `≤0xC011`: `|=0x80` — the `0xC000..0xC011` reserve band.
- cls `0xC` id `0xC012..0xC01E`: `|=0x100` — the 13 live foe slots.

Proven: `foeflag` (id `0xC012`, clear bit, set) → `cell+4 & 0x100`;
`foe80` (`0xC011`) → `&0x80`; `foeend` (`0xC01E`) → `&0x100`.

So `3008A0` is not a lookup — it is the **spawn-bit update plus
active-set registration** call: update the class bitmap, notify on
change, and (dispatch mode) set the class flag on the state object.

## Real layer added

`3008A0` (subject), `309F30`, `2FD420`, `325F40`, `309440` (the
`322C50` bound resolver), `46A630`, `252FD0`. Scripted: `46AB10`,
`252E60`, plus the whole inherited boundary set from EXP-157.

## Boundary disclosure

Fixture recs/bitmap/state-object cell are planted; runtime-only pointers
(`q[row+8]` bitmap, `q[0x2EBF190]`) are disclosed. `46AB10`/`252E60`
returns are scripted. MODEL-PROVEN/NATIVE-REPLAY evidence only — no
initialized-gameplay claim.
