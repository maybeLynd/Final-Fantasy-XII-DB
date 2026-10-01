# PCD-4: who writes the `+0x100` / `+0x102` guard words (OPUS, 2026-09-26)

**Evidence class: NATIVE/STATIC.** A linear disassembly of every executable section of the authority image
(SHA `73461d08…`, asserted by both scripts). No execution.

- **`sweep.py`** finds every `mov/add/sub/inc/dec/and/or/xor` whose memory destination is `[reg + 0x100]` or
  `[reg + 0x102]`, at word, dword or qword width. It groups them by containing function, using
  `Tools/work/graph/functions.tsv`.
- **`receivers.py`** finds, for one write per outside function, the last instruction that set the base register.

## Result (`sweep_output.txt`, `receivers_output.txt`)

**Eight functions** write both words at word width.

**The class's own three** change both identically:

| function | sites |
|---|---|
| `00639290` | `inc` at `006392F0` / `006392FA` |
| `0063D410` | `inc` at `0063D4C5` / `0063D4CF` |
| `0063D790` | `add 0xFFFF` at `0063D7C2` / `0063D7C9` |

Their constructor `00632E80` and the reset clear both words with one dword store of zero:
- `00632ED1 xor ecx, ecx` / `00632ED3 mov dword [rsi + 0x100], ecx`;
- `0063D5DE xor eax, eax` / `0063D5E0 mov dword [rcx + 0x100], eax`.

**Five outside functions** write the two words with independent values:

| function | writes | receiver |
|---|---|---|
| `00266530` | `+0x102` ← `cx`, `+0x100` ← `r13w` | a pointer taken from an array at `[rdx + r10·8 + 8]` |
| `003AAA50` | `+0x100` ← `0x502`, `+0x102` ← `5` | **a stack local** (`lea rbp, [rsp − 0x198]`): not a descriptor |
| `0041B550` | word writes to both, including an `or` | `this` in `rcx` |
| `00552250` | `add` and `mov` to both, separately | `[rbx + 0x160]` |
| `005528C0` | `mov` and `sub` to both, separately | `this` in `rcx` (it is called from `00552250`) |

`00269F40` writes `+0x102` alone (`this` in `rcx`).

**Reading.** For a `PClassDescriptorDynamic` written only by its class's code, the two words are one member count,
and the guard is "member count non-zero". That the four outside receivers are other types is **not shown**. So
"always equal for every object" is conditioned on it, not proven. Used by `CONTRACT-phyre-class-descriptor.md` §14
(`PCD-4`).
