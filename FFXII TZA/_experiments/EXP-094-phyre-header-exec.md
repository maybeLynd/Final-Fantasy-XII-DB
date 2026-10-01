---
experiment: EXP-094
title: Phyre cluster header load under isolated original execution
contract: ../22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md
method: B
live_game: false
tool: evidence/phyre-header-exec/check.py
---
# EXP-094 — phyre-header-exec

**Status:** complete · **25/25 cases, 10/10 mutants, stable across two processes**
**Evidence:** `evidence/phyre-header-exec/` (`check.py`, `result.json`,
`bodies.json`, `run.log`, `run2.log`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-phyre-cluster-header.md` (Phyre `PSerialization::PBinary`
`PClusterHeader` load) modeled the descriptor `0x2CAA0A0` as opaque and the
byte-swap as scripted. Native analysis identified `0x2CAA0A0` as the real
reflection descriptor
`Phyre::PClassDescriptorConcrete<Phyre::PSerialization::PBinary::PClusterHeader>`;
the loader `0059A3B0` itself does `lea rcx,[0x2CAA0A0]` and calls the
descriptor walker `0063E2E0` on the raw header buffer. This package re-drives
the whole ladder from shipped bytes: real descriptor construction, real
descriptor-driven member swap, real namespace block swap, real stream
accounting — with disclosed fixtures only at the stream I/O boundary and the
deferred reflection member graph.

## Executed bodies (real shipping bytes)

21 bodies, spans + sha256 in `bodies.json`. Headline set:

| VA | role |
|---|---|
| `00160210` | static-init: registers the PClusterHeader descriptor |
| `00597690` | descriptor ctor — `PClassDescriptor` setup, member slots |
| `00632D80` | descriptor body init (size `0x54`, parent link `0x2CA9DA0`) |
| `006373D0` | TLS/lazy-init context getter (gs:[0x58] slot machinery) |
| `0063DC80`/`0063DF90`/`0063DFA0` | member registrations into `0x2CA9C00`/`+0xC60`/`+0xCC0` |
| `0059A3B0` | **the loader** — read `0x54` hdr, marker, descswap, ids, ns, ext |
| `0063E2E0` | descriptor walk entry — fwd/rev member list + parent chain |
| `0063CE80` | per-member dispatch — flags/kind gate, offset calc, resolver |
| `0059FDB0` | per-element engine — `call [typeVtbl+0]`, stride `[typeObj+0x38]` |
| `0059A6F0` | ns read wrapper — stream read + accounting + swap dispatch |
| `0059C180` | ns orchestrator — fixed dwords + sub-record + counted tail |
| `0059A780` | counted `0x24`-byte record swapper |
| `0059A8B0` | SSE2 dword byte-swap table + scalar tail |
| `00686D00`/`0069E780` | id1/id2 constant getters |
| `0067B100` | gvec growth for extended headers |
| `0017D260`/`00584730` | ns buffer alloc/free (real; sink to stubbed heap pair) |
| `00861EBA` | `memcpy` IAT thunk (real thunk → fixture memcpy) |

## Stubbed boundaries (all disclosed)

Patched to `ret`, args logged:

| VA | role |
|---|---|
| `0019C580` | heap alloc sink (bump arena backstop) |
| `0019C570` | heap free sink |
| `00808B90` | CRT `atexit` inside static init |
| `008092FC`/`0080929C` | lazy-init acquire/release in `006373D0` (not taken) |

## Fixture boundaries (disclosed)

- Stream object: vtbl `+0x10` ready leaf, `+0x28` read leaf
  (`min(len,remaining)` copy, cursor advance) — legitimate I/O boundary; no
  shipped memory-stream class exists to run instead.
- Member-node graph: `00160210` builds the descriptor but leaves `+0x80`
  self-linked — member registration is deferred finalize machinery too deep
  to replay. Nodes spliced into `desc+0x80` (and `0x2CA9DA0+0x80` for the
  parent arm) per the layout decoded from `0063CE80`.
- Member-type objects/vtables: `+0x00` vtbl (slot `+0` = swap leaf),
  `+0x38` stride. Swap leaf logs `(addr,flag)` and performs a real `bswap`.
- `memcpy` IAT slot `0x8C2A68` → fixture routine.
- TLS: `gs:[0x58]` slot array, slot[idx] ctx with `ctx+4` count vs
  `0x2CF94EC` lazy-state; returns real `0x1F2E330` contents.

## Findings (native-verified semantics)

1. **Loader ABI**: `(rcx=stream, rdx=hdrbuf, r8=nsRec{+0 cap|bit31,+8 buf},
   r9=gvec{+0 size,+8 buf}, arg5=swapFlag*, arg6=outLen*, arg7=idGate)`.
2. **arg7 is an input gate**: the real caller `0059E070` sets it to `1`,
   enabling the id compares unconditionally — ids are validated even on
   native-endian headers (`le-badid1` → 6). `arg7=0` tolerates wrong ids
   (`arg7-skip-ids` → 0).
3. **Null `nsRec.buf` is a hard error (6) regardless of ns length** —
   `test r13,r13` at `0x59A4D3` precedes the length paths.
4. **Error codes**: `9` short header/ns/ext-tail read; `6` bad marker
   (post-swap retest), bad ids, null nsbuf, `nsSize < 0x54−outLen`;
   `0xD` alloc/gvec-grow failure; short-header return is `0x54−0x4B=9`.
5. **`outLen` field (`hdr+4`)** three-way dispatch: `==0x54` → plain ns
   read; `>0x54` → `0067B100` grows `gvec`, whole header copied to
   `gvec.buf`, `outLen−0x54` tail streamed in; `<0x54` → header tail
   `memcpy`'d into `nsRec.buf`, requires `nsSize ≥ 0x54−outLen` else 6.
6. **Double swap**: when the swap flag was set *and* `outLen!=0x54`, the
   loader runs `0063E2E0` a **second** time on the header before the
   ext-tail read (`be-ext`: 10 leaf hits = 5 members × 2 passes).
7. **`0063E2E0` walk**: `r8b` flag — `1` forward via `desc+0x80` fwd links,
   `0` reverse via `+0x88` back links; then `desc+0x78` parent chain
   repeats the same walk (`walk-parent` ordered own-then-parent).
8. **`0063CE80` member gate**: node `+0x28` flag bit1 skips the member;
   kind `[declType+0x5C]` selects count (`1`→`[vtbl+0x38]` size fetch,
   `2`→requires bit6); dest = `data + node+0x48 − classDesc+0xF4`;
   resolver `node+0x50` may override the type object.
9. **`0059FDB0` engine**: `count` elements, leaf `call [typeVtbl+0]` with
   `(rcx=typeObj, rdx=elem, r8b=flag)`, `elem += [typeObj+0x38]`, `bl |= al`.
10. **ns swap is real specialized code**: `0059C180` byte-swaps 8 fixed
    dwords, walks a counted `0x24`-record table (`0059A780`, mixed
    bswap/shift-mask fields), then SSE2-swaps the dword tail
    (`0059A8B0`). `ns-swap-full` produces byte-exact LE output.
11. **Stream accounting `stream+0x18` is cumulative** across header, ns
    and ext-tail reads (`mut-acct` kills it at both sites).

## Mutation campaign

10 mutants, all killed: marker immediates at **both** compare sites
(`0x59A401`, `0x59A41B`), header size `0x54`, stream accounting (both
`add` sites), forced id-gate (`movzx dil` → `mov edi,1`), walk direction
`je`→`jmp`, ns fixed-dword `bswap`, per-element vtbl deref (faults on
`call [0]` — expected kill), member-flag offset `+0x28`→`+0x2C`,
ns short-read compare, parent-recursion `jne`→nop.

## Harness bugs found during construction

- Fixture `cmova` used `4C 0F 47 C2` (`cmova r8,rdx` — REX.R extends reg,
  not rm) so the stream `min()` never applied; short reads silently
  over-read. Corrected to `49 0F 47 C2` (`cmova rax,r10`).
- Swap-leaf log store `4C 89 41 08` wrote `[rcx+8]` (REX.B missing) —
  clobbered the type object instead of logging. Corrected `4D 89 41 08`.
- `SWAP_FN` (0x24 bytes) overran `GETTYPE_FN` at `CODE+0x80`; moved to
  `CODE+0x90`.
- `emu_start` doesn't push a return address — stack args land at
  `sp+0x28/+0x30/+0x38`, not `+0x20/+0x28/+0x30`.
- Prior-session disassembly was offset by `0x120000` (canonical VA vs
  section RVA); every address was re-verified against shipped bytes.

## Fixture disclosure

Hand-planted: stream vtbl + data window, header/ns buffers, `nsRec`/`gvec`
records, member nodes/type objects/vtables, class-desc stub (`+0xF4=0`),
alloc arena, TLS slots, lazy-state `0x2CF94EC`, `memcpy` IAT slot,
fixture routines (read/memcpy/swap-leaf/getType/ready).

This is **NATIVE-REPLAY on hand-built fixtures** — not live-game proof.
The member graph is a disclosed fixture: the deferred reflection
registration pass that would populate it natively was out of scope.

## Unreached scope

- Real member-type swap leaves (Phyre primitive `PType` vtables) — the
  fixture leaf stands in; their construction needs the deferred finalize.
- `0063E2E0` resolver arm (`node+0x50`) and kind-1/kind-2 dispatch arms
  (`[vtbl+0x20]`/`[vtbl+0x38]` calls) — fixture members are all kind-0.
- `0059E070` (the real caller) — ABI taken from it, not executed.

## Reproduction

```
python "Database/FFXII TZA/_experiments/evidence/phyre-header-exec/check.py"
```

Requires the shipping EXE at the recorded path (hash-asserted).
