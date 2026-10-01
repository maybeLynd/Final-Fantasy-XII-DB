# Static answers for SWE2-CONTRACT's RC-12, RC-13 and RC-14 (FABLE, Claude Opus 5.5, 2026-09-30)

SWE2-CONTRACT registered these rows on 2026-09-30. It holds the pages (the scheduling page,
`01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md`) and the
RC register section. FABLE did the research (`FABLE-RC-12-13-14-STATIC-0930`, target keys only) and routes the answers
for incorporation. Scripts run from this folder; they use FABLE's disassembly helper
(`Database/Tools/work/FABLE/pub140-scratch/disr.py`) and the decompiled shipped corpus (`.../pub140-scratch/corpus/us`,
1,114 scripts).

## RC-12: which special-function slot each footer reader asks for — answered

~~**The footer is 1-based.** `special[t]` sits at `+2*t` of the resolved `+0x18` block, and word `+0` is the count. Each
reader bounds its slot with `cmp c, word [base]; jge` and reads `word [base + 2*(c+1)]`, so `t = c + 1`.~~
*(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc12-footer-channels-runstate-0930](../rc12-footer-channels-runstate-0930/README.md):)* **The footer is 0-based.** Word `+0` is the count and `special[k]` sits at `+2 + 2k`. Each reader bounds its slot with `cmp c, word [base]; jge` and reads `word [base + 2 + 2c]`, so `k = c`. The record override word a reader checks first is `+0xC8 + 2k`, the same `k`: `0025DF00` reads `+0xDE` (`0025E159`), and `sysReqchg`'s writer `0025AF60` stores `[rax + rbx*2 + 0xC8]` (`0025AFA1`). The numbers in the declaration table below are this raw index `k`: the decompiler's printed `function NAME(n)` equals it (ORACLE's control B, 14,081 declarations).

~~The control is the wait resolver: `0025DF00` compares with 11 and reads `+0x18` (`0025E186`), which is `special[12]`,
the `mapjump` slot the page names.~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930:)* The wait resolver `0025DF00` compares with 11 and reads `+0x18` (`0025E186`), which is `special[11]`, the `parameter` slot, not the `mapjump` slot the page names.

The slot names are the special types the shipped scripts declare (`function NAME(t)`):

| t | declared as (count) |
|---|---|
| 1 main (5,231) | 2 talk (4,771) |
| 3 touch (405) | 4 touchon (260) |
| 5 touchoff (230) | 6 across (18) |
| 7 spawn (6) | 8 fieldsign1 (71) |
| 9 initevent (90) | 11 parameter (21) |
| 12 mapjump (1,525) | 13 fieldsign2 (101) / touch2 (8) |
| 14 respawn (6) | 16 talkhold (669) |
| 17 talkterm (669) | 10, 15, 18: no shipped declaration |

[`rc12_special_slots.py`](rc12_special_slots.py), [output](rc12_special_slots.out), control PASS:

| reader | site(s) | slot(s) |
|---|---|---|
| `0025AE00` | `0025AEF9` | ~~11 `parameter`~~ 10: the spawn table's `talk` override slot (see `00263D40`) |
| `0025B820` | `0025B977`; `0025B9C6`, `0025BA62` | ~~11 `parameter`; 3 `touch` (twice)~~ 10; 2 `talk` (twice) |
| `0025BAD0` | `0025BD19` | ~~17 `talkterm`~~ 16 `talkhold` |
| `0025C230` | `0025C4BE`, `0025C58B`, `0025C63B`, `0025C755`, `0025C7BC` | ~~4 `touchon`, 14 `respawn`, 9 `initevent`, 6 `across`, 5 `touchoff`~~ 3 `touch`, 13 `fieldsign2`, 8 `fieldsign1`, 5 `touchoff`, 4 `touchon` |
| `0025C830` | `0025CFD7`, `0025D087`, `0025D154`, `0025D2A7`, `0025D356` | ~~the same five: 4, 14, 9, 6, 5~~ the same five: 3, 13, 8, 5, 4 |
| `00263050` | `002631E8` | ~~18: a slot no shipped script declares~~ 17 `talkterm` |
| `00263D40` | `00263D72` | **no fixed slot**: ~~a generic accessor~~ the spawn-table accessor (see below) |

