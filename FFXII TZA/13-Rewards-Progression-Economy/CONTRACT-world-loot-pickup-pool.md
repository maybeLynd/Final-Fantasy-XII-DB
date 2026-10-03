---
contract: hold up to ten world loot pickups in a fixed pool on one FIFO list, age them through a blink ladder, and retire each one by a single shared sequence
category: 13-Rewards-Progression-Economy
scope: subsystem
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md
entries: ["00319B10", "00319CA0", "00319600", "00319920", "003197B0", "00319830", "00319A00"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every operation below was disassembled and read in this session (OPUS, 2026-09-20); the
    pool extent, the two list globals and the two padding spans were additionally measured
    image-wide over 34,270 function bodies with a positive control. No runtime observation.
last_reviewed: 2026-09-29
audit:
  by: OPUS
  date: 2026-09-21
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-world-loot-falsification-pass-1
---

# Contract — the world loot pickup pool

> **Provenance, stated once.** Every claim below was re-derived from the shipping image in this
> session unless it is tagged **[page]**, which marks a statement carried from
> [the system page](world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) without independent
> re-derivation here. Nothing is carried silently. **[live]** marks what only runtime can settle,
> and is never asserted.

## 1. Purpose

When something in the world drops loot, the game materialises a pickup the player can walk over.
At most ten exist at once. Each one fades through a blink and then disappears on its own; walking
over it grants its items instead. When an eleventh drop happens, **the oldest pickup is sacrificed
so the new one can exist** — a drop is never refused.

## 2. Interface

| | |
|---|---|
| entry point(s) | `00319B10` init (387 B) · `00319CA0` create (394 B) · `00319600` tick (423 B) · `00319920` collect (215 B) · `003197B0` remove (113 B) · `00319A00`, `00319830` index wrappers (26 B each) |
| create | `rcx` = drop buffer (56 B, seven `{u16 id, u32 qty}`), `rdx` = float3 position |
| tick | no arguments; walks the active list once per field frame **[page]** |
| collect | `rcx` = node, `edx` = a value forwarded to the presentation call as its payload |
| remove | `rcx` = node, `edx` = the same payload |
| returns | none of the five returns a value used by its callers |

## 3. Types

`WorldLootPickupNode`, size `0x60`, ten of them at `02EC0FA0`.

| off | size | field | note |
|---|---|---|---|
| `+0x00` | 4 | `slotIndex` | 0–9, written once at init, **never rewritten**; the key into the presence table |
| `+0x04` | 4 | `state` | `0` = free; `1`…`7` = the ladder |
| `+0x08` | 4 | `materialiseStamp` | the field clock when the node reached state 2 |
| `+0x0C` | 4 | — | **alignment padding**, see §4 |
| `+0x10` | 8 | `prev` | `WorldLootPickupNode*`, null at list head |
| `+0x18` | 8 | `next` | `WorldLootPickupNode*`, null at list tail |
| `+0x20` | 56 | `dropEntries[7]` | `{u16 itemId; u32 quantity}`, stride 8; ~~`itemId == 0xFFFF` ends the run~~ an `itemId` of `0xFFFF` is **skipped**, and all seven entries are always visited *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 309; `00319943`–`00319972` re-read.)* |
| `+0x58` | 4 | `objectHandle` | the world object; `0` when free |
| `+0x5C` | 4 | — | **tail padding**, see §4 |

`WorldLootDropEntry`, size `8`: `itemId` u16 at `+0x00`, two bytes of padding, `quantity` u32 at
`+0x04`.

## 4. Preconditions · postconditions · invariants

**I1 — the pool is exactly ten nodes of `0x60`, and three independent witnesses agree.** The create
scan uses a literal `cmp eax, 0xA` with `add rbx, 0x60` (`00319CD0`, `00319CCC`); the init function
writes ten `slotIndex` values `0…9`; and `g_pWorldLootPickupListHead` sits at `02EC1360`, which is
`02EC0FA0 + 10 × 0x60` exactly — **an eleventh node would overlap the head pointer**.

