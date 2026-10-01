---
system: How a script changes how the party looks — LOD, shadows, and taking hits
category: 01-Script-VM-Native-Bridge
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS) — the visible-membership question answered 2026-09-30 (RC-18: map 1 is the engine's own follower source) (SWE2-CONTRACT); 002E5C90 (the position re-place through the transform node) and 002E8CE0 (the LOD refresh) read 2026-09-18
owner_layer: Script_VM_Native_Bridge — from the ledger, not inferred from callers
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 46 addresses cited - 4 data, 25 entry, 17 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-30
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-party-appearance-pass-1 - the family argument reproduces in full: all seven body sizes, the four 187-byte handlers differing by EXACTLY ONE ADDRESS in their call sets, the four setters, partyusecharhit's late argument read, both wrappers' six instructions at their published addresses, the 53-byte setter, the two 8- and 11-byte collector adapters, and 0026AD60's bit pair instruction-exact; CORRECTED: the enumeration denominator is 63 verbs containing 'party' (16 begin with it), not 49 - the conclusion is unaffected and stronger, since the wider net still closes on the same four
  crossref_clean: false
  reopened_count: 0
---

# How a script changes how the party looks — LOD, shadows, and taking hits

## 1. What the player sees

Walk into a town and your two followers trail behind you. Step into a cutscene and they are gone —
or they are still there, but flattened, or their shadows have vanished, or they no longer flinch
when something clips them.

None of that is the engine deciding. **A zone script asked for it, one setting at a time, for the
whole party at once.** The same handful of script commands appear over and over across the game's
maps: *drop everybody's detail*, *turn the party's shadows off*, *stop the party reacting to hits*,
*put the projected shadow back*. They exist because a scene author needs the party to stop looking
like it is wandering around loose in the middle of a staged moment — and because a map with a big
view needs to spend its rendering budget on the view rather than on three characters standing behind
the camera.

The important thing for a modder: **these commands do not target a character.** They take one value
and apply it to *every* party member the game currently considers present. There is no per-character
form of them in this family. If a script wants one character different from the others, this is not
the tool it reaches for.

## 2. The family

Seven script commands sit in one consecutive block of the dispatch table. **Four are literally the
same 187-byte function with one call swapped, two are argument-free wrappers around a third, and one
is the same shape doing three things per member instead of one.** All seven are read.

| Call id | Verb | Handler | Body | What it sets |
|---|---|---|---:|---|
| `040D` | `partyusemapid` | `0033FD60` | 312 B | a mutually-exclusive **bit pair** in the actor's flags byte, then a re-place |
| `040E` | `partyusecharhit` | `00340700` | 187 B | whether the member reacts to being hit |
| `040F` | `partysetlod` | `00341190` | 187 B | the member's level-of-detail index |
| `0410` | `partyshowshadow` | `00341B90` | 187 B | the member's blob shadow on/off |
| `0411` | `partyshowshadow_411` | `00342360` | 82 B | **pushes `1`** and tail-jumps to `0410` |
| `0412` | `partyhideshadow` | `00342830` | 79 B | **pushes `0`** and tail-jumps to `0410` |
| `0413` | `setpartyprojectionshadow` | `00342B30` | 187 B | the member's projected shadow mode |

**The four 187-byte handlers are members of one family, proven rather than assumed.** Each was
disassembled and its call targets compared: all four call the same argument reader, the same two
collectors and the same stack-cookie check, and differ **only** in which per-member setter they
invoke.

| Handler | argument | collector A | collector B | **per-member setter** | cookie |
|---|---|---|---|---|---|
| `00340700` `partyusecharhit` | `00267E10` | `0031B670` | `0031B680` | **`0026A430`** | `00808C40` |
| `00341190` `partysetlod` | `00267E10` | `0031B670` | `0031B680` | **`002EC680`** | `00808C40` |
| `00341B90` `partyshowshadow` | `00267E10` | `0031B670` | `0031B680` | **`002ECD80`** | `00808C40` |
| `00342B30` `setpartyprojectionshadow` | `00267E10` | `0031B670` | `0031B680` | **`002E8730`** | `00808C40` |

*(Enumeration method: every verb whose name contains `party` was taken from the dispatch table —
**63** of them, ~~49~~ (corrected §8; 16 *begin* with `party`, and 49 is neither) — and the four
sharing a body size of exactly 187 bytes were compared instruction by instruction. `partyusecharhit` reads its argument after the collectors rather than before; the
instruction set is otherwise identical.)*

### The shape, in full

Written out as the four handlers execute it:

```c
void party_setting_verb(/* ... */ VMValueStack *stack)
{
    int32_t value = VMValueStack_PopInt32CoerceFloat32(stack);   /* 00267E10 */

    void *group_a[4];  int n_a = party_collect(group_a, 4, /*selector*/ 0);  /* 0031B670 */
    void *group_b[4];  int n_b = party_collect(group_b, 4, /*selector*/ 1);  /* 0031B680 */

    for (int i = 0; i < n_a; i++)
        if (group_a[i]) setter(group_a[i], value);
    for (int i = 0; i < n_b; i++)
        if (group_b[i]) setter(group_b[i], value);
}
```

**One value, two groups of up to four, the same setter for both.** The verbs never treat the two
groups differently — the split is inherited from the collector, not chosen here.

### The two wrappers: three verbs, one behaviour

`0411` and `0412` do not implement anything. Each pushes a constant onto the value stack and
tail-jumps into `partyshowshadow`, which then pops it as its argument:

```text
00342360  mov edx, 1              ; partyshowshadow_411
00342388  call 00267F90           ; VMValueStack_PushInt32
003423AD  jmp  00341B90           ; -> partyshowshadow

00342830  xor edx, edx            ; partyhideshadow
00342855  call 00267F90           ; VMValueStack_PushInt32
0034287A  jmp  00341B90           ; -> partyshowshadow
```

So a script may write `partyshowshadow <value>`, or use the argument-free `partyshowshadow_411` /
`partyhideshadow`. **All three end in the same 53-byte setter**, and `0410` with a value of `1` is
byte-for-byte the same behaviour as `0411`. Both wrappers save and restore `rcx`/`rdx`/`r8`/`r9`
around the push, so the tail-jump receives the original four arguments untouched.

### `partyusemapid` — the same shape, three calls per member

`040D` is the family shape (both collectors, the same argument reader, the same cookie) with a
three-call body per member instead of one:

```c
for each member m:
    FUN_0026AD60(m, value);                     /* the flag pair, below   */
    float p[3];
    Actor_GetWorldPosition(m, &p[2], &p[1], &p[0]);   /* 00265020         */
    FUN_002E5DF0(m, p[0], p[1], p[2]);          /* the same values back   */
```

**The position is read and written back unchanged** — the three floats are not touched between the
call that produces them and the call that consumes them. This is a *re-place at the current
position*, which is what you do when a flag change means the actor must be re-resolved against the
world rather than moved.

The name is misleading, and the bytes say so. `0026AD60` sets no id:

```c
uint8_t b = (value != 0);
*((uint8_t *)m + 0x08) &= 0xF9;                     /* clear bits 1 and 2 */
*((uint8_t *)m + 0x08) |= (uint8_t)((b << 1) | ((!b) << 2));
```

**Bit 1 and bit 2 of `m[+0x08]` are a mutually-exclusive pair** — exactly one is set, chosen by the
argument. It is a two-way switch written as two bits, not a flag and not an identifier.

That byte is shared: `partyusecharhit` writes **bit 3** of the same `m[+0x08]` (§4). So `+0x08` is a
flags byte with at least three of its eight bits driven by this verb family alone.

## 3. What counts as "the party"

`0031B670` and `0031B680` are 8- and 11-byte adapters. Both tail-jump to the same collector at
`0031B5A0`, one with the selector `0` and the other with `1`:

```text
0031B670   xor r8d, r8d      ; selector 0
0031B673   jmp 0031B5A0

0031B680   mov r8d, 1        ; selector 1
0031B686   jmp 0031B5A0
```

The collector walks **exactly four slots** — `cmp ebx, 4` is the loop bound, and it is a constant,
not a variable. For each slot:

```c
int party_collect(void **out, int capacity, int selector)
{
    int written = 0, w = 0;
    for (int slot = 0; slot < 4; slot++) {
        if (w >= capacity) break;

        uint8_t id;
        if (BattleEncodedId_IsValidForClass(0x17, slot, 0))          /* 00322C50 */
            id = *((uint8_t *)*(void **)0x02EBF190 + 0x5A5A + 2 * slot);
        else
            id = 0xFF;                                               /* empty slot */

        void *unit = BattleUnit_FindByDefinitionSelector(id);        /* 002367A0 */
        if (!unit)                       continue;
        if (!(*(uint8_t *)unit & 0x10))  continue;                   /* +0x00 bit 4 */

        void *rec = *(void **)((char *)unit + 0x698);
        if (!rec)                        continue;
        if (*((uint8_t *)rec + 5) != 0)  continue;                   /* +0x05 must be 0 */

        int in_range = ((uint8_t)(*((uint8_t *)rec + 4) - 7) <= 0x12); /* +0x04 in 7..25 */
        if (in_range != selector)        continue;                   /* THE SPLIT */

        out[w++] = *(void **)((char *)unit + 0x10);                  /* NOT the unit itself */
        written++;
    }
    return written;
}
```

### The table is already documented, and it is not the one you would guess

`0x5A5A` is not a fresh discovery. [The five parallel slot
maps](../../11-Party/the-five-parallel-slot-maps.md) established that `02EBF190` carries **five**
arrays exactly `0x12` apart — `0x5A48`, `0x5A5A`, `0x5A6C`, `0x5A7E`, `0x5A90` — each **nine**
two-byte slots, all validated by the same class-`0x17` check. [Active party, reserve, and the moment
the leader changes](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) §2b
then named three of them by censusing what asks for them:

| map | base | what it is |
|---:|---|---|
| 0 | `0x5A48` | the active roster — the only one the initialiser fills |
| **1** | **`0x5A5A`** | **the combat-processing set** — who earns and who is serviced each tick |
| 3 | `0x5A7E` | the general gameplay map — *"a `Party` function, the script-VM bridge"* |

**These verbs read map 1, not map 3.** That is worth stating because map 3 is the one §2b names the
script-VM bridge as passing — so the party-presentation family is an exception inside its own
subsystem: it dresses the characters that **combat** is currently servicing, not the ones general
gameplay addresses.

It is also invisible to that census. §2b counted callers of
`BattleSlotMap_ResolveMappedBattleSlot`; **this collector never calls the resolver** — it computes
`[02EBF190] + 0x5A5A + 2*slot` inline. It is therefore one of the 60 reads found by the separate
displacement census in that document, and not one of the 31 resolver sites. A consumer that reads
the displacement directly cannot be found by asking who called the accessor.

Three facts a reimplementation must not get wrong:

1. **Four slots of the nine.** The array has **nine** entries; this collector's loop bound is the
   immediate `4`, so it reads **slots 0-3 only** and never looks at 4-8. Stride is 2 bytes and only
   the low byte is read. A slot whose `BattleEncodedId_IsValidForClass(0x17, slot, 0)` is false is
   given id `0xFF` — the same empty-slot sentinel §2 of the party document found both of its
   functions testing.
2. **The split is a range test on one byte.** `rec[+0x04]` is compared as
   `(uint8_t)(rec[+4] - 7) <= 0x12` — that is, **`rec[+0x04]` between 7 and 25 inclusive**, 19
   values. Selector `1` takes those; selector `0` takes everything else. Both groups get the same
   treatment from every verb in this family, so a reimplementation that merged them would produce
   identical output **for these verbs** — and would break the moment a verb used one group only.
3. **The object handed to the setter is `unit[+0x10]`, not the unit.** Every field offset in §4 is
   relative to *that* object.

## 4. The four setters, with their exact writes

### `partysetlod` → `002EC680` (26 B)

```c
if (!a) return;
void *pres = *(void **)((char *)a + 0xC0);          /* the presentation object */
if (!pres) return;
*((uint8_t *)pres + 0x13) = (uint8_t)value;         /* the LOD index, a whole byte */
FUN_002e8ce0(pres);                                 /* 002E8CE0, 309 B - refresh */
```

**The LOD is a byte, not a flag.** The verb's argument is written whole to `pres[+0x13]`; nothing
clamps it in this function.

### `partyshowshadow` → `002ECD80` (53 B)

```c
if (*((uint8_t *)a + 0x18) == 1) return;            /* gate 1 */
if ((*((uint8_t *)a + 0x03) & 0xE0) != 0x60) return; /* gate 2: top three bits == 0b011 */
void *pres = *(void **)((char *)a + 0xC0);
if (!pres) return;
*((uint8_t *)pres + 0x151) &= ~0x08;
*((uint8_t *)pres + 0x151) |= (uint8_t)((value & 1) << 3);
Actor_RefreshPresentationVisibility(pres);          /* 002E8FD0 */
```

**Two gates that can silently drop a member**: `a[+0x18] == 1` skips it entirely, and
`(a[+0x03] & 0xE0)` must equal exactly `0x60`. Only the **low bit** of the argument is used.

### `setpartyprojectionshadow` → `002E8730` (192 B)

This one does not touch the presentation object's own bytes. It indexes a record table:

```c
void *pres = *(void **)((char *)a + 0xC0);
if (!pres) return;
if (*(int32_t *)pres == -1) return;
int16_t idx = *(int16_t *)pres;
if (idx == -1) return;
char *e = *(char **)0x022C6F28 + (int64_t)idx * 0x740;   /* 0x740-byte records */
if (*(int32_t *)(e + 0x284) == 0) return;

if (value) {                                  /* ON  */
    *(uint32_t *)(e + 0x304) &= ~0x2000u;
    *(uint32_t *)(e + 0x304) |=  0x1000u;
} else {                                      /* OFF */
    *(uint32_t *)(e + 0x304) &= ~0x3000u;     /* clears BOTH bits */
}
*(uint32_t *)(e + 0x290) |= 0x400000u;        /* set either way */
```

**`e[+0x304]` bits `0x1000` and `0x2000` are a two-bit field, not two flags.** The verb writes `01`
for on and `00` for off, and never writes `10` or `11` — so a third and fourth state exist that this
verb cannot reach. `e[+0x290] |= 0x400000` is set on **both** paths, which is the signature of a
"this record changed" bit rather than part of the setting.

### `partyusecharhit` → `0026A430` (37 B)

```c
uint8_t b = (value != 0);                     /* normalised to 0 or 1 */
*((uint8_t *)a + 0x08) &= ~0x08;
*((uint8_t *)a + 0x09) &= ~0x40;
*((uint8_t *)a + 0x09) |= (uint8_t)(b << 6);  /* +0x09 bit 6 */
*((uint8_t *)a + 0x08) |= (uint8_t)(b << 3);  /* +0x08 bit 3 */
```

**One boolean sets two bits in two different bytes**, and this setter writes the actor object
directly — it never dereferences `+0xC0`. Any reimplementation that keeps these as one flag will
diverge from the original the moment something else writes one of the two bytes.

## 5. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0033FD60` | `partyusemapid` handler | 312 B | verb `040D`; flag pair + re-place |
| `00340700` | `partyusecharhit` handler | 187 B | verb `040E` |
| `00341190` | `partysetlod` handler | 187 B | verb `040F` |
| `00341B90` | `partyshowshadow` handler | 187 B | verb `0410` |
| `00342360` | `partyshowshadow_411` handler | 82 B | verb `0411`; **pushes `1`**, tail-jumps to `00341B90` |
| `00342830` | `partyhideshadow` handler | 79 B | verb `0412`; **pushes `0`**, tail-jumps to `00341B90` |
| `00342B30` | `setpartyprojectionshadow` handler | 187 B | verb `0413` |
| `0031B5A0` | the party collector | 202 B | four slots, two gates, one range test |
| `0031B670` | collector adapter, selector 0 | 8 B | `xor r8d,r8d ; jmp 0031B5A0` |
| `0031B680` | collector adapter, selector 1 | 11 B | `mov r8d,1 ; jmp 0031B5A0` |
| `00267E10` | `VMValueStack_PopInt32CoerceFloat32` | 78 B | the one argument these verbs take |
| `00267F90` | `VMValueStack_PushInt32` | 39 B | how `0411`/`0412` supply their constant |
| `0026AD60` | the `partyusemapid` flag pair | 34 B | `m[+0x08]` bits 1 and 2, mutually exclusive |
| `00265020` | `Actor_GetWorldPosition` | 61 B | the read half of the re-place |
| `002E5DF0` | position write adapter | 22 B | appends a zero fifth argument, calls `002E5C90` |
| `002E5C90` | the position re-place | 340 B | **read 2026-09-18 (FABLE)**, see the residue bullet below |
| `00322C50` | `BattleEncodedId_IsValidForClass` | 1,025 B | called with class `0x17` per slot |
| `002367A0` | `BattleUnit_FindByDefinitionSelector` | 126 B | id -> unit |
| `0026A430` | char-hit setter | 37 B | `+0x08` bit 3 and `+0x09` bit 6 |
| `002EC680` | LOD setter | 26 B | `pres[+0x13]` whole byte |
| `002ECD80` | blob-shadow setter | 53 B | `pres[+0x151]` bit 3 |
| `002E8730` | projection-shadow setter | 192 B | record `+0x304` two-bit field |
| `002E8CE0` | LOD refresh | 309 B | **read 2026-09-18 (FABLE)**, see the residue bullet below |
| `002E8FD0` | `Actor_RefreshPresentationVisibility` | 793 B | called by the blob-shadow setter |
| `02EBF190` | authored table base | pointer | party slot ids at `+0x5A5A`, stride 2 |
| `022C6F28` | record table base | pointer | `0x740`-byte records, indexed by `pres[+0x00]` as `int16` |

## Call chain (SWE2-CONTRACT, 2026-09-30)

```
zone script: CALL 040D .. 0413 (partyusemapid, partyusecharhit, partysetlod, partyshowshadow[_411], partyhideshadow,
             setpartyprojectionshadow)
  -> the verb handler (0033FD60 .. 00342B30): pops one value (00267E10)            <- THIS SYSTEM
       -> 0031B670 / 0031B680 -> the party collector 0031B5A0: slot map 1 [02EBF190]+0x5A5A, four slots,
          class 0x17 check (00322C50), 002367A0 id -> unit, two gates and the 7..25 range split
       -> per member, one setter: 002EC680 (LOD), 002ECD80 (shadow), 002E8730 (projection shadow),
          0026A430 (hit reaction), 0026AD60 + the re-place 002E5DF0 -> 002E5C90 (partyusemapid)
            -> Actor_RefreshPresentationVisibility 002E8FD0 / the LOD refresh 002E8CE0
               -> the character render record 022C6F28 + id x 0x740
```

**Upstream (who causes this):** authored zone scripts, typically around staged scenes.

**Downstream (what this causes):** per-member presentation flags and the render record's LOD, shadow, visibility and
position state.

**Do not confuse with:** the party standard-motion verbs, which walk the live roster rather than slot map 1
([the party standard-motion verbs](the-party-standard-motion-verbs.md)).

## Modding notes (SWE2-CONTRACT, 2026-09-30)

- **Best intervention point:** the verb handlers, which apply one value to every collected member; there is no
  per-character form in this family (§1).
- **Breaks if:** a mod expects these verbs to reach a character missing from slot map 1; the collector reads map 1
  and gates it, so such a character is left alone (§3, RC-18).
- **Regenerates itself:** the LOD refresh re-derives the render record's thresholds from the presentation record's
  `+0x13` (§6), so write the presentation byte, not the thresholds.
- **Multiplayer / XIIOnline:** the effects are script-driven presentation; every client runs the same script, so they
  are not a local decision to suppress.

## Claims, evidence and tier (SWE2-CONTRACT, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| Seven verbs, one shape: pop one value, collect map 1, apply one setter per member | the seven handlers read; §2 and the falsification pass 1 family argument | 1 |
| The collector reads map 1 with class 0x17 and a 7..25 split | `0031B5A0` read; SP-1's first half (the party-table rows) | 1 |
| The four setters' exact writes | §4, each body read | 1 |
| `partyusemapid` re-places the actor through the transform node | `002E5C90` read (§6) | 1 |
| The LOD refresh pins the last level at 1,000,000 | `002E8CE0` read (§6) | 1 |
| Render record `+0x140` is the model transform's translation source | `_types/fields.tsv` | 1 |

## 6. What this document does not establish

- **What the flag pair in `m[+0x08]` bits 1-2 selects.** The write is exact; the meaning is not.
  The verb is named `partyusemapid`, which suggests *use the map's own placement* versus something
  else, but that is the name's suggestion and not evidence. Filed with `SP-1`.
- ~~**What `002E5C90` (340 B, unnamed) does with the position.**~~ `002E5DF0` is a 22-byte adapter that
  appends a fifth argument of `0` and calls it. ~~That the round trip is a re-place is inferred from
  the values being passed through unmodified, not from reading the callee.~~ **Read 2026-09-18 (FABLE): it is the re-place, and the point makes a round trip through the render object's transform.** `002E5C90(actor, x, y, z, mode)` returns at once for a record linked as a summon source (`byte +0x18 == 1`) and does nothing but the final call for an actor whose kind bits (`byte +3 & 0xE0`) are not `0x60`. Otherwise it writes the point into ~~the movement body~~ the **movement context** `[actor+0xB8]` (*corrected 2026-09-18, FABLE: the 0x230-byte context at actor `+0x120` in [the context census](../../04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md); the movement body is the pooled record at the secondary context's `+0x138`, the node below*) at `+0`..`+8`, adds the context's attachment offset `+0x40`..`+0x48` when `+0x107` bit 1 is set (`002E5D06`..`002E5D28`), asks `00267260(actor)` (true when `003B7730` holds, the ~~render record~~ secondary context `[actor+0xC0]` exists without `+0x14F` bit 0 and with the movement body (the transform node) at `+0x138`, `actor+9` bit 0 is set, and it returns `actor+8` bit 1), pushes the point into that node through `003DB1B0(node, &p)` (`00380D30(node+0x30, &p)`, 0 when the node's word `+0x82` is negative) and, when the predicate held, reads the node's resolved position `+0x30`..`+0x38` back through `003DAE00`, then stores the point minus the offset back into the movement context (`002E5D68`..`002E5DB1`) and calls `002E6000(actor, mode)`: for the same kind, with the render record live and without `+0x14F` bit 0, that sets the record's position through `003EC3D0(id, x, y + 00263910(), z, mode)` (`002E6041`..`002E6067`). So the verb's position goes movement context → movement body → (resolved) movement context → render record *(names corrected 2026-09-18)*.
