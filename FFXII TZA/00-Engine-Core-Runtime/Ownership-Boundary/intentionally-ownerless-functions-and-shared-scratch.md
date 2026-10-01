---
system: The 585 intentionally ownerless functions, and the shared scratch buffers they write
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: none — this document exists to audit the absence of an owner
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 1 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708, on SNAPSHOT-IDENTITY - replaced rather than re-targeted because that basis is FALSE for this document, which cites a record that changed
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
origin: open question B-4 — "585 functions are deliberately FinalNoPrimaryOwner; re-audit that this is still correct rather than inherited"
---

# The 585 intentionally ownerless functions, and the shared scratch buffers they write

> The ledger accounts for 38,131 functions three ways: 9,409 belong to a subsystem, 28,137 are
> classified by mechanism, and **585 are declared to belong to nobody on purpose** *(figures re-derived
> at GN161 2026-09-14 — written against 38,003 / 9,409 / 28,009 / 585; the write-rate measurements
> below were taken on that earlier set and bound the current one)*. This document
> asks whether that third decision was earned function by function or applied in bulk — and answers
> it by re-deriving the population from the image instead of re-reading the tag.

**The decision holds.** Three independent measurements agree, and the strongest of them is one the
classification could easily have failed. **Three labels within it do not hold**, and they are named.

## 1. What the player sees

Nothing here has a name in the game — and that is the point.

Underneath every visible thing FFXII draws sits a layer of small, sharp helpers: the maths that fits
a curve between two points, packs a colour into a word, walks a mesh, turns a matrix into a screen
position. A Mist-charge animation uses them. So does the map. So does the licence board, and the
weather, and the way a character's shadow falls.

None of them belongs to any of those things. They are the engine's shared tools, and asking "which
part of the game owns this?" is the wrong question — the honest answer is *none of them*.

Two of those tools are workbenches: small slabs of scratch memory the whole engine borrows to do
geometry in. **Two hundred and fifteen different functions write the larger one**, and they come from
graphics, sound, movement and character code alike. Nobody owns the workbench either. It is just
where the work happens.

This matters to a modder for one blunt reason. If you hook one of these helpers expecting to change
how *one* system behaves, you will change how *everything* behaves — and if you leave a value behind
in the scratch memory, the next thing to use the workbench inherits your mess.

## 2. Native mechanism

### 2.1 What the classification actually claims

Each of the 585 carries a sealed decision block. The wording is uniform and it states a testable
rule:

```
DECISION=FINAL_INTENTIONAL_NO_PRIMARY_OWNER_SHARED_INFRASTRUCTURE
CLASS=FINAL_NO_OWNER_ROUTER_ADAPTER_OR_THUNK
POLICY=...primary ownership requires independent subsystem state/lifecycle authority;
       routers, read-side helpers, caller-owned materializers, shared infrastructure and
       lower serializers remain intentionally ownerless.
```

**"Independent subsystem state authority" is measurable.** A router or a read-side helper does not
write module-level state; a function that does is asserting exactly the authority the policy says
would make it owned. So the audit does not re-read the tags — it measures the property the policy
names, over the whole image, and compares.

Below `DECISION` sits a second field that makes the audit sharper, because it subdivides the
population into six classes that predict *different* behaviour:

| CLASS (prefix `FINAL_NO_OWNER_` dropped) | n |
|---|---:|
| `ROUTER_ADAPTER_OR_THUNK` | 254 |
| `READ_QUERY_RESOLUTION_SUPPORT` | 107 |
| `SHARED_GENERIC_INFRASTRUCTURE` | 104 |
| `CROSS_CATEGORY_CONSUMER_OR_BOUNDARY` | 55 |
| `CALLER_OWNED_OR_TRANSIENT_MATERIALIZATION` | 50 |
| `PRIOR_SEALED_BOUNDARY_OTHER` | 15 |

**A bulk sweep would spread those six labels at random across the code. An earned classification
would not.** That is the test.

### 2.2 The population is not what the question implies

Before measuring anything: **583 of the 585 carry `GFZ_V120_X0_PRESENTATION_*` prior evidence**, and
the remaining two are `LEGACY`. All 585 were sealed by a single later batch,
`GFZ_V120_X0_RESIDUAL_CLOSURE_BL`.

So this is **not a whole-image ownerless population**. It is the Presentation category's ownerless
residue, re-sealed in one pass. Any statement of the form "585 functions across the engine have no
owner" is wrong about the *across the engine* part. Every other category's ownerless functions are
accounted for differently — they carry a `CodeDomain` tag instead.

### 2.3 The measurement, with controls

For every function in the image, decoded from the shipped bytes (stopping at `int3` padding, so a
ledger extent that over-runs into the next function cannot contaminate the count): how many
module-level **objects** does it write? A write is a RIP-relative store whose target lies outside
`.text`; adjacent targets within 8 bytes are coalesced into one object, because a function writing
sixty-four consecutive bytes is writing one buffer, not sixty-four globals.

| group | n | writes any module state | median body | median objects written |
|---|---:|---:|---:|---:|
| **the 585 ownerless** | 585 | **10.1 %** | 70 B | 2 |
| control — `PrimaryOwner` | 9,409 | **21.5 %** | 95 B | 1 |
| control — `CodeDomain` only | 28,137 *(was 28,009)* | 17.1 % | 60 B | 1 |
| control — unresolved residual | 30 *(was 158)* | 24.7 % | 828 B | — |

**The ownerless population writes module state at less than half the rate of the owned population.**
That is the direction the policy predicts, it is measured against three controls rather than asserted,
and it is the single figure that would have exposed a bulk sweep: a sweep would have produced a rate
indistinguishable from its neighbours.

### 2.4 The six classes predict the code — which a bulk sweep cannot do

| CLASS | n | median body | median callees | writes state |
|---|---:|---:|---:|---:|
| `READ_QUERY_RESOLUTION_SUPPORT` | 107 | 82 B | 1 | **0.0 %** |
| `ROUTER_ADAPTER_OR_THUNK` | 254 | 56 B | 2 | 2.8 % |
| `CROSS_CATEGORY_CONSUMER_OR_BOUNDARY` | 55 | 130 B | **3** | 12.7 % |
| `SHARED_GENERIC_INFRASTRUCTURE` | 104 | 91 B | 1 | 13.5 % |
| `PRIOR_SEALED_BOUNDARY_OTHER` | 15 | 58 B | 2 | 20.0 % |
| `CALLER_OWNED_OR_TRANSIENT_MATERIALIZATION` | 50 | **279 B** | **0** | **56.0 %** |

Read down the last column. The classes order themselves exactly as their names promise:

- **107 functions labelled "read/query" and not one of them writes a single byte of module state.**
  107 for 107. That is the strongest evidence in this document, because it is the one result a
  careless classification could not have produced by luck.
- **"Router/adapter/thunk"** — median 56 bytes, two callees, 2.8 % write anything. That is a router.
- **"Caller-owned or transient materialization"** — median 279 bytes, **zero** callees, **56 %** write
  module state. A leaf that computes and deposits its answer in shared scratch. Also exactly what the
  name says, and the *opposite* profile from the router class.

Six labels, six distinct profiles, ordered correctly. **The labels were read off the code.**

### 2.5 The shared scratch buffers

The apparent counterexamples — the ownerless functions that *do* write module state — turn out to be
the strongest confirmation, once you look at *where* they write. Nearly all of it lands in one
`.data` page, `022D8F00`–`022D9500`.

> **CORRECTED 2026-09-02 — the object count below is wrong, and the way it was obtained was worse.**
> It came from coalescing write targets by **address adjacency**, which this database bans as proof.
> Re-derived from writer sets, the page holds **62 objects, not 13**, and the "660-byte buffer" is
> three separate 64-byte row blocks plus several unrelated slots. The page is now documented properly
> as [the shared transform workbench](../Shared-Transform-Workbench/the-shared-transform-workbench.md)
> — an **argument-passing area** with one proven 4×4 matrix at `022D91B0`, an unowned clear routine,
> and exactly one function in the image that reads a row it did not write. The table below is kept
> because the *writer counts* in it are correct and are what carried the B-4 argument; only the
> object boundaries were wrong.

The figures as first published:

| object | size | distinct writers | owned writers | ownerless writers |
|---|---:|---:|---|---:|
| `022D9198`–`022D9428` | 660 B | **215** | Presentation 128 · Audio 4 · Movement 2 · ActorEntity 1 | 30 |
| `022D8F90`–`022D900E` | 130 B | 76 | Presentation 33 | 16 |
| `022D8F30`–`022D8F50` | 36 B | 29 | Presentation 6 | 7 |
| `022D9110`–`022D9138` | 44 B | 19 | Presentation 13 · Audio 1 | 2 |

**A 660-byte buffer written by 215 different functions belonging to four different subsystems is not
any one subsystem's state.** It is a shared workbench, and a helper that writes it is borrowing it,
not owning it — which is precisely the distinction the policy draws.

**Do not read the whole page as one object.** It holds **62**, and at least one of them is real
subsystem state documented elsewhere: `022D9138` is the enable/mode word of a random-number stream
([RNG streams](../../21-RNG-And-Determinism/rng-streams.md)), written by just two functions. Address
proximity inside a `.data` page carries no meaning — **only writer sets do**, which is the correction
in [the workbench document](../Shared-Transform-Workbench/the-shared-transform-workbench.md) §10.

## 3. Key addresses

Addresses are Ghidra image base `0x00120000`.

| Address | Working name | Body | Role |
|---|---|---:|---|
| `003B8670` | authored-event / bootstrap coordinator | 4,578 B | **mislabelled** `ROUTER_ADAPTER_OR_THUNK`; 63 distinct callees, 15 written objects |
| `00521BB0` | scratch materializer | 1,757 B | **mislabelled** `ROUTER_ADAPTER_OR_THUNK`; 1 callee, 14 objects, all scratch |
| `005004C0` | effect-subtype switchboard | 497 B | 39 callees — a router, but a large one |
| `00433830` | shared tessellation helper | 3,202 B | writes one 52-byte scratch run byte-wise |
| `00259180` | RNG stream seeding | — | one of only two writers of `022D9138` |

