## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives

**Attack.** The contract's addressed clauses were turned into checks at their instructions: RL-1's mask tests and
template, RL-3's copy length, RL-4's cleanup layout, RL-6's disposal order, RL-7's submission state, RL-8's pin pair,
and §2 / §3's disposal tail, owner records, lane copy, resets and lookup. SECTION-06/08/09/10's executions are carried,
not re-run. Script: `Tools/analysis-kit/gfz-scripts/falsify_resource_ownership.py`, output
`falsify_resource_ownership.out`, image `73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| O1 | RL-1 the parser tests mask 4 at `003EE018` / `003EE117` | **survives**. Both are `test byte [rax + 2], 4` |
| O2 | RL-1 `003B38B0` supplies a type-3 template with flags `0x0C` | **survives**. `mov byte [rsp + 0x20], 3`, `or byte [rsp + 0x22], 0xc` |
| O3 | RL-3 the copy length is truncated toward zero to a multiple of 16 | **survives**. `cdq` / `and edx, 0xf` / `add eax, edx` / `and eax, 0xfffffff0`, interleaved with argument set-up, at four sites in `003EDAD0` |
| O4 | RL-4 cleanup layout versus ownership | **survives**. In `003A9600` (the 800 runs) and `003A9950` (A00), when context+3 mask 1 is set, `+0x870` / `+0x878` is freed only when mask 4 is clear, and is always cleared. When mask 1 is clear, the 8-byte entries are walked to `0xA00` / `0x1800` (indices 1..319 / 1..767) with no mask-4 test. Both end by releasing the lookup table (`jmp 003697F0`). `0024F410` calls both |
| O5 | RL-6 the disposal order | **survives**. `00409EC0 call 003B37E0` (ticket), `00409EC8 call 00409730` (entry reset), `00409ED3 call 0051FCF0` (bank slot) |
| O6 | §2 `0041E490`'s disposal with the original representation | **survives**. It acquires (`003AB880`) and releases (`003AB940`), then `mov rcx, [rdi + 0xd90]`, `mov rdx, rbx`, `jmp 00409D60` |
| O7 | §3 the 0x1C owner records at `02B581A0` | **survives**. The lookup, arm and delete helpers all address `02B581A0` with the record stride |
| O8 | §3 `0051EEB0` copies two 16-byte lanes | **survives**. Two `movaps` loads and two stores to `[rdi]` / `[rdi + 0x10]` |
| O9 | RL-8 the pin pair | **survives**. `00409960` reaches `003AB880`, and `00409C00` reaches `003AB940` |
| O10 | §2 the resets: eighty records and one group's sixteen | **survives** |
| O11 | RL-7 submission writes state 3 regardless | **survives**. `003DDABE mov dword [rbx + 4], 3` follows the last call, with no result test between |
| O12 | §2 the lookup exposes only state 4 | **survives**. `cmp dword [rax + rcx + 4], 4` |

**Verdict.** The contract's addressed clauses hold. Tier 1 (static).
