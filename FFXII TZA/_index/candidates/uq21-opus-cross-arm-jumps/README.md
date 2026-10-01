# UQ-21: the console's cross-arm jumps are the compiler's tail merging (OPUS, 2026-09-26)

**Evidence class: STATIC. `live_game: false`.**

**The question.** 14 arms of the developer console's dispatcher (`001D1660`) end by jumping into another arm's
interior, at 21 sites. UQ-21 asked whether those are shared tails by design or an artefact of the compiler folding
identical code.

**4 / 4 pass. `run_output.txt` and `result.json` are byte-identical over two runs (md5 `388df2f6dbf8f6e6e65c67b028de2722`).**

| case | observed |
|---|---|
| `X1` | The population reproduces: **21 jumps from 14 arms** into another arm's interior. A jump to an arm's start, such as the do-nothing arm `001D4BFA`, is a normal exit and is not counted. |
| `X2` | Every target is an instruction boundary of its host arm. |
| `X3` | **Every jump lands at the maximal common suffix.** The instruction before the `jmp` always differs from the instruction before the target, so the shared code starts exactly where the two instruction streams become identical. rip-relative operands are compared by the address they resolve to. That is the placement cross-jumping produces. Control: an arm compared with itself agrees on every instruction. |
| `X4` | **8 of the 21 enter in the middle of an expression**, a place no source-level label can occupy. **6** carry a call argument across the jump: the jumping arm sets `xmm0`, or `edx` and `r8d`, and the host's next call reads it. **2**, ids 276 and 280, carry the **CPU flags**: the host's first instruction is `setne`. The other 13 enter at statement boundaries. |

**The clearest case.** Ids 276, 280 and 281 are three toggles, one per property, and each would be a single statement
in source: `obj->Set(prop, obj->field != 1)`.

```
id 276  001D4A28  mov rcx,[01F82D20] ; xor esi,esi ; cmp dword [rcx+0x3C],1 ; lea edx,[rsi+0xF] ; jmp 001D4B59
id 280  001D4B37  mov rcx,[01F82D20] ; xor esi,esi ; cmp dword [rcx+0x30],1 ; lea edx,[rsi+0xC] ; jmp 001D4B59
id 281  001D4B49  mov rcx,[01F82D20] ; xor esi,esi ; cmp dword [rcx+0x34],1 ; lea edx,[rsi+0xD]
        001D4B59  setne sil ; mov r8d,esi ; call 001DF340 ; ...
```

The three arms become identical at `setne`. The jump lands there, carrying `rcx`, `edx` and the flags of the arm's own
`cmp`. No source construct places a label between a comparison and the `setne` that consumes it. The compiler merged
the common suffix of three separate statements.

**Answer.** An artefact of the compiler, not a shared tail by design.
- All 21 jumps sit at the maximal common suffix.
- 8 of them sit where only the compiler can put a join.

The practical consequence is the one the slice already drew: an arm's behaviour is its extent plus the host suffix it
jumps into. A reimplementation should write each arm as its own full statement.

**Run:** `python check.py` (seconds). It needs `Tools/work/exe/FFXII_TZA.exe`.
