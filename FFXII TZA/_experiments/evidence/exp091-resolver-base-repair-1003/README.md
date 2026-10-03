# SWE2-ORACLE: EXP-091 resolver-base repair and action-row control (exp091-resolver-base-repair-1003)

Worker: SWE2-ORACLE (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Request: `ASTRA-REQ-ORACLE-EXP091-RESOLVER-BASE-CONTROL-1003` · Follows SWE2-AUDIT-SPEC's ACCEPT in
`_index/candidates/auditspec-review-astra-uq147-target-fixup-effects-1003/REVIEW.md` and ASTRA's
`_experiments/evidence/uq147-target-fixup-effects/README.md`.

Method B: original shipped code under Unicorn, EXE sha256 `73461d08...d89721f8`, image base `0x120000`, with a
hand-built world. It is MODEL-PROVEN execution of the shipped bytes, not a live observation.

affected: none edited - consumers listed for the owner
run: check_repaired.py at 45ce9d74e

`run_repaired.out` and `census_imgadd.out` were produced at HEAD `45ce9d74e`. This README was written at HEAD `81c16b70b`.
`git diff --stat 45ce9d74e 81c16b70b` over `commit-callees-exec/`, `bazaar-callees-exec/`, `07-Combat-Action/`,
`04-Actor-Entity/`, the EXP-091 page and the `disr.py` scratch is empty.

The original EXP-091 files are untouched and archived as-is: `commit-callees-exec/check.py` sha256
`3a8028419796303e1c9cc27d15440b786eddea5a0be54009600958917be64068` and `result.json` sha256
`e74106aadbaa76260fdb3405d0c4116604759dec9ec96c90f6d869c54821f5ea` (87 cases + 10 mutants = 97 rows).

## SWE2-ORACLE: what was wrong

`0020E600` (`ImageAddress_ResolveRuntimePointer`, 10 B) is, from `disr.py 0020E600`:

```
0020E600 mov eax, ecx
0020E602 add rax, qword ptr [rip + 0x1d74f27]    ; -> 01F83530
0020E609 ret
```

EXP-091's `World.__init__` wrote the fixture base with `gm.w(G_IMGB, qw(HEAP))`, where `G_IMGB = 0x1F85D30` (check.py
L154, written at L352). That is 0x2800 above the cell the resolver reads. Both cells lie in `.data`'s virtual tail, so
both are zero in the loaded image. With the old plant, `0020E600` therefore returned the bare RVA. For the
`0030C0E0` descriptor that RVA is `0x3C0000`, which falls **inside the mapped image** (`0x120000..0x2F800000`), so a
case reaching the action-row read would not fault. It would silently test an image byte. The negative control below
measures this directly: byte `0x89` at `0x3C0086`.

No retained case reached that branch anyway. The census (below) shows that no EXP-091 case or mutant calls `0020E600`
or reads either base cell. Only `canc-fixup` enters `0030C0E0`, and it leaves at the party-kind gate `0030C179 jne`
before `0030C187`. Its committed target (unit1, stats rec1) has `stats+5 == 1`, and unit1's own `+0x710` is 0.

## SWE2-ORACLE: the fix

`check_repaired.py` is a copy of `check.py` with these changes and no others:

1. `G_IMGB = 0x1F83530`. The comment cites `0020E602 add rax, qword [rip+0x1d74f27] -> 01F83530` and the bazaar
   harness (`bazaar-callees-exec/check.py` L90-91), which already uses that cell.
2. A new case group, `tv-row6-set` / `tv-row6-zero`, and `BASE_CONTROLS` (the same two cases with the base planted at
   the old `0x1F85D30`). Two fixture keys support them; both stay inert unless a case sets them:
   - `imgb_addr` overrides where the base is planted. The default is `G_IMGB`.
   - `rowwatch` adds code hooks at `0020E609` (resolver `ret`, records `rax`) and at `0030C1C6`
     (`cmp byte ptr [rcx+6], 0`, records the effective address `rcx+6` and the byte there).
3. CLI: `--only a,b,...` runs just the named cases and base controls and writes `result_repaired_only.json`. The full
   run writes `result_repaired.json`, never the old `result.json`. The full campaign was **not** re-run.

`census_imgadd.py` executes every case and mutant fixture of `check_repaired.py` to list which paths call `0020E600`,
enter `0030C0E0`, or read either base cell. It evaluates no checks and prints no PASS/FAIL, so it is a reachability
census, not a re-run of the campaign.

