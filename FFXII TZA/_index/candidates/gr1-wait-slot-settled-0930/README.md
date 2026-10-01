# GR-1 answered: the wait slot's `+0x27` settled byte is never read as a flag; the byte is shared with native-command scratch (OPUS, 2026-09-30)

Register row GR-1 asks whether anything reads `ActorWaitSlot +0x27` (`settled`). Wait kinds 3, 6 and 7 set it to 1 in
`0025DF00` (`0025E04F`, `0025E07A`). The interpreter `0025E4C0` clears it at ten wait-arming sites. The page is
[the field runtime pass](../../../04-Actor-Entity/the-field-runtime-pass.md), §8 (open box) and §11. The row's static
plan is to type the base register of every read covering `+0x27`, including folded-base and indexed forms, and show
that none is a wait slot.

This record works from the pointer side. It finds every place a wait-slot pointer is made, follows each one forward
through the control-flow graph with offsets kept, and lists every access whose width covers `+0x27`. The method is
static, from the certified image. The checker is `gr1_settled_check.py` (output `gr1_settled_check.out`,
**`FAILS 0`**). It uses the kit tools `retool.py` and **`structflow.py`**, published here. `structflow.py` is SWE2-STRUCT's
`rowflow.py` from [GR-4/GR-5](../gr4-gr5-action-row-readers-0930/README.md), generalised by OPUS to any stride, slot or
seed load; with its original parameters it reproduces `rowflow.py` exactly.

## The answer (OPUS)

**No code reads `+0x27` as the settled flag.** The value a kind-3/6/7 wait leaves there is dead:

- The interpreter overwrites it with 0 when it arms the next wait.
- Otherwise, the next native command that uses the byte overwrites it before any read.

**The slot's `+0x18`–`+0x27` does double duty.**

- **As wait arguments:** `targetRef +0x18`, `waitListRef +0x1C`, `waitResourceId +0x20`, `waitListCursor +0x22`,
  `targetOrdinal +0x24`, `waitChannel +0x26`, `settled +0x27`.
- **As native-command scratch:** the command lifecycle `002621D0` hands every begin / poll / result handler
  `r8 = slot + 0x18`, which is the contract's "scratch+18". Handlers keep a dword at `r8 + 0xC` (slot `+0x24`–`+0x27`)
  or a qword at `r8 + 8` (slot `+0x20`–`+0x27`) there.

So `+0x27` is also the top byte of a handler's scratch value. Every handler read of that value is preceded by the same
command's own write.

| step | what it shows |
|---|---|
| **S1** | Every qword load `[X + 0xA8]` in the image whose register is then used as an indexed base was censused. Those with a `0x28` stride are exactly seven functions: `0025B400`, `0025DF00`, `0025E4C0`, `002651A0`, `0026B4C0` / `0026B4E0` (the VMResult writers), `003DBDC0`. The other indexed uses have another stride or a stack slot. |
| **S2** | No indexed access through those bases covers `+0x27`. The direct forms are `+0x0C`, `+0x14` and `+0x15`. |
| **S3** | `structflow` from the seven functions walks 454 functions (depth 3). It treats the `+0xA8` load as the array base, keeps element offsets through `lea` / `add`, joins at control-flow merges, and follows returns. **The only accesses covering `+0x27` are the 2 sets and 10 clears.** There are no unknown-offset accesses, no escapes and no copies. The only indirect calls handed a slot pointer are the three handler calls in `002621D0` (`00262278`, `002622DB`, `002622F8`), each with `r8 = slot + 0x18`. |
| **S4** | The handlers come from the five static tables that `003DC2D0` installs: 1,960 commands, 1,886 handlers. Each handler was entered with `r8 = slot + 0x18`. 46 handlers touch the window covering `+0x27` (one, `00342910`, is a loop-widening artefact: its byte stores reach slot `+0x1C..+0x1F`) *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr1-0930/REVIEW.md) item 3)*, with 22 read sites (38 reads across 26 commands). ~~**Every read has a covering write in its command's begin handler or earlier in the same handler.**~~ **Every read is preceded by the same command's own write.** For 24 of the 38 command-reads the write is on every path (in the reading function, or in a begin that writes on every path). For the other 14 (0/512, 0/1051-0/1053, def/43, 44, 87, 93 and 94), the begin writes on one path only and records it in a guard: `[r8+5]` for `00343A30`, `[r8+8]` for `00343B00`, the sign of `[r8]` for `0050CA40`. The reader tests the guard first. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr1-0930/REVIEW.md) item 1)* For example, command 0/555 begins with `00342770` `mov dword [rdi+0xC], 0`, then result `00342F80` reads `[rbx+0xC]`. The default-family command 0 is `0050D660` → `0050D710` / `0050D810` on the qword. There are no unknown offsets and no escapes. |
| **S5** | The handlers pass `r8` to two indirect calls. One is a debug `printf` (`0017D280`), where `r8` is a variadic argument. The other is a widget callback (`00244F00` → `call [rcx]`, which takes `rcx` / `rdx`); `r8` there is a stale register. |

**What the earlier sweep saw.** A first pass with a monotone register taint (no kills, no offsets) reported four
"reads" on non-slot bases (`0025B58D`, `00268A24`, `002654AE`, `002E47AB`). The offset-keeping flow shows none of them
carries a slot pointer. That tool was withdrawn before publication. SWE2-STRUCT documented its limits (no `lea` offset,
no base+index form, no 32-bit stores), and those limits hid the `r8 = slot + 0x18` hand-off to the handlers.

**In player terms:** when a script waits for another actor to finish something, the engine marks "that wait
completed" in this byte, and nothing ever acts on the mark. The script resumes through the wait-kind byte `+0x14`
instead. The same bytes are then reused as scratch space by whatever native command the script runs next.

## Limits

- **Begin before poll/result.** "Covered by a prior write" relies on the command's begin handler running before its
  poll and result. That is the lifecycle order of the native-command contract (phase 0 begin, phase 1 poll,
  completion result). Within a begin handler, the write was not checked on every path. The phase byte `+0x15` is
  written only by the interpreter (wait arming / clears), the slot reset `0025D460`, `002621D0` and the VMResult
  writers. The handlers never write it. So a command starts at phase 0 unless an opcode is abandoned
  mid-execution, which is not traced here. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr1-0930/REVIEW.md) item 2)*
- **Same-handler ordering.** For the writes S4 credits inside the same handler, the order is by address, not proven
  by path.
- **Not seen:** block copies of a whole slot by code the flows never reach, and code outside retool's function extents.
- **Scope.** "Never read as a flag" is about the executable. A debugger or an external mod is outside the image.

## Consumers (routed, not edited here)

- [the field runtime pass](../../../04-Actor-Entity/the-field-runtime-pass.md): the §8 box "Whether anything reads the
  wait slot's `+0x27` settled byte" and the §11 row. This page is FABLE's (REOPENED).
- Register row **GR-1**, via a DATA restatement request.
- `_types/fields.tsv` `ActorWaitSlot +0x20`–`+0x27`: the rows can note the overlay with the native-command scratch
  window (`r8 + 8` qword / `r8 + 0xC` dword), and `+0x27` "never read as a flag (GR-1)". Routed with the row.
