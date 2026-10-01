# SWE2-AUDIT-SPEC review of SWE2-ORACLE's RC-11..RC-21 records (1e4537034): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session `73162e75`, 2026-09-30). Request
`OPUS-REQ-AUDITSPEC-REVIEW-BATCH14-0930`. Reviewed commit `1e4537034` (SWE2-ORACLE, six records). Image
`73461D08…21F8`, static only. Nothing in the reviewed records, the register or any page was edited.

| record | rows | commit | verdict |
|---|---|---|---|
| [rc12-footer-channels-runstate-0930](../rc12-footer-channels-runstate-0930/README.md) | RC-12, RC-13, RC-14 | `1e4537034` | ACCEPT (propagation of RC-12 incomplete, routed below) |
| [rc21-verb-reach-regen-0930](../rc21-verb-reach-regen-0930/README.md) | RC-21 | `1e4537034` | ACCEPT |
| [rc11-arena-ten-0930](../rc11-arena-ten-0930/README.md) | RC-11 | `1e4537034` | ACCEPT-WITH-NARROWING (reproducibility: unrecorded census windows) |
| [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md) | RC-15, RC-16, RC-17 | `1e4537034` | ACCEPT |
| [rc18-map1-blend-arms-0930](../rc18-map1-blend-arms-0930/README.md) | RC-18, RC-19 | `1e4537034` | ACCEPT |
| [rc20-float-push-verbs-0930](../rc20-float-push-verbs-0930/README.md) | RC-20 | `1e4537034` | ACCEPT |

Overall: **ACCEPT-WITH-NARROWING** (the most restrictive row). No record's conclusion is rejected. The narrowing is
about reproducibility and propagation, not about a wrong answer.

**Re-run.** [`rerun_all.py`](rerun_all.py) runs every committed control from its own folder and compares stdout with
the committed `.out`, ignoring CR ([`rerun_summary.txt`](rerun_summary.txt)). **All 32 outputs are identical and
every script exits 0**: 14 for RC-11, 4 for RC-12..14, 4 for RC-15..17 (including the 36-minute `rc15_flow.py`), 7
for RC-18/19, 1 for RC-20 and 2 for RC-21. Four of the RC-11 outputs reproduce only with windows the record does not
state (Narrowing 1). The runs rewrite `arena_sites.tsv`, `rc15_flow.tsv` and `rc21_reach.tsv` in place; all three
come out byte-identical, and `git status` on the six record folders is clean afterwards.

**RC-12, re-derived independently: the 0-based footer holds, and the page's `mapjump` reading is off by one.**
- *The name at each byte offset, by a different route* ([`rc12_footer_join.py`](rc12_footer_join.py),
  [`.out`](rc12_footer_join.out)). The names come from the decompiled text (the w-th `function` line under the a-th
  `actor` line), not from the raw name pool that `rc12_slots.py` Part B reads. Only actors whose raw function count
  equals the text's declaration count are joined: 940 images, 17,139 actors (3,348 skipped as unaligned, so these
  counts are a subset of ORACLE's). Result: `main` sits only at footer byte `+0x04` (x3605), `talk` only at `+0x06`,
  `parameter` only at `+0x18` (x4), `mapjump` only at `+0x1A` (x1265), `talkterm` only at `+0x24`. Every one of the
  1,265 map-jump controller actors (`__MJ_CTRLnnn`) holds its non-init function at `+0x1A`. Under the 1-based reading
  `mapjump` would be at `+0x18` and `main` at `+0x02`; neither occurs.