**I2 — free is exactly `state == 0`.** Both the scan (`cmp dword ptr [rbx+4], ebp` with `ebp = 0`)
and every retirement path (which zeroes `state`) use this and nothing else.

**I3 — `slotIndex` is immutable after init.** No path outside `00319B10` writes `+0x00`. Retirement
zeroes `state`, `stamp`, both links and the handle — **never the slot index** — so a reused node
keeps its original presence key.

**I4 — `+0x0C` and `+0x5C` are padding, not state.** Measured image-wide over 34,270 bodies:
**0 of 10 slots referenced at either offset**, while the known live field `+0x58` **is** found at the
same stride — so this is measured absence, not an instrument that never fired. The layout forces
both: `prev` at `+0x10` is 8-byte aligned, so the 4-byte `materialiseStamp` ending at `+0x0C` pads to
it; and the pointer members give the struct 8-byte alignment, so a final 4-byte field at `+0x58`
rounds the size `0x5C → 0x60`. Four write paths corroborate — init, create, tick-despawn and collect
each write every live field and skip both holes, and init and every retirement write `+0x04` as **one
qword**, merging `state` and `stamp`.

**I5 — the list is FIFO.** Append is at `g_pWorldLootPickupListTail` (`00319D67`); eviction takes
`g_pWorldLootPickupListHead` (`00319CDC`).

**I6 — list/pool coherence.** A node is on the list **iff** `state != 0`. Every path that sets
`state = 0` unlinks first, and the only path that sets `state = 1` appends.

## 5. State

| symbol | address | role |
|---|---|---|
| `g_aWorldLootPickupNodes` | `02EC0FA0` … `02EC135F` | the ten nodes |
| `g_pWorldLootPickupListHead` | `02EC1360` | oldest; the eviction victim |
| `g_pWorldLootPickupListTail` | `02EC1368` | newest; the append point |
| field clock | `0208D45C` | BSS, so `0` at image load **[page]** |
| lifetime step | `01CEBCAC` | `-30.0f`, `.rdata` **[page]** |
| runtime scalar | `01DFE0B8` | `1.0f` default **[page]** |
| pickups collected | `022C3174` | incremented once per collect (`00319974`); read as the chain-rank penalty factor and zeroed on a rank advance by `EnemyChain_TryAdvanceRank` (`003183D0`), see §6 and pass 1 |

**The three addresses in the first three rows are contributed by this contract**: the page names all
three symbols and gives the address of none.

## 6. Relationships

* `0028F000(ECX = handle, EDX = op, R8 = payload*)` — the presentation call, **read per opcode
  2026-09-21 (OPUS)**; the opcode set below is re-derived, not carried.