Addresses are Ghidra image base `0x00120000`. **Every row above is a function.**

### Data addresses cited by this document

These are `.data` BSS regions, not functions; the byte counts are **region extents, not body
sizes**, and this block carries no body-size column for that reason.

| Address | Name | Kind | Contents |
|---|---|---|---|
| `022D9198`–`022D9428` | primary shared geometry scratch | BSS region, 660-byte | written by 215 functions across 4 owner categories |
| `022D8F90`–`022D900E` | secondary shared scratch | BSS region, 130-byte | written by 76 functions |
| `022D8F30`–`022D8F50` | small shared scratch | BSS region, 36-byte | 29 writers |

## 4. Data structures and formulas

There is no formula here; the object of study is a classification rule. Stated exactly as it was
tested:

```
owned(f)      :=  f holds independent subsystem state or lifecycle authority
ownerless(f)  :=  not owned(f)                        [router | read-side helper |
                                                       caller-owned materializer |
                                                       shared infrastructure | serializer]

test applied  :=  writes_module_state(f)
                    = exists a RIP-relative store in f's real body whose target
                      lies outside .text

objects(f)    :=  count of maximal runs over sorted write targets, joining any two
                  targets whose gap is <= 8 bytes
```

The `<= 8` coalescing threshold is the one free parameter and it matters: without it, `00433830`
reports **84 objects** (it writes 84 consecutive bytes of one buffer) instead of the correct **1 run
of 52 bytes plus 11 others**. See §10 — that error was made and caught.

## 5. Call chain

There is no single chain; that is the finding. What can be said in both directions:

**Upstream.** The ownerless functions are called from everywhere, but the call graph does **not**
independently corroborate "shared across subsystems": only **1 of the 585** has callers in three or
more distinct owner categories. Most callers are themselves unowned or `CodeDomain`-classified, so
the caller graph is too sparse to carry the claim. **The ownership decision rests on what each
function does, not on who calls it** — which is also what the evidence standard requires, since
caller ownership may never be inherited by a callee.

The tagged-caller edges that do exist are consistent with ownerlessness rather than against it:
**Input** calls `00225570`/`00225680` (through `001E0E30`/`001E0C30`, 11 edges — and `0046E990`
calls Input-side `0035B550`/`0035B2xx` back); **Party** calls `00263E30` from `003273D0` (interior read 2026-09-17, SWE2-FRONTIER: 1,075 B — `00236850` first at [`0032751C`](../../_index/ADDRESS-INDEX.md), `00269C70`/`00236850`/`00236820` ×2 — `PartyConfiguration_SetSelectorsAndReconcileRoster` per the verb page)/
`003261D0`/`003272A0`/`0031B7xx` (10 edges); **Gameplay** calls `00263E30`/`00265020` from
`00321380`/`003176E0`/`0031ADB0` (5); **platform** code (`006239C0`/`0061F200`/`0061F710`/
`006209xx`) calls `00225690` (4); **economy** `002FB150`/`00312280` calls `00265020` (2). Five
layers consuming the helpers this page catalogues is what shared usage looks like, not an ownership
leak — and where a helper does carry a tag (`00225570`/`00225680` are `PrimaryOwner:Audio`, §10's
seven-row defect), the tag, not the caller, decides.

**Downstream.** Into the shared scratch objects of §2.5, and back to the caller through registers and
caller-provided buffers.

**Do not confuse with:**

- [`../Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../Shared-State-Accessors/cross-subsystem-accessor-hubs.md)
  — three tiny functions with 168 callers across 14 subsystems. Those are *hubs*: heavily called
  seams. These 585 are *helpers*: they may be called once. The two sets answer different questions.
- The 30 unresolved residual functions *(158 when written; R109 classified 128)*. Those are **not yet classified**; these are classified as
  *having no owner*, which is a positive finding.
- `CodeDomain` classification. A `CodeDomain` tag says what mechanism a function implements; the
  ownerless decision says no subsystem holds its state. **The three layers are disjoint by
  construction** — 9,409 + 585 + 28,009 = 38,003 — and none of the 585 carries a `CodeDomain` tag.

## 6. Modding notes

- **These are the safest functions in the game to *read* and the most dangerous to *change*.** A
  helper with no owner is used by code you did not think about. `00433830` alone is reached from
  tessellation, mesh building and colour packing paths.
- **The shared scratch is not yours.** If you hook a helper that writes `022D9198`–`022D9428`, you are
  writing a buffer 215 other functions also write, with no lock and no ownership. Leave it as you
  found it, or corrupt whatever runs next.
- **Do not treat `022D8F00`–`022D9500` as one region.** It is 13 objects; one of them (`022D9138`) is
  an RNG control word, and writing it changes determinism.
- **Best intervention point:** the caller, not the helper. Every one of these was classified ownerless
  precisely because the transaction belongs to whoever called it.
- ~~**Three labels in the table are wrong** (§7) — `003B8670`, `00521BB0`, `005004C0` are not routers.~~
  **TWO are wrong (corrected 2026-09-22, FABLE):** `003B8670` and `00521BB0` hold state and are not
  routers; **`005004C0` IS one** — no `call` in its 497 bytes and forty tail-jump targets — so its
  label is right and only its size is an outlier. §7.
  The *ownerless* decision on all three still holds; only the sub-label is wrong.
- **XIIOnline:** an ownerless helper has no authoritative state to replicate. Anything worth
  synchronising is in the caller. Replicating scratch would be replicating a workbench.

## 7. What is not known

- [x] **~~Three~~ `ROUTER_ADAPTER_OR_THUNK` labels are wrong.** `003B8670` (4,578 B, 63 distinct callees,
      15 written objects scattered over 11 pages) is a coordinator, not a router; `00521BB0`
      (1,757 B, 1 callee, 14 objects all in shared scratch) is a materializer; `005004C0` (497 B,
      39 callees) is a switchboard. Their **ownerless status is not in doubt** — all three fail the
      state-authority test at the subsystem level — but the class field should be
      `CROSS_CATEGORY_CONSUMER_OR_BOUNDARY` for the first, `CALLER_OWNED_OR_TRANSIENT_MATERIALIZATION`
      for the second. **BQ-11.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5), restating this page's own 2026-09-22 correction (section 7's reading
      below):** **two** labels are wrong, not three. The fixes stand: `003B8670` should be
      `CROSS_CATEGORY_CONSUMER_OR_BOUNDARY` and `00521BB0` `CALLER_OWNED_OR_TRANSIENT_MATERIALIZATION`.
      `005004C0`'s label is correct: 497 B, no `call`, forty `jmp` targets, a dispatcher by construction. The
      error rate is 2 of 585, 0.34 %. Rewriting the two sealed decision blocks in the GZF is a ledger edit, not
      a question, and it is not queued.
- [x] ~~What `003B8670` actually is. Its own summary calls it a *"higher-level authored-event / game /
      UI / Actor / bootstrap interpreter"* — 930 instructions, 97 calls to 63 functions, 2 indirect
      calls, and 15 private objects including `0209218C+20` and `020925A0+12` that nothing else in
      the image writes. A function of that shape with exclusive state is a system, and it has no
      document.~~ **BQ-12 ANSWERED 2026-09-12 (FABLE): it is the battle action's authored
      timeline interpreter** — see §12 below and [`action-timeline-opcodes.tsv`](action-timeline-opcodes.tsv).
- [x] ~~What the 660-byte object at `022D9198` and the 130-byte object at `022D8F90` are.~~
      **ANSWERED 2026-09-02** — they are not objects. The page is an **argument-passing area** of
      16-byte rows with one proven 4×4 matrix at `022D91B0`, and it has no owner because nothing
      persists in it: 215 of 216 row-touchers write before reading.
      [Full document](../Shared-Transform-Workbench/the-shared-transform-workbench.md). **BQ-13.**
- [x] ~~Whether the eight `Gi*` backend factories each caching a constructed object in one
      exclusive global should count as lifecycle authority.~~ **RULED 2026-09-15 (OPUS): THEY DO
      NOT. `FinalNoPrimaryOwner` is correct, and the fitting ownerless class is
      *caller-owned materializer*. BQ-34.**
      - **Every one of the eight cache globals is WRITE-ONLY.** Whole-image census, positive control
        `022D8EB4` returning 26 references so absence is meaningful, over 34,270 function bodies:
        `02EAF900`, `02EAF910`, `02EAF920`, `02EB37F8`, `02EB3828`, `02EB3838`, `02EB3848` and
        `02EB3858` carry **one reference each** — two for `02EB3828`, both stores by the same
        function — and **every reference is the factory's own store**. Nothing reads them.
        Nothing frees them. **No instruction takes the address of any of them**, so no pointer to
        one can be formed and reached another way.
      - **So the rule's first limb fails: this is not independent subsystem state.** State that no
        subsystem ever reads is not subsystem state. Three of the eight objects are **8 bytes** —
        `00862E50`, `008652B0`, `00865320` — which `00862E50` shows is a vtable pointer and
        nothing else (`lea rcx, [01CCFA00]` / `mov [rax], rcx`). The others are `0x10`, `0x18`,
        `0x70` and `0x90`.
      - **And the second limb fails: there is no lifecycle to have authority over.** The factory
        allocates, installs a vtable, stores, and returns. **There is no release, no destructor, no
        refcount, and no re-check** — the factory does not even read its own slot to avoid
        allocating twice. A creation with no subsequent event is not a lifetime.
      - **Correction to this box's own wording:** *“caching”* overstates it. A cache is read;
        these are written and never read. The global is incidental — the constructed object leaves
        in `rax`, which is the materializer shape the rule already names.
      - *Mechanically re-checkable by anyone: the claim is one census over eight addresses with a
        stated control. If any of the eight is read anywhere, this ruling is wrong and should be
        reopened against OPUS.* *(Renumbered 2026-09-14,
      FABLE: this box carried `BQ-14`, which the register uses for a different, superseded question about the objects in
      `022D8F00`–`022D9500`; `OPUS-REQ-FABLE-QUESTION-REGISTER-THREE`.)*
- [x] The other categories' ownerless functions. This population is 583/585 Presentation. Whether
      every other category's shared helpers were held to the same rule is untested. **BQ-15.**
      *NOT A QUESTION 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-2 ruling: the work is carried by the board task `FABLE-CARRIER-TOOLING-AND-CHECKER-PROPOSALS-0926`.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 585 functions carry a final no-owner decision, disjoint from owner and CodeDomain tags | the sealed snapshot's own accounting: 9,409 + 585 + 28,009 = 38,003 explicit, overlap 0 | 1 |
| The policy's own wording, and the six CLASS values | the `RESIDUAL_CLOSURE_BL` comment block on all 585 | 3 |
| 583 of 585 have Presentation prior evidence | `GFZ_V120_X0_PRESENTATION_*` block headers counted across the population | 3 |
| The 585 write module state at 10.1 %, against 21.5 % for owned functions | whole-image disassembly of all 38,161 real bodies, RIP-relative stores outside `.text` | 1 |
| The six classes have distinct, name-consistent profiles; `READ_QUERY_*` is 0/107 | same census, grouped by the CLASS field | 1 |
| `022D9198`–`022D9428` is 660 B written by 215 functions across 4 owner categories | coalesced write-target runs over every function that writes the page | 1 |
| `022D9138` inside the same page is RNG state with 2 writers | writer set for that address; corroborated by [`rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md) | 1 + 9 |
| `003B8670` is not a router | complete body: 930 instructions, 97 direct calls to 63 distinct functions, 2 indirect, 15 written objects, 8 of them exclusive | 1 |
| Only 1 of the 585 has callers in 3+ owner categories | reverse call graph over the whole image | 11 |