- ~~What class `0x17` selects.~~ **Already answered** by [the encoded-id class
  registry](../../00-Engine-Core-Runtime/the-encoded-id-class-registry.md): class 23 is *the party
  configuration*, with a literal bound of **9**. That is the nine-slot array above, and it is why
  this collector's bound of 4 is a deliberate subset rather than the array's size.
- **What `rec[+0x04]` in 7..25 means.** The split is proven; its meaning is not. Filed as `SP-1`.
  > *SP-1's first half answered 2026-09-12 (FABLE).* The stats record's `+4` word is the definition
  > id, whose low byte is the party-table row for a party-kind unit ([the record kind byte](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) AL-1 / AL-2, with
  > the row census): **rows 0–5 are the six playables, 6 is Reks, 7–16 the named guests (Amalia, the
  > three Basch variants, Lamont, the two Vosslers, Larsa, the two Reddases), 17–25 the nine "No name"
  > reserve rows, 26 the Chocobo, 27–39 the Espers.** So `(rec[+4] − 7) <= 0x12` selects **the guest
  > band — every party-table unit that is neither one of the seven player-controlled characters nor
  > the Chocobo nor an Esper** — and the verbs' two collections are "the player's characters" and
  > "the guests". The same range test is the AI selector's opcode 34 operand 3 ([the gambit page](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) Z-1),
  > and its neighbour operand 4 is the Esper band 27–39. The second half — whether map 1 is the
  > membership the player sees following them — remains open.
