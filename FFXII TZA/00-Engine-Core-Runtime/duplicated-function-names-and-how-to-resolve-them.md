---
system: Duplicated function names, and how to resolve them
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: CodeDomain — shared; no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 22 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-03
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-thunk-names-pass-1
  crossref_clean: true
  reopened_count: 0
---

# Duplicated function names, and how to resolve them

> **Seven hundred and fifty functions in this image have a five-byte `jmp` thunk pointing at them, and
> only fifty-eight of those thunks share their target's name.** A caller census that names the body
> returns **zero** for 140 of them and **undercounts** 185 more — and the name-sharing cases, which
> this document opens with, are the small visible corner of that.
>
> **The title says "names" because that is where the hazard was found. Section 4 says "thunks"
> because that is what it is.**

## 1. Why this matters

Two separate failures in one session came from one collision, `RNG_MT19937_Seed`:

- a **caller census returned zero** — the query named the **body** (`00863D30`) while the call graph
  indexed the **thunk** (`00379CF0`), which is what callers actually reference;
- a **bulk anchoring pass wrote the wrong address** — a name→address map kept whichever entry came
  last, and stamped the body's address onto the thunk's row.

> **Two tools, two assumptions, one name.** Neither failure looked like a failure: the census returned
> a clean zero, and the anchor was a real address of a real function with that name.

## 2. The census

Every name in the function list carried by more than one entry:

| classification | groups |
|---|---:|
| **thunk + body** — one entry is a short `jmp` to another entry in the same group | **53** |
| **thunk chain** — a thunk whose target is itself a thunk | 1 — **and §4's rule cannot identify it; §9** |
| **genuinely distinct bodies** | **3** |
| **total** | **57** |

Group sizes among the thunk+body cases: **48 pairs, 3 triples, one group of four, one of five.**

## 3. The three genuine collisions are compiler artifacts, not engine naming

