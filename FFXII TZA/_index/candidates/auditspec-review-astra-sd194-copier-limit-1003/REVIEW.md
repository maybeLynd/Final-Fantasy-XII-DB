# SWE2-AUDIT-SPEC review: ASTRA SD-194 namespace copier limit and NULL exception

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-SD194-COPIER-LIMIT-1003` (reviews `ASTRA-PUBLISH-SD194-COPIER-AND-QUEUE78-1003`) · commit reviewed `a3d7433c2cbcfaf47ccff9ef2f35a972df17572c`, at HEAD `a19ddeadd`
Package: `_experiments/evidence/sd194-copier-limit/` (unchanged since `a3d7433c2`). Image pin `73461d08…21f8`, base `0x120000`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every local fact holds at the shipping bytes:

- the signed-32 whole-domain counter bound;
- the copy-first, NEXT-byte termination;
- `max(1,C)` copied bytes plus one NUL;
- the 260-byte requirement for limit 259;
- NULL slot → `-1` with no destination access, and the caller ignoring the return.

The package keeps two things separate, as it should: the write-count bound, which in fact survives any aliasing because the counter lives only in registers, and the first-NUL count formula, which needs a disjoint, non-interfering source.

OPEN stays OPEN:

- pointer, index and capacity validity;
- the bytes a missing name leaves in the inherited buffer;
- imported `memcpy`;
- natural reachability, request acceptance, lifetime and presentation.

This is not a whole-SD194 closure and grants no execution credit.

## SWE2-AUDIT-SPEC identity and integrity

- `manifest.json` hashes to `b918c8860b8ce742d56b7871cb08655c7ce2d49a98b9a126150d6afba320bc21`, as named. It lists 106 members, and all match size and sha256 (0 mismatches). The only unlisted file is `manifest.json` itself. Its `limits` field reads "STATIC_ONLY counter/write bound, successful lookup only; natural missing-name bytes and reachability open." Its `acceptance` field reads "independent acceptance not awarded".
- The current drivers are `prove.py` `e8265fe7…5a9c`, `control.py` `baf3ecc0…b648` and `run.py` `ead6c845…32c3`.
- `proof-03.status.json` (`4ee3e583…c610`) records `driver_sha256` `e8265fe7…5a9c`, `terminal: true`, `exit: 0` and `exception: null`. Its stdout is `{"producer_complete": true, "operation_pins": 29, "boundary_calculations": 54, "native_or_live_runs": 0}`, and stderr is empty.
- `control-02.status.json` records the driver `baf3ecc0…`, exit 0 and stdout `{"status": "THREE_ACTUAL_PREREQUISITE_REFUSALS", "native_or_live_runs": 0}`. All three `controls-02/*/receipt.json` carry the current `prove.py` hash `e8265fe7…`, exit 1, and `expected_refusal: true`.
- `controls-01/` was produced by an earlier `prove.py` (`afd6b2e2…`) and is retained history, not current-driver evidence.
- `retained/source-01.json` is `2c66378a…9fa8` and `retained/capture.py` is `005b4e66…65dc`, both equal to the `PINS`. Every file common to `retained/` and the canonical `sd194-stale-name-slice/` is byte-identical: `diff -rq` reports no "differ" line.

## SWE2-AUDIT-SPEC reproduction

Venv python 3.14.6 with capstone 5.0.7. Outputs went to absolute scratch paths, and nothing was written into the package.

- `prove.py <scratch>/result-rerun.json`: exit 0, stdout `{"producer_complete": true, "operation_pins": 29, "boundary_calculations": 54, "native_or_live_runs": 0}`. The output is **byte-identical** to `result-03.json`.
- `control.py <scratch>/controls-rerun result-03.json proof-03.status.json`: exit 0, stdout `{"status": "THREE_ACTUAL_PREREQUISITE_REFUSALS", "native_or_live_runs": 0}`.
  - The three children each exited 1, with no `result.json`. Their final stderr lines are `ValueError: upstream capture failed/incomplete`, `ValueError: retained source identity changed` and `ValueError: retained source identity changed`.
  - The stdout hashes equal `controls-02`'s. The stderr hashes differ only because tracebacks print the scratch path.
  - `positive_result_sha256` and `driver_sha256` are equal to `controls-02/result.json`.

## SWE2-AUDIT-SPEC re-derivation from the shipping image (`disr.py`; raw bytes via `disw.py`)

- **Bytes.** `d[off(0x2DF880):off(0x2DF8D9)]` is 89 B, with sha256 `f71f6f4a0633fa327a47b23f16231e23be086270b133f30357e49520d74f9800`. That equals the pinned body hash and the retained capture.
  - `prove.py` itself never opens the EXE. It binds bytes by the source-file hash, the body hash and the validator re-decode. This review's image read closes that link.
  - The 29 decoded instructions equal the `OPS` table exactly. There is no `call`. The branches are `2DF89E jne 2DF8A4`, `2DF8C7 jge 2DF8CE` and `2DF8CC jne 2DF8B3`, all internal, and there are two `ret`s (`2DF8A3`, `2DF8D8`). The CFG is closed.
- **NULL slot.**
  - `rax = [0215F000 + sx(ecx)*8]`, then `rax = [rax + sx(edx)*8]`. `0215F000` is zero-initialised `.data`.
  - `test rax,rax / jne`. The fall-through is `or eax,-1 / ret`.
  - The only memory touched is the two table loads. There is no destination (`r11` = incoming `r8`) read or write. **Holds.**
- **Non-NULL loop.** `rdx = D−S`, `r9 = sx(r9d)` (signed C), `r8 = −S`, `r10d = 0`. Each iteration does:

  `movzx ecx,[rax]` (S+i) / `inc r10d` / `mov [rdx+rax],cl` (D+i) / `rax++` / `rcx = rax−S = t` / `cmp rcx,r9; jge exit` (signed 64) / `cmp byte [rax],0` (S+t, the **next** byte) / `jne loop`.

  The exit is `mov byte [sx(r10d)+D],0` / `xor eax,eax` / `ret`.
  - The first byte is copied before any test.
  - The loop continues only while `t < C` and `S[t] != 0`. So `t ≤ max(1,C)`, and `C ≤ 1` exits after one byte.
  - `r10d = t ≤ INT_MAX` never wraps, and `movsxd` restores `t` exactly.
  - A NUL at S+0 is copied and does not stop the loop.
  - The return is 0, not the count. **Holds.**
- **Aliasing.** `t`, `C`, `S` and `D` are held only in `rax`/`rcx`/`rdx`/`r8`/`r9`/`r10`, and the table pointer is read once before the loop. A store cannot change the count bound, given valid accesses and intact code. Only the "first NUL at offset ≥ 1" formula depends on source contents, so it needs a disjoint, non-interfering source. The package's separation is correct, and its overlap statement is if anything weaker than what the bytes give.
- **Caller `00377DC0`.**
  - `377DFF lea r8,[rbp+60h]` / `377E03 mov r9d,103h` (raw `41 b9 03 01 00 00`) / `377E09 call 2DF880` (raw `e8 72 7a f6 ff`). C = 259, so successful writes go to D+0…D+259 and need 260 bytes.
  - After the call, `eax` is next touched at `377E20 movzx eax,byte [rbp+rdx+60h]`, a write. The intervening `xor r15d,r15d` / `mov edx,r15d` / two `nop` forms do not read it, so **the −1 is ignored**.
  - With `rbp = entry−0x1A8`, the destination is entry−0x148. The cookie slot is `rbp+170h` = entry−0x38, which leaves 0x110 = 272 frame bytes. That is enough for 260, as a sanity check only; it does not establish capacity in general, and the package keeps capacity as a premise.

## SWE2-AUDIT-SPEC control sensitivity

- **`upstream-failed`.** The defect is a failed capture used as input. The control sets `capture-01.status.json` `exit` to 1, and the prover refuses with `upstream capture failed/incomplete` before reading the source. **Sensitive.**
- **`incomplete-source`.** The defect is a truncated body. The control pops the last record and recomputes the body sha, and the prover refuses with `retained source identity changed`. **Sensitive, through the whole-file pin.**
- **`changed-limit-branch`.** The defect is a different limit test, `jge` changed to `jg` with coherent bytes `7f05` and a recomputed body sha. It is refused with the same message, by the same whole-file pin.
  - The control is sensitive: any edit to the source changes the value checked.
  - But it does not exercise the downstream checks it might appear to: the body end/sha pin, the `OPS` sequence, the CFG helper or the store roles. The README's sentence "reject ... coherent altered `JGE` bytes" is literally true. Readers should take it as "any altered source record is refused by the retained-source hash pin", not as a test of the semantic layer. Because that layer sits behind two hash pins, file and body, nothing can pass it unchanged, so this is not a defect.
- **The 54 boundary calculations.** These evaluate `selected_count()` against its own bounds, so they are arithmetic sanity checks, not controls on the machine code. The package says exactly that.

## SWE2-AUDIT-SPEC claims audit

- "zero/negative limit still copies one byte plus NUL", "limit is not capacity", "returns 0 not count": **hold**.
- "NULL resolved name returns −1 with no destination access; caller ignores −1; successful bound does not establish a NUL on the missing-name branch": **hold**.
- "All 29 operations pinned; no opaque calls; CFG closed": **hold**.
- The limits keep inherited missing-name bytes, field reachability, request acceptance, allocator/lifetime, imported `memcpy` and presentation OPEN, and premise valid pointers/index/capacity. This is **not overclaimed**. "This package closes a local initialization prerequisite without closing SD194's natural-state question" is the right scope.
- Queue-78 admin reconciliation carries no scientific weight here, as the request states.

## SWE2-AUDIT-SPEC notes (non-blocking)

- Have `prove.py` compare the 89-byte body (and the two caller instructions) with the pinned EXE, so the image link is checked by the producer and not only by review.
- Add one actual control that changes a semantic field while re-pinning both hashes, for example by passing a patched `PINS`. Then the `OPS`/CFG layer has its own refusal receipt.
- For consumers (DATA/OPUS), the exact clause: "For a valid non-NULL resolved name, `002DF880` copies `1..max(1,signed32(R9D))` bytes and then one NUL, and returns 0. At `00377E09` (R9D = 259) that is at most destination offsets 0..259, which needs 260 writable bytes. A NULL slot returns −1 without touching the destination, and `00377DC0` ignores the return, so no NUL or bound follows on that branch."
