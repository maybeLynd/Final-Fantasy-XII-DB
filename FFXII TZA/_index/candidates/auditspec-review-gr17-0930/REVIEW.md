# SWE2-AUDIT-SPEC review of GR-17, the .ard reward-table lifetime and its effect-data residue (OPUS lane SWE2-ORACLE, 3613e9cdb): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). This
resumes a parked draft, whose STATE notes (removed on publication) this record supersedes. Measured at HEAD `48de14c6b`. Evidence is
static: the certified image (sha256 asserted by `ov31_indep.py`) and the shipped file
`D:/FFXII_TZA_extract/ps2data/effect_finish/jp/common/c_all.efx`. Two records were reviewed:
[`gr17-reward-table-lifetime-0930/`](../gr17-reward-table-lifetime-0930/README.md) and
[`gr17-effect-residue-0930/`](../gr17-effect-residue-0930/README.md), both at `3613e9cdb`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-GR17-0930 | `_index/candidates/gr17-reward-table-lifetime-0930/` + `gr17-effect-residue-0930/` | `3613e9cdb` | ACCEPT-WITH-NARROWING |

**Re-run.** Both checkers exit 0 with `FAILS 0`.
- [rerun_gr17_lifetime_check.out](rerun_gr17_lifetime_check.out) is identical to the committed `.out`, ignoring CR.
- [rerun_gr17_effect_residue_check.out](rerun_gr17_effect_residue_check.out) is also identical, apart from the
  reviewer's appended `EXIT 0` line.
- `git status --porcelain` is empty on both package directories.
- The parked draft's [gr17_indep.py](gr17_indep.py) parts A, B, CD and E were re-run, and each reproduces its committed
  `.out` exactly.

**Re-derived independently.** The draft's scripts are [gr17_indep.py](gr17_indep.py),
[gr17_graph2.py](gr17_graph2.py) and [gr17_path2.py](gr17_path2.py). This round added
[gr17_e65.py](gr17_e65.py) / [.out](gr17_e65.out), [gr17_383.py](gr17_383.py) / [.out](gr17_383.out),
[gr17_jccfix.py](gr17_jccfix.py) / [.out](gr17_jccfix.out), [gr17_window.py](gr17_window.py) / [.out](gr17_window.out),
[gr17_efx.py](gr17_efx.py) / [.out](gr17_efx.out), [gr17_ops.py](gr17_ops.py) / [.out](gr17_ops.out) and
[gr17_4ff.py](gr17_4ff.py) / [.out](gr17_4ff.out).

- **Callers, the manager gate, and `+0x774` (parked draft, reproduced).**
  - **Callers.** The E8/E9 callers of the allocation, release, reader and stop chains match S1 and S5–S7. They have no
    jcc callers and no abs64 slots.
  - **Manager gate.** The 47 functions that form a manager-array pointer contain one `+0x28` dword store, `0026C957`.
    No rip-relative store lands on a record's `+0x28`.
  - **`+0x774` displacement.** It appears at 10 sites. The writes are `00236BE6`, `0032A045`, `0070B571` (movss) and
    `007D2959` (a float constant), which matches E1.
  - **Immediates.** The only `0x774` immediate is a shifted decode at `00329F87`, inside `00329F86`'s
    `cmp [rcx+0x774]`.
- **The jcc path `00262AFC` / `00262B12` → `002E65A0` → `00312280` is not real.**
  - Both sites are `call 0x2e65a0`. `002E65A0` is not in the no-jcc reach set.
  - In the draft's jcc graph, the reach runs `002E65A0` → `002E6880` → `002E6EB0`, then an edge `002E70C9 je 0x325260`.
  - That `je` is not in `002E6EB0`, whose `.pdata` range is `002E6EB0-002E7072` and ends at `002E7071 ret`. It belongs
    to the separate no-`.pdata` leaf `002E70C0`: `test rcx,rcx / je / test [rcx+0xd],1 / je 00325260 / ret`.
  - That leaf is named only by two rip leas, `002EA4A3` and `002EA605`. It has no E8/E9 or jcc caller.
  - The draft's instrument attributed the leaf to the nearest preceding call target.
  - With leaf attribution fixed ([gr17_jccfix.out](gr17_jccfix.out)), the jcc edges add only the two address-taken
    leaves `002E7090` and `002E70C0`. `002E6EB0` and `002E65A0` do not reach.
- **The 382-vs-383 count.**
  - The package's own graph (retool CALLS) gives **383 functions including `00312280` itself**, which is 382 excluding
    it.
  - This review's `.pdata`-root graph gives 382, including the target.
  - The two sets differ only in how jump-thunk heads are named. There are 11 names such as `00510830` / `00510840` on
    one side and 10 roots such as `00510810` on the other, and none of the differences is a reach difference.
  - So the Limits sentence "135 of the 383 functions that can reach `00312280`" counts the target among the reachers.
- **The S9 window, including the site kind the package skips.**
  - Recounted over the package's own ranges, the window has 175 direct call/tail sites. The package prints 174. The
    difference is range and extent bookkeeping, not a different reaching set.
  - Only `0025B225` → `00234200` and `0023423F` → `00300140` reach.
  - There are 0 cross-function jcc sites in the window.
  - Image-wide, of 24,348 boundary-aligned rel32 jcc inside `.pdata` code, none targets another function ([gr17_jccctrl.out](gr17_jccctrl.out)). Every
    cross-function jcc (155 kept) sits in a no-`.pdata` leaf.
