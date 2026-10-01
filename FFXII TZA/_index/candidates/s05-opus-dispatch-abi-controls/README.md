# The encoded-id query dispatch `00309EC0`: its table and its argument order, with a rejecting regression (OPUS, 2026-09-26)

This is a repair-and-prevention package. It settles two claims about one dispatch and ships the regression that rejects
both wrong readings.

| claim | status | where it came from |
|---|---|---|
| the registry base is `01EC81F0` | **REFUTED** | `69e9cad19` (ORACLE, an EXP-151 sync) changed the token in `the-encoded-id-class-registry.md`'s `00309EC0` paragraph, with no instruction evidence. `291ec5588` (a SECTION-05 overlay, snapshot-based) reverted it. `FRONTIER-REQ-OPUS-VERIFY-01EC81F0-VS-01EEBCC0-S05-MERGE` asked which is right |
| the callback is tail-called with `(0, cx)` | **CORRECTED** to `handler(id, 0)` | `CONTRACT-encoded-id-space-and-class-registry.md`'s `00309EC0` paragraph, landed by SWE2-EC7 batch-141 (`548f6a37b`). The contract owner (OPUS) corrects it; the old text stays struck |

**The authority is the image, not a newer message.** SHA-256 `73461d08…21f8`, image base `0x120000` (already included in
every address).

## A. Re-derived from the instruction bytes

```
00309EE8  410fb7c0        movzx eax, r8w
00309EEC  48c1e80c        shr   rax, 0xc              ; class nibble
00309EF0  486bd058        imul  rdx, rax, 0x58        ; 0x58-stride row
00309EF4  488d05c51dbe01  lea   rax, [rip+0x1BE1DC5]  ; next ip 00309EFB -> 01EEBCC0
00309EFF  4803d0          add   rdx, rax
00309F08  8b423c          mov   eax, [rdx+0x3c]       ; count, then dec / cmp / jg: signed index bound
00309F11  488b4250        mov   rax, [rdx+0x50]       ; the row's query handler
00309F15  4885c0 7409     test rax, rax / je -> return 0
00309F1A  33d2            xor   edx, edx              ; 2nd argument = 0
00309F1C  410fb7c8        movzx ecx, r8w              ; 1st argument = the zero-extended ENCODED ID (not the index)
00309F20  48ffe0          jmp   rax                   ; tail call: handler(id, 0)
0030944F  488d05a228be01  lea   rax, [rip+0x1BE28A2]  ; next ip 00309456 -> 01EEBCF8 = 01EEBCC0 + 0x38 (the class-id field)
```

**`01EEBCC0` is the class table.**
- Row 0 holds: offset `0x4748`, `+0x10` = 64, `+0x28` = `0x57C0`, `+0x38` = 5, `+0x3C` = 64, `+0x48` = `002FD150`,
  `+0x50` = `002FD8D0`.
- **19** rip-relative references in code reach it, including `00309EF7`.

**`01EC81F0` is not.**
- **No** instruction references it.
- Read as fifteen `0x58` rows, **every `+0x3C` count is 0**, so a dispatcher using it would reject every id.
- From `+0x2F0` the span holds an unrelated pointer table.
- It lies `0x23AD0` below the real table. **How the token was produced is not established.**