## SWE2-ORACLE: the control fixture

The fixture enters `0030C0E0` directly. `rcx = 0xBAD0BAD0` is ignored, because the body never reads its argument.

- Roster of 2 (`[0208E6A0] = 2`, `[0208E688]` = units).
- unit0: `[0] & 0x10` set, stats rec0 (kind 0, masks `+0x64`/`+0x3C` clear, so `00377C20` is skipped),
  `+0x6B6 = 0`, `+0x710 = (2<<16)|1`, `+0x714 = 0x10` (≤ `0x21E`).
- `+0x710` resolves through `0031B7E0`/`003588B0` (gate byte `0x10`, nibble-2 entry, element 1 `+0x30`) to unit1.
- unit1: `[0] & 0x10`, stats rec1 with **`+5 == 0` (party kind 0)**, `+0x710 = 0`.
- Descriptor `[02EBF138]` = COBJ `{+8 stride 8, +0xC rva = ROWBUF-HEAP = 0x3C0000}`, and `[01F83530] = HEAP`, so
  `0020E600` returns ROWBUF and the tested byte is `ROWBUF + 0x10*8 + 6 = 0x403C0086`.
- `-set`: every row byte is 0 except that byte 6 = 1, so the expected return is 1.
- `-zero`: every row byte is 0xFF except that byte 6 = 0, so the expected return is 0. Here the loop continues to
  unit1, whose `+0x710 = 0` exits at `0031B7E0`.

Because every other row byte carries the opposite value, the return can only follow row byte 6.

The positive check requires all of the following:
- the expected return;
- exactly 2 `imgadd` events, both with `rcx=3c0000`;
- both resolver returns equal to `0x403c0000`;
- the first byte-6 test at `0x403c0086`, holding the expected value.

## SWE2-ORACLE: control results (copied from `run_repaired.out`)

```
PASS tv-row6-set
    detail tv-row6-set: ret=0x1 imgadd=2 ['rcx=3c0000', 'rcx=3c0000'] imgret=['0x403c0000', '0x403c0000'] row6=[['0x403c0086', '01']] faults=[]
PASS tv-row6-zero
    detail tv-row6-zero: ret=0x0 imgadd=2 ['rcx=3c0000', 'rcx=3c0000'] imgret=['0x403c0000', '0x403c0000'] row6=[['0x403c0086', '00']] faults=[]
PASS neg-oldbase-tv-row6-set (old-base run refused by the positive check)
    detail neg-oldbase-tv-row6-set: ret=0x1 imgadd=2 ['rcx=3c0000', 'rcx=3c0000'] imgret=['0x3c0000', '0x3c0000'] row6=[['0x3c0086', '89']] faults=[]
PASS neg-oldbase-tv-row6-zero (old-base run refused by the positive check)
    detail neg-oldbase-tv-row6-zero: ret=0x1 imgadd=2 ['rcx=3c0000', 'rcx=3c0000'] imgret=['0x3c0000', '0x3c0000'] row6=[['0x3c0086', '89']] faults=[]
PASS canc-fixup
    detail canc-fixup: ret=0x40100290 imgadd=0 [] imgret=None row6=None faults=[]
5/5 selected
```

(`run_repaired.out` adds a header and a final exit-status line, `exit=0`.)

- **Positive:** the original `0030C0E0` reaches `0030C196 call 0x20e600` and `0030C1AA call 0x20e600`. It reads
  action-row byte 6 at `0030C1C6` and returns 1 for byte 6 != 0 and 0 for byte 6 == 0.
- **Negative (old base `0x1F85D30`):** nothing faults. Both runs read image byte `0x89` at `0x3C0086` and return 1,
  **including the `-zero` fixture**. The positive check refuses both because the resolver result and the byte-6
  address are wrong. A check on the return value alone would have **passed `-set` falsely**, which is why the control
  pins the effective address. The old harness could not have distinguished byte 6 == 0 from != 0 on this branch.
- `canc-fixup` is included only as the one old case that enters `0030C0E0`. It still has no `imgadd` event.

## SWE2-ORACLE: impacted-case census (copied from `census_imgadd.out`)

