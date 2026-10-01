# UC-5a: the 7 `call`-predecessor blocks, and the continuation tails (OPUS, 2026-09-26)

**Evidence class: STATIC. `live_game: false`.**

UC-5 left two things open:
- the 7 unlisted blocks whose predecessor ends in a `call` (548 bytes). They are ambiguous until each callee is checked
  for `noreturn`;
- whether any continuation tail hides a real entry that the four-form reference union (rel32 / RIP-lea / DIR64 /
  `.pdata`) cannot see.

**5 / 5 pass. `run_output.txt` and `result.json` are byte-identical over two runs (md5 `4b2c537949d3efa82af3cdefbc4a1357`).**

| case | observed |
|---|---|
| `U1` | The admissions table's `call`-predecessor rows are 7 blocks and 548 bytes: 4 classed `table`, 3 `ambiguous`. |
| `U2` | **The 4 table blocks are switch data from end to end, not code.** Every part is named by an image-base-relative operand in the predecessor, and every index byte is below its table's entry count. `0020FAD4` is a 21-entry DWORD table, an 80-byte index table and a second 7-entry DWORD table. `0081C290` is 7 DWORDs plus a 79-byte index. `0082CE48` is 9 DWORDs plus a 167-byte index. `007E3CC5` is a 3-byte alignment `nop` plus a 7-entry DWORD table. |
| `U3` | **`00829E85` and `0082A657` are dead.** Each is a single dangling `mov rdi,[rsp+0x40]` followed by `int3` padding, and nothing branches to either. The call before each, to `00824330` in the Lua 5.2 error path, never returns: `00824330` calls `00823860` and then `int3`; `00823860` calls `0081E2C0` and then `int3`; and `0081E2C0` ends either in the `longjmp` import thunk plus `int3`, or in the panic call, the imported `abort` and `int3`. |
| `U4` | **`0082E041` is part of `0082DCE0`**, a cold error path reached by that function's own `ja` at `0082DE8B`. It is `call 00823710` (which runs `0081D3A0` and then `int3`), then `int3`. |
| `U5` | **No route outside the union names a tail.** Every DWORD position in the mapped image, at any alignment, is compared against each of the 162 continuation tails' RVAs. The only aligned hit outside `.text` is `0036F22E`'s `.pdata` entry: the route pass 6 bans, which the page already discounted. The 7 hits in `.text` are bytes of other functions' instructions (immediates and rel32 fields), each decoded in `result.json`. The 2 hits in `.rdata` are unaligned. Control: the same scan finds the switch-table RVA stored at `0020FAD4`. |

**Answer.** None of the 7 blocks is a separate function:
- 4 are switch tables;
- 1 is a reachable cold path of its predecessor;
- 2 are unreachable remnants after a call that never returns.

The tails hide no entry that any static route in the image names. Only an address built by arithmetic could still reach
one, and no static scan can exclude that.

**Why U5 is informative here** when FABLE's image-relative scan of the head blocks was not. That scan tested address
*ranges* against 73,248 runs of `.text`-range dwords, and any range collects hits. This one tests 162 exact start
addresses, and the aligned hits come to one, a known `.pdata` entry.

**Run:** `python check.py` (about a minute). It needs `Tools/work/exe/FFXII_TZA.exe`, `Tools/work/graph/functions.tsv` and
the page's `unlisted-body-admissions.tsv`.