## B / C. The executed discriminator and its mutants: `check.py`

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`, no application stub.** The world is block 355's `world.py`
(the S-29 inventory world). This harness asserts the image SHA itself, and compares the whole 0x66-byte body of
`00309EC0` with the bytes above.
- The storage is bound by the shipped rebase `0030B6A0`.
- **Decoy table:** `01EC81F0` is overwritten *in emulator memory only* (its bytes are saved, and restored afterwards). The
  decoy rows get count `0xFFF` and point `+0x50` at the **other** query handler.
- **Argument capture:** at both query handlers' entries (`002FD8D0`, `002FD970`), plus a read hook on the `+0x50` fetch.
  The dispatcher is entered with a junk `RDX` (`0x5A5A`), so it must set `EDX` itself.
- **Three readings as predicates:**
  - VALID = the `+0x50` read comes from `01EEBCC0` + class·0x58, the real handler is entered, `ecx` = id, `edx` = 0;
  - WRONG_BASE = the read comes from the decoy;
  - SWAPPED = `ecx` = 0 and `edx` = id.
- **Ids:** `0005`, `1007`, `2003` (packed) and `3004`, `C001` (bitset).
- **Mutants** of the private image, each restored:
  - `M_BASE` rewrites the `lea` displacement at `00309EF7` to target `01EC81F0`;
  - `M_SWAP` rewrites `00309F1A` to `movzx edx, r8w` / `xor ecx, ecx` (the same 6 bytes).

## D. Text regression

The current consumers are checked:
- the contract;
- the class-registry page;
- the query-record page;
- the accessor-hubs page.

**Rule:** no unstruck paragraph that cites `00309EC0` / `00309F20` may give it the base `01EC81F0`, or a
`(0, cx)` / `(0, id)` order next to its tail dispatch.

**Self-tests:** the contract's verbatim pre-repair sentence must be rejected as SWAPPED, and `69e9cad19`'s token
paragraph must be rejected as WRONG_BASE.

**Before the contract fix, D failed on the contract. That was the regression working.**

## Result

**7 / 7 pass, and `result.json` is byte-identical over two runs** (md5 `4d6f2cfaa8fe3c91067a28894b844203`).

| case | observed |
|---|---|
| `A_image_identity_body_bytes_and_operands` | SHA and body are equal; `lea` → `01EEBCC0`; tail `33d2 410fb7c8 48ffe0`; `00309440` → `01EEBCF8`; every decoy-span `+0x3C` is 0 |
| `B_shipped_passes_VALID` | for all five ids: for example `0005` → read `01EEBD10` (row 0 `+0x50`), entered `002FD8D0` with `ecx=5, edx=0`; `1007` → `01EEBD68`, `ecx=1007, edx=0` |
| `B_shipped_fails_WRONG_BASE_and_SWAPPED` | neither wrong reading matches the shipped execution |
| `C_M_BASE_fails_VALID_passes_only_WRONG_BASE` | `0005` → read `01EC8240`, entered the decoy's `002FD970` |
| `C_M_SWAP_fails_VALID_passes_only_SWAPPED` | `0005` → `ecx=0, edx=5` |
| `C_image_restored_and_VALID_again` | the body bytes are back, and VALID holds again |
| `D_text_regression_selftests_and_current_consumers_clean` | both self-tests reject; all four consumers are clean after the contract fix |

**Publication state of the contract hunk: ROUTED, not yet at HEAD.**
- The contract is an overlay carrier, and `overlay-publication-plan.md` ruling 1 makes SWE2-FRONTIER its only publisher.
  `publish_paths.sh` refuses anyone else, correctly.
- The one-paragraph correction is therefore handed to FRONTIER, as `Tools/work/OPUS/s05abi_contract.patch` (sha256
  `b2d0f6c9…`, against HEAD's contract with sha256 `837130f8…`). The request is
  `OPUS-REQ-FRONTIER-APPLY-00309EC0-ABI-HUNK`.
- Part D above was run on the worktree text that carries that hunk. **Until FRONTIER publishes it, D run against HEAD
  rejects the contract**, which is its self-test on the pre-repair sentence. The finding stays open until the hunk is at
  HEAD (EVIDENCE-POLICY 4a).

**Scope.** These controls prove the **dispatch and its ABI**: which table, which row field, which registers. They do
**not** prove what any inventory callback means. That is `CONTRACT-inventory-class-storage` and its own evidence.

**How it is attached.** The contract's `00309EC0` paragraph cites this directory as its regression. Re-run it after any
edit to that paragraph or its consumers: `python check.py`. It exits 0 only when all seven cases pass (1 otherwise), and `result.json`
records `ok`.