- **Whether these verbs act on the same characters the player sees following them.** Map 1 is the
  combat-processing set; whether that is the same membership as the field followers, in every state,
  was not established here. *(Answered as RC-18, the next box: map 1 is the engine's own follower source. Pointer
  2026-09-30, OPUS.)*
- [x] **RC-18.** Whether party slot map 1 (`[02EBF190] + 0x5A5A`, the combat-processing set the appearance verbs
  collect) is the same membership as the characters the player sees following, in every state — SP-1's second half,
  left open when SP-1's first half was answered. The motion verbs read the live roster `0209A1F0` instead
  ([the party standard-motion verbs](the-party-standard-motion-verbs.md) §3; SP-2 bounds when the two can disagree).
  Registered 2026-09-30 (SWE2-CONTRACT); static first: the writers of map 1 against the follower spawn path.
  *Applied 2026-09-30 (records) RC-18:* **ANSWERED 2026-09-30 (static; ORACLE's record `_index/candidates/rc18-map1-blend-arms-0930/`, commit `1e4537034`): map 1 is the engine's own follower source.** `PartyFollow_SolveFormation` (`00338490`) and `PartyFollow_ApplyGoal` (`003246C0`) both walk map-1 slots 0–3 through `0031B810`, and every rebuild of map 1 (`003266C0`) re-binds the roster to it. The sets differ only by exclusions that record tabulates, the leader among them (it is skipped at `003385EC`).
- **What the downstream consumers do with these bits.** ~~`002E8CE0` (309 B) is unread, and~~
  `Actor_RefreshPresentationVisibility` (793 B) was identified by name only. *(Read since: the interior citation at
  the foot of this page traces its tag gate, its triple-clear arm and the per-record visibility flag writes through
  `00428E10` / `00428DE0` / `00429020`; pointer 2026-09-30, SWE2-CONTRACT.)* *`002E8CE0` read 2026-09-18 (FABLE):* it is the LOD refresh and reads the presentation record's `byte +0x13` as the local LOD level count `n`: when negative it calls `CharacterRenderRecord_EnableLocalLodThresholds(rec, 0)` on the actor's render record (`022C6F28 + id × 0x740`, only when `+0x284` is non-zero) and returns; otherwise it enables local thresholds (`003E5E50`, 1), sets levels 1..n-1 to `0.0` and level `n` to `1000000.0` (`0091573C`) through `CharacterRenderRecord_SetLocalLodThreshold` (`002E8D90`..`002E8E00`). The record's `+0x13` thus chooses how many LOD levels the actor keeps and pins the last at a distance it never reaches. **This is why the
  document is `L1` and not `L2`:** the verb layer is reproducible byte for byte, the presentation
  consequence is not.
- **Any runtime observation.** Every claim here is static: disassembly of the shipped bytes at the
  certified hash. Nothing was watched in a running game, and no value was seen to change.

## 6b. Related

- [The five parallel slot maps](../../11-Party/the-five-parallel-slot-maps.md) — the five bases and
  the resolver.
- [Active party, reserve, and the moment the leader changes](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md)
  — §2b names map 1 as the combat-processing set.
- [The encoded-id class registry](../../00-Engine-Core-Runtime/the-encoded-id-class-registry.md) —
  class 23 (`0x17`) and its literal bound of nine.

## 7. Falsification checklist

- [x] **The four 187-byte handlers are one family.** *Killer:* any instruction difference beyond the
      setter call. Compared: only the setter target differs, plus argument-read ordering in `040E`.
- [x] **The collector reads four of the nine slots.** *Killer:* a non-constant loop bound, or a
      bound of 9. `cmp ebx, 4` at `0031B644` is an immediate, and the array is nine entries per the
      party documents — so the subset is real and deliberate.
- [x] **These verbs read map 1, not map 3.** *Killer:* a different displacement. The `lea`/`add`
      chain resolves `0x5A5A`, computed with a tool, not read off the page.
- [x] **The split is `rec[+4]` in 7..25.** *Killer:* a different comparison. `sub al,7 ; cmp al,0x12 ;
      setbe` at `0031B625`-`0031B629` is an unsigned range test, which is exactly `7 <= x <= 25`.
- [x] **Only the low bit of the argument reaches the blob shadow.** *Killer:* a wider mask.
      `and dl,1` at `002ECDA3`.

> **PASS 9 RUN AGAINST THIS LIST — 2026-09-13 (OPUS). Five killer tests executed on the bytes; all
> five claims survive, and one is stronger than its own caveat says.**
>
> | claim | named killer | at the bytes | verdict |
> |---|---|---|---|
> | only the low bit reaches the blob shadow | `and dl,1` at `002ECDA3` | `and dl,1` → `shl dl,3` → `or [rax+0x151],dl` | **holds** — and it lands at **bit 3 of `+0x151`** |
> | the split is `rec[+4]` in 7..25 | `sub al,7 / cmp al,0x12 / setbe` at `0031B625` | exactly that | **holds** — `0x12` = 18, so `7..25` |
> | the subset bound is 4 of 9 | `cmp ebx,4` at `0031B644` | `cmp ebx,4 / jl` | **holds** |
> | the projection shadow is a two-bit field | the off path clears `0x3000` at `002E87DB` | `and dword [rcx+0x304], 0xFFFFCFFF` | **holds** — `~0xFFFFCFFF` = `0x3000`, **bits 12–13** |
> | these verbs read map 1, not map 3 | a different displacement | `mov esi, 0x5A5A` at `0031B5CD`, then `mov rax,[02EBF190]` at `0031B5ED` | **holds, and is understated** |
>
> **THE LAST ONE'S CAVEAT IS TOO MODEST.** It reads *"the `lea`/`add` chain resolves `0x5A5A`,
> computed with a tool, not read off the page."* **It is read off the page**: the collector
> `0031B5A0` carries the displacement as a **literal immediate**, `mov esi, 0x5A5A`, twenty-four
> bytes before it loads the map base. All five map displacements are present as dword immediates in
> `.text` — `0x5A48` ×31, `0x5A5A` ×16, `0x5A6C` ×2, `0x5A7E` ×8, `0x5A90` ×8 — so *which* map a
> site reads is a first-tier reading throughout, not a derived figure.
>
> **And the base cross-confirms today's AG-1 work.** `02EBF190` is the **battle system runtime state
> block**, located this session at `021B290C` (`02164280 + 0x4E68C`) with accessor offsets reaching
> `+0x5AE4`. The five party maps at `+0x5A48`…`+0x5A90` fall inside that reach — **two independent
> lines of work agreeing on the same structure's extent.**
>
> *No claim on this list was refuted. That is the result, and it is worth as much as a refutation
> would have been.*
- [x] **`0411` and `0412` are wrappers, not implementations.** *Killer:* any write of their own.
      Neither touches memory beyond saving registers; both end in `jmp 00341B90`.
- [x] **`partyusemapid` leaves the position unchanged.** *Killer:* arithmetic between the get and
      the set. The three `movss` loads at `0033FDF1`-`0033FE06` read back exactly the slots
      `Actor_GetWorldPosition` was given.
- [x] **The projection shadow is a two-bit field.** *Killer:* the off path clearing only `0x2000`.
      It clears `0x3000` — both bits — at `002E87DB`.

> **The three remaining killers run 2026-09-14 (FABLE); all hold, and the list is ticked.** OPUS's pass 9 above had
> already executed the first five and the projection-shadow killer (`and dword [rcx+0x304], 0xFFFFCFFF` at `002E87DB`)
> without ticking the boxes.
> - **`0411` / `0412` are wrappers.** `00342360` (82 B) and `00342830` (79 B) save four argument registers, load
>   `edx = 1` (`0034237A`) or `xor edx, edx` (`0034284A`), call `VMValueStack_PushInt32` `00267F90`, restore, and
>   `jmp 00341B90`. They contain no store of their own. The only write is the callee's push onto the VM value stack.
> - **`partyusemapid` leaves the position unchanged.** In both member loops `Actor_GetWorldPosition(actor, &a, &b, &c)`
>   fills `[rsp+0x28]` / `[rsp+0x24]` / `[rsp+0x20]`. The next three instructions load them into `xmm1` / `xmm2` /
>   `xmm3` in the same order, and `002E5DF0(actor, …)` follows with no arithmetic between (`0033FDEC`–`0033FE06`,
>   `0033FE47`–`0033FE61`).

## 8. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only. Every address and size below was re-measured from the shipped image and the function
list. Nothing executed.)*

