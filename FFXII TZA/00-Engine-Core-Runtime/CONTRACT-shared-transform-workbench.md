---
contract: A shared matrix parameter area with no owner — write your operands, call, read the result
category: 00-Engine-Core-Runtime
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: Shared-Transform-Workbench/the-shared-transform-workbench.md
entries: ["003970A0", "0036D9E0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the section's raw-backing test on the region's ends, every rip-relative
    access to `022D8F00`–`022D9500` classified as read or write, the 16-byte-wide accesses counted by
    distinct address with their alignment histogram, and each of the eighteen read-only functions
    resolved to the slots it actually touches. **This records checks performed on that date, not the
    method of the original derivation**, which is on the workbench page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-workbench-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the shared transform workbench

> **Authored 2026-09-22 by FABLE.** S-05's binding gap is *"two family contracts, one DIFFERENTIAL
> TESTED; **the borrow discipline is stated, the subsystem is not**"*. The two —
> [`CONTRACT-transform-workbench-save-restore.md`](CONTRACT-transform-workbench-save-restore.md) and
> [`CONTRACT-transform-primitives.md`](CONTRACT-transform-primitives.md) — cover *how to borrow the
> area* and *what the primitives compute*. **Neither says what the area IS**, and the answer is a
> negative one that matters: it has no owner.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants, and TW-4 and TW-5 are statements no single operation's contract can make.

## 1. Purpose

Give four subsystems a place to hand matrices to shared routines — a calling convention implemented
in memory rather than in registers.

## 2. Interface

The area is `022D8F00`–`022D9500` in `.data`. There is no API: callers address the rows directly.
The two bodies this contract names are the only ones with distinguished roles:

| | body | role |
|---|---|---|
| the one consumer | `003970A0` (44 B) | copies the matrix at `022D91B0` out as one 64-byte block |
| the one initialiser | `0036D9E0` (918 B) | writes 80 slots and reads none — a bulk clear |

## 3. Types

```
022D8F00 .. 022D9500   an array of 16-byte rows (TW-2)
  022D91B0 .. 022D91EF    the one proven 4x4 matrix (TW-3)
  022D94B0, 022D94B4      NOT matrix data — a separate object (TW-6)
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**TW-1 — The area has no static layout, because it has no static bytes.** Both ends of the region
lie **past `.data`'s `SizeOfRawData`**, so it is zero-filled at load and everything in it is built at
run time. *There is nothing to read in the image; the structure has to come from the code that
touches it — which is why every invariant below is a code measurement and not a data one.*

**TW-2 — It is an array of 16-byte rows, and the proof is alignment, not adjacency.** Of every
address in the region accessed 16 bytes wide there are **46 distinct ones, and the alignment
histogram is `{0: 46}`** — every one 16-byte aligned, no exceptions, across 3,892 access sites. *A
region that merely happened to hold floats would not do that.*

**TW-3 — Exactly ONE matrix is established, by the engine's own statement.** `003970A0` copies four
consecutive rows from `022D91B0` as one contiguous 64-byte block — four `movups` loads and four
stores into `[rcx + 0x00..0x30]` — which is a 4×4 matrix asserted by the code rather than inferred
from address adjacency. **The rest of the area does not divide into further 64-byte matrices on any
established stride**: rows are accessed in runs of 4, 6, 8 and more, and a sliding window over a long
run manufactures apparent "bases" 16 bytes apart. *That grouping is `BQ-16` and this contract does
not close it.*

**TW-4 — It is ARGUMENTS, not state, and the whole image contains exactly one counter-example.**
State is written by one party and read back by another later; arguments are written and read by the
same party in the same breath. Measured over every rip-relative access to the region:

| | |
|---|---:|
| functions touching the region | **267** |
| of those, functions that write | **249** |
| functions that only read | **18** |
| — of those, reading **only** the record-table base (TW-6) | **16** |
| — reading a single `dword` at `022D8F0C` | 1 (`00501820`) |
| — **reading matrix rows they did not write** | **1** (`003970A0`) |

**So one function in the entire image consumes a matrix it did not write**, and it is the getter of
TW-3. *Everything else writes its operands, calls, and reads its own result back.*

**TW-5 — There is no owner, and "shared scratch" undersells it.** Presentation dominates *use* — 144
writing functions against Audio's 4, ActorEntity's 1, Movement's 2 and UI's 1 — but use is not
ownership, and all three ownership tests fail: **no subsystem keeps an exclusive sub-area** (Audio
writes just four slots Presentation does not, the rest write none); **Presentation does not hold the
lifecycle**, since the only whole-area initialiser `0036D9E0` is unowned; and **nothing persists for
an owner to hold** (TW-4). *It is a shared parameter area, and it has no owner because there is no
transaction to own.*

**TW-6 — Two slots in the same page are a DIFFERENT OBJECT.** `022D94B0` and `022D94B4` are read
8 bytes wide, never as floats, by 16 of the 18 read-only functions — **and no rip-relative store to
them exists anywhere in the image**. *Corrected 2026-09-23 (SWE2-CONTRACT, re-verified owner-side):
the page's BQ-17 already resolved them — they are **not pointers but the base of a 32-entry table of
24-byte records** `{u32 id @+0; u16 state @+4; s8 @+8; …; u8 flags @+0x10}`. Every reference is a
`lea` that takes the base once; readers and writers alike index it (`base + idx·24`), which is why a
rip-relative-*store* census sees nothing — the writers are indexed stores through the taken base:
`0036DE5A` and `0036DF6A` (`lea r9,[rip→022D94B4]`; `mov word [r9 + rdx*8], r10w` — both are "set
state word = idx+4 for all 32 slots" reset loops), and `0036E2F8` (`lea rax,[rip→022D94B0]`; `or
byte [rax + rdx + 0x10], dil` — the `+0x10` flag byte).* They are a record table that happens to
live in the same page as the workbench, and a census of "who reads the workbench without
writing it" returns 18 until you ask what each of them reads.

## 5. State

**Owned:** nothing, by anyone (TW-5). **Written:** the rows, by 249 functions across five owner
categories. **Read back:** by the writer, in the same breath — except `003970A0`. **Not part of this
subsystem despite its address:** the record table (TW-6).

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-transform-workbench-save-restore.md`](CONTRACT-transform-workbench-save-restore.md) — how a borrower saves and restores |
| **Sibling** | [`CONTRACT-transform-primitives.md`](CONTRACT-transform-primitives.md) — what the shared routines compute |
| **Analogue** | the ScriptVM operand stack — one handler pushes arguments for another to pop, the same convention in a different medium |

