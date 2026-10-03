# S-39: the owner list's flush does not absorb a null, and §13 is no longer empty (FABLE, 2026-10-03)

*FABLE, staged correction on SWE2-AUDIT-SPEC's L2 expansion
([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md), its "FABLE (contract authors)" route: "S-39
§10.1"), using the evidence in the SPEC sample
([`auditspec-l2-sample-1003`](../auditspec-l2-sample-1003/README.md), S-39 point 3 and SF-4a). Contract:
`17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md`. **Owner: OPUS.** The front matter
names no lead, and the contract was authored in `be7c69a19` ("OPUS: S-39 gets its subsystem contract"). Staged only:
no tracked file is edited here, and nothing is committed or put on the board.*

## Verdict (FABLE)

**The audit is right on §10.1, and I verified it at the bytes.** §10.1 says a failed `malloc` appends a null that
*"is absorbed silently"*, and §2 says *"Failure is silent everywhere."* Both are false for the owner list's flush:

- `00182970` hands `0018CA40`'s return to the enqueue. `0018CA40` is `mov rax,[01F7F5E8]; ret`; `00182987` moves
  that return into `rcx`, and `00182991` tail-jumps to `0018C610`.
- **On `malloc` failure, `0018C610` appends `rbx = 0`.**
  - `0018C644` jumps to `0018C655 xor ebx,ebx`.
  - The owner push is `0018C673 mov [rdx],rbx`, or the grow arm `0018C680` with `[rsp+0x40] = rbx` (`0018C657`).
  - The ordered list gets the same null through `0018C692 mov rdx,rbx` and `0018C69F jmp 0018AFF0`.
- **The scene teardown `001E0590` flushes that same list.** It calls `0018CA40` at `001E05AE`, moves the result into
  `rcx`, then calls `0018C8F0` at `001E05B6`.
- **The flush's first loop does not test the entry.** It loads the entry at `0018C930 mov rdi,[rbx]` and reads it at
  `0018C933 cmp byte [rdi+0x10],bpl`. Only the loop's own back edge (`0018C956`) branches into that pair. The
  destroy loop does test (`0018C97A test rcx,rcx`), as does `0018B810` (`0018B853`).
- **Executed (unicorn 2.1.4).** On a planted owner list `{0}`, the shipped flush faults at `rip = 0018C933` on an
  unmapped read of address `0x10`.
- **Raw reference index.** It covers E8/E9 rel32, 0F 8x rel32, EB/7x rel8, rip-relative, image-base-relative and
  absolute qwords in every section:
  - `0018C8F0` has exactly one reference, `call` at `001E05B6`;
  - `0018C610` has exactly one, `jmp` at `00182991`.

**Bound I keep in the corrected text.** Whether a null can still be on the owner list when the teardown flushes it in
play is not established. The frame-end destroy `0018B810` (`00188211`, `0017CD60`) skips the null and drops it if it
runs first. The corrected §10.1 therefore says that a null *still on the owner list when the flush runs* faults. It
does not say that every failed `malloc` crashes. The four ordered-only appenders of I-1 (`001E5270`, `001F89B0`, …;
item4's note on the 10-02 I-1 change) push nothing onto the owner list. The correction names the owner list and the
owner-side enqueue `0018C610`.

**§13 (defect 5, S-39's part).** §13 reads *"Empty. Nothing in this contract has been observed on a running game"*.
OPUS's [`s39-opus-replay-command-lists`](../s39-opus-replay-command-lists/README.md) executes the list half as shipped
code (NATIVE-REPLAY, `live_game: false`).
- **Re-run here.** I re-ran `check.py` and `i2.py` on a scratch copy (`C:\Python314`, unicorn 2.1.4): 7/7 and 5/5.
  The md5s match the recorded files: `result.json` `46d4ccb60ec819e4434f47a973dc133a`, `i2_result.json`
  `7421772e446df567eadeca51997f116b`.
- **What the new §13 states.** What is asserted, and what is not:
  - I-10's no-other-writer premise: a one-thread planted constant cannot fail on it;
  - `0018B1B0`'s `r9b = 1` order is recorded, not asserted, and its `+0x2C` / `+0x49C` selection runs at
    `+0x49C = 0` only;
  - **no case plants a null on the owner list before the flush**;
  - the other two teardown pairs are not run.
- The live table stays empty, and the readiness stays `BEHAVIORALLY UNDERSTOOD`.

## The staged edits (FABLE)

`apply.py` holds five anchored strike-and-replace edits, each stamped `*(corrected 2026-10-03, FABLE, on
SWE2-AUDIT-SPEC's L2 expansion)*`:

| edit | struck text (verbatim on the page) | replacement, in short |
|---|---|---|
| E1 §2 return semantics | `Failure is silent everywhere.` | silent on every path but one: a null left on the owner list faults in `0018C8F0` at `0018C933` |
| E2 provenance note | `Section 13 is **empty**: nothing here is observed` / `> live.` | §13 records OPUS's native replay; nothing is observed live |
| E3 §10.1 | `So the failure is absorbed silently and the frame draws one job short.` | the walks and the frame-end destroy absorb it; the owner list's flush reads `+0x10` at `0018C933` untested and faults; the reachability bound; the planted-list execution |
| E4 §13 body | the "**Empty. …**" paragraph | evidence class NATIVE-REPLAY, the two runs and their md5s, executed-and-asserted vs not-asserted bullets |
| E5 §16 FULL SUBSYSTEM | `cannot be claimed while §13 is empty` | cannot be claimed while §13 holds no live observation |

I did not touch the rest of the S-39 repairs the sample lists, because they are outside this route:
- declaring `02EBA3F8` (OPUS, type store);
- §14.2's second reader `001E2AF0` of `+0x29`;
- the `+0x2A` / `+0x08` type rows;
- the runtime-cell narrowing (SWE2-DATA).

§10.6's grow-path sentence and §16's "never reaches it" clause predate the 10-02 I-3 correction. I noticed that and
did not draft it, since it is not this defect.

**Dry run** (`apply_dryrun.out`, run WITHOUT `--apply`). The page is clean in the shared tree, so the dry run read
the working tree:

```
page Database/FFXII TZA/17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md  source working tree (clean)  HEAD 1e18553b0  mode dry-run
line endings LF
PASS E1 section 2 return semantics: anchored once, would replace (+196 chars)
PASS E2 provenance note on section 13: anchored once, would replace (+203 chars)
PASS E3 section 10.1 null entry: anchored once, would replace (+1143 chars)
PASS E4 section 13 body: anchored once, would replace (+2408 chars)
PASS E5 section 16 FULL SUBSYSTEM: anchored once, would replace (+182 chars)
edits 5, to change 5
FAILS 0
```

**Idempotency.** I applied the five edits once to an in-memory copy, then counted each full replacement: every one
occurs exactly once (1, 1, 1, 1, 1). A second run would therefore SKIP all five.

**Owed before publish.**
- The new interior citations sit in functions the contract already cites, so no new function is cited:
  - `0018C97A` and `0018C680` are inside `0018C8F0` / `0018C610`;
  - `001E05AE` is inside `001E0590`.
- An xlayer edge pre-check on the staged page was **not run** here.
- The contract is OPUS's, so the publisher needs OPUS's agreement or an OPUS-run apply.

## The check (FABLE)

`check_s39.py` (with `rawidx.py`, the raw reference index, and rvlib from
`../fable-review-astra-ov42-caller-quotient-bound-1002/`) prints 12 PASS/FAIL lines and `FAILS N`:

- **S1–S6, static:** the getter hand-off, the enqueue's null path, the teardown call, the untested load and
  dereference, the only branch into it, and the two destroy loops that do test.
- **R1–R2:** the raw reference index for `0018C8F0` and `0018C610`.
- **U1:** the null entry faults at `0018C933`, reading `0x10`.
- **U2, harness control:** a non-null entry with `+0x10 = 1` runs to return and empties the vector, so the harness
  itself does not fault.
- **Sensitivity controls:**
  - **C1** evaluates the old reading ("the flush null-tests before its first dereference") on the shipping image.
    It must come out False.
  - **C2** patches a copy of the image at `0018C930` with `mov rdi,[rbx]; test rdi,rdi; je 0018C94C; nop`. The
    detector must then report "tested", and the null-entry run must return cleanly. If the check could not see the
    defect, C2 would fail. If the shipping image were null-tested as §10.1 implies, S4, U1 and C1 would fail.

Result: `check_s39.out`, 12 PASS, **FAILS 0** (md5 `5071770bf89a3e288f1129c39fbaa41f`).

## Consumer check (FABLE)

affected: Database/FFXII TZA/17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md

- consumer: 17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md §2 "return semantics" ("Failure is silent everywhere"): revised-here
- consumer: 17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md provenance note and §16 FULL SUBSYSTEM ("§13 is empty"): revised-here
- consumer: 17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md §12 `flushOwner` pseudo-code (no null test in loop 1): agrees
- consumer: 17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md (L1919 cites `0018C933` in the flush; states no null absorption): agrees
- consumer: _index/L2-VERDICTS.md S-39 runtime cell ("I-1..I-10 all stub-free … every named runtime invariant covered"): routed-to-SWE2-DATA (narrowing already filed by SWE2-AUDIT-SPEC: I-10 premise static, `r9b` order unasserted, no null-owner case)
- consumer: _index/candidates/opus-runtime-closers-index.md S-39 rows (lists `G_handshake_I10` under I-10): routed-to-OPUS (I-10's shape only, not its premise)
- consumer: _index/candidates/s39-opus-replay-command-lists/README.md ("a failed `malloc` appends a null to both lists"; no null-owner flush case): agrees
- consumer: _index/candidates/auditspec-l2-sample-1003/README.md S-39 point 3 and SF-4a: agrees

run: check_s39.py at 1e18553b0 (re-run; first run at 4207b4a16) (FAILS 0, 12 PASS; unicorn 2.1.4 under C:\Python314; exe sha256 73461d08… asserted by rvlib)
