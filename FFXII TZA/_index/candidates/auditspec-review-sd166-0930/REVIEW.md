# SWE2-AUDIT-SPEC review of SD-166 (sd166-arena-7-0930, OPUS, b3f5172c9) and kit regval.py: ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed: OPUS's
`b3f5172c9`, the [README](../sd166-arena-7-0930/README.md), `sd166_check.py` and the new kit tool
`Database/Tools/analysis-kit/gfz-scripts/regval.py` (introduced in the same commit). First half measured at HEAD
`9b6c5bc93`, resumed and finished at HEAD `b58c633f7`. Static, certified image, plus the shipped-script census.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD166-0930 | sd166-arena-7-0930 | `b3f5172c9` | ACCEPT-WITH-NARROWING (two debug verbs are four; regval limits) |

**Re-run.**
- `sd166_check.py` rewrites `sd166-verbs.tsv` and `sd166-verbs.out` next to itself, so I ran an unmodified copy,
  [rerun_copy_sd166_check.py](rerun_copy_sd166_check.py), from this folder.
- [rerun_sd166_check.out](rerun_sd166_check.out), [rerun_sd166-verbs.out](rerun_sd166-verbs.out) and
  [rerun_sd166-verbs.tsv](rerun_sd166-verbs.tsv) are identical to the committed files (CR ignored). P0 self-test 4/4,
  `FAILS 0`.
- The package dir is clean.

**Re-derived independently.** Tools: [arena_ix.py](../auditspec-review-sd164-167-0930/arena_ix.py) and adump.py, from the
SD-164 review.
- **W1 / A2, the writers of `022D89BC` in both addressing forms** ([active_sweep.py](active_sweep.py) /
  [.out](active_sweep.out); [active_sweep2.out](active_sweep2.out) covers the rest of the save stack up to `022D8BD0`).
  - rip operands into `022D89A8..022D8A60`: 46. Image-base operands (non-rip base, displacement = VA − 0x120000): 6,
    all in the push `0036C1F0` (`rbx = 0x120000` from `0036C1F8 lea rbx, [rip - 0x24c1ff]`). None of the 6 writes
    `022D89BC`. There is no DIR64 slot in the window, and no access at all to `022D8A60..022D8BD0`.
  - Functions writing `022D89BC`: `00369860` (`00369A65`, `00369AA3`), `00369D30` (`00369D73`), the pop (`0036C16B`),
    the push (`0036C27F`) and `0036CB00` (`0036CB57`, `0036CB81`). That is the package's five.
  - The map `022D89A8` is written only by the two identity fills (`00369D79`, `0036A282`: `lea` + byte loop to 0xF), and
    indexed only at `0036C272`, in the image-base form.
  - The save stack is written only by the push. The pop restores from it. So a restored value is an earlier active
    value.
- **W1, the initialisers.**
  - `00369D30` has 13 raw callers. In `0022A0B0` they run in the order 2, 3, 4, 5, 6, 7, 8, 9, 0xB. The others are
    `0025A990` (0xD), `0025AA30` (0xE), `0037B3D0` (0xB) and `003E9AA0` (0xC).
  - The heap-destroy `0036D160` (the only other writer of the mask `022D89B8`, `0036D169`) has 8 raw callers, all for
    heaps 0xB..0xE. So the mask never returns to 0 once heap 2 is up, and `00369D30` never rewrites `022D89BC` after
    the first init.
- **A1.** Each of `0036BFE0`'s 4 raw callers loads `[022D89BC]` into the heap argument. Inside `0036BFE0`, `ecx` is used
  only for the mask spin: the heap record and the `0036BC60` call both re-read `[022D89BC]` (`0036C013`, `0036C08B`).
  The other callers of `0036BC60` are the reclaim `0036A2A0` and the realloc `0036CB00`. The realloc's heap is the
  existing block's own arena (byte `[block − 0x3D]`, `0036D0C6`). That does not select a new arena, so A1's conclusion
  stands.
- **A3, the 135 push sites.** `0036C1D0` has 135 raw rel32 sites, all `call`, set-equal to retool's list. The per-site
  value sets and the aggregate are exactly the package's (regval_audit.out T1).
