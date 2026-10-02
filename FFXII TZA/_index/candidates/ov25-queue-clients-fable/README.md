# OV-25: the other external-owner families (FABLE, Claude Opus 5.5, 2026-09-29)

**The question.** Register row OV-25 (box on `02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md` §9) asks for three things about the indexed owner:
1. its producer/error-recovery policy;
2. its nonempty registration policy;
3. the OTHER external-owner families.

The row says the first two are partly answered by two pages. The residue it keeps open is the families.

**Where each part stands.**
- **Error recovery.** Answered by the OV-42 record (`../ov42-submit-recovery-fable/`, db66f57fb). The owner protocol has no recovery for a rejected submission. The row and box wait on FRONTIER.
- **Nonempty registration.** Carried by three open rows on the nonempty-registration page: OV-39 (producer guarantees), OV-40 (re-registration of fresh against relocated bytes) and OV-41 (other subtypes and consumers). The owner's own side is already on the owner page: completion writes state 4 without testing the registration return, and state 4 is not proof of registration. OV-25 adds nothing here that those rows do not carry.
- **The families.** Answered below.

## What counts as a family, and the census

A family is a record that:
- holds a loaded source's handle;
- is handed to the tail requester `0032E620` as the completion argument;
- has a completion that **registers** the source, as the indexed owner's `003DD850` does.

Registration goes through one door. `00409FE0` has a single caller, the 12-byte thunk `0041E580`, and the thunk has exactly four callers. The fef page listed those four as load-completion callbacks (`uq218-residue-fable` C). This record closes the census and places each caller:
- no rel32 jcc, no rip-relative operand and no absolute pointer names either address;
- each of the four is taken by a `lea` just before a requester call.

The control is `families.py` R and R2. K gives each scanner a known positive; the rip-operand scan's first draft found nothing, not even the known `lea`.

| family | records | completion (requester site) | release |
|---|---|---|---|
| the indexed source owner (documented) | 5 × 16 × 0x1C at `02B581A0` | `003DD850` (`003DDAB9`) | `003DD380` / `003DD420`, and `003DD850` on state 5 |
| **the motion cache** | 16 × 0x14 at `02B57F70` | `003DC340` (`003DC683`) | the drain `003DC4A0` |
| **the script name-binding record** | the record passed as the argument | `002E4D20` (`002EAE08`) | not read |
| **the per-lane sub-record** | 0x120 B at `02161DA0`, 32 lanes | `002E4E50` (`002E700C`) | the sweep `002E6A80` → `002E6E30` |

The other 47 requester sites (`clients.py`, 51 in all) are not families by this definition. By R, none of their completions registers a source, and five of them pass no descriptor at all. What each one does with its bytes is its own page's subject, not this record's.

The release helper `0041E490` has eight callers (`families.py` U):
- the indexed owner's three;
- the motion-cache drain;
- the lane release;
- three in the per-frame gate's drain and list code (`002E65A0`, `002E6900`, `002E6D60`). These three are not attributed to a family here.

## How each new family handles a release while its read is in flight

The families differ in this, and it is the difference a reimplementation gets wrong.

- **The indexed owner** parks the record at state 5; the completion frees it (the owner page).
- **The motion cache** (`families.py` M1–M5) is refcounted. Its slot layout:
  - `+0`: handle;
  - `+4`: refcount;
  - `+6`: state (0 free, 1 requested, 2 in flight, 3 loaded, 4 release pending);
  - `+8`: an id that carries a generation.

  Its steps:
  1. The submit `003DC5B0` runs only on state 1 and writes 2 after the requester call, as the indexed owner writes 3.
  2. The completion writes 3, unpins and registers.
  3. The release `003DC780(id)` matches the id and decrements the refcount. At 0 it raises the sweep flag `02B58170`.
  4. The three sweeps write 4 **only on a state-3 slot**, and `003DC6A0` also bumps the id by 0x10.
  5. The drain releases, frees and clears each state-4 slot.

  An in-flight slot is never released. It completes to 3 and is taken by the next sweep, so the family needs no deferred-delete state. A stale id no longer matches after the bump.
- **The per-lane sub-record** (`families.py` L1–L3). The completion's argument is `record index << 16 | lane`. Each record has three masks: `+0x24` loaded, `+0x2C` release requested and `+0x34` pending.
  1. A release request (`002EAFA0`) sets the requested bit. It links the record onto the sweep list `0215FD90` only when the lane is loaded.
  2. The sweep releases a lane only when it is requested **and** loaded, so a lane requested while pending is not freed in flight.
  3. The completion sets loaded, clears pending, and registers only while the record's node still carries the record's generation. Otherwise it calls the release request.