> **THE WHOLE DISPATCH, from the jump table that follows the body at `0028F09C`.** The op is
> validated as `lea eax, [rdx-1]` / `cmp eax, 5` / `ja`, so **valid ops are `1`–`6`**, and the
> target is `image + 0x16F09C + (op-1)*4`. The manager `[0209BE80]` is null-tested first; a null
> manager returns `0` without dispatching.
>
> | op | target | payload | calls | returns |
> |---|---|---|---|---|
> | 1 | `0028F034` | **reads `[payload+0x10]`, `[payload+0x14]`, and passes `payload` itself** | `003FA160` (tail) | that call's value |
> | 2 | `0028F050` | **reads `dword[payload]`** | `003FAA10` | **the handle** |
> | 3 | `0028F063` | **reads `dword[payload]`** | `003FA820` | **the handle** |
> | 4 | `0028F076` | **IGNORED** — `xor edx, edx` | `003FA820` | `0` |
> | 5 | `0028F076` | **IGNORED** — the *same target as op 4* | `003FA820` | `0` |
> | 6 | `0028F088` | **IGNORED** | `003FA900` on `manager+0x57E0` | `0` |
>
> **OPS 4 AND 5 ARE NOT MERELY SIMILAR, THEY ARE THE SAME CODE.** The jump table's fourth and fifth
> entries hold the identical offset. Whatever distinguishes *despawn* from *eviction*, the
> presentation layer does not see it — the distinction lives entirely in the caller.
>
> **AND OP 3 IS THE SAME OPERATION WITH AN ARGUMENT.** It reaches `003FA820` too, differing only in
> passing `dword[payload]` where ops 4 and 5 pass zero. §12's "reimplement it once" is stronger than
> it claimed: three of the four retire sites collapse to one call with one varying operand.
>
> **WHAT THAT CALL DOES TO THE VISUAL, AND WHAT IT DOES NOT** *(added 2026-10-02, OPUS, from ASTRA's
> [s33 visual retirement clock](../_experiments/evidence/s33-visual-retirement-clock/README.md), SWE2-AUDIT-SPEC ACCEPT,
> consumed by FABLE in [`astra-returns-s33-fable-1002`](../_index/candidates/astra-returns-s33-fable-1002/README.md))*.
> With a zero second argument (ops 4 and 5), on a visual that is occupied (bit 0), not yet retired (bit 1) and without
> bit 3, `003FA820` sets bit 1, zeroes `+0x290` and `+0x294`, and returns. **It does not free the visual's slot.** The
> visual's own per-call update later runs its phases down to 0. Only a later call of the visual manager clears the
> flags word and unlinks the record, in the recycle pass that runs before that call's update pass (the bodies are
> named by role here; FABLE's record lists them). How long that takes depends on the fade and the frame step. No fixed window is established, and with a
> zero frame step the fade never falls. Op 3's non-zero argument takes another path, which this note does not cover.
>
> **A RETURN VALUE OF `0` IS AMBIGUOUS AND CANNOT BE TESTED.** Ops 4, 5 and 6 return `0` on success;
> so does an out-of-range opcode, and so does a null manager. **A caller cannot distinguish success
> from either failure by the result**, which is a constraint on any reimplementation that wants to
> report errors here — the original does not.
* `002FB2A0(slotIndex)` — clears the presence table entry.
* `00300B80(itemId, quantity, 1)` — grants one stack to the inventory.
* `002FB150` overlap test and `00319850` nearest selector read the pool; neither mutates it.
* `EnemyChain_TryAdvanceRank` (`003183D0`) reads the collected counter `022C3174`. On the path where the chain count has
  not passed the rank's threshold, it subtracts `(rank + 1) × counter` unless `022C3178` bit 0 waives it, and zeroes the counter on a rank advance. So collecting a
  pickup slows the enemy chain. See [the chain page](loot-drops-and-enemy-chain.md). *(Added 2026-09-29, pass 1.)*

## 7. State transitions

```
free(0) --create--> 1 --world object ready--> 2 --+
                                                  |  blink steps, states 2..6
                                 6 <--------------+
                                 |
                                 7 --stamp+1800 <= now--> RETIRE --> free(0)
       any state --collect--> RETIRE --> free(0)
       any state --remove --> RETIRE --> free(0)
       any state --evicted (pool full, node is head)--> RETIRE --> free(0)
```

**State 1 → 2 [page]:** when `FUN_0028EFE0(handle) == 2` the node stamps the clock, moves to 2 and
publishes its position.

**States 2–6, and 7.** `00319664` computes `cvttss2si(-30.0f × scalar) = -30`, then
`imul ecx, eax, 0x3C` → `-1800`, then `stamp − (−1800)` and compares the field clock: **state 7 fires
at `now ≥ stamp + 1800`**. `003196E9` builds `7 − state` and `0x3C` the same way for 2–6. Both match
the page's `stamp + 30 × (0x3C − (7 − state))`, verified rather than carried.

## 8. Script · resource · event interactions

None directly. The drop buffer is produced upstream; the pool neither reads authored tables nor
runs script.

## 9. Determinism

**Fully deterministic given the field clock.** No RNG is read on any path. The blink schedule is a
pure function of `materialiseStamp`, the clock, and the `01DFE0B8` scalar; the eviction victim is a
pure function of list order. **Two machines with the same clock and the same drop sequence produce
the same pool state** — which is what makes this reproducible in a differential test.

