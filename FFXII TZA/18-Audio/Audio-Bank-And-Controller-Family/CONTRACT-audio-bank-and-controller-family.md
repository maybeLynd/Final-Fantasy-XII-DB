---
contract: Twelve audio classes in two layouts that share no slot meaning — six uniform banks and six controllers that are not
category: 18-Audio
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md
entries: ["00222550", "00222C00", "0021ABC0", "0021B150", "0021B0D0", "00212810"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — **every one of the twelve classes' vtables resolved from its own RTTI
    complete-object locator** rather than from a page's list, each slot count taken by walking to
    the first non-code qword, the four adjustor thunks and their targets disassembled, the broadcast
    body read **with its loop-back target resolved**, and the Music cross-check swept for `free`.
    **This records checks performed on that date, not the method of the original derivation**, which
    is on the family page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-audio-bank-family-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the audio bank and controller family

> **Authored 2026-09-22 by FABLE.** S-41's binding gap is *"1 of 3 pages contracted"*. The sound
> request was already contracted and
> [the spatial source objects](../CONTRACT-spatial-source-objects.md) were taken at `1afaa62de`;
> **this takes the bank and controller family, so all three of S-41's pages now carry a contract.**
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is seven
> such invariants, and **AC-1, AC-2 and AC-5 are statements about twelve classes at once** — none of
> which any single class's contract could make.

## 1. Purpose

Hold the sound banks the game has loaded, and give each kind of audio its own way of driving them.

## 2. Interface

**Twelve concrete classes, every vtable resolved from its own RTTI locator:**

| | vtable | slots | slot 0 | slot 7 |
|---|---|---:|---|---|
| `AudioBank` | `009078B0` | 11 | `00222550` | `00218260` (52 B) |
| `MusicAudioBank` | `00907910` | 11 | **`00222C00`** | `002182A0` (52 B) |
| `SebAudioBank` | `00907D80` | 11 | `00222550` | `0021ABC0` (52 B) |
| `SepAudioBank` | `00907B48` | 11 | `00222550` | `002195D0` (52 B) |
| `ShoutAudioBank` | `00907F90` | 11 | `00222550` | `0021BF20` (52 B) |
| `StreamAudioBank` | `009081A0` | 11 | `00222550` | `0021CD80` (52 B) |
| `AudioController` | `00906CD0` | **7** | `002127D0` | **absent** |
| `MusicAudioController` | `00907970` | 8 | `002182E0` | `00218980` (9 B) |
| `SebAudioController` | `00907DE0` | 8 | `0021AC00` | `0021B150` (9 B) |
| `SepAudioController` | `00907BA8` | 8 | `00219610` | `00219B10` (9 B) |
| `ShoutAudioController` | `00907FF0` | 8 | `0021BF60` | `0021C440` (9 B) |
| `StreamAudioController` | `00908200` | **7** | `0021CDC0` | **absent** |

## 3. Types

```
bank    +0x08  an intrusive entry list; each node's payload is at node +0x10
        +0x38  the id the slot-10 and slot-9 gates test
controller
        +0x08  the same entry list shape
        +0x20  a SECOND BASE SUBOBJECT -- present in four of six (AC-3)
        +0x60  a keyed map, erased through slot 3
```

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**AC-1 — Two layouts, and NOTHING means the same thing across them.** The scalar-deleting destructor
is **slot 7 on every bank** and **slot 0 on every controller**. *So a reader who learns one half's
slot map and applies it to the other is wrong at the first slot they try*, and the two halves cannot
be one hierarchy shifted by an offset.

**AC-2 — The banks are UNIFORM and the controllers are NOT.** All six banks have **exactly 11
slots**, and every one of their slot 7s is a **52-byte** body in the sized-`operator delete` idiom
(`call <destructor>` / `test bl, 1` / `mov edx, <size>` / `call free`). The controllers split:
**`AudioController` and `StreamAudioController` have 7 slots; the other four have 8.** *So "the
controller layout" is not one layout either, and the extra slot is the whole difference.*

**AC-3 — That extra slot is a SECOND BASE, and it is present in exactly four of six.** Each of the
four 8-slot controllers' slot 7 is a **9-byte** thunk, and all four are the same two instructions —
`add rcx, 0x20` then `jmp` — to **four distinct bodies of exactly 161 bytes each**. `add rcx, 0x20`
before dispatch is the `this`-adjustment for a secondary base subobject at `+0x20`. *The four
targets being separate 161-byte bodies rather than one folded body is what makes this four
inheritance paths and not one.*

**AC-4 — The bank broadcast dispatches through the BANK's own vtable, and re-resolves it on every
entry.** `00222550` walks the `+0x08` list and calls `[this_vtable + 0x48]` — slot 9 — once per
entry, passing the node's payload as `rdx` and `this` as `rcx`. **The vtable load
`00222580 mov rax, qword ptr [rdi]` is the loop-back target itself** (`jne 0x222580` at
`00222596`), so it happens once per entry rather than once per call.

> **This corrects the family page**, which cites that exact instruction and reads it as
> *"`rax = [this]` loaded once before the loop"*. It is **inside** the loop. *The consequence is a
> reentrancy property: a slot-9 override installed while a broadcast is running takes effect for the
> entries that follow.*

**AC-5 — Five of the six banks share slot 0 VERBATIM, and the sixth is the cross-check.** `AudioBank`,
`Seb`, `Sep`, `Shout` and `Stream` all point slot 0 at the same body `00222550`; only
`MusicAudioBank` differs, at `00222C00` (101 B), **which makes zero calls to `free`**. *That is what
proves AC-1 rather than merely asserting it: if the two halves were one hierarchy shifted by an
offset, a bank's slot 0 would be a destructor — and the one bank that does not share the common body
still is not one.*

**AC-6 — Slot 10 is a FIVE-BIT COMMAND MASK on one shared manager byte, split across the classes.**
~~Carried from [the page](audio-bank-and-controller-family.md) §2 and not re-derived: every concrete bank reads the
manager's `+0x3C` and re-dispatches a different slot per bit — `& 1` → slot 0, `& 2` and `& 4` →
slot 9, `& 8` → slot 3, `& 0x10` → slot 4, `& 0x20` → slot 5.~~ *Corrected 2026-09-26 (FABLE, Claude Opus 5.5), from
the executed dispatch (`_index/candidates/s41-opus-replay-bank-family/check.py`, ALL PASS, re-run by FABLE) and the
bytes, re-read. The old sentence holds only as a union over the classes.* Each bank's slot 10 reads the manager's
`+0x3C` and acts on its own subset of the bits:

| class (vtable) | slot 10 | bits it acts on |
|---|---|---|
| `MusicAudioBank` (`00907910`) | `00222C70` | `& 1` → slot 0 (`jmp [rax]`) |
| `SepAudioBank` (`00907B48`) | `00223540` | `& 2` → slot 9, as a tail jump; only when bit 2 is clear, `& 8` / `& 0x10` / `& 0x20` → its slots 3 / 4 / 5 |
| `SebAudioBank` (`00907D80`) | `00224B30` | nothing when its own `+0x38` is 0; otherwise `& 2` → slot 9, as a tail jump, and only when bit 2 is clear, `& 8` / `& 0x10` / `& 0x20` → **direct calls** to `00224290` / `002240B0` / `00224470`, not its vtable slots 3 / 4 / 5 (`00224180` / `00223FA0` / `00224360`) |
| `ShoutAudioBank` (`00907F90`), `StreamAudioBank` (`009081A0`) | `00225440` | `& 4` → slot 9 only |
| `AudioBank` (`009078B0`) | `_purecall` | — |

*A port that implements one uniform mask gets four of the five concrete banks wrong.*

**AC-7 — One 1000-id band, 150000–150999, is treated apart, and both classes test the same band.**
~~**AC-7 — The six-digit id space splits at 150999 / 151000, and both halves use the same boundary.**
Also carried from [the page](audio-bank-and-controller-family.md) §2: Sep's slot 3/4/5 gates and
Seb's three iterator copies both test the `0x249F0` boundary, by a reciprocal divide in the Seb case.
*The split is a property of the id space, not of either class.*~~ *(the original heading, body and closing line,
verbatim; the struck span was re-quoted exactly on 2026-09-26)* *Corrected 2026-09-26 (FABLE, Claude Opus 5.5), from the bytes and the executed case
`AC7_sep_slot3_skips_the_band_150000_to_150999_only`.*
- Sep's slots 3 and 4 (`00223100`, `002230D0`) compute `[+0x38] − 0x249F0` and return on an unsigned `< 0x3E8`. So
  they skip only the band 150000–150999: ids below 150000 wrap high and pass, as do ids from 151000 up (149999
  passes, 150000 and 150999 do not, 151000 passes).
- Sep's slot 5 (`00223130`) tests the same window with `jae`, so it acts **only** inside the band.
- Seb's iterator copies skip an entry whose `[+0x24] / 1000 == 150` (reciprocal `0x10624DD3`, `sar 6`, `cmp 0x96`):
  the same band.

*The band is a property of the id space, not of either class. "Splits at 150999/151000" was that band's upper edge,
read as a split.*

## 5. State

**Owned:** each bank's entry list and each controller's `+0x60` map. **Shared:** the manager byte
AC-6 reads. **Not owned:** the driver objects both halves call into.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`../Audio-Boundary/CONTRACT-sound-request.md`](../Audio-Boundary/CONTRACT-sound-request.md) — S-41's first |
| **Sibling** | [`../CONTRACT-spatial-source-objects.md`](../CONTRACT-spatial-source-objects.md) — S-41's second |
| **Consumes** | the `.seb` slot flag byte, whose five bank consumers are read on [the block-index page](../Sound-Bank-And-Voice-Formats/seb-se-block-index.md) |

