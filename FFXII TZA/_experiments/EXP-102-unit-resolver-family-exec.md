---
experiment: EXP-102
title: Unit-resolver family under isolated original execution
contract: ../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md
method: B
live_game: false
tool: evidence/unit-resolver-family-exec/check.py
---
# EXP-102 — unit-resolver-family-exec

**Status:** complete · **52/52 cases, 16/16 mutants, stable across three processes**
**Evidence:** `evidence/unit-resolver-family-exec/` (`check.py`,
`result.json`, `bodies.json`, `run.log`, `run2.log`, `run3.log`,
`gen_bodies.py`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The `0031B7xx`/`00263Exx`/`003588xx` neighbourhood is a coherent family of
small unit/handle/table resolvers clustered around the same pool and table
globals as EXP-101's `BattleStats_FindOwningBattleUnit`. Together they form
the lookup layer the battle/stat runtime resolves units, kinds, handles and
class ids through. This experiment executes **all seventeen bodies of the
family from shipped bytes — no scripted boundary exists anywhere in this
package**.

| VA | role | execution |
|---|---|---|
| `0031B770` | kind-to-unit sibling scan | **real** (106 B) |
| `0031B750` | byte accessor `unit+0xEA9` | **real** (8 B) |
| `0031B760` | null-safe `+0x30` follower | **real** (13 B) |
| `0031B7E0` | flag-gated handle resolver | **real** (42 B) |
| `0031B8C0` | TIDX-then-chain resolver | **real** (31 B) |
| `0031B8E0` | definition/kind resolver via VALID arm 2 | **real** (103 B) |
| `00263E30` | shared `[rcx+0x30]` accessor | **real** (5 B) |
| `00263E40` | `rcx + dword[rcx+0x4C] + sext(edx)` | **real** (14 B) |
| `00263E50` | nullable chain resolver to B750 | **real** (22 B) |
| `00263750` | 4-entry table index accessor | **real** (23 B) |
| `003588B0` | handle decoder | **real** (143 B) |
| `00263FF0` | family record indexer | **real** (21 B) |
| `00309440` | class lookup from handle bits | **real** (30 B) |
| `00322C50` | validity dispatcher (32 arms + tail) | **real** (1025 B) |
| `00236850` | pool count getter | **real** (7 B) |
| `00236820` | bounds-checked element getter | **real** (37 B) |
| `0020E600` | resolver base accessor | **real** (10 B) |

## Measured semantics (native execution, not static reading)

```
0031B770(cl):                          ; kind -> owning unit
  if (cl > 0x27) return 0              ; JA bound, kind space 0..0x27
  row = qword[qword[0x2EBF190] + 8] + cl*0x1C8
  for i in 0..COUNT()-1:               ; same COUNT/GET pair as EXP-101
    u = GET(i); if (u && u[0x698]==row) return u
  return 0                             ; first hit wins on duplicates

0031B750:   return byte [rcx + 0xEA9]
0031B760:   rcx ? jmp 00263E30 : 0     ; null-safe follower
00263E30:   return qword [rcx + 0x30]  ; shared tail for the family
00263E40:   return rcx + dword[rcx+0x4C] + sext(edx)
00263E50:   !rcx -> 0xFFFFFFFF         ; "or eax,-1", NOT a zero
            ![rcx+0x30] -> 0xFFFFFFFF  ; null chain also -1
            else jmp 0031B750          ; byte[chain+0xEA9]
00263750:   ecx > 3 -> 0 ; else qword[0x209A1F0 + ecx*8]

0031B8C0(ecx):                         ; TIDX then chain
  o = 00263750(ecx); !o -> 0
  else jmp 00263E30 -> o[0x30]

0031B7E0(rcx):                         ; feature-flag-gated
  !(byte[0x2089340] & 0x10) -> 0       ; flag clear: no decode at all
  h = 003588B0(rcx);  !h -> 0
  else jmp 00263E30 -> h[0x30]

003588B0(h):                           ; handle decoder
  !h -> 0                              ; entry token still fires
  tag = h>>20 & 0x7FF ; fam = h>>16 & 0xF ; idx = h & 0xFFFF
  fam >= 5 -> 0                        ; families 5..15 refused
  rec = 00263FF0(fam)                  ; = 0x2098E10 + fam*0x288
  checks in order: [rec+8] elems ptr, [rec] hdr,
          idx < [rec+0x20] bound, [rec+0x10]&1 live flag,
          idx < [elems] count, elem ptr != 0
  elem->u16[+0x16] != tag -> 0         ; stale-handle rejection
  else return elem object pointer

00263FF0:   return 0x2098E10 + sext(ecx)*0x288
00309440:   fam = (ecx & 0xFFFF) >> 12
            fam > 0xE -> 0xFFFFFFFF    ; "-1", unsigned in rax
            else dword[0x1EEBCF8 + fam*0x58 + tableoff]

00322C50(ecx, edx):                    ; validity dispatcher
  i = ecx - 1 ; i > 0x1F -> 0          ; 32 valid arms
  jmp jt[i]                            ; MSVC dword-RVA table @0x323054
  arm 0 (auto): CLS(edx) -> jt[cls-1]  ; re-dispatch on class
  arm 1 (deftab): edx < dword[deftab+4]
  shared tail: bound check + return

0031B8E0(id):                          ; kind byte resolver
  if (!VALID(2, id)) -> 0xFFFFFFFF     ; deftab-count bound via arm 2
  t = [0x2EBF130];  !t -> 0xFFFFFFFF
  r = 0020E600(dword[t+0xC]); !r -> 0xFFFFFFFF
  r2 = 0020E600(dword[t+0xC])          ; RESOLVE called TWICE, same arg
  a = r2 + word[t+8]*id ;  !a -> 0xFFFFFFFF
  return byte[a + 7]

0020E600:   return qword[0x1F83530] + ecx
00236850:   return dword[0x208E6A0]    ; EXP-101 pool globals, reused
00236820:   i<0 || i>count-1 -> 0 ; else [0x208E688] + i*0xF50
```

Findings measured by the suite:

- **KIND calls RESOLVE twice with the identical argument.** A successful
  `kind-ok` trace is `V2:2=1 R40=… R40=…`; the second resolve's result is
  what the `word[tab+8]*id + byte[+7]` addressing consumes. `kind-no-resolve`
  (resolve returns 0) shows only one `R` — the `test rax; je` between the
  calls is a real early-out.
- **KIND failure returns are `0xFFFFFFFF`, not 0** (`or eax, -1`), matching
  `00263E50`'s null-chain convention — both encode "no object" as -1 while
  the scan/accessor family uses 0.
- **The VALID auto-detect arm re-dispatches on the class result.**
  `VALID(1,id)` calls `CLS(id)` and jumps `jt[cls-1]`: `valid-auto-arm1`
  (id `0x2002`, class 2) lands on arm index 1 — the deftab-count bound —
  returning 1; `valid-auto-fail` (id `0x2005`, same class, count-exceeded)
  returns 0. The nested `c` token gets its `=2` annotation (the watch fires
  inside VALID's body) while the direct-entry `V` token does not — the
  function's return goes straight to the harness end address.
- **HDEC's family mask is 4 bits but only families < 5 are valid.**
  `hdec-fam5` (fam 5) and `hdec-fam8` (fam 8) both refuse; the mask mutant
  (0xF → 0x7) makes fam-8 wrap to fam-0 and diverges.
- **HDEC checks tag staleness last** — a structurally valid record with a
  dead element or live flag cleared still reaches the tag compare; only a
  tag match at `elem+0x16` returns the object.
- **`0031B7E0`'s flag bit is `0x10`** in the byte at `[0x2089340]`; with it
  clear, the handle is never decoded — no `H` token fires at all
  (`b7e0-off` trace is empty).
- **The `K` (kindscan) trace shows the EXP-101 getter pair reused** —
  `K3 n g0` for a hit at index 0 — confirming both scans share the
  count/base globals `[0x208E6A0]`/`[0x208E688]` and stride `0xF50`.

## Mutants

16/16 killed. The set covers the kind bound (`0x27` → `0x26`) and branch
polarity (`ja` → `jbe`), the kind-table stride (`0x1C8` → `0x1C0`), the
back-pointer offset (`+8` → `+0`), the table source (decoy at
`[0x2EBF198]`), B760's null guard (`jne` → `jmp`), B750's byte offset
(`0xEA9` → `0xEA8`), E50's null-chain polarity (`jne` → `je`), B7E0's flag
bit (`0x10` → `0x20`), TIDX's bound (3 → 2), HDEC's family mask
(`0xF` → `0x7`) and tag compare (`cmovne` → `cmove`), KIND's stride field
(`word[tab+8]` → `word[tab+0xA]`) and byte offset (`+7` → `+8`), CLS's
family shift (`>>12` → `>>13`), and the resolver base
(`[0x1F83530]` → decoy `[0x1F83538]`).

## Not claimed

- Callers of any family member are not executed; the package covers the
  resolver layer, not its consumers.
- What `unit+0xEA9`, `obj+0x30`, `elem+0x16`, or the def-table row bytes
  *mean* beyond the measured addressing is not established.
- VALID's other 30 arms are exercised only where reached (auto-detect
  re-dispatch and arm 2); their bodies execute but are not individually
  contracted here.
- The CLS table row layout beyond the family-indexed dword is not
  exercised.
- No live-process behavior; all tables, pools and records are authored
  fixtures.

## Files

- `check.py` — Unicorn harness; whole image mapped, pool/table globals
  planted in `.data`, authored-data arena `0x50000000`.
- `gen_bodies.py` — CFG span walker (dword-RVA jump tables seeded).
- `result.json` — per-case traces/observables + mutant outcomes.
- `bodies.json` — span + sha256 of the seventeen real bodies.
