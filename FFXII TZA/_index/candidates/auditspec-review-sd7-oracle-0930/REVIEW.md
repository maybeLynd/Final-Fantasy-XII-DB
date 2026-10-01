# SWE2-AUDIT-SPEC review of SD-7 (sd7-stored-app-pointer-0930 at dedfaf0d7): REJECT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
SWE2-ORACLE's `dedfaf0d7`, [README](../sd7-stored-app-pointer-0930/README.md) and `sd7_app_pointer_sites.py`. Work began
at HEAD `9b6c5bc93` (parked) and was resumed and finished at HEAD `48de14c6b`; no commit between them touches the
record directory. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| ORACLE-REQ-AUDITSPEC-SD7-0930 | sd7-stored-app-pointer-0930 | `dedfaf0d7` | REJECT |

**Defect.** The E1 test breaks its own rule. The README counts "the stack" among the holders of the application
pointer, and `e1()` does refuse to exclude a load based on `rsp`. But it treats a load through a **frame-pointer `rbp`**
as a holder displacement, and those are stack slots too. **8 E1 rows** rest on exactly that: a stack-passed argument
of a PPFX function, read through `rbp`. regval does not follow a stack argument into the caller, so nothing bounds
those values. So "133 by holder displacement" and "158 of 192 excluded" are wrong. The correct figures are **125 and
150**.

**Re-run.** [rerun_sd7_app_pointer_sites.out](rerun_sd7_app_pointer_sites.out) is identical to the committed `.out`
(CR ignored). K1-K5 and S1 PASS, `FAILS 0`. I re-ran it again at `48de14c6b`: still identical. Package dir clean after
the re-runs: yes (`git status --porcelain --ignored` on it is empty). [dump_pkg_rows.py](dump_pkg_rows.py) captures the
package's own 192 rows into `pkg_rows.json`, for comparison only.

**The defect, settled with numbers** ([sd7_rbp.py](sd7_rbp.py) / [.out](sd7_rbp.out),
[sd7_e1base.py](sd7_e1base.py) / [.out](sd7_e1base.out), [sd7_ctx.py](sd7_ctx.py) / [.out](sd7_ctx.out)).
- **R1.** I emulated the prologue of each E1 row's load. Each of the 8 is `mov rax,rsp … lea rbp,[rax-k]`, with no
  rewrite of `rbp` before the load. Each load is a slot in the caller's frame, past the home area:

  | function | sites | load | frame (rbp) | slot read |
  |---|---|---|---|---|
  | `00739530` | `00739C9D` | `007397BE [rbp+0x138]` | entry−0x58 | entry+0xE0 |
  | `00739DF0` | `0073A753`, `0073A894` | `00739E85 [rbp+0x550]` | entry−0x498 | entry+0xB8 |
  | `0073BD30` | `0073C4FF` | `0073C4B7 [rbp+0x200]` | entry−0x1B8 | entry+0x48 |
  | `0073BD30` | `0073C56A` | `0073C521 [rbp+0x208]` | entry−0x1B8 | entry+0x50 |
  | `0073E570` | `0073E63A`, `0073E8DC`, `0073E9BE` | `0073E5A6 [rbp+0x9f]` | entry−0x2F | entry+0x70 |

- **The other 3 rbp rows are legitimate.**
  - `0074C790` ×2: `rbp` is a pointer loaded from a stack slot at `0074C7A6 mov rbp,[rsp+0x188]`
    ([sd7_0074C790_root.out](sd7_0074C790_root.out)), so `[rbp+0xa8]` is an object field.
  - `00771B30` (`00771C06`): the same. `rbp` comes from `00771BC9 mov rbp,[rsp+0x1a8]`, so `00771BF3 [rbp+0xa8]` is a field.
- **The 7 rows the first probe flagged through `rcx` / `rax` / `r8` are not stack loads.** I read each by hand:
  - `00764240` ×2 and `007677B0` ×2: the base is an array element, `[rdi+rbx*8]` or `[rbp+rbx*8-0x40]`;
  - `0078E3C0`: the base is the incoming `this`;
  - `00623B10` ×2: the leaf `0061ECD3`, where `rcx` is incoming.
- **All 133 E1 rows** (sd7_e1base): I took the last write of each load base, on the aligned walk, with a root-prologue
  fallback for chained chunks. Exactly those 8 rows have a stack-derived base. The other 125 do not.