## 7. State transitions

Per controller: *register an entry (slot 5) → drain the request queue (slot 7, where present) →
dispatch → erase from the map (slot 3).* Per bank: *broadcast over the entries (slot 0) → arm one
(slot 9) → tear down (slot 2, destructor at slot 7).*

## 8. Script · resource · event interactions

None directly. The banks are populated from loaded `.seb` / `.sab` data.

## 9. Determinism

Deterministic. No generator is drawn in either layout.

## 10. Failure paths and edge conditions

- `StreamAudioController` has **no slot 7**, so anything that dispatches slot 7 generically across
  controllers is wrong for it — its queue drain is reached directly instead (AC-2, AC-3).
- A bank whose entry list is empty broadcasts to nobody: `00222550` tests head against the sentinel
  before the first iteration (`00222571`).

## 11. Observable behaviour

None directly. This is the shelf the sounds sit on; what it looks like when it breaks is a category
of audio going silent while the others keep playing.

## 12. Reproduction formula

Resolve all twelve vtables from RTTI and assert **11 slots for every bank** and **7 / 8 / 8 / 8 / 8 /
7 for the controllers in the order above** (AC-2). Assert every bank's slot 7 is 52 bytes and every
present controller slot 7 is 9 bytes (AC-2, AC-3). Disassemble the four thunk targets and assert
**161 bytes each and four distinct addresses** (AC-3). Resolve `00222550`'s loop-back target and
assert it is `00222580`, the vtable load (AC-4). Sweep `00222C00` for `free` and assert **zero**
(AC-5).