### ✔ The family argument reproduces in full

| claim | measured |
|---|---|
| the seven bodies are **312 / 187 / 187 / 187 / 82 / 79 / 187** | **all seven** |
| the four 187-byte handlers share the argument reader, both collectors and the cookie, and **differ only in the setter** | **exactly**: each call set is `{00267E10, 0031B670, 0031B680, setter×2, 00808C40}`, and the only pairwise difference between any two is the setter |
| the four setters are `0026A430` / `002EC680` / `002ECD80` / `002E8730` | **those four, one per handler** |
| `partyusecharhit` reads its argument **after** the collectors | **yes** — its order is `0031B670`, `0031B680`, `00267E10`; the other three read first |
| the setter runs for **both** groups | **the setter appears twice in each of the four**, once per collector's loop |
| `0411` pushes `1`, `0412` pushes `0`, both tail-jump to `0410` | **`mov edx, 1` / `xor edx, edx` at `0034237A` / `0034284A`, `call 00267F90`, `jmp 00341B90`** — all six instructions at their published addresses |
| "all three end in the same **53-byte** setter" | **`002ECD80` is 53 B** |
| `0031B670` is 8 B and `0031B680` 11 B, both tail-jumping to `0031B5A0` with selectors 0 and 1 | **8 and 11**, `xor r8d, r8d` / `mov r8d, 1` then `jmp 0x31B5A0` |
| `0026AD60`'s bit pair | **`and byte [rcx+8], 0xF9`** clears bits 1 and 2, then `setne` / `sete` / two `add al, al` build exactly `(b << 1) \| ((!b) << 2)` and OR it back — §2's C is instruction-exact |