## 10. Failure paths and edge conditions

* **Pool full** — no refusal. The head is retired mid-call and immediately reused (`00319CDC`
  through `00319D3C`, then falling into the append at `00319D3F`). A player can see a pickup vanish
  with no despawn.
* **The payload slot is uninitialised for ops 4 and 5.** Both the tick despawn (`003196BF`) and the
  eviction (`00319D1A`) do `lea r8, [rsp+0x20]` **without writing `[rsp+0x20]`**; only collect
  (`003199BB`) and remove (`003197F5`) store a value there first. So ops 4 and 5 are handed stack
  residue. See §14.
* **Empty list** — the tick returns immediately on a null head (`0031961F`).
* ~~**Short drop buffer** — the grant loop stops at the first `itemId == 0xFFFF`, but create always
  copies the full 56 bytes, so entries past the sentinel are copied and never read.~~
  **`0xFFFF` is a skip marker, not a sentinel.** *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 309; `00319943`–`00319972` re-read.)* The collect loop runs exactly seven times
  (`esi = 7`, `00319943`). On each entry it tests the id word against `0xFFFF` and jumps over **that entry only**
  (`00319954`–`00319958`, `je 0031996A`); every other entry goes to `Inventory_GrantEncodedLootItem(id, qty, 1)`.
  - Entries after a `0xFFFF` are still granted.
  - An all-zero entry is granted as `00300B80(0, 0, 1)`. EXP-141's collect case observes four such `0:0` grants.
  - Create's `+0x58` handle is the only value EXP-141's stubs supply.

## 11. Observable behaviour

Ten pickups maximum; the eleventh drop destroys the oldest. Each pickup disappears 1800 field-clock
units — sixty seconds at either frame rate **[page]** — after it materialises, having blinked through
five intermediate steps. Walking over one grants ~~every entry before the sentinel~~ every entry whose id is not `0xFFFF`,
including zero entries, and increments the collected counter *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 309; `00319943`–`00319972` re-read.)*.

## 12. Reproduction formula

```c
#define LOOT_POOL_N 10
typedef struct { uint16_t itemId; uint16_t _pad; uint32_t quantity; } DropEntry;  /* 8 */
typedef struct {
    uint32_t  slotIndex;          /* +0x00, set once at init, never rewritten */
    uint32_t  state;              /* +0x04, 0 = free                          */
    uint32_t  materialiseStamp;   /* +0x08                                    */
    uint32_t  _pad0C;             /* +0x0C, forced by the pointer below       */
    struct Node *prev, *next;     /* +0x10, +0x18                             */
    DropEntry drops[7];           /* +0x20 .. +0x57                           */
    uint32_t  objectHandle;       /* +0x58                                    */
    uint32_t  _pad5C;             /* +0x5C, forced by struct alignment        */
} Node;                           /* sizeof == 0x60 */

static void retire(Node *n, int op, uint32_t payload) {   /* the shared sequence */
    if (n->prev) n->prev->next = n->next; else g_head = n->next;
    if (n->next) n->next->prev = n->prev; else g_tail = n->prev;
    presentation(n->objectHandle, op, &payload);
    presence_clear(n->slotIndex);
    n->state = 0; n->materialiseStamp = 0;   /* one 8-byte store in the original */
    n->next = n->prev = NULL; n->objectHandle = 0;
}
```

`retire` appears **four times** in the image — eviction (op 5), despawn (op 4), collect (op 3),
remove (op 3) — identical but for the opcode and payload. Reimplement it once.

## 13. Runtime validation