## 13. Runtime validation

**None.** No experiment executes these bodies. S-41's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*

## 14. Unresolved

- What the secondary base at `+0x20` **is** — AC-3 establishes that four controllers have one and
  that its methods are four separate bodies, not what interface it implements.
- Why `StreamAudioController` alone among the concrete controllers lacks it.
- What the five commands of AC-6's mask mean to a player.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| AC-1, AC-2 — the two layouts and the slot counts | **all twelve vtables resolved from their own RTTI complete-object locators**, each walked to its first non-code qword; the page's own figures reproduced independently | 1 |
| AC-3 — four thunks, four 161-byte targets | the four 9-byte bodies disassembled in full and each target's extent read | 1 |
| AC-4 — the per-entry vtable load | `00222550` disassembled **with its jump targets resolved**: `00222596 jne 0x222580` lands on the vtable load, which is the control — a load before the loop would not be a branch target | 1 |
| AC-5 — five share, Music differs | the six slot-0 addresses compared, and `00222C00` swept for `free`: zero | 1 |
| AC-6, AC-7 — the command mask (per class) and the id band — *restated 2026-09-26 from the executed dispatch* | [the family page](audio-bank-and-controller-family.md) §2, falsified 2026-09-02 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on AC-1 through AC-5. **AC-1 is the one that
decides whether the port is even structurally right**: one slot map for "audio objects" is the
natural design and it is wrong at slot 0 and slot 7 simultaneously. **AC-4 is the subtle one** — a
port that hoists the vtable load out of the broadcast loop is faster, matches on every ordinary
input, and differs exactly when an override is installed mid-broadcast.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Audio — internal.** All twelve classes, the broadcast, the thunks and the destructors are this
  category's own.
