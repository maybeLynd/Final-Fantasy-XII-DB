# SWE2-AUDIT-SPEC review of ASTRA's title member-notification route (title-member-notification-routing at 0fcf9349e): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75), 2026-09-30. Producer: ASTRA. Reviewed:
commit `0fcf9349e`, packet [`title-member-notification-routing/`](../../../_experiments/evidence/title-member-notification-routing/README.md)
(final result `title-member-notification-result-03.json`, controls `title-member-prerequisite-controls-02/`). Image
sha256 `73461d089620…21f8`, base `0x120000`, static reads only.

| request | reviewed task | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-TITLE-MEMBER-NOTIFICATION-0930 | ASTRA-PUBLISH-TITLE-MEMBER-NOTIFICATION-0930 | `0fcf9349e` | ACCEPT |

**Clause by clause** (own decode of the image with `tk.py`, own raw sweeps; figures copied from `mn_indep.out`):

- *Both title request factories.* `00393FF0` (118 B) makes exactly four direct transfers: `00393FFD` → `00249580`,
  `00394029` → `002493D0`, `00394048` → `00249320`, `00394061` jmp → `00249410`. `002493D0` calls `00249210` at
  `002493DE`; `00249320` calls it at `00249332`. Both factories have other callers (21 and 4 raw sites, and `00249210`
  has 25), so "the title factories" means these two call sites, not a census of every user of `00249210`.
- *Descriptor `002495C0` and the low32 member context.* `00249274 lea rax,[rip+0x345]` resolves to `002495C0` and is
  stored at `[rsp+0x40]`. `00249286` stores the member pointer's low 32 bits (`ebx`) at `[rsp+0x38]`. The block is
  passed as `[rsp+0x20]` into `002492F3 call 0032E620`, and `002492F8 inc word [rbp+0x18]` follows. An all-`.text` rip
  sweep finds exactly **one** instruction forming `002495C0`: `00249274`, with no raw-only hit and no relocation.
- *Member callback before the done-count increment; ordinary owner call.* `002495C0` (147 B) does
  `movsxd rbx, ecx` (the 32-bit context sign-extended), then `call [rbx+0x10]` at `002495E8` if it is non-null, then
  `inc word [rdi+0x1A]` at `002495ED` (`rdi` = member+0 = ticket). The owner notification needs three things: sealed
  (`test byte [rdi],2`), equal (`[rdi+0x1A] == [rdi+0x18]`) and custom-zero (`[rdi+4] == 0`). Then `rcx = [rdi+8]`,
  message `0x10` is written at `[rsp+0x20]`, `rdx = &msg`, and the call is `call [[rcx]]` at **`00249632`**. After it
  come `and [rdi], ~1` (`00249634`) and `and [rbx+0x20], ~1` (`00249637`).
- *The separate watcher factory.* The only instruction forming `00248700` is `002491DC` inside `002491B0`, which calls
  `00244F50`. `00248700` calls `002494F0` at `00248746`. The old sites belong to other bodies: `0024947D` is in
  `00249410` and `0024955D` is in `002494F0`. Neither the watcher factory nor its handler forms `002495C0`, so it does
  not replace the descriptor.
- *The 19-entry controller table, from `cmp 0x12`.* `00582889 dec eax` / `0058288E cmp eax,0x12` / `ja 00582F24`,
  then a jump through image-base-relative dwords at `00582F54`, which gives 19 entries for messages 1..19. Entry 17,
  message 18, is `00582E81`. The decoded body ends at `00582F50 ret` (fsize 1777), so the table is data after the code.
- *Checker controls and final sibling inputs* reproduce; see **Re-run**. Failed capture01 and the `00394026` guess
  are history only, and nothing semantic rests on them.

**Precision the packet leaves implicit** (non-blocking; suggested sentence for ASTRA below):

1. Both factories install the member-specific callback themselves, **after `00249210` returns**:
   - `002493D0` writes `[m+0x10] = 00249670` (→ `0024A1D0`) and `[m+0x18]` = the `0024A4E0` result;
   - `00249320` writes `[m+0x10] = 00249660` (→ `002A00F0`).

   Because `002495C0` skips a null `[m+0x10]`, "callback first" holds for a completion that runs after `0032E620`
   returns. The factory install and the `+0x18` increment both follow the submit, so a completion *inside*
   `0032E620` is outside this route.
2. On the custom-nonzero branch (`[ticket+4] != 0`) the code calls `[ticket+0x10]` and **skips** the ticket bit-0
   clear at `00249634`. Only the member bit at `+0x20` is cleared there.
3. The member context is 32 bits, sign-extended. Members come from the pool whose pointer is at `0208F578` (0x30
   entries × 0x28). The route assumes those addresses survive the round trip, and the packet does not test that.

**Re-run.** `prove-title-member-notification.py` was run to a fresh `rerun_result.json` and is **identical** to
`title-member-notification-result-03.json` on all 15 keys, including the input and retained-input hashes.
`exercise-title-member-prerequisites.py` was run into a scratch directory outside the repo: status COMPLETE,
positive exit 0 with a result; the four other cases (incomplete wrapper, failed role, missing source, changed
instruction bytes) exit 1 with no result (`rerun_controls_summary.txt`). The packet stayed clean before and after.

**Controls.** The five invocation cases are sensitive to their defects: each mutates exactly the prerequisite it
names. The two witness mutations (a changed descriptor displacement, `00249632` turned into a `nop`) do exercise the
witness table. Four of the six `controls` keys (`member_callback_is_2495c0`, `watcher_factory_is_distinct_2491b0`,
`requested_count_18_done_count_1a`, `controller_message18_bound`) are literal `True`. Their substance is checked
elsewhere, by the witness table, the `rip_target` asserts and the table-bytes check, but the names overstate them as
tests. Retained-body integrity is real: the checker re-hashes `00393FF0` / `00394070` / `00249580` against the image.
All 29 retained bodies match the EXE; see the sibling review's `rg_indep.out`, R9.

**Suggested wording for ASTRA** (append to the README's routing paragraph):
> The member-specific callback at member+0x10 is installed by each factory after `00249210` returns (`002493D0`:
> `00249670`, with +0x18 from `0024A4E0`; `00249320`: `00249660`), and `002495C0` skips it when null. The custom
> (`ticket+4` nonzero) branch calls `ticket+0x10` and does not clear ticket bit 0. The member context is a
> sign-extended 32-bit value.

**Limits kept** (as stated by ASTRA): no natural pending teardown, no post-teardown delivery, no cancellation or
drain, no exclusion of watchers created by omitted services, no lifetime safety, no full OV29 closure. This review
adds no runtime observation.