- **R2: corrected partition.** I re-ran the package's own `e2` / `e3` / `slot_disps` on the 8 rows. None of E2, E3 or E4
  takes any of them, so all 8 go to the residue. The corrected partition is **E1 125, E2 13, E3 2, E4 10, residue 42**:
  150 of 192 excluded. All 8 belong to the PPFX group, which grows from 20 to 28.

**Re-derived independently, and holding** ([sd7_indep.py](sd7_indep.py) / [.out](sd7_indep.out); pefile + capstone;
it reproduces its committed `.out` exactly).
- **K1.** A raw FF /2 and FF /4 sweep at displacement 0x78 (any base, SIB, disp8 or disp32) decodes 192 sites. 188 lie
  on `.pdata` boundaries. The other 4 are leaf tail-call thunks outside `.pdata` (`0017F168`, `00789DEA`, `007E8BA6`,
  `008581A3`), and the package has them too. The match is 192/192. No rbp-, rsp- or index-based dispatch form exists.
  Control A0: the same sweep at 0xF0 finds `0079C23A`.
- **K4.** `008C5760` holds 31 code pointers, and the next qword is not code. Slot 15 is `0017D1A0`. The
  GameApplication TD RVA occurs twice: in its COL and in its own BCD. Only one CHD holds that BCD, GameApplication's own
  `01CEC020`, with 4 bases. No class derives from it, so the 31-slot E4 threshold holds.
- **E4.** I read all 10 windows. The object register is non-volatile and not written between the site and the dispatch
  at slot 31 or above. At `00863850`, `+0x138` precedes the site through the same `rsi`; I read that one by hand.
- **E3.** `001FBB40` installs `009043D8` DynGeo3DInstance, and `001FB870` installs `00904328` DynGeoTextureInstance.
- **E2.** I recomputed the raw vtable memberships of all 13 methods. None is in GameApplication's hierarchy.
- **G.** 19 non-residue rows took their terms in callers. None of them has an address-taken function in a
  3-level direct-caller chain. The instrument's positive controls pass ([sd7_gctl.py](sd7_gctl.py) / [.out](sd7_gctl.out)):
  - `0017D1A0` shows q1;
  - `00227EE0` shows lea1;
  - the chain from `002475D0` reaches its caller's root `00227EE0`.

**Controls.** R1 has a positive and a negative control:
- positive: `00739C9D`, read by hand, must come out a stack slot, and it does;
- negative: `0074C790`, whose rbp is a loaded pointer, must not, and it does not.

sd7_e1base has the same pair: the 8 rows, and `0074C8EC` / `0074CA3D` / `00771C06`. Its first run failed its positive
control. The cause was a too-short decode window and the chained chunk of `00739530`, and both were fixed. The package's
S1 gate checks only that the partition sums to 192, so it cannot see a misclassification between the classes.

**Citations checked.** I opened these, and each supports its sentence:
- the E3 constructor `lea`s `001FBB4E` / `001FB87E`;
- the 10 E4 dispatches (sd7_indep D);
- the slot-15 / slot-30 entries of `008C5760`.

`0079914C` (K2) I took from the package's own PASS; I did not re-read it. **Prose
defect:** the PPFX group says its rows are "loads at `+0x20`, `+0x38`, `+0x78` or `+0` … or stack slots". But
`0075DA10` ×2 have the terms `006FF4B4 [rbx-8]`, `0075DCD4 [rdx+0xa8]` and "argument rdx of `0075DD70`: no direct
caller". They stay in the residue only because that argument is unresolved.

**Runtime routing.** None. The record claims nothing live.

**Repair the producer applies.**
1. `e1()`: treat a load whose base is a frame pointer as a stack slot, the same as `rsp`. A frame pointer here means an
   `rbp` set to entry rsp − k in the prologue and not rewritten. With that change the S1 output must read
   `E1 125, E2 13, E3 2, E4 10, residue 42`. Gate the partition values, not only their sum.
2. README, method table: E1 **125**. Add this rule sentence: "A load through a frame-pointer `rbp` is a stack slot and
   is never excluded."
3. README title and row text: "150 of the 192 … 42 remain". The PPFX group is 28: add `00739530`,
   `00739DF0` ×2, `0073BD30` ×2 (`0073C4FF`, `0073C56A`) and `0073E570` ×3, each "a stack-passed argument read through
   the frame pointer". The row totals become 5 render-context, 4 Bullet, 28 PPFX and 5 game code.
4. PPFX group text: add "or, at `0075DA10` ×2, an argument of `0075DD70`, which has no direct caller".
