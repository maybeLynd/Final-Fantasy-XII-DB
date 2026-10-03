---
contract: read one authored field's permission bits, with a save flag able to replace two of them outright
category: 03-World-Area-Field
scope: family
readiness: DIFFERENTIAL TESTED   # the ALGORITHM, over a PLANTED table; the authored data is unread — see §13
confidence: PROVEN
implements: 03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md
entries: ["00377C20", "00377480", "00377A40", "00377BA0", "003779F0", "00377700", "00377C70", "00313F60", "00320160"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 49 addresses cited - 3 data, 16 entry, 30 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-field-accessors-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the field record accessors

Seven functions read one 3-byte authored record out of `navimapdata.bin` and hand back one bit
region each. They share a prologue instruction for instruction, and they differ in exactly two
places that matter: **what they return when the table is not there, and whether a saved flag can
overrule the authored answer.**

The first contract in `03-World-Area-Field`.

## 1. Purpose

`00377C20` alone is consulted by more distinct subsystems than any other gameplay predicate in this
database. What all seven return on a missing table is therefore not an edge case — it is the
behaviour of most of the game on a path nobody notices.

## 2. Interface

| accessor | entry | field id from | returns |
|---|---|---|---|
| bit 15 | `00377C20` | `003148F0`, the active-or-pending field | `0` or `1` |
| bit 15 | `00377480` | `ecx`, explicit | `0` or `1` |
| bit 14 | `00377A40` | `ecx`, explicit | `0` or `1` |
| bits 12–13 | `00377BA0` | `003148F0` | `0..3`, **save-overridable** |
| bits 0–11 | `003779F0` | `ecx`, explicit | `0..0xFFE`, or **`-1` for none** |
| byte 2, bit 0 | `00377700` | `003148F0` | `0` or `1`, save-gated |
| byte 2, bits 4–6 | `00377C70` | `003148F0` | `0..7` |

### The record's bits, decomposed — `C-11` answered on the encoding axis

Every accessor reads the same two quantities and takes a different part of them. Collected, they
decompose both completely enough to name `C-11`'s remainder:

| quantity | part | taken by | shape |
|---|---|---|---|
| the `u16` at `+8`/`+9` | bits 0–11 | `003779F0` | `and 0xFFF`, `0xFFF` means none |
| | **bits 12–13** | `00377BA0` | `shr 0xC` / `and 3` — a **two-bit** field |
| | **bit 14** | `00377A40` | `shr 0xE` / `and 1` |
| | bit 15 | `00377C20`, `00377480` | `shr 0xF` |
| the byte at `+0xA` | **bit 0** | `00377700` | `not` then `test al, 1` — tested **inverted** |
| | ~~**bits 4–7**~~ **bits 4–6** | `00377C70` | `shr 4` then `and 7` *(corrected 2026-10-02, OPUS: `00377C99 shr eax, 4` / `00377C9C and eax, 7`; bit 7 is never taken)* |

**`C-11` asks for "the meaning of the other 15 bits of the `u16`, and of the third byte".** The
*encoding* is now closed: the `u16` is four fields, not one flag and a remainder, and the third byte
is at least two. **~~Bits 1–3 of the byte are the only part no accessor touches.~~** **Bits 1–3 and bit 7 of the byte are the parts no accessor touches** *(corrected 2026-10-02, OPUS: `00377C70` takes bits 4–6, `00377C9C and eax, 7`; §14's execution note)*.

What this does not give is the **semantics** — what a two-bit field at 12–13 selects, or why bit 0 of
the byte is read inverted. That is authored meaning and is FABLE's; the shapes above are what the
consumers make of the data, which is the half that is mine.

> **The semantics arrived, and they are cited here rather than left a document away**
> (`FABLE-NOTICE-C11-SEMANTICS`, 2026-09-12). A reimplementer reading a shape should not have to
> find a second page to learn what the value means.
>
> - **Bits 12–13 are the field's MP regime.** `002F957E` divides by `3.0`; `002F9234` and `002F93D6`
>   triple; `00303043` compares the raw value. So values **2 and 3** divide periodic MP recovery by
>   three and triple MP damage gain.
> - **Bit 0 of the third byte is folded into the actor-system global `02099DE7`** — `0026A20B` and
>   `00268E29` store `(00377700() == 0)` there, which is why the accessor tests it **inverted**.
>
> Evidence and the consumer list are FABLE's, on the navimapdata page's `C-11` consumers section.
> **Not re-derived here**, and the split stands: the encoding above is proven by this contract's own
> reading, the meanings in this box are cited. `C-11` is narrowed and `FZ-28` is opened in their
> place.

Two thunks carry callers in: `00313F60` (5 bytes) reaches `00377C20`, and `00320160` reaches
`00377BA0`. Microsoft x64 throughout.

## 3. Types

`FieldRecordTable` at `*(void**)0x02ADD100` — **a pointer slot, not the table** — with the record
count at `+0x04` and `FieldRecord`s of 3 bytes from `+0x08`. `PersistentFlagPayload` supplies the
override, at `+0x1062` and `+0x1063`.

## 4. Preconditions · postconditions · invariants

**There are no preconditions.** Every accessor validates everything it uses, and none of them can
fail to return:

1. **the pointer may be null** — `test r8, r8` / `je`, checked by all seven. The check does not make the answer
   neutral everywhere. **`00377700` returns 1 for a null table or an out-of-range id**: its reject path zeroes the
   byte (`00377728 xor dl, dl`), and its own `not` / `test al, 1` turns that into 1. Only the save gate
   `[payload + 0x1062]` bit 0, read by `00314A60`, can force 0 (§10) *(Added 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 304.)*;
2. **the id is bounded unsigned** against the count — `cmp id, [table+4]` / `jae` — which is what
   rejects a negative id even though the id is sign-extended one instruction later (`movsxd`). The implicit-id
   accessors never present a negative id at all. `003148F0` clamps it with `cmovs` (`00314903`), so they read
   **record 0** for a negative saved field id, not "no record" (§7) *(Added 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 304.)*.

Nothing is written. These are pure reads of authored data, and the only state any of them consults
beyond the table is the save payload in §7.

## 5. State

None of their own.

## 6. Relationships

- **Consumers — RE-DERIVED 2026-09-11, and the old numbers did not survive.** ~~`00377C20` has 65
  direct callers plus 47 through the thunk.~~ Measured with `check_caller_claims.py` (`memcpy`
  control: 632 sites), counting **sites and functions separately**, because they are different
  numbers and "65 direct callers" is ~~neither of them~~ the function count without the thunk itself *(corrected 2026-10-02, OPUS: `retool.py callers 00377C20` lists 80 sites in 66 functions, and one of the 66 is the thunk `00313F60`, whose `jmp` is the 80th site; without it, 79 sites in 65 functions)*:

  | entry | direct sites | distinct functions | note |
  |---|---:|---:|---|
  | `00377C20` bit 15 | **79** | ~~**66**~~ **65** | plus one `jmp` from its thunk, whose function makes 66 *(corrected 2026-10-02, OPUS: the 79 sites lie in 65 functions; the thunk `00313F60` is the 66th, `retool.py callers 00377C20`)* |
  | `00313F60` (thunk → `00377C20`) | **67** | **47** | the 47 matches the old figure; ~~the 65 does not match either column~~ the 65 is the direct column without the thunk *(corrected 2026-10-02, OPUS: `retool.py callers 00377C20 00313F60`)* |
  | `003779F0` bits 0–11 | 9 | 9 | |
  | `00377700` byte 2 bit 0 | 6 | 6 | |
  | `00377A40` bit 14 | 5 | 5 | |
  | `00377C70` byte 2 bits 4–6 | 5 | 3 | |
  | `00377480` bit 15, explicit id | **1** | **1** | |
  | `00377BA0` bits 12–13 | **0** | — | **reached ONLY through its thunk** |
  | `00320160` (thunk → `00377BA0`) | 8 | 4 | |

  **Two of these change how the family should be read.** `00377BA0`, the only save-overridable
  accessor, has **no direct caller at all** — every consumer goes through `00320160`, so a census
  that ignores thunks reports the game's one overridable permission as dead code. And `00377480`,
  the explicit-id twin of `00377C20`, has exactly **one** caller against the other's 79: the
  active-field variant is the one the game actually uses.

  The subsystem attributions in the old sentence are unchanged and not re-derived here: `003779F0`
  read by UI and achievements; `00377700` by ActorEntity and Movement; `00377C70` by
  `PartyFocus_SelectAndRequestDefaultActor` and `BattleGroup_RefreshFourActorDefinitions`.
- **`19-Save-Load-Settings` reaches in here**, and §7 is that link.

## 7. State transitions — the save override

`00377BA0` is the only accessor whose answer can come from somewhere other than the table, and the
shape is a **replacement, not a merge**:

```
00377BA4  call 00314AA0            ; is the override enabled?
00377BA9  test eax, eax
00377BAB  je   00377BB6            ; no  -> read the authored bits
00377BB1  jmp  00314AC0            ; yes -> TAIL-JUMP; the table is never touched
```

and both sides of that decision live in the save image:

| | |
|---|---|
| `00314AA0` `SaveFlags_GetPayload1062Bit7` | calls `002EF2B0 SaveImage_GetPersistentPayloadBase`, then `byte [buf + 0x1062] >> 7` — **bit 7 of `PersistentFlagPayload +0x1062`** |
| `00314AC0` `SaveFlags_GetPayload1063Bits4To5` | same base call, then `(byte [buf + 0x1063] >> 4) & 3` — **bits 4–5 of `PersistentFlagPayload +0x1063`** |

> **Named 2026-09-11 after a naming collision I caused.** An earlier revision of this section
> described both wrappers as *"`SaveImage_GetPersistentPayloadBase()` then …"*, and
> `check_consistency.py` reads the first token beside an address as that address's **name** — so
> three wrappers were being named after the function they share. The names above are
> `Field-Record-Table/field-record-table-navimapdata.md`'s, which had them right; `002EF2B0` is
> the shared base getter and the three `00314Axx` functions are its callers, not aliases of it.
> **Describing a function by what it calls reads as naming it by what it calls.**

Which is exactly what the store's `fieldRecordOverrideBits` row already says from the other end:
*bits 4-5 are a two-bit SAVE OVERRIDE for the field record's own bits 12-13.* **The two subsystems
were describing one mechanism and this contract is where they meet.**

### There is a SECOND save gate, and it is the opposite shape — ADDED 2026-09-11

`00377700` also consults the save image, through a third query this contract did not name:

| | |
|---|---|
| `00314A60` `SaveFlags_GetPayload1062Bit0` | same base call, then `byte [buf + 0x1062] & 1` — **bit 0 of the SAME byte as the override enable** |

So **`PersistentFlagPayload +0x1062` carries at least two independent flags**: bit 7 enables the
bits-12-13 replacement, and bit 0 vetoes `00377700`. They were driven independently under execution
and neither affects the other.

**The two gates are not the same mechanism, and §14 asked exactly this.**

| | `00377BA0` | `00377700` |
|---|---|---|
| shape | **replacement** | **veto** |
| when the save says yes | tail-jumps; **the table is never read** | still reads the record |
| what the save can do | supply any of `0..3` | only force the answer to **0** |
| can it force a `1`? | n/a | **no** — a set veto bit always yields 0 |

A reconstruction that generalised either shape to the other would be wrong in a direction ordinary
play would rarely reveal: the merge form agrees with the replacement form on every field whose
authored bits 12–13 happen to be `0`. The differential test plants a record whose authored value is
`3` for exactly that reason, and the merge mutant fails on 51 comparisons.

### And the id source clamps — ADDED 2026-09-11

`003148F0` is `xor ecx,ecx` / `test eax,eax` / `cmovs eax,ecx` over `[payload + 0x1044]`, so a
**negative** saved field id becomes `0`. It reads **record 0**, not "no record". The four accessors
that take their id from this function can therefore never present a negative id to the bound, which
is why the unsigned compare only matters for the three that take `ecx` from a caller.

The consequence a reconstruction must not smooth over: when the flag is set, the authored value is
not consulted, not masked, not blended. The tail-jump means `02ADD100` is never dereferenced on that
path — so a save can produce an answer for a field whose record does not exist.

~~`00377700` is described as save-gated by the referenced page; the gating is in its caller, not in the
accessor, and is not specified here.~~ *Corrected 2026-09-25 (FABLE, Claude Opus 5.5):* the gate **is** inside
the accessor. `00377700` itself calls `00314A60` (`00377733`) and returns 0 when `[payload + 0x1062]` bit 0 is set,
as "There is a SECOND save gate" above already reads.

## 8. Script · resource · event interactions

The whole table is one authored resource — `navimapdata.bin`, magic `NAV\x02`, registered at
`00378B80` — and the pointer at `02ADD100` is where the resource system publishes it. Nothing here
loads or reloads it.

## 9. Determinism

Fully deterministic given the table and the save byte.

## 10. Failure paths and edge conditions

**Every accessor takes the same constant on failure and they do not agree on what it means.** On a
null pointer or an out-of-range id each loads `0xFFF` (or, for the byte-2 pair, a zero byte) and runs
the *same* shift-and-mask it would have run on real data:

| accessor | on failure | |
|---|---|---|
| `00377C20`, `00377480` | `0xFFF >> 15` | **0** — permission denied |
| `00377A40` | `(0xFFF >> 14) & 1` | **0** |
| `00377BA0` | `(0xFFF >> 12) & 3` | **0** |
| `003779F0` | `0xFFF & 0xFFF`, then `cmp 0xFFF` / `cmove -1` | **−1** |
| `00377700` | `xor dl, dl`, then **its own** `not` / `test al,1` | **1**, unless the save vetoes — **CORRECTED 2026-09-11** |
| `00377C70` | `xor dl, dl`, `>> 4 & 7` | **0** |

> ### ⚠ `00377700`'s row said **0** and the branch **not taken**. Both halves were wrong.
>
> ~~`xor dl, dl`, caller does `not` / `test al,1` → **0**, and the guarded branch is **not**
> taken.~~ **Falsified by execution 2026-09-11** (`diff_field_record.py`, the shipped body under
> Unicorn with a planted null pointer).
>
> The `not` / `test` is **inside `00377700`**, not in a caller — `0037772A movzx eax,dl` /
> `0037772D not eax` / `0037772F test al,1` / `00377731 je 0x377746`. So a **zero** byte makes
> `~b2 & 1` **non-zero**, the `je` is **not** taken, and control reaches the save query. The
> accessor's full rule is:
>
> ```
> return 1  iff  (record byte 2, bit 0) == 0   AND   (PersistentFlagPayload +0x1062, bit 0) == 0
> return 0  otherwise
> ```
>
> **A missing table is therefore the most PERMISSIVE input to this accessor, not the least.** The
> failure constant is a zero byte exactly as stated, and a zero byte is the *permitting* value
> because bit 0 is read inverted — which §2's decomposition table records and this table did not
> carry through.
>
> **How it was established.** The contract's own documented behaviour was built as a mutant —
> `if (!record) return 0;` — and the differential test rejects it on **106 comparisons**, while
> the corrected reconstruction passes all 2,982. The falsification therefore has a positive
> control and is not one implementation's opinion of another.
>
> **The summary sentence below moves with it**: one constant, **five** benign zeros, one sentinel,
> and one **permissive 1**.

**`003779F0` is the one to look at twice.** `0xFFF` is not its failure value passed through — it is
an *authored sentinel*. The tail at `00377A23`–`00377A32` is `or eax, 0xffffffff` / `and edx, 0xfff`
/ `cmp edx, 0xfff` / `cmove edx, eax`, so a record that really contains `0xFFF` also returns `−1`.
**A missing table is therefore indistinguishable from an authored "none"** at this accessor, and
distinguishable at every other one only as a zero that could equally be a real zero. No accessor
reports the difference.

~~One constant, six benign zeros and one sentinel.~~ **One constant, five benign zeros, one
sentinel and one permissive `1`.** That is a design decision, and a reconstruction that picked a
single uniform default would move behaviour in **three** directions at once — and in the
`00377700` case it would deny a permission the shipped game grants.

## 11. Observable behaviour

**Two halves, and only one of them is established.** ~~Not established; this is static.~~

**Established 2026-09-11, by calling the shipped accessors** (§13) — the family's own observable
behaviour, given a table and a save payload:

- each accessor returns the bit region §2 assigns it, over records covering every bit pattern that
  matters, including the all-set and all-clear extremes;
- a **missing table** yields the per-accessor constants of §10 — five zeros, `003779F0`'s `−1`, and
  `00377700`'s **`1`**, which is what falsified that table's sixth row;
- an **out-of-range id** is indistinguishable from a missing table at every accessor, including at
  `0x80000000` and `0xFFFFFFFF`, because the bound is unsigned;
- a **negative saved field id** reads record 0 rather than missing, through the `cmovs` in
  `003148F0`;
- with the **override enabled**, `00377BA0` returns the saved two bits and the authored value has no
  influence at all — driven over all four values against a record whose authored bits are `3`, so
  the two behaviours disagree on every case rather than on some;
- with the **veto bit set**, `00377700` returns `0` regardless of the record, and with it clear the
  record's bit 0 decides — the two gates are independent and were driven independently.

**Not established, and it needs the running game:** everything a *player* could see. Whether actions
gated on `00377C20` are refused in a field whose record sets bit 15; whether a save-overridden field
behaves per the save in play, including in a field whose record does not exist; and whether the
null-table window is ever entered at all — which matters more now that §10's correction makes that
window *permissive* for one accessor rather than uniformly denying.

The distinction is the point: calling a function establishes what the function does, and nothing
about when the game calls it.

## 12. Reproduction formula

```c
static FieldRecord *field_record(uint32_t id)          /* the shared prologue */
{
    FieldRecordTable *t = *(FieldRecordTable **)0x02ADD100;
    if (!t) return 0;                                  /* test r8,r8 */
    if (id >= t->recordCount) return 0;                /* UNSIGNED cmp / jae */
    return (FieldRecord *)((char *)t + 8 + (int32_t)id * 3);
}

int field_bit15(void) { FieldRecord *r = field_record(current_field());
                        return (r ? r->w : 0xFFF) >> 15; }

int field_bits12_13(void) {
    if (save_override_enabled())  return save_override_value();   /* TAIL-JUMP, no table read */
    FieldRecord *r = field_record(current_field());
    return ((r ? r->w : 0xFFF) >> 12) & 3;
}

int field_bits0_11(void) {
    FieldRecord *r = field_record(id);
    uint32_t v = (r ? r->w : 0xFFF) & 0xFFF;
    return v == 0xFFF ? -1 : (int)v;                   /* the sentinel, not just a mask */
}
```

`r->w` is the little-endian u16 the code composes from bytes `+0` and `+1`; there is no 16-bit load
anywhere in this family.

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-11)
~~None. No accessor in this family has been executed under
observation.~~ All seven accessors and both thunks have now been executed — the shipped bodies, at
their real virtual addresses, under Unicorn, **with no stubs anywhere**.

**Instrument:** [`Reconstruction/Tests/Differential/diff_field_record.py`](../../../Reconstruction/Tests/Differential/diff_field_record.py)
against [`Reconstruction/Game/World/field_record.c`](../../../Reconstruction/Game/World/field_record.c),
on `FFXII_TZA.exe` `73461D08…`.

**Why no stubs were needed**, which is the reason this family was reachable at all: the id source
and all three save queries funnel through `002EF2B0` → `002EF640`, and `002EF640` is
`lea rax, [02164280]; ret`. The persistent payload base is therefore `02164280 + 0x200`, a fixed
image address, so the saved field id, the override enable, the override value and the veto bit are
four **plantable bytes** rather than anything a stub has to invent.

**Result: 426 cases — 26 chosen for their edges, 400 random — 2,982 comparisons, 0 mismatches.**
249 of the 426 reach a real record and 399 produce a non-trivial answer, so the green result is not
mostly two implementations agreeing on a failure.

| §13's own checks | outcome |
|---|---|
| 1. the override's precedence | **ANSWERED, and more strongly than proposed.** Driven over all four override values against a record whose authored bits 12–13 are `3`, so replacement and merge disagree on *every* case rather than on some. The authored value has no influence at all. A merge-shaped reconstruction fails on 51 comparisons |
| 2. the null-table window | **ANSWERED for what the accessors do, and it falsified §10.** Every accessor was run against a null pointer slot. `00377700` returns **1**, not 0 — see §10's correction box. **Whether `02ADD100` is ever null in play is NOT answered and cannot be here**; that half stays live-only, below |

**Also executed:** the unsigned bound (`0x80000000` and `0xFFFFFFFF` rejected exactly like an id one
past the end); the `cmovs` clamp (a negative saved id reads record 0); the `0xFFF` sentinel being
indistinguishable from a missing table; and both save gates driven independently, which is how bit 0
of `+0x1062` was found.

**Claims about the bytes, re-derived on every run:** all six table-reading accessors share the
prologue shape `mov test je cmp jae movsxd`; six unsigned `jae` bounds checks and **zero** signed
branches among them; both thunks confirmed to jump to the entries §2 names.

**The harness was shown to have teeth.** Three deliberately wrong reconstructions were run: the
contract's own §10 behaviour (106 mismatches), a merged rather than replacing override (51), and a
**signed** bound — which does not produce a wrong answer but **crashes the driver** with an access
violation on id `0x80000000`, because the sign-extended index reads far outside the table. That is
worth stating plainly: in this family the unsigned compare is not a correctness nicety, it is the
only thing between a hostile id and an out-of-bounds read.

### What is still owed, and it is live-only

**Is `02ADD100` ever null while gameplay is running?** §10 describes a window; nothing here shows
that any shipped path enters it. It may be a boot-order guard no consumer reaches. One breakpoint on
`00377C5F` settles it — and the answer matters in both directions now, because the window is *not*
the benign all-zeros the contract described: it is a state in which `00377700` grants a permission.

Queued, not requested of an absent agent; the live-automation pause stands.

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**41 generated points: 39 KILLED · 1 SURVIVED · 1 EQUIVALENT · 0 NO_BUILD · 0 TIMEOUT · 0 INVALID. Verdict `FAIL`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/field_record` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

The single survivor is **kind A, provably equivalent**: `g_saved_field_id < 0 ? 0 : g_saved_field_id` mutated to `< 1` differs only at 0, where both return 0.

## 14. Unresolved

- ~~What the bit regions mean. The referenced page carries what is known; this contract deliberately~~
  ~~adds nothing to it.~~ *(answered: the semantics are cited in §2, "The semantics arrived", 2026-09-12; 2026-10-02, OPUS)*
- ~~Whether `00377700`'s caller-side save gate has the same replacement shape as `00377BA0`'s.~~
  **CLOSED 2026-09-11 — it does not, and the gate is not caller-side.** It is inside `00377700`,
  through `00314A60`, and it is a **veto** rather than a replacement: the record is read either
  way, and the save bit can only force a `0`. See §7's comparison table. Established by executing
  both accessors over both gate values against records with the relevant bits set and clear.
- ~~Whether the two override helpers read the same save byte.~~ **CLOSED — they do not.** The
  bits-12-13 pair reads `+0x1062` bit 7 and `+0x1063` bits 4–5; the veto reads `+0x1062` **bit 0**.
  One byte, two independent flags, driven independently under execution.
- The four bytes at the table's `+0x00`, left undeclared — see the type store. ~~**Still open**~~ *(answered: the magic `'N''A''V'` `0x02` — field-record-table-navimapdata.md's file layout and this contract's own table row; 2026-10-02, OPUS)*, and
  the harness plants zeros there; nothing in the family reads them, which is consistent with the
  store's silence but does not identify them.
- **NEW.** Bits 1–3 of the record's third byte. §2's decomposition shows no accessor touches them,
  and this run confirms it from the other side: every third-byte value in the case set was driven
  and only bits 0 and 4–6 ever changed an answer. **Bit 7 of that byte is also dead** — `00377C70`
  does `shr 4` then `and 7`, so it takes three bits, not four.
- **NEW, and it is the one that matters for a reconstruction.** Whether the null-table window is
  ever entered in play — now a live question with a consequence, because §10's correction makes
  that window *permissive* for `00377700` rather than uniformly denying.

## 15. Evidence

From the shipping image (`73461D08…`) by two methods: disassembly, and **execution of the shipped
bodies** under Unicorn against an independent reconstruction, with no stubs.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the shared prologue is identical in all seven | re-derived on every harness run: six table-reading accessors, one normalised shape `mov test je cmp jae movsxd`, checked per accessor and never assumed from the first. Entries `00377C20`, `00377480`, `00377A40`, `00377BA0`, `003779F0`, `00377700`, `00377C70` | 1 | PROVEN |
| the bound is an UNSIGNED compare against the count | six `jae` — `00377C39`, `00377490`, `00377A50`, `00377A00`, `00377718`, `00377C88` — and **zero** signed branches in the six bodies; **executed** with ids `0x80000000` and `0xFFFFFFFF`, both rejected exactly like an id one past the end. A signed-bound mutant does not merely answer wrongly — it reads out of bounds and **crashes**. `00377BA0` carries the same bound at `00377BCB` on its table path, after the save-override consult | 1 | PROVEN |
| the record is three bytes and the u16 is composed, not loaded | two `movzx` and a `shl 8` in every u16-reading accessor — `00377C42`/`00377C50`, `00377499`/`003774A7`, `00377A59`/`00377A67`, `00377BD4`/`00377BE2`, `00377A09`/`00377A17` — no 16-bit load in the family; `00377700` and `00377C70` read byte `+0x0A` directly and compose no u16. **Executed** over records planted at a 3-byte stride, which every answer depends on | 1 | PROVEN |
| the failure constants differ per accessor | `mov edx, 0xfff` against `xor dl, dl` in the two halves; **executed** against a null pointer slot, all seven compared at once — **and this is what falsified §10's row for `00377700`**, with the old behaviour built as a mutant and rejected on 106 comparisons | 1 | PROVEN |
| `003779F0`'s `0xFFF` is an authored sentinel, not only a failure value | the tail at `00377A23`–`00377A32`; **executed** with a record containing `0xFFF` beside a null table — both return `−1`, which is §10's indistinguishability | 1 | PROVEN |
| the save override on bits 12–13 REPLACES rather than merges | the tail-jump at `00377BB1`; **executed** over all four override values against a record whose authored bits 12–13 are `3`, so the two shapes disagree on every case. The merge mutant fails on 51 | 1 | PROVEN |
| who consumes each accessor | a caller census, **re-derived 2026-09-11** with a `memcpy` control: `00377C20` at 79 sites in 66 functions, its thunk at 67 in 47, and `00377BA0` reached **only** through its thunk. See §6 — the earlier "65 direct callers" matched neither column. **Not executed**, and a census is not an execution | 1 | PROVEN |

The one thing a reading of a single accessor would have got wrong is `003779F0`'s `−1`: its failure
constant is visible at `00377A1E mov edx, 0xfff`, and only the tail twenty instructions later shows
that `0xFFF` is a sentinel rather than a value.

**And the one thing reading every accessor still got wrong** is `00377700`'s failure value. The
family was read end to end, the inversion was noticed and recorded in §2, and §10's row still
concluded `0` — because the reader who wrote the failure table was answering *"what constant is
substituted"* and the answer to *"what does the function return"* is the opposite. **Running it was
the only thing that caught that**, and it is the clearest argument in this contract for why the
evidence classes are kept separate.

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

**Re-derived from the bytes, and this document already had all of it.** `00377C39` is `jae` —
unsigned, as §15 says. The record stride is **three bytes**, visible in the addressing rather than
stated: `00377C3E lea rax, [r8 + rcx*2]` then `[rcx + rax + 8]` is `r8 + 3·index + 8`. The `u16` is
**composed**, `00377C42`/`00377C4B`/`00377C50 shl edx, 8`/`00377C53 add edx, ecx`, then
`00377C55 shr edx, 0xF`. And the failure path really is `0xFFF >> 15` — §10's table has it, with the
right value.

### What this pass adds: which permission, and how far it reaches

§10 calls the failure value **"permission denied"** and stops there, correctly — a local document
should not guess what a bit governs. But two facts settled elsewhere today name it:

1. **`00377C20` is the override in the HP write's downed-combatant predicate.**
   [`CONTRACT-hp-write-and-lethal-transition`](../08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md)
   §15a shows `00300621`–`00300635` and `0030152B`–`0030153F` running the *same five instructions* —
   `(unit[+0x64] | unit[+0x3C]) & 0x80000003`, then `call 0x377C20`, then **bail when it returns
   zero**. So *the active field record's bit 15* is what decides whether a downed combatant is still
   actionable and still harmable.
2. **110 distinct functions across 16 subsystems reach it**, by two routes with no overlap: 65
   directly and 47 through the 5-byte thunk `00313F60`. (§6's own census counts *call sites* and
   gets 79/66 and 67/47; these are the same population counted differently, and ~~three functions use~~
   ~~both routes~~ two functions use both routes, `00253C70` and `003266C0` *(corrected 2026-10-02, OPUS: `retool.py callers 00377C20 00313F60`; 65 + 47 − 2 = 110)*.)

> **Therefore: with no field record table, the override denies at every one of those sites.** §10
> already says the failure value is `0`; what it could not say is that `0` means *bail* in the guard
> that decides whether damage lands. **A local "permission denied" is a global refusal**, and the two
> halves of that sentence live in different contracts.

**The claims needed nothing.** Like
[the gameplay generators](../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md), this document
has already been corrected by its own pilot — §10's `00377700` row was falsified by execution on
2026-09-11 and carries the old text struck through — and an independent re-derivation only confirms.

**Mechanical:** no body-size drift; banned-evidence sweep clean; all sixteen cited functions resolve.

## 16. Parity plan

Reproduce: the unsigned bound on a sign-extended id, the per-accessor failure defaults exactly as
tabulated, the `0xFFF` sentinel at `003779F0`, and the override's tail-jump precedence.

**Done, at the algorithm level** — see §13. Per-dimension verdicts are declared by the harness and
generated into [`PARITY-STATUS.md`](../_index/PARITY-STATUS.md): `CALCULATION`, `EDGE-CASE` and
`FULL-SUBSYSTEM` covered — the last because all seven accessors and both thunks run, which is every
entry point this contract declares; `INTEGRATION` not covered, because the table is **planted** and
nothing here reads `navimapdata.bin`; `STRUCTURAL` and `STATE-TRANSITION` are `N/A` because nothing
in this family writes anything.

**Four things a reimplementer must take from this contract that the old plan did not name:**

1. **`00377700` returns `1` when there is no record**, not `0`. Its bit is read inverted.
2. **The two save gates are different mechanisms.** Replacement for bits 12–13; veto for byte 2
   bit 0. They are not interchangeable and they read different bits of different bytes.
3. **`+0x1062` holds two flags.** Bit 7 and bit 0, independent.
4. **The unsigned bound is load-bearing, not stylistic.** Getting it signed does not produce a
   wrong permission; it produces an out-of-bounds read. A reimplementation in a language with
   signed-by-default integers must be explicit here.

## 17. Related

- `03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md` — the table, the
  resource and the bit inventory.
- `_types` — `FieldRecordTable`, `FieldRecord`, `PersistentFlagPayload +0x1062` and `+0x1063`.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

The two accessors this contract specifies are shared services. Their callers are the crossings, and none of them
changes what the accessors return.

- **Presentation — CLIENT.** The action-permission bit (`00377C20`) is read by:
  - `AddMotion_ApplyBonePose`;
  - `BattleUnit_ComputePresentationSuppression…`;
  - `BattleUnit_BroadcastPartyCombatTargetRel…`;
  - `PartyCombat_UpdateStanceState`.

  The field id (`003148F0`) is read by two Presentation-filed bodies of about 4.8 KB each.
- **Items_Equipment_Shops_License — CLIENT.** `Inventory_QueryOwnedCountIncludingReservedActionItems` and
  `Equipment_UnequipEncodedItemFromActiveRoster` read the permission bit. A field that forbids actions therefore also
  shapes the item count and the unequip path.
- **Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot` reads the permission bit.
- **Spawn_Encounter_Lifecycle — CLIENT.**
  - `SpawnLifecycle_CheckAndRetireByNativeRange` and `Spawn_ValidateCandidateDistanceToPlayers` read the permission bit
    through its 5-byte thunk `00313F60`.
  - `SpawnKeep_RotatePersistenceBanksForAreaTransition` reads the field id.
- **Audio — CLIENT, not read.** A 335-byte Audio-filed body reads the field id and also calls
  `SaveImage_GetPersistentPayloadBase` (`002EF2B0`), so it combines the current field with persistent save state. The
  body was read only to its first branch, and what it selects is open.
- **ActorEntity - CLIENT and SERVICE (22 edges).** `002EF2B0` is also called by bodies filed to ActorEntity: `0025D9E0`, `002628B0`, `0026C8C0`; `0022A0B0` reaches bodies filed to ActorEntity: `002368D0` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (3 edges).** `0022A0B0`, `0036F4D0` are also called by bodies filed to core runtime: `0017D4C0`, `0022A0B0`; `0022A0B0` reaches bodies filed to core runtime: `0022BDF0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT (6 edges).** `00313F60`, `00377C20` are also called by bodies filed to Gameplay: `003176E0` (Combat), `003257D0` (CombatAction), `00307D10` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (3 edges).** `00313F60`, `00377C20` are also called by bodies filed to input: `00253C70`; `0022A0B0` reaches bodies filed to input: `0035B270` - shared machinery across the layer boundary, no shared ownership.
- **InputGameplay - CLIENT (1 edge).** `00377C20` is also called by bodies filed to InputGameplay: `00313A00` (FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation) - shared machinery across the layer boundary, no shared ownership.
- **Movement - SERVICE (35 edges).** `0026E760` reaches bodies filed to movement: `0026E640`, `0026E960`, `00322220` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (4 edges).** `00313F60`, `00377C20`, `00377C70` are also called by bodies filed to party: `0023B040`, `0031AC00`, `00304180` - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT (2 edges).** `003148F0`, `003779F0` are also called by bodies filed to PlatformOnlineAchievements: `003160C0` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (1 edge).** `0022A0B0` reaches bodies filed to random selection: `00379CF0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (5 edges).** `0022A0B0` reaches bodies filed to resource: `00259DF0`, `002DF9A0`, `0032EAE0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (7 edges).** `003148F0`, `00314A60`, `00377C20` are also called by bodies filed to script VM / native bridge: `0033F310`, `00357450`, `00350FD0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (5 edges).** `00313F60`, `00377C20` are also called by bodies filed to status/periodic terminal: `00320450`, `00329A20`, `0030E360` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - CLIENT (12 edges).** `002EF2B0` is also called by bodies filed to story/event: `0032A8A0`, `0032A930`, `0032A9A0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (10 edges).** `00313F60`, `003148F0` are also called by bodies filed to UI: `0031EB20`, `00322A80` (BattleMenu), `0029C530` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — CLIENT.** `BattleStats_ModifyHPAndProcessLethalState` and a 681-byte formula body call field-record accessors this contract covers.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleEnmity_WriteAllCombatantIds`, owned by that layer, calls `00313F60` on this page. That caller is the all-ids write over the same byte table, taking its value and its mode from the two arguments; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## The `00320160` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`00320160` is the 5-byte thunk to `00377BA0` this contract already
isolates. `00377BA0` (102 B): `003148F0` resolves the record
(`00377BB6`), `[02ADD100]` supplies the bound `dword[r8+4]`
(`00377BBB`/`00377BC7`), `byte[rcx+rax+9]` and `byte[rcx+rax+8]` are
~~the compared kind bytes~~ the two bytes of the flags `u16`, combined by `00377BE2 shl edx, 8` / `00377BE5 add` (`00377BD4`/`00377BDD`), ~~and the value is~~
~~masked to `0xFFF` (`00377BF4`)~~ and the success path has no `0xFFF` mask: `00377BF4` is the missing-table path's failure constant *(corrected 2026-10-02, OPUS: `00377BE7 shr edx, 0xC` / `00377BEA and edx, 3` / `00377BF3 ret`)* — matching the documented `shr 0xC /
and 3` two-bit read.

| member | role | interior |
| --- | --- | --- |
| `00377BA0` (102 B) | the save-overridable bits-12–13 accessor — member call `00314AA0` (`00377BA4`), member tail `00314AC0` (`00377BB1`) | [`00377BC7`](../_index/ADDRESS-INDEX.md) |
| `00314AA0` (24 B) | field-record byte getter A — `002EF2B0` → `byte[rax+0x1062]` (`00314AA9`) | [`00314AA9`](../_index/ADDRESS-INDEX.md) |
| `00314AC0` (27 B) | field-record byte getter B — `002EF2B0` → `byte[rax+0x1063]` (`00314AC9`) | [`00314AC9`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002EF2B0`, `003148F0`. The two
getters differ only in the `+0x1062`/`+0x1063` byte they read off the
`002EF2B0` record — consistent with the accessor's save-override
fallback pair.

## SWE2-EC7-21 update (2026-09-18) — `003ECF70` stride-walking record iterator

`003ECF70` (84 B) is the `02EBB7D0` static descriptor init the field-record
readers publish: ten `[rip]` stores fill the block — `+0x00` = `-1`,
`+0x10`/`+0x20`/`+0x34` = 0, `+0x14` = `0xA`, `+0x18`/`+0x2C` = `0x64`,
`+0x28` = `0xA`, `+0x30` = `-1` — the default record the `0026Exxx` map-pack
reader cluster seeds against. Interior anchor `003ECF72` (the first `[rip]`
store). Callers `0026E760`/`0026E7D0`/`0026EAC0`/`0026EAF0`/`0036F4D0` — the
`0026Exxx` field-record reader cluster.

**CoreRuntimeScheduling — CLIENT (SWE2-EC7 2026-09-18, 1 edge).** `0022A0B0`,
owned by that layer, calls `0036F4D0` — one of the `003ECF70` callers
this section names. The scheduling layer drives the same field-record scan; the
crossing is that the layer consults this contract's accessor, not that this page
owns anything in that layer.

## SWE2-EC7-22 update (2026-09-18) — `003EC860` guarded callback invoker

`003EC860` (50 B) is the guarded invoker the `0026Exxx` field-record readers
share: `rbx = rcx`, `rcx = [rcx]` object, `rdx` non-null -> `call rdx` with
the stored object, `[rbx]` reload on exit — the callback hop the map-pack
iterator arms install. Interior anchor `003EC876` (the `call rdx`). Callers
`0026E760`/`0026E7D0`/`0026EAC0`/`0026EAF0`/`00467B20` — the same
field-record reader cluster as `003ECF70`.
