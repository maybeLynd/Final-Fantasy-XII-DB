---
system: How a script changes the battle party - the asynchronous party verbs, what each begin does, and the one poll they share
category: 01-Script-VM-Native-Bridge
status: DOCUMENTED
owner_layer: PrimaryOwner:ScriptVM
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: eleven bodies disassembled from the authority image and read whole, 2026-09-19 - four begin callbacks
    (0034D4E0, 00350CD0, 00350160, 00352AF0), two polls (003506A0, 0034CDF0), the pending test 003596B0 and its callee
    00324360, the roster-contains test 003596D0, the two mask builders 00359BA0 and 00359C00 and the non-guest collector
    00320800; the verbs located in the dispatch table by the accessor frame (begin at tbl + 0x20n + 8, poll at + 0x10) and
    named from the bundled community catalogue, an external authored source
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-battle-party-verbs-falsification-pass-1
  note: written by FABLE for FRONTIER-REQ-FABLE-LAST-96-UNCITED-BODIES; static throughout. The roster mutators the
    begins end in, the three add verbs' begins and the flag pair keyed 0x13 are not read and are named as such. Verb
    names are leads from an authored catalogue; here each name was checked against what its begin does; pending first
    review
---

# How a script changes the battle party

Eight script verbs change who is in the party. All eight are **asynchronous** - they have a begin callback and a poll
callback and no result - because a change to the party sets off the party read-in
([the party read-in state machine](the-party-read-in-state-machine.md)), which takes frames; the script waits until it
is over. This page reads all eight begins and all three polls.

## 1. The eight verbs

Located by the accessor frame of [the dispatch table](../scriptvm-native-dispatch-table.md); names from the bundled
catalogue ([async-verbs-by-accessor.tsv](../Verb-Dispatch/members/async-verbs-by-accessor.tsv)).

| call id | authored name | begin | poll |
|---|---|---|---|
| `0x353` | `addpartymember` | `0034C030` | `0034C370` |
| `0x354` | `removepartymember` | `0034C030` *(shared with the verb above)* | `0034CDF0` |
| `0x355` | `setbattlemember` | `0034D4E0` | `003506A0` |
| `0x358` | `removebattlemember` | `00350160` | `003506A0` |
| `0x359` | `setbattlememberone` | `00350CD0` | `003506A0` |
| `0x35A` | `setbattlememberlock` | `00351A40` | `003506A0` |
| `0x35B` | `addguestbattlemember` | `00352190` | `003506A0` |
| `0x35C` | `removeguestbattlemember` | `00352AF0` | `003506A0` |

Characters are **selectors**: 0-6 the main characters, 7-25 guests
([active party and reserve](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md)). The *runtime
roster* is the first four of the nine party slots.

## 2. What the four begins have in common

Each pops its arguments from the script stack, then **raises flag `0x13`** through the engine's flag setter (the one the
world-tick page reads with `0xF`; the setter itself was not read here *(answered: `003601B0` / `003601C0` set and clear bit `cl` of `022CB720`, falsification pass 1 row B1; 2026-10-02, OPUS)*) before it touches the party *(corrected 2026-10-02, OPUS: `setbattlemember` raises it before its first pop, `0034D542` then `0034D558`)*. ~~The two `set` verbs~~ `setbattlemember`, `setbattlememberone` and `addguestbattlemember` *(corrected 2026-10-02, OPUS: slot loops `0034D520`–`0034D53B`, `00350CF5`–`00350D10`, `003521A6`–`003521C1`; `setbattlememberlock` has none)*
first walk roster slots 0-3 and call one routine on every actor present with a zero argument *(what it clears was not
read)*.

## 3. The begins

**`setbattlemember(a, b, c)` - `0034D4E0` (277 B).** Pops three selectors, the last argument first. A negative selector
means "no one" and is skipped. It builds a mask of the requested selectors and notes whether the **preferred focus** -
the leader - is among them. **The request is carried out only if every requested selector is an available main
character**: the mask must be a subset of the non-guest party mask (section 5) restricted to its low seven bits. If so
the roster's first three slots are reconciled to the request. Then, **if the leader is not one of the requested three,
the first requested selector becomes the leader** - even when the reconcile was refused.

**`setbattlememberone(a)` - `00350CD0` (159 B).** A guest selector does nothing. For a main character: if it is in the
runtime roster, **every other roster member is demoted to the reserve**, leaving it alone; if it is not in the roster,
the same is done around the roster's *first* member instead - the verb never brings anyone in.

**`removebattlemember(a)` - `00350160` (98 B).** A guest selector does nothing. A main character is moved out of the
runtime roster **only while the roster holds more than one** - the last member cannot be removed.

**`removeguestbattlemember(a)` - `00352AF0` (57 B).** The mirror image: it removes the selector **only when it is a
guest**.

**The add side, read whole 2026-09-19 after the first publish of this page** (a bucket audit showed these three
bodies credited while still marked *not read*).

- **`0034C030` (33 B), the begin shared by `addpartymember` and `removepartymember`, does no party work**: it zeroes
  the verb's state dword and stores the popped selector at state `+4`. Everything happens in the poll.
- **`addguestbattlemember` - `00352190` (94 B)**: the `set` verbs' preamble (the four roster actors, then the flag),
  and then it adds the selector **only when it is a guest**.
- **`setbattlememberlock` - `00351A40` (81 B)**: pops the lock flag, then the selector, raises the flag, and - **for a
  main character only** - hands the selector and the flag (as 0 or 1) to the lock routine, which was not read.

## 4. The polls