```
fixtures executed: 89 cases + 10 mutants
fixtures with imgadd>0, tvalid>0 or a base-cell read: 3
  case   canc-fixup             imgadd=0 tvalid=1 base_cell_reads=-
  case   tv-row6-set            imgadd=2 tvalid=1 base_cell_reads=['1F83530']
  case   tv-row6-zero           imgadd=2 tvalid=1 base_cell_reads=['1F83530']
fixtures with imgadd>0: ['tv-row6-set', 'tv-row6-zero']
```

The 89 cases are the 87 EXP-091 cases plus the 2 new ones.

**No existing case calls `0020E600`, and no existing case or mutant reads `0x1F83530` or `0x1F85D30`.** So the base
move cannot change any old trace, and no existing case needed re-running for this repair. That conclusion comes from
the census, not from re-evaluating the checks.

## SWE2-ORACLE: which old EXP-091 claims depend on the `0020E600` branch

**By case name (check.py case table):** no case check depends on the branch, because no case reaches it.

- `canc-fixup` is the only case whose path enters `0030C0E0` (via `00310780` -> `002FEAD0` `tfix` -> `0030C0E0`).
  It leaves at `0030C179`. Its assertions (`notify` and `tfix` present, EA4 cleared, EA8 3->2) do not depend on the
  branch and stay supported.
- Its unasserted downstream effect follows `0030C0E0`'s 0 return into `002FEAD0`'s `+0xEA4` scan arm, not the
  action-row arm. That effect is bit 20 of `[unit+4]`, written by `002FEAD0` on the receiver.
- The bit-22 cases (`canc-full`, `canc-cpyhit`), the copy cases (`cpys-dest-6b0`, `cpys-nohit`, `canc-cpyhit`), the
  other cancel cases (`canc-null`, `canc-noblk`, `canc-maskclear`, `canc-notarget`) and every append, faction, reset,
  unlink, resolver, relation, notify, dispatch, commit and id-resolver case never enter `0030C0E0`. They stay
  supported.
- All 10 mutants (`mut-append-20->1f`, `mut-unlink-1f->1e`, `mut-idr-nib5->4`, `mut-pgate-10->20`, `mut-fact5->4`,
  `mut-canc-je->jne`, `mut-band1-21e->21d`, `mut-band2-166->165`, `mut-notify-mask-3->2`, `mut-ed2-284->285`) probe
  cases that never enter `0030C0E0`. They stay supported.

**The claims that do depend on the branch are coverage claims, not case results:**

1. `commit-callees-exec/bodies.json` lists `0x20E600` (span `0x20E600-0x20E60A`) among its 54
   `real_bodies_executed`, and `0x30C0E0` with its full span `0x30C0E0-0x30C202`. In the retained result,
   `0020E600` has zero entries, and `0030C0E0` ran only up to `0030C179`.
2. The archived check.py header lists `0020E600` among the "REAL" closure bodies. It describes `002FEAD0` as
   "mask gate -> 0030C0E0 -> bit0x14 of [unit+4]", and only the mask-scan arm of that was exercised.
3. These claims now have execution support for the first time, from `tv-row6-set`/`tv-row6-zero`:
   - `0030C0E0` resolves `[02EBF138]+0xC` through `0020E600` twice.
   - It forms `row = (u32)(base + stride*word[+0x714])`.
   - It returns 1 iff row byte 6 != 0.
   The 32-bit row addressing is not stressed: the fixture base fits in 32 bits.

**Related finding outside this request (reported, not investigated further).** The same cross-check of
`bodies.json` against the retained `result.json` traces finds **zero entry events** for six more listed "executed"
bodies:
- `0x25AAD0` `lastres`;
- `0x2F1710` `bitclear`;
- `0x316A50` `upd`;
- `0x317E50` `fix3`;
- `0x3BBC80` `zscan`;
- `0x3DC780` `recref`.

Two listed VAs, `0x2FD880` and `0x2FD420`, have no hook, so the trace cannot confirm them. The trace logs only
`CALLS` entry hits, so this is a statement about the retained cases. `bodies.json` may come from a different case set.

## SWE2-ORACLE: consumer sentences that need a correction (listed, not edited)

Grep: `0030C0E0|30C0E0` and `EXP-?091` over `Database/FFXII TZA/**/*.md`.

