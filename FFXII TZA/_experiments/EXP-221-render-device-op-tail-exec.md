# EXP-221 — `181xxx` emit-tail wrappers → `1Bxxxx` render-device methods (op tail real)

**Status:** complete — **540/540 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256 `c3f4e69217` prefix; 540 cases),
zero unexpected faults** (the 10 faulted cases are the same pre-existing
intentional-null fixtures that assert the fault).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..220; +4 cases this round)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

| body | semantics |
|------|-----------|
| `001B1C00` | render-device singleton getter (2 insns): `return q[0x1F811E8]`. Called once per wrapper plus once per `181460` inner iteration (11 hits per emit tail). |
| `00181560` | thin wrapper: `sub rsp,0x28; call 1B1C00; jmp 1B1910`. |
| `001B1910` | device reset: `1B0100(dev)` → `861EC0` memset hook on `dev+0x3930`, size `0x178`, fill 0 → `d[dev+0x3A4C/50/54/58] = 0x80` ×4. |
| `001B0100` | slot-clear loop: for `edx` in `0..d[dev+0x3928]` (signed), resets the `0x58`-byte record at `dev+0x2328+idx*0x58` — `q[+0x40]=q[+0x38]` (end=begin), `q[0]=0`, `q[8]=0`, `d[+0x10]=1`, `q[+0x14]=1`, `q[+0x20]=0`, `d[+0x1C]=0`, `d[+0x28]=0`, `d[+0x2C]=1`, `d[+0x30]=1` — then `d[dev+0x3928] = −1`. Negative cursor early-outs to the same −1 write. |
| `001819A0` | arg-shuffling wrapper: `1B2410(dev, edx=ecx, r8d=edx, r9=r8)` plus six stack dwords `{0, orig_r9d, caller_starg, 1, 0, 0}` staged at `[rsp+0x20..0x48]`. |
| `001B2410` | texture-region props: `d[+0x3930]=edx`, `d[+0x3934]=r8d`; `r9==0` → `b[+0x3938]=0`, else `17D2E0(dev+0x3938, r9)` name copy; then six caller stack dwords → `d[+0x3AA0]`, `d[+0x3A38]`, `d[+0x3A3C]`, `d[+0x3A40]`, `d[+0x3A44]`, `d[+0x3A48]`. |
| `0017D2E0` | string-copy wrapper: `16D670()` → `q[0x1EBA3D0]` (CRT options global) `| 1` → calls through `q[0x8C2F08]` with `(rcx=opts, rdx=dst, r8=-1, r9=src, [20]=0, [28]=&stashed)` — `__stdio_common_vsnprintf_s`-shaped (options OR, `_TRUNCATE` size, va_list). The call target stays a scripted sink (`scrtfmt`) performing the byte copy; negative eax → `cmovs eax,-1`. |
| `0016D670` | leaf: `return &0x1EBA3D0` (CRT options global address). |
| `00181870` | thin wrapper: `1B2490(dev, edx=ecx)`. |
| `001B2490` | mode-table write: `d[dev+0x3A60] = d[0x8F80F8 + edx*4]` — shipped table `[0,1,6,2,3,4,5,0]`; emit tail passes edx=3 → **2**. |
| `00181460` | vertex-batch wrapper: `edx−2` outer × fixed-3 inner loop calling `1B1C00()`+`1B06D0(dev, rec)` per `0x30` record; source walks `rcx` with stride `0x30` and wraps (`outer1` re-reads `+0x30` — records land `[s0,s30,s60,s30,s60,s90]` for edx=4). `edx≤2` → no-op. |
| `001B06D0` | slot-vector append: cursor `d[dev+0x3928]` — `<0`, `>0x3F`, or `q[slot]!=0` → seal: `inc` cursor, init fresh record (`d[+0x10]=1`, `q[0]=0`, `q[8]=0`, `q[+0x2C]=0`, `q[+0x20]=0`, `d[+0x1C]=0`, `d[+0x28]=0`, `q[+0x14]=1`, `q[+0x40]=q[+0x38]`); append `0x30`-byte record (three `movaps`) at `q[slot+0x40]`, `end+=0x30`; full → `jmp 1AED50(slot+0x38, end, rec)`. |
| `001AED50` | `vector<0x30-rec>::insert`/`_Emplace_reallocate` (≈50 insns): non-grow shift-insert; grow doubles capacity (`max(1,2·count)` via `0x2AAAAAAAAAAAAAAB` magic), allocator fn `q[q[vec+0x18]+8]` (`rcx=&vec+0x18`, `rdx=newcap*0x30`, `r8=0x10`), three-copy splice, dealloc `q[q[vec+0x18]+0x18]` on the old block, stores begin/end/cap. |
| `001816B0` | thin wrapper: `1B22D0(dev, rcx)` → `q[dev+0x3A68]=rdx`. |
| `00181910` | thin wrapper: `1B22E0(dev, rcx)` → `q[dev+0x3A70]=rdx`. |

## Emitted evidence in `c5f0-f3f`/`c5f0-f42`

Both emit tails now run the full op sequence on the planted
`q[0x1F811E8]` device: reset (`rdcur=1` → `1B0100` clears slots 0–1 then
−1), props (`r8=name ptr → 17D2E0` copy into `+0x3938`), mode write
(`d[+0x3A60]=tbl[3]=2`), six `1B06D0` appends with two real `1AED50`
reallocs (cap 2→4→8; `s2alloc`/`s2dealloc` scripted sinks ×2 each),
`q[+0x3A68]=0x44`/`q[+0x3A70]=0` stores. Asserts verify the copied
`0x30` records land byte-equal in the grown vector, the slot-reset and
append-init patterns differ as shipped (`d[+0x2C]` 1 vs 0), and the
memset/`0x80` seeds/prop fields land at `+0x3930`…`+0x3AA0`.