**`003506A0` (33 B), shared by six verbs.** It asks whether a party mutation is still pending (`003596B0`, 24 B: true
unless `00324360`, a boolean of `0037CB50`, answers exactly 1). **`0037CB50` (46 B, read whole 2026-09-19) is the end
test of the party read-in task**: it answers 1 when no read-in task exists, or when the task's slot cursor has left
the roster - past slot 3 when its step is positive, below slot 0 when it is negative
([the party read-in state machine](the-party-read-in-state-machine.md), the verb task). **So what these verbs wait
for is the read-in task having rebuilt all four roster slots.** While pending it returns
non-zero and the script keeps waiting; when it is over it **lowers flag `0x13`** and returns 0.

**`0034CDF0` (97 B), the poll of `removepartymember`, does the work itself** - a three-state machine on the verb's
per-call state block: **states 0 and 1 do the same thing in the same call** (0 is first set to 1 and falls through) -
remove the main character whose selector is the block's byte `+4`, raise flag `0x13`, become 2, return 1; state 2 is
the shared poll's wait, returning non-zero while pending and otherwise lowering the flag and returning 0. Any other
state returns 1.

**`0034C370` (96 B), the poll of `addpartymember`, is its mirror**: states 0 and 1 raise flag `0x13` and *then* add
the main-character selector to an available reserve index; state 2 is the same wait. **The two orders differ - the
add raises the flag before it changes the party, the remove changes the party before it raises the flag.**

## 5. The helpers

| body | what it does |
|---|---|
| `003596D0` (107 B) | is this selector in the runtime roster? collects slots 0-3 and compares |
| `00359BA0` (93 B) | bit mask of the runtime roster's selectors |
| `00359C00` (93 B) | bit mask of every **non-guest** selector in all nine party slots |
| `00359740` (107 B) | is this selector among the non-guest members of all nine slots? the same collection, compared |
| `00320800` (144 B) | the collector under it: for slots 0-8, a valid slot's selector is kept when it is 6 or below, or `0x1A`..`0xFE` |

## 6. What a reimplementation must keep

- The verbs are asynchronous: a script that changes the party **waits** for the read-in; one that did not would run
  ahead of actors that do not exist yet.
- `setbattlemember` is all-or-nothing on availability, but **changes the leader regardless**.
- `setbattlememberone` and `removebattlemember` can never empty the roster.
- Guests and main characters have separate removal verbs, and each silently ignores the other kind.

**Not read:** the roster mutators the begins end in (reconcile, demote, move-out, the two removers); the lock routine
`setbattlememberlock` ends in; the flag setter and clearer keyed `0x13` *(answered: falsification pass 1 row B1; 2026-10-02, OPUS)*; the
per-actor routine ~~the two `set` verbs~~ the three preamble verbs *(corrected 2026-10-02, OPUS: as §2)* call first.

| body | anchors |
|---|---|
| `0034D4E0` `setbattlemember` begin (277 B) | `0034D513`, `0034D522`, `0034D531`, `0034D542`, `0034D558`, `0034D568`, `0034D570`, `0034D57D`, `0034D584`, `0034D58C`, `0034D59B`, `0034D5A0`, `0034D5A7`, `0034D5C3` |
| `00350CD0` `setbattlememberone` begin (159 B) | `00350CEC`, `00350CF7`, `00350D06`, `00350D17`, `00350D20`, `00350D2B`, `00350D44`, `00350D4D`, `00350D52` |
| `00320800` non-guest collector (144 B) | `0032083E`, `00320847`, `0032084E`, `00320852`, `0032085A`, `00320863`, `00320870` |

## Cross-subsystem neighbours

**Party - CLIENT.** Every begin on this page ends in a Party-layer mutator and the helpers read the Party layer's
nine-slot array; this page describes the script's side only and names no Party mutator by address.

**Gameplay - SERVICE.** `00320800` calls `00322C50`, the encoded-id validity test owned by that layer, with class
`0x17` and the slot index - it asks only whether the slot is a valid party-configuration id (the active-party page
reads that test). The crossing is that call, not a shared responsibility.

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives

**Attack.** Sections 1 to 5 were turned into checks at their instructions. The eight verbs' begin / poll pairs were
checked against the verb table. Script: `Tools/analysis-kit/gfz-scripts/falsify_battle_party_verbs.py`, output
`falsify_battle_party_verbs.out`, image `73461d08…`, 0 BROKEN, exit 0. The roster mutators and the lock routine stay
unread, as the page says.

| # | Clause attacked | Result |
|---|---|---|
| B0 | sizes; the verb table | **survives**: all 17; the eight begin / poll pairs as tabled |
| B1 | section 2: the flag and the preamble | **survives**: `003601B0` / `003601C0` set and clear bit `cl` of `022CB720`; every begin raises `0x13`; the slot-0..3 preamble in the three verbs that have it |
| B2 | section 3: `setbattlemember` | **survives**: negative selectors are skipped. The reconcile runs only on a subset of (non-guest & `0x7F`). The leader is changed whenever it was not requested, independently of the reconcile |
| B3 | section 3: the other begins | **survives**: `setbattlememberone`; `removebattlemember` with its count > 1 guard; the guest-only pair; the main-only lock; `0034C030` |
| B4 | section 4: the shared poll | **survives**: pending = !(read-in ended). The read-in has ended when there is no task, or the cursor is past 3 on a positive step, or below 0 otherwise; the flag is cleared when it ends |
| B5 | section 4: the two per-verb polls | **survives**: remove mutates, then raises the flag; add raises the flag, then mutates |
| B6 | section 5: the collector | **survives** |
| B7 | section 2: "each pops its arguments … then raises flag `0x13`" | **precision**: `setbattlemember` runs its preamble and raises the flag (`0034D542`) before its first pop (`0034D558`). The other begins pop first. In every begin the flag still rises before the party changes |

No correction.
