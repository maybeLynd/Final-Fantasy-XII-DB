> Drafted by a Claude Opus 5.5 subagent pass under FABLE, 2026-09-27. The follower it used is `ga1_row_follower.py`, published here and run by the control `ga1_open_bytes.py`. FABLE re-ran the control and re-read the `+0x0A` reader (`0031E288`) and the nine `battle_pack.bin` copies.

# GA-1: status_data.bin row bytes +0x11 to +0x1D, readers and values

Date: 2026-09-27 (machine date). Executable: `Tools/work/exe/FFXII_TZA.exe`, image base 0x120000.
This is static work: capstone decode of the executable, plus the shipped bytes.

**Open set.** GA-1's latest status (2026-09-26) still lists `+0x11`-`+0x1D` as open. `+0x13` was
answered that day (an order key, read at `0031E241`), so this report treats it as a known positive,
not an open byte. The open set is `+0x11`, `+0x12`, and `+0x14` to `+0x1D`: twelve columns.

## Result in one paragraph

**No instruction reads any of `+0x11`, `+0x12`, or `+0x14` to `+0x1D` from a status row pointer.** The routes
searched are listed below. No wider access covers them either. The only status-row reads that span
more than one byte are:
- dword `+0x0C` (`0030E68A`), covering `+0x0C`-`+0x0F`
- dword `+0x20` (`00387E5D`, `0038FE0D`, `003909DC`), covering `+0x20`-`+0x23`
- word `+0x00`, `+0x06` and `+0x0A`

No qword or xmmword load of a status row exists. The bytes nearest the open range are read one byte
at a time: `+0x10` at `0031E22C` and `+0x13` at `0031E241`. No row pointer reaches a memcpy or any
other callee.

No code decides a meaning for these twelve columns. The only reading available is from the data
(see the end of this report), and its confidence is low.

## How the table is reached (provenance)

- `00236C30` loads the battle-pack header pointer `[0208E680]` and reads the section offset
  `mov ecx, dword ptr [rax + 0x40]` at `00236D91`. It then calls `003847B0`, which does
  `movsxd rdx, ecx`, `lea rcx, <02EBF118>` and `jmp 0x3845f0`. `003845F0` stores the header into the
  slot (`mov qword ptr [rcx], rdx` at `003845F4`) and rebases the header's `+0x0C`.
- A row pointer is `ImageAddress_ResolveRuntimePointer(dword [H+0xC])` (`0020E600`) plus
  `word [H+8]` (40) times the id. It is formed by a 32-bit `add` or `lea`, for example
  `0038770B imul ecx, ebx` / `0038770E add ecx, eax` in `003876D0`.
- **The runtime bytes are the shipped bytes in every language.** The file-table strings name
  `status_data.bin` only for in and ch. All nine `test_battle/*/binaryfile/battle_pack.bin` copies (ch, cn, de, es, fr,
  in, it, kr, us) carry `status_data.bin` byte-for-byte at their header `+0x40` offset. That is the
  section `00236D91` binds. The four loose copies (kr/in/cn/ch) have md5
  `99134f6bb3466528c3320e0a4371df5c` and are identical.

## Routes covered

1. **All references to the slot.** A raw sweep (`ga1_rawslot.py`) tested every byte offset of
   `.text`, the only executable section, for a rip-relative disp32 with an immediate tail of 0, 1, 2 or 4 bytes. It
   found **130 references to `02EBF118`, and all 130 decode as real instructions**, matching the 130
   in the y1p cache across the 18 listed functions. No section holds `02EBF118` as an absolute qword,
   a dword, or an RVA. The image-base-relative form (`ibrel.py 02EBF100 02EBF130`) finds 0 operands.
   No `lea` points at the start of the registry area to reach `+0x118` by offset: each slot has its
   own `lea`, and the only `lea` of `02EBF118` is the binder `003847B3`.
2. **All references to the pack header** `0208E680`: 45 rip references in the raw sweep, all real
   instructions, in `00236C30` (42), `002368D0` (2) and `00238850` (1). None are absolute or RVA
   constants, and there are 0 image-base-relative operands. The only use of section `+0x40` is `00236D91`,
   which passes it to the binder.
