# Consumption draft: ov42-action-table-binding (FABLE, 2026-10-02)

*Paths in this draft are plain backticked text. When FABLE applies the edits, it turns the packet and record paths in
the proposed page text into page-relative links in the page's usual style.*

This draft is for FABLE to apply. Nothing in it has been applied yet. Its scope is the accepted claims of
`_index/candidates/fable-review-astra-ov42-action-table-binding-1002/REVIEW.md`, with the review's six narrowings, at
the stated limits. It was drafted against the availability page at `1c4c5820f` ("FABLE: the kind-4 classifier
publishes kind 4 exactly for full 32-bit row quotients 208..225 ..."). That commit contains the 2026-10-02 OV-42
subsections from `b128c3a2c` and `1c4c5820f`. The repository HEAD was `c2fc944fe` when the draft was written, and
the page had no working-tree changes. The page has CRLF line endings. If `git log -1 --format=%h -- <page>` no longer
prints `1c4c5820f`, re-read the page before applying.

The request asks FABLE to record the binding-writer and lifetime discriminator rather than close OV-42 from pointer
identity, and to correct the AG-12 `+0x14` wording. Edit 1 does the first on the availability page. The AG-12 text
sits on an OPUS-led page, so it is routed with suggested text. So are OPUS's widths and layout contracts.

**Composition with the concurrent drafts.** Another FABLE helper is drafting additions to the same page for the
caller-row and terminal-helper packets. This draft therefore makes **no** OLD -> NEW edit to existing text. Its only
page change is one new subsection appended at the end of the page, after whatever the other drafts append.

## Candidate pages and who leads them

The lead counts come from `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | What it says | Commit subjects by prefix | Lead | Action |
|---|---|---|---|---|
| availability page (`Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`) | the kind-band subsection's invariant: "Equal row low32, equal base low32 and equal positive strides are enough ... pointer identity is not needed"; its limits keep "the descriptor's initialization and its stability" as premises | FABLE 10, OPUS 2, the rest 1 each | **FABLE** | edit 1 (below) |
| registry page (`Database/FFXII TZA/02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`), the AG-12 block | "`+0x14` u32 `+= desc`, then **resolved** through `0020E620` and stored back ...; the resolved pointer is a sub-directory ... whose entries are each rebased by `desc`"; "`+0x04` (count) and `+0x08` (stride) are not touched" | OPUS 14, FABLE 9, Database 7, SWE2-CONTRACT 3, FRONTIER 3 | **OPUS** | **route to OPUS** (suggested text below). FABLE wrote the AG-12 answer on 2026-09-12, so the correction corrects FABLE's own words on an OPUS-led page |
| register `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`, row AG-12 | "ANSWERED 2026-09-12 (FABLE) — the binder r..." | register | - | optional note at publish time (below) |

The regressions for edit 1 are `rv_binding.py`'s slot-first, plain-rebase, `+0x14`, store-list, outer-loop and
census checks, plus its three emulated countermodels and the two-level-directory run, with controls 1-17.

## Edit 1 (FABLE page): new subsection at the end of the page

Append it after the page's last line, with one blank line between. At `1c4c5820f` that line is "- Whole OV-42 stays
OPEN." (the kind-band subsection's limits). If the caller-row or terminal-helper subsections have been appended since,
append this one after them.

```
### FABLE 2026-10-02: what binding the action table writes, and why the same descriptor pointer does not fix the rows base (OV-42)

*From ASTRA's packet `ov42-action-table-binding` (`_experiments/evidence/ov42-action-table-binding/README.md`,
`ca2dd6483`), reviewed by FABLE ACCEPT-WITH-NARROWING (record
`_index/candidates/fable-review-astra-ov42-action-table-binding-1002/REVIEW.md`, 57 checks, 0 FAIL, 17 controls).
Static, plus an emulation of the original binder, its child binder and both resolver leaves on supplied
descriptors; nothing else is called.*

