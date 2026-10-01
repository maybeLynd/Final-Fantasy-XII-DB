---
experiment: EXP-110
title: Phyre script-execution callers — three loader callers (00684D10 / 00684F60 / 00686280) under isolated original execution
contract: ../23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md
method: B
live_game: false
tool: evidence/phyre-script-callers-exec/check.py
---
# EXP-110 — phyre-script-callers-exec

**Status:** complete · **48/48 cases, 38/38 mutants, stable across three
processes**
**Evidence:** `evidence/phyre-script-callers-exec/` (`check.py`,
`result.json`, `bodies.json`, `run.log`, `gen_bodies.py`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-lua-chunk-loader` named three unread Phyre script-execution
callers feeding the chunk loader `00683C30`. This experiment executes
all three shipped bodies — plus the nine real TValue-stack leaves they
reach — under Unicorn and diffs them against an independent model on
return values, boundary-call traces, pool checkout/cursor state, Lua
stack top pointers, full 16-byte TValue slot images (including stale
bytes), copied pool bytes, and out-parameter `{q value, field}` writes.

| VA | role | execution |
|---|---|---|
| `00684D10` | D10 — script-execute wrapper, `0x2E41050` pool checkout | **real** (585 B) |
| `00684F60` | F60 — script-execute wrapper, setfield + optional second pcall | **real** (470 B) |
| `00686280` | C280 — two-pool caller + vararg marshal + result dispatch | **real** (1447 B) |
| `0080FD00` | GETTOP — `(top − frame)/0x10` | **real** (19 B) |
| `00811130` | SETTOP — top-pointer move, no byte clear | **real** (71 B) |
| `00810450` | PUSHB — push boolean `{d0=!!v, ty=1}` | **real** (27 B) |
| `00810580` | PUSHI — push integer `{d0=f32(v), ty=3}` | **real** (28 B) |
| `00810640` | PUSHN — push number `{d0=f32(f64), ty=3}` | **real** (20 B) |
| `008105A0` | PUSHP — push light userdata `{q0=p, ty=2}` | **real** (19 B) |
| `008113D0` | TOBOOL — nil→0, number 0→0, else→1 | **real** (147 B) |
| `008119F0` | TYPE — `d[slot+8]&0xF` | **real** (121 B) |
| `006372A0` | SING — returns shipped const `0x02CF8270` | **real** (7 B) |

Scripted boundaries (entry-intercepted, args captured, planted returns):
`00683C30` LOAD (chunk loader — the contract's subject, exercised
through its callers), `00810340` PCALL, `00811530` ERRSTR, `005CDAA0`
LOG, `0080FB20` PUSHLS, `00810730` IDXOP, `00810ED0` SETFLD (popped
slot's type tag recorded — the real consumer of PUSHP's tag),
`00682AA0` COPY (185-insn deep copy), `00682D20` MARSH, `006811B0`
ITER, `00681010` DISP, `0080F420` GROW, `006810B0` GETA, `00681130`
GETB, `00811470` TONUM, `00636920` MSHL, `00861EBA` CPY86, and the
twelve TLS singleton getters `SENTS[0..11]` (`gs:[0x58]` reads —
cannot run under Unicorn; each returns a planted token `SENTB+k*0x10`).

## Measured semantics (native execution, not static reading)

TValue = 16-byte slot `{q0 value, d8 type-tag}`; state exposes
`q[state+0x20]` = frame base and `q[state+0x10]` = top pointer.

### D10 `00684D10(obj, buf, ...)`

```
env = q[obj+8] ; name = env + 0x50 ; st = q[env]
hdr = q[0x2E41050]                      ; element pool header
if hdr:
    cur = d[hdr+8] & 0x7FFFFFFF          ; capacity masked at bit31
    if cur < cap: elem = q[hdr] + cur*0x28 ; elem++ consumed
if elem && q[elem+0x20]: buf = q[elem+0x20] ; pool buffer wins
LOAD(buf, name) -> 0 on fail: ret esi (uninit/0xFFFFFFFE seen)
GETTOP; PCALL(st, 0, -1, 0)
fail: ERRSTR(-1); LOG(0xD6FEB0, r, str, 0); SETTOP(-2); ret
same buf: IDXOP copy loop / diff buf: COPY deep-copy (scripted)
PCALL again; esi = GETTOP - orig_depth    ; result-count delta
pool slot cursor-- iff cursor lands on checked-out slot
```

### F60 `00684F60(obj, buf, idx)`

```
env = q[obj+8] == 0 -> ret 7 ; q[env] == 0 -> ret 1
st = q[env] ; LOAD(buf, env) == 0 -> ret esi (9 observed)
PUSHP(st, env)                            ; {q0=env, ty=2}
SETFLD(st, 0xD701A0)                      ; pops the userdata TV
PCALL(st, 0, 0, 0)
fail: ERRSTR(-1); LOG(0xD6FFD8, r, str, 0); SETTOP(-2); ret
o20 >= 0: IDXOP; packed-string lookup via 8-stride string table;
          second PCALL(st, 1, 0, 0); fail -> same error path
```

### C280 `00686280(obj, vario, rtag, ...)`

```
env = q[obj+8] ; name = env + 0x50 ; st = q[env]
for hdr in (q[0x2E41020], q[0x2E41050]):   ; two-pool search
    cur = d[hdr+8] & 0x7FFFFFFF
    if cur < cap && state-check fails: elem = q[hdr] + cur*0x28
vario == 0 -> ret 0
PUSHLS(st, packed)                        ; declared nil push
if TYPE(-1) == 0 -> ret 0                 ; nil result bails
LOAD(elem_buf or arg, name); PCALL
marshal loop per vararg element: tag compared against SENTS[0..11]
  in order; s0 -> PUSHB, s9/s10 -> PUSHN, everything else -> PUSHI;
  unmatched -> DISP (+ LOG 0xD6FEE0 when it declines)
PCALL(st, 1+nargs, 1, 0); fail -> error path
result dispatch on rtag against SENTS[0..8] only:
  s0:    TOBOOL(-1) -> byte  [r14+8] = !!v        ; r14 = vario
  s1,s2: TONUM(-1) -> byte  [r14+8] = al
  s3,s4: TONUM     -> word  [r14+8] = ax
  s5,s6: TONUM     -> dword [r14+8] = eax
  s7,s8: TONUM     -> qword [r14+8] = rax
  else:  GETA(rtag,...) -> {q,b} / GETB -> {q,b} /
         rtag == SING|1 -> MSHL q-result /
         unknown -> LOG(0xD6FF20, r14=vario, 0, 0), ret 0
q[r14] = 0 on all direct arms              ; out-param {0, value}
pool slot cursor-- iff cursor == checked-out slot
```

## Execution findings (beyond the contract's static reading)

1. **Result store sizes are 1/2/4/8, not 1/4/8** — the s3/s4 arm is a
   `word` store (`mov [r14+8], bx`), distinct from s5/s6's `dword`.
   A static grouping of "small numeric" arms reads it as dword.
2. **Result dispatch compares only SENTS[0..8]** — the sentinel loop
   bound is 9, not 12; s9/s10 (number sentinels in the marshal) and s11
   fall into the GETA/GETB/MSHL/unknown fallback instead.
3. **Marshal s11 is a PUSHI arm, not a dedicated pusher** — only three
   typed pushes exist in the marshal loop: PUSHB (s0), PUSHN (s9, s10),
   PUSHI (all other matched tags). The DISPATCH helper `00681010` is
   invoked only for unmatched tags.
4. **Stack pops preserve bytes** — SETTOP and the pcall-side pops move
   `q[state+0x10]` only; popped TValue images stay resident and are
   re-observable if the top revisits the slot. The model must keep
   slot storage indexed independently of logical depth (negative
   depths occur: pcall can push top below the frame base).
5. **`006372A0` is a constant getter, not a TLS read** — it returns the
   shipped constant `0x02CF8270` (verified in `bodies.json`); the
   `SING|1` compare in the dispatch is against `0x02CF8271`.
6. **Null-state checkouts stay consumed** — C280 checks out exactly one
   element per pool even when the element's state fails its gate; the
   cursor advances regardless (`c280-nullstate-skip`).
7. **C280's cursor holder points directly at the payload array** — the
   marshal reads `q[holder + i*8]` with no second indirection.
8. **Unknown-result LOG uses leftover `r14` (= vario) as r8** — not a
   recomputed argument; visible only in the trace.
9. **D10's early-exit `esi` is uninitialised** — observed `0xFFFFFFFE`
   on the loader-fail path, matching the register's leftover state.
10. **SETFLD consumes PUSHP's type tag** — the popped slot's `d8` is
    the only path by which the light-userdata tag (`ty=2`) is
    observable; recorded by the stub to kill `m-pp-ty`.

## Mutation campaign

38 byte-precise mutations across all three subjects and eight leaves —
payload masks, null-gate inversions, capacity bit31→30 masks, element
stride/field repoints, pcall arg counts, copy-back counts, pool-pop
slot compares, dispatch result offsets (`+8` on the byte, word and
qword arms), marshal cursor stride and arg-counter direction, `SING|1`
constant, ret-code constants, string-table index scale, and leaf
semantics (GETTOP stride/bias, SETTOP stride, pusher type tags and
top-advance, TOBOOL nil gate, TYPE tag mask, SING constant).
**38/38 killed.** Three initial findings were harness gaps, resolved:

- `m-d10-nargs` → VA off by one (opcode byte at `0x684EC5`).
- `m-c280-b8` → repointed to the s0 arm's store at `0x686680`; the
  original site was the s1 arm's store — unreachable under `rtag=SENTB`.
  Resolved alongside the s3/s4 word-arm correction + `c280-res-word`.
- `m-pp-ty` (PUSHP tag 2→3) → the pushed slot is overwritten by the
  pcall result in every f60 case; the tag is observable only through
  the SETFLD consumer. The stub now records the popped slot's `d8` in
  the trace (`f<state>:<name>:<ty>`), which is what real
  `lua_setfield` reads.

## Limitations

- TLS singleton getters are scripted: `gs:[0x58]` cannot be emulated
  under Unicorn, so the twelve sentinels are planted tokens
  (`SENTB+k*0x10`); their get calls are traced, their returns planted.
- The chunk loader `00683C30` itself is a boundary — this package
  exercises its callers, not its internals (the contract's separate
  subject).
- Pool element state checks and the second-pcall argument formation
  are modelled at the observed boundary; interior pcall behaviour is
  planted per case.
- `bodies.json` holds per-body spans + sha256 over the shipped bytes;
  coverage is instruction-start ratio, same convention as EXP-107–109.