**`00263D40` shows the `+0x18` block holds more than the footer.** ~~It walks `esi + 1` count-prefixed lists
`{u16 n; u16 items[n]}` from the footer (`00263D90`-`00263D9F`), then returns item `rdi` of the last (`00263DA8`).~~
*(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930:)* It skips `esi + 1` count-prefixed lists `{u16 n; u16 items[n]}`, the footer and `esi` more (`00263D90`-`00263D9F`), then returns item `rdi` of the next list (`00263DA8`); selector 0 is the first list after the footer.
`0025AE00` passes list index `ebp`, checked to be at most 4 (`0025AE4E`), and item `r12` (`0025AE57`-`0025AE62`), both
from its own arguments: `ebp` = its second argument (`mov ebp, edx`, `0025AE11`) and `r12d` = its third
(`mov r12d, r8d`, `0025AE0E`). ~~So the block is the special footer (list 0) followed by up to four more lists, and this reader
asks for whatever its caller names.~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc12-footer-channels-runstate-0930](../rc12-footer-channels-runstate-0930/README.md):)* So the block is the special footer followed by the spawn-table lists that ORACLE's record names (`entry`, `spawn`, `talk`, `touch`, `respawn`, selectors 0 to 4). Their contents are ORACLE's reading and are not re-derived here.

Limits:
- ~~`00263050`'s slot 18 is read from the image, but no shipped script declares type 18. It always gets the "none" answer
  on shipped data, unless a declaration form the decompiler does not print exists.~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930:)* `00263050` reads slot 17, `talkterm` (`+0x24`, `002631E8`).
- ~~Lists 1 to 4 of the block are not decoded here.~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930:)* The lists after the footer are the spawn table (ORACLE's record); they are not decoded here.

## RC-13: what a request channel means to a script author — answered from the shipped scripts

~~The engine gives a channel no meaning beyond its scheduling priority: the highest channel runs first, as the page
states.~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc12-footer-channels-runstate-0930](../rc12-footer-channels-runstate-0930/README.md):)* The highest channel runs first, as the page states, but the engine also files each special function it triggers on a fixed channel (for example `touch` on channel 3 at `0025C4F4` and `main` on channel 0 at `002669F5`; ORACLE's record lists the rest), and a `REQ` onto a channel whose occupancy bit in record word `+6` is set is refused (`003DB888`-`003DB890`). The shipped scripts still use channels by a clear convention.

[`rc13_channels.py`](rc13_channels.py) ([output](rc13_channels.out)) tallies every `REQ`-family call written as
`sysReq*(channel, Target::function)`, which is 88% of the literal-channel calls. The rest pass `reqArr` arrays or
computed targets. The census groups calls by channel and by the function requested:

| channel | calls (scripts) | what is requested there |
|---|---|---|
| 0 | 2 (2) | essentially unused |
| 1 | 26,879 (841) | ~~**the default: the actor's own behaviour**~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-rc121314-0930 §5 N1:)* **the default and largest channel: the actor's own behaviour (movement, turns, doors, event lights; no single function above 8% of its calls)** - movement (`移動`), turns, doors, event lights, hit objects, `logic_main` |
| 2 | 6,646 (423) | **placement and conversation**: NPC placement (`NPC配置`), `talk_*`, `party_menu`, load / save; ~~most `sysReqchg` calls~~ (the tally includes 1,804 `sysReqchg` calls, which are slot 2, not channel 2: see the 16 / 17 row) |
| 3 | 1,822 (323) | **show-side presentation**: `clip_show`, `talking` / `talkend`, mouth-flap on / off, camera clear, bind off |
| 4 | 1,479 (147) | **hide-side presentation**: `clip_hide`, mouth open / close (`パクオン` / `パクオフ`) |
| 5 | 889 (39) | **NPC placement and position changes**, mostly as `sysReqi` (immediate) |
| 6 | 20 (4) | rare camera / cleanup helpers |
| 7 | 213 (31) | ~~**reset, cancel and cleanup**~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-rc121314-0930 §5 N1:)* **mostly reset, cancel and cleanup (about half its parsed calls), also some repositioning and item hand-overs** (`リセット`, `ポイントキャンセル`, `clear`): the top channel pre-empts the rest |
| ~~16, 17~~ | ~~24, 26 (8, 9)~~ | ~~only `sysReqchg` to `talkhold_*` / `talkterm_*`. The engine clamps a channel to the slot count - 1 from above (page section 2.4), so these land on the top channel~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930:)* not channels: `sysReqchg`'s first operand is an override slot (`0025AF60` bounds it to `0x11` at `0025AF7E` and stores `[rax + rbx*2 + 0xC8]` at `0025AFA1`), so these are slots 16 `talkhold` and 17 `talkterm`. The `sysReqchg` calls counted under channels 2 to 5 (1,804, 14, 8 and 8 in ORACLE's `rc13_script_channels.out`) are slots too. |