**On the caller-graph row:** it is tier 11 and is used here **only to refuse a claim**, never to
support one. It is why §5 says the decision rests on behaviour rather than on cross-subsystem use.

**Superseded readings:** this document's own first measurement counted write *addresses* rather than
write *objects* and reported that one function writes 84 globals. It writes 84 consecutive bytes of
one buffer. Corrected before publication; recorded in §10 because the corrected number changes the
argument, not just the figure.

## 9. Related

- [`../Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../Shared-State-Accessors/cross-subsystem-accessor-hubs.md) — the *hub* half of the same seam story
- [`../../21-RNG-And-Determinism/rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md) — owns `022D9138`, inside the page this document maps
- [`../../24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](../../24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md) — B-2, the other population audit, and the method this one follows
- [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) — the layer separation this document audits

## 10. Falsification pass 2026-09-02 — including the measurement that was wrong

**Attack chosen.** B-4 asks whether 585 classifications are earned or inherited. The failure mode is
specific and has bitten this database repeatedly: a tag population mistaken for a census. So the
population was **re-derived from the image** — every one of the 38,161 real function bodies
disassembled and measured for the property the policy names — rather than re-selected from the tag,
and every figure was computed against three control groups, because a rate with no control is not
evidence.

### KILLED, before publication: "one function writes 84 globals"

The first census reported that `00433830`, labelled *shared generic infrastructure*, writes **84
distinct globals** — which would have made it the clearest counterexample in the set, a supposed
helper with more module state than most owned functions. The addresses:

```
022D8F90 022D8F91 022D8F92 022D8F93 022D8F94 022D8F95 022D8F96 022D8F97 ...
```

**Eighty-four consecutive bytes.** One buffer, written byte-wise. The metric counted addresses; the
question needed objects. Recomputed with adjacent targets coalesced, the same function writes **12
objects**, the largest a 52-byte run — and the population maximum drops from 84 to **15**.

It was caught by printing the addresses instead of trusting the count, after an unrelated check
(`022D9138`, already documented as RNG state, sitting inside the supposed "scratchpad") forced a look
at the region's internals. **The fifth measurement defect found in this run, and the fifth to produce
a plausible number rather than an obvious failure.**

It also killed a second claim that had already been drafted: that `022D8F00`–`022D9500` is *one*
1,436-byte shared scratchpad. It is **thirteen objects**, one of which is RNG control state. The
corrected reading is narrower and true.

### SURVIVED: the classification is earned

Three independent results, any one of which could have failed:

1. **10.1 % against 21.5 %.** The ownerless population writes module state at less than half the rate
   of the owned population, with `CodeDomain`-only at 17.1 % and the unresolved residual at 24.7 %.
   A bulk sweep has no mechanism for producing that separation.
2. **107 of 107.** Every function labelled `READ_QUERY_RESOLUTION_SUPPORT` writes zero module state.
   Not most — all. A label applied without reading the code cannot achieve that on a sample of 107.
3. **Six classes, six profiles, correctly ordered.** `CALLER_OWNED_OR_TRANSIENT_MATERIALIZATION` has
   **zero** median callees, the largest median body (279 B) and a 56 % write rate;
   `ROUTER_ADAPTER_OR_THUNK` has two callees, a 56-byte median body and 2.8 %. Those are opposite
   profiles under labels that promise opposite behaviour.

### SURVIVED: the apparent counterexamples are confirmations

The ownerless functions that write the most module state write it into buffers that **215 and 76
other functions** also write, spanning Presentation, Audio, Movement and ActorEntity. A function
borrowing a workbench four subsystems share is the definition of the thing the policy calls
ownerless. The counterexample list, read closely, is the proof.

### FOUND: three labels that are wrong, and the ownership decision that is not

`003B8670`, `00521BB0` and `005004C0` are labelled `ROUTER_ADAPTER_OR_THUNK` against a class median of
56 bytes and 2 callees. They are 4,578 B / 63 callees, 1,757 B / 14 written objects, and 497 B /
39 callees. ~~**None is a router.**~~ **TWO are not routers — corrected 2026-09-22 (FABLE), and this
document already said so in the other place.** §3's key-address table calls `005004C0` *“39 callees
— a router, but a large one”*, which contradicts the sentence here; **the bytes side with §3.**

> **`005004C0` is a dispatcher, and its own body is unambiguous about it.** In 497 bytes it
> contains **no `call` instruction of any kind** and **forty distinct `jmp` targets**, with its
> indices bounded twice (`005004E3 cmp rcx, 0x200`, `00500510 cmp eax, 0xd1`). *A body that only
> ever tail-jumps and never calls is a dispatcher by construction* — the graph's “39 callees” are
> those tail jumps, not calls. **So its `ROUTER_ADAPTER_OR_THUNK` label is correct**; what is
> unusual is its size, not its kind, and `effect-subtype switchboard` is the right working name.

> **The method is what went wrong here, not the arithmetic.** All three were judged against the
> class median by **callee count and byte size** — both measures of *how big*, neither a measure of
> *what kind*. `003B8670` (15 written objects, 8 exclusive) and `00521BB0` (14 objects, all
> scratch) fail on kind as well: they hold state. `005004C0` writes nothing it owns and merely
> routes. **An outlier on size is not a mislabel.**

All three nonetheless fail the state-authority test at subsystem level, so their *ownerless* status
stands and only **two** sub-labels are wrong (**BQ-11**). **Two** mislabels in 585 is a **0.34 %**
error rate in a field that no tool checks.

### Disposition of BL-1 — the retraction question, bounded

BL-1 warns that GFZ ownership retractions live only in comment prose, so any tag-based census
over-counts. Swept across all 38,161 comments:

| marker | functions | in the 585 | still carrying a `PrimaryOwner` |
|---|---:|---:|---:|
| `SUPERSEDES` | **7** | 0 | **7** |
| `RECLASSIFY` | **7** | 0 | **7** |
| `REJECT` | 3,461 | 27 | 499 |

**`SUPERSEDES` and `RECLASSIFY` mark the same seven functions** — `00182E80`, `001DC3D0`, `00225570`,
`00225580`, `00225680`, `00225690`, `002256A0` — all `PrimaryOwner:Audio`, all still tagged. BL-1's defect is real and is **exactly seven rows**, not a systemic over-count.

**`REJECT` is not a retraction marker.** It appears as
`SOURCE_REJECTION_REASON=REJECT_<CATEGORY>_...`, which declines ownership *for* that category — a
boundary, not a withdrawal. The machine test: **zero** owned functions carry a `REJECT` naming their
own owner category. The tags and the prose do not contradict each other anywhere except those seven.

### What was tried and did not break anything

- **Looked for the 585 inside category 24**, where this question was routed. **Zero of the 585 carry a
  `CompilerGenerated`/`Microsoft`/`Thunk` CodeDomain tag** — they cannot be, since the layers are
  disjoint. The routing assumption was wrong and the document is filed here instead.
- **Tried to corroborate "shared" from the call graph.** It does not: only 1 of the 585 has callers in
  three or more owner categories. Recorded as a limit rather than quietly dropped.
- **Checked the region against documents that already cite it.** `rng-streams.md` claims `022D9138`;
  the writer set agrees (2 writers) and the address falls in a 44-byte run distinct from the two big
  scratch buffers. **No contradiction** — but it is the observation that broke the one-scratchpad
  reading.
- **A pointer-write detector** (writes through a register loaded from a global) returned **zero hits
  across all 38,161 functions**, which is impossible. It is a broken measure, so it is reported
  nowhere in this document rather than reported as a zero.

### Status

`DOCUMENTED`, one falsification pass. **B-4 answered: earned, not inherited**, with three named
exceptions in the sub-labels and none in the ownership decision itself. What would kill it: a member
of `READ_QUERY_RESOLUTION_SUPPORT` shown to write module state; a demonstration that
`022D9198`–`022D9428` is read back across a subsystem boundary as durable state rather than scratch;
or an eighth retraction marker outside the `SUPERSEDES`/`RECLASSIFY` pair.

## 12. What `003B8670` is — the action timeline interpreter (BQ-12, 2026-09-12, FABLE)

`003B8670(record /*rcx*/, prevTime /*edx*/, nowTime /*r8d*/, nowTimeF /*xmm3*/)` walks an
**authored timeline record** and fires every entry whose time key has just been crossed. The record
is a resource sub-object: byte `+1` is its kind and only kind **2** reaches this function (both entry
points test it: `004FF2C0` at `004FF2D0`, `0046EFD0` at `0046F098`); byte `+0x10` is the entry count
(zero → return 1 at once); entries are **16 bytes from `+0x14`** — byte `+0` the opcode `1 … 128`,
word `+2` the time key, the rest opcode-specific. The gate (`003B875D`–`003B8771`) fires an entry
when `key ≤ nowTime` and, if `nowTime ≠ 0`, `key > prevTime` — i.e. once, on the frame the
playhead passes it — and the opcode indexes a 128-entry byte table at `003B994C` into a 62-case
jump table at `003B9854` (`003B8777`–`003B879B`); the full opcode → case → callee table is the
side file. The two drivers are the same instance walker: `0046EFD0` (from the sub-resource
instantiation `00333280` / `003331A0`) resolves the record through
`ImageAddress_ResolveRuntimePointer` from the ten-entry table of a render object's resource
(`0046F083`–`0046F088`, the mount page's "sub-resource" mechanism) and passes the instance's words
`+8` / `+0xA` and float `+0xC` as the playhead; `004FF2C0` (from `0046E990` and `0046EFD0`) does the
same for kind 2 and routes kinds `≤ 1` and `3` elsewhere (`00538820`, `005372D0`).

**The private state is the current action context.** The singleton `[02F97348]` — 57 references
in this body — is read as: `+8` the acting unit, `+0x10[i]` and `+0x90[i]` two per-target handle
arrays, `+0x372` the target count, `+0x374` the hits delivered (incremented per hit opcode), `+0xC`
a per-target hit mask, `+0x368` / `+0x36A` / `+0x378` flag words. Opcode **3** is the hit: it takes
target `i` from `[02EBA4F0] + 0x10` (or 0), refuses past the count or when `+0x378` bit 9 is set,
sets `+0x36A` bit 5, calls `ActorTimeline_DispatchEventToBattleUnit(context + 8, target, &out)` and
then `0024ED80` / `00322850`, and marks the target's bit in `+0xC` (`003B87E7`–`003B88E6`); opcodes
~~13, 26 and 34~~ **13, 26, 34 and 37** *(corrected 2026-09-29, FABLE: opcode 37 was missing)* dispatch other timeline events the
same way. The event kinds are:
- 3, the hit: kind 0;
- 13: kind 1;
- 26: kind 3, 6, 7 or 8, for entry dword `+4` = 0, 1, 2 or 3;
- 34: kind 2;
- 37: kind 4.

Opcodes 13, 26, 34 and 37 pass the acting unit and no target. Kind 6, and kind 4 behind further gates, set the acting unit's flag bit
34. That is the bit that releases a dead body (`_index/candidates/pkg-gp-spawn-respawn/teardown.py` T). Opcodes **28** / **29** place and turn an
actor (`ActorHandle_ResolveRegistryEntryByPackedId`, `Actor_GetWorldPosition`, `0026AF80`,
`Actor_SetFacingHeading_Variant0`); **10** / **11** run the render reset family the frame page
documents (`003ACA90`, `003AFD30`, `003B6930` — the shadow pools of BT-1); **52** / **53**
touch the shadow objects (`003B5310`, `003AF330`); **31** posts audio (`Audio_PostSequenced`);
**14–19** call the `002FCA00` battle family; **21**, **22**, **32**, **40** resolve a render record
(`003A3FD0`, `003326C0`) and drive it; 66 opcodes (4, 23, 64–127) are no-ops in this build;
~~128 and a dozen others are inline without a call~~ *(Corrected 2026-09-30, SWE2-DATA, on SWE2-ORACLE's [GR-17 residue record](../../_index/candidates/gr17-effect-residue-0930/README.md), [consumer check](../../_index/candidates/data-gr7-gr17-fieldmap-0930/README.md): opcode 128 calls `002EB740` - it builds a target from `+0x90` / `+0x10` and joins the call at `003B8A13`, past opcode 26's `xor edx, edx`, as event kind 5 with that target, authored alongside the hit (347 times each across the corpus); a dozen others are inline without a call)*. So: **a 128-opcode, time-keyed interpreter over
authored per-action tracks — hits, placement, shadows, effects, audio — with the singleton as its
context.** What each opcode's operands mean, and the authoring-side name of the track, are the
residue; the identity is settled.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `00188B10` | 643 | per-entry loop over `[rsi+0xB08..0xB30]` fields: `00258130`/`00259360`/`0025A890` accessors, `00610330`, repeating `00182E80` x11/`00182EB0` x11/`001EEE80` x10 |

## The `003B8670` exclusive subtree — the interpreter's 33 opcode helpers (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 33 frontier functions to `003B8670` — the machinery under
the opcode arms §12 names. All signature-swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| action-context arms | `0024B6F0` (`020921A0`–`020921BC` cells — `A0`/`A4`/`A8`/`AC`/`B4`/`BC` + `003A6D90`/`003588B0`/`00265020`/`00265200`/`00263F70`/`00263E70`/`003B7E10`), `0024C3C0` (`020910A0`/`02092170`), `0024F9B0` (`020925A0`–`B4` cells + `0026A430`/`0026AF80`), `00333520`, `00333640`, `003A4070` (`02096A20` + `003B0BF0`), `003A7F60` (`02EBEF98` + `003697F0`), `003B8260` (1,028 B — `0020E600` ×7 + resolve `003E1350`/`003E1610` + `003B3CA0` ×2, `00D115BC`–`E0` table + `02EBA4F0`; interior verified 2026-09-17, SWE2-FRONTIER — `0031E880` first at [`003B82D7`](../../_index/ADDRESS-INDEX.md)), `003B99D0` (1,501 B — 24 helpers, `020926F4` + `02EBA4F0`; interior 2026-09-17, SWE2-FRONTIER —
`02EBA4F0` loaded ×5 beginning [`003B9A2A`](../../_index/ADDRESS-INDEX.md), helper set
`0046C8D0`/`003616F0`/`00181DD0` ×2 each — the opcode-5/39 arm), `003B9FE0` (`0024B240`), `003BA020` (`00182B40`/`00375900`/`0017F2A0`/`001E0580`, `020926D0`), `003BA1F0` (`01DFE0B4`/`020926F6`/`02EBA4F0`/`02EC0F88`/`02F97340`) | bodies that read `02F97348` (the §12 action context) or `02EBA4F0` (the target array) — the heavyweight opcode arms |
| `02EBEF88` family + wrappers | `003A8C80`, `003A8CB0`, `003A8CE0`, `003A8D40` (33–89 B each on `02EBEF88`), `003A8DD0` (423 B — `001EDDA0`/`003A8AE0`/`002F31C0`), `003A8290` (`004FF080`/`004FF0D0`, `02EBEF98`); wrappers `003326F0`/`00333430`/`003335A0`/`00333A40` (each `0046EE70` + `003697F0` + one `003A8Cxx`) | a shared sub-object at `02EBEF88` with four field ops plus one larger step — `0046EE70`/`003697F0` bracket it |
| hit/target helpers | `00322850` (the §12 post-hit call — `003588B0` ×2 + `00263E30` ×2), `0042F2A0` (`0020E600` + `004219C0`/`00426E40`, `022C6F28`), `00423190`/`004231E0` (72 B twins: `0020E600` + `0051B9E0`), `003BA150` (`002EE050` ×2 + `003A6BA0`, `01EFE318`/`022C6F28`), `0046CC20` (`002E9D90`), `003D7C50` (`02EBBA00`) | resolve-and-apply steps behind the hit/placement opcodes |
| leaves | `0017F2A0` (`00189120`/`0018CA40`/`0018B8B0` — a command-list emit), `003333B0`, `00333620`, `00379940` | small bodies the arms call |

This confirms §12's shape from the callee side: the singleton context `02F97348` and the target
array `02EBA4F0` dominate the subtree exactly as the opcode analysis describes. The `02EBEF88`
sub-family is new — a distinct sub-object the interpreter's own helpers share.

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This document named these bodies only at their entries. Each interior address was read in the
shipping image; the notes say what the instruction does, not yet the body's full role.

| body | interior cite | what is there |
|---|---|---|
| `00433830` | `00433886` | `movss dword ptr [rip+…], …` — writes `022D9304`, tail of a `022D8F90`-based scratch block of ~0x380 bytes |
| `00521BB0` | `00521C46` | `movss dword ptr [rip+…], xmm1` — writes `022D9380` after `movups` fills of `022D9230`–`022D9330`; four `0036DD80` calls follow |
| `0046E990` | `0046EAB2` | `call memcpy` inside a body that opens with `00250000`/`001EDDA0` and writes `02EBA4F0`, `02EC0F88`, `02F97348` |

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Combat — CLIENT.** `FUN_003206e0`, owned by that layer, calls `00263E30` on this page. That caller is a 176-byte routine behind the same `byte[02089340] & 0x10` gate, resolving through `003588B0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `003272A0` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAction — CLIENT.** `Battle_ProcessActionTargetEntry`, owned by that layer, calls `00263E30` on this page. That caller is the per-target entry step, seeded with the float constant at `01CEBCAC` and working in a `0x40`-byte frame with one preserved SSE register; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_ResolveByActorHandle`, owned by that layer, calls `00263E30` on this page. That caller is a 55-byte resolver behind the same `byte[02089340] & 0x10` gate as the focus-handle pair: it takes the handle through `003588B0` and `00263E30` and returns the resulting unit's `+0x698` **stats record** rather than the unit itself; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Save_Load_Settings — CLIENT.** `FUN_005817d0`, owned by that layer, calls `00225580` on this page. That caller is the two-argument form of the same reset over `[02CA99C8]`: `qword[+0xD4]` becomes `0xFFFF` and `+0xDC` is cleared before the two values are applied; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT.** `0042ED60` on the presentation layer calls `003697C0`, the scratch-pool descriptor `+0x62` release — the render pipeline reaches this ownerless helper, not shared ownership.
**Audio and Resource — CLIENT (shared-callee edges, SWE2-EC7-189).** The list helpers `0016D6D0`/`0016DA60` my `001B67F0` entry names are generic unlink/free primitives also reached by audio-side callers (`002187D0`/`00219D80`/`0021AF80`) and resource-side callers (`0020B840`/`0020BFA0`/`006761F0`). The crossing is those layers consulting shared helpers this page names, not shared responsibility. Edge list from `edges.tsv`.

**ActorEntity, Script VM bridge and WorldAreaField — CLIENT (shared-callee edges, SWE2-EC7 batch-161).** The drain-then-notify helper `003EA3E0` this page now names reaches loader plumbing (`002DEE90`/`002DF690`/`0035EA30`) whose callers span the actor-entity layer (`0031B770`/`00321170` and siblings), the script-vm native bridge (`0034AF50`/`0033F7F0`/`00342490` calling `00263C30`/`00263FF0`) and the field/world-area layer (`003775D0`, `00377C20`). Those layers consult shared request plumbing named here; no actor, bridge or field state is owned by this page. Edge list from `edges.tsv`.
- **Items_Equipment_Shops_License — MECHANICAL (1 edge).** 1 Items_Equipment_Shops_License-side calls into shared helper(s) the page cites (`BattleUnit_GetBySlotIndex` (00236820)) - the helpers' general call surface, not a Items_Equipment_Shops_License relationship of this page's subjects.
- **Movement — CLIENT and SERVICE (116 edges).** 100 inbound (Movement bodies `0024B6F0`, `PartyFollow_SolveFormation` (00338490), `00326D60` call page-cited `Actor_GetWorldPosition` (00265020), `PartyFocus_GetCurrentPackedActorHandle` (003590D0), `BattleUnit_GetBySlotIndex` (00236820)); 16 outbound (page-cited `003B8670`, `0026AFE0`, `0024F9B0` call Movement bodies `00265200`, `Actor_SetFacingHeading_Variant0` (0026B5A0), `0026AF80`). Substantive edges include `BattleUnit_GetSlotCount` (00236850) is called by `00337D90`; `BattleUnit_GetSlotCount` (00236850) is called by `00337C10`; `BattleUnit_GetSlotCount` (00236850) is called by `00326D60`; `BattleUnit_GetSlotCount` (00236850) is called by `003278D0`; the remaining edges run through shared helpers the page cites.
- **PlatformOnlineAchievements — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared PlatformOnlineAchievements plumbing (`00316A50`) - the helpers' general call surface, not a PlatformOnlineAchievements relationship of this page's subjects.
- **Spawn_Encounter_Lifecycle — CLIENT (8 edges).** 8 inbound (Spawn_Encounter_Lifecycle bodies `Spawn_TrySelectCandidatePosition` (00234AF0), `Spawn_CountActiveCapTrackedActors` (00308D90), `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0) call page-cited `Actor_GetWorldPosition` (00265020), `BattleUnit_GetPartyLeader` (003272A0), `BattleUnit_GetBySlotIndex` (00236820)). Substantive edges include `BattleUnit_GetSlotCount` (00236850) is called by `Spawn_CountActiveCapTrackedActors` (00308D90); `00265200` is called by `Spawn_TrySelectCandidatePosition` (00234AF0); `BattleUnit_GetPartyLeader` (003272A0) is called by `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0); `BattleUnit_GetPartyLeader` (003272A0) is called by `Spawn_TrySelectCandidatePosition` (00234AF0); the remaining edges run through shared helpers the page cites.
- **Status_Periodic_Terminal — CLIENT (4 edges).** 4 inbound (Status_Periodic_Terminal bodies `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` (00386860), `BattleUnit_RecoverFromTerminalStatusSetIfClear` (00301140), `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0) call page-cited `ActorWork_GetBattleUnitRaw` (00263E30), `002ECF10`, `Loot_FindOverlappingPickupIndex` (002FB150)). Substantive edges include `Loot_FindOverlappingPickupIndex` (002FB150) is called by `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0); the remaining edges run through shared helpers the page cites.
- **UI — CLIENT and SERVICE (23 edges).** 22 inbound (UI bodies `0024B9B0`, `BattleMenu_BuildCommandEntryList` (0031EB20), `00322A80` call page-cited `00225580`, `00254550`, `BattleUnit_GetBySlotIndex` (00236820)); 1 outbound (page-cited `0031E880` call UI bodies `BattleMenu_BuildCommandEntryList` (0031EB20)). Substantive edges include `00181DD0` is called by `0024B9B0`; `001E0E30` is called by `0029B870`; `00225580` is called by `00299090`; `00225580` is called by `002986E0`; the remaining edges run through shared helpers the page cites.
## The `004FF2C0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`004FF2C0` (85 B) is the multi-arm record interpreter this page cites:
`byte[rcx+1]` selects the arm (`1`/`2`/`3` at `004FF2CB`–`004FF2D5`) —
`005372D0` (`004FF2DD`), `00538820` (`004FF306`), and the
`005375B0`/`003B9FB0`/`005388F0` tails (`004FF340`–`004FF34A`) — then a
`0x61`-bound image-base switch `byte[00120000+rax+0x3DF3D8]` → `jmp rdx`
(`004FF380`–`004FF39B`), a second `0x3E0270` table at `004FF463`,
`word[rbx+0x20]` compares (`004FF477`/`004FF4B8`/`004FF4ED`), `002F31C0`
(`004FF3B6`), `0036A190` (`004FF481`).