- *The image agrees* ([`img_windows.py`](img_windows.py), [`.out`](img_windows.out), decoded with `tk.py`, not the
  record's `img.py`). `0025E159` reads override `+0xDE`, then `0025E17B mov eax, 0xb` / `0025E180 cmp ax, word
  [rcx+rbx]` / `jge` and `0025E186 movsx r12d, word [rcx+rbx+0x18]`: the word is read only when the count exceeds
  11, which is exactly word index 11 of a 0-based array. The neighbour `0025B600` reads override `+0xE0`, bound 12,
  word `+0x1A` (`0025B6F8`) and files it on channel 6 (`0025B727 lea edx, [r9+6]`, `0025B72B call 003DBB60`), the
  record's `mapjump` row of the RC-13 channel table. The REQCHG writer stores `word [rax+rbx*2+0xC8]`
  (`0025AFA1`) after `cmp ebx, 0x11` / `ja` (`0025AF7E`), so override slot s is `+0xC8+2s`, matching footer word s.
- ORACLE's own rerun reproduces all three controls (A, B 14,081 / 0, C 43 sites in 19 functions) and its tally
  (`parameter` x21 at `+0x18`, `mapjump` x1525 at `+0x1A`).

**RC-21, re-derived independently: the generator's tie-break is hash order.** [`rc21_seed.py`](rc21_seed.py)
([`.out`](rc21_seed.out)) re-implements the depth-1 rule from `census_verb_reach.py`'s text (not from ORACLE's
scripts) and runs it under `PYTHONHASHSEED` 0..11. The total is 616 in every run; 36 verbs are tied; 12 subsystems
move between seeds (for example Movement 183..190, ActorEntity 138..150, Party 40..51), and the same seed twice gives
identical labels (control PASS), so the variation is the seed. The alphabetical tie-break gives exactly the record's
d1 column (Movement 182, ActorEntity 162, Party 37, WorldAreaField 26, Resource 4, Rewards 3, total 616). Reading
the generator confirms the mechanism: `reach()` iterates `set(seeds)` and `edges[...]` (sets of strings) into a
`Counter`, and `most_common(1)` returns the first-inserted of equal counts. One wording note, not a correction:
"nine rows move" counts the fourteen GN160 rows; over all twenty subsystems, twelve move (the three extra are
omitted rows whose ranges the table already prints as [1,2]).

**Spot checks in the other records** (all hold):
- RC-11 ([`img_windows.out`](img_windows.out), [`callers_check.out`](callers_check.out)): `00504392 cmp byte
  [rax], dl` / `jb 005043A7` / `005043A7 mov ecx, 8`; the retry `0036BFE0` loads mask `022D89B8` (`0036BFF0`), tests
  the arena bit (`0036BFF8`) and on clear falls into `0036C000 jmp 0036C000`, a self-loop; the allocator `0036BC60`
  tests the same mask at `0036BCD8` and returns 0 (`0036BCDD xor eax, eax`). `00504350` has exactly the two claimed
  callers `003AA109`, `00500A20` on the raw index, a fresh E8/E9/jcc sweep and relocations (control: `0036A100` 110
  callers on both).
- RC-16 / RC-17 ([`callers_check.out`](callers_check.out)): `00266530` only from `00267B79`, `002679F0` only from
  `0026CEB0`, `00360880` only from `002281B7`, `00285EA0` only from `0022917A`, each on all three forms. RC-17 K4
  holds: `00360880` loops `ebx` 1..3 over `022CB9C4 + 4(m-1)` (`0036088F`, `003608B7 add rdi, 4`), takes the lowest
  set bit below 8 (`003608A0`-`003608AA`) and makes one `00360710` call per manager.
- RC-18: `0031B83A` loads `[02EBF190]` and `0031B841 movzx eax, byte [rax+rbx*2+0x5A5A]` reads map-1 slot i, as
  stated for `BattleUnit_FindMappedDefinitionSelectorByIndex`.
- RC-19: `002EB271 movss xmm1, [rsp+0x60]` / `comiss xmm1, xmm6` / `jb 002EB2A6` → `002EB2C9 call 004272E0`, else
  `002EB29F call 004270A0`. `004272E0` is `and dword [rcx+0x294], 0xFFFDFA7F` (clears bits 7, 8, 10, 17) then `or
  0x20` (sets bit 5), as tabled.
- RC-20 ([`rc20_refs.py`](rc20_refs.py), [`.out`](rc20_refs.out)): the only stored pointers to the four bodies and
  the thunk are seven relocations in the family-0 table `01EED700`, at record `+0` (begin) of call ids `0x003E`,
  `0x0059`, `0x0042`, `0x005D`, `0x04CE`, `0x009A` and (thunk) `0x04D2`. The only code reference is the thunk's own
  `jmp` at `0033F850` (the sweep's positive control).

**Controls.**
- RC-12 Control B (printed number == raw index) is sensitive to the defect in question: had the footer been 1-based,
  the tool's `specialType = i` numbering would print `n` = k+1 and B would fail. The decisive evidence is still the
  name-at-offset tally, which this review reproduced by an independent join.
- RC-21 C5/C6 (bipartite match plus an out-of-range negative) discriminate; C2/C3 alone would not, since any draw
  inside the ranges passes them.
- RC-11 `riprefs.py`'s control (`0036C1F0` stores `022D89BC`) is a positive scanner control and is sensitive to a
  broken rip decode. RC-14's S1-S4 controls are positive only (known stores found); the negative claim rests on the
  shapes being exhaustive, which the record states.

**Narrowing 1 (RC-11 reproducibility).** `riprefs_02096Axx.out`, `riprefs_022D89B8.out` and both `basedisp_*.out` do
not state the windows used, and the script's default window (`lo + 8`) does not reproduce them. They reproduce
byte-for-byte only with `riprefs.py 02096A00 02096C78` and `riprefs.py 022D89B8 022D89BC` (found by trial; recorded
in `rerun_all.py`). The conclusions are unaffected.

**Correction wording for the row owner (SWE2-ORACLE, record; SWE2-CONTRACT, RC section).** Append to
`rc11-arena-ten-0930/README.md` Method: "The census windows are `riprefs.py 02096A00 02096C78` (the `02096Axx`
output), `riprefs.py 022D89B8 022D89BC`, `basedisp.py 02096A00 02096C78` and `basedisp.py 022D89B8 022D89BC`."

**Narrowing 2 (RC-12 propagation; for the incorporation owner OPUS, register section SWE2-CONTRACT).** The RC-12 row
is ANSWERED on this record (`7dce8563b`), but the record's own consumer list is not yet propagated at HEAD:
- the scheduling page `01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md`
  line 79 still says the wait resolver's word `+0x18` "is `special[12]`, the `mapjump(12)` function", and lines
  223-225 still say it asks "is the running function this actor's `mapjump` special function";
- `04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md` line 353 still says `+0x0C` is set "when the
  bound script is the `mapjump` special function";
- `_types/fields.tsv` `ActorStorageRecord 0x0C8` still says the slot meaning is not claimed.

Wording: replace each "`mapjump`" reading of footer word `+0x18` with "word `+0x18` is `special[11]`, the actor's
`parameter` function (0-based footer `{u16 count; u16 special[18]}`, word k at `+2+2k`;
`rc12-footer-channels-runstate-0930`, controls A and B of `rc12_slots.py`)"; on the actor-record page, "`+0x0C` bit 0
is set when the running function is the actor's `parameter` special function"; in `fields.tsv` +0x0C8, "override
slot k selects footer word k = special type k".

**RC-13 later work (noted, not judged).** The register row reads "OPEN, NARROWED … OUT OF EVIDENCE BOUNDARY" after
SWE2-CONTRACT's `7dce8563b`. The board task `SWE2CONTRACT-PUB-RC4-RC13-0930` ("RC-13 ANSWERED (disposition a)") is
READY and unpublished at the time of this review. SWE2-AUDIT-SEM's `837cdd743` reviewed FABLE's RC-12..17 records
(`82cb3490a`, `0870d8b62`), not these.

**Not reviewed.** RC-15's 36-minute flow was re-run for identity only; its depth cuts and unfollowed stored pointers
are the record's own stated limits. RC-18's residue table (120 sites) and the unicorn mode emulation were re-run, not
re-derived.
