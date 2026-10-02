---
contract: Find a resource section by tag and name, and turn its offset into a pointer
category: 02-Resource-And-Asset-Pipeline
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: resource-section-addressing.md
entries: ["00409C30", "00409660", "004096C0", "00409600", "00409780", "00409210", "00409A60"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — all four bodies read at instruction level, the eight name compares located
    at their header displacements, both 32-bit sums and their sign extensions, the `-1` sentinel
    test, and an image-wide sweep for the `@ALL` literal. **This records checks performed on that
    date, not the method of the original derivation**, which is on the section-addressing page;
    see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-section-addressing-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
external_production:
  section: SECTION-10
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md
---

# Contract — resource section addressing

> **Authored 2026-09-22 by FABLE.** S-09's binding gap is *"one contract covers row lookup, not the
> binder or section addressing"*. This takes **section addressing**; the `.ard` binder remains
> uncontracted and this document does not claim it.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants over four bodies, and the sharpest is that **this subsystem does not fail closed**.

## 1. Purpose

Answer "where is the section called X of kind Y in this resource" — and hand back a pointer.

## 2. Interface

| | body | size |
|---|---|---:|
| match one header | `ResourceSectionHeader_MatchesTagAndName32` (`00409C30`) | 101 B |
| find a section's pointer | `ResourceEntry_FindSectionPointerByTagAndName` (`00409660`) | 89 B |
| resolve an offset | `ResourceEntry_ResolveSectionOffset` (`004096C0`) | 41 B |
| resolve an entry's base | `ResourceEntry_GetResolvedBasePointer` (`00409600`) | 86 B |

## 3. Types

```
ResourceSectionHeader
  +0x00        the raw section tag
  +0x10 .. +0x2F   the 32-byte name key   (RA-2)

ResourceEntry
  +0x04   mode           0 = inline, 1 = handle+cache, anything else = RA-4
  +0x10   inline data    (mode 0)
  +0x30   handle         (mode 1)
  +0x38   cached pointer (mode 1)
```

Global: `02B62E10`, the engine-wide re-resolve flag (RA-5).

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**RA-1 — Both query criteria have wildcards, and one of them is spelled in ASCII.** A tag of `0`
matches anything, and so does `0x4C4C4140` — the little-endian dword whose bytes read **`@ALL`**. A
`NULL` name matches anything. *The `@ALL` literal appears at exactly one site in the image*,
`00409C34`, so the wildcard is this matcher's and nothing else re-implements it.

**RA-2 — The name test is 32 bytes wide and every byte participates.** Eight dword compares, at
header displacements `+0x10`, `+0x14`, `+0x18`, `+0x1C`, `+0x20`, `+0x24`, `+0x28`, `+0x2C`
(`00409C48`–`00409C87`), against the query at `[r8 + 0 .. 0x1C]`. **It is not a string compare**: a
name must match through whatever padding follows it. Because the caller's name is normalised into a
fixed scratch buffer first, the engine supplies that padding — *and the consequence is a
**31-character limit** on section names*, which the page derives and this contract carries.

**RA-3 — The pointer arithmetic is 32-bit, then sign-extended — in both resolvers.**
`004096DF add eax, ebx` / `004096E1 cdqe`, and identically `004096A4 add eax, [rsp+0x40]` /
`004096A8 movsxd rbx, eax`. **A base above 4 GB does not survive either helper**, and a low-32 sum
reaching `0x80000000` comes back **sign-extended** — a pointer in the top half of the low 4 GB
becomes a negative 64-bit value. *An implementation using 64-bit arithmetic throughout will differ
from the original exactly where it matters.*

**RA-4 — THE LOOKUP DOES NOT FAIL CLOSED, and this is the invariant to design against.** An entry
whose mode is neither 0 nor 1 resolves its base to **NULL** — and `004096C0` then **adds the offset
to that zero base without testing it**. So for any offset other than `0` and `-1`, an entry of an
unsupported mode returns a **non-null pointer equal to the sign-extended offset itself**.

The two explicit guards are null entry and offset `-1`. **They are not the only ways to return
NULL:** unsupported mode with offset0 returns0, and `low32(base)+offset` can wrap to0 even in a valid
mode. SECTION-10 executes cached base `0xFFFFFFF0` plus offset `0x10`, which returns NULL. Adding a
new base-validity guard changes other native results; a small nonnull return alone does not prove
that the referenced storage is readable. The fixtures establish arithmetic, not a live caller crash.

**RA-5 — Mode 1's cache is invalidated engine-wide by one byte.** `00409600` branches on
`entry+0x04`: mode 0 resolves from inline data at `+0x10`; mode 1 re-resolves through the handle at
`+0x30` and refreshes the cache at `+0x38` **only while `02B62E10` is non-zero** (`00409622`),
otherwise returning the cached pointer unexamined. This byte controls this cache-refresh path. It is not the complete movement/consumer protocol:
SECTION-07 separately establishes the arena movement latch and EFX refresh paths. While the cache
flag is clear, this accessor does not independently validate a stale cache.

**RA-6 — `-1` is the only failure value that crosses the boundary.** It is what the find-by-tag-and-name
path returns when nothing matches, and it is the one offset `004096C0` tests for (`004096D5
cmp ebx, -1`). *So "not found" and "found at offset −1" are indistinguishable by construction, and
every caller's failure handling rests on that single sentinel.*

### RA-7 — PRF index and offset are separate outputs

The container magic is `0x50524640` (bytes `@FRP`, often called PRF in handoffs). Version0 walks
DWORD offsets at+30; version1 walks at+40 and skips zero slots. Offsets are relative to ~~the TABLE~~
~~BASE~~ the start of that offset array (`+0x30` or `+0x40`); the offset the lookup returns adds that bias and so is table-base relative *(corrected 2026-10-02, OPUS: `00409780+0xE7` `lea ecx, [rax + 0x40]` then `00409780+0xED` `add ecx, r10d` locates a section, and `00409780+0x115` `add ecx, 0x40` forms the returned offset; `00409780+0x148` / `00409780+0x170` for `+0x30`)*, not to each slot. The root is tested before children. A matching PRF root returns offset0
but leaves index=-1; a matching plain header returns offset0/index0. Child matches return the
actual authored slot index, including sparse slots. Unsupported versions and missing matches leave
both outputs=-1. Do not use a negative index as proof that the offset failed.

`00409A60` zero-pads the root and admitted child names before mode0 copy or mode1 retention.
The normalized query is31 characters plus NUL; the direct matcher still compares all32 bytes.
The code assumes readable, suitably terminated strings and valid offset/count tables; no malformed
asset safety guarantee follows from these fixtures.

## 5. State

**Owned allocations:** none by the lookup itself. The full lookup is not pure: it normalizes a
nonnull name into shared scratch `02B62E20`, initializes the output index/offset, and may refresh
entry+38 under RA-5. The separate setup `00409A60` normalizes names IN the supplied source before
copying or borrowing it. Thus lookup observation and source setup have different write footprints.
Mode0 holds an owning buffer descriptor at entry+10; it is not inline payload bytes.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-authored-table-row-lookup.md`](CONTRACT-authored-table-row-lookup.md) — S-09's contracted third |
| **Uncontracted** | the `.ard` binder — S-09's remaining gap, not claimed here |
| **Upstream** | whoever sets `02B62E10` |

## 7. State transitions

*query → match (RA-1, RA-2) → offset or `-1` → resolve (RA-3) against a base that may be zero
(RA-4) → pointer.* An entry in mode 1 additionally transitions *cached → re-resolved* whenever RA-5's
flag is set at the moment it is asked.

## 8. Script · resource · event interactions

The section headers and their names are authored. Nothing here writes them.

## 9. Determinism

Deterministic given the entry, the query and `02B62E10`. No generator is drawn.

## 10. Failure paths and edge conditions

- Null entry or offset `-1` → NULL. Otherwise return `sext32(low32(base)+offset)`, which may itself be zero (RA-4).
- A name longer than 31 characters cannot be matched (RA-2).
- A base whose low 32 bits plus the offset reach `0x80000000` is returned sign-extended (RA-3).
- Mode 1 with the flag clear returns whatever the cache holds, with no validity test (RA-5).

## 11. Observable behaviour

Lookups by name work up to 31 characters; a wildcard tag can be written either as zero or as the
four characters `@ALL`; and a resource whose entry is in an unexpected state does not report a
missing section — it reports a section at a very low address.

## 12. Reproduction formula

Resolve an entry with mode 2 and offset `0x100` and assert the result is `0x100`, **not `NULL`**
(RA-4). Match a 32-byte name differing only in its final padding byte and assert it fails (RA-2).
Set the low 32 bits of a base so that base+offset crosses `0x80000000` and assert the returned value
is negative when sign-extended (RA-3).

## 13. Runtime validation

**SECTION-10 isolated original-code evidence:** nonempty PRF0/1 lookup and normalization,
sparse version1 entries, wildcard/root/child outputs, invalid version/mode, and zero/wrapping
resolution run against synthetic records. The complete package has159 named assertions and8
rejected private-image variants; that aggregate is not159 section-addressing states. No live FF12
or exhaustive authored archive is claimed. [Evidence, exact inputs and limits](../_experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md).

## 14. Unresolved

- Complete live scheduling/reentrancy of `02B62E10`; the owning page already records static setter/clearer sites. Do not confuse a static setter with whole-game timing proof.
- Whether any caller distinguishes "not found" from a genuine offset of `-1` (RA-6).
- The `.ard` binder, which is S-09's other uncontracted half and is not attempted here.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| RA-1 — the two tag wildcards | `00409C34`'s compare, **and an image-wide sweep returning exactly one site for the `@ALL` literal** | 1 |
| RA-2 — eight dword compares at `+0x10`..`+0x2C` | every compare read at its address in `00409C30` | 1 |
| RA-3 — 32-bit sums, sign-extended, in both resolvers | `004096DF`/`004096E1` and `004096A4`/`004096A8` | 1 |
| RA-4 — no base test | `004096C0` read in full: the only tests are the null entry and `cmp ebx, -1` at `004096D5`; the `add` follows unconditionally | 1 |
| RA-5 — the global flag | `00409622`'s `cmp byte ptr [02B62E10], 0` and the two arms around it | 1 |
| The 31-character limit and the normalisation buffer | [the section-addressing page](resource-section-addressing.md) §9, and ASTRA's width correction folded there | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on RA-1 through RA-6. **RA-4 is the one to test
first, and the one not to "fix"**: validating the base is the safer-looking choice and it changes
behaviour.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Resource — internal.** All four bodies are this category's own.
- **Presentation — MECHANICAL, and it is the largest consumer.** Several of that layer's bodies call
  the find and the two resolvers directly: section addressing is how the render side reaches authored
  data. **That fan-in is itself a fact this contract asserts** — RA-4 holds no matter who calls, which
  is what makes a non-failing lookup everyone's problem rather than this subsystem's.
- **Every other layer reached is MECHANICAL**, through the two mode resolvers' callees. *Their
  addresses are deliberately not cited: each is a hub, and naming one imports its whole edge set for
  a statement this contract does not make.*

## 17. Related

- [Resource section addressing](resource-section-addressing.md) — the mechanism
- [Contract — authored table row lookup](CONTRACT-authored-table-row-lookup.md) — S-09's contracted third
- [The authored-data table registry](authored-data-table-registry.md)

`00409780` (429 B) is the `PRF@` name-table lookup: the caller's name resolves through `00409210` against `02B62E20`, the section pointer comes from `003AB7F0` (live) or `0051EE00` (blob at `+0x10`), `dword[0] == 0x50524640` gates the scan and the `+0xC`-counted offset table walks `+0x40`-biased (form 1) or `+0x30`-biased (form 0) elements through `00409C30` matches - the first hit writes its index to `*rsi` and its count to `*r9`, all misses writing -1.

Interior anchor `0040981A` (function `00409780`).

## Cross-subsystem neighbours — batch-144 addition

**Presentation — CLIENT.** `003AB7F0` — the live-section resolver `00409780` consults — is called across the presentation layer (`003B3480`, `003B3550`, `003B38B0`, `0042FB80`, `0046E6F0`, `0051F4C0` and ~20 more), and the name-table helper `00409210` takes calls from `0041D220`/`00424D80` on that layer — the page resolves resource names into structures the presentation layer consumes.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** RA-1 to RA-6 and §2's sizes became checks at their instructions. RA-1's "one site" claim was tested by a raw
search of `.text` for the dword, with each hit decoded. Script: `Tools/analysis-kit/gfz-scripts/falsify_section_addressing.py`,
output `falsify_section_addressing.out`, image `73461d08…`, 0 BROKEN, exit 0. RA-7 and the SECTION-10 overlay rest on
their own evidence and were not re-executed; this pass does not touch the overlay's acceptance.

| # | Clause attacked | Result |
|---|---|---|
| X0 | §2 | **survives**: 101 / 89 / 41 / 86 B |
| X1 | RA-1 | **survives**: tag 0 and `0x4C4C4140` skip the tag test, and a NULL name returns 1; the immediate occurs once in `.text`, at `00409C34` |
| X2 | RA-2 | **survives**: eight dword compares, `[rcx + 0x10 .. 0x2C]` against `[r8 + 0 .. 0x1C]` |
| X3 | RA-3 | **survives**: 32-bit add then `cdqe` / `movsxd` in both resolvers |
| X4 | RA-4 | **survives**: an unsupported mode gives base 0, and neither resolver tests it before adding; the explicit guards are the null entry and offset `-1` |
| X5 | RA-5 | **survives**: the `+0x38` refresh through `+0x30` only while `02B62E10` is non-zero; mode 0 tail-jumps with `entry + 0x10` |
| X6 | RA-6 | **survives, with precision**: `-1` is the offset output of `00409780` and the one offset `004096C0` tests; the pointer finder `00409660` turns it into NULL |

No correction.