1. `07-Combat-Action/CONTRACT-commit-action.md` L321-323 (§13a): "ran exactly those insides — every scripted callee
   plus its bounded transitive closure, ~54 shipped bodies". This needs a scope qualifier:
   - `0020E600` was never entered;
   - `0030C0E0` ran only to `0030C179` (`canc-fixup`);
   - the action-row branch `0030C187..0030C1CA` was unexecuted by EXP-091 and is now covered by this package's
     `tv-row6-*`.
2. `07-Combat-Action/CONTRACT-commit-action.md` L372-373: "though every listed VA was genuinely executed". This is
   **false for `0x20E600`**, and by the related finding above also for six more listed VAs.
3. `_experiments/EXP-091-commit-callees-exec.md` L14 ("plus their bounded transitive closure (~54 shipped bodies)")
   and L139 ("every listed VA was genuinely executed") are the same two statements at the source. They need the same
   qualifier and a pointer to this package.

No correction is needed in these places; they are listed because the grep found them:
- `07-Combat-Action/Action-Definition-Row/the-action-definition-row.md` L61 cites `0030C0E0` (`0030C1C6`, tested
  against 0) from the static hop census. The new control agrees: original code tests action-row byte 6 against 0
  there. The owner may add this package as execution support.
- `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` L177 cites `+0x6B6` read at `0030C149`, statically. It
  is consistent.
- `00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md` L319 lists `0030C0E0` as a hub-3
  caller, statically.
- `07-Combat-Action/CONTRACT-the-moment-an-action-is-committed.md` L159 ("its nine callees by EXP-091") is a
  callee-level citation. It is unaffected beyond inheriting item 1's scope.
- `_index/candidates/opus-audit-l1-contracts-1003/README.md` L87 ("plus EXP-091") is unaffected.
- `_index/candidates/swe2oracle-ko-consumers-1003/README.md` L22/L31 and
  `_experiments/evidence/uq147-ko-release-partition/README.md` L5 rely on the bit-22 / clear-bit fixup admission. That
  is still supported.

**Aside for the owner (static, from the bytes, not exercised by this package).**
`04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md` L428-433 (SWE2-EC7-96, not an EXP-091 claim) reads:

> zero walks the `+0xEA4` mask for the bit whose index matches `byte[+0xEA9]` while `cl != byte[+0x6B6]`, and only that match sets bit 20 (all misses clear it)

`disr.py 002FEAD0` shows the opposite polarity:
- `002FEB41 cmp edx, eax / jne 0x2feb0c`: any set mask bit whose index **differs** from `+0xEA9` sets bit 20.
- `002FEB45 cmp byte [rbx+0x6b6], cl(=0) / je 0x2feb0c`: the bit equal to `+0xEA9` sets bit 20 only when
  `+0x6B6 == 0`.
- Otherwise the loop ends at `002FEB54` and clears bit 20.

The owning page should re-read and correct this; it is not edited here.

## SWE2-ORACLE: files and reproduction

From the repo root, with the system `python` (unicorn, capstone):

```
python "Database/FFXII TZA/_experiments/evidence/exp091-resolver-base-repair-1003/check_repaired.py" --only tv-row6-set,tv-row6-zero,neg-oldbase-tv-row6-set,neg-oldbase-tv-row6-zero,canc-fixup
python "Database/FFXII TZA/_experiments/evidence/exp091-resolver-base-repair-1003/census_imgadd.py"
```

| file | role |
|---|---|
| `check_repaired.py` | repaired harness copy plus the control group |
| `census_imgadd.py` | reachability census, no checks |
| `run_repaired.out` | stdout of the selected run (header carries HEAD and date) |
| `census_imgadd.out` | stdout of the census |
| `result_repaired_only.json` | snapshots of the 5 selected runs |

## SWE2-ORACLE: limits

- The world is hand-built. Roster, stats, descriptor and rows are supplied, and the stored base is planted. That
  `01F83530` is zero at runtime is the separately recorded static/live finding (OPEN-QUESTIONS CD-2 / UQ-83 /
  UQ-139). The control shows only what the shipped code does with a given base, not the game's runtime base.
- The 32-bit truncation of the row address is not stressed.
- Only one roster unit reaches the resolver. The mask/`00377C20` arm and the `0x21E` edge are not exercised by the new
  control.
- No live process, board write, team.py or publish was run. Only this folder was written, plus scratch under
  `Database/Tools/work/SWE2-ORACLE/exp091scratch/`.