| name | entries |
|---|---|
| `` `scalar_deleting_destructor' `` | `00788F10` (62 B), `008087C4` (137 B), `00854F00` (62 B) |
| `malloc` | `0085E730` (7 B), `00861F2C` (6 B) |
| `scheduler_resource_allocation_error` | **eight** identical 47-byte bodies from `001F17B0` to `001F1ED0` |

**All three are generated, not authored.** MSVC emits one `scalar_deleting_destructor` per class;
the eight `scheduler_resource_allocation_error` bodies are duplicated throw helpers of identical
size. **No engine function shares a name with a different engine function** — every other collision
is a name and its own thunk.

> **That is the reassuring half of the result:** ambiguity here is a property of the *linker*, not of
> the naming, so it is mechanically resolvable rather than requiring a judgement about which
> `Foo` was meant.

## 4. The resolution rule

Within a group, the thunk is identifiable without ambiguity: **its body is ≤ 16 bytes and its first
instruction is a `jmp` to another entry in the same group.** Everything else is the body.

> **Not without ambiguity — the rule misses the one chain §2 counts (2026-09-13, §9).**
> `thunk_FUN_0035b650` is `00379F20` → `0035B450` → `0035B650`. `00379F20`'s first instruction is
> **`mov dl, 2`**, not a `jmp`, and `0035B450`'s `jmp` leaves the name group. So the group this
> document singles out as the chain is exactly the one its resolution rule cannot classify — and
> `00379F20` is **not a transparent forwarder**: it presets an argument.

**Which one to take depends on the question, and this is where both failures came from:**

| the question | resolve to | because |
|---|---|---|
| *what calls this?* | the **thunk** — or the union | callers reference the thunk; the body may have **zero** direct callers |
| *what does this do?* | the **body** | the thunk is one instruction |
| *what address do I cite?* | the **body**, unless the claim is about the thunk | an anchor should reach the code the claim describes |
| *is this reachable at all?* | **the union, followed transitively** | a thunk chain exists (§2) |

> **A name is not an address in this corpus.** Resolving one to the other is a choice, and a tool that
> makes it silently has answered a different question than the one it was asked.

### How large the caller-census exposure actually is — and it is not 53

The first row of that table is not a theoretical hazard. Within the 53 name-collision groups,
**30 bodies have zero direct callers** ~~while their thunk has some~~ — `RNG_MT19937_Seed` among
them, alongside `WorldTransition_RequeueCurrentFieldForRestore` and all four
`InputGameplay_GetActorStateAwareRemappedMask*` variants.

> **Corrected 2026-09-13 (§9): the 30 is right; the clause holds for 13 of them.** All six named
> above are among the 13. For the other **17 the thunk has no edge either** — so the
> body-versus-thunk hazard this sentence exists to illustrate does not apply to those, and
> something else reaches them: every one of the six sampled is the target of a stored pointer
> (§9).

**But 53 is the wrong denominator, and this document said so a revision too late.**

Dropping the name requirement and asking instead *which listed functions have a short `jmp` thunk
pointing at them*:

| | functions |
|---|---:|
| have at least one short `jmp` thunk aimed at them | **750** |
| …of which the thunk **shares** the target's name | **58** |
| …of which the thunk has a **different** name — invisible to any name-keyed census | **692** |

And of the 325 whose thunks actually carry callers:

| | functions |
|---|---:|
| target has **ZERO** direct callers — a body-named census returns `0` | **140** |
| target has callers but **silently undercounts** by the thunk route | **185** |

> **The hazard is thunks, not duplicated names — and only 8 % of thunks share their target's name.**
> A census keyed on the name finds the name-shaped subset of a thunk-shaped problem, which is exactly
> the failure this document was written to describe, committed by the document itself.

**Both of this session's failures land in the corrected population:** the false *"zero callers"* is
one of the **140**, and a gil caller count published as 19 when it was 22 is one of the **185** — see
[`gil-storage-clamp-and-every-path-that-moves-it.md`](../13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md) §4.

**A zero from a caller census is not evidence of anything until thunks are followed.** It looks
identical to a real absence, and **an undercount looks like a number**, which is worse.

**Any claim of the form "N callers" needs to say whether thunk routes were included.**

> **…and which graph they were counted in (added 2026-09-13, §9).** The **750 / 58 / 692** above
> are derivable from the image alone. The **325 / 140 / 185** are not: they reproduce exactly
> from `Tools/work/graph/edges.tsv`, while a direct `rel32` census over the **whole** of `.text`
> — the unlisted gaps included — reaches **234 / 132 / 102**. Neither is wrong. But a document
> whose closing rule is the sentence above has to name its own edge set, and this one did not.

### The 750 is itself a lower bound, and by how much

Every count here is taken over the **function list**, which covers 92.91 % of its own span — so a
thunk sitting in the 509,214 bytes between listed bodies is invisible to this census exactly as it is
to any other.

Scanning those 33,346 gap regions for a five-byte `E9` jump landing on a listed function:

| | |
|---|---:|
| `E9` -> listed function inside the gaps | 255 |
| …**isolated**, padding on both sides — a standalone thunk | **17** |
| …embedded in surrounding bytes — the tail of unlisted code | 238 |
| distinct targets gaining a thunk this census could not see | **16** |

> **So 750 should be read as at least 766.** The undercount is real and small — about 2 % — which is
> worth knowing precisely because the *raw* hit count would have suggested 34 %.

**The isolation test is what separates them.** An `E9` in unlisted bytes is far more often the tail of
a function Ghidra never defined than a thunk; **only padding on both sides makes it a standalone
stub.** Counting the 255 would have inflated this document's own correction fifteenfold.

## 5. Modding notes

**A hook placed on the body will miss callers that go through the thunk**, and vice versa — the same
hazard as an accessor that some readers bypass. **For 750 functions in this image, *"hook the
function"* is ambiguous until the thunks are resolved**, and for 140 of them the body is not where
the calls arrive at all.

## 6. What is not known

- **Why some functions have thunks and others do not.** 750 of ~34,000 listed functions have one;
  nothing here explains the selection.
- **How many of the 692 differently-named thunks are load-bearing** in documents that cite their
  targets. The 58 name-sharing cases were reviewed against the corpus; the other 692 were not.
- **Whether the thunks are incremental-linking stubs or deliberate indirection.** Their uniform
  five-byte `jmp` shape is consistent with the former and this document does not establish it.
  *Narrowed 2026-09-13 (§9):* the uniformity is **exact** — all **835** entries the rule accepts
  are a bare five-byte `jmp` and nothing else. But `00379F20`, the chain's first link, presets
  `dl = 2` before jumping, so **at least one stub in this image is a default-argument forwarder**
  — deliberate indirection, and outside the 835 precisely because the rule requires a bare jump.
- [x] ~~**Whether any thunk is ever the target of a data pointer** rather than a call.~~
  **Answered 2026-09-13 (OPUS, §9): yes, and it is not rare — 384 of the 835 thunks, 46 %.**
  They are named by **641** aligned qword references in `.rdata` and **171** in `.data`. For
  those the address other code *holds* is the thunk, which is a third route past both censuses.

## 7. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 57 names carried by >1 entry | grouping the whole function list by name | 1 |
| 53 are thunk+body | each short entry disassembled; first instruction is `jmp` to a group member | 1 |
| Group sizes 48/3/1/1 | the same grouping | 1 |
| The three distinct-body collisions | their sizes and addresses read from the list; bodies inspected for the `jmp` test and found not to be thunks | 1 |
| `RNG_MT19937_Seed`'s thunk is `00379CF0` → `00863D30` | the five-byte body decoded: `jmp 0x863d30` | 1 |
| 30 of 53 bodies have zero direct callers | direct-caller counts taken for both entries of every group | 1 |
| 750 functions have a short `jmp` thunk aimed at them; 58 share the name | every listed function <= 16 bytes disassembled and its `jmp` target resolved against the function list | 1 |
| 140 targets return zero from a body census; 185 undercount | direct-caller counts for each target and its thunks | 1 |
| 17 further standalone thunks lie in unlisted bytes, reaching 16 targets | every inter-body gap scanned for an isolated five-byte `E9` to a listed entry | 1 |

**Controls.** The thunk test is positive, not assumed: every short entry was disassembled and
classified by **whether its first instruction is a `jmp` whose target is another member of the same
name group**. The four non-thunk groups were produced by that test failing, not by exclusion — which
is why the chain case (`thunk to a thunk`) separated out rather than being miscounted as a body.

## 8. Related

- [`which-roll-is-on-which-generator.md`](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) §11 — the caller census that returned zero, and why.
- [`the-encoded-id-class-registry.md`](the-encoded-id-class-registry.md) — a reference document whose anchoring pass hit the same collision.

## 8b. The other direction: one address, several identities - `0016D6A0` (added 2026-09-13, OPUS)

This document is about **one name on several addresses**. The inverse happens too, and it is worse
for a reader, because nothing in a name list shows it.

**`0016D6A0` has a three-byte body: `ret`.** It is reached as at least two different things:

| reached as | from | argument convention |
|---|---|---|
| the **Control Flow Guard check** | `GuardCFCheckFunctionPointer` in the load config points at slot `008C31C0`, which holds `0016D6A0`; the forwarder `0017E7D0` jumps to it and the census names it `_guard_check_icall` | a single target pointer |
| the **array-delete helper** | all **1,149** `PClassDescriptorForType` deleting destructors call it as `mov edx, <objectSize> / mov rcx, this / call 0016D6A0` | `this` plus a size |

**Those are not the same function.** A CFG check and an array-delete helper have different
signatures and different callers, and both call sites are in the shipped image.

**Measured:** the body is `ret`, and it is called from two contexts with incompatible argument
conventions. **Inferred:** MSVC's `/OPT:ICF` folded them, because every no-op compiles to the same
three bytes and the linker merges identical COMDATs. The inference is the natural one and it is
labelled, not asserted.

Two things follow that a reconstruction needs:

- **The census name is one identity, not the identity.** `_guard_check_icall` is what *a* caller
  believes it is calling. Reading the name as the function's purpose gets the deleting-destructor
  call sites exactly backwards.
- **The array-delete arm of all 1,149 destructors frees nothing.** The size is computed, passed and
  discarded. A reconstruction that implements it as a real `operator delete[]` will free memory the
  shipped game does not.

Corroborating the first row: the image's `GuardCFFunctionTable` and `GuardCFFunctionCount` are
**both 0**, so CFG ships with no valid-target table and its check is *supposed* to be inert
([the thunk layer](../24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md)
§12). **A folded no-op is invisible to every instrument that works on names**, which is the same
lesson as §4's resolution rule pointed the other way: resolve by address and by body, never by
label.

Found while proving the deleting-destructor family in
[Phyre reflection](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
§9.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment. 144 documents hit on
`thunk`, which is the point of the page.)*

### What reproduces, and the mistake I made first

| claim | measured |
|---|---|
| **57** names carried by more than one entry | **57** |
| **53** name-collision groups containing a thunk | **53** |
| the three genuinely distinct groups, with their addresses and sizes | all three, exactly as listed |
| `RNG_MT19937_Seed`'s thunk `00379CF0` → `00863D30` | the five bytes decode to `jmp 0x863d30` |
| **750** functions with a short `jmp` thunk; **58** name-sharing; **692** not | **750 / 58 / 692** |
| **30** bodies in the 53 groups with zero callers | **30** |
| **325** targets whose thunks carry callers; **140** zero; **185** undercount | **325 / 140 / 185** |
| **238** embedded `E9`s in the unlisted gaps | **238** |

> **The 325 / 140 / 185 did not reproduce until I found the right graph, and I nearly filed that as a
> defect.** A direct `rel32` census over every listed function body gives **234 / 132 / 102**. Widening
> it to a byte scan of the **whole** of `.text` — so the 509 KB of unlisted gaps are included, which
> was my first hypothesis for the gap — changes **nothing**: still 234 / 132 / 102. Adding data-pointer
> references overshoots to 614 / 256 / 358. The numbers come from
> **`Tools/work/graph/edges.tsv`**, where all three land exactly, on all three snapshots of it.
>
> **That is the finding, not a correction.** This document's closing rule is *"any claim of the form
> 'N callers' needs to say whether thunk routes were included"*. The same standard applies one level
> up: **it has to say which graph**, because the same question has two defensible answers here that
> differ by 40 %.

### ⚠ "30 bodies have zero callers **while their thunk has some**" — true of 13

Counted in `edges.tsv`, **30** bodies in the 53 groups have no incoming edge, exactly as claimed. But
only **13** of them have a thunk that does. The six names §4 offers are all among the 13
(`RNG_MT19937_Seed` `00863D30` against thunk `00379CF0` with 2;
`WorldTransition_RequeueCurrentFieldForRestore` `00314530` against `00267C90` with 3; and all four
`InputGameplay_GetActorStateAwareRemappedMask*` bodies against thunks with 3, 3, 4 and 3) — **so every
example is right and the generalisation is not.**

For the other **17**, body and thunk are *both* edgeless. Three of the seventeen:

| name | body | thunk |
|---|---|---|
| `SpawnGroup_TeardownAllGroupedSpawnUnits` | `00234880` | `00510840` |
| `SpawnGroup_TeardownAllUngroupedSpawnUnits` | `00237690` | `00510830` |
| `Spawn_SetAllSpawnBackedUnitsCurrentHPZero` | `002352E0` | `0050F650` |

> **They are not dead, and the reason is the very thing §6 wondered about.** Every one of the six
> sampled thunks occurs as an aligned qword elsewhere in the image — they are **reached through a
> stored pointer**, so neither the body census nor the thunk census can see the call. The hazard for
> these 17 is worse than the one §4 describes, because *both* keyed censuses return zero.

### ⚠ The one thunk chain is outside §4's rule

§4 says the thunk is identifiable *without ambiguity* by "body ≤ 16 bytes and its **first
instruction** is a `jmp` to another entry in the same group". The group §2 counts as the chain:

```asm
00379F20  mov  dl, 2          ; thunk_FUN_0035b650  -- first instruction is NOT a jmp
00379F22  jmp  0x35B450
0035B450  jmp  0x35B650       ; thunk_FUN_0035b650  -- target is OUTSIDE the name group
```

**Neither entry satisfies the rule**, so the classifier that produced §2's table cannot have produced
that row by this rule, and a reader re-running it gets 52 groups plus one it cannot place. It also
matters in itself: **`00379F20` is not a transparent forwarder.** It sets `dl = 2` and then jumps, so
calling `0035B450` is not equivalent to calling `00379F20`. §6 asks whether the thunks are linker
stubs or deliberate indirection — **this one is deliberate**, a default-argument forwarder, and it is
outside the 835 exactly because the rule demands a bare jump.

Within the 835 the rule *does* accept, the uniformity is total: **every one is a bare five-byte `jmp`
and nothing else**, no trailing padding, no setup.

### ⚠ §6's last unknown, answered: 384 of 835 thunks are pointer targets

Every aligned qword in every non-`.text` section was compared against the 835 thunk addresses:

| | |
|---|---:|
| thunks named by at least one aligned qword outside `.text` | **384 of 835 (46 %)** |
| references in `.rdata` | **641** |
| references in `.data` | **171** |

**Nearly half of these stubs are things other code *holds*, not just things other code calls.** That
sharpens §5's modding note: for those 384, replacing or hooking the body does not intercept a
dispatch through the stored pointer at all, because the pointer names the thunk.

### The gap figures do not reproduce, and I could not recover the rule

§4's last table gives 33,346 regions, 509,214 bytes, 255 `E9` hits, 17 isolated, 16 targets. Building
the gap set from the function list and scanning it gives **33,329 / 509,056 / 253 / 15 / 14** — and
that is stable across **all three** snapshots in `Tools/work/graph/` and three different definitions
of the `.text` range (`min(vs, rs)`, `vs`, and the function-list span). **The embedded count reproduces
exactly at 238**, so the entire difference is 17 more regions and 158 more bytes carrying two more
isolated hits.

> **This is recorded as a reproducibility gap, not as an error.** The deltas are small, one-directional
> and consistent, and the conclusion is untouched: the 750 is a lower bound by about 2 %, **at least
> 764** by this count against the page's 766. But a census offered as re-runnable should be
> re-runnable, and this one is not, from anything in the repository.

**Not claimed.** Which of the 692 differently-named thunks are load-bearing in documents — §6's second
unknown is untouched. Why some functions have thunks — untouched. Whether the 384 pointer references
are vtable slots, jump tables or something else: the **sections** were measured, the structures were
not. The 17 double-edgeless cases were sampled at six, not all seventeen. `edges.tsv`'s own
construction was not audited — it is used here as the page's source, not as ground truth. Nothing was
executed and nothing was observed live.

*(Pass 22 adjacency, 2026-09-14: `002352E0` calls **combat-formula** `00300520` (1 edge) — one of
the duplicated-name bodies lives on the combat side; the disambiguation stands on address, and
this edge is just that body's real neighbour.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `00234880` on this page calls `BattleUnit_TeardownAndDespawn`, owned by that layer. What it reaches is the teardown: it clears `qword[+0x6F8]`, `dword[+0x748]` and `dword[+0x770]`, then branches on **bit `0xE` of `qword[+0]`** for the rest; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAction — CLIENT.** `BattleUnit_HandleActorTimelineEvent`, owned by that layer, calls `00300520` on this page. That caller is the timeline-event handler: it resolves the unit, refuses when bit 1 of `byte[+0]` is set, and otherwise dispatches on the event's `dword[+0]` through a jump table **bounded at 8**; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — SERVICE.** `00300530` (`BattleStats_ModifyHPAndProcessLethalState`, CombatFormula), the shared sibling body `00300520` tails into, calls `BattleTargetBuffer_FindActorWorkIndex` (`00316D70`) and `BattleUnit_DispatchActorPresentationEvent` (`003299B0`) on that layer — the target-work-index resolve and the presentation-event dispatch the HP-modify path runs. Crossing is consumption, not shared ownership.

**Status_Periodic_Terminal — SERVICE.** The same `00300530` calls `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) — the derived-status side-effect pass that follows the HP write. Crossing is consumption, not shared ownership.
- **Input — SERVICE (2 edges).** 2 outbound (page-cited `WorldTransition_RequeueCurrentFieldForRestore` (00314530), `0035B650` call Input bodies `00182D80`, `0035B2F0`). Substantive edges include `WorldTransition_RequeueCurrentFieldForRestore` (00314530) calls `00182D80`; `0035B650` calls `0035B2F0`.
- **RNG_Random_Selection — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_SeedState` (00866D60)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **Resource — SERVICE (1 edge).** 1 outbound (page-cited `WorldTransition_RequeueCurrentFieldForRestore` (00314530) call Resource bodies `001D6C40`). Substantive edges include `WorldTransition_RequeueCurrentFieldForRestore` (00314530) calls `001D6C40`.
- **SaveLoad — CLIENT (1 edge).** 1 inbound (SaveLoad bodies `00280140` call page-cited `WorldTransition_RequeueCurrentFieldForRestore` (00267C90)). Substantive edges include `WorldTransition_RequeueCurrentFieldForRestore` (00267C90) is called by `00280140`.
- **Save_Load_Settings — MECHANICAL (2 edges).** 1 Save_Load_Settings-side calls into shared helper(s) the page cites (`RNG_MT19937_Seed` (00379CF0)); 1 call from page-cited bodies into shared Save_Load_Settings plumbing (`SaveImage_GetPersistentPayloadBase` (002EF2B0)) - the helpers' general call surface, not a Save_Load_Settings relationship of this page's subjects.
- **Spawn_Encounter_Lifecycle — CLIENT and SERVICE (3 edges).** 2 inbound (Spawn_Encounter_Lifecycle bodies `SpawnUnit_FinalizeSpawnEntryActivation` (0023A410), `Spawn_SetAllSpawnBackedUnitsCurrentHPZero` (002352E0) call page-cited `BattleStats_SetCurrentHP` (00300520)); 1 outbound (page-cited `BattleStats_ModifyHPAndProcessLethalState` (00300530) call Spawn_Encounter_Lifecycle bodies `SpawnGroup_RecordMemberDeathAndHandleCompletion` (00306F00)). Substantive edges include `BattleStats_SetCurrentHP` (00300520) is called by `SpawnUnit_FinalizeSpawnEntryActivation` (0023A410); `BattleStats_SetCurrentHP` (00300520) is called by `Spawn_SetAllSpawnBackedUnitsCurrentHPZero` (002352E0); the remaining edges run through shared helpers the page cites.
## The `0035B450` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0035B450` (5 B) — `jmp 0035B650` thunk.

