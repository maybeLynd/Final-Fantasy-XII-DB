---
contract: calculator slots 60-79 - what a preparation step reads, what it writes, and what it leaves alone
category: 08-Combat-Formula
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md
entries: ["00389DD0", "00389F80", "0038A110", "0038A1F0", "0038A2D0", "0038A3A0", "0038A470",
          "0038A590", "0038A680", "0038A820", "0038A9D0", "0038AA90", "0038AAF0", "0038ABC0",
          "0038AD70", "0038AE50", "003849B0", "00385680", "00385F60"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 82 addresses cited - 17 data, 26 entry, 39 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-preparation-step-family-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the preparation step family, calculator slots 60–79

Twenty slots of the 202-slot calculator table hold **sixteen distinct functions**, and the sixteen do
not agree on what they read or on what they write. Fourteen write all three scratch words; one writes
two; one writes only the multiplier. Fifteen take two arguments in practice; **one reads a third**.

That spread is the contract. A reimplementation that treats the family as sixteen interchangeable
"compute the damage multiplier" functions will compile, run, and be wrong in the two places where the
family is not uniform.

## 1. Purpose

The page this implements establishes the arithmetic of the seven named variants. It leaves open which
of them applies, and does not name the other nine. This states the family's interface, its writes and
— the part a reimplementer cannot recover from prose — **the memory each member leaves unchanged**.

## 2. Interface

| | |
|---|---|
| how reached | **only** `call qword ptr [imageBase + slot*8 + 0x1DDA5C0]`, table base `01EFA5C0` |
| call sites | exactly two in the image: `003859FF` (preview) and `003863D0` (resolution) — **and that now includes tail jumps** (below) |
| `rcx` | the attacker's **`BattleStatsRecord`** |
| `rdx` | the defender's **`BattleStatsRecord`** |
| `r8` | the caller's stack result record — `rsp+0x38` at `003859F4`, `rsp+0x48` at `003863C5` |
| returns | nothing used by either caller |

> **CORRECTED 2026-09-11 — these were published as `BattleUnit` and they are not.** Every offset this
> family reads is a declared `BattleStatsRecord` field: `+0x2A` strength, `+0x2B` magick power,
> `+0x2C` vitality, `+0x2D` speed, `+0x2E` attack, `+0x2F` defence, `+0x30` magick resist, `+0x1C2`
> level, and `+0x50` the `uint16[5]` equipment slots. **None of them exists on `BattleUnit`.**
>
> **How it survived a peer review of the same table:** `BattleUnit` *does* have bytes at two of those
> offsets, meaning something else entirely — `+0x2C` is `presentationEventParameter` and `+0x30` is
> `killerActorHandle` (renamed from a garbled `theKillerIdThe` on 2026-09-12). A reimplementation written from the old §2 and §12 would have compiled, run, and
> read the wrong fields of the wrong struct. This is the exact failure the rule about compilation
> never being ABI proof exists for, and it was in the contract's most load-bearing line.

**"Exactly two" was re-tested for tail jumps, 2026-09-11.** A `call`-only sweep hid a dispatch from me twice in one session — the frame pump's sixteenth group and a registry binder — because MSVC tail-calls the last thing a function does. Re-run over **both** `call` and `jmp` through a scale-8 index: **11 indexed indirect transfers image-wide, 3 of them tail jumps, and none of the three reaches `0x1DDA5C0`.** The two call sites stand, now as a tested claim rather than an assumed one.

**The third argument is real and is read by exactly one member.** `0038A680` (slot 72) does
`test byte ptr [r8 + 0x1b], 2` at `0038A6B1`, before any call, so `r8` there is still the argument.
The other fifteen never touch `r8` before reassigning it. A two-argument signature is therefore
**correct for fifteen of sixteen and silently wrong for slot 72** — compilation proves nothing here.

## 3. Types

| | |
|---|---|
| the calculator table | `01EFA5C0`, **202 entries** of 8 bytes, ending `01EFAC08` |
| unassigned slots | `0016D6A0`, whose body is `ret 0` — and it is **`_guard_check_icall`**, the Control Flow Guard stub, three bytes because guard is disabled in this build. **CORRECTED 2026-09-11:** this row read "a real no-op handler, not padding or a guard". The behaviour was right and the identification was wrong — it is literally the guard function, neutered, which is what MSVC emits when CFG is off. An unassigned slot therefore points at the CFG stub rather than at a purpose-built no-op, and a reimplementation needs a function that returns, not a null |
| the scratch triple | `02AEE054` multiplier, `02AEE058` attack + variance, `02AEE05C` defender stat |
| attacker fields read (all `BattleStatsRecord`) | `+0x1C2` level; `+0x2A` strength, `+0x2B` magick power, `+0x2C` vitality, `+0x2D` speed; `+0x2E` weapon attack; `+0x52` = **`equipmentSlots[1]`**, element 1 of the `uint16[5]` at `+0x50` (slot 72 only) |
| defender fields read (all `BattleStatsRecord`) | `+0x2F` defence; `+0x30` magick resist (**slots 62 and 69**). **Slots 60/63, 70, 74 and 61/64/75 read no defender at all.** |

The table's extent was computed, not cited: slots `0..201` all hold entries that appear in the
function graph, and slot 202 (`01EFAC10`) holds `3F80000000060303`, which is not a code address. That
agrees with the 202 of [the step table](Step-Table/combat-formula-step-table.md), derived separately.

**One member of the family is unreachable in this build.** Slot 73 (`0038A820`) is named by **no
recipe** — neither preview nor resolution list, across all 109 — and has **no direct call site**: its
table entry `01EFA808` has zero referencing instructions image-wide. It is a real, complete function
sitting in the dispatch table that nothing can select. A reimplementation should keep it and keep it
unreachable; wiring it to anything would add behaviour the original does not have.

It is not alone in the table: of the 202 slots, 38 hold the `ret 0`, 160 are named by at least one
recipe, two (37 and 118) are reached only by direct `call qword ptr [rip]` sites, and **two — 73 and
131 — are reachable by nothing at all**.

## 4. Preconditions · postconditions · invariants

**Precondition: `rcx` and `rdx` are non-NULL.** No member tests either; slot 65 dereferences `rcx+0x2A`
in its fourth instruction.

**Precondition: the slot is in range — and nothing enforces it.** Both dispatchers load the slot from
the recipe list and index the table with no bound check:

```
003859F0  movsxd rax, dword ptr [r15 + rdi*4]     preview
003859FF  call   qword ptr [r12 + rax*8 + 0x1dda5c0]
003863C0  movsxd rax, dword ptr [r13 + rbp*4]     resolution
003863D0  call   qword ptr [rbx + rax*8 + 0x1dda5c0]
```

The **recipe id** is bounded (`cmp …, 0x6D` at `00385980`, `00386182`, `0038620D`); the **slot inside
the recipe is not**. An authored list carrying a slot ≥ 202 calls through whatever `.data` follows the
table. This matters to modding, which is where recipe lists get edited.

**Postcondition: the scratch words this member writes hold its results; the rest are untouched.**

## 5. State

The three scratch words, and nothing else. No member writes through `rcx`, `rdx` or `r8`.

**Measured 2026-09-12 rather than asserted.** The differential poisons all three words with bit
patterns no computation in this family can produce and compares them after every call, so a word
a member LEAVES ALONE is a different result from one it rewrites with the same value. Sixteen of
the suite's calls come back carrying a poison word. **`0038AA90` writes the multiplier and
nothing else; `0038A9D0` writes the first two and leaves the defence term.** Two members —
`00389F80` and `0038A470` — write an immediate `0` to the defence term rather than leaving it,
which is the same value a fresh frame would hold and a different fact about the code.

## 6. Relationships

- **The slot comes from a recipe, not from a weapon.** Recipe id → the pointer table at `01EF96C0` →
  two `-1`-terminated slot lists; the preview runs the first, the resolution the second. That
  mechanism is [the recipe system's](Recipe-System/ranged-weapon-recipes.md) and is cited, not
  re-derived. **Preparation slots appear in the second list**, which is why they are invisible to a
  reading of the first.
- **Recipes 20–29 differ only in this slot** — identical preview lists, and resolution lists identical
  but for the preparation entry: 20→65, 21→66, 22→67, 23→68, 24→69, 25→66, 26→65, 27→70, 28→71,
  29→72. That is the shape of "which weapon type selects which variant" as the data expresses it.
- **`BattleFormula_ResetScratchState` `003849B0` zeroes all three** (`00384A29`/`2F`/`35`) and has
  exactly two callers — the same two dispatchers, at `0038585E` and `00386001`, both **before** their
  walk. So a member that skips a word leaves a defined zero on the first step of a program, and the
  previous step's value after that.

## 7. State transitions

```
Reset            003849B0        054 = 058 = 05C = 0
for slot in list:
    handler(attacker, defender, &result)      no bound check on slot
    if [02AEDFB8] == 1: break                 003859AC / 003863D7
```

### What one member does — the shape all sixteen share

Added 2026-09-12 from a read of every body, and executed the same day. The section above
described the DISPATCH and left the members to §12's two examples; this is the template the
other fourteen also follow.

```
m      = (level + statA) * statB              BattleStatsRecord +0x1C2, and two stat bytes
054    = f(m)                                 one of six closed forms
attack = (float)atk[+0x2E]  or  an authored row's byte
gate   = attack * 0.125f
frac   = gate < 0.01f ? 0
                      : (float)(MT_draw() % (int)(gate * 100.0f)) / 100.0f
058    = attack + frac
05C    = (float)def[+0x2F] or def[+0x30], or an immediate 0, or untouched
```

| body | m = (level + ·) × · | `054` | attack term | `05C` |
|---|---|---|---|---|
| `00389DD0` | magick × magick | m/256 + 2 | row `+0x10` | def `+0x30` |
| `00389F80` | magick × magick | m/256 + 2 | row `+0x10` | **immediate 0** |
| `0038A110` | speed × strength | **m / 218** + 1 | weapon | def `+0x2F` |
| `0038A1F0` | magick × strength | m/256 + 1 | weapon | def `+0x2F` |
| `0038A2D0` | vitality × strength | **(m/256) doubled**, no addend | weapon | def `+0x2F` |
| `0038A3A0` | strength × strength | m/256 + 1 | weapon | **def `+0x30`** |
| `0038A470` | **none** | attack + frac₁ | weapon, **a second draw** | **immediate 0** |
| `0038A590` | strength × strength | m/256 + 1 | level + weapon + strength | def `+0x2F` |
| `0038A680` | strength × strength | m/256, **no addend** | see below | def `+0x2F` |
| `0038A820` | strength × strength | m/256, **no addend** | row `+0x10` | def `+0x2F` |
| `0038A9D0` | none | row `+0x11` | row `+0x10` | **untouched** |
| `0038AA90` | none | row `+0x10` | **untouched** | **untouched** |
| `0038AAF0` | strength × strength | m/256 + 1 | weapon | def `+0x2F` |
| `0038ABC0` | strength × strength | m/256 + 2 | row `+0x10` | def `+0x2F` |
| `0038AD70` | strength × strength | **(m/256) × 1.5** + 1 | weapon | def `+0x2F` |
| `0038AE50` | magick × magick | m/256 + 1 | weapon | def `+0x2F` |

**Two members take their gate from the combatant rather than from the weapon.** `0038A590` and
`0038A680`'s level form build it from `(level + strength) * 0.125f`, so a unit with no weapon
still draws. Everything else gates on `atk[+0x2E] * 0.125f`.

**`0038A470` draws TWICE against one gate**, once into `054` and once into `058`, and the two
draws are separate calls — the suite's cursor moves by two.

**`0038A680` (slot 72) is two computations behind one entry.** Bit 1 of the result record's
`+0x1B` selects the level form; that form is then gated again on the attacker's
`equipmentSlots[1]` at `+0x52` against the dword at `[02EBF0F8] + 4` plus `0x1000`. The compare
at `0038A6EB` is `jae`, **unsigned**, and the fallback is re-tested as a SIXTEEN-bit compare
against `0x1000` (`0038A6F4`), so the exact value `0x1000` passes whatever the limit is. The
level form's result is halved: `((level + strength) + frac) * 0.5f`. A limit whose `+0x1000`
carries into bit 31 is the only place a signed compare would disagree, and the suite drives it
there.

## 8. Script · resource · event interactions

Four members reach authored data instead of the combatants, through the registry idiom
`resolve(header + 0x0C)` at `0020E600` with the stride from the `u16` at `+0x08`: slots 60/63, 61/64/75,
62 and 74 read row bytes `+0x10` (and `+0x11` for 74). **Slots 61/64/75 and 74 read no combatant at
all** — they are table lookups wearing a preparation's signature.

## 9. Determinism

Deterministic given the stat bytes, except where the member draws variance through `00379CD0`. The two
authored-row-only members draw nothing.

## 10. Failure paths and edge conditions

**The authored-row members dereference NULL when the table is absent.** In `0038AA90` the miss path is
`xor eax, eax` at `0038AAD2` falling into `movzx ecx, byte ptr [rax + 0x10]` at `0038AAD4`; `0038A9D0`
has the same shape twice (`0038AA1D`→`0038AA20`, and `0038AA6E`) with `rbx` zeroed at `0038A9DD`. Both
arms are reached when the registry pointer at `02EBF138` is NULL or the row does not resolve. This is
the same class as `OPUS-NOTICE-REWARDNULL` and is **not** established as reachable in play.

**Executed 2026-09-12, with a caveat that matters.** All six row-reading members were driven
with the registry pointer null, and both sides compute the same row address — `0` — and read
`+0x10` of it. The fixture MAPS A PAGE AT ADDRESS ZERO so that the two can be compared at all.
**The shipped process has nothing mapped there**, so what the run establishes is that the
reconstruction reaches the same doomed address by the same arithmetic, and NOT that the path
survives. A green line here is agreement about a crash, not the absence of one.

**The divisor has exactly one guard.** `(int)(gate * 100.0f)` feeds an unsigned `div` with no
further test, so a zero divisor is prevented only by the `comiss` against `0.01f` above it. A
weapon byte of `0` gives a gate of `0`, which is below the threshold, so no draw is taken and no
divide happens — driven at `0`, `1`, `2`, `7`, `8` and `0xFF` across nine members. A
reconstruction that replaced the `0.01f` test with a test against zero would divide by zero on
the first weapon byte in `1..7`.

## 11. Observable behaviour

Not established. Nothing in this family has been executed under observation.

## 12. Reproduction formula

```c
/* the table, not one function: sixteen bodies behind twenty slots */
typedef void (*CalcStep)(BattleStatsRecord *atk, BattleStatsRecord *def, ResultRecord *r);
extern CalcStep calc_table[202];            /* 01EFA5C0 */

/* slot 72 is the reason the third parameter is in the signature at all */
static void Prep_Slot72(BattleStatsRecord *a, BattleStatsRecord *d, ResultRecord *r) /* 0038A680 */
{
    int m = (a->level + a->strength) * a->strength;     /* +0x1C2, +0x2A */
    scratch.multiplier = m * (1.0f/256.0f);             /* 02AEE054 */
    if (r->flags1B & 2) { /* ... */ }                   /* the arg nobody else reads */
    scratch.attack  = /* ... a->equipmentSlots[1] (+0x52), a->+0x2E ... */;
    scratch.defence = d->defence;        /* 02AEE05C -- d is read ONCE, at +0x2F */
}

static void Prep_Slot61(BattleStatsRecord *a, BattleStatsRecord *d, ResultRecord *r) /* 0038AA90 */
{
    (void)a; (void)d; (void)r;                          /* reads no combatant */
    scratch.multiplier = (float)AuthoredRow()->byte10;  /* 02AEE054 ONLY */
    /* 02AEE058 and 02AEE05C are deliberately left as the previous step left them */
}
```

## 13. Runtime validation

**Executed 2026-09-12 as the twenty-eighth differential pilot (`OPUS-PREPFAMILY-ISOLATED`).
Evidence class: isolated original-code. Not observed in a running game, and nothing below claims
otherwise.**

`Reconstruction/Tests/Differential/diff_prep_step.py` runs **all sixteen bodies** as shipped bytes
under Unicorn at their real virtual addresses, against `Reconstruction/Game/Combat/prep_step.c`
built by MSVC at `/W4 /O2`.

**This is the first pilot with no oracle at all.** The family's only shared callee, `00379CD0`, is a
`jmp` thunk to `00863BF0` — the MT19937 draw — and it runs for real: cursor `02EB4230`, 624-word
state `02EB3870`, lazy self-seed `00866D60` with 5489, twist `00866B90`. The reconstruction side
**links the RNG pilot's own reconstruction**, `Rng_MtDraw`, already executed in its own differential,
and the fixture plants ONE state into both. The draws are therefore compared, not scripted.
`0020E600` runs for real too, as it did in the shape pilot. So a green run here is evidence about
the composition of two reconstructions and not only about one body in isolation.

    diff_prep_step   : 598 compared lines, 0 mismatches, 210 scratch images (126 distinct),
                       26 calls leaving a scratch word untouched, one image page mapped on demand
    negative controls: eight, each a plausible misreading - slot 61 tidied into writing all three
                       words (8 lines); a signed remainder (3); the product's second operand made
                       the first (24); the wrong defender byte in 0038A3A0 (8); an offset instead
                       of the doubling in 0038A2D0 (8); a signed equipment compare (8); 0038A9D0
                       reading +0x10 twice (6); the row address built in 64 bits (12)
    mutation campaign: 67 mutants, 61 KILLED, 1 SURVIVED, 1 EQUIVALENT, 4 NO_BUILD, inputs stable and hashes re-checked

**Two of the eight controls PASSED on the first fixture, and both were real gaps.** A signed
equipment compare agrees with the unsigned one everywhere below the signed boundary, and a 64-bit
row address agrees with the 32-bit one everywhere below four gigabytes. Cases were added that put
each over its boundary — a limit of `0x7FFFF000`, and a stride-times-index product of `0x100000110`
— and both controls then failed. **Nothing else in the suite can see either property**, which is
the argument for keeping those two cases.

**The campaign's first round left four survivors; three were one gap.** All three sat in the row
helper's null guard, which cannot fire while the resolver's base is non-zero — `base = heapBase +
reference` is zero only when both are, and every case planted a base of `0x30000000`. Cases with a
base of zero close them. §10 already said both arms are reached "when the row does not resolve";
nothing had ever put the fixture in that state.

**The one remaining survivor is equivalent, by argument rather than by `/Brepro`.** Mutating slot
72's `limit = 0` initialiser to `1` changes nothing observable: the initialiser matters only when
`[02EBF0F8]` is null, and the only equipment value that could distinguish `limit + 0x1000` of
`0x1000` from `0x1001` is exactly `0x1000` — which the separate SIXTEEN-bit re-test at `0038A6F4`
accepts either way. The `== 0x1000` re-test makes the first unit of the limit unreachable. It is
reported as SURVIVED because the tool proves equivalence only by identical bytes, and these differ.

**What this run does not establish.**

- **Nothing here has been observed in a running game.** §13's two requests below stand.
- The **two dispatchers**, the recipe lists and the reset at `003849B0` are out of scope: this is
  the sixteen bodies, called directly, one at a time.
- **The generator's SIMD arm is not executed.** `00866B96` tests the CPU-feature dword at
  `01F44858`, whose value in the shipping image is `1`, so the scalar arm runs on both sides. The
  `>= 2` arm is never entered here and nothing about it is claimed.
- **The null-row path is agreement about a crash, not the absence of one.** The fixture maps a page
  at address zero so the two sides can be compared; the shipped process has nothing mapped there.
  What is shown is that both reach the same doomed address by the same arithmetic.
- One image page, `01F44000`, is mapped on demand from the image rather than listed in advance.
  Pages arrive from the file; a page the file does not cover arrives as zeros, which is what the
  loader does with `.bss`.

**Still wanted from a running game**, unchanged by this run:

1. Break on `003863D0` and record `rax`. A capture of the slots that actually occur settles §6's
   recipe mapping against live play. Filed as **class C** of `OPUS-REQ-ASTRA-TRIAGED-QUEUE`.
2. The **class A** check — call `0038AA90` with the registry pointer at `02EBF138` NULL and confirm
   §10's dereference — is now **half answered**: the arithmetic is confirmed in isolation, and what
   remains is whether the process faults, which only a process can show.

Requested from ASTRA; not claimed by me.

### 13a. `EXP-111` cited — the twist this section already relies on, executed (FABLE, 2026-09-22)

[`EXP-111`](../_experiments/EXP-111-mt-twist-simd-exec.md) carries
`contract: ../08-Combat-Formula/CONTRACT-preparation-step-family.md` and was never cited back; under
the cite-or-decline ruling it is **CITED**, and it is the one of the eight routed by
`FRONTIER-REQ-FABLE-EXPERIMENT-BACKREFS` that needed no argument.

**This section already depends on that body by name.** It records that the family's only shared
callee `00379CD0` is a `jmp` thunk to `00863BF0`, the MT19937 draw, which *"runs for real"* with
lazy self-seed `00866D60` and **twist `00866B90`**. `EXP-111` executes exactly that twist as shipped
bytes **under both values of its feature gate**, against an independently computed reference — 8/8
state cases, 20/20 mutants, stable across both arms.

**What it adds to this contract specifically:** the pilot compares draws rather than scripting them,
so every green run here has been resting on the twist being right. `EXP-111` establishes that
separately, and **under both gate values** — so the comparison holds on whichever arm the host
selects, which the differential alone could not show because it exercises one arm per run.

## 14. Unresolved

- Semantic names for the nine unnamed members. The read sets below are the evidence; the naming is
  **E-3** and belongs to the semantic lead.
- ~~Whether slot 70's defender `+0x2E` read is a distinct mechanic~~ — **void, 2026-09-12**: there is
  no defender read. §15's re-derivation binds `mov rbx, rcx` at `0038A47A`, so all three `+0x2E`
  reads are the **attacker's**, and the slot stores an immediate `0` to `02AEE05C` at `0038A573`
  instead of measuring anything against the defender. The question was asked of a row that the same
  section had already corrected.
- Whether any recipe list reachable in play carries an out-of-range slot (§4).

## 15. Evidence

Static, from the shipping image (`73461D08…`), read with a disassembler over every function body in
the graph rather than by pattern match.

**The read sets carry a positive control.** The same instrument was run first on the seven **named**
variants and reproduced [the page's](Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)
table exactly — attacker `+0x2A`/`+0x2B`/`+0x2C`/`+0x2D`, level `+0x1C2`, weapon `+0x2E`, defender
`+0x2F` for six and `+0x30` for one, with no discrepancy. Only then were the nine unnamed read.

| slot | function | attacker | defender | authored row | writes |
|---|---|---|---|---|---|
| 60, 63 | `00389F80` | `+0x2B`, `+0x1C2` | — | `+0x10` | 054, 058, 05C |
| 61, 64, 75 | `0038AA90` | — | — | `+0x10` | **054 only** |
| 62 | `00389DD0` | `+0x2B`, `+0x1C2` | **`+0x30`** | `+0x10` | 054, 058, 05C |
| 65, 76 | `0038AAF0` | `+0x2A`, `+0x1C2`, `+0x2E` | `+0x2F` | — | 054, 058, 05C |
| 66 | `0038A110` | `+0x2D`, `+0x2A`, `+0x1C2`, `+0x2E` | `+0x2F` | — | 054, 058, 05C |
| 67 | `0038A1F0` | `+0x2B`, `+0x2A`, `+0x1C2`, `+0x2E` | `+0x2F` | — | 054, 058, 05C |
| 68 | `0038A2D0` | `+0x2C`, `+0x2A`, `+0x1C2`, `+0x2E` | `+0x2F` | — | 054, 058, 05C |
| 69 | `0038A3A0` | `+0x2A`, `+0x1C2`, `+0x2E` | **`+0x30`** | — | 054, 058, 05C |
| 70 | `0038A470` | `+0x2E` (three reads) | **none** | — | 054, 058, 05C |
| 71 | `0038A590` | `+0x2A`, `+0x1C2`, `+0x2E` | `+0x2F` | — | 054, 058, 05C |
| 72 | `0038A680` | `+0x2A`, `+0x1C2`, `+0x2E`, **`+0x52`** | `+0x2F` only | — | 054, 058, 05C |
| 73 | `0038A820` | `+0x2A`, `+0x1C2` | `+0x2F` | `+0x10` | 054, 058, 05C |
| 74 | `0038A9D0` | — | — | `+0x10`, `+0x11` | **054, 058** |
| 77 | `0038ABC0` | `+0x2A`, `+0x1C2` | `+0x2F` | `+0x10` | 054, 058, 05C |
| 78 | `0038AD70` | `+0x2A`, `+0x1C2`, `+0x2E` | `+0x2F` | — | 054, 058, 05C |
| 79 | `0038AE50` | `+0x2B`, `+0x1C2`, `+0x2E` | `+0x2F` | — | 054, 058, 05C |

**Slots 70 and 72 were wrong here until 2026-09-11, and FABLE caught it**
(`FABLE-CONTRA-OPUS-PREP7072`). Both are corrected above and both errors were the same one, made in
the paragraph that warned about it.

Registers were bound to roles before the reads were attributed: `0038A590` does `mov rdi, rdx` /
`mov rbx, rcx` and `0038A680` does `mov rsi, rdx` / `mov rbx, rcx`, so `rbx` is the **attacker** in
both. I wrote that sentence, corrected slot 71 with it, and then filled the slot 70 and 72 rows from
an instrument that reports register names -- carrying over `rbx` = defender from `0038AAF0`, where
`mov rbx, rdx` really does make it the defender. **The binding is per function and I checked it per
paragraph.**

**And re-deriving the whole table found a third row of mine wrong, which FABLE had not flagged.**
Because the failure was a method applied unevenly rather than a slip, every row was rebuilt by an
analyser that propagates `rcx`/`rdx`/`r8` through their aliases **per function** instead of reporting
register names. It reproduces FABLE's two corrections exactly, and it also shows **slot 62 reads the
defender at `+0x30`** — `mov rsi, rdx` at `00389DE3`, `movzx eax, byte ptr [rsi + 0x30]` at
`00389F50` — where this table had said it reads no defender at all. That makes `+0x30` a **two**-slot
field, not slot 69's alone.

Verified on the bodies: `0038A470` binds `mov rbx, rcx` at `0038A47A`, so all three `+0x2E` reads
(`0038A476`, `0038A4CD`, `0038A51C`) are the **attacker** and the slot makes **no defender read at
all** -- it stores an immediate `0` to `02AEE05C` at `0038A573` instead. `0038A680` binds `rsi = rdx`
at `0038A694` and `rbx = rcx` at `0038A69E`; every `+0x2A`, `+0x1C2` and `+0x2E` read goes through
`rbx`, and its **only** defender read is `[rsi + 0x2F]` at `0038A7F6`. **Slot 72 is one-sided**, not
two-sided as this section claimed.

`rcx` is not reassigned before `0038A6E2`, so the `+0x52` read is on the same object the other
attacker reads use; per FABLE's census it is the **weapon-slot word** rather than an unnamed attacker
field, which is why §3 now names it as such.

**Limit.** The reads are those of each body in isolation. A member that calls `0020E600` may reach
further through the registry; those calls are named, not followed.

**Claim table added 2026-09-12 (`OPUS-S15-CLAIM-TABLES-SIX`).** The prose and the read-set table
above state the method and its two corrections and are kept; this enumerates the claims so a pilot's
`CONTRACT_MAP` can be derived from them. **Nothing in this family has been executed** (§13), so no
row claims more than static evidence.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the family is reached only through the table at 01EFA5C0, from exactly two call sites | a sweep over **both** `call` and `jmp` through a scale-8 index: 11 indexed indirect transfers image-wide, 3 of them tail jumps, none of the three reaching `0x1DDA5C0` | 1 (static) | PROVEN  **§15a**: confirmed for the FAMILY. The table itself carries **five** references — the two indexed dispatchers plus three flat `call qword [01EFA5C0]` at `00388282`, `00388A63`, `00388ADD`, which reach **slot 0 = `00387F40`, not a member**. Slots 60–79 have exactly the two |
| the two record arguments are BattleStatsRecord, not BattleUnit | every offset the sixteen bodies read is a declared `BattleStatsRecord` field and none exists on `BattleUnit`; published as `BattleUnit` until 2026-09-11 and corrected | 1 (static) | PROVEN |
| the third argument is real and is read by exactly one member | `0038A680` tests `[r8 + 0x1b]` at `0038A6B1` before any call; the other fifteen reassign `r8` before touching it | 1 (static) | PROVEN |
| neither dispatcher bounds the slot | `003859F0`/`003859FF` and `003863C0`/`003863D0` index the table with the recipe's slot and no compare; only the recipe **id** is bounded | 1 (static) | PROVEN |
| the members write only the three scratch words and never through their arguments | every write in all sixteen bodies lands on `02AEE054`, `02AEE058` or `02AEE05C` | 1 (static) | PROVEN |
| **TWO** of the sixteen write only a subset of the three words | slots 61/64/75 (`0038AA90`) write `054` alone and slot 74 (`0038A9D0`) writes `054` and `058`, so a skipped word keeps the previous step's value. **This row said THREE**, while its own evidence named two bodies; corrected 2026-09-12 by measurement, not by re-reading — the differential poisons all three words and calls every member, and exactly these two come back carrying a poison word | 1 (isolated original-code) | PROVEN |
| the reset zeroes all three and runs before each walk | `003849B0` at `00384A29`/`2F`/`35`, with exactly two callers — the same two dispatchers, at `0038585E` and `00386001` | 1 (static) | PROVEN |
| the walk stops as soon as 02AEDFB8 is 1 | `003859AC` and `003863D7` | 1 (static) | PROVEN |
| the slot comes from a recipe's second list, not from a weapon | the recipe pointer table at `01EF96C0` and its two `-1`-terminated lists; cited from the recipe system rather than re-derived here | 1 (static) | HIGH |
| recipes 20-29 differ only in this slot | identical preview lists and resolution lists differing only in the preparation entry, 20→65 … 29→72 | 1 (static) | PROVEN |
| the defender's +0x30 is read by two slots, not one | `00389DD0` binds `mov rsi, rdx` at `00389DE3` and reads `[rsi + 0x30]` at `00389F50`, alongside slot 69 | 1 (static) | PROVEN |
| slot 70 makes no defender read at all | `mov rbx, rcx` at `0038A47A` makes all three `+0x2E` reads the attacker's; the slot stores an immediate `0` at `0038A573` | 1 (static) | PROVEN |
| slot 72 is one-sided | `rsi = rdx` at `0038A694`, `rbx = rcx` at `0038A69E`; its only defender read is `[rsi + 0x2F]` at `0038A7F6` | 1 (static) | PROVEN |
| the read sets are per body in isolation | a member that calls `0020E600` may reach further through the registry; those calls are named, not followed | 1 (static) | PROVEN |
| the sixteen bodies share one template, with six closed forms for the multiplier | `m = (level + statA) * statB` then one of: `m/256 + 1`, `+ 2`, no addend, doubled, `× 1.5 + 1`, or `m / 218`. Every form executed, compared as a BIT PATTERN rather than a decimal | 1 (isolated original-code) | PROVEN |
| the variance gate is 0.01f and is the divisor's ONLY guard | `comiss` against `008F30E4` = `0.00999999977648`; `(int)(gate * 100.0f)` then feeds an unsigned `div` with no further test. Executed at weapon bytes 0, 1, 2, 7, 8 and 0xFF across nine members: below the threshold no draw is taken at all, which the generator's cursor shows | 1 (isolated original-code) | PROVEN |
| the remainder is UNSIGNED, on the raw 32-bit draw | `xor edx, edx` then `div ecx` — `00389F12`/`00389F32` and the same pair at `0038A0AB`/`0038A0CB`, `0038A18D`/`0038A1A9`, `0038A26D`/`0038A289`, `0038A349`/`0038A365`, `0038A419`/`0038A435`, `0038A4EB`/`0038A4F9`, `0038A52C`/`0038A545`, `0038A611`/`0038A62A`, `0038A733`/`0038A751`, `0038A7BD`/`0038A7D9`, `0038A95A`/`0038A97A`, `0038AB69`/`0038AB85`, `0038AD02`/`0038AD22`, `0038ADF1`/`0038AE0D`, `0038AEC9`/`0038AEE5`; never `cdq`/`idiv`. A reconstruction using C's signed `%` fails on 3 of the suite's lines - the draws where the tempered word exceeds 0x7FFFFFFF | 1 (isolated original-code) | PROVEN |
| the authored row address is built in THIRTY-TWO-bit arithmetic | `imul edx, [02AEDFD4]` then `add eax, edx`, both 32-bit, on a 64-bit base. Executed with a stride-times-index product of `0x100000110`: the shipped code reads the byte at `+0x110` and a 64-bit reconstruction addresses `0x130000110` and fails on 12 lines. **No other case in the suite can see this**, which is why one exists for it | 1 (isolated original-code) | PROVEN |
| slot 72's equipment compare is UNSIGNED, and 0x1000 passes whatever the limit is | `0038A6EB jae` against `[02EBF0F8]+4 + 0x1000`, with a SIXTEEN-bit re-test against `0x1000` at `0038A6F4`. Executed at limits above the signed boundary, where a signed compare disagrees on 8 lines | 1 (isolated original-code) | PROVEN |
| two members write an IMMEDIATE ZERO to the defence term rather than leaving it | `0038A0E8` in `00389F80` and `0038A573` in `0038A470`. The same value a fresh frame holds, and a different fact about the code: the poison test distinguishes them from the two that leave the word | 1 (isolated original-code) | PROVEN |
| 0038A470 draws TWICE against one gate | two separate calls through `00379CD0`, one into `054` and one into `058`; the generator's cursor moves by two across the call | 1 (isolated original-code) | PROVEN |
| the family's only shared callee is the MT19937 draw | `00379CD0` is a `jmp` thunk to `00863BF0`, whose cursor is `02EB4230`, state `02EB3870`, lazy self-seed `00866D60` with 5489, twist `00866B90`. **Executed for real on both sides**: the fixture plants one state into the shipped generator and into the RNG pilot's reconstruction, so the draws are compared rather than scripted. Includes a cursor at 0x26E, 0x26F and 0x270 and an unseeded first draw | 1 (isolated original-code) | PROVEN |
| the null-row path computes the same doomed address on both sides | driven with the registry pointer null across all six row-reading members. **The fixture maps a page at address zero so the two are comparable at all; the shipped process has nothing mapped there.** What is established is the arithmetic, NOT that the path survives | 1 (isolated original-code) | PROVEN |
| the SIMD arm of the generator's twist is NOT executed | `00866B96` tests the CPU-feature dword at `01F44858`, whose value in the shipping image is `1`, so the scalar arm runs. The `>= 2` arm is never entered here and nothing about it is claimed | none | UNKNOWN |
| nothing observed at runtime | — see §13 | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every claim survived. Two of them survived *a tool that said otherwise*, and that is the part worth
keeping: both are shapes where a looser instrument returns a confident wrong answer.

### The write census, exhaustive over all sixteen bodies

Every instruction whose destination is memory, in each of the sixteen members, decoded per function
from `functions.tsv` bounds:

| | |
|---|---|
| writes to the three scratch words | as §15's per-slot map says, **including both subset cases** — `0038AA90` (slots 61/64/75) writes **`054` alone**, `0038A9D0` (slot 74) writes **`054` and `058`**, the other fourteen write all three |
| stack-frame register saves (`[rsp+N]`) | **23** — `mov [rsp+8], rbx`, `movaps [rsp+0x20], xmm6` and kin |
| **writes anywhere else** | **0** |

**"Never through their arguments" therefore holds**, and the residue is named rather than filtered:
the only non-scratch destinations in the family are each body's own register-save prologue.

### Trap 1 — `test` is not a write

My first detector counted any instruction with a memory *first operand* as a store, which put
`0038A6B1 test byte ptr [r8 + 0x1B], 2` in the write list. It is a read. Excluding `test`/`cmp`/`bt`
leaves the 23 stack saves and nothing else.

### Trap 2 — `r8` stops being the third argument

§15 says the third argument *"is read by exactly one member"*. A sweep for **any** memory operand
based on `r8` finds **four** bodies — `00389DD0`, `0038A680`, `0038A820`, `0038ABC0` — and would look
like a refutation. It is not: `r8` holds the third argument only until something overwrites it or a
call clobbers it. Under **the contract's own criterion** — the read must happen *before any call*,
with `r8` still live — exactly **one** body qualifies:

```asm
0038A6B1  test byte ptr [r8 + 0x1B], 2      ; 0038A680, slot 72
```

The other three touch `r8` only after it has been reused as scratch. **The claim is right and the
loose reading is wrong**, which is recorded here so the next sweep does not re-discover the four and
call it a defect.

### Trap 3 — the dispatch table has five call sites, and the family has two

§15 says the family *"is reached only through the table at `01EFA5C0`, from exactly two call sites"*.
The table is referenced **five** times in four functions:

| site | form |
|---|---|
| `003859FF` in `BattleFormula_EvaluateTargetPreview` | `call qword [r12 + rax*8 + 0x1DDA5C0]` — indexed |
| `003863D0` in `BattleFormula_ResolveTargetResult` | `call qword [rbx + rax*8 + 0x1DDA5C0]` — indexed |
| `00388282`, `00388A63`, `00388ADD` | `call qword [01EFA5C0]` — **flat, slot 0** |

**Slot 0 holds `00387F40`, which is not one of the sixteen members.** The three flat sites reach a
different entry entirely; the family's slots **60–79** are reached only by the two indexed
dispatchers, and those slots read back exactly as the per-slot map has them (60 → `00389F80`,
61 → `0038AA90`, 62 → `00389DD0`, 79 → `0038AE50`). **The claim is about the family and it holds** —
but its wording invites a reader to check the *table's* call sites and find five.

**Not claimed:** nothing here is a live observation, and no execution was performed.

## 16. Parity plan

Reproduce, in this order of loss-likelihood: the **partial writes** of slots 61/64/75 and 74 — a
reimplementation that zeroes or fills all three changes every program those slots appear in; the
**third argument** of slot 72; the **`ret 0`** for unassigned slots, so an unknown slot leaves the
triple alone rather than faulting; and the **absence of a bound check**, which is a behaviour a
reimplementation should decide about deliberately rather than inherit by accident.

## 17. Related

- `08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md` — the arithmetic
- `08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md` — the two lists and the dispatchers
- `08-Combat-Formula/Step-Table/combat-formula-step-table.md` — the 202 slots
- `08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md` — the scratch census this refines

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

`RNG_MT19937_NextU32_Thunk` (`00379CD0`), the gameplay MT draw this page cites, has callers in three other layers:

- **CoreRuntimeScheduling — SERVICE, with a determinism consequence.** The boot frame modes 0 and 1 (255 B and 219 B)
  each draw once per dispatch and discard the value. The formula rolls therefore start from a stream that boot has
  already advanced ([the generator contract](../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md) §6 note).
- **Rewards_Progression_Economy — CLIENT.** The HP and MP growth functions (178 B and 171 B) draw it for the level-up
  bonus ([what happens when a character levels up](../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)).
- **Status_Periodic_Terminal — CLIENT.** `BattleFormula_AdvanceStatusTimersAndBuildResult` draws it for status timers.

`BattleFormula_ResolveTargetResult` (`00385F60`) is also run by `BattleUnit_RunPeriodicCombatMaintenance`, which makes
it a **CLIENT** edge in **Status_Periodic_Terminal**. The periodic tick calls the same result resolver this family
belongs to ([the periodic tick](../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md)).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Script_VM_Native_Bridge — CLIENT (2 edges).** Two script verb bodies call `RNG_MT19937_NextU32_Thunk` (`00379CD0`): `00354BF0` pops an integer bound `n` from the value stack, draws one word and hands back the high half of `word * n` (a draw in `0..n-1`), and `00355140` hands back a raw draw. Script verbs take draws from the same gameplay stream the preparation members use for variance, so a script's random call advances the stream a later formula roll reads.

**WorldAreaField — CLIENT (2 edges).** The weather bodies `0025ABA0` (the slot-switch picker of the weather contract, which returns the slot to switch to) and `0025ACA0` call `00379CD0`. The weather roll is another consumer of the one gameplay stream; it shares the generator with this family, not any step state.
