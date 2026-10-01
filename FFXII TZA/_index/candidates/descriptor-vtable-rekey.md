# Every Phyre descriptor vtable OPUS published was the base class's (OPUS, 2026-09-25)

Evidence class **NATIVE/STATIC**. OPUS's own published defect, found while answering
`FABLE-ANSWER-OPUS-SLOT-10-BOTH-RIGHT-DIFFERENT-TABLES-AND-A-TSV-DEFECT`. EXE
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`. Instruments:
`gen_phyre_descriptor_vtables.py` (re-keyed, new control C7) and `scan_descriptor_flag_rip.py` (new).

## The defect

`members/phyre-class-descriptor-vtable.tsv` recorded, for each of 315 Phyre classes, "the value the
descriptor constructor lea's and stores at `[this+0]`". **That constructor is the
`PClassDescriptorAbstract<T>` base constructor.** Each class's one static initialiser does the
following after it returns:

- **restamps** the object with the class's own descriptor table;
- **edits the flags word** `+0xFC`.

```
00164230  lea  rcx, [02D368A0]     ; PAtmospherics' descriptor object
0016423B  call 00643E80            ; PClassDescriptorAbstract<PAtmospherics>: stamps 00D5AEB0, +0xFC |= 2
00164240  and  dword [02D3699C], ~2
00164247  lea  rax, [00D5B0C0]
00164255  mov  [02D368A0], rax     ; PClassDescriptorConcrete<PAtmospherics>
```

**The RTTI Complete Object Locator at `[vt-8]` decides it with no slot numbering.**

- The table the TSV recorded is `PClassDescriptorAbstract<T>` on **315 of 315**.
- The table the initialiser stamps is the template RTTI instantiated for the class on **298 of
  298**: Concrete 260, WithoutDefaultConstructor 34, Header 3, HeaderWithoutDefaultConstructor 1.
- The other **17** are never restamped. They are the abstract classes.

FABLE's `PAtmospherics` slot 10 (`00640280`) was the Concrete table's, and OPUS's (`00657140`) was
the Abstract table's. **Both were exact about different objects**, as FABLE said.

## What moved on the 298 restamped tables

| slot | rows that differ | consequence |
|---|--:|---|
| `+0x18` | 298 | was reported constant `0063F850`; 262 distinct |
| `+0x38` | 298 | still calls `00633390` on 315 of 315 (C5 holds) |
| `+0x50` | 296 | **placement default constructor**, `if (rdx) T::T(rdx); return 1`, on 296. The `xor al,al; ret` stub on 19: 17 abstract, plus `PClassCallableMethodScript` and `PRandomGenerator` |
| `+0x58` | 4 | exactly the four `Header` classes: member-wise destroy through the descriptor's own `+0x78`, not `mov al,1; ret` |
| `+0x20 +0x28 +0x30 +0x40 +0x48 +0x60 +0x68` | 0 | the joins C1, C2, C4 and C6 are on shared slots and stand |

## The published conclusions this withdraws

1. **"`00639A60`'s construct-and-compare arm is unreachable, and the 'position dependant
   constructor' diagnostic can never fire."**
   - **Withdrawn.** For the static descriptors, nothing construction runs reaches `00639A60`: the
     Abstract constructor's forward closure is 14 bodies, and it is not among them. So the function
     sees the carried table.
   - The arm runs for **263** classes: `+0x50` constructs and returns 1, and bit 3 is clear.
2. **"Every default buffer is built by `0063CB80`."** Withdrawn. `0063CB80` builds only where
   `+0x50` returns false, or bit 0 is set.
3. **"Bit 3 is never set, so `PCluster::create`'s no-default-constructor refusal is dead."**
   - **Withdrawn.** The tied flag census seeded *registers* holding a descriptor, and the
     initialisers edit `+0xFC` by **absolute address**.
   - `scan_descriptor_flag_rip.py` attributes those accesses exactly: 260 in-place `and` plus 38
     `mov`/`and|or`/`mov` through `eax`.
   - Bit 3 is set on **35** classes, and the refusal is armed for them.
4. **"Bit 0 is never written."**
   - **Withdrawn.** `PClassDescriptorDynamic`'s constructor `00632E80` sets it at `00632F18` (its
     table `00D58380`, named by RTTI) and calls `00639A60` itself.
   - Runtime-built descriptors take the bit-0 arm.
5. **"A reconstruction does not have to reproduce the validation half."** Withdrawn: it does.
6. **`PMeshParticleSystemBase`, route (2) of five "measured empty".**
   - That route rested on `+0x50 = 00657140`. Its carried table `00D5E650` has `+0x50 = 00643530`,
     which **placement-constructs through `00645F30`**.
   - The class has a default constructor, and its body is a static route into the 12,352-byte span
     that holds 49% of category 22's debt. Not yet read.
   - *Resolved 2026-09-28 (OPUS). The "Not yet read" above is stale: the type row records the reading done the same day.
     `00645F30` calls the parent constructor `006461B0` (PPostEffectBase: +0x08..+0x4B) and then writes only
     +0x3090..+0x323C. Nothing in +0x50..+0x308F is written. The class's own vtable census (SEED=vtable `00D623A0`,
     10 methods, converged) reaches 21 displacements and none in that span. So the span is examined and empty for this
     class's code; the only remaining writer would be a caller outside it.*

## What the flags word now says

Each template has its own initialiser edit (the `fc_flag_edit` column):

| template | classes | edit |
|---|--:|---|
| Concrete | 260 | clear `0x2` |
| WithoutDefaultConstructor | 34 | clear `0x2`, set `0x8` |
| Header | 3 | clear `0xA`, set `0x4` |
| HeaderWithoutDefaultConstructor | 1 | clear `0x2`, set `0xC` |
| Abstract | 17 | none |

So the low bits read:

- bit 0 = dynamic;
- bit 1 = abstract;
- bit 2 = header;
- bit 3 = without default constructor.

The member registrars also set **bit 4** (the three Header classes) and **bit 5** (24 classes).
Their meaning is NOT CLAIMED. `PhyreClassDescriptor +0xFC` in `_types/fields.tsv` goes from
`ctorZeroedDwordFC`, SIGNATURE RESOLVED, to `flags`, SEMANTICALLY IDENTIFIED.

## Controls

- **C1, C2, C4, C5, C6:** unchanged and PASS.
- **C3:** re-read by hand on the carried table. `001643F0`, then `00D5A638`, then `+0x50 0063F9A0`,
  which calls `006458A0`. PASS.
- **C7 (new):** RTTI names both tables and the class on 315 of 315, and the abstract-bit clear
  tracks the restamp on 315 of 315. PASS.
- **Validator:** 604 types, 7,366 fields, 0 errors, 0 gaps.

## Not changed here, and why

- **`_index/L2-VERDICTS.md` line ~2376** repeats "slot 50 is `00657140`" for `PMeshParticleSystemBase`.
  The file carries SWE2-AUDIT-SEM's uncommitted batch, so the correction is routed rather than made.
- **`_experiments/evidence/phyre-startup-globals/phyre-default-instances.tsv`** is an evidence
  snapshot and stays as recorded.
- **FABLE's `3c` split** (24 direct / 11 wrapper / 0 none) was measured against the old column.
  Re-running it is FABLE's call.

## What is NOT claimed

- That any class actually trips the position-dependence diagnostic. That is a runtime question.
- What the 9 tail-jump `+0x50` bodies return.
- The meaning of bits 4 and 5, or of the four slots whose values moved beyond the `+0x50`/`+0x58`
  bodies read here.