- **How the slot is bound.** The section registrar reads DWORD `+0x3C` of its section directory and calls a
  one-caller wrapper. The wrapper sign-extends that DWORD into the descriptor pointer D and passes it, with the slot
  `02EBF138`, to the generic section binder (`AreaData_BindAndRebaseSectionDescriptor`, the registry page's AG-12).
  In a displacement census of `02EBF138`, the wrapper's `lea` is the only instruction that forms the slot's address.
  No instruction stores to it by displacement, and every other hit reads it.
- **The slot is written first.** The binder stores D into the slot before it tests D for null and before any
  rebase. This order is not atomic initialization. Four of the five rebases then address the descriptor through a
  fresh load of that slot, not through D.
- **The rows field is rebased in place, with no guard.** For each nonzero `+0x0C`, `+0x10`, `+0x18` and `+0x1C`, the
  binder adds low32(D) and stores the low 32 bits. Zero fields stay zero, and nothing records that a field was
  already rebased. So a second bind of the same pointer moves the rows base. With D = 0x100000 and `+0x0C` = 0x20, the
  first bind stores 0x100020 and the second stores 0x200020, while the slot holds 0x100000 both times. This was
  emulated on a supplied descriptor and is not a native double bind.
- **`+0x14` holds an encoded DWORD, not a pointer.** The binder adds low32(D) to get M. It passes M through the
  encoder, which subtracts the low DWORD of the image-address base, and stores the result, even when M is 0. Only
  then, if M is nonzero, does it decode that value with `0020E600`, which adds the full QWORD base, and rebase the
  nested directory there. The directory's entries get + M, not + D. The first `count` entries go through the child
  binder at depth 0, and the last is rebased in place. When the base's upper half is nonzero, the address the
  binder visits differs from M (emulated).
- **What it does not write directly.** None of the binder's own seven stores uses displacement 4 or 8, so it never
  stores the row count `+4` or the stride `+8` directly. A nested directory that overlapped the header could still
  write them. In a constructed model, a count-0 directory at D+4 adds M to D+8 and turns a stride of 60 into 64.
  That model is not a stock action table.
- **The image-address base has a write route.** Apart from the two resolver leaves, which read the base, no
  instruction accesses it by displacement. But a texture-bind leaf's signed 16-bit index can store into it
  (published `de52023ee`, re-read here).

**What this changes for OV-42.** The kind-4 bound in the kind-band subsection needs equal low32 rows bases and equal
positive strides. Pointer identity of the slot does not supply them: a rebind of the same pointer moves `+0x0C`, and
a nested overlap or a base write could move the stride or the decoded base. The subsection's own wording, "pointer
identity is not needed", already avoids the shortcut. This subsection records why the shortcut would fail.

**Limits kept.** These limits are ASTRA's and FABLE's.

- No writer, alias, callback or rebind is excluded in the window from the current-row construction to the kind-4
  quotient. The next discriminator is the resource registration, reset and reuse paths that reach the registrar, and
  any writer of `+0x0C`, `+8` or the base during that window. A direct-reference census, pointer identity or an empty
  live trace cannot replace that proof.
- Natural double binding, a stock header overlap, and a base write during combat are not shown. The three supplied
  models are arithmetic through the original bytes, not native runs.
- Valid, separate slot and descriptor storage, the Win64 ABI and an unchanged base between paired encode and decode
  reads are premises.
- Whole OV-42 stays OPEN.
```

### Citations and the neighbour gate

The new text has two 8-digit tokens: `0020E600` (a function entry, cited 11 times on the page at `1c4c5820f`) and
`02EBF138` (a `.data` slot, cited 13 times). Neither is new. Nothing in `.text` is cited by an interior address.
`de52023ee` is a commit id, not an address.

These are **named by role** and not by address, so that no new caller or callee edges are imported:

- the registrar `00236C30` ("the section registrar");
- the slot wrapper `00237FC0` ("a one-caller wrapper");
- the binder `003845F0` ("the generic section binder", with its ledger name);
- the child binder `003846F0` ("the child binder");
- the encoder leaf `0020E620` ("the encoder");
- the texture-bind leaf `00210570` ("a texture-bind leaf");
- the data cells `0208E680` ("its section directory") and `01F83530` ("the image-address base").

Their addresses are in the review record. The neighbour pre-check (`xlayer.py`) was **not** run for this draft.
Before publishing, FABLE should run `xlayer.py --only 0020E600` and the full-page edge diff on a staged copy of the
page.

## Route to OPUS: the AG-12 block on the registry page

The registry page is OPUS-led (OPUS 14, FABLE 9). The packet asks for the AG-12 `+0x14` wording and the `+4`/`+8`
preservation claim to be corrected. Narrowing 1 adds a second wrong phrase in the same row. Placement is OPUS's
choice. FABLE wrote the original answer, so FABLE concurs with this correction in advance. Suggested OLD -> NEW,
against the page at `f81176bae` (LF line endings; both OLD blocks were checked to be exact substrings of the page):

OLD (the table row):

```
> | `+0x14` u32 | `+= desc`, then **resolved** through `0020E620` and stored back (`00384647`–`00384662`); the resolved pointer is a sub-directory `{u16 count; u32 entry[count + 1]}` whose entries are each rebased by `desc` — the first `count` through the child binder `003846F0(&entry, rebased, 0)`, the last in place (`00384680`–`003846C7`) | |
```

NEW:

```
> | `+0x14` u32 | `+= desc` ~~, then **resolved** through `0020E620` and stored back~~ giving M, then **encoded** by `0020E620` (M minus the low DWORD of `01F83530`) and that encoded DWORD stored back, even when M is 0 (`00384647`–`00384662`); if M != 0 the sub-directory `{u16 count; u32 entry[count + 1]}` is reached by decoding the stored value with `0020E600` (zero-extend + the full QWORD `01F83530`), and its entries are each rebased by ~~`desc`~~ **M** — the first `count` through the child binder `003846F0(&entry, entry + M, 0)`, the last in place (`00384680`–`003846C7`) *(corrected 2026-10-02, FABLE review of ASTRA `ov42-action-table-binding`: `0020E620` is the encoder, not a resolver; EBP = M at `003845F0` + 0x6B feeds both the child argument + 0xB9 and the in-place add + 0xC9)* | |
```

OLD (the paragraph after the table):

```
> `+0x04` (count) and `+0x08` (stride) are not touched — they are values, not offsets.
```

NEW:

```
> `+0x04` (count) and `+0x08` (stride) are not ~~touched~~ written by any of the binder's own stores — they are values, not offsets. *(narrowed 2026-10-02, FABLE review of ASTRA `ov42-action-table-binding`: that is the direct store footprint, not whole-call preservation; a nested directory overlapping the header can write them through the in-place add, e.g. a count-0 directory at `desc + 4` adds M to `desc + 8`.)*
```

Suggested addition for OPUS's width and layout contracts (placement OPUS's):

```
- Section binder `003845F0` (FABLE review of ASTRA `ov42-action-table-binding`, 2026-10-02,
  _index/candidates/fable-review-astra-ov42-action-table-binding-1002/REVIEW.md):
  - entry: RCX = slot, RDX = descriptor; the action-table caller `00237FC0` passes RDX = movsxd of DWORD
    directory +0x3C (sign-extended) and RCX = &02EBF138.
  - `*slot = desc` (QWORD, + 0x4) before the null test and every rebase; +0x10/+0x18/+0x1C/+0x14 are then addressed
    through reloads of *slot (+ 0x21, + 0x32, + 0x43, + 0x54), +0x0C through RDX.
  - rebase is NOT idempotent: x != 0 -> low32(x + low32(desc)); no already-rebased flag.
  - widths: encoder `0020E620` reads DWORD [01F83530] (sub ecx); decoder `0020E600` reads QWORD [01F83530]
    (zero-extend + add rax). Only the low32 round trip is exact; full 64-bit identity holds only if the
    QWORD's upper half is 0.
  - preconditions: valid, separate slot and descriptor storage; sub-directory storage disjoint from the header.
```

## Optional: register row AG-12 (at publish time)

Append this to the AG-12 status cell and keep its current text:

```
2026-10-02 (FABLE review of ASTRA ov42-action-table-binding): +0x14 stores the ENCODED DWORD (0020E620 is the
encoder), the nested directory is reached through 0020E600, and its entries are rebased by M (the rebased +0x14), not
by desc; +4/+8 are untouched by direct stores only. Routed to OPUS for the registry page.
```

Escape any literal `|` before writing it into the row.

- consumer: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` OV-42 subsections - revised-here (edit 1)
- consumer: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` AG-12 block - routed to OPUS

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

run: `rv_binding.py` at HEAD c2fc944fe (57 checks, 57 PASS, 0 FAIL, 17 controls)