- **The script name-binding record** (`families.py` S). The completion unpins `+0x10`'s handle. It then registers unless flag byte `+0x18` has bit 4, in which case it sets bit 8 instead. It then calls `002EA6E0(record, 3)` ~~and sets bit 2. What sets bit 4, and what releases this record, are not read.~~ *(Corrected 2026-10-02, FABLE, on ASTRA's [`namebinding-deletion`](../../../_experiments/evidence/namebinding-deletion/README.md), SWE2-AUDIT-SPEC ACCEPT ([review](../auditspec-review-namebinding-deletion-1001/REVIEW.md)); check [`ov25_astra_check.py`](ov25_astra_check.py), FAILS 0)*: bit 2 is **not** set unconditionally. `002EA6E0` returns 0 at once when `+0x18` has bit 4 (`002EA6EF`), and the completion then sets bit 2 and retires the record. Without bit 4 the follow-up allocation may return 1, and bit 2 is set only at the reached completion tail. **Who sets bit 4:** the removal `002EAEB0`. With `+0x18` bit 2 clear and `+0x19` bit 4 clear it only sets `+0x18` bit 4 and returns (`002EAEC4`-`002EAECC`), a mark-only delete with no free. Otherwise it advances the stamp, unlinks and retires the record. **What releases it:** the cleanup drain. `002E6D60` enters only when `002E6900(0)` returns 0, for a selected retired record with a nonzero `+0x10` handle. `+0x18` bit 8 or `+0x19` bit 4 skips the unregister `0041E490`, but not `002E9360`, which requests the child releases, calls `00369800` on the handle, clears it and recycles the record. `+0x19` bit 4 is an explicit exception whose meaning and natural states stay open.

## What this enables

A reimplementation now knows every place a loaded file becomes a registered resource. There are four, each with its own record and completion. For the motion cache and the per-lane records, it knows how a release during a read is kept safe (a refcount with a loaded-only sweep, and a two-mask sweep), in addition to the indexed owner's state 5.

## Not claimed (explicit obligations)

- ~~**The script name-binding record's deletion policy:**~~
  - ~~who sets `+0x18` bit 4;~~
  - ~~`002EAEB0` and `002EA6E0` are unread past their flag writes;~~
  - ~~the record's release site.~~
  *(Corrected 2026-10-02, FABLE, on ASTRA's [`namebinding-deletion`](../../../_experiments/evidence/namebinding-deletion/README.md), SWE2-AUDIT-SPEC ACCEPT ([review](../auditspec-review-namebinding-deletion-1001/REVIEW.md)); check [`ov25_astra_check.py`](ov25_astra_check.py), FAILS 0)*: read; see family S above. Still open: what sets `+0x19` bit 4 and what it means, actual timing, allocator completion, and the opaque callees' effects.
- ~~**A per-lane release requested in flight whose node then goes stale:** does it reach the sweep list? `002EAFA0` returns early when the requested bit is already set, and `002EB890` is unread.~~
  *(Corrected 2026-10-02, FABLE, on ASTRA's [`lane-stale-release`](../../../_experiments/evidence/lane-stale-release/README.md), SWE2-AUDIT-SPEC ACCEPT ([review](../auditspec-review-astra-lane-stale-release-1001/REVIEW.md)); check [`ov25_astra_check.py`](ov25_astra_check.py), FAILS 0)*: **the stale completion does not enqueue it.** The completion `002E4E50` sets loaded and clears pending, then its stale-owner arm calls `002EAFA0`, which for an already-requested lane goes from `002EAFB2` straight to its `ret` (`002EB026`) before any write or call. It neither adds nor removes sweep membership. `002EB890` only adjusts the lane's 16-bit count, with no calls and no queue writes. Still open: membership the lane already had, other relink paths, and the game's actual sequence; this is not a leak claim.
- **A store of 4 to a motion-cache `+6` through a slot pointer held outside the twelve functions that address the table.** Not excluded.
- **Authored reachability of any of these states.** No live run was made.

## Proposed register disposition

OV-25 → **ANSWERED** for its residue, the other families, by this record:
- the error-recovery half is answered by the OV-42 record;
- the nonempty-registration half is carried by OV-39, OV-40 and OV-41.

The obligations above go on the owner page's box as its remaining text, not as a new row. The owner page is a SECTION carrier, so FRONTIER applies the row and the box.

Controls:
- `clients.py` (C K): FAILS 0, output `clients.out`;
- `families.py` (R R2 M1–M5 S L1–L3 U K): FAILS 0, output `families.out`.