3. **Row-pointer follower** (`ga1_taint.py`): a may-taint forward dataflow over each function's CFG,
   joining with a union at merges.
   - Tags: the header `H`, `[H+0xC]`, the stride, and the row pointer `R(k)`, where k is the byte
     offset inside the row.
   - It follows register copies, `lea`/`add`/`sub` with immediates, `cmov`, `xchg`, push/pop, and
     stack spills and reloads. Stack slots are normalised to the function's entry frame, and a frame
     pointer formed by `lea r, [rsp+n]` is followed.
   - It follows callees that receive a tagged value in rcx/rdx/r8/r9 or in an outgoing stack slot
     (`[rsp+0x20..]` maps to the callee's entry `+0x28..`), memoised, to depth 7. Direct tail jumps
     count as callees.
   - Functions that return `R` in rax count as accessors, and their image-wide callers from the y1p
     call index are analysed too.
   - Every memory operand whose base or index carries `R(k)` is recorded with offset k+disp and its
     access width. An `R` stored to non-stack memory counts as an escape.
   - Jump tables use image-base-relative RVA tables, decoded with a bound and a byte-index table
     found by looking back across blocks. **Each of the 130 slot loads is also a CFG root**, so an
     arm reached only through a table undecodable from the entry is still analysed. The coverage
     check reports all 130 roots reached in all 18 functions.
4. **Candidate sweep.** I listed every memory operand with displacement 0x11-0x1D (any base, any
   width that overlaps the range) in the CFG-reachable code of the 18 functions, then traced each
   base by hand. The candidates are in the table below.
5. **Compiled-in copies.** I searched the whole image for each column as a 32-byte vector in id
   order, as a rank-to-status list, and as 32 dwords. Nothing was found for any open column, so
   no native table replaces them.

**Result of the follower:** it reached 13 distinct row offsets:
`+0x00 +0x02 +0x06 +0x08 +0x09 +0x0A +0x0C +0x10 +0x13 +0x20 +0x24 +0x26 +0x27`.
- **Calls receiving a status row pointer: 0.**
- **Escapes (a row pointer stored to non-stack memory): 0.**
- **Row pointers spilled to the stack: 0.**
- **Accessors whose callers read through them: 0.** `003908A0` was flagged, but only because rax
  still holds the resolved records base on its void return path after `00390932`, and it has no
  direct callers.
- Calls with a stale `H` in rdx went to `002F9860` (`0031E28C`) and to `__security_check_cookie`
  (`0038622D`). The follower analysed both and found no row access.

## Control results

**Positive controls (the task's). All three were found before any "no reader" result was accepted:**

| control | found |
|---|---|
| `+0x20` in `00387CB0` | `00387E5D mov eax, dword ptr [rcx + 0x20]` (width 4) |
| `+0x20` in `003908A0` | `003909DC mov eax, dword ptr [rdi + 0x20]` (width 4) |
| `+0x08` in `00387730` | `003877A6 cmp byte ptr [rcx + 8], 0xff`; `00387883 movzx eax, byte ptr [rsi + 8]`; `0038788D movzx eax, byte ptr [rbx + 8]`; `0038792C movzx eax, byte ptr [rbx + 8]`; `00387938 movzx eax, byte ptr [rbp + 8]` (all width 1) |

The third `+0x20` reader named in the register (`0038FCE0`) is also found:
`0038FE0D mov eax, dword ptr [rcx + 0x20]`.

**Sensitivity control (the defect that let the 2026-09-15 census miss a reader).** That census missed
the `+0x13` reader in the query filler's status arm. The arm is reached through the class jump table
`0031C612 mov ecx, dword ptr [r14 + rax*4 + 0x1fe598]` / `0031C61D jmp rcx`. The first run of this
follower missed it too: it recorded no access in `0031C5D0`. With jump-table lookback and slot-load
roots, it recovers the arm's reads:
- `0031E1D4` / `0031E20E` word `+0x00`
- `0031E248` byte `+0x02`
- `0031E295` word `+0x06`
- `0031E288` word `+0x0A`
- `0031E22C` byte `+0x10`
- **`0031E241` byte `+0x13`**
- `0031E233` byte `+0x26`
- `0031E23A` byte `+0x27`
- four byte reads of `+0x24` at `0031E2A5` / `0031E2B7` / `0031E2C6` / `0031E2D6`

These are exactly the bytes the order-key package (`ga1_status_order_keys.py`, K1) names.

**Interprocedural sensitivity.** I ran the same engine unchanged on the action table slot `02EBF138`
(129 functions). It found 316 row accesses, **39 of them inside callees that received a row pointer
as an argument**, from 111 calls that pass a row pointer. Examples:
- `0030EF83 cmp byte ptr [rdi + 0x1e], 3`, via `00304850` then `0030EF20`
- `00320DE9 movzx ecx, byte ptr [rax + rdx + 2]`, via `00304850`, `002FEB80` then `00320D70`, an
  indexed operand

So the argument-following route works, and the status table's zero is a real zero on that route.

## Candidate reads at displacements 0x11-0x1D in the 18 functions, with base provenance

None of them is a status row:

| instruction | width | base is | why |
|---|---|---|---|
| `00387D0D cmp byte ptr [rsi + 0x1b], 0x80` (in `00387CB0`) | 1 | the evaluation context (arg 3) | `00387CD1 mov rsi, r8`; the same base is tested at `00387D07 cmp word ptr [rsi], 0x59` and `00387D85 test dword ptr [rsi + 8], edi` |
| `0031C981 movzx eax, word ptr [rbp + 0x12]` (in `0031C5D0`) | 2 | an equipment row (class 6, `02EBF0F8`) | the arm resolves `02EBF0F8` at `0031C929`-`0031C956`; the same arm reads `[rbp + 0x18/0x19/0x1a]` at `0031CA6F`-`0031CAA0` |
| `0031C9DA`/`0031C9F8`/`0031CA07`/`0031CA16 movzx ecx, byte ptr [rax + 0x13/0x12/0x11/0x14]` | 1 | the row resolved from `dword [rbp + 0x28]` of that equipment row | `0031C9D2 mov ecx, dword ptr [rbp + 0x28]` / `call 0x20e600` |
| `003860DF`/`003860EF`/`003860FD movzx ..., byte ptr [rdi + 0x12]` (in `00385F60`) | 1 | a 64-byte-stride slot record | `00385FCC movzx edi, byte ptr [rax + 0xea9]` / `00385FDA shl rdi, 6` / `00385FDE add rdi, rax`, or `00385FAB`/`00385FAF` |
| `00385FF7 movzx ebp, word ptr [rdi + 0x10]` | 2 | the same slot record | as above |
| `003861FD movzx ebp, byte ptr [rcx + 0x19]` (in `00385F60`) | 1 | an action row (`02EBF138`) | the action-table resolve just above |
| `003875AE mov eax, dword ptr [rbx + 0x18]` (in `003872D0`) | 4 | an action row | `0038758C`-`003875AC`, `02EBF138` |
| `00385307`/`00385382 mov ..., dword ptr [rcx + 0x18]` (in `003851F0`) | 4 | an action row | `003852D8`-`003852FA` and `00385353`-`00385375`, `02EBF138` |
| `0038FD60 test dword ptr [rcx + 0x18], ebx` (in `0038FCE0`) | 4 | an action row | `0038FD20`-`0038FD5A`, `02EBF138` |
| `0031DA1F mov eax, dword ptr [rbp + 0x10]` | 4 | class `02EBF058` row | nearest slot load `0031D9E8` |
| `0031DBAA movzx eax, byte ptr [rbp + 0x13]` | 1 | action row | `0031DB6E`, `02EBF138` |
| `0031E019`-`0031E031`, `0031E110`-`0031E128` word `+0x10..+0x16` | 2 | License node row | `0031DF7F` / `0031E07D`, `02EBF038` |
| `0031D034`/`0031D07C word ptr [rax + 0x14]` | 2 | gambit row | `0031D016` / `0031D05E`, `02EBF0D8` |
| `002C4865`, `002C4A05`, `002C4C56`, `002C4ED5`, `002C5016`, `002C5189 mov rcx, qword ptr [rax + 0x18]` (in `002C4720`) | 8 | a UI object returned by `0035D330` | the `call 0x35d330` just before each read |
| `00536698`, `005366AC` etc. `dword ptr [rax + 0x14]`; `005368D9` / `00536942` / `0053695B` `[rbp + 0x10/0x18]` (in `00536410`) | 4 / 8 | the `02EBF018` header; a stack frame | `0053668C` loads `02EBF018`; `00536420 lea rbp, [rsp - 0x2d0]` |

Other operands in the range are stores into the unit, query or UI records (`[rsi + 0x18]`,
`[rbx + 0x10/0x18]`) or `lea` arithmetic (`002C4B10 lea r8d, [r9 + 0x1d]`,
`0046A3A4 lea edx, [r14 + 0x19]`). None is a load through a status row.

## Per-offset tables

Rows are named by the id in `+0x00`'s low byte and the register's status order (0 KO ... 31 X-Zone).
Every row not listed carries 0xFF. Each column obeys the register's law: n present values are exactly
{32-n .. 31}, each once. I re-derived the counts from the bytes.

| offset | readers (function, instruction, width) | shipped values (non-0xFF; id in brackets) | meaning | confidence |
|---|---|---|---|---|
| `+0x11` | **none found** (routes 1-5) | Regen(25)=27, Sap(10)=28, Poison(8)=29, Disease(16)=30, HP Critical(29)=31 (n=5) | not decided by code | no-reader: high |
| `+0x12` | **none found**. `0031C981` (word `+0x12`) and `003860DF` (byte `+0x12`) are not status rows (see above) | Silence(9)=31 (n=1) | not decided by code | high |
| `+0x14` | **none found** | Immobilize(14)=28, Lure(17)=29, Sap(10)=30, Float(26)=31 (n=4) | not decided by code | high |
| `+0x15` | **none found** | Berserk(27)=29, Immobilize(14)=30, Float(26)=31 (n=3) | not decided by code | high |
| `+0x16` | **none found** | Berserk(27)=28, Confuse(5)=29, Sleep(4)=30, Stop(3)=31 (n=4) | not decided by code | high |
| `+0x17` | **none found** | Shell(19)=25, Protect(18)=26, Reverse(12)=27, Oil(11)=28, Stop(3)=29, Petrify(2)=30, HP Critical(29)=31 (n=7) | not decided by code | high |
| `+0x18` | **none found** | Lure(17)=29, Poison(8)=30, HP Critical(29)=31 (n=3) | not decided by code | high |
| `+0x19` | **none found** | Blind(7)=28, Haste(20)=29, Slow(15)=30, Lure(17)=31 (n=4) | not decided by code | high |
| `+0x1A` | **none found** | Bubble(28)=27, Reflect(23)=28, Faith(22)=29, Bravery(21)=30, Float(26)=31 (n=5) | not decided by code | high |
| `+0x1B` | **none found**. `00387D0D cmp byte ptr [rsi + 0x1b], 0x80` reads the evaluation context, not a row | Invisible(24)=31 (n=1) | not decided by code | high |
| `+0x1C` | **none found** | Immobilize(14)=29, Float(26)=30, Stop(3)=31 (n=3) | not decided by code | high |
| `+0x1D` | **none found** | Haste(20)=30, Slow(15)=31 (n=2) | not decided by code | high |
| `+0x13` (known positive, already answered) | `0031E241 movzx eax, byte ptr [rbp + 0x13]` (w1), stored to query record `+0x23` at `0031E245` | 28 present, 0xFF on KO, Stone, HP Critical, X-Zone | display order key (register 2026-09-26) | high |

**Wider accesses:** none covers any open byte. Every read the follower found and its width:
- `+0x00`: w2 ×3, at `0031E1D4`, `0031E20E` and `0053662B`
- `+0x02`: w1
- `+0x06`: w2 ×21, plus w1 ×2 at `00387DC6` and `00390953`
- `+0x08`, `+0x09`: w1
- `+0x0A`: w2
- `+0x0C`: w4 (covers `+0x0C`-`+0x0F`)
- `+0x10`, `+0x13`: w1
- `+0x20`: w4 (covers `+0x20`-`+0x23`)
- `+0x24`, `+0x26`, `+0x27`: w1

The follower also listed `003854EC nop dword ptr [rax]` in `003851F0` as a `+0x00` operand. It is a
multi-byte nop and does not read memory.

**A reading from the data only (not a finding, confidence low).** The columns group statuses that
compete for one presentation or behaviour channel, and rank them 31 downward:
- `+0x1D` Haste/Slow: speed
- `+0x1C` Stop/Float/Immobilize: movement
- `+0x16` Stop/Sleep/Confuse/Berserk: action control
- `+0x11` HP Critical/Disease/Poison/Sap/Regen: HP
- `+0x1B` Invisible alone
- `+0x12` Silence alone

This looks like a per-channel priority table, most likely a PS2-era visual-effect priority that the
PC port no longer consults. No instruction in this executable supports or refutes that.

## Side findings (outside the open set)

- **`+0x0A` reader: the register's citation is wrong.** GA-1 (2026-09-18) says `+0x0A` is "read as a
  word at `0031C81A` in `0031C5D0`". That instruction, `0031C81A movzx eax, word ptr [rbp + 0xa]`,
  reads a **class-5 row (`02EBF100`)**: its arm loads `02EBF100` at `0031C723`-`0031C7E1`. The status
  row's `+0x0A` is read at **`0031E288 movzx ecx, word ptr [rsi + 0xa]`** and passed as ecx to
  `002F9860`. That function begins with a divide by 1000 (`002F9866 mov eax, 0x10624dd3` /
  `002F986D imul ecx` / `002F986F sar edx, 6`). Its result is stored to the class-26 query record
  `+0x10` at `0031E291`. So the word `0x2EE0 + id` (12000 + id) is a text id resolved by the
  id/1000 group lookup, not an unconsumed index. This contradicts the register's "not a string-pool
  key ... whose consumer is the residue". Which string it resolves to was not checked here.
- `+0x24` has four byte reads (`0031E2A5`, `0031E2B7`, `0031E2C6`, `0031E2D6`). They copy row bits 0-3
  into query record `+0x25` bits 1-4, as the register states.