**The differ-only-in-the-setter claim is the page's load-bearing one**, and it is the kind that a
call-set comparison either confirms or destroys. It confirms: over four bodies of 187 bytes each,
the symmetric difference of any two call sets is **one address**.

### ✖ Corrected: the enumeration denominator

§2's method note says *"every verb whose name contains `party` … 49 of them"*. The dispatch table
holds **63** such verbs (63 distinct names, 72 distinct handler addresses); **16** *begin* with
`party`. **49 is neither number.**

**The conclusion is unaffected and in fact stronger.** Of the 63, exactly **four** have a handler of
187 bytes — `040E`, `040F`, `0410`, `0413` — so the wider net still closes on the same four. Image-wide
there are **48** functions of exactly 187 bytes, which is why the "party verbs first" restriction is
what makes the test sharp rather than the size alone.

**Not claimed.** What the four setters do — **none of their bodies was read here**, only their
identity and arity as call targets. The collector `0031B5A0` (202 B) was read only for the two
adapters' selectors; §3's walk of it stands as written. Nothing was executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Movement — CLIENT and SERVICE.**
  - `Actor_GetWorldPosition` (`00265020`, 104 raw sites) is read by `BattleUnit_PublishLocomotionPosition…`,
    `Movement_UpdateSteeringTowardTarget`, `BattleLocomotion_BuildSolverContext` and thirteen more movement bodies.
  - `BattleUnit_FindByDefinitionSelector` is read by `BattleLocomotion_DecodeOrderGoal` and a 419-byte body.
  - `Actor_RefreshPresentationVisibility` (`002E8FD0`) is called by two movement bodies (997 B and 2,026 B).
  - The 26-byte `002EC680` and the 37-byte `0026A430` are read by movement helpers.
  - `002E5C90` / `002E5DF0` sit inside movement code: the 22-byte `002E5DF0` forwards to `002E5C90`, and `0033FD60`
    reaches it.
  - The id-validity query is also asked by two locomotion bodies.
