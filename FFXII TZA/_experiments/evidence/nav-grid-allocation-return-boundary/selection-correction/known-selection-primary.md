The allocation wrappers never take an arena argument. **`0036A100` passes `[022D89BC]` to the arena allocator
`0036BC60`** (`0036A113`); its retry at `0036A12E` passes the same global to the second allocator `0036BFE0` (`0036A149`).
`0036A1A0` does the same. A caller that wants its block from a
particular arena therefore **pushes a selection, allocates, and pops** — and that pattern is one of the most
used in the engine: **109 functions push through `0036C1D0` (135 call sites) and every one of them also pops
through `0036C140`** (111 functions, 153 sites, 19 of them tail jumps), from the resource loaders, effects,
text and actor code alike.

| operation | body | effect |
|---|---|---|
| push `0036C1D0(arena, category)` | `lea r9,[rsp]` / `mov r9,[r9+4]` / `sub r9,5`, then tail-jump to `0036C1F0` with stack index 0 (`0036C1D0`–`0036C1DF`). The return address is at `[rsp]`, so the qword at `[rsp+4]` **straddles** two slots: its low dword is the return address's high dword, and its high dword is residue from the caller's frame. ~~the caller's call-site address~~ The stored value, minus 5, identifies no call site. | a saved "tag" with no meaning and no consumer (below) |
| `0036C1F0(arena, category, stack, tag)` | depth `[022D89C0 + stack×4]`; **depth ≥ 31 spins forever** (`0036C20B`–`0036C211`). Saves the current state as a 16-byte record at `022D89D0 + (stack×32 + depth)×16`: `+0` u16 the active arena `022D89BC`, `+2` u8 the category `022D8E18`, `+3` u8 `022D8E28`, `+8` the tag `022D8E20` (`0036C213`–`0036C252`). Depth + 1. Then installs the new category (`0036C265`), the tag (`0036C26B`) and **the active arena through the map `022D89A8[arena]`**. The id is sign-extended (`0036C262`) and indexes the 15-byte map with **no bounds check** (`0036C272`–`0036C27F`). | ~~the requested id is not the arena index; the map translates it~~ **In the retail image the map translates nothing.** Its only writers are two identity fills, `00369DA0` in the initializer and `0036A290` in `0036A280`, so `map[id] == id` for ids 0–14. An id of 15 or more reads past the map into `022D89B7` and beyond. |
| pop `0036C140()` | depth of stack 0 − 1, **spinning forever if it was not positive** (`0036C146`–`0036C150`); restores all four fields from the record (`0036C167`–`0036C18D`) | the previous selection is back |
| byte push `0036C1A0(value)` / pop `0036C110()` | A second, 32-deep stack of the byte `022D8E1C` at `022D8DD0`, depth `022D89C8` (`0036C1A7`–`0036C1C9`, `0036C116`–`0036C12F`). ~~the pop simply returns when the depth is already negative~~ **The failure behaviour differs from the main stack.** A push at depth ≥ 31 returns without saving or installing anything (`0036C1AB`): the new byte is silently dropped. A pop returns unchanged only when the depth is negative (`0036C118`). At depth 0 it decrements to −1 and installs `022D8DD0[−1]` = `022D8DCF`, the last byte of the unused stack-1 records (`0036C11A`–`0036C12F`). | 18 functions, each using both |

**What the saved fields do.** The active arena is the wrappers' first argument. **The category byte is stamped into
the header of the blocks the two wrappers and `0036B160` return.** Each copies `022D8E18` to `block − 0x3E`:
`0036A15F` in `0036A100`, `0036A206` in `0036A1A0`, `0036B1CA` in `0036B160`. So such a block records which scope
allocated it. ~~every block's header~~ The other direct callers of `0036BC60` stamp nothing at that offset:
`0036A2A0`, `0036CB00`, and the retry allocator `0036BFE0`, whose result the wrappers stamp themselves. Whether
`0036A2A0` and `0036CB00` produce blocks that carry this header is not traced.

`022D8E1C` is the arena allocator's fallback where a free-list record supplies no byte `+0x16` (`0036BD19`, `0036BD21`,
`0036BD44`, `0036BD4F`). `022D8E28` is compared in `0036A490` (`0036A4F6`). **The tag `022D8E20` is saved and restored
and read by nothing.** The first scan here covered rip-relative operands only. SWE2-AUDIT-SEM's census then covered
rip-relative, image-base-indexed, immediate-built-pointer and data-qword forms and found no consumer of `022D8E20`
(`REVIEW-arena-selection-stack.md` in the auditor's work directory).

**The initializer `00369D30(arena, …)`.** It returns at once for an arena above 14 (`00369D47`). **Only when no arena has
been initialized yet** (the init mask `022D89B8` is zero, `00369D6E`), it:
- sets the active arena `022D89BC` to its argument;
- identity-fills the map;
- zeroes `022D8E28`, both stack depths (a qword store at `022D89C0`), the byte-stack depth (a qword store at `022D89C8`),
  `022D8E1C`, the tag `022D8E20` and `022D8E10`;
- sets the category `022D8E18` to `0xFF` (`00369D73`–`00369DC5`; `r8d` is cleared at `00369D57` before the stores).

~~sets the category to `0xFF`, the tag, `022D8E1C` and `022D8E28` to its argument~~ Every call then ORs `1 << arena`
into the mask (`00369DCC`–`00369DE7`), so a later arena's initialization leaves the stack state alone.

**Only stack 0 is used.** `0036C1F0` is general over a stack index, but its only caller is `0036C1D0`, which passes 0,
and the pop hard-codes stack 0. The depth array has two dwords (`022D89C0`, `022D89C4`), and the record array
`022D89D0` up to `022D8DD0` (exclusive) is `0x400` bytes: **exactly two stacks** of 32 × 16. The game drives one.

**The allocator will not run unselected.** `0036BC60` spins forever when its third argument `r8` is zero **and** the
stack-0 depth is zero (`0036BC79`–`0036BC87`). `r8` is zero at five of its six direct call sites: both wrappers
(`0036A11C`, `0036A1C6`), `0036B160` (`0036B17E`), `0036CB00` (`0036CF04`) and `0036BFE0` (`0036C0A4`). `0036A2A0`
passes `rbx` (`0036A3B5`) and passes the gate whenever that is non-zero. So an allocation through the wrappers requires at
least one pushed selection. **The push / allocate / pop discipline is enforced by a hang**, not only by convention.

**Scope discipline, and its exception.** Push and pop are always paired inside one function except in **two effect
constructors reached through the jump table at `0043EBF0`**, `0052A130` and `0052ADF0`, which pop **only on their
allocation-failure branch** (`0052A302` after a failed `0036A190` at `0052A2F1`; `0052AFE4` after `0052AFD3`). The
matching push lies upstream of the dispatcher and is not traced here; on success the selection stays pushed past
their return. **Both overflow and underflow of the main stack hang the thread** rather than fail, so a mismatched pop is