~~**None.** Nothing here was observed running; every statement is static.~~ **[live]** The page's own
`UQ-137` — that the `+0x58` handle requires the world-object manager to sit below 4 GB — ~~is a live~~
~~question and remains open.~~ is closed *(answered: see the register row UQ-137, SUPERSEDED 2026-09-26 under the runtime rule — the requirement chain is static and replayed (EXP-141) — and the pool page's ticked §5 box; 2026-10-02, OPUS)*.

### 13a. The five ops execute — `EXP-141`, and why nothing cited it (FABLE, 2026-09-21)

**`EXP-141` (`world-loot-pickup-pool-exec`) ran the exact five entry points §2 names** —
`00319B10`, `00319CA0`, `00319600`, `00319920`, `003197B0` — as shipped bytes under Unicorn,
**68/68 functional cases and 57/57 byte-precise mutants killed, stable across three processes**,
through the real presentation dispatcher, presence helpers, object lookup, drop-tier classifier and
pointer decoder.

| this contract said | execution found |
|---|---|
| INIT clears the ten nodes | Unrolled: `state+stamp` zeroed as **one qword** at `+4`, links `+0x10`/`+0x18` and handle `+0x58` cleared, slot index written, head/tail globals zeroed, then a tail-jump that clears the ten presence flag bytes at `0x22BE7F0 + i·0x20` |
| CREATE finds a free slot | **The scan reads `d[node+4]` with stride `0x60`** — the *state dword*, not the handle and not a flag byte. On a **full** pool it retires the head through presentation op5 **before** relinking and then reuses that same node at the tail |
| the drop payload is copied in | **56 bytes** (three `movups` + one `movsd`) into `node+0x20..0x57`; `d[node+4] = 1` arms state 1; the op1 return is stored at `node+0x58` |
| the blink ladder advances per tick | TICK walks the head list **once**; **the retire clears the node's next pointer before the loop advance reads it, so a despawn ends the walk — at most one retirement per tick** |

**Two things execution added that the static reading could not.** The op1 payload's fifth word is
`TBLZ[gidx]` read out of the table at `0x1EED3A8`, which **ships as the identity `[0,1,2,3]`** — so
under shipped data it is indistinguishable from `gidx`, and the experiment separated them by
patching `TBLZ[3]` and watching the patched value arrive. And the rare classifier's jump-table arms
are **compiler-interleaved**, not sequential, so the class-to-tier map is `[1,2,3,4,6,7,8,9,5]` by
arm rather than by order — a reimplementation that reads the arms in address order gets four of nine
classes wrong.

**The evidence class is `NATIVE-REPLAY`-adjacent, and the boundary is disclosed.** The executed
instruction stream, branch outcomes, callback order and arguments, and memory effects are native
authority for the inputs supplied; **the pool, descriptor, item rows and manager are synthetic
fixtures and are MODEL-PROVEN**, and five leaf calls are scripted at their boundaries (the
dispatcher, marshalling and return plumbing are real). **So this does not make the row live**: what
is still unobserved is that *initialized gameplay* drives these inputs — reachability, not
behaviour. ~~`UQ-137` is untouched by it.~~ *(answered: `UQ-137` is closed, SUPERSEDED 2026-09-26 — see §13; 2026-10-02, OPUS)*

> **Why this subsection had to be written at all.** `EXP-141` declares
> `contract: 08-World-Entities/CONTRACT-world-loot-pickup-pool.md` in its frontmatter, and **that
> directory does not exist** — this contract lives under `13-Rewards-Progression-Economy/`. It is the
> **only** experiment in the corpus whose `contract:` path fails to resolve (141 carry the key: 65
> honestly declare `none — <reason>`, 75 resolve, 1 does not). One wrong path is why a complete
> execution package aimed at the verdict table's **first** row sat uncited on every page for as long
> as it did. The experiment record is ORACLE's artifact and is **not** edited here; the frontmatter
> repair is routed to its owner.

**One neighbour note, because the word would otherwise account for the layer by accident.** Adding
§13a puts the word *gameplay* on this page, which is enough to clear the **Gameplay** layer in the
crossing audit — and an accounting that happens by coincidence is not an accounting. So, said
deliberately: the **Gameplay** edges here are two callers of a single shared predicate this contract
already cites, reached from the reward and licence sides of the game rather than from the pool.
**The far ends are not cited** — naming one would import its neighbours for a crossing this contract
does not assert — and the relationship class is *a shared callee's other callers*, not a dependency
of the pickup pool.

## 14. Unresolved

* ~~**Does `0028F000` read its payload for ops 4 and 5?**~~ **RESOLVED 2026-09-21 (OPUS): the
  callee ignores it, and the stack-residue alternative is refuted.** Ops 4 and 5 share the single
  jump-table target `0028F076`, whose first instruction is `xor edx, edx`; **`R10` — the payload
  pointer — is never read on that path**. The uninitialised stack slot the two callers pass is
  therefore harmless, and **no behaviour here depends on stack residue**. See §6 for the full
  opcode table. *This removes the only nondeterminism this contract had entertained.*
* **State 1 → 2** — the page's reading is `FUN_0028EFE0(handle) == 2`. **`0028EFE0` re-derived
  2026-09-21 (OPUS) and it is not a field read**: `mov edx, ecx` / `mov rcx, [0209BE80]` /
  `add rcx, 0x57E0` / `jmp 003FA730` — a tail call into the manager's **`+0x57E0` sub-object**,
  passing the handle. So the state the ladder tests is owned by that sub-object, not by the pool
  node. ~~**What `003FA730` returns for a given handle is still not re-derived**~~ — **ANSWERED
  2026-09-21 (FABLE, from `EXP-141`): the transition is a read of the resolved object's own
  `+0x260`.** Execution records state 1 as *handle lookup through `0028EFE0` → `d[obj+0x260] == 2`
  → publish presence → state 2*, so the `== 2` is compared against a dword field of the world
  object, not a return value computed by the sub-object. **What remains is narrower**: what *writes*
  `[obj+0x260]`, and whether it takes values other than 2 **[page]**.
* ~~**`00319850`, the nearest selector, still has no caller** in the function graph **[page]**~~ —
  **CORRECTED 2026-09-23 (SWE2-CONTRACT): it has exactly one — `BattleLocomotion_DecodeOrderGoal`
  (`00312730`) calls it at `003129AF`, on order-goal opcode `0x4165`** (the `>0x4035` tail switch subtracts
  `0x4124`, then `1`, `0x25`, `4`, and tests `0x17`: `0x4124+1+0x25+4+0x17 = 0x4165` — the
  second-to-last opcode of the `0x4000`–`0x4166` internal-order band). The call passes the unit
  (`rcx`) and a position out-pointer (`rdx`) and treats a negative return as *no pickup found* —
  so order `0x4165` resolves to "the nearest active world pickup". The function-graph index simply never
  recorded the edge; a whole-`.pdata` immediate-operand census finds it (and no other caller —
  `call`/`jmp`, `lea`, data-slot and disp32-RVA forms all negative besides this one site).
* ~~**`UQ-137`** **[live]**.~~ *(answered: `UQ-137` is closed, SUPERSEDED 2026-09-26 — see §13; 2026-10-02, OPUS)*

## 15. Evidence

~~Static only~~ **— static plus one isolated-execution package, `EXP-141` (§13a), whose class is
NATIVE-REPLAY over MODEL-PROVEN fixtures; updated 2026-09-21 (FABLE)** — all against
`73461d08…21f8`. Read this session: `00319B10`, `00319CA0`, `00319600`,
`00319920`, `003197B0`. Measured: `data_xref_scan.py` over 34,270 bodies for `+0x0C` and `+0x5C`
across all ten slots — **0 of 10 each**, with the pool base resolving and the live field `+0x58`
found at the same stride as a positive control. `check_alignment.py` passes and does not list this
type, so its `0x60` already satisfies the tail-padding rule I4 rests on.

## 16. Parity plan

A differential test can drive this from §12 without the binary: seed a clock, issue eleven drops,
and compare the pool array and the two list globals byte-for-byte after each step. The blink ladder
is checkable by stepping the clock to `stamp + 30 × (0x3C − (7 − state))` for each state and
asserting the transition fires on that tick and not the one before. **The padding bytes must be
excluded from any byte-for-byte compare**, since no path writes them and their contents are whatever
the allocation left behind.

## Falsification pass 1 — 2026-09-29 (OPUS): every clause survives; the collected counter's reader added

**Attack.** Every structural clause of §2-§10 and §12 became a check that fails if the shipping image says otherwise. The
checks decode every listed body in `.text`, so the field census, caller counts and the call closure are whole-image.
Script: `Tools/analysis-kit/gfz-scripts/falsify_world_loot.py`, output `falsify_world_loot.out`, image `73461d08…`, 0 BROKEN.

| # | Clause attacked | Killer | Result |
|---|---|---|---|
| W0 | §2 sizes and callers | another size or caller | **survives**: 387, 394, 423, 215, 113, 26, 26 B; init has 2 call sites, the rest 1 each |
| W1 | I1 ten nodes of `0x60` | another bound, stride or slot set | **survives**: `add rbx, 0x60` / `cmp eax, 0xa`; init writes `+0x00` of nodes 0-9; head = pool + 10 × `0x60` |
| W2 | I3 `slotIndex` written only by init | a second writer | **survives**: every RIP-relative store to `+0x00` is init's; no zero-displacement dword store in the other six |
| W3 | I4 `+0x0C` and `+0x5C` are padding | a reference at either offset | **survives**: image-wide RIP hits `+0x0C` 0, `+0x5C` 0, `+0x58` 10 (control); no register-relative use in the entries |
| W4 | I5 FIFO | another append or victim | **survives**: tail store at `00319D67`, head load at `00319CDC` |
| W5 | §12 the four retire opcodes | another opcode | **survives**: eviction 5, despawn 4, collect 3, remove 3, plus blink 2 and create 1; six presentation calls |
| W6 | §6 dispatch | another range or table | **survives**: `lea eax, [rdx-1] / cmp eax, 5 / ja`; table entries 4 and 5 identical (`0028F076`: `mov rcx, rbx / xor edx, edx / call 003FA820`); op 3 also calls `003FA820` |
| W7 | §10 ops 4 and 5 get an unwritten payload | a store before the `lea` | **survives, made exact** (below) |
| W8 | §5 the collected counter | another writer | **survives**, and it has a reader outside the pool (below) |
| W9 | §2 no caller uses a return value | a read of `eax` after a call | **survives** at all six call sites |
| W10 | §9 no RNG on any path | a generator in the closure | **survives** over the whole 215-body closure, presentation layer included: no generator entry, and no reference to the gameplay LCG or presentation PRNG cells |

* **W8: `022C3174` is the chain penalty's input, not only a statistic.** The pool increments it once per collect
  (`00319974`). `EnemyChain_TryAdvanceRank` (`003183D0`) is its only other reader:
  * when the chain count has not passed the current rank's threshold, it multiplies the counter by `rank + 1` and subtracts
    the product from the count (`0031842A`), unless the waiver bit at `022C3178` is set;
  * it zeroes it when the rank advances (`003184EC`).

  So every pickup collected makes the next chain rank harder to reach until the rank advances.
  [The chain page](loot-drops-and-enemy-chain.md) already documents this penalty. §6 did not relate the two, and now does.
* **W7: what the despawn's payload holds.** In create, nothing writes `[rsp+0x20]` before the eviction's `lea` at
  `00319D1A`. In the tick, `[rsp+0x20]` is written only by the blink (`00319720`) and at `0031976F`, both later in the
  loop body, and the loop jumps back to `00319640`. So the despawn at `003196BF` passes one of two values:
  * the previous iteration's blink payload, or the `movdqa` at `0031976F`;
  * older stack contents, on the first iteration.

  Neither matters, because ops 4 and 5 zero `edx` and never read the payload (W6).

Consumer record: [`_index/candidates/world-loot-falsification-pass-1-0929/`](../_index/candidates/world-loot-falsification-pass-1-0929/README.md).
No contradiction row: nothing the contract asserted was false.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE (4 edges).** `Loot_FindOverlappingPickupIndex` (`002FB150`) calls `Actor_GetWorldPosition` (`00265020`) and `ActorRuntime_GetClass3FloatPair` (`00265090`), and `BattleLocomotion_DecodeOrderGoal` (`00312730`) calls `00265090` and `BattleUnit_FindByDefinitionSelector` (`002367A0`). The overlap test takes the collecting unit's position and its two radii from those getters, and the order-goal decoder resolves units and radii the same way; the pool's own state is not reached.

**CombatAI — CLIENT (1 edge).** `AiOrder_CheckActionPreconditions` (`00301830`) calls `00312730`: an AI order's precondition check decodes the order's goal through the same decoder whose opcode `0x4165` arm asks this pool for the nearest active pickup (section 14).

**CombatAction — CLIENT (1 edge).** `002FDA60`, a 464-byte switch arm the census names caseD_4000, calls `00312730`: the action side decodes internal orders of the `0x4000` band through the same decoder, one of whose opcodes is the "go to the nearest pickup" goal.

**Core — CLIENT (1 edge).** `002341C0`, a 62-byte battle-storage reset batch, calls `Loot_InitializeWorldPickupPool` (`00319B10`) after clearing the pending action queues, the navigation dataset and the perception cache: the pool reset of this contract is one step of that batch.

**Gameplay — SERVICE and CLIENT (3 edges).** `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` (`00316DF0`) and `DefinitionRuntime_DeactivateAndRemoveConfiguredItems` (`00323540`) call the grant `00300B80`, and `00312730` calls `BattleRuntime_GetModeDependentDistanceThreshold` (`00309A90`). Definition activation grants and removes items through the same call the collect path uses, and the order-goal decoder takes a mode-dependent distance from that layer; neither touches a pool slot.

**Items_Equipment_Shops_License — SERVICE and CLIENT (3 edges).** `Loot_CollectWorldPickupAndGrantInventory` (`00319920`) calls `Inventory_GrantEncodedLootItem` (`00300B80`), which tail-calls `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`003008A0`) with the discovery update forced on, and `BattleStats_SetLicenseNodeStateAndApplySideEffects` (`00323910`) calls `00300B80` too. The seven-entry grant of a collected pickup is that layer's inventory write; the licence side effect is another user of the same grant.

**Movement — SERVICE and CLIENT (6 edges).** `00312730` calls `Loot_FindNearestActivePickupPosition` (`00319850`) on order-goal opcode `0x4165` (section 14) and calls that layer's `00309B10`, `BattleUnit_GetNavigationClearanceRadius` (`0030A130`), `00312DF0` and `0031ABE0`; and the visual create `003FA160` calls `0026E350`, the two-step registry resolve it runs when placing a pickup record. Movement consults the pool for an order goal, and the pickup visual uses one movement-filed resolve at placement; the pool's slot state is written by neither.

**Party — SERVICE (2 edges).** `00312730` calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`) and `BattleUnit_GetPartyLeader` (`003272A0`): the order-goal decoder resolves the focused unit and the party leader through that layer; which opcodes use them is not read here, and the pool's own bodies call neither.

**Presentation — SERVICE (1 edge).** `Loot_CreateWorldPickup` (`00319CA0`) calls `Loot_DeriveWorldPickupPresentationTier` (`00319A20`), filed to that layer: the pickup's visual tier is computed there from the seven drop entries, and the tier travels in the create op's payload.

**Resource — SERVICE (1 edge).** The visual create `003FA160` calls `0024A5A0`, the lookup that finds an entry by name in the 64-slot named-image table: the pickup's two visual objects are fetched by name, and no pool state crosses.

**Script_VM_Native_Bridge — CLIENT (1 edge).** `0050FAF0`, a 205-byte script-VM body, calls the grant `00300B80`: a script native grants an item through the same call a collected pickup uses, without touching the pool.

**Status_Periodic_Terminal — CLIENT (3 edges).** `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) calls `002FB150`, `Loot_RemoveWorldPickupByIndexWithoutGrant` (`00319830`) and `Loot_CollectWorldPickupByIndex` (`00319A00`): the periodic maintenance runner is the pool's only collector, and chooses between the collect and the no-grant remove by whether the unit's stats record is a party record.
