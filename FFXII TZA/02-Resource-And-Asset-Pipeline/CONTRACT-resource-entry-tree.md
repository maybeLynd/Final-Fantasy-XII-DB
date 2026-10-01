---
contract: add and remove a resource entry from its arena's ordered tree, with membership as an invariant
category: 02-Resource-And-Asset-Pipeline
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md
entries: ["0036B4E0", "0036B410", "0036C790", "0036A000", "0036D170", "003AB880", "003AB940"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 31 addresses cited - 1 data, 9 entry, 21 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-13
  last_pass_state: "opus-tree-contract-falsification-pass-1 - four load-bearing claims attacked against the shipping bytes and survived (root is a full pointer, verified at the STORE as well as the read; jle is signed; equal keys take +0x28; both membership guards proceed only on their own polarity, so add and remove are idempotent). ONE FAILED: section 3 said insert clears +0x2C and +0x24, and it clears +0x28 as well - corrected in place, and a reimplementation following the old text would have inserted nodes carrying a stale right-child offset. ATTACKED 2026-09-15 by SWE2-ORACLE's EXP-083 and the 4 GiB narrowing FAILED - it was stated as a symmetric window and the codec domain is one-sided [base, base+2^32); 0036C790's rebalancing is now executed rather than unattacked. STILL not attacked: the handle ABI beyond confirming the tail calls"
  crossref_clean: false
  reopened_count: 0
external_production:
  section: SECTION-08
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section08-external-source-owners/REVIEW.md
---

# Contract — the resource entry tree, and the bit that says an entry is in it

Each arena keeps its entries in an **ordered binary tree**. This contract states the node layout, the
ordering rule, the add/remove pair, and the one-bit invariant that makes the pair safe to call.

Raised by ASTRA (`ASTRA-REQ-OPUS-RESOURCE-RELEASE-TREE`, section 18 of
[the authored-reference lifetime evidence](authored-reference-lifetime-evidence.md)) and re-derived
here from the shipping bodies.

## 1. The node, and why its links are not pointers

| where | width | field |
|---|---|---|
| `arena + 0x50` | **8** | the tree **root — a full pointer** (`0036B427 mov rsi, qword ptr [rcx+0x50]`) |
| `entry + 0x18` | 4 | the **ordering key**, compared **signed** |
| `entry + 0x24` | 4 | left link — an **arena offset**, not a pointer |
| `entry + 0x28` | 4 | right link — an **arena offset** |
| `entry + 0x2C` | 4 | parent link — an **arena offset** |
| `entry + 0x15` bit 1 | — | **"this entry is in the tree"** |
| `entry + 0x3E` | 2 | cleared to 0 on insert |

**The root is a full 64-bit pointer and the three links are 32-bit arena offsets.** Every traversal
step therefore goes through `0020E600` (offset → pointer) and every store through `0020E620`
(pointer → offset):

```asm
0036B50F  mov  ecx, dword ptr [rbx+0x24]   ; the left link, 32 bits
0036B512  call 0x20E600                    ; + arena base -> a real pointer
...
0036B546  call 0x20E620                    ; and back to 32 bits to store
0036B54B  xor  esi, esi
0036B54D  mov  dword ptr [rdi+0x2c], eax   ; parent
```

> **This inherits the 4 GiB constraint, not merely resembles it.** `0020E620` subtracts the arena
> base as a **`dword`** and computes entirely in 32 bits, while `0020E600` adds it as a **`qword`** —
> the asymmetry established in
> [`CONTRACT-efx-source-rebase.md` §4](CONTRACT-efx-source-rebase.md).
>
> ⚠ **CORRECTED 2026-09-15 (OPUS, accepting `SWE2-ORACLE`'s EXP-083). This paragraph used to say
> every node "must live within 4 GiB of `[0x01F83530]`", and that is wrong in a way that matters:
> it reads as a window either side of the base. It is not a window — the domain is one-sided.**
> The offset is an unsigned 32-bit quantity, so the representable set is exactly
> **`[base, base + 2^32)`**: a node *above* the base by less than 4 GiB round-trips, and a node
> **below** the base does not, at any distance.
>
> **Executed, not argued.** EXP-083 planted an arena at base `0x30000000` and encoded a node at 0:
> `enc(0)` decodes to `0x1_0000_0000`, and the second insert faults at `0x1_0000_0018`. The 32-bit
> subtraction takes `0 - 0x30000000` to `0xD0000000`, the `qword` add takes it back to
> `0xD0000000 + 0x30000000` = `0x1_0000_0000`, and the node is gone. So the failure is not a
> wrap *inside* the arena as this page previously said — it is a fault outside it.
>
> **Nodes above 4 GiB alias silently to their low dword**, which is the quiet half of the same fact
> and the one a reimplementation will not notice.
>
> **In THIS build the precondition holds, and that is a static result, not a lucky run.**
> `[0x01F83530]` is ~~zero for the life of the process~~ **zero at image load** *(scope restated 2026-09-26, below)*: the address sits in `.data` but **past the
> section's file-backed extent** (`.data` raw data ends at `01F7E400`), so it is zero at load, and
> `check_contract_globals` finds **no writer and no `lea`** anywhere in the image — that instrument's
> own two positive controls pass, so the absence is measured rather than assumed. With base 0 the
> domain is `[0, 2^32)` and the constraint reads: **every node must live below 4 GiB, absolutely.**
> *Scope restated 2026-09-26 (FABLE, Claude Opus 5.5), on the reconciliation in
> [the authored-table row lookup](CONTRACT-authored-table-row-lookup.md) §7:* the paragraph above holds for the
> **load-time** value and is too strong as an image fact.
> - **`[0x01F83530]` is zero at image load.** Nothing in the census above is wrong about that.
> - **One in-image store route reaches it.** The texture-id table writer bounds its id only from above, so an id of
>   `0xFFFB` stores a pointer into this cell (replayed on the unmodified bytes:
>   `members/image_address_base_writer_bounds.py`).
> - **The route is undriven, not absent.** Every id producer that has been read keeps ids below `0x4000` at the
>   shipped width.
> - So **"zero for the life of the process" is supported, not proven**. The 4 GiB constraint holds on the load-time
>   value and on every state that route leaves untouched. `check_contract_globals`' "no writer" measures its own
>   instruments, not the image.
>
> *Residual, and it is ASTRA-shaped:* a live read of `[0x01F83530]` would retire the last caveat. The
> static case above is strong but it is static, and nothing here proves the loader cannot publish a
> base before the first insert. One narrowing, two subsystems — and now one executed refutation.

## 2. The ordering rule is signed, and equal goes right

```asm
0036B4E0                                   ; insert, 177 bytes
0036B507  mov  eax, dword ptr [rdi+0x18]   ; the new node's key
0036B50A  cmp  dword ptr [rbx+0x18], eax   ; the current node's key
0036B50D  jle  0x36B529                    ; <-- SIGNED, and it takes the RIGHT branch
```

**`jle`, not `jbe`** — the key is a **signed** 32-bit value, and a negative key sorts below every
positive one rather than above them. **Equal keys take the `+0x28` (right) branch**, so an insert
never stops at an equal node: duplicates are permitted and are ordered after their equals.

## 3. The pair, and the invariant that guards it

`003AB880` and `003AB940` look like two teardown calls and are not. They are **the two halves of
membership**, each tail-calling through the handle ABI (untagged input → both do nothing; see
[`CONTRACT-efx-source-rebase.md` §2](CONTRACT-efx-source-rebase.md)):

| | `003AB880` → `0036A000` | `003AB940` → `0036D170` |
|---|---|---|
| guard | `test byte [rbx+0x15], 2` — must be **set** | `test byte [rbx+0x15], 2` — must be **clear** |
| action | `call 0x36C790` — **remove** | `call 0x36B410` — **add** |
| then | `and byte [rbx+0x15], 0xFD` — **clears** the bit | `or byte [rbx+0x15], 2` — **sets** it |

> **`+0x15` bit 1 is tree membership and nothing more.** ASTRA's caution that it is *"not a named
> general pin protocol"* is right and worth keeping: the bit does not mean pinned, locked or alive —
> it means *this node is linked into the tree*, and the guard makes both operations **idempotent**:
> adding twice and removing twice are both no-ops rather than corruption.

**`0036B410` clears the node's own links before inserting** — `20E620(0)` into **`+0x2C`, `+0x24` AND `+0x28`**
— so an entry never enters the tree carrying stale parent or child offsets. **This said two of the three
until falsification pass 1 counted them:** `0036B437` parent, `0036B441` left, `0036B449` right, each
from its own `20E620(0)`, and then `0036B44E mov word ptr [rbx+0x3e], ax` with `eax` zero. Naming
only two would have left a reimplementation inserting nodes that keep a stale RIGHT offset.

## Falsification pass 1 — 2026-09-13 (OPUS)

Every load-bearing claim attacked against the shipping bytes, not against the page it came from.
**Four survived, one was incomplete, and the incomplete one would have produced a real defect.**

| claim | verdict | what the image says |
|---|---|---|
| §1 the root is a full 64-bit pointer | **SURVIVES, strengthened** | `0036B427 mov rsi, qword ptr [rcx+0x50]` reads it, and `0036B457 mov qword ptr [rdi+0x50], rbx` **stores** it — directly, without `0020E620`, unlike every link |
| §2 the key is compared SIGNED | **SURVIVES** | `0036B50D jle`, the signed form |
| §2 equal keys take the RIGHT branch | **SURVIVES** | `jle` targets `0036B529`, which reads `+0x28` |
| §3 the guards make the pair idempotent | **SURVIVES** | remove at `0036A03E`/`0036A042` proceeds only when the bit is SET; add at `0036D1A4`/`0036D1A8` proceeds only when CLEAR |
| §3 insert clears `+0x2C` and `+0x24` | **INCOMPLETE** | it clears **three** links, `+0x28` as well |

**The store side of the root is better evidence than the read side, and the contract cited only the
read.** A `mov rsi, [rcx+0x50]` is consistent with an 8-byte field holding anything; `mov [rdi+0x50],
rbx` writing a live pointer with no `0020E620` in sight, in a function where every other link store
goes through it, is the asymmetry itself. Added above.

**The one failure is the kind a contract exists to prevent.** §3 named two of the three link clears.
A reimplementation following it literally would insert a node still carrying a stale right-child
offset, and the tree would be structurally wrong from the first re-insertion of a recycled entry —
silently, because every traversal step still resolves through `0020E600` and lands on a real node.

**What this pass did NOT attack**, and so cannot be read as having cleared: `0036C790`'s rebalancing
(§4 already says it is not re-derived here), the 4 GiB narrowing inherited from
`CONTRACT-efx-source-rebase.md` §4, and the handle-ABI behaviour of `003AB880` / `003AB940`, whose
trampolines were read only far enough to confirm they tail-call `0036A000` and `0036D170`.

## 4. What this contract does not establish

- ~~**`0036C790`'s rebalancing.**~~ **Re-derived 2026-09-18 — ASTRA's prose is right, and the
  detail is now byte-proven.** `0036C790(tree, node)` resolves `parent = +0x2C`, `left = +0x24`,
  `right = +0x28` through `0020E600`. Root case (`rbx==0`): right present → `tree+0x50 = right`,
  `right.+0x2C = 0020E620(0)`, `right.+0x3E = 0`, then `0036B4E0(right, left, 0x4AA)` reinserts the
  left subtree; only left → `tree+0x50 = left`, same parent/flag clears, no reinsert; neither →
  `tree+0x50 = 0`. Non-root with right: `0036B4E0(right, left, 0x4BF)` runs **first** (while the
  right subtree is still intact), then `right.+0x2C = 0020E620(parent)`, the parent's matching
  child slot (`+0x24` or `+0x28`, chosen by which one resolves to the node) is rewritten to
  `right`, and `+0x3E` is cleared on **both** `right` and `parent`. Non-root without right:
  `0036B490(parent, left, 0x4DF)` when the node was the parent's `+0x24`, else
  `0036B5A0(parent, left, 0x4E3)` — the left subtree is spliced straight into the vacated slot.
  So "promotes the right child and reinserts the left" is exact; EXP-083's execution and the
  static body now agree.
- ~~**The standalone tree helper does not clear the removed node's links or its flag**~~ —
  **byte-proven on both sides 2026-09-18.** `0036C790` writes only to parent/children/root — no
  store ever touches `[node+X]`; the removed node keeps its links and `+0x15` bit 1. The clearing
  is `0036A000`'s, after the call returns: `and byte [node+0x15], 0xFD` at `0036A078` and
  `word [node+0x3E] = 0` at `0036A080` (`rdi` is `xor`'d at `0036A04D`). Calling the helper
  directly leaves a linked-in-shape node that claims membership — exactly the hazard ASTRA flagged.
- **`+0x18` is the allocated payload-byte extent used by the mover (SECTION-07).** The original
  `0036A2A0` takes this length from the source and passes it through `004746F0` to the copy import;
  the selectors compare it against free-block extents. It is not a semantic resource used-length.
  The whole controlled 0x400-byte allocation is copied, including bytes beyond the parsed payload.
- **The release chain above this level — bounded SECTION-06 evidence now exists.** The matched
  `00409D60` → `003B37E0(entry+0x44)` → `0024F4D0`/`0024F410`, per-row `00409730`, and
  original allocation-release path execute in the new fixture. `00409CA0`, all specialized children,
  real movement/IO timing and whole-game reference lifetime are not thereby validated. See the
  SECTION-06 production section below and the [ownership contract](CONTRACT-resource-input-ownership.md).

## 5. A correction this contract carries

An earlier revision of `CONTRACT-efx-source-rebase.md`, written the same day, described
`0036D170`'s `test byte [rbx+0x15], 2` as **part of the generation validation**. It is not: the
generation check is `word [slot+6]` against `word [obj+0x1C]`, and the `+0x15` test is the
**membership guard** documented above. The mischaracterisation did not reach any conclusion in that
contract — §3 and §4 there are unaffected — and the table has been corrected in place with a pointer
here.

## 6. Relationships

**The pair's plumbing.** `003AB880` and `003AB940` are handle-ABI trampolines: a tagged input
tail-calls `0036A000` (remove) / `0036D170` (add); an untagged one is passed through unchanged or
ignored. Both inner bodies run the generation check (`word [slot+6]` vs `word [obj+0x1C]`) before
touching the tree — the resolver sibling `0036B130` notably does not (see
[`CONTRACT-efx-source-rebase.md`](CONTRACT-efx-source-rebase.md) §2).

**Inside the tree.** `0036D170` → `0036B410` (insert: clears `+0x2C`/`+0x24`/`+0x28` via
`0020E620(0)`, zeroes `+0x3E`, walks the signed ordering). `0036A000` → `0036C790` (remove, 359
bytes — the rebalancing is ASTRA's reading, §4). Every link store goes through `0020E620` and every
link load through `0020E600`; the root at `arena+0x50` is the exception, a full pointer.

**Above the pair.** SECTION-06 connects the matched `00409D60` path through effect-ticket and
context teardown to per-entry backing release; it does not execute every caller such as `00409CA0`.
The tree pair changes membership without freeing storage, while actual `003AB7C0` destruction
reaches the slot-removal/allocation-release path. The original tree codec uses `[01F83530]`;
that codec base is not evidence that every layer shares one owner or one pointer representation.

## 7. State transitions

```
entry:     not-in-tree  (+0x15 bit1 clear)
             -- 003AB940 tagged & generation ok & bit clear
                --> 0036D170: 0036B410 clears links +0x2C/+0x24/+0x28, word +0x3E = 0,
                    inserts by signed key (equal goes right), sets +0x15 bit1 --> in-tree
in-tree    -- 003AB880 tagged & generation ok & bit set
            --> 0036A000: 0036C790 unlinks/rebalances, clears +0x15 bit1 --> not-in-tree
guards:    untagged input -> no-op; generation mismatch -> no-op;
           add-when-in / remove-when-out -> no-op  (the pair is idempotent)
```

## 8. Script · resource · event interactions

No script verb or authored table participates directly — this is the **arena's internal index**:
resource entries are the rows the resource pipeline allocates, and the tree is how an arena finds
one. The ordering key at `+0x18` is the quantity the arena orders by (ASTRA calls it a payload
length; signed comparison proven, the quantity itself not).

## 9. Determinism

- **RNG** — none.
- **Ordering** — total order by the signed 32-bit key; equal keys insert to the right, so the tree's
  shape for a given insertion sequence is fully determined.
- **Threading** — not established; no lock appears in the read bodies.

## 10. Failure paths and edge conditions

- **Untagged input** — both trampolines no-op (`003AB880` returns the input unchanged; `003AB940`
  returns with no call and no write).
- **Generation mismatch** — the `+6`/`+0x1C` word check fails before any tree access.
- **Double add / double remove** — no-ops by the `+0x15` bit-1 guard; this is the invariant that
  makes the pair safe.
- **Duplicate keys** — permitted, ordered after their equals (`jle` takes `+0x28`).
- **Outside the codec domain** — *corrected 2026-09-15 from "4 GiB wrap", which described the
  wrong failure.* The domain is `[base, base + 2^32)`. A node **above** it aliases to its low
  dword and traversal lands on the wrong node, silently. A node **below the base** does not wrap
  into the arena at all — it decodes above the domain and the next insert **faults**: EXP-083 saw
  `enc(0)` under base `0x30000000` decode to `0x1_0000_0000` and fault at `0x1_0000_0018`. A loud
  failure and a silent one, not one failure (§1).
- **Stale-link insertion** — impossible through `0036B410` (it clears all three links first), but
  reachable through the standalone helper if called directly (§4).

## 11. Observable behaviour

The tree is observable in arena memory: the root pointer at `arena+0x50`, each entry's `+0x18` key
and `+0x24`/`+0x28`/`+0x2C` offset links, the membership bit at `+0x15` bit 1, and `+0x3E` cleared
on insert. [`EXP-083`](../_experiments/EXP-083-resource-entry-tree-execution.md) (SWE2-ORACLE) executed the whole call graph as shipped under isolated original-code
execution - 45 cases, 5 mutants detected - and observed these fields directly. It is not a live-game
observation. *(updated 2026-09-15, OPUS: EXP-083 published in `feed9f67`)*

## 12. Reproduction formula

```
add (003AB940 -> 0036D170 -> 0036B410):
    if untagged(handle): return                    # pass-through/no-op at the trampoline
    if word[slot+6] != word[obj+0x1C]: return      # generation check
    if entry.+0x15 & 2: return                     # already in the tree: idempotent
    entry.+0x2C = entry.+0x24 = entry.+0x28 = off(0);  entry.+0x3E = 0
    cur = [arena+0x50]                             # full pointer
    walk: if (s32)cur.+0x18 <= (s32)entry.+0x18: go +0x28 else +0x24   # SIGNED; equal goes right
    store entry's offset at the leaf link; parent link at +0x2C; entry.+0x15 |= 2

remove (003AB880 -> 0036A000 -> 0036C790):
    same tag and generation gates; requires +0x15 bit1 SET
    tree = (byte[node+3] < 0xF) ? 022D7FD0 + byte[node+3]*0xA8 : 0    # kind byte picks the tree
    0036C790 unlinks and rebalances: promotes the right child, reinserts the left through 0036B4E0
        (EXECUTED in EXP-083; statically re-derived 2026-09-18, section 15)
    entry.+0x15 &= ~2 ; entry.+0x3E = 0                              # caller-side, not the helper

link conversion:  ptr = off + qword[01F83530]      # 0020E600, zero-extended offset
                  off = ptr - dword[01F83530]      # 0020E620, 32-bit subtraction
```

## 13. Runtime validation

**Evidence class: static original-code reading, plus isolated original-code execution (method B).** *(updated 2026-09-15, OPUS: EXP-083 published in `feed9f67`)*

[`EXP-083`](../_experiments/EXP-083-resource-entry-tree-execution.md) executed all eleven bodies of the closed call graph as shipped, with no callee stubbed:
`0020E600`/`0020E620`, `0036B410`, `0036B4E0`, `0036B490`/`0036B5A0`, `0036C790`, `0036D170`/`0036A000`
and `003AB880`/`003AB940`. It ran 45 cases and detected all 5 byte-level mutants. The two touched globals
are injected fixture values, disclosed by the record. Its findings are the EXP-083 rows of section 15.
**No live game was involved, so a runtime observation remains open** and nothing here claims one. Review:
audit pending: `SWE2-ORACLE-REQ-AUDITSPEC-TREE-REVIEW`.

~~Evidence class: static original-code reading. An experiment is in flight. (2026-09-13.)~~ *That was
the state before the record existed; kept as history.*

## 14. Unresolved

1. ~~**`0036C790`'s rebalancing** — ASTRA reports it promotes the right child and reinserts the left;
   the parent/left/right reads are consistent but it is not re-derived here (§4).~~ **Resolved by
   execution:** [`EXP-083`](../_experiments/EXP-083-resource-entry-tree-execution.md) ran real removals and compared the link repair (section 15). *(updated 2026-09-15, OPUS: EXP-083 published in `feed9f67`)*
2. **`+0x18` extent resolved at allocator granularity by SECTION-07:** payload allocation bytes,
   used by selector comparisons and the actual mover copy. Whether a caller uses every byte for
   semantic content is a different question; no such implication is made.
3. **The release chain above the pair — bounded production added in SECTION-06.** The actual
   `409D60` -> ticket/context -> entry-buffer -> native-free path is executed in synthetic state;
   `409CA0` is checked statically, not newly executed. Live timing, all tag forms and complex child
   callbacks remain open. See the new section below; this is not a whole-tree or L2 acceptance.
4. ~~**EXP-083's result** — the in-flight experiment is the §13 evidence this contract waits on.~~
   **Landed** (section 13). What remains open is a live-game observation of the pair, which EXP-083 by design is not.

## 15. Evidence

> **Numbered 15, header lowercase `claim`, on purpose.** `parity_status.py` reads a
> contract's claim list from a heading that literally begins `## 15.` and keeps only a table
> whose first header cell is `claim`; miss either and it finds **zero** claims and refuses
> any harness written against this page instead of reporting a mismatch.

| claim | evidence | tier |
|---|---|---|
| the root at arena+0x50 is a full pointer while the three links are 32-bit arena offsets | `0036B427` loads it as a `qword`; `+0x24`/`+0x28`/`+0x2C` go through `20E600`/`20E620` | 1 |
| the ordering key at entry+0x18 is compared SIGNED, and equal takes the right branch | `0036B50D jle`, not `jbe`, taking the `+0x28` arm | 1 |
| +0x15 bit 1 is tree membership and nothing else | `0036A000` requires it set, removes, clears it; `0036D170` requires it clear, adds, sets it | 1 |
| both operations are idempotent because of that guard | the same two `test byte [rbx+0x15], 2` sites | 1 (static) |
| **`0036C790`'s rebalancing** — the root promotes its right child and reinserts the left through `0036B4E0` | **EXECUTED** by `SWE2-ORACLE` EXP-083; **statically re-derived 2026-09-18** — non-root with right: `0036B4E0(right, left)` first, then `right.+0x2C = parent`, parent's matching slot rewritten, `+0x3E` cleared on right+parent; without right: `0036B490`/`0036B5A0` splices left into the slot; the two agree | 1 |
| `0036C790` never writes the removed node — no `[node+X]` store exists; `0036A000` clears `+0x15` bit 1 and `+0x3E` itself after the call | full-body scan: every store targets `rbx`/`rsi`/`rdi`/`[r14+0x50]`; `0036A078 and byte [rbx+0x15],0xFD`; `0036A080 mov word [rbx+0x3E],di` with `rdi` xor'd at `0036A04D` | 1 (static) |
| `0036A000` picks the tree object by `byte[node+3]`: `022D7FD0 + kind*0xA8` when `< 0xF`, else 0 | `0036A04F cmp eax,0xF` / `imul rcx,rax,0xA8` / `lea rax,[022D7FD0]` / `add rcx,rax`; `rcx=rdi(=0)` otherwise — same root field `+0x50` as the arena claim | 1 (static) |
| the codec domain is `[base, base + 2^32)` and is **one-sided** — a node below the base never round-trips | EXP-083: base `0x30000000`, `enc(0)` decodes to `0x1_0000_0000`, second insert faults at `0x1_0000_0018` | 1 |
| nodes above 4 GiB alias silently to their low dword | EXP-083, same run | 1 |
| `[0x01F83530]` is ~~zero for the life of this build~~ **zero at image load; one undriven in-image store route exists (2026-09-26)** | past `.data`'s file-backed extent `01F7E400`, and `check_contract_globals` finds no writer and no `lea` by its own instruments (its controls pass); the texture-id writer's signed-index store reaches the cell at id `0xFFFB` and no producer read drives it (the authored-table row lookup contract §7) | 1 (static) |
| `0036D170` lacks the null-object check `0036A000` has — index ≥ `0xF` yields `ctx = 0` and faults at `[0x50]` | EXP-083 | 1 |
| removing a non-member returns `obj+0x40` with no observable removal | EXP-083 | 1 |
| **what the `+0x18` key measures** | **not established** | none |

## 16. Parity plan

~~`EXP-083` (SWE2-ORACLE, in flight) is the execution path for this contract — this section records
the plan, not a result.~~ *(updated 2026-09-15, OPUS: EXP-083 published in `feed9f67`)* [`EXP-083`](../_experiments/EXP-083-resource-entry-tree-execution.md) executed the ORIGINAL bodies, not a reconstruction.
The parity plan below is still a plan: no reconstruction of section 12 has been diffed against them. A fixture plants a small arena, inserts entries by handle in a scripted
order (including duplicate keys), removes them, and compares the link offsets and the `+0x15` bit
against an independent reconstruction of §12's algorithm.

**Dimensions that apply:** `STRUCTURAL` (tree invariants: ordering, parent links, no stale
children), `STATE-TRANSITION` (membership bit per call), `EDGE-CASE` (equal keys go right, untagged
no-op, generation mismatch, double add/remove). **Not covered, recorded:** `INTEGRATION` — the
release chain above the pair now has bounded original-code SECTION-06 evidence (§14), not
independent reconstruction parity or whole-game lifetime proof; the 4 GiB wrap is a fixture-only hazard unless the allocator's
guarantee (BW-2) is established. `RNG`, `TIMING`, `PRESENTATION` are `N/A`.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**Audio — CLIENT.** The tree insert `0036D170` is also called by three 83-byte Audio-filed bodies, and the resolver
sibling `0036B130` by a 256-byte one. The entry tree is the shared resource arena, and sound code is one of its clients.

## SWE2-EC7-21 update (2026-09-18) — `00409600` base-resolver window

`00409600` (86 B) is the `ResourceEntry_GetResolvedBasePointer` mode dispatch the
entry-tree docs name: null `rcx` returns 0; `[rcx+4]` selects the path — mode 0
tails `0051EE00` on `&rcx+0x10`, mode 1 returns the cached `+0x38` base or, when
the `027A2E10` flag is armed, resolves `+0x30` through `003AB7F0` and republishes
the result to `+0x38`; any other mode returns 0. Interior anchor `00409616` (the
`+0x4` kind read). Callers `00409660`/`004096C0`/`00417F40`/`004256E0` — including
the `004256E0` consumer the steering/coast-down contracts name.

## SWE2-EC7-29 update (2026-09-18) — `0036C790` three-id relink

`0036C790` (359 B) is the relink an instruction record `rdx` drives
through the entry tree's id table: `rdx[+0x2C]`/`[+0x24]`/`[+0x28]`
resolve through `0020E600` into records A/B/C (rbx/rsi/rdi). No A: the
container head `[r14+0x50]` repoints to C, or B when C is absent —
stamping `+0x2C = 0020E620()` and clearing `+0x3E`, with
`0036B4E0(C, B, 0x4AA)` on the C arm — and nulls when both are absent.
A and C: `0036B4E0(C, B, 0x4BF)` runs first, `C[+0x2C] = 0020E620(A)`,
then whichever of `A[+0x24]`/`A[+0x28]` resolves back to `rdx` is
overwritten with `0020E620(C)` — the node inherits the excised record's
link slot. A alone: `0020E600(A[+0x24]) == rdx` runs
`0036B490(A, B, 0x4DF)`, `0020E600(A[+0x28]) == rdx` runs
`0036B5A0(A, B, 0x4E3)` — the two asymmetric repair arms. `+0x3E` flags
clear on every touched record. Interior anchor `0036C804` (the
`0036B4E0` call on the fresh-link arm).


## Current release-chain reconciliation — SECTION-06 (2026-09-22)

[Ownership/lifetime specification](the-resource-owner-from-copy-or-borrow-to-disposal.md) and
[production review](../_experiments/evidence/continuation-section06-resource-lifetime/REVIEW.md)
connect the previously static upper chain to actual original-instruction controls.
`003AB880` removes tagged tree membership and returns payload; `003AB940` adds it back.
These operations preserve allocated backing and are not counted retain/release operations:
two original acquires followed by one release already reinsert the node in the tested state.
The generation mismatch check preserves the existing member. Actual `003AB7C0`/`00369800`
release clears the handle-slot owner and releases the native allocation through `00369860`.

At the entry layer, `00409D60` sweeps selected matched render references, cancels the exact effect
ticket through `003B37E0`, calls row teardown `00409730`, and removes the indexed bank slot.
Context cleanup happens before the entry's copied backing is released. Mode1 source backing
survives that row's cleanup. A slot array element being recycled is not a heap allocation being
freed. Cache+38 survives row reset and must not establish validity.

The fixture executes the original allocator, membership pair and tagged/raw release. It constructs
its own arena/handle slots; it does not execute the game's source movement/reclamation scheduler,
all tree shapes or live deletion. Historical EXP-083 coverage remains separate. The meaning of the
node's +18 ordering key remains as previously bounded, not silently solved by this new lifecycle.

## Tree membership controls movement eligibility — SECTION-07 (2026-09-23)

The original compaction selectors search this tree. `0036AAD0` uses an equal-sized, higher-address
eligible member for the current free head; the recorded smaller candidate is not used as a best-fit
fallback. `0036ABE0` can instead move the physical successor of a hole when its allocation bit is
set and `header+0x15 & 6 == 2`, or search for an exact candidate. Mask `0x04` inhibits these choices.

The original acquire removes the tagged block from the eligible tree, and in the controlled fixture
it cannot then be moved by either selector. Release reinserts it and makes it eligible again unless
mask `0x04` inhibits movement. This supplies a concrete consumer for membership, **not a nesting reference
count or a proof of thread-safe pin discipline**. A pin/unpin pair must not be replaced by two frees.

The original mover frees the old block, copies the allocation bytes into the selected free region,
reissues its header, updates the existing slot/generation and reinserts its membership. The public
`00369C60(arena, 0)` can move twice: one exact pass plus one adjacent/search pass. Arena+0x62 records
successful compaction until its explicit clear, not completion of all pointer repair.

[Producer/consumer specification](the-source-block-mover-and-separate-consumer-refresh.md) and
[execution evidence](../_experiments/evidence/continuation-section07-source-movement/REVIEW.md).
The tested copy paths are non-overlapping. A separate small-hole control reaches overlap and stops
at the original import without claiming its eventual copy result. All-game interleavings and the
external owner/reload policy remain open; no terminal verdict is changed.


## Concrete client exclusion and external-source disposal — SECTION-08 (2026-09-23)

The previously established membership pair now has an executed real client.00409960 finds a
selected source view, pins a tagged mode1 entry through003AB880 and returns its resolved interior;
00409C00 ends the view through003AB940. An original consumer0041FCF0 brackets its use at0041FFA0
and0041FFF8 (static whole-body read, not full consumer execution). Failed selection returnsNULL
without acquiring. Two successful acquisitions and ONE release restore eligibility, after which
actual compaction moves the source. Copy-mode00409A60 similarly unpins even a pre-existing pin.
This is not a nesting reference count, atomic lock, or proof of arbitrary callback safety.

0041E490 calls acquire then release BEFORE passing the original source representation to the
bank disposal at00409D60. A tagged representation and its resolved pointer are not interchangeable
match keys. That wrapper alone does not free external backing. The indexed source owner at
02B581A0 separately frees through00369800 after the original bank/context disposal chain.
While an owner is in-flight, deletion changes state3 to5; the source remains allocated and the
request callback remains pending until completion. The source-release policy is now concrete for
this five-by-sixteen owner family, not inferred from a nonzero cache or tree node.

See [the external-owner/view mechanism](the-external-source-owner-and-borrowed-view-lifetime.md)
and [SECTION-08 proof boundaries](../_experiments/evidence/continuation-section08-external-source-owners/REVIEW.md).
No global L2 verdict or formal independent acceptance changes here.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Presentation — CLIENT, 69 edges: the render-record layer is the tree's main consumer.**
- **`003AB7F0`, the section resolver, has 28 presentation callers.** Among them are
  `CharacterRenderRecord_MaintainPresentationResourceReferences`, `CharacterRenderRecord_RefreshLoadedResourceBindings`
  and the `PresentationEntryReferenceContainer_*` release and resolve bodies.
- **The named entries have presentation callers too:** `ResourceEntry_FindSectionPointerByTagAndName` (`00409660`, 6),
  `ResourceEntry_ResolveSectionOffset` (`004096C0`, 5) and `ResourceEntry_GetResolvedBasePointer` (`00409600`, 2).
- **The consumers this page names are presentation bodies with presentation callees:**
  - `PresentationAuthoredCommand_Class09_ActivateLoadedResourceState` (`00417F40`, 8 callees, including the
    UV-snapshot copy `003B5CE0`);
  - the `+0x457` writer `004256E0` (5, including `CharacterRenderRecord_RefreshFCPPayloadByRecordId`);
  - the release chain `003B37E0` → `0024F410` / `0024F4D0`.
- **The arena helpers** `0036B130`, `00369C60`, `0036A000` and `0041E490` are also reached from the presentation
  maintenance caller `002E65A0` and from `003CCF20`, `003CD2C0` and `003DD4C0`.

What is drawn from these sections belongs to the render-record pages (`CONTRACT-render-record-pool-lifecycle`,
`the-character-render-record-array`). This contract owns the tree and its lookups.

**Script_VM_Native_Bridge — CLIENT, five edges.** The script adapters `0050DDA0`, `0050E300`, `0050DEB0`, `0050D5E0` and
`0050DF30` call the arena and tree entry points `00369800`, `00369C60`, `0036A000`, `0036B130` and `0036D170`. For
example, `0050E300` pops the arena id and repeat flag for `00369C60` (`CONTRACT-efx-source-rebase` §8). The script VM
owns the verbs; this contract owns what they reach.

**CombatAction — CLIENT, one edge.** `002FC3C0`, one of the resource request queue's asking-form callers
(`the-resource-request-queue`), calls the release leaf `0024F410`. It is a combat action body releasing an entry,
not a combat claim of this contract.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page and the cited pages read them; no new body read
(OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*