## Corrections of record

- **`s1819a0`'s string arm does fire** in `f3f`/`f42`: the name pointer
  is the wrapper's `r8` (recorded `0x40034C40`), forwarded as `1B2410`'s
  `r9` — nonzero → `17D2E0` runs. The earlier resume note claiming the
  `r9==0` path was wrong (it read the wrapper's `r9`, not the forwarded
  `r8`).
- **`181460` is not a thin wrapper** — it's a `(edx−2)×3` nested loop
  over `1B1C00`+`1B06D0` with the source cursor re-reading `+0x30`
  per outer iteration.
- **`1B0100` vs `1B06D0` init patterns differ** — reset writes
  `d[+0x2C]=1, d[+0x30]=1`; append-init writes `q[+0x2C]=0` and leaves
  `+0x30` alone. The two patterns now distinguish which path a slot saw.
- **`1AED50`'s allocator is a fn-ptr struct, not a vtable** — alloc at
  `q[obj+8]` (vs `1E7A20`'s vtable `+0x10`), dealloc at `q[obj+0x18]`,
  `this` = `&vec+0x18` (address of the embedded pointer, not the object).
- Direct-entry `entry` skips the caller's `rargs` record — entry-point
  tags must not be counted in asserts (only their callees are recorded).

## New fixtures (all disclosed synthetic)

- `rdev` (`q[0x1F811E8]`, 0x4000): `d[+0x3928]` cursor (`rdcur` case
  key, default 1 so `1B0100`'s loop runs); slot records at `+0x2328`
  stride `0x58`.
- `rvbuf`/`raobj`: slot0's planted sub-vector — begin/end `rvbuf`,
  cap `rvbuf+rvcap` (default 0x60 = 2 records → grow on append 3/5),
  allocator fn-ptr struct `raobj` (`+8`→`0x7000A110` `s2alloc`,
  `+0x18`→`0x7000A118` `s2dealloc`); slot1 carries `raobj` too so the
  seal path's empty-vector grow resolves.
- `rsrc`: eight `0x30` source records with distinct qwords
  (`0x1100+i*0x100+j`) making append copies byte-checkable.
- `rname` `"RDEVNM"`: name source for the `1B2410` `r9≠0` arm.
- `scrtfmt` sink at `0x1CCECB4` (the `q[0x8C2F08]` target): byte-copies
  `r9`→`rdx` to NUL, bounded at `0x168` (the `+0x3938` field extent to
  `+0x3AA0`), returns count. Disclosed stand-in for the CRT
  `vsnprintf`-family callee — semantics verified only as string copy;
  no `%` conversion exercised by the fixtures.
- `s2alloc`/`s2dealloc` scripted VAs at `0x7000A110`/`0x7000A118`:
  bump-alloc via `self.alloc(0x400)` (distinct buffers per call) and a
  sink — same disclosure class as EXP-220's `salloc`/`sdealloc`.

## New cases (4)

- `rdev-append` — `181460` entry, edx=4 → 6 appends into slot0's
  cap-2 vector; two real `1AED50` reallocs (2→4→8), all six records
  verified byte-equal against `rsrc` at the `{0,30,60,30,60,90}`
  offsets.
- `rdev-seal` — `1B06D0` entry, `rdcur=0` + `q[slot0]=1` → seal, bump
  to slot1, append-init pattern, `1AED50` empty-vector grow (alloc ×1,
  no dealloc — begin was null).
- `rdev-props` — `1819A0` entry, `rcx=0x11/rdx=0x22/r8=rname/r9=0x33`
  → `d[+0x3930]=0x11`, `d[+0x3934]=0x22`, `"RDEVNM"` at `+0x3938`,
  `d[+0x3A38]=0x33`, `d[+0x3A40]=1`, zeros elsewhere.
- `rdev-reset` — `181560` entry, `rdcur=2` → `1B0100` clears slots
  0–2 (verified field-by-field), cursor −1, memset hook `[rdev+0x3930,
  0x178]`, four `0x80` seeds.

## Remaining scripted boundaries (unchanged class)

- `181330` → `1B03D0` (~148 insns, multi-callee: `16D6A0`, `182F50`,
  `1A1470`, `1B0100`, `1FB810`/`1FB840`/`1FB870`, `229DE0`) — the one
  emit-tail op left scripted.
- `scrtfmt` — the `q[0x8C2F08]` CRT target (`__stdio_common_vsnprintf_s`
  or sibling): approximated as a bounded byte copy; the options global
  `q[0x1EBA3D0]` and `%`-conversion semantics are unverified.
- `s2alloc`/`s2dealloc` — slot-vector allocator internals.
- `19C5D0`/`1C5F20` (`1E94E0` flag-0 init), `2AC2F0`, sibling thunks
  `17F850`/`17FA10`/`17FB00`/`17FD30`, `3FFDF0`, `254A10`, `861EC0`
  memset hook — unchanged from EXP-220.

## Next candidates (EXP-222+)

- `1B03D0` — the last scripted emit-tail op (deep; needs its callee
  set modeled first).
- `1E94E0`'s flag-0 arm — the `19C5D0`/`1C5F20` lazy-init chain.
- Sibling thunks `17F850`/`17FA10`/`17FB00`/`17FD30` → `1E9920`,
  `1E9C80`, `1E9D20`, `1E8580`/`1EB150`/`1EB110`.
- `2AC2F0` control-code decoder — the remaining scripted interpreter
  boundary.
- `2A9F00`'s glyph-loop gate — the only natural `17F7C0` path.
- `17D2E0`'s CRT target — identify `q[0x8C2F08]`'s import and verify
  semantics beyond plain string copy.
