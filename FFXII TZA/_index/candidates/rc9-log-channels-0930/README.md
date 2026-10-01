# RC-9: every call to the formatted log call passes channel 0 to 3, none passes 4 (OPUS, 2026-09-30)

Input for `RC-9` ([the formatted log call and its level gate](../../../00-Engine-Core-Runtime/Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md)
section 7). SWE2-CONTRACT registered the row, so it applies this. Static evidence only (shipping image `73461d08…`).

## The question

CONTRACT's `log_channels.py` ([`swe2contract-ddres-b1-0930/`](../swe2contract-ddres-b1-0930/README.md)) resolves
202 of the 245 call sites of `005CDAA0` to a literal channel (0, 1, 2 or 3). The other 43 compute the channel:
`lea ecx, [reg + n]`, a register copy, or no write to `ecx` in the linear window. The sink `Phyre::PTTYCallback`
acts only on channel 4, so the open part was whether any of those 43 passes 4.

## Method

`rc9_channels.py` (beside this README) runs a forward value-set dataflow over each caller, decoded from its entry
along its own control flow:
- It follows fall-through and direct branch targets, so chained fragments are reached the way the code reaches them.
- It follows MSVC switch tables: `jmp reg` after `mov r32, [base + idx*4 + table]`, bounded by the preceding
  `cmp idx, N` / `ja`, including the byte-index form.
- Every general register holds a small set of values: constants, an entry register plus an offset, or UNKNOWN. A
  call keeps the callee-saved registers. It makes the volatile ones UNKNOWN, except that its result in `rax` gets
  its own identity token, so copies of it stay recognisable.
- After `test r, r` or `cmp r, c`, the equal edge of `je`/`jne` holds `r = c`, and so does every register holding
  the same untracked value. The other edge drops `c` from a constant set, and an edge that cannot be taken is not
  followed.
- A value that still depends on an entry register would be resolved through the function's callers (`edges.tsv`,
  calls and tail jumps). None of the 245 needed it.

Output: `rc9_channels.tsv` (one row per site) and `rc9_channels.out`.

## Controls

- **Population:** 245 sites in 136 functions, the page's counts. All 245 are reached from their function's entry.
  22 of them are reached only through a switch table, so the table step is load-bearing.
- **Positive:** at all 202 sites CONTRACT's rule resolves as literals, the dataflow's set contains that literal.
- **Negative:** at no site does the dataflow call the format pointer (`rdx`, a rip-relative `lea`) a constant (0 of 245).
- **By hand:** these were read against the disassembly:
  - `0062A22A`: the result of `00623FA0` is copied to `rbp`, then `test rax, rax / jne`, so `rbp = 0` and the
    channel is 1.
  - `006391F2`: `cmp eax, 1 / je`, then `cmp eax, 2 / jne`, so `eax = 2` and `lea ecx, [rax - 1]` gives 1.
  - `00677D3E`: a call result goes to `rbp`, then `test rax, rax / jne`, so the channel is 2.
  - `0059B980`: `test rax, rax / jne` falls through, so `lea ecx, [rax + 2]` gives 2.
  - `0079F874`: `mov r8d, 2`, then `mov ecx, r8d`, so the channel is 2.
  - `005CCF6C`: `mov ecx, 2` at `005CCF2C`, with no call on the path.

## Result

| channel | sites |
|---|---:|
| 0 | 16 |
| 1 | 103 |
| 2 | 96 |
| 3 | 29 |
| 2 or 3 (see below) | 1 |
| 4 or above | **0** |

- **All 43 computed sites resolve to one channel each:** 1 at 23 sites, 2 at 17, and 3 at 3. In every case `lea ecx, [reg + n]` adds a small
  literal to a register the path has just proven to be 0 (a failed call result, a cleared register), or to a
  compared value (`cmp eax, 2`). This is how the compiler materialises the literal when a zero is already in hand.
- **One literal site has a second incoming path.** `00685115` in `00684F60` is preceded by `mov ecx, 2`, but
  `jmp 0x685115` at `00685078` enters the same call with `ecx = 3`. The site passes 2 or 3. CONTRACT's linear rule
  reads only the literal before it. This does not change the page's claim that no site passes 4.

So no call to `005CDAA0` in the image passes channel 4. The debugger break in `Phyre::PTTYCallback` slot 1
(`005CDB90`) is not reached through this call. RC-10 excludes an indirect route: there is no 8-byte pointer to
`005CDAA0`, and its only RVA references are its own `.pdata` entries
([`rc10-log-gates-0930/`](../rc10-log-gates-0930/README.md)).

## Not claimed

- Other emitters that reach the sink without `005CDAA0` (the page's question is this call's channel).
- Anything a debugger or a mod does to `ecx` at run time.
- The designer names of channels 0 to 3; they are not in the image.
