# OPUS's 14-Story byte verdicts on FABLE's two flag-bank pages (FABLE, 2026-10-02)

Board request OPUS-REQ-FABLE-STORY-READINESS-VERDICTS-1002. OPUS decided 13 value items of the 14-Story readiness map
at the shipping image ([`byte-verdicts.md`](../opus-story-readiness-fixes-1002/byte-verdicts.md), control
[`story_check.py`](../opus-story-readiness-fixes-1002/story_check.py)) and applied its own share: the shared README and
its event-memory page. This record holds FABLE's share, which covers the two flag-bank pages. Every changed sentence
strikes the HEAD text and restates it, tagged *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-Vn, record)*.
Two notes are tagged *clarified* (C-V11's id-set span and C-V12's `bpl`), because the page text there is not wrong.
The front matter, checkboxes and register rows are unchanged. The edits are in
`Database/Tools/work/FABLE/storyfix/apply.py`: 14 anchors per page, each matching exactly once, all-or-nothing.

## What changed, per verdict

| verdict | `persistent-flag-banks.md` | `CONTRACT-persistent-flag-banks.md` |
|---|---|---|
| C-V1: five storage banks, six accessor families | the lede ("Six banks of them"); the §2 heading "Six banks, all inside the save payload", plus a one-line note under it | §1 "Six banks of flags"; §2 "the other five banks have a dedicated query" becomes four banks with five query functions; §3 "The six banks are what is mapped"; the §15 evidence row "six banks, offsets and sizes" |
| C-V2: a new game sets 52 flags, because id 0 is dropped | §8f "What the player sees": "Room for fifty-three authored ids" becomes fifty-two, because `SetPrimary` accepts only ids 2 to 0x1FF | §11 "the ids in `mapjumpgroupinit.bin` are switched on" becomes 52 of the 53 |
| C-V3: the gate is 122 B | - | the subtree section: "~127 B" becomes 122 B (`0032A8A0` to its `ret` at `0032A919`) |
| C-V4: the reader's entry is `002BA530` | - | §14 item 1 and the §15 Bank2048 evidence row: `002BA548` is struck and replaced with `002BA530`, because `002BA548` is an instruction inside that function |
| C-V5: the gate reads Primary, not `Bank64A` | the inlined-write census table: the gate is struck from the `Bank64A` `+0x1384` row (its test is Primary `+0x14F4`, `0032A900`) | - |
| C-V6: `0032A8C6` is inside the gate | - | the §15 "four Bank64 accessors" row: `0032A8C6` is struck from the siblings' unsigned compares and labelled as the gate's own `jb` after its `0x200` bound |
| C-V8: two pairs, not 50 / 45 / 5 | the §8d table row for `002FAFD0`; a note under the §8d code sketch; "A three-way outcome, 50 / 45 / 5" becomes two two-way pairs (50 / 50 without the armlet, 95 / 5 with it) | - |
| C-V9: field widths | the §8d table: `record[2]` becomes byte `+0x04`, and `record[2]` is described as counting shorts; `record[9]` becomes byte `+0x09`. The note under the sketch says `record` is a byte pointer there. "A different record layout" now gives byte offsets `+0x09` / `+0x04` / `+0x0B` | - |
| C-V10: one flag writer downstream of a roll | §8d "Two, and only two" now reads "two functions both draw and set a flag, but only `002F8060` sets it after its draw; `002FAFD0` sets it at `002FAFFD`, before its first draw at `002FB01D`". "What this settles" and the §8e conclusion ("Exactly two functions ... turn a random draw into permanent save state") are restated: in neither function does the flag depend on the draw | - (its §9 and §16 already say this) |
| C-V11: `SetBank64A` has no lower bound | - | §10's "between `+0x1164` and `+0x1384`" becomes `+0x1384` + trunc(id / 8) with no lower bound (a signed `jge` at `0032AC77` / `0032AC7A`), and that span belongs to an id set. The 2026-09-08 correction's "down to `0x0FE0`" gains a clarified note: the span is the test id set's, and ids -1 to -7 write nothing |
| C-V12: `bpl` is 0, so `002628B0` clears `+0x1534` | - (its AA-8 item already says "also clears it") | §14 item 3: the writer `00262A76` (`bpl`) gains a clarified note that `bpl` is zero there, so this writer clears the byte |
| C-V13: 163 calls in 98 functions | the AA-5 answer: 104 becomes 98 | §14 item 2 and the §15 gap evidence row: 104 becomes 98 |
| C-V14: the gate has 32 callers | §8b: "30 query callers" becomes 32 callers of the gate (59 direct call sites in 31 functions, plus one caller through the gate's thunk). The setter count, 4, was not re-derived and is unchanged | - (§6 already says 32) |

Every verdict was placed. Three edits go beyond the line numbers that `byte-verdicts.md` lists. Each one states the
same fact the verdict decides, on the same page:
- C-V1 on the main page's lede and on CONTRACT §3 and the §15 row.
- C-V10 on "What this settles".
- C-V13 on the CONTRACT §15 gap row.

The C-V11 "query twin" was checked before the edit. `QueryBank64A` `0032A9A0` has the same signed `jl` (`0032A9A4`
/ `0032A9A7`) and the same truncating index. A negative multiple of 8 reads before the bank. Any other negative id
gives a shift of 25 or more on `dl`, so its mask is 0 and the query returns false. The query twin therefore agrees
with the setter, and the pages say nothing about it that this verdict changes.

Left as it is: the main page's UQ-138 question text ("Six banks with different capacities implies six different
categories", line 488). That sentence is the closed question's original wording, and §2 and AA-4 now carry the count.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/14-Story-Event-Quest-Hunt/persistent-flag-banks.md`
affected: `Database/FFXII TZA/14-Story-Event-Quest-Hunt/CONTRACT-persistent-flag-banks.md`

- consumer: `persistent-flag-banks.md`, the lede, §2, the AA-5 answer, §8b, §8d, "What this settles", the
  inlined-write census table, §8e and §8f "What the player sees": revised-here
- consumer: `CONTRACT-persistent-flag-banks.md`, §1, §2, §3, §10, §11, §14 items 1 to 3, §15 and the subtree
  section: revised-here
- consumer: the README of 14-Story and `event-memory-at-actor-bind.md` (OPUS applied them,
  [`apply_14story.py`](../opus-story-readiness-fixes-1002/apply_14story.py)): agrees
- consumer: CONTRACT §2's interface table (`0032A8A0` 122 B), §6 (32 callers), §9 and §16 (one roll-fed writer), the
  §14 `mapjumpgroupinit.bin` row (52 set) and §15a's per-helper census rows: agrees, and these are unchanged
- consumer: the main page's AF-6 answer (two pairs, record widths) and its AA-8 item (`002628B0` clears `+0x1534`):
  agrees, and these are unchanged

Addresses behind the restated text that are kept off the pages, by role. These functions are filed to other layers,
are thunks, or are not cited on the page at HEAD. Each page gains only addresses inside functions it already cites,
none of them a declared-family member.

| role on the page | address(es) |
|---|---|
| the gate's thunk (the 32nd caller is its one caller) | `0032A920` (5-byte `jmp` to the gate); its caller `00321190`, call at `00321244` |
| a gate caller that also tail-jumps to it | `003FFF40`, `jmp` at `003FFF62` |
| `SetPrimary` accepts only ids 2 to 0x1FF | `0032AB64` `lea eax, [rcx-2]`; `0032AB6A` `cmp eax, 0x1FD`; `0032AB6F` `ja` |
| `+0x1384` + trunc(id / 8), and a shifted mask of 0 | `0032AC81`-`0032AC9A` (`cdq` / `and edx, 7` / `add` / `sar edi, 3`); `0032AC9F` `shl bl, cl` |
| the query twin's matching guard and index | `0032A9A4` / `0032A9A7` `cmp ecx, 0x40` / `jl`; `0032A9E2` `shl dl, cl`; `0032A9E4` `test` at `+0x1384` |
| `002F8060` draws, compares and then sets | the draw at `002F8218` (`call 00379CD0`); `002F8231` `cmp r8d, 0x4B`; the set at `002F8253` |
| `002FAFD0`'s first draw comes after its flag write | the flag id `movzx` at `002FAFEA`; the gil-chance byte `+0x0B` at `002FB036`; the armlet test at `002FB0E1` / `002FB0E7` after the status gate at `002FB0DA` |
| the trap's flag id is byte `+0x04` (`record[2]` counts shorts) | trap `002FA740`: `002FA7E8` `movzx eax, byte [rdi+4]`; `002FA81E` `movsx eax, word [rdi+2]`; `002FA815` byte `+5` |
| `bpl` is zero at the `+0x1534` store | `002628B0`: `0026292A` `xor ebp, ebp`; `ebp` is stored and never reloaded before `00262A76` |
| `Bank512`'s Low and High pairs address one region | the queries test at `0032AAAB` / `0032AB1F`; High adds `0x100` at `0032AAE7` (query) and `0032AE04` (setter); the setters `or` at `0032ADB6` / `0032AE3A` |
| the census's three helpers (C-V13) | `002EF2B0` 121 calls / 70 functions, `002EF640` 40 / 28, `002EF2D0` 2 / 2 |

Checks on copies of the HEAD pages: `apply.py --check` and then the real apply each matched 14 anchors per page.
The `adrift_predict.py` HITS were 0 before and 0 after on both pages. The added citations are five on the main page,
in `002FAFD0` and `0032A8A0`, and two on the contract, in `002BA530` and `0032A8A0`. None of them is in a function the
page does not already cite (`storyfix/newcites.py`).

run: [story_check.py](../opus-story-readiness-fixes-1002/story_check.py) at 31f29775a (FAILS 0)