| member | role | interior |
| --- | --- | --- |
| `0035B650` | `movzx edi, dl`, `movsxd rdx, ecx`, `qword[02EC0B68]` non-null (`0035B656`/`0035B663`) | [`0035B656`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `00379CF0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00379CF0` (`RNG_MT19937_Seed`, 5 B) — `jmp 00863D30`.

| member | role | interior |
| --- | --- | --- |
| `00863D30` | same `02EB4234`/`01CCFAC8` prologue; `ebx = ecx` seed (`00863D36`/`00863D49`) | [`00863D36`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `0050F650`/`00510840` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

| root | member (target) | role | interior |
| --- | --- | --- | --- |
| `0050F650` (`Spawn_SetAllSpawnBackedUnitsCurrentHPZero`) | `002352E0` | `dword[0208E6A0]`-counted zero loop | [`002352E8`](../_index/ADDRESS-INDEX.md) |
| `00510840` (`SpawnGroup_TeardownAllGroupedSpawnUnits`) | `00234880` | same `0208E6A0` count — teardown loop | [`00234888`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-19 update (2026-05-15) — `00300520` combat-formula field-read fragment

`00300520` (8 B) is the combat-formula callee this page records `002352E0` reaching (1 edge): its whole body is `sub edx, dword[rcx+0x48]` (`00300520`) + `jmp 00300530` (`00300523`) — it subtracts the record's `+0x48` field from the caller's operand and tails into the shared sibling body `00300530`, the two-instruction prefix the family's callers enter.
