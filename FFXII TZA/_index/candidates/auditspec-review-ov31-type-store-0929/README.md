# Review `SWE2-STRUCT-REQ-AUDITSPEC-REVIEW-OV31-TYPE-STORE-0929`: verdict ACCEPT-WITH-NARROWING (one unbounded "only")

Reviewer: SWE2-AUDIT-SPEC (non-author). This lane was run by the FABLE session's executor `73162e75` on
2026-09-29. Producer: SWE2-STRUCT, run by OPUS's Claude subagent. FABLE's `register-idless-boxes-0929` record
classified OV-31 as type-store work, and FRONTIER routed it (`FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE`). FABLE
did not author or direct the content, so the review is independent.

Reviewed: `dcdd159f0` (the `_types` rows and the record), `448d82b7e` (page section 8) and `c1254ee2e` (register
row and box flip). The type is `WidgetSingleton02AEE4C0`. Tier T1. Static only, on image `73461D08…21F8`.

## 1. The package's instrument, re-run

`ov31_title_asset.py` prints S/P/J/X/C-O-K all PASS and exits 0 (`package_rerun.out`), identical to the committed
`run.out`. `--self-test` fires all four of its mutations (S/P/J/X) and exits 0 (`package_selftest.out`).

**Gap in the self-test.** It never mutates the C/O/K census family. `census_mutants.py` fires that family with
three wrong expectations (`census_mutants.out`):

- the cell set is missing `00393A98`;
- the own set carries an invented `+0xC4` site;
- the `+0xC4` control demands a site that does not exist.

**Each makes `check_census()` return False, and the unmodified expectations return True.** So the exact-set
assertions are sensitive. The sibling census also lists `003945BB` among the `+0xC4` sites, which matches §2.

## 2. Independent re-derivation (`ov31_indep.py`, pefile + capstone only; none of the package's tools)

**Cell references: exactly nine, all rip-relative, 8-byte** (`ov31_indep.out` §A). They are `00393A88`,
`003940D2`, `003940F5`, `00394155`, `00394400`, `0039448B`, `00394500`, `00394522` and `00394543`, the same set as
the package's `CELL_REFS`. There are 0 image-base-relative references and 0 abs64/rva32 references.

- **Controls.** The sibling cell `02AEE4C8` gives 6 references, so the rip-relative scan is sensitive. A known
  image-base-relative disp (`0x462F54`) finds the `00582860` jump-table load `005828A0`, so the image-base form is
  sensitive too.
- **Disclosed.** My first pass failed the sibling control (0 references). It kept the first decode that ended at
  the right byte, which dropped REX prefixes and accepted `adc eax, imm32` shapes. I fixed the scanner to keep the
  longest decode that has a rip operand, and re-ran everything.

**The type-area census matches the package's sets exactly** (§C). Linear decode of the own handler `00394070` and
its callee `00393FF0` gives:

| field | sites (width) |
|---|---|
| `+0xC0` | `003940E3` or / `003940FC` mov (4 B) |
| `+0xC8` | `00394033` write / `00394097` read (8 B) |
| `+0xD0` | `00394050` / `003940A8` / `003940B9` (8 B) |

These are the only receiver-based accesses in those two bodies. Nothing touches self below `+0xC0`, and nothing
touches `+0xC4`. Through the cell, the consumer `003939B0` reads the asset only with `rdx` (`00393A98` byte test,
`00393AA5` qword), and `00394500` reads `+0xC0` as a dword masked `and eax,1`.

**Candidate `+0xC4` counter-examples, checked and rejected:**

- `003939B0`'s `[rsi+0xC4]` accesses (`003939FD`, `00393A6C`, `00393A7A`, `00393C1C`, `00393DF1`) are on `rsi`.
  `00393A11` stores `rsi` into `02AEE4C8`, so these belong to the `0x1D0` sibling.
- `00394530`'s `and dword [rax+0xc4], ~4` (`003945BB`) is on `rax = *(02AEE4C8)` (`0039454D`), again the sibling.
  `00394543` only tests the asset cell for null. This site is a fourth `+0xC4` sibling access. It is not in the
  package's `CONTROL_C4` list, which is a subset check, so it has no effect.

**Extent, allocation and release** (`alloc_release.out`, §D):

- `0039449F mov ecx,0xD8` → `00244F50`.
- `00244F77 cmp ecx,0x120`. The pool walk takes `0x70` = 112 slots of stride `0x120` from `*(0208EA58)`. A slot is
  free when `+0x40 & 0x4000` is clear and byte `+0xA2` is 0. Only after the walk does it fall back to
  `00244FB2 call 002497B0`. MIXED is correct.
