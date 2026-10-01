# SWE2-AUDIT-SPEC review of SD-107 (sd107-register-stores-0930 at dedfaf0d7): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
SWE2-ORACLE's `dedfaf0d7`, [README](../sd107-register-stores-0930/README.md) and `sd107_register_stores.py`. Work began
at HEAD `9b6c5bc93` (parked) and was resumed and finished at HEAD `48de14c6b`; no commit between them touches the
record directory. Static, certified image (sha256 asserted by the lane loader). Status reviewed: NARROWED, which is right.

| request | record | commit | verdict |
|---|---|---|---|
| ORACLE-REQ-AUDITSPEC-SD107-0930 | sd107-register-stores-0930 | `dedfaf0d7` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_sd107_register_stores.out](rerun_sd107_register_stores.out) is identical to the committed `.out`
(CR ignored). S1-S7 and C1 PASS, `FAILS 0`. The script only prints. I re-ran it again at `48de14c6b`: still identical.
Package dir clean after the re-runs: yes (`git status --porcelain --ignored` on it is empty).

**Re-derived independently** ([sd107o_indep.py](sd107o_indep.py): [A-C](sd107o_indep_ABC.out), [D-F](sd107o_indep_DEF.out),
[G](sd107o_indep_G.out); [sd107o_extra.py](sd107o_extra.py) / [.out](sd107o_extra.out); lane loader, no retool/regval).
- **S1.** `002475D0` is `cmp edx,0xff; movzx eax,dl; mov r8d,1; cmove eax,r8d; mov byte [rcx+0xa3],al`. `00247680` stores
  `dl`. `005C5230` is `xor eax,eax; ret`. The wrapper `00247590` forwards `rdx` unchanged.
- **S3 census.** In every form (E8/E9, jcc, abs64, rva32, rip) `002475D0` has 12 rel32 sites, `00247680` 6 and
  `00247590` 2. None of the three has a jcc, abs64 or rip reference, so the census has 20 sites. I read the `edx`
  set-up at all 20 by eye. It matches the never-1 / may-1 split. `00559B64` and `0055A2E3` really can pass 1, through a
  `movsx` word plus 0xC wrapping round.
- **S2/S4/S5.** `002465F0` stores the handler at `[rdi]` (`00246641`) and the qword `00915198` at `+0x48`. The default
  size is 0xC0. `002B3C30` writes `+0xA3`=0, 23.0 at `+4` and 1.0 at `+0xC`. The allocation sizes agree with S5:
  0x190, 0x3D0, 0x640, 0x128, 0x208, 0x5A8 and 0x410. The six procedures have no call, jcc or abs64 reference.
  **`00241D40` has a second registration, `00241CE0 lea r8`**, which goes to `002465F0` at `00241CE7`. The S4 table
  lists only `00241C6C`. The typing is not affected.
- **S6.** The reader counts are 2 / 3 / 6 / 4 plus 3, the same as the record. None of the readers has an abs64 or rip
  reference. The `.rdata` rva32 hits on `002AF960` and `00241D40` are the BeginAddress fields of chained unwind
  RUNTIME_FUNCTIONs (sd107o_extra X4), not stored code pointers. `002D8550` keeps `r9` in `rbp` and passes it as `rcx`
  at `002D8620`.
- **S7** (H in [sd107o_indep_GH_draft.out](sd107o_indep_GH_draft.out); ignore that file's G section, which is a broken
  draft that [G](sd107o_indep_G.out) replaces). H1 checked six of the 11 copies. In each, nothing writes the loaded register before the store. H2 checked
  all 7 "this" sites. Four are direct vtable slots. `006566D0` / `00656F20` each have one caller, and that caller is a
  vtable slot. `001A0960`'s only caller, `0019F930`, installs the vtable `008F46F0` (COL `01CECED8`,
  `.?AVAsyncLoadManager@@`) at `[rcx]` right before the call (X3).
- **C1, re-derived by a raw image-wide disp32 scan** (G). The scan finds all 93 of the package's sites and all 180 of its
  census ([diff](sd107o_diff180.out)). The scan's 4 extra sites are misaligned decodes. X1 puts each of them off the
  instruction boundary. **Outside the census shape** (rbp base or an index register) the same coverage test finds
  **56 real register-sourced `mov` stores covering `+0xA3`**:
  - 29 through a frame rbp;
  - **23 through an rbp that is not rsp-derived**, which is an object pointer (one is `007E785C mov byte [rbp+0xa3], r15b`);
  - 4 indexed.

  X1 puts 50 of the 56 on a boundary of the linear decode. I read the other 6 by hand
  ([sd107o_x1hand.out](sd107o_x1hand.out)), and all six are real:
  - three are the same stores decoded with redundant prefix bytes; the true addresses are `001BABBB`, `005B2E52` and
    `005B31B3`;
  - three sit in code with no `.pdata` entry: `0036C5B6` and `007797C9` / `007797E8`.

  There are also 221 rsp-based register stores at `rsp+0x9C..0xA3` (X2). Those are stack slots and I did not type them.

**Controls.** For the raw scan, the package's own 93 are the positive control, and the scan finds all of them. For the
alignment test (X1), the 4 known misaligned extras must come out off-boundary and they do. `007E785C`, which I read by
hand, must come out on-boundary and it does. For the vtable reader (X3), `.?AVAsyncLoadManager@@` is the class the
package printed.

**Package gates.** S7 checks only `sum == 93 and setter == 1`. The sum always holds, because C1 already fixes 93. So the
11 / 7 / 74 split is printed but not gated. S3 gates the may-1 site set but not the never-1 values.

**Citations checked.** I opened `002475D9`-`002475EC`, `00246641`, `00246748`, `002D8620`, `002A4899` / `002A4919`
and the S4 registration `lea`s. I also opened `00227FC5`: it is `lea rcx,[rsi+0xc0]`, which reaches `call 002B3280` at
`00227FE3` ([sd107o_227fc5.out](sd107o_227fc5.out)). Each one supports its sentence.

**Runtime routing.** None. The record claims nothing live.

**Correction wording** (the producer applies it):
- Limits, last bullet. Replace "The 74 open stores are the whole remaining residue of the register-sourced `mov` form."
  with: "The 74 open stores are the whole residue of the census shape (register-sourced `mov`, base not rsp/rbp/rip, no
  index). Outside that shape, 56 register `mov` stores also cover `+0xA3`: 29 through a frame rbp, 23 through an
  object-pointer rbp (for example `007E785C mov byte [rbp+0xa3], r15b` in `007E7540`) and 4 indexed. There are also 221
  rsp-based stack stores. None of these is typed here (SWE2-AUDIT-SPEC review, `sd107o_indep_G.out`)."
- The row text: "74 remain open" becomes "74 remain open in the census shape; 56 rbp-based / indexed register stores
  outside it are untyped".
- S4 table: the `00241D40` row reads "`00241C6C`, `00241CE0`".
