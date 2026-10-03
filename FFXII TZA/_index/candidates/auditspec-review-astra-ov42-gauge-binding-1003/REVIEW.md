# SWE2-AUDIT-SPEC review: ASTRA OV42 stat-bar callback binding and local effect boundary

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-OV42-GAUGE-BINDING-1003` (reviews `ASTRA-PUBLISH-OV42-GAUGE-AND-CHECKPOINT77-1003`) · reviewed at HEAD `99e830a39`
Package: `_experiments/evidence/ov42-gauge-callback-binding/` (publisher commit `64cb2c0c3`, unchanged since). Image pin `73461d08…21f8`, base `0x120000`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The verdict is bounded to the package's own limits: STATIC_ONLY, the four named bodies (822 B), and the stated ABI, private-stack and non-overlap premises. Every established local fact holds at the bytes. The OPEN items stay OPEN: the actual initialized value at `+0x38`, natural reachability, reuse and lifetime, scheduling, resource binding, presentation, and transitive helper effects. The prover's call-set check does not see jump-form transfers. A census written for this review shows the image has none in these bodies, so no claim changes. The repair is in the notes.

## SWE2-AUDIT-SPEC identity and integrity

- `Database/Tools/work/exe/FFXII_TZA.exe` hashes to `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`. The optional header ImageBase is `0x120000`.
- `manifest.json` hashes to `03ce4f39…116d0e` and lists 65 members. All 65 match their committed bytes and sizes. The only unlisted file is the manifest itself, so 66 package paths are tracked. The 93-path count is the whole commit `64cb2c0c3`. As the request says, this integrity check is not semantic acceptance.
- `prove.py` hashes to `91033a44…4435a`, the producer driver named on the board.

## SWE2-AUDIT-SPEC physical extents (`.pdata`, read for this review)

| entry | RUNTIME_FUNCTION records | unwind | bytes |
|---|---|---|---|
| `00296360` | one root `296360-296448` | `01D53190`, flags 0 | 0xE8 = 232 |
| `00297C10` | root `297C10-297C85` (`01D790EC`, flags 0) + chained `297C85-297CE2` (`01D6EB78`) + chained `297CE2-297D04` (`01D6EB8C`); both chains point to the root | flags 4 | 0xF4 = 244 |
| `003F89C0` | one root `3F89C0-3F8A23` | `01D7945C`, flags 0 | 0x63 = 99 |
| `002973E0` | one root `2973E0-2974D7` | `01DE0B0C`, flags 0 | 0xF7 = 247 |

- The three registration bodies total 575 B, and the four bodies total 822 B, as stated.
- `extents-01.json` records the same three chained fragments for `297C10`, with the chain-footer bytes. The `.rdata` RVA hits at `01D6EB80`/`01D6EB90` are exactly those chain footers.
- The handlers are single roots: `29B7D0-29B802` and `29B810-29B862`.

## SWE2-AUDIT-SPEC re-derivation from the shipping image (`disr.py` / capstone, not the producer's tools)

- **`00296360`: registration leg.**
  - The unregister leg runs first when dword `0209C2F0` != 0: `3F8A30` on `0209C240`/`0209C298`, then the flag is cleared.
  - The admission guards are `edi` (= incoming `edx`) != 0, `rbx` (= incoming `rcx`) != 0 and dword `[rbx+4]` != 0. All three branch to the epilogue with `je`.
  - The admitted leg makes two calls to `3F89C0`, each with `rdx=0`, `r8d=0` and `r9=rbx` (context):
    - `rcx=0209C240` with `[rsp+20h]=29B7D0` (`2963C1` lea, `2963D1` store, call `2963E2`);
    - `rcx=0209C298` (= `0209C240+58h`) with `[rsp+20h]=29B810` (`2963E7`, `2963F4`, `296402`).
  - It then links both through `3F8A50` and stores `rbx` to `0209C288`/`0209C2E0`, which are the context `+48h` of each half.
  - **Holds.**
- **`00297C10`: the free and matched paths.**
  - The table holds four rows of stride `0xC0`: `rdi = rax-7Eh` for `rax = 0209BFBE … 0209C1FE`, bound `r8 = 0209C2BE`, giving rows at `0209BF40`, `0209C000`, `0209C0C0` and `0209C180`.
  - The first loop finds a row in which either half's word `+26h` has bit 2 set (`test [rax-58h],2` / `test [rax],2`) and dword `+0B0h` equals `[rsi+4]`. Such a row jumps `297C45 je 297CE2`.
  - The second loop takes the first row in which both halves have bit 2 clear. It runs `297C7E…297CD8`: `3F89C0(row, 0, 0, rsi, 29B7D0)` and `3F89C0(row+58h, 0, 0, rsi, 29B810)`, then `3F8A50` on each half. With no free row, it returns 0 without writing.
  - The matched tail `297CE2-297D04` has no call and no jump. Its only non-stack writes are qword `[rdi+48h]`, qword `[rdi+0A0h]` and dword `[rdi+0B0h]`. Nothing writes `+38h` or `+90h` (`=58h+38h`).
  - **Holds.** The callback identity of a matched row is whatever it held before; H2 is supported locally.
  - Note that `0209C240`, the record `296360` uses, is the slot just past this four-row table. The scan bound excludes it.
- **`003F89C0`: initializer.**
  - The prologue is three home-slot stores, then `push rdi` and `sub rsp,20h`, so the current SP is entry SP - 28h. `[rsp+50h]` is therefore entry `SP+28h`, the caller's `[rsp+20h]`: the fifth argument.
  - It memsets 0x58 bytes, then: `or word [rsi+26h],1`; `mov [rsi+38h],rax` (qword callback); `mov [rsi+40h],ebx` (dword, = incoming `r8d`); `mov [rsi+48h],rdi` (qword, = incoming `r9`).
  - It then runs `test rax,rax / je 3F8A0E`, so a NULL callback skips. For a non-NULL callback it does `r8=rbp` (incoming `edx`), `edx=0`, `rcx=rsi` and **`call rax`**: a synchronous call with event 0, not a tail jump.
  - **Holds.**
- **`002973E0`: consumer.**
  - The four direct calls are `297414→271960`, `297430→272730`, `297450→2726C0` and `297498→2727C0`.
  - Every `jcc`/`jmp` target is inside `2973E0-2974D7` (`2974C5`, `297437`, `297455`, `2974C0`, `297482`, `297493`, `29748F`). There is no `call reg`, `call [mem]` or `jmp reg/[mem]`.
  - Its own non-stack writes are word `[rbx+14h]` (`29749F`), dword `[rbx+50h]` (`2974A8`) and RMW word `[rbx+26h]` (`2974C0`).
  - **Holds.** H3 is refuted for this body. Transitive effects through the four helpers are not examined, and stay OPEN as the package says.
- **Synchronous boundary (the conditional `synchronous_limit`).**
  - `0028F1F0` builds the pair `{edx, r8d}` at `[rsp+20h]`. It picks the record (via `296280`, or the default via `2962C0` gated by id `+0B0h`), or record+58h when `r9d` != 0, and calls `3F8980` at `28F246`.
  - `3F8980` calls a non-NULL `[rcx+38h]` with `edx=1` and `r8=&pair`.
  - `29B7D0` (event 1) and `29B810` (event `edx-1==0`) each call `2973E0`.
  - So the claim that a bar update can run synchronously before the caller continues holds, conditional on a non-NULL installed handler. That conditional form is how the package states it.

## SWE2-AUDIT-SPEC raw reference index (image-wide, written for this review)

The census covered every byte offset of all sections. It looked for E8/E9 rel32, `0F 8x` rel32 and rel8 `EB`/`7x` targets, rip-relative disp32 at end offsets +4/+5/+6/+8, absolute qwords, and 32-bit image-relative dwords (which also covers `[base+disp]` with base `0x120000`). The targets were `2973E0`, `3F89C0`, `29B7D0`, `29B810`, `296360`, `297C10` and `3F8980`.

- **`2973E0`:** only `call` at `29B7EA` (in `29B7D0`) and `29B851` (in `29B810`), plus its `.pdata`. There is no jcc, table, qword or RVA reference. Handlers call the consumer, never the reverse.
- **`29B7D0` / `29B810`:** referenced only by the four LEAs `2963C1`, `2963E7`, `297C7E` and `297C9F`, plus `.pdata`. There is no qword or RVA table entry.
- **`3F89C0`:** exactly four direct callers, the four sites above. `3F8980` has one direct caller, `28F246`.
- **Consequence for consumers (not claimed by the package; stated here as bounded corroboration):**
  - Every callback value that `3F89C0` installs is `29B7D0` at a row or default half, or `29B810` at the `+58h` half.
  - No `+38h` writer outside `3F89C0` was swept, for example by direct store or bulk copy. "Actual initialized +38" therefore stays OPEN.
- **Event 0 is a no-op for both prescribed handlers.** `29B7D0`: `cmp edx,1 / jne → xor eax,eax; ret`. `29B810`: `sub edx,1` gives -1, `cmp edx,1 / jne → xor eax,eax; ret`. The initializer's synchronous `event 0` call therefore runs no bar update for these handlers. The package does not claim one. Consumers should not read the registration call as an update.

## SWE2-AUDIT-SPEC reproduction (disposable copy in the reviewer scratchpad)

The copy kept the package at its repository-relative depth, with copies of the pinned EXE and the reviewed adapter `reg_tracking.py` (`5fcc6484…`). It ran under the analysis venv python, Python 3.14.6 with capstone 5.0.7.

- `prove.py result-rerun.json`: exit 0, same stdout. The result is **byte-identical** to the retained `result-01.json`.
- `control.py`, after removing the retained control outputs from the copy: exit 0, same stdout. All three CLI refusals are the same as retained, each with exit 1, no `refused.json`, and the same final stderr line:
  - `target-extent-incomplete`: "required complete current extent artifact";
  - `target-wrapper-incomplete`: "required complete current capture wrapper";
  - `target-capture-failed`: "required successful capture-target-01".
  - `control-result-01.json` differs only in `artifact_cases[].inputs`. The retained run predates `README.md`, `manifest.json`, `environment-01.json` and the `control-01.*` receipts, and an earlier `KNOWN-PRECONDITIONS.md`. This is administrative, not a semantic difference.
- **Control sensitivity (in-memory harness over `derive()`).** The four producer source controls are refused, but three of them (`2963E7` args, `297C45` args, `3F89F4` args) trip the literal `ops` pin table, not the semantic checks they are labelled for. Extra mutations written for this review test those checks:
  - LEA `rip_target` only (text kept), `2963E7→29B7D0`: **refused** ("actual LEA callback identity changed").
  - Callback store displacement only (text kept), `3F89F4` `+38→+40`: **refused** ("callback store role/layout changed").
  - The matched tail gains `call 3F89C0`: **refused**. The matched tail gains a write to `[rdi+38h]`: **refused**. The consumer gains a write to `[rbx+38h]`: **refused**.
  - Consumer `297435 jmp` retargeted to `29B7D0` (a direct tail transfer to a handler): **ACCEPTED**.
  - Consumer `297435` changed to `jmp rax`: **ACCEPTED**.
  - Matched tail `297CFE` changed to `jmp 3F89C0`: **ACCEPTED**.
  - The prover's "complete consumer call set", "no indirect call" and "matching-row tail … calls initializer" checks filter on `mnemonic == 'call'` only. The shipped bodies contain no such transfer (see the re-derivation), so the facts stand on this review's transfer census, not on the prover alone.

## SWE2-AUDIT-SPEC claims audit

- **EXP243** is described as zero `3F8980` hits under a BSS-zero fixture (`EXP-243-gauge-event-post-28F1F0-exec.md`: early-out at `28F24B`, `3F8980` "×0"). The package states that this is not a control for initialized callbacks, and credits none of its executions. **Correct.**
- The canonical naming of the handlers is consumed, not re-derived or re-credited, and the prepared handler capture driver was not run. **Correct.**
- `result-01.json` `remaining`, README "Controls and limits" and the manifest `limits` keep natural state, transitive effects, lifetime, scheduling, resource binding and presentation OPEN. **No overclaim found.**

## SWE2-AUDIT-SPEC notes (non-blocking repairs)

- **Prover transfer check.** In `derive()`, take the consumer and matched-tail transfer sets over every `call`/`jmp`/`jcc` whose target leaves the body, plus every register or memory operand transfer. Require the four helper calls and no other exit except `ret`. Add the three accepted mutations above as source controls with FAILS expected.
- **Control labelling.** Each semantic control should mutate only the field its check reads (`memory.rip_target`, `memory.displacement`), so that the refusal reason names the semantic check rather than the text pin.
- **Control input snapshot.** Re-running `control.py` now records seven more input files and a changed `KNOWN-PRECONDITIONS.md`. Either re-run it after the final edits or note that the inputs list predates them.