- **Every other layer reached is MECHANICAL**, through these bodies' own callees — chiefly the
  driver the banks and controllers both call into. *Their addresses are deliberately not cited: the
  driver is a hub, and naming one of its entries imports its whole edge set for a statement the slot
  map already makes.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document, so *audio* in ordinary prose can clear a layer
> nothing here dispositions — the defect measured in
> `../../_index/candidates/fable-crossings-prose-false-clears.tsv`.

## 17. Related

- [The audio bank and controller family](audio-bank-and-controller-family.md) — the mechanism
- [Contract — the sound request](../Audio-Boundary/CONTRACT-sound-request.md) — S-41's first
- [Contract — spatial source objects](../CONTRACT-spatial-source-objects.md) — S-41's second

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives, as corrected on 2026-09-26

**Attack.** §2's twelve vtables and AC-1 to AC-7 became checks. The vtables were read from `.rdata` and slot counts
taken as runs of `.text` pointers; AC-6 and AC-7 are as corrected on 2026-09-26. Script:
`Tools/analysis-kit/gfz-scripts/falsify_audio_bank_family.py`, output `falsify_audio_bank_family.out`, image `73461d08…`,
0 BROKEN, exit 0. OPUS's executed dispatch (`s41-opus-replay-bank-family`) is not repeated.

| # | Clause attacked | Result |
|---|---|---|
| A0 | §2 | **survives**: every bank has 11 slots and the controllers 7 or 8 as tabulated; every slot 0 and slot 7 as cited |
| A1 | AC-1, AC-2 | **survives**: every bank's slot 7 is a 52-byte sized delete calling `00809950`; every controller's slot 0 calls the same free routine |
| A2 | AC-3 | **survives**: four 9-byte `add rcx, 0x20; jmp` thunks, to four distinct 161-byte bodies |
| A3 | AC-4 | **survives**: the vtable load at `00222580` is the loop-back target, and slot 9 is called inside the loop |
| A4 | AC-5 | **survives**: five banks share `00222550`; Music's `00222C00` (101 B) calls no free routine |
| A5 | AC-6 as corrected | **survives**: slot 10 is `00222C70` / `00223540` / `00224B30` / `00225440` (Shout and Stream); AudioBank's jumps through the IAT to `_purecall`; each reads manager `+0x3C` |
| A6 | AC-7 as corrected | **survives**: Sep's slots 3, 4 and 5 test `0x249F0` ± `0x3E8` (below with `jb`, inside with `jae`); six Seb bodies carry the `/1000 == 150` test |

No correction.
