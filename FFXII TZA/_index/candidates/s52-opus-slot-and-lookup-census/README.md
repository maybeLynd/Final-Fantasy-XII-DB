# S-52: the manager-slot contract's two remaining debts, answered statically (OPUS, 2026-09-26)

**Evidence: STATIC (the SHA-asserted image) plus a DATA census.** The census covers the decompiled shipped field scripts,
FABLE's corpus `Tools/work/FABLE/pub140-scratch/corpus/us/*.txt`: 1,114 files, the corpus the navigation page's
`setmapidfloor` count used. **Domain: that corpus.** Other script sources (battle scripts, other languages) are not censused.

**The debts.** `CONTRACT-manager-slot-entry-tables.md` §13 lists them as *"still owed, and it is live-only"*, and AUDIT-SEM's
S-52 gap names both:
- **(2)** whether any caller ever passes a fifth argument large enough to leave the slot;
- **(3)** whether `002640C0` ever returns a slot other than the one side B would have been handed.

**6 / 6 pass; `result.json` is byte-identical over two runs (md5 `c47c1149…`).**

| case | observed |
|---|---|
| `T1_four_handlers_slot_from_002640C0_three_pops_first_pop_is_arg5` | the only callers of the binds `003DA400` (A) and `003DD230` (B) are four script verbs: `camerastart_7d` (`0034F2F0`), `camerastart_7e` (`0034F930`), `camerashakestart_1a2` (`003492F0`) and `camerashakestart_1a3` (`00349730`). Each takes its slot from `002640C0` and pops three VM values (`00267E10`). **The first pop is the fifth argument** (`mov [rsp+0x20], ebx`) |
| `T1_7e_and_1a3_push_minus1_7d_and_1a2_do_not` | `7e` and `1a3` push `-1` first (`00267F90`, `edx = -1`), so their fifth argument is always `-1` (index 0 after the clamp). `7d` and `1a2` push nothing, so theirs is the script's **last** argument (LIFO) |
| `T2_subframe_is_1_mainframe_is_0` | `getcamerasubframe` `0050D1C0` → `0053DD10` = `mov eax, 1`, always 1. `getcameramainframe` `0050F100` → `005C5230` = `xor eax, eax`, always 0 |
| `C1_corpus_last_args_are_the_two_natives_or_literal_110` | 1,114 scripts: `camerastart_7e` 3,833 calls, `camerashakestart_1a3` 328, `camerastart_7d` 39, **`camerashakestart_1a2` none**. The 39 `7d` calls end in `getcamerasubframe()` 37 times, `getcameramainframe()` once, and the literal **110** once |
| `C2_max_index_110_stores_at_F4_inside_the_0x200_slot` | the largest shipped `lookupIndex` is 110. Side A then writes its reverse-lookup word at `slot + 0x18 + 2 × 110` = **`slot + 0xF4`** (`003DA4B9`), **inside** the `0x200`-byte slot. **No shipped call leaves the slot.** An index above 1 still writes past the two words the reset clears (§14.3, unchanged). Side B's callers pass `-1` or nothing |
| `T3_both_resets_read_the_current_slot_context_02099D70` | `002640C0` is `mov rax, [02099D70]; ret`, the current-manager-slot context. Side A's reset `003DA370` reads it at `003DA38F`. Side B's reset `003DCF60` has **one** caller, `0034B100`, which reads it at `0034B104` and passes it at `0034B109` with nothing in between. **Both sides therefore resolve the same slot, by construction**, whenever they run from one context |

**What this changes.** Debt (2) is answered for the censused corpus: the largest value is 110, inside the slot. Debt (3) is
answered structurally: side B's slot comes from the same `002640C0` read. Neither needs the live game.

**What it does not settle.** Whether some other code path writes `[02099D70]` between a verb's slot read and its bind. The
`02099D70` writers are save / set / restore wrappers (`0025AFC0`, `0025E400`, `002623A0`, `00263050`, `00263230`, `00263AC0`,
`00264050`, `0026C3E0`, `0026C5D0`, `0026E060`), the pass's publish (`0025DA8C` / `0025DAB3`), `0026A480` and the two
binders. Inside the four handlers, no call intervenes between the read and the bind except the VM pops.