## 7. State transitions

Per use: *write operands into rows → call a shared routine → read the result back.* There is no
transition the area itself owns; `0036D9E0` clears it wholesale and belongs to nobody.

## 8. Script · resource · event interactions

None. Nothing authored reaches this area.

## 9. Determinism

Deterministic. The area's contents are whatever the current borrower put there; nothing persists
between borrows by design (TW-4).

## 10. Failure paths and edge conditions

- **There is no protection of any kind.** Two borrowers overlapping in time would silently overwrite
  one another; what prevents that is the save/restore discipline of the sibling contract, not
  anything here.
- The area is zero at load (TW-1), so a reader that runs before any writer reads zeros, not garbage.

## 11. Observable behaviour

None directly. The workbench is invisible except through the results the shared routines return.

## 12. Reproduction formula

Sweep every rip-relative access to `022D8F00`–`022D9500`, split by read/write, and assert **249
writers and 18 read-only**; then resolve each of the 18 and assert **16 touch only `022D94B0`/
`022D94B4`** and exactly one reads matrix rows (TW-4, TW-6). Count distinct 16-byte-wide addresses
and assert **46, all 16-aligned** (TW-2).

## 13. Runtime validation

**One sibling is DIFFERENTIAL TESTED**; nothing here executes these bodies, and this contract claims
no runtime evidence of its own. *Stated rather than left blank so a CONTRACT READY header is not read
as evidence of execution.*

## 14. Unresolved

- ~~`BQ-16` — how the region divides beyond the one proven matrix (TW-3).~~ **CLOSED 2026-09-23
  (SWE2-CONTRACT): stale — answered on the owning page (BQ-16, ticked 2026-09-13): the region
  does not divide into matrices at all. It is the VU0 register bank — 31 vector registers and
  ACC ([the-ee-and-vu0-register-bank.md](Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md)) —
  and every 16-byte offset looks like a base because every one *is* a distinct register; a
  "matrix" is four consecutive registers one routine happens to use together.**
- ~~What writes the two pointer slots, given no rip-relative store exists (TW-6).~~ **CLOSED
  2026-09-23 (SWE2-CONTRACT): the item was stale — the owning page's BQ-17 answered it
  2026-09-12, and re-verification owner-side confirms every detail.** `022D94B0`/`022D94B4` are
  the base of a 32-entry, 24-byte record table, not pointers. The writers are indexed stores
  through a `lea`-taken base — a form no rip-relative-store census can see: `0036DE5A` and
  `0036DF6A` (`lea r9,[rip→022D94B4]` → `mov word [r9 + rdx*8], r10w`, the state-word reset
  loops for all 32 slots) and `0036E2F8` (`lea rax,[rip→022D94B0]` → `or byte [rax + rdx +
  0x10], dil`, the `+0x10` flag byte). TW-6's wording corrected above.