- **The `.efx` parse, independent of the package's parser.**
  - **Source of the format.** It was derived from the dispatcher `003EDAD0`:
    - chunk = `{u32 len, u16 0x100, u16 type}`, and the handler gets `chunk+0xC`;
    - `003A79C0`: the header is `chunk+0x10`, id `chunk[0xD]`;
    - `003A7B50`: the slot is `(chunk[0xC], chunk[0xD])`, count `chunk[0x13]` (0 → 0x40);
    - `003A77F0`: the track is `(chunk[0xC..0xE])`, and its bytes are moved from `chunk+0x1C`;
    - `0024FE70` runs header byte `0xA+seq` (`0024FF23`);
    - `0046EFD0` runs tracks 1..n-1 with `[5]&1` and `[1]==2` (`0046F092`/`0046F098`);
    - `003B8670` reads count `[0x10]`, entries at `0x14+16k`, time u16 at `+2` (`003B875D`) and opcode byte at `+0`
      (`003B8777`).
  - **The file.** `c_all.efx` on D: has sha256 `0f2f15d9…9029`, the same as the package's pin. It is the only
    `c_all.efx` in the extract, and `01E127B8` → `0096BEA0` names exactly this path.
  - **Walk.** 2,800 chunks, ending at 1,017,904, which is the file end and the `+0xC` size field. No 0x6x0 chunk lies
    off the walk, and no 0x6x0 length breaks the `& ~15` copy.
  - **Counts.** 191 headers, 218 slots and 1,272 tracks. The track kinds are {1: 1074, 2: 40, 3: 158}.
  - **Kind-2 opcodes, over all 40 tracks:** {5: 19, 6: 17, 9: 1, 25: 14, 26: 4, 39: 1, 41: 14}. None of the reaching
    set {3, 17, 24, 31, 34, 40} is present.
  - **The 14 ids.** For each of 104–111 and 142–147, stop sequence 1 is slot 2, whose track 1 fires (6, 41, 25) at time
    0. The start slot is 1 (header byte `+2`), and its one kind-2 track fires (5).
  - This matches E7 exactly.
- **E5 / E6 sample.**
  - **Opcode arms.** Decoded through `003B8787`/`003B8790`, the arms with a reaching direct callee are
    {3, 13, 17, 26, 34, 37, 40, 128}, and the arms with an indirect call are {24, 31}.
  - **Opcode 26.** Its arm `003B89A9`–`003B8A1C` passes event kinds 8, 7, 6 and 3 only.
  - **`00319F50`'s kind arms.** Only arms 0 and 2 reach `0030E360`.
  - **The opcodes `c_all` carries.** Arms 5, 6, 9, 25, 39 and 41 have no reaching callee.
  - **`0046EFD0`'s other launches** (`003A8240`, `003A8020`, `003A8AE0`, `005372D0`, `0046EF10`, `00314960`,
    `001EDDA0`) do not reach.
  - **`004FF2C0`.** It does reach in a plain graph, because its kind-2 arm tail-jumps to `003B8670` (`004FF2FE`). But
    `0046EFD0` calls it only for kind 3 (`0046F129`–`0046F14B`), which it sends to `005372D0` (`004FF2D5`–`004FF2DD`).
    That arm is dead from this call site, so E5 holds as written.

**Controls.**
- **Opcode instrument.** Opcode 3 is the positive control. The same parser finds 347 opcode-3 and 6 opcode-34 entries
  over 3,288 shipped `.efx` files, in 346 files; the first is `ps2data/effect_finish/in/magic/m0179.efx`. Every walk
  ends at its file end.
- **Leaf attribution.** The control for the fix is the misattributed edge itself, which must, and does, land on node
  `002E70C0`.
- **Opcode reach.** Opcode 3's arm must reach, and it does.
- **Reach graph.** `0046EFD0`, `003B8670` and `00319F50` reach.
- **Not covered.** The "0 cross-function jcc inside `.pdata`" count has no in-`.pdata` positive, because none exists.
  The same root comparison does find the 155 leaf-level ones.

**Citations checked.**
- `0024FF23`, `0046F092`, `0046F098`, `0046F0AF`, `003B875D`, `003B8777` and `0023423F` / `002342CE` all say what the
  records state.
- The parent README's point 5 already carries the kind-5 route correction (`0024FE30` → `003B1260` → `0024FE70`) that
  the residue record asked for.

**Runtime routing.** Nothing is routed live. The two `00319F50` early exits are left unsettled by the residue record,
and the verdict does not depend on them.

**Correction wording.** In `gr17-reward-table-lifetime-0930/README.md` Limits, replace "135 of the 383 functions that
can reach `00312280` are address-taken" with:

> 135 of the 382 functions that can reach `00312280` (383 counting `00312280` itself, which is not address-taken) are
> address-taken

Optionally, after "Direct edges only.", add:

> Conditional tail jumps (jcc) were also checked: none leaves a framed function, and the jcc edges from frameless leaves
> add only the address-taken leaves `002E7090` / `002E70C0` (a review finding, `auditspec-review-gr17-0930/gr17_jccfix.out`).

Package-gate notes:
- S9's scan counts only `call` / `jmp`, so a jcc tail would be invisible to it. None exists in the window, but the gate
  would not see one.
- E5 tests `005372D0`, not `004FF2C0`. That is correct only because of the kind-3 argument read above.