- **Items_Equipment_Shops_License — MECHANICAL.** `BattleEncodedId_IsValidForClass` (`00322C50`) is shared with
  thirteen licence, equipment and class-D functions (`BattleStats_HasRequiredLicenseForEquipment`,
  `Equipment_CheckItemEligibleForSlot`, `BattleIdClassD_*` …).
- **Spawn_Encounter_Lifecycle — CLIENT.** `Actor_GetWorldPosition` is read by `Spawn_TrySelectCandidatePosition`,
  `Spawn_ValidateCandidateDistanceToPlayers` and `SpawnLifecycle_CheckAndRetireByNativeRange`.
- **Audio — CLIENT.** `Actor_GetWorldPosition` is read by the 1,036-byte positional Audio body.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** `BattleEncodedId_IsValidForClass` is also called by three status bodies: `BattleStats_RecomputeDerivedStateAndAutoStatuses`, `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` and `BattleUnit_RunPeriodicCombatMaintenance`. The status layer validates encoded ids through the same class check.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `BattleStats_RebuildEffectiveStatsAndAffinityState`, owned by that layer, calls `00322C50` on this page. That caller is the effective-stats re-form, and it says where its output lives: with no explicit destination it writes the record's **own `+0x24` block, `0x24` bytes wide**, and the block at `+0x50`, taking its mode from the flag word at `+0x3C`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `00265020` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `BattleMenu_BuildCommandEntryList`, owned by that layer, calls `00322C50` on this page. That caller is the command-list build, and the ceiling is in the first instruction: the menu kind is bounded at **`0x22`** into a jump table, after which `dword[+0x40]` is zeroed and `dword[+0x44]` set to `-1` before any entry is written; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
- **CombatAI — MECHANICAL (13 edges).** 13 CombatAI-side calls into shared helper(s) the page cites (`BattleEncodedId_IsValidForClass` (00322C50), `BattleUnit_FindMappedDefinitionSelectorByIndex` (0031B810), `BattleUnit_FindByDefinitionSelector` (002367A0)) - the helpers' general call surface, not a CombatAI relationship of this page's subjects.
- **Gameplay — CLIENT and SERVICE (12 edges).** 7 inbound (Gameplay bodies `00312B40`, `0031ADB0`, `BattleAction_FindApproachGeometryAroundTarget` (00339630) call page-cited `Actor_GetWorldPosition` (00265020), `BattleUnit_FindMappedDefinitionSelectorByIndex` (0031B810), `BattleEncodedId_IsValidForClass` (00322C50)); 5 outbound (page-cited `BattleGroup_RefreshFourActorDefinitions` (003266C0), `BattleUnit_FindByDefinitionSelector` (002367A0), `0031B5A0` call Gameplay bodies `BattleEncodedId_IsValidForClass` (00322C50), `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (0030D9A0)). Substantive edges include `BattleGroup_RefreshFourActorDefinitions` (003266C0) calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (0030D9A0); the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (4 edges).** 1 inbound (WorldAreaField bodies `BattleSystem_RunFieldFrameOrchestrator` (00234590) call page-cited `BattleGroup_RefreshFourActorDefinitions` (003266C0), `PartyFollow_ApplyGoal` (003246C0)); 3 outbound (page-cited `BattleGroup_RefreshFourActorDefinitions` (003266C0) call WorldAreaField bodies `FieldData_GetActiveFieldRecordBit15` (00313F60), `FieldData_GetActiveFieldRecordBit15` (00377C20), `00377C70`).
## Interior citation — frontier hub `002E8FD0` (2026-09-18, SWE2-EC7)

`002E8FD0` — 793 B, 15 callers (5 A-measured);
`Actor_RefreshPresentationVisibility` — the body the party-look verbs end in. Interior
verified: `[+0xC0]` supplies the record, its `+0x30`/`+0x60`/`+0x90` triple become `r15`/`r14`/
`r12` (`002E8FE6`–`002E902B`); the `& 0xE0 == 0x60` tag gate picks the actor arm
(`002E902F`–`002E903A`); `byte[+0x11] & 6 == 6` takes the `002EE190` + `002E8AC0` + `002E8A70`
triple-clear (`002E90A9`–`002E90CC`); otherwise the `word [rbx]` handle indexes the `0x740`
render-record array at `020FB7xx` (`imul rcx, rax, 0x740` at
[`002E90F4`](../../_index/ADDRESS-INDEX.md)/`002E9136`) and `00428E10`/`00428DE0`/`00429020`
write the per-record visibility flags, with `[+0x284]` as the present-check. The `+0x151 >> 3 & 1`
bit at `002E916A` is the visibility source flag mirrored into the refresh.

## SWE2-EC7-22 update (2026-09-18) — `003DAE00` 12-byte copy-out

`003DAE00` (23 B) is the null-safe copy-out the presentation verbs use:
`rcx == 0` -> ret; else `[rcx+0x30]`/`[+0x34]`/`[+0x38]` written to `[rdx]`/
`[rdx+4]`/`[rdx+8]` — the three-lane record field the party-look verbs read.
Interior anchor `003DAE05` (the first field load).

## SWE2-EC7-30 update (2026-09-18) — `00267260` move-eligibility predicate

`00267260` (78 B) is the predicate the re-place paragraph describes:
`003B7730(actor)` must hold, then — only when the `+0xC0` secondary
context exists — it must have `byte[+0x14F] & 1` clear and the
`+0x138` transform node present; `byte[actor+9] & 1` must be set;
and the answer is `byte[actor+8] >> 1 & 1`. Any failed gate returns
0. Interior anchor `00267286` (the `+0x14F` bit test).

## SWE2-EC7-43 update (2026-09-19) - `00429020`

`00429020` (277 B) is a party-presentation-verb body - `0042E7A0`/`01F44830`/`022C6F28`, `00426220`/`0042EF90`/`00808C40`. Interior anchor `0042906F` (a `00426220` call).

## SWE2-EC7-49 update (2026-09-19) - `00340700`

`00340700` (187 B) is a body - `00267E10`/`0026A430`/`0031B670`/`0031B680`/`00808C40`. Interior anchor `0034072E` (a `00267E10` call).

## SWE2-EC7-49 update (2026-09-19) - `00341190`

`00341190` (187 B) is a body - `00267E10`/`002EC680`/`0031B670`/`0031B680`/`00808C40`. Interior anchor `003411B4` (a `00267E10` call).

## SWE2-EC7-49 update (2026-09-19) - `00341B90`

`00341B90` (187 B) is a body - `00267E10`/`002ECD80`/`0031B670`/`0031B680`/`00808C40`. Interior anchor `00341BB4` (a `00267E10` call).

## SWE2-EC7-49 update (2026-09-19) - `00342B30`

`00342B30` (187 B) is a body - `00267E10`/`002E8730`/`0031B670`/`0031B680`/`00808C40`. Interior anchor `00342B54` (a `00267E10` call).

## SWE2-EC7-73 update (2026-09-19) - `003E5E50` flag bit setter measured

`003E5E50` (17 B) is the `+0xC0` bit-0 setter the party-look verbs call:
`byte[+0xC0] = (byte[+0xC0] & ~1) | (dl & 1)` - one presentation flag,
three instructions.
Interior anchor `003E5E5A` (the `or` merge).

## SWE2-EC7-86 update (2026-09-20) - `003E5E70` validated float store measured

`003E5E70` (38 B) is the bounded float write the party-verb
callers run: `edx >= 8` or a negative `xmm2` returns -1.0f;
otherwise `xmm2` is stored to `[rcx + edx*4 + 0xA0]` and
returned - an 8-slot float array at `+0xA0` behind a guard.
Interior anchor `003E5E8C` (the `movss` store).

`003EC3D0` (314 B) is the `022C6F28` record write `002E6000`/`003EB8E0` call: `cx == -1` exits; `sx(cx) * 0x740 + 022C6F28` resolves the record (live check `dword[+0x284]` nonzero else null), `+0x290 & 0x100000` skips the compare, `+0x284 & 0x8000000` requires `word[+6]==-1`, else `word[+6]==-1` alone clears `+0x140`/`+0x148`/`+0x14C=1.0f`; otherwise ucomiss-compares xmm1-3 against `+0x140`/`+0x144`/`+0x148` and on change clears `+0x284` bit `0x200` and stores the triple with `+0x14C`=1.0f - the scripted colour/alpha triple a party-dress verb writes. *(That last reading is superseded, 2026-09-30, SWE2-CONTRACT: §6 reads the caller `002E6000` passing the re-placed point `(x, y + 00263910(), z)`, and `_types/fields.tsv` declares render record `+0x140` as `modelTransformTranslationSource`, the vec3 the model transform's translation row is copied from — so the triple is a position, not a colour.)*

Interior anchor `003EC456` (function `003EC3D0`).