- Whether any pair of borrowers can overlap in time (§10).

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| TW-1 — no static bytes | the section header's `SizeOfRawData` tested against both ends of the region | 1 |
| TW-2 — 46 distinct addresses, all aligned | every 16-byte-wide access enumerated and reduced to distinct addresses, with the alignment histogram printed | 1 |
| TW-4 — 267 / 249 / 18, and the split of the 18 | every rip-relative access classified, then **each of the eighteen resolved to the slots it touches**, **with `003970A0` as the control** — a sweep showing it as a writer would not be measuring the page's claim | 1 |
| TW-3 — the one matrix | `003970A0` disassembled in full: four `movups` pairs from `022D91B0`..`022D91E0` | 1 |
| TW-5's owner tables and TW-6's "written through a register" | [the workbench page](Shared-Transform-Workbench/the-shared-transform-workbench.md) §2.5–§2.6 | 1 |
| TW-6 writers are indexed stores through a `lea`-taken base, not rip-stores — `022D94B0`/`B4` = a 32×24-byte record table | owner-side re-verification of BQ-17: `lea r9,[rip→022D94B4]` at `0036DE30`/`0036DF3D` feeding `mov word [r9+rdx*8]` at `0036DE5A`/`0036DF6A`; `lea rax,[rip→022D94B0]` at `0036E2EA` feeding `or byte [rax+rdx+0x10]` at `0036E2F8` | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on TW-1 through TW-6. **TW-5 is the one that shapes
the port**: giving the area an owner — the obvious design — turns a parameter convention into shared
mutable state and invites exactly the protection the original does without.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CoreRuntimeScheduling — internal.** The two named bodies are this category's own.
- **Presentation, Audio, ActorEntity, Movement, UI — MECHANICAL, and their presence is TW-5's
  subject.** Each writes the region; none owns it. **That fan-in is the finding**, not an incidental
  edge, and it is why this contract exists at subsystem scope. *No further address is cited for them:
  the writers number 249 and naming any of them would import its edge set for a statement already
  made by the counts.*

## 17. Related

- [The shared transform workbench](Shared-Transform-Workbench/the-shared-transform-workbench.md) — the mechanism
- [Contract — transform workbench save/restore](CONTRACT-transform-workbench-save-restore.md)
- [Contract — transform primitives](CONTRACT-transform-primitives.md)

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives, and every count reproduces

**Attack.** TW-1 to TW-4 and TW-6 became checks, with the census recomputed image-wide over every RIP-relative access to
`022D8F00`-`022D9500`. Script: `Tools/analysis-kit/gfz-scripts/falsify_workbench.py`, output `falsify_workbench.out`, image
`73461d08…`, 0 BROKEN. TW-5's ownership judgement is not re-litigated. §14 already points to the reading that the region
holds the VU0 register bank.

| # | Clause attacked | Result |
|---|---|---|
| W1 | TW-1 | **survives**: `.data`'s file-backed bytes end at `01F7E400`, before the region |
| W2 | TW-2 | **survives, exactly**: 46 distinct 16-byte-wide addresses, all aligned, over **3,892** 16-byte access sites |
| W3 | TW-3 | **survives**: `003970A0` (44 B) loads `022D91B0`/`C0`/`D0`/`E0` and stores them to `[rcx + 0 .. 0x30]` |
| W4 | TW-4 | **survives, exactly**: 267 functions, 249 writers, 18 read-only - 16 on the table base only, `00501820` on `022D8F0C`, `003970A0` on the matrix |
| W5 | TW-6 | **survives**: no RIP-relative store reaches `022D94B0`/`022D94B4`; the cited sites are the indexed stores through a `lea`-taken base |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names the edges of the two cited bodies.*

**Presentation — CLIENT (32 edges).** Twenty-nine Presentation bodies of 793 to 1,983 bytes in one address run (among them `0044CC50`, `0044D080`, `00455560`, `004584E0` and `0045D2F0`; thirteen are called directly by the effect type dispatcher, nine by neighbouring bodies in the run, seven by no direct call) call the one consumer `003970A0` to copy the workbench matrix at `022D91B0` out as one 64-byte block; the channel-rate emit `003DFFE0` and the rig frame `CharacterRender_UpdateCombatLookAndAuxControllers` (`003E00C0`) call the one initialiser `0036D9E0`, the bulk clear of 80 slots; and `00502280` calls `00501820`, the read-only body that reads the dword at `022D8F0C`, which `00502280` itself writes twice. These are the presentation side of TW-5's fan-in: these effect-side bodies read the one established matrix, the rig frame and the channel emit run the bulk clear, and the region is shared scratch that no presentation body owns.
