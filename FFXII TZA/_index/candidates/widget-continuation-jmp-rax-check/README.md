# The widget release's `+0x08` continuation: skipped when null, entered by `jmp rax` (OPUS, 2026-09-26)

**Evidence class: STATIC** (the shipping image, every instruction decoded at its address), `live_game: false`.

A rejecting regression for the restatement of
[`CONTRACT-widget-object.md`](../../../16-UI/Widget-Object-Model/CONTRACT-widget-object.md) §16 (the teardown's step 9
and the `+0x08` ABI), requested by FABLE (`FABLE-REQ-OPUS-WIDGET-S16-CONTINUATION-JMP-RAX`). §16 said the continuation
is *"entered by `jmp rbx` after `add rsp,0x20` / `pop rbx`"*. The image jumps through `rax`, and a null `+0x08` is
skipped. The section's conclusions are unchanged: a tail continuation on the caller's frame, no defined arguments, and
it runs after the free or pool return.

**3 / 3 pass; `result.json` is byte-identical over two runs (md5 `0b637b75e9c383ccfe1953239e4f14bb`).**

| case | what the image shows |
|---|---|
| `J1` | `002483CA mov rbx, [rdi+8]` reads the continuation before `002483CE mov [rdi], 0` nulls the handler |
| `J2` | `002483F8 test rbx, rbx` / `je 00248408`; `00248408`–`0024840D` is `add rsp,0x20` / `pop rbx` / `ret` |
| `J3` | `002483FD`–`00248405` is `mov rax, rbx` / `add rsp, 0x20` / `pop rbx` / `jmp rax` |

**Consumers.**

| consumer | state |
|---|---|
| §16 step 9 | revised-here (struck; restated) |
| §16 "The `+0x08` ABI", the entry bullet | revised-here (struck; `jmp rax`, and a new bullet on the null skip) |
| the state diagram, "saved +0x08, if non-null ──▶ `jmp` continuation" | agrees |
| §16's conclusions (caller's frame, no arguments, after free/pool) and the later batch-callback cross-reference | agrees |

Run: `python check.py` (needs `pefile` and `capstone`, and the shipping EXE at the path in the script).