For a script author, then:
- 1 is where an actor's own logic runs;
- 2 carries conversation and placement;
- 3 and 4 are the paired show / hide presentation channels, including lip flap;
- 5 is placement and repositioning;
- ~~7 is the interrupting cleanup channel.~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-rc121314-0930 §5 N1:)* 7 is mostly the reset, cancel and cleanup channel.

This is an authored convention, not an engine rule. Limit: the 12% of calls through `reqArr` arrays and computed
targets are counted by channel (the plain column) but not by function.

## RC-14: who moves an entry's run state from 1 to 2 — answered: two more promoters, same shape

A displacement sweep for `+0x11` cannot see the promotion loop: it advances a pointer to `+0x11` first
(`add rax, 0x11` ... `mov byte [rax], 2` at `003DBB35`). So [`rc14_runstate.py`](rc14_runstate.py)
([output](rc14_runstate.out)) is structural:
- an **entry-deriving** function loads the entry table `[.. + 0xa0]` and walks it with the `0x14` stride;
- in the 33 such functions it lists every byte store at `+0x11`, every byte store of 2, and every store through a
  pointer the function advanced by `0x11`.

Controls found: the promotion store `003DBB35`, the insert `003DB7A0` (`003DB8E9` / `003DB9E4`) and the unlink stores
`003DC1A4` / `003DC233`.

**Two more 1 -> 2 promoters exist, each the same loop** as `003DBB35`: `cmp byte [p], 1; jne; mov byte [p], 2;
add p, 0x14`, gated by the record's `+0x63` flag, followed by `ActorResource_SelectPendingEntryForExecution`.
- **`003DB245` in `003DB1F0`**, a sweep over every record of a manager (`003DB21A` resolves each ordinal up to
  `[manager+0x20]`), which then halves `+0x63` (`003DB25A`). It is called by `ActorSystem_InitializeManagerRuntime`
  (`0026D365`) and at **two call sites in `World_UpdateSimulationTick`** (`00314124`, `00314211`; whether both run every
  tick was not read). This is the world-tick promotion the page's section 2.5 was looking for ("the wait resolver `0025DF00` is the candidate"): it is not
  the wait resolver, it is this sweep.
- **`003DBCAC` in `003DBBF0`**, the submit path the motion setter uses (see `../fable-astra-live-facts-0930/ov16_static.md`),
  taken after a successful insert when the target is not the requester (`003DBC7F`-`003DBC87`).

`003DB754` (in `ActorResource_SelectPendingEntryForExecution`) stores the actor record's own `+0x11`, the current channel,
not an entry's run state.

**Limit.** A function that receives an entry pointer as an argument, without walking the table itself, falls outside the
structural criterion. The start `ActorResource_StartEntryScriptExecution`'s state-3 store at `003DBE68` is the example: it
is missed here, though the page already lists it. SWE2-CONTRACT's displacement sweep covered such functions for the `+0x11`
displacement. The two sweeps together cover both forms, but not a pointer both passed in and pre-advanced.


**Incorporation (SWE2-CONTRACT):**
- rows RC-12, RC-13 and RC-14: ANSWERED, citing this record;
- the scheduling page sections 2.5 (the two promoters), 2.6 (the slot map and the multi-list block) and 8 (the channel
  conventions).