| member | role | interior |
| --- | --- | --- |
| `005372D0` (316 B) | stat/id resolve battery — `dword[rcx+0x1C]` → `0020E600` (`005372E4`), `xmm0 -= 1.0f` (`00537308`), `byte[rbx+0x12]` vs 4 (`00537319`), `0020E600` chain → `[rax+0x18]` (`0053732B`–`00537333`) | [`00537319`](../../_index/ADDRESS-INDEX.md) |
| `00538820` (203 B) | record-field setter — `word[rcx+0x10]` vs 0 (`00538834`), `[rbx+0x14]` bit 1 (`00538853`), `word[rdx+8]` / `byte[rbx]` (`0053885C`–`00538862`), `02EBEF90` (`00538871`) | [`00538862`](../../_index/ADDRESS-INDEX.md) |
| `0035B580` (74 B) | slot-state transition writer — `cl` indexes `[02EC0B80]` (`0035B584`), `word[r8+2]` vs `ecx` (`0035B59D`), `byte[r8+1]` vs 1 (`0035B5A4`), `02EC0B40` bit test (`0035B5AB`), writes `byte[r8+1] = 4`, `byte[r8+0x1C] = dl` (`0035B5BB`–`0035B5C2`) | [`0035B5AB`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `005375B0`, `003B9FB0`, `005388F0`,
`002F31C0`, `0036A190`, `0020E600`, `003B8670`.

## Interior citation — frontier hub `003697F0` (2026-09-17, SWE2-EC7)

`003697F0` — 13 B, 140 frontier callers at census. Interior verified:
[`003697F5`](../../_index/ADDRESS-INDEX.md) is `xor edx, edx` — the body is `test rcx, rcx; je ret;
xor edx, edx; jmp 00369860`: a **null-safe release entry** — NULL is a no-op, otherwise forward
to `00369860` with `arg2 = 0`. `00369860` (1,009 B) is the validating deallocator: it rejects a
pointer whose `−0x40` header does not carry magic `0xFF12` or whose low bits are set
(`test r14b, 3`), formats a diagnostic dump of the `0xB0`+`0xD0` byte neighbourhood through
`0017D2E0`, reports through `0036A570`, and aborts; the good path unlinks through the
`0036Axxx`/`0036Bxxx` heap family. This is why `the-widget-message-protocol` reads call sites as
"release the storage → `003697F0` (heap)": the hub is the heap-free guard.

NOT claimed: which heap `00369860` serves (CRT vs arena) or the `arg2` flag's meaning — callers
always pass 0 through this wrapper.

## Interior citation — frontier hub `002F31C0` (2026-09-17, SWE2-EC7)

`002F31C0` — 233 B, 42 frontier callers at census; this page already records it among the
ownerless pool. Interior verified: [`002F31F9`](../../_index/ADDRESS-INDEX.md) is `jmp r8` — the
body dispatches on `byte[rcx] - 0x40` through a 0x92-wide two-level table stored inline at
`002F32AC`/`002F32C8` (six named case targets `00464050`/`00464B80`/`00461250`/`00465120`/
`003D90C0`/`00460120`, default `0043E9C0`), then **unlinks `rbx` from its intrusive list**
(`[rbx+0x28]`/`+0x30` prev/next fixup into `rdi`'s `+0x118`/`+0x128` list heads) and pushes it onto
the `rdi+0x120` list. A type-tagged retire-and-requeue.

NOT claimed: the six handlers' identities (they are the per-type teardown paths, not read here)
or which list pair `rdi` heads.

## Interior citation — frontier hub `003A3FD0` (2026-09-18, SWE2-EC7)

`003A3FD0` — 149 B, 7 A-measured callers; the routed dword getter. Interior verified: reads
the `02F97348`-band state object — when `word[+0x378] & 0x200` the value comes from
`02096A20` via `002E9B80` ([`003A4005`](../../_index/ADDRESS-INDEX.md) region); otherwise `byte[rcx]` selects:
kind 3 returns `[+8]` directly, kinds 5/6/7/8/9 (the `al & 0xFA` mask at `003A3FF6`) resolve
`003B0BF0([+4])` and take `[result+0x11]==1 ? [gbl+8] : table[rbx*4+0x90]`, anything else
`table[ecx*4+0x90]` or `[+8]` when the entry is 0 — every miss path funnels to
`002E9B80`-shaped `-1` at `003A405C`.


### Interior citation — frontier hubs `00182EB0`, `00182E80` (2026-09-18, SWE2-EC7)

The two ownerless 41-byte singleton getters share one shape: `001DDAB0()` twice —
once to test for null, once for the pointer — then tail-forward the object to a
handler, with a constant fallback when the singleton does not exist yet.
`00182EB0` tails `00225680` ([`00182ECA`](../../_index/ADDRESS-INDEX.md)) and
falls back to `0x780`; `00182E80` tails `002256A0`
([`00182E9A`](../../_index/ADDRESS-INDEX.md)) and falls back to `0x438`. The two
fallbacks are the IDs the absent-singleton path substitutes — this is the
reclassify pair the table above rows against.

### Interior citation — frontier hub `0024ED80` (2026-09-18, SWE2-EC7)

`0024ED80` — 132 B, 13 callers: the global-bank publisher paired with
`0024EE60`'s unlink. It copies `[rcx+0x340]`'s sub-record cells —
`[+0x18]`/`[+0x38]`/`[+0x840]`/`[+0x848]`/`[+0x850]` — plus `[rcx+0x120]`/
`[+0x130]`/`[+0x1B8]` into the `02F3E9xx`/`02F484xx` global bank
([`0024ED95`](../../_index/ADDRESS-INDEX.md)), then tails `0024FCF0`. The owner
hand-off the opcode flow names.

### Interior citation — frontier hub `003326C0` (2026-09-18, SWE2-EC7)

`003326C0` — 40 B, 11 callers: the fifth `+0x284`-gated render-record resolve.
`word cx == -1` returns NULL; otherwise `imul rax, rax, 0x740` at
[`003326CF`](../../_index/ADDRESS-INDEX.md) strides into the `022C6F28` array
and `cmove` returns the record only while its `[+0x284]` dword is zero —
sibling of `002E73C0`/`002ECEC0`/`002ECF10`, this arm returning the pointer
itself rather than tailing a consumer.
## SWE2-EC7-18 update (2026-05-15) — `003ACA90` shadow-pool field read fragment

`003ACA90` (9 B) is one of the BT-1 shadow-pool bodies this page counts: its whole body is `not cl` + `and byte[02B3F501], cl` + `ret` (`003ACA90`..`003ACA98`) — a global flag-byte bit-clear on the caller's mask — confirming the ownerless classification: a two-instruction shared leaf with no owning subsystem.

## SWE2-EC7-30 update (2026-09-18) — `0026AF80` config-gated `002E4A10` dispatch

`0026AF80` (85 B) is the movement helper the `0024F9B0` action-context
arm calls: `0026AFE0(obj)` runs first, then `byte[obj+0x15]` picks a
row of the `02098E10` config table (0x288-stride, rows < 3 only) and
the row's `+0x10` flag byte decides — the `002E4A10` tail dispatch
runs unless the row exists, its bit 0 is set, and its bit 7 is
clear; everything else (kind >= 3, flag bit 0 clear, or flag bit 7
set) forwards. Interior anchor `0026AFC9` (the `jmp 002E4A10` tail).

## SWE2-EC7-34 update (2026-09-19) - `00465120`

`00465120` (963 B) is a gated kind processor - `test word[rcx+0x232]&0x712`, `byte[rcx+0x230]<=9` switch, `00263FF0`/`00263C30`/`00465510`/`003A6BA0`/`002E9B80`. Interior anchor `00465183` (an `00263FF0` call).

## SWE2-EC7-36 update (2026-09-19) - `00188B10`

`00188B10` (643 B) is a shared-scratch loop - `00182EB0`/`00182E80`/`001EEE80` decuples plus `00610330`/`0060F6B0`. Interior anchor `00188B27` (an `00182EB0` call).

## SWE2-EC7-36 update (2026-09-19) - `003E1350`

`003E1350` (629 B) is an image-pointer sweep - 32 `0020E600` resolves then `00472810`. Interior anchor `003E1378` (an `0020E600` call).

## SWE2-EC7-36 update (2026-09-19) - `003E1610`

`003E1610` (629 B) is the sibling sweep - 32 `0020E600` resolves then `00472950`. Interior anchor `003E1638` (an `0020E600` call).

## SWE2-EC7-39 update (2026-09-19) - `003A8DD0`

`003A8DD0` (423 B) is the `02EBEF88` family's larger step the page names - `001EDDA0`/`003A8AE0`/`002F31C0`. Interior anchor `003A8E9E` (an `001EDDA0` call).

## SWE2-EC7-42 update (2026-09-19) - `004219C0`

`004219C0` (305 B) is an ownerless body - `0020E600` triple/`002ED570` pair/`00372800` pair/`0046E640`/`003E5D30`. Interior anchor `004219E7` (a `0020E600` call).

## SWE2-EC7-42 update (2026-09-19) - `003BA020`

`003BA020` (298 B) is an ownerless body - `01CEBB70`/`01F44830`/`020926D0`/`02F97348`, `00182B40`/`00375900`/`0017F2A0`/`001E0580`/`00808C40` pair. Interior anchor `003BA0A9` (an `00182B40` call).

## SWE2-EC7-45 update (2026-09-19) - `003BA1F0`

`003BA1F0` (238 B) is a body - `001EDDA0`/`0024ED80`/`00250000`/`003B02A0`. Interior anchor `003BA218` (an `001EDDA0` call).

## SWE2-EC7-47 update (2026-09-19) - `003331A0`

`003331A0` (217 B) is the record-resolving instantiation - `003697F0`/`0036A190`/`0046EE30`/`0046EE70`/`0046EFD0`. Interior anchor `003331F8` (a `003697F0` call).

## SWE2-EC7-48 update (2026-09-19) - `00333280`

`00333280` (201 B) is the record-resolving instantiation sibling - `003697F0`/`0036A190`/`0046EE30`/`0046EE70`/`0046EFD0`. Interior anchor `003332D1` (a `003697F0` call).

## SWE2-EC7-49 update (2026-09-19) - `0018B8B0`

`0018B8B0` (188 B) is the command-list emit leaf - `0018B4E0`/`001AB570`/`001F1810`/`0085E730`. Interior anchor `0018B8E1` (an `0018B4E0` call).

## SWE2-EC7-49 update (2026-09-19) - `0024B6F0`

`0024B6F0` (188 B) is a body - `00263E70`/`00263F70`/`00265020`/`00265200`/`003588B0`/`003A6D90`/`003B7E10`. Interior anchor `0024B711` (a `00263E70` call).

## SWE2-EC7-54 update (2026-09-19) - `00465510`

`00465510` (355 B) is an intentionally-ownerless gated processor tail - `003E5E50`/`00428AF0`/`00428CD0` plus `022C6F28`. Interior anchor `004655ED` (a `00428AF0` call).

## SWE2-EC7-59 update (2026-09-19) - `0046E640`

`0046E640` (161 B) is an ownerless body - `0020E620`/`002ED570`/`00370390`. Interior anchor `0046E66E` (a `002ED570` call).


## SWE2-EC7-59 update (2026-09-19) - `003A7F60`

`003A7F60` (160 B) is an ownerless action-context arm - `003697F0` single call plus `02EBEF98`/`02F97348`. Interior anchor `003A7FE1` (a `003697F0` call).


## SWE2-EC7-59 update (2026-09-19) - `00182B40`

`00182B40` (159 B) is an ownerless shared helper - `00186A90`/`00186AA0`/`00189120`/`001B66F0`/`001B6C40` plus `008C5B44`/`008C5B48`/`02CF7480`. Interior anchor `00182B44` (a `001B6C40` call).


## SWE2-EC7-59 update (2026-09-19) - `003BA150`

`003BA150` (159 B) is an ownerless hit/target helper - `002EE050`/`003A6BA0` plus `01EFE318`/`022C6F28`. Interior anchor `003BA15E` (a `003A6BA0` call).

## SWE2-EC7-60 update (2026-09-19) - `001B66F0`

`001B66F0` (242 B) is an ownerless shared helper - `001AB570`/`001B6560`/`00210EC0`. Interior anchor `001B676F` (a `00210EC0` call).

## SWE2-EC7-61 update (2026-09-19) - `001B6560`

`001B6560` (256 B) is an ownerless shared helper - `001A5810`/`001EDF00`/`005CC8A0`/`005CD0A0` plus `008F3CB0` and the `"EASTL set"` literal. Interior anchor `001B6581` (a `005CC8A0` call).


## SWE2-EC7-61 update (2026-09-19) - `002FCA00`

`002FCA00` (152 B) is a call-free `02EC32E0` `0x38`-stride record scan - match `dword[+0]` then `byte[+0x23]&0xF` nibble -> return code (nibble 7 -> 5). Interior anchor `002FCA22` (the `+0x23` nibble read).


## SWE2-EC7-61 update (2026-09-19) - `0046EE70`

`0046EE70` (151 B) is a `02EBEF88` bracketing helper - `0035B1A0`/`003EA3E0`. Interior anchor `0046EEA3` (a `0035B1A0` call).



## SWE2-EC7-63 update (2026-09-19) - `0024F9B0`

`0024F9B0` (144 B) is an action-context arm - `0026A430`/`0026AF80`/`003588B0`/`003A6D90` plus `020921B0`/`020925A0`-`020925A8` cells. Interior anchor `0024F9CB` (a `003A6D90` call).



## SWE2-EC7-63 update (2026-09-19) - `003D7C50`

`003D7C50` (144 B) is a call-free `02EBBA00` `0x84`-stride scan - `word[r9]==cx && dword[r9+4]==edx` over 32 slots. Interior anchor `003D7C71` (the `word[r9]` scan load).



## SWE2-EC7-66 update (2026-09-19) - `003D90C0`

`003D90C0` (134 B) is a `003D90C0`/`00460120` unlink arm - `002EA8B0`/`00314960` plus `02092628`/`02092631`/`02092632`/`02F97348`. Interior anchor `003D912A` (a `002EA8B0` call).



## SWE2-EC7-66 update (2026-09-19) - `00322850`

`00322850` (132 B) is a hit/target helper - `00263E30`/`003588B0` plus `02089340`. Interior anchor `00322865` (a `003588B0` call).


## SWE2-EC7-67 update - `00333A40`

`00333A40` (128 B) is an ownerless-scratch body - `0046EE70`/`003697F0`/`003A8D40`. Interior anchor `00333A82` (a `0046EE70` call).

## SWE2-EC7-70 update (2026-09-19) - `003A6D90` shared indexed read measured

`003A6D90` (86 B) is the `02F97348`-global indexed read the action-context
arms share: `word[+0x378] & 0x200` clear reads the record's own table -
`byte[0] == 3` returns -1, `ecx == -1` takes `[+0x90]` falling back to
`[+0x10]` when 0, else `[rdx + ecx*4 + 0x10]`; bit set indexes the shared
`02096A24` dword table with `ecx` (or 0) clamped below `[02096B24]`, and
out-of-range returns -1.
Interior anchor `003A6DDB` (the `02096A24` table lea).

## SWE2-EC7-81 update (2026-09-20) - `00537410` authored-ramp evaluator measured

`00537410` (409 B, stack-cookie) is the `[rcx+0x20] +0x11`-dispatch
the ownerless callers run: kinds `<= 2` take the id path -
`word[rbx+0x10] != -1`, `word[+0x36A] & 0x800` else
`003590D0`/`002E9B80` re-check, `022C6F28 + id*0x740` record's
`+0x284` gate, `00421E20` 0x100-copy into the scratch frame; kind
`== 3` resolves through `003A8240` and copies the `+0x30` vector.
Either path runs `00361CF0(&vec, rdi, ...)` (the ramp frame), then
`002F1F40` samples and `* 0x7F / 255` rescales into `[rdi]`; a dead
path writes `esi` = 0 and returns 0.
Interior anchor `00537466` (the `003A8240` resolve call).

## SWE2-EC7-82 update (2026-09-20) - `0046EE30` record init measured

`0046EE30` (51 B) is the init the ownerless callers run on their
records: `[+0]` takes `rdx`, `+0xA`/`+0xC`/`+0x12` zero, `word[+8]`
takes `r8w`, `byte[+0x10]` takes `r9b`, then `00250000()` writes the
result to `[+0x160]` - a five-field fill plus one computed slot.
Interior anchor `0046EE52` (the `00250000` call).

## SWE2-EC7-85 update (2026-09-20) - `003ED0E0` globals-derived record build measured

`003ED0E0` (85 B) is the four-field record builder the fade pass
(`0041E960`) and its siblings call: `[rcx]` takes
`cvtsi2ss(0xFF - byte_global)`, `[rcx+4]` zeroes, `[rcx+8]` takes a
global constant divided by `cvtdq2ps(dword_global2)`, and `[rcx+0xC]`
takes `cvtdq2ps(dword_global1)` - three globals folded into a scale
record, call-free.
Interior anchor `003ED11F` (the `divss`).

## SWE2-EC7-89 update (2026-09-20) - `003B3EA0` scratch-slot claim measured

`003B3EA0` (107 B) is the slot claim the shared-scratch callers
run: `002DF170()` first, then the `02EBCC80..02EBCD80` ring is
scanned 8-at-a-time for a clear flag byte; the free slot takes
`byte`=1, `dword[+4]`=`ecx`, and `word[+2]`=`bx` grown by
`max(2, ebx / 4)` rounded toward zero - a self-extending
0x100-byte scratch allocation.
Interior anchor `003B3EDB` (the claim arm).

## SWE2-EC7-94 update (2026-09-20) - `0035B550` + `0035B2F0` measured

`0035B550` (37 B) is the keyed float write `0046E990`, `0046EDD0`
and `005372D0` use against the `0x20`-stride slot table at
`02EB8BD6`: `cl-1` picks the slot, `ecx>>8` must equal the slot's
`+2` tag word, and only then does `xmm1` land at `+0x10`.
Interior anchor `0035B56D` (the `xmm1` store).

`0035B2F0` (135 B) is the slot claim `0035B650` and `005372D0` run
on the same table: the `02EB8BB8` index byte picks a 0x20 record
(0xFF returns 0), a nonzero `+1` flag returns 0 (occupied), and a
free slot is staged - `+1`=1, `+8`=rcx, `+0x10`=1.0f, the `+0`/
`+0x14`/`+0x16`/`+0x18`/`+0x19`/`+0x1A` fields are seeded from the
`02EB8Bxx` counter chain, and `dx` lands at `+0x1A`.
Interior anchor `0035B32D` (the `+8` record pointer store).

## SWE2-EC7-105 update (2026-09-20) - `00263F70` + `00263E70` measured

`00263F70` (11 B) and `00263E70` (11 B) are
the single-bit readers `0024B6F0` and
`003B8670` call on a record's flag bytes:
`(byte[rcx + 8] >> 3) & 1` and
`(byte[rcx + 9] >> 6) & 1` respectively -
adjacent-flag-bit fetches with no owner,
exactly the shared-leaf shape this page
predicts.
Interior anchors `00263F74` and `00263E74`
(the shifts).

`00426E40` (122 B) is the `022C6F28` chain-tail append `0042F2A0`/`0042F6C0`/`0042F880` run on the shared scratch records: `word[rcx]` copies to `[rdx+6]`; a `0xFFFF` at `[rcx+8]` adopts `word[rdx]` as the head index; otherwise the function walks the 0x740-stride record array from index `[rcx+8]`, following each entry's `+0xA` link (an entry whose `+0x284` reads 0 collapses to the null branch) until a `+0xA` of `0xFFFF`, then stores `word[rdx]` into the tail's `+0xA` — the list-attach primitive behind the hit/placement helpers.

Interior anchor `00426E71` (function `00426E40`).

`00193AD0` (636 B) is the rect re-layout the shared-scratch loop `00188B10` runs (already named beside it on this page): `+0x2E0`/`+0x2E4` compare-and-store on dirty, five `001EEE80` refreshes across `+0x280`..`+0x298` plus the midpoint-aligned `+0x2A0` write, then `001DC4A0`/`001DC4C0`/`001DC510`/`001DC590`/`001FDF70`/`00615BC0`/`00616700`/`00624660`/`00624670`/`0065C750` - the render-pass record's resize-on-change.

Interior anchor `00193B10` (function `00193AD0`).

`002FCCC0` (562 B) is the keyed release `002EAD00` and `003B8670` call: `r9d & 0x3F < 0x30` selects a 0x38-stride record of `02EC32E0`, `[rdi]` must equal the key and `byte[+0x23] & 0xF == 5`, then the `02EC3D60` list sums `word[+0x20]`-indexed `& 0x1F` fields, `003AFFB0(0x24 - sum)` and `0036C1D0(8)` run, a 0x3B0 stack record is `00861EC0`-zeroed with `word=0x101`/`dword=ebx`, and `0024B270` fires - the interpreter's keyed teardown.

Interior anchor `002FCD80` (function `002FCCC0`).

`003AFFB0` (383 B) is the population count `002FCCC0` calls: walks `02EBEC18` records (`0x90` stride to `02EBEF78`) and counts into `ebp` each slot whose six `dword` fields (`-0x18`, `0`, `+0x18`, `+0x30`, `+0x48`, `+0x60`) are all non-zero; `0036C1D0`/`0024EE60`/`0036C140` follow - the scratch pool's live-slot census.

Interior anchor `003B0079` (function `003AFFB0`).

`0036C140` (84 B) is the shared-scratch record-stack pop `003AFFB0`'s census tail and the ~75 resource consumers run: spins while `dword[022D89C0] <= 0`, decrements it, then copies the top 16-byte record at `022D89D0 + idx*16` out - `word[+0]` to `022D89BC`, `byte[+2]` to `022D8E18`, `qword[+8]` to `022D8E20`, `byte[+3]` to `022D8E28` - the scratch pool's pending-work dequeue.

Interior anchor `0036C167` (function `0036C140`).

`0036C1D0` (20 B) is the call-site shim `0036C140`'s caller set takes into `0036C1F0`: `r9 = qword[rsp+4] - 5`, `r8 = 0`, tail-jump - the stack-context-loading entry into the queue-tail executor.

Interior anchor `0036C1D7` (function `0036C1D0`).

`0036C110` (38 B) is the scratch byte-stack pop paired with `0036C1A0`: when `dword[022D89C8] >= 0`, decrement it and copy `byte[022D8DD0 + idx]` into `022D8E1C` - the pool's slot-index dequeue half.

Interior anchor `0036C12B` (function `0036C110`).

`0036C1A0` (48 B) is the scratch byte-stack push: while `dword[022D89C8] < 0x1F`, store `byte[022D8E1C]` at `022D8DD0[idx]`, bump the count and keep `022D8E1C = ecx` - the slot-index enqueue half of the `0036C110` pair.

Interior anchor `0036C1BB` (function `0036C1A0`).

`00369800` (85 B) is the tagged-pointer release the `00369860` family fronts: rejects `ecx` of `0`, `(cl&3)==0` or `< 0x100000`; masks the low tag bits, `0036A9C0` resolves the arena, and when `[rcx+8]` and its `+0x40` are non-null tail-enters `00369860(rbx+0x40, 0)` - the validating-release entry.

Interior anchor `00369846` (function `00369800`).

`0036B160` (148 B) is the scratch-pool service body the seven consumers run on the dequeued record: `ecx = dword[022D89BC]` (the class word `0036C140` pops) with `edx` = the caller's arg resolves through `0036BC60`, falling back to `0036BFE0` with `dword[rsp+0x28] = 1` when the lookup returns null; `0036C4B0(class, record)` dispatches and a nonzero answer drives `0036A000(ecx)`, then `byte[obj-0x3E] = [022D8E18]` (the popped tag byte), `dword[obj-0x10] = 0020E620(0)`, `word[obj-2] = 0`, `0036D170(result)` - the dequeue's execution half.

Interior anchor `0036B181` (function `0036B160`).

`0036C750` (57 B) is the shared basename helper: a strlen scan reaches the terminator, then walks back for the last backslash or slash and returns the pointer just past it (or the string start when no separator exists) - the path-tail read the field-record, script and loader callers share.

Interior anchor `0036C773` (function `0036C750`).

`00254550` (9 B) is the nine-byte shared bit-test leaf: `bt ecx, edx` / `setb al` returns bit `edx` of mask `ecx` as a bool - the flag probe five unrelated bodies inline through one call.

Interior anchor `00254552` (function `00254550`).

`0036B130` (41 B) is the tagged-handle payload read: rejects `ecx` of `0`, `(cl&3) == 0` or `< 0x100000`, masks the two tag bits off and returns `[handle+8] + 0x40` - the object-payload half of the `0036C5D0`-style tagged decode.

Interior anchor `0036B14D` (function `0036B130`).

`0036C5D0` (79 B) is the tagged-handle re-tag: the same `0036B130` decode gates (`(cl&3) != 0`, `>= 0x100000`, mask, `[h+8]` object), then on a tag change moves `dword[obj+0x18]` between the per-class counters `dword[022D8E10 + old*4]` and `dword[022D8E10 + new*4]`, writes `byte[obj+0x17] = new` and zeroes `word[obj+0x3E]` - the scratch pool's class reassignment beside the `022D8E18`/`022D8E20` dequeue fields.

Interior anchor `0036C605` (function `0036C5D0`).

`0036BFE0` (261 B) is the scratch-pool fallback `0036B160` drops to: bit `ecx` of `dword[022D89B8]` must be set or the body parks on `jmp $` (the fail-closed assert); `dword[022D89BC]` picks the current 0xA8-stride descriptor in `022D7FD0` (0xE max, else null), its `qword[+0xA0]` callback (if present) scores the caller's arg, then on a still-valid index with `qword[+0x50]` set the pair `0036AAD0(desc, 0)` / `0036ABE0(desc)` counts free entries and marks `byte[+2]`/`byte[+0x62]` dirty; `0036BC60(arg, 0, 0)` finally runs the real dequeue and the whole body retries from the index read while the score/callback state says the chosen arena cannot serve - the retry-until-served sibling of `0036B160`.

Interior anchor `0036C013` (function `0036BFE0`).

`003697C0` (47 B) is the scratch-pool `+0x62` flag clear beside `0036BFE0`: `bt dword[022D89B8], ecx` fail-closes on the census bit, `ecx <= 0xE` indexes the `022D7FD0` descriptors at `0xA8` stride and clears `byte[+0x62]` - an out-of-range index writes `0` to absolute `0x62`, the pool's loud assert - the descriptor release the frame and render-pool callers share.

Interior anchor `003697C6` (function `003697C0`).

`0036AAD0` (261 B) is the counted record sweep `0036BFE0` runs over `[rcx+0x90]`: it walks `[r13+0x50]` chains, resolving each record's `+0x24`/`+0x28` members through `0020E600`, keeps the live predecessor in `rdi` across the `+0x18` ordering (`>`, `==`, `<` arms), skips links whose `+0x15` byte carries bit 2, calls `0036A2A0` on each accepted record while `r12d` stays set, and returns the accepted count

Interior anchor `0036AB46` (function `0036AAD0`).

`0036A9C0` (260 B) is the linked-record splice `00369800` uses: on a live record with `byte[+5]` set it resolves the owning table by `byte[+4]` (`*0xA8` into `022D7FD0`, or none past `0xF`), splices the record out of the `+0x40`/`+0x48` word-indexed chain (fixing neighbours' `word[+2]` back-links), relinks it at the table head, clears the parent record's `+0x15` bit 2 with a `0036C790` notify when bit 1 was armed, and marks the record free (`byte[+5]`/`word[+6]`/`qword[+8]` zeroed)

Interior anchor `0036AA25` (function `0036A9C0`).

`0036ABE0` (243 B) is the filtered relink `0036BFE0` runs: it walks the `[rcx+0x90]` chain through `0020E600`-resolved `+8` links, keeps nodes whose `+0x10` record's `+0x15&6` is not 2, and re-splices each against the `[r14+0x50]` chain (`+0x24`/`+0x28` resolved) ordered on `+0x18` rank under `+0x15&4`

Interior anchor `0036AC73` (function `0036ABE0`).

`001B67F0` (210 B) is the locked pool-acquire `001B66F0` wraps: `005CD4F0` takes the `+0x10` lock, `+0x98 == 0` grows via `001EE040`, else `[+0x80]` is unlinked by `0016D6D0`/`0016DA60` and freed through `[+0xA0]` vtable `+0x18` after `+0x98` decrements; the value then `00199DB0`-emplaces into the `+0x38` map and `005CD820` releases - ownerless scratch with lock discipline

Interior anchor `001B6818` (function `001B67F0`).

`002FCBF0` (196 B) is the locked freelist pop `003B8670` calls for node storage: inside the `0036C1D0`/`0036C140` critical pair it unlinks the `02EC3D70` head, enqueues the node on the `02EC3D60`/`02EC3D68` list tail, stamps `[rbx+0x20] = di`, folds `++02EC3D78 << 6` into `[rbx]` and clears `+0x23` bits `0x1F`; a `002FC860` init returning 0 clears the `+0x23` nibble entirely and yields 0, else `[rbx]` is returned

Interior anchor `002FCC2B` (function `002FCBF0`).

`003EA3E0` (77 B) is the wait-and-release pair `003EA330` (voice-slot reset) and `0046EE70` both run per pending entry: when `ecx` is nonnull the loop calls `0035EA30(0)` then `0016D6A0()` (the known `ret 0` stub) while `002DEE90(ecx)` still reports the request live; once it drains, a nonnull `edx` goes to `002DF690` - the loader's drain-then-notify on a request handle

Interior anchor `003EA402` (function `003EA3E0`).

`00539CF0` (167 B) is one of the three fixed-offset broadcast updaters `005004C0` multiplexes: after `00500470`, arg `edx` goes to `0042FCF0` at `+0x80`, `00430AF0` at `+0xD0`/`+0x110`/`+0x150`, `004304F0` at `+0x190`, `00431770` at `+0x1A0`; a nonzero `+0x2BC` byte routes `003AA280(0, 0x56, al)` through `0020E620` into `+0x2D0`, returning `+0x2E0`

Interior anchor `00539D0D` (function `00539CF0`).

`00539270` (164 B) is the sibling broadcast in the same `005004C0` set: `00500470`, then `edx` to `00430AF0` at `+0x80`/`+0xC0`/`+0x100`/`+0x140`, `0042FCF0` at `+0x180`/`+0x1D0`, `004304F0` at `+0x220`/`+0x230`/`+0x240`, returning `+0x2A0`

Interior anchor `0053928D` (function `00539270`).

`00539560` (164 B) is the third broadcast arm: `00500470`, `00430AF0` at `+0x80`/`+0xC0`/`+0x100`, `0042FCF0` at `+0x140`/`+0x190`, `004304F0` at `+0x1E0`/`+0x1F0`/`+0x200`/`+0x210`, returning `+0x254`

Interior anchor `0053957D` (function `00539560`).

`0024C3C0` (157 B) is the type-bucketed unlink-and-relink the action-context row already lists: it walks the `020910A0 + ecx*8 + 0x50` head for `rdx`, splices each node out of the `[+0x348]`/`[+0x350]` doubly-linked list (fixing the bucket head through the node's own `[rax]` byte index when `+0x350` is null), then pushes the removed node onto `02092170`

Interior anchor `0024C3E0` (function `0024C3C0`).

`0036C1F0` (150 B) is the staged-selection slot push `0036C1D0` wraps under its arena guard: `dword[021B89C0 + ecx*4]` is the per-index count (capped `0x1F`, spinning in place at the cap); the next record at `021B89D0 + (ecx*0x20 + count)*8` takes `word` = `022D89BC`, bytes = `022D8E18`/`022D8E28`, qword = `022D8E20`, the count bumps, then the body reflects the staged globals back - `edx -> 022D8E18`, `r9 -> 022D8E20`, `byte[021B89A8 + ecx] -> 022D89BC` - the ownerless staged-args-to-record handoff.

Interior anchor `0036C224` (function `0036C1F0`).

`003A9070` (143 B) is the row delete on the `02EBEF88` sub-object this page's family table names: `[[02EBEF88]+0x18]` holds up to 32 eight-byte rows; the `(dword[+0], byte[+4])` match on `(ecx, edx)` is found, then `word[+6]` decides - zero means compact-delete by shifting every later row down and stamping `0xFFFFFFFF` at the tail, non-zero means `byte[+5] |= 1` and a 1 return - the tombstone-or-remove branch of the shared table.

Interior anchor `003A90C0` (function `003A9070`).

`003A96A0` (142 B) is the resolve-and-bind sibling on `02EBEF90`: `word[rcx]` indexes `[02EBEF90]`'s pointer table into `rbp`, `003A9790` resolves `ecx`/`ebx` into `rdi`, `00861EBA` copies the caller's `rsi+4` string into it, `00442460` stores `edi + dword[02EBB738]`, and when `rbp` is non-null `003A9590(rbp, rdi)` links it; returns `rsi + 4 + rbx` past the read - the string-slot bind the table's consumers ride.

Interior anchor `003A96ED` (function `003A96A0`).

`003A9790` (198 B) is the find-or-make slot installer `003A96A0`'s bind path calls on `02EBEF90`: a nonzero `ecx` selects that row directly, zero scans `+8` onward for the first empty slot up to `0x140`; a live occupant is released through `003697F0`, `0036A100` carves the replacement, `byte[+0x282] = bpl` and `word[+0x280] = bx` are stamped, and the record lands at `[[02EBEF90]] + idx*8` - a full table returns 0 - the slot-claim half of the shared scratch table.

Interior anchor `003A97DA` (function `003A9790`).
