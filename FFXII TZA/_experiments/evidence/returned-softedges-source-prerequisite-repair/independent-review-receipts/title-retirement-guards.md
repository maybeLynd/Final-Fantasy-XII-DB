# SWE2-AUDIT-SPEC review of ASTRA's title retirement local guards (title-retirement-local-guards final02 at aa84f3faa): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75), 2026-09-30. Producer: ASTRA. Reviewed:
commit `aa84f3faa`, packet [`title-retirement-local-guards/`](../../../_experiments/evidence/title-retirement-local-guards/README.md)
(final result `title-retirement-local-guards-result-02.json`, controls `title-retirement-input-controls-02/`).
Image sha256 `73461d089620…21f8`, static reads only. The prior title sender review/census was not re-run, as asked.

| request | reviewed task | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-TITLE-RETIREMENT-GUARDS-0930 | ASTRA-PUBLISH-TITLE-RETIREMENT-GUARDS-0930 | `aa84f3faa` | ACCEPT |

**Why an image re-derivation was needed.** `prove-title-retirement-guards.py` reads **no EXE bytes**. It trusts the
retained listing's mnemonics under two hash pins, so every clause below was decoded again from the shipping image
(`rg_indep.py` / `rg_indep.out`).

**Clause by clause:**

- *`0024A680` is 141 B in full.* Decoded from the image: 141 bytes, sha256 `d9acb85e3fd2…2a78d`, equal to the pinned
  body.
- *Membership loop.* `0024A695 lea rax,[rip+0x1e44ee4]` gives `0208F580`. Each iteration tests two slots (`cmp`/`je`
  at `0024A6A2` and `0024A6AB`), adds `0x48` twice and `r8d` by 2, while `r8d < 0x40`. An odd hit takes
  `inc r8d` (`0024A6C0`); an even hit jumps straight to the bound test. `cmp r8d,0x40` / `je 0024A702` then skips
  every effect. That is 64 records × 0x48, and `0208F580 + 64*0x48 = 02090780`, exactly the counter.
- *No local active-bit-0x20 or pending-ticket rejection.* The body touches `[rbx+0x38]` twice: the read at
  `0024A6CE`, which is masked `& 0x3F00` and so excludes 0x20, and the store `and [rbx+0x38], 0xFFFFFFDF`. There is no
  test of 0x20, no access to the ticket pool, and no other flag read.
- *Normal path: clear bit 0x20, then DEC.* The last effects are `0024A6F8 and [rbx+0x38],~0x20` and
  `0024A6FC dec dword [rip+…]`, which resolves to `02090780`.
- *Release predicates.* `00181610` runs first; it calls `001B1C00`. Then, if `flags & 0x3F00 == 0x1400` and `[+0x10]`
  is non-null, it calls `003697F0` with `[+0x10]`. When mode (`edi`) is non-zero, it calls `003697F0` with `[+0x18]`
  without a null test of its own. `003697F0` opens with `test rcx,rcx`/`je ret`,
  so it handles NULL.
- *No local pointer clear.* The only stores in the body are the `rbx` spill, the `and` and the `dec`; nothing writes
  `+0x10` or `+0x18`.
- *NULL and invalid addresses return.* `test rcx,rcx`/`je 0024A70C ret`, and a non-member address goes to `0024A702`,
  the epilogue. The function sets no meaningful return value: after a miss `rax` is the loop cursor `02090780`.
- *Final02 `00249580`.* It starts `lea rax,[rip+…]` = `02090790`, tests `byte [rax],1`, steps `add rax,0x20`, and
  loops `cmp edx,0xC`/`jl`. It returns 0 when all 12 are busy, and otherwise zeroes and sets bit 0 and stores `rcx` at
  +8. The ticket pool `02090790..02090910` sits 16 bytes past the counter, separate from the resource pool.
- *Repeat eligibility and DEC are local and conditional.* The address test is membership only, so after the local
  0x20 clear a recognized record still passes, and a normal repeated call reaches the DEC again. No idempotence,
  free-safety, reentrancy or cancellation claim is made.

**Corroboration beyond the packet.** The counter `02090780` has exactly two references in the image, both
rip-relative, with 0 image-base-relative:
- `0024A58A inc` in `0024A4E0`, the record allocator, which also sets `[+0x38] |= 0xA0`;
- the DEC at `0024A6FC`.

`002493D0`, the title factory in the sibling routing review, stores the `0024A4E0` result at member+0x18. The caller
`00394097` passes `[rbx+0xC8]` with `edx = 1`, and the only `+0xC8` operand in `00394070` (190 B) is that load, so
it does not clear `+0xC8`. All 29 retained SECTION04 bodies hash equal to the EXE bytes (R9).

**Final02 input guards.** Several things are refused before any guard is derived:
- a changed manifest or disassembly generation (two sha256 pins);
- a wrong-build manifest;
- a gap or mixed bytes in any of the five bodies (the body sha is rebuilt from the listing);
- the rip targets `0208F580` / `02090780` / `02090790`, which are decoded from the encoded displacement, not from a
  comment.

**Re-run.** The positive was run to a fresh `rerun_result.json` and is **identical** to
`title-retirement-local-guards-result-02.json`. The packet's `control-title-retirement-inputs.py` writes into the
packet, so its two cases were re-created in a scratch directory by `rerun_refusals.py`:
- missing-manifest: exit 1, no result;
- same-count-changed-mask: exit 1, no result, "retained input generation changed".

The packet stayed clean before and after.

**Controls.** The same-count mask mutation is caught by the **hash pin**, not by the semantic gate, so on its own it
does not show that `need()` can see the change. A reviewer control set the pin to the mutated file's hash so only
`need(0x24a6d1, 'and', 'eax, 0x3f00')` could refuse. It refused: exit 1, "required original operation changed
0x24a6d1". So both layers are sensitive. The capture's three access-role controls (store / LEA / RMW) test the
op_kind adapter; they cannot detect a wrong range selection.

**Correction wording for ASTRA** (inbox line 8 and the request text):
> The manager/key preparation capture is 167 bytes: `001B1C00` 8 B (`mov rax,[01F811E8]`; `ret`) plus `001B1440`
> 159 B, ending with `ret` at `001B14DE` (end-exclusive `001B14DF`). It is not 166 B. It remains preparation only.

**Limits kept:** local guards only. Transitive `002495C0` cancellation and drain, natural pending teardown, the
`00181610` → `001B1C00` → `001B1960` tracker effects, `003697F0` free effects and overall counter integrity all
stay OPEN.