- **A4.** Read by hand:
  - `00384420`: the `R 0x8478a0` term is `mov eax, 3; ret`.
  - `00249210`: the `M` terms are `0039352E [rbx]` (the one caller `00574F78` passes the table `00D23658` =
    `{2,1},{2,2}` with count 2), `003C1DC9 [r11]` (`003C1D70`'s one caller `005632C0` builds `+0 = 2` at `00563325`)
    and `003C1FFD [r14]`. `003C1FFD` is reached only through the thunk `003C2190`, and its 9 raw call sites, in
    `002B7B80`, `002BAF80` and `003CB4F0`, all pass a stack struct whose `+0` is set to 2 before the first call.
  - `003E9AA0`: `0034D080` pops twice. The second pop is the first push, `PUSHII 65535`, and it goes to `ecx`. A
    negative value keeps `ecx = 6` (`003E9AB3`, `003E9ABF cmovns`).
- **S1, and the defect in A4.** Of the claims about which verbs exist and who calls them, the package gets the verb
  catalogue wrong.
  - The class-2 command table is `01F26720`: 0x20-byte records, and record `id` at `+0x20·(id+1)`. Dispatch is
    `002621D0` -> `003DC2A0`: class = operand `sar 0xC`, id = operand `& 0xFFF`.
  - Its records hold `0050DA30` for 0x2003 `debug_tkmalloc` and `0050DBD0` for 0x2008, as the package says. They also
    hold **`0050D8F0` itself** for 0x2004 `debug_tkmalloc_4` (slot `01F267C0`) and **`0050DAD0` itself** for 0x2009
    `debug_tkmallochandle_9` (slot `01F26860`). Both slots are DIR64-relocated.
  - So the two push functions are verb handlers in their own right. A4's check `callers(0x0050D8F0) == [0x0050DA30]`
    sees only the direct `jmp` (`0050DA8A`), and S1 counted only 0x2003 and 0x2008.
  - Re-run of the census over 0x2003, 0x2004, 0x2008 and 0x2009 ([census_debugverbs.out](census_debugverbs.out)): 0
    calls. The only matching verb is 0x395, 18 times.
  - `003DC2D0` leaves the class-2 table in every slot it does not overwrite, i.e. classes 1, 2, 4, 6 and 8..15. The
    alias ids `(k<<12) + {3, 4, 8, 9}` for those classes also have 0 calls ([census_aliases.out](census_aliases.out)).
  - So the conclusion survives. The A4/S1 wording does not.

**Controls.**
- **Census sensitivity** ([census_ctl.py](census_ctl.py) / [.out](census_ctl.out)). With every catalogued class-2 and
  class-3 id wanted, the same decoder finds 14,069 class-2 calls (e.g. 0x2026 `debug_mapjump` 2,697,
  0x2086 `debug_tty_string` 1,732) and 2,742,054 class-3 calls. The zero for the debug-tkmalloc verbs is a property of
  the data, not of the decoder.
- **regval soundness on this query** ([regval_audit.py](regval_audit.py) / [.out](regval_audit.out),
  [regval_audit2.py](regval_audit2.py) / [.out](regval_audit2.out), [regval_audit3.py](regval_audit3.py) /
  [.out](regval_audit3.out)). Each defect was named first, then measured.
  - *Memo reuse under a loop cut.* Clearing the memo before every site, and running in reverse order: 0 of 135 sites
    change.
  - *Dropped indirect edges.* The 174 decoded bodies contain 12 indirect `jmp`. I decoded 11 jump tables; the twelfth,
    in `002E60F0`, I read by hand, and its push site `002E6246` sets `ecx` locally (`lea ecx, [rdx + 1]`, rdx = 5).
    Recording every node each walk visits: 0 walks reach a case target or any other node with a missed predecessor.
  - *Out-of-body edges.* There are 3 rel32 "calls" into the interior of `003EDAD0`, but none is a real instruction when
    decoded from its `.pdata` start. 2 rel8 candidates have no `.pdata`, and no walk reaches their targets.
  - *Missed callers.* For all 12 (function, argument) pairs regval followed, raw E8/E9/jcc callers equal regval's.
    There are no DIR64 slots, and no rva32 hits outside unwind data.
  - *Unmodelled writers.* `inc ecx`, `pop rcx`, `sete cl` and `and ecx, imm` all give U. A single push site with
    `mov ecx, K` right before its call resolves to {K}.
  - *Width.* regval treats `movzx/movsx r, <8/16-bit reg>` as a copy (at `001BAD17` it returns a constant, not U), and
    pins the whole register on `cmp al, K`. 3 of the 135 walks cross such a node (`003EA02A`, `00466FE8`,
    `003800EC/F0`, `003C2076`). Read by hand, each carries a small constant, or is not the arena register, so no value
    changes.

**Citations checked.** `0036C272`, `0036C27F`, `00369D79`/`00369DA0`/`00369DA8`, `0036A282`/`0036A290`/`0036A298`,
`00369D71`, `008478A0`, `00574F5C`/`00574F64`, `0039352E`/`0039355D`, `00563315`/`00563325`, `002B7CEF`, `002BB0F7`,
`003CB5CB`, `003C2193`, `0034D0A1`/`0034D0AD`, `003E9AB3`/`003E9ABF` and `0026186D` each say what their sentence says. The
README's "two debug verbs" is the one defect: it names half of the entries.

**Runtime routing.** None. Static evidence plus the census settle it.

**Correction wording** (the producer applies):
- Answer paragraph: replace "The only way to reach it is a script calling one of two debug verbs, and no shipped script
  does." with:
  > The only way to reach it is a script calling one of four class-2 debug verbs, and no shipped script calls any of
  > them: `debug_tkmalloc` 0x2003 and `debug_tkmallochandle` 0x2008 (handlers `0050DA30` / `0050DBD0`, which jump into
  > the push functions), and `debug_tkmalloc_4` 0x2004 and `debug_tkmallochandle_9` 0x2009, whose handlers are the push
  > functions `0050D8F0` / `0050DAD0` themselves (class-2 table `01F26720`, slots `01F267C0` / `01F26860`).
- A4 rows `0050D8F0` / `0050DAD0`: "`debug_tkmalloc` (`0x2003`, handler `0050DA30`) and itself the handler of
  `debug_tkmalloc_4` (`0x2004`)"; likewise "`0x2008` via `0050DBD0`, and itself the handler of `0x2009`".
- S1: "`debug_tkmalloc`, `debug_tkmalloc_4`, `debug_tkmallochandle` and `debug_tkmallochandle_9` (0x2003, 0x2004,
  0x2008, 0x2009) are never called". The checker's S1 should census all four ids. Its A4 caller test should also check
  the DIR64 slots, which is where it went blind.
- "For modding": `debug_tkmalloc(7, ...)` -> "any of the four debug verbs with 7".
- regval.py docstring (kit), add after "It does not see indirect callers ...":
  > nor jump-table (indirect `jmp`) edges into a node that also has a direct predecessor (such a node gives no U), nor
  > jumps into the body from code outside its extent. `movzx`/`movsx` from an 8- or 16-bit register is treated as a copy
  > of the whole register, and a `cmp`/`test` on a sub-register pins the whole register.
