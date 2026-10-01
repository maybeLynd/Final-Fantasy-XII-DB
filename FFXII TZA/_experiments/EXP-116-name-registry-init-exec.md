---
experiment: EXP-116
title: Input-name-registry initialisation — the real CRT init sequence (240 thunks over insert twins 00879570/00876C80) builds both shipped lists under Unicorn
contract: ../15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md
method: B
live_game: false
tool: evidence/name-registry-init-exec/check.py
---
# EXP-116 — name-registry-init-exec

**Status:** complete · **10/10 functional cases, 17/17 mutants, stable
across three processes**
**Evidence:** `evidence/name-registry-init-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

When the game boots, the input-name registry that menus and key-binding
screens display — "Button_0", "Key_A", "Empty" — is built by the CRT
static-initialiser pass, not by any gameplay code. The contract
reconstructed both lists and compared them live node-for-node, but the
initialisation itself had never been executed: the two insert bodies
were only partially emulated (channels only) and the 240 per-name
initialiser thunks — each `lea rcx,[static node]; call insert; lea
rcx,[dtor-cb]; jmp atexit` — had never run, least of all in the real
**.CRT-table order, which is shuffled** relative to the thunk arrays.

This experiment executes the shipped initialisation end to end: all 97
key thunks and all 143 channel thunks run in table order over the
shipped node objects and name strings, calling the **real insert
twins**, starting from the real load-time state (both list heads are
BSS — zero in the shipped image).

| VA | role | execution |
|---|---|---|
| `00879570` | channel registry insert | **real** (132 B, 40 insns) |
| `00876C80` | key registry insert (twin) | **real** (132 B, 40 insns) |
| `0016B5E0`+97×`0x20` | key init thunks | **real** (all 97, .CRT order) |
| `0016C380`+143×`0x20` | channel init thunks | **real** (all 143, .CRT order) |
| `00808B90` | `atexit` registrar | disclosed scripted boundary |

Each thunk's second `lea` loads the destructor-callback thunk and the
`jmp` reaches `atexit`; the harness records the callback argument as an
`ate:` trace token and returns — the registrar's bookkeeping has no
effect on the lists. Every node pointer, name string, link field and
the .CRT order come from shipped bytes; the only injected objects are
the fake node/name for the dup and null edge cases, which are
disclosed.

## Measured semantics (native execution, not static reading)

**INSERT `00879570(rcx=node)` / `00876C80(rcx=node)`** — identical
logic differing only in the RIP-relative list-head displacement
(`0x02EB9D80` channels, `0x02EB83B8` keys):

1. `name = [rcx+8]`; if null → return `0x11`.
2. Walk the list from the head; per node, byte-compare
   `[node+8]` vs `name` via a cursor+delta loop
   (`edx=*p1; ecx=*p2; sub; jne out; p1++; loop while *p2`).
   A zero-terminator tie (`edx==0` after the loop) → return `0x12`,
   no link written.
3. Otherwise push-front: `[rcx+0x10] = head; head = rcx`; return `0`.

**Initialisation result** — after the real sequences run:

- **Keys:** 97 nodes, head `Key_A`=28 → tail `Empty`=0 — strictly
  descending by registration position, `Empty` first registered.
- **Channels:** 143 nodes, head `Button_0`=11 → tail `Empty`=0,
  including the shipped alias groups (`Button_0`/`Button_Square`/
  `Button_X`/`Button_LeftMB` all carry value 11, `Button_1`/
  `Button_Cross` carry 12, …).
- All 240 names unique within their list; the produced chain is
  node-for-node identical to an independent Python simulation over the
  shipped .CRT order — which the earlier live comparison had already
  matched against the game's own lists.
- `ins` observables confirm every thunk passes its own static node;
  `ate:` tokens confirm every thunk completes through the `atexit`
  boundary with its own dtor-callback thunk.

## Execution findings (beyond the static reading)

1. **The .CRT table order is genuinely load-bearing.** The thunk
   arrays are contiguous (97 + 143 × `0x20`) but the table links them
   shuffled (`0x16B5E0 → 0x16B760 → 0x16BFE0 → 0x16C020 → …`). Running
   in address order would produce a different list order; the executed
   shuffled order is what produces `Empty` at the tail and the alias
   groups adjacent — matching the live lists.
2. **Duplicate names return `0x12` and do not link.** Both a fake node
   pointing at the *same* shipped name pointer (`dup-shipped-name`)
   and a fake node pointing at a *copied* name at a different address
   (`dup-copied-name`) return `0x12` — the check is byte-content, not
   pointer identity. `m-cmpdec` (inc→dec in the compare walk) is only
   distinguishable on the copied-name case: with a shared pointer the
   backward walk still compares identical bytes.
3. **No type separation between the lists.** `cross-list` inserts a
   real *key* node through the *channel* insert — it links onto the
   channel head with return 0. The twins differ only in which head
   global they touch.
4. **First-registration wins on duplicates.** `dup-shipped-name`
   leaves the list unchanged — the shipped name already registered
   stays put; the late duplicate is refused. Combined with push-front
   order this is what keeps `Empty=0` reachable at the tail.
5. **The `ate:` trace doubles as a progress receipt.** A count-cut
   harness bug initially dropped the last two thunks' tokens before
   their inserts could finish a 141-node scan (~50–70 insns/node with
   the per-byte compare) — the missing tokens, not a memory diff, were
   the first signal.

## Mutation campaign

17 byte-precise mutations, every site verified against shipped bytes
before patching:

- **Insert compare (6):** `sub edx,ecx`→`add` (equality inverted —
  kills on dup cases only, since unique names never reach the tie),
  `inc`→`dec` cursor (backward walk — distinguishable only when the
  compared names sit at different addresses), `je`→`jne` dup-exit
  (every non-head name "duplicates"), scan-loop `jne`→`je` (checks
  only the head), name-load `+8`→`+0x10` (compares link pointers as
  strings), scan-next `+0x10`→`+0x18` (walks the value field).
- **List plumbing (5):** empty-list `je`→`jne` (scans from a null
  head → wild read), insert next-store `+0x10`→`+0x18` (writes the
  value field; chain truncates to head), head-store displacement
  `9F`→`A3` (head lands at `0x2EB9D84`; the real head reads a shifted
  pointer — wild-follow recorded as a `wildnext` fault), NULL-name
  `jne`→`je` (every insert returns `0x11`; list stays empty),
  head-guard + null-return immediates `0x11`/`0x12` swapped on the
  edge cases.
- **Key twin (3):** the same compare/exit/store sites at `00876Cxx`,
  including a key-side dup case — proving both twins independently.
- **Thunk (2):** `call` rel32 retargeted `00879570`→`00876C80` (a
  channel node registers onto the *key* head — observable as a missing
  channel node plus a polluted key chain), and the `lea` node-arg
  displacement `7D`→`5D` (registers the adjacent static object — the
  `ins` arg record catches the wrong pointer immediately).

**17/17 killed.** Zero coverage-gap survivors — six mutations were
repointed onto discriminating cases before the campaign ran (a broken
dup-scan is unobservable while every name is unique, and the
backward-walk mutation is unobservable while both names share one
pointer).

## Limitations

- `atexit` is a scripted boundary: the registrar's callback-table
  writes are not modelled; the `ate:` token records that each thunk
  reached it with the right argument. The 240 dtor-callback thunks
  themselves were not executed (they run at process exit, not init).
- The CRT dispatch loop that *walks* the init table is not executed —
  the harness drives the extracted shipped order directly. What is
  proven is that running the shipped thunks in the shipped order over
  the shipped objects builds exactly the recovered lists.
- Fake node/name objects for `dup-*`, `null-name`, `fresh-*` cases are
  injected fixtures (disclosed); every shipped-list element is real.
- `bodies.json` holds body span + sha256 over shipped bytes for both
  inserts and all 240 thunks; instruction-start coverage convention
  matches EXP-107–115.