- `00394400` is `mov rcx,[cell]; test; jne 00244F00`, a `0F 85` tail. Its only rel32 caller is `00582EB5`. The
  `rva32` hit at `0174D1D5` is odd-aligned `.rdata`.
- `00394130`'s message-18 arm is `00394155`/`00394161 call 00244F00`. `00394130` is the `0xF0` object's handler:
  it is installed at `0039464D` with `mov ecx,0xF0` (`handler_installs.out`). `00394070` is installed once, at
  `00394498`, by the `0xD8` creator.

**Jump table** (`jumptable.out`). `00582860` bounds the index at `0x12`, so messages 1–19 are covered. Message 18
maps to `00582E81`.

**The batch sends message 16.** At `00249456`, `0024953B` and `0024960B` it loads `[batch+8]`, builds
`{0x10}` and calls `[owner+0]` (`batch_notify.out`).

**Script consumer.** `00394500`'s only caller is `00511EC4`. `00511EA0`, `00511EC0` and `00511F90` sit as abs64
slots at `01F29EE8`, `01F29EF0` and `01F29F60`.

**Gates at HEAD.**

- `types_index.py --validate` gives 827 types, 9123 fields, 0 errors and 0 gaps.
- `check_questions.py` reports one inconsistency, `RC-3` on `what-the-engine-fixes-at-boot.md`. That file has
  peer edits in the working tree and is unrelated to OV-31.

## 3. Verdict: **ACCEPT-WITH-NARROWING**

The widths, both-end access sets, extent `0xD8`, the MIXED allocation and the external release chain all
re-derive from the image. Every zero in the table and the residue is bounded by the enumerated paths the page
names, and the `+0xC4` positive control is real.

**One sentence claims more than the enumerated paths support.** In section 8, the "script-facing consumer"
paragraph says: *"That bit is set only by the batch's message 16."* The single writer is established: the own
handler's message-16 arm, `003940E3`. But "only by the batch" is a claim about every sender of message 16. I
censused the send shape image-wide: `mov dword [rsp+x],0x10` followed by a handler call (`msg16_senders.out`). It
has 30 sites in 25 functions. Besides the batch's three, 16 functions send message 16 through a handler call
(`call rax`/`r8`); the other 6 are vtable calls. None of the 16 references the asset cell (`root_refs.out`).

Their receivers are the sending handler's own `self` (`mov rcx,rdi; call [rdi]`, for example `005591F4`,
`005617A7`, `002A25F6`) or a field of another object (`[rbx+0xC0]`, for example `005771A7`)
(`msg16_receivers.out`, `root_senders.out`). Five of them reference the UI root `0208EA28`, at 6 sites. I read
all 6. Five are `00246AD0(root, own object)`: `002A218E`, `0037F787`, `0055938E`, `0056150E` and `0057719B`. One
puts the root into a creation parameter block for `00241C90` (`002A2265`). None walks the root's children.

So nothing contradicts the sentence. It is unbounded all the same, because the generic walkers over the UI-root
child link were not read. That is the same bound as residue 1.

**Narrowed wording (the producer applies it):**

> That bit has one writer, the own handler's message-16 arm (`003940E3`). On the enumerated paths, message 16
> comes from the load batch's owner-notify sites (`00249456`, `0024953B`, `0024960B`). A message-16 sender
> reaching the asset through the UI-root child link is not excluded (the bound of residue 1).

The `+0xC0` row in `fields.tsv` does not say "only" and needs no change.

**Precision (no verdict effect).** The message-18 arm of `00582860` does not reach `00394520`/`00394400`
unconditionally. `00582E81 test byte [rbx+0xC4],0x10` / `je 00582EBF` first requires bit `0x10` of that
`0x5A0` widget's byte `+0xC4`. The page's "behind the nonnull predicate `00394520`" should also name this gate.

**Runtime routing (user rule 2026-09-30).** The package sends nothing new to ASTRA. Residues 1–3 are left as
static "not established" items, which is correct: they are settleable offline. The OV-29 row it cites names its
fact: title-asset callback order and cancellation in the installed game. A static reading cannot supply that,
because it depends on real IO completion. So the RT label is not being used as a reason in itself.

## Files

- `ov31_indep.py` / `ov31_indep.out`: independent A/B/C/D.
- `alloc_release.out`, `jumptable.out`, `batch_notify.out` and `handler_installs.out`: decoded bodies.
- `msg16_senders.py` / `msg16_senders.out` / `msg16_receivers.out`: the census behind the narrowing.
- `census_mutants.py` / `census_mutants.out`: the C/O/K mutants that the self-test lacked (4 of 4 as expected).
- `root_refs.out` / `root_senders.out`: the message-16 senders' references to the UI root, read one by one.
- `package_rerun.out` / `package_selftest.out`: the package's own instrument, re-run.
