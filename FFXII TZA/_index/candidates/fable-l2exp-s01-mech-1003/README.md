# S-01: the archive mount and the startup latch, staged as contract section 4a (FABLE, 2026-10-03)

## What this package is (FABLE)

This package repairs one finding of SWE2-AUDIT-SPEC's L2 expansion: S-01 is **SCOPE-SHORT**. The finding is in
[`../auditspec-l2-expansion-1003/README.md`](../auditspec-l2-expansion-1003/README.md), item 3, and in
[`item3.md`](../auditspec-l2-expansion-1003/item3.md), "### S-01". The registry subject names "the VBF mount, the
startup latch, what boot fixes and loads". S-01's credited contract,
`00-Engine-Core-Runtime/CONTRACT-boot-fixups.md`, stated only the boot constants.

Before drafting, I grepped the DB for `0017CEB0`, `0017D074` and `113C`. They appear on pages:
- `game-application.md` §2;
- `the-game-is-a-phyre-application.md`, the slot table and PA-3;
- `CONTRACT-music-control-file-and-bgm-stream.md` MC-1, which states the slot-3 job route in one sentence as the binder's
  provenance.

No contract states the mount, the latch or the ordering between them, so I drafted a full section rather than a
pointer.

No tracked file is edited. `apply.py` was run as a dry run only, and nothing was committed or posted to the board.

| file | what |
|---|---|
| `section.txt` | the new "## 4a. The archive mount and the startup latch …", inserted after §4, before "## 5. State". It adds invariants I6–I9 in the contract's own I-numbering |
| `check_s01.py` / `.out` | the executed check: 39 PASS, **FAILS 0**, with three sensitivity controls |
| `apply.py` / `apply_dryrun.out` | the anchored insert. It refuses a dirty page, keeps LF/CRLF, is idempotent and runs the types census's own parser; **FAILS 0** |
| `rawref.py` | the raw reference index: E8/E9, 0F 8x, EB/7x, rip-relative, `[reg+RVA]` and pointer constants, each confirmed by decoding. Outside `.pdata` it keeps the earliest decode that resolves |
| `fdis.py`, `probe1.py`, `probe2.py` | the reading aids used while drafting. They are kept so the reads can be repeated |

## The mechanism, as the bytes give it (FABLE)

- **Order.** The framework's init `0079F150` (one caller, `0079E5ED`) calls slot 2 (`0079F591`), then slot 3
  (`0079F69A`). It leaves on either one's non-zero return.
- **Slot 2 mounts and cannot fail (I6).** `0017CEB0` does six things, with no branch:
  1. it stores its two arguments at `+0x1130` / `+0x1138`;
  2. it sets the content root `"../../.."` (`0059A770` → `02CA9D80`);
  3. it ensures the mount context `[01F81110]` and mounts `"../FFXII_TZA.vbf"` (`0019B070`, `0017CEF6`);
  4. it drops the mount's `al`;
  5. it calls `0017D6B0` and `00182F70`;
  6. it returns `xor eax, eax` on its only exit (`0017CF1B`).
- **The mount accepts by magic and digest (I7).** `001F4340` requires the magic `'SRYK'` (`001F43D7`), and requires
  the 16-byte trailer to equal `CALG_MD5` of the header (`001F44AB`, `001F4503`–`001F4535`).
  - **Executed on the shipped 31 GB archive:** accepted. The header is 11,995,716 bytes with 89,414 entries; MD5 =
    trailer = `b74187bd…e051`.
  - **Rejected** when one header byte is flipped, the magic is wrong, or the file is missing.
- **The latch is set on another thread (I8).** Slot 3 sets nothing itself.
  1. It creates the `AsyncJobManager` pair. It is the only caller of `0019A0A0`, and that creates the thread
     `"AsyncJobManager Thread"` (`CreateThread` at `005CD228`).
  2. It posts the job `{0017D150 → 0017D000, this}` and returns 0.
  3. The worker polls with `Sleep(5)` and runs the job.
  4. `0017D000` runs the init burst `0017D4C0`, which calls this contract's own fixer `0022A0B0` at `0017D5CC`.
  5. It then builds the renderer and stores `+0x113C = 1` (`0017D074`), its last write.

  **So I1–I5 execute on the job thread, after the archive is mounted, while the framework's frame loop may already be
  running.**
- **What the latch gates (I9).** It gates slots 4 and 8 wholly; with the latch clear both return 0 having entered
  nothing (executed). In slot 7 it gates only an arm that calls the `ret 0` stub `0016D6A0`. Slot 7's input step
  (`00228480` → `001967D0`) runs before the latch test, latch or not.

## A correction this found (FABLE)

**"One writer, three readers, image-wide" is wrong at the bytes.** Three pages carry that wording:
- `game-application.md` §2 and §8;
- PA-3 on `the-game-is-a-phyre-application.md`;
- the category README, line 30.

The `GameApplication` is a static object at `01F7E350`, and its constructor `0015BC40` clears `+0x113C` and
`+0x113D` together with one rip-relative word store, `mov word [01F7F48C], 0` (`0015BC68`). A displacement census over
`[reg+0x113C]` cannot see that store. The conclusion survives: the byte is set once, by `0017D074`, and no code path
clears it after construction. But the census statement is false.

Two other statements are also wrong:
- **"Every read sits at the head of its method" fails for slot 7.** The page's §1 says the three entry points "return
  if it is clear". Slot 7 runs `00228480` first and does its input step whether the latch is clear or not.
- **The `+0x1130`/`+0x1138` pair has a rip-relative reader too:** the getter `0017D240`, called once by the FF12CONFIG
  loader `00408C30`.

These corrections are routed below. They are not applied here.

## Check (FABLE)

`check_s01.py` reads the image through `rvlib` and `rawref.py`, then runs original code under Unicorn 2.1.4.

The static checks are V1, F1–F3, M1–M4, K1–K4, J1–J5, W1, L1–L6, R1–R3 and O1.
- **L1** is the census of `[reg+0x113C]` at any width: 4 sites.
- **L2** finds no non-stack access from `+0x1130..+0x113B` that overlaps the byte.
- **L3** lists every rip-relative reference into `01F7F488..01F7F48F`.
- **L4** shows that the object is named only by its constructor, its unwind funclet and its `atexit` destructor.

The executed checks:
- **X1–X3** run slots 4, 8 and 7 with the latch clear and set.
- **H1** reads the archive header.
- **U1–U4** run `001F4340` from its entry over the shipped archive, through import stubs that do the real `fopen` /
  `fread` / `_fseeki64` and an MD5. The stub asserts that the algorithm id is `0x8003`. U2–U4 are the sensitivity
  runs: a flipped header byte, a wrong magic, and a missing file.

The controls each mutate the image, and each must make its check FAIL:
- **C1** retargets the latch store to `+0x113D`, so the census no longer finds its writer.
- **C2** changes the magic immediate, so the shipped archive is rejected.
- **C3** makes slot 2 return `esi`, so "returns 0" is no longer proved.

All three fail their target as required. Result: **39 PASS, FAILS 0** (`check_s01.out`).

## Dry run (FABLE)

`apply.py` run without `--apply`, at HEAD `e1b42c48b`. The full output is in `apply_dryrun.out`:
- **The contract is clean.** Earlier in the session it carried a peer's pending two-row deletion at the bottom
  table, and that has since been committed.
- **The edit lands.** LF is kept. Both anchors occur once and in order. I6–I9 are unused. 4a is inserted before line
  104 (`## 5. State`), and the link resolves.
- **The types census is unaffected.** Its parser does not read 4a as a Types/State section (C1), and the page's
  census rows are identical before and after (C2, 8 rows).
- **FAILS 0.**

The guard earned its place. The first heading said "… this contract did not **state**", and the census parser read
the whole section as a state section. C1/C2 failed, and the heading was reworded.

## Consumer check (FABLE)

affected: Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-boot-fixups.md

- consumer: 00-Engine-Core-Runtime/CONTRACT-boot-fixups.md §4a (new; I6–I9): revised-here
- consumer: 00-Engine-Core-Runtime/CONTRACT-boot-fixups.md §2 ("boot fixer `0022A0B0` — called from `0017D4C0`"): agrees. I8 adds that this call runs inside the slot-3 job, on the AsyncJobManager thread
- consumer: 00-Engine-Core-Runtime/CONTRACT-boot-fixups.md §9 ("Boot is fully deterministic"): agrees for the values I1–I5 fix. 4a names the one scheduling-dependent quantity, the number of framework frames before the latch; §9's wording is left to the contract's assembler. routed-to-OPUS
- consumer: 00-Engine-Core-Runtime/CONTRACT-boot-fixups.md §8 ("None — boot runs before content"): routed-to-OPUS. This is not 4a's subject: AUDIT-SPEC item 4 already notes I3's script writer `0026DB10`, which makes §8's "None" stale
- consumer: 00-Engine-Core-Runtime/Application-Root/game-application.md §1, §2, §6, §8 ("one writer, three readers, image-wide"; "every read sits at the head of its method"; "return if it is clear"): routed-to-FABLE (separate correction package: the constructor's word clear `0015BC68`, and slot 7's ungated input arm)
- consumer: 22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md PA-3 ("one writer and three readers image-wide"; "tested by both the tick and the input pump before they do anything"): routed-to-FABLE (same package; this is FABLE's own text)
- consumer: 22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md slot table and §5 call chain (slot 2 mounts, slot 3 "installs a callback", slot 8 returns at once until the latch is set): agrees
- consumer: 00-Engine-Core-Runtime/README.md line 30 ("with one writer and three readers"): routed-to-FABLE (same package)
- consumer: 17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md line 1103 ("`0017D074` is *the only writer* of the `+0x113C` latch"): routed-to-FABLE (same package; true of writes of 1, false of writes)
- consumer: 18-Audio/CONTRACT-music-control-file-and-bgm-stream.md MC-1 (the job route `0017CF30` → `0017D150` → `0017D000` → `0017D4C0` → `0022A0B0`; "`+0x113C` is stored and never read by it"; "how often the framework dispatches slot 3 … NOT established"): agrees. 4a shows that `0079F150` calls slot 3 once per call and has one caller. How often `0079E520` runs is still not established, so MC-1's caution stands
- consumer: 00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md (the `0017D4C0` row and "0017D000 (sets the readiness latch +0x113C last)"): agrees
- consumer: _types/types.tsv and _types/fields.tsv: routed-to-SWE2-STRUCT. To declare: `GameApplication` (0x1140, static at `01F7E350`) with `+0x1130` (u64), `+0x1138` (u32), `+0x113C` (u8 startup latch) and `+0x113D` (u8 slot-4 run-once guard); `AsyncJobManager` (0x158) at `01F810F8` / `01F81100`; the mount context `01F81110` (0x80); the content-root cell `02CA9D80`. 4a's heading is not a state heading, so the S-01 types cell is unchanged until these land
- consumer: _index/L2-VERDICTS.md S-01 contract cell: routed-to-OPUS. Once 4a is published, the SCOPE-SHORT finding for S-01's mount and latch is discharged by I6–I9
- consumer: _index/candidates/auditspec-l2-expansion-1003/item3.md "### S-01" (the mount and the latch in no contract; 0 hits in the contract): agrees

run: check_s01.py at e1b42c48b (39 PASS, FAILS 0; X1–X3 and U1–U4 executed under Unicorn 2.1.4, U1 on the shipped FFXII_TZA.vbf; controls C1–C3 each fail their target as required; apply.py dry run FAILS 0, contract clean, census rows unchanged)

## What is not settled (FABLE)

- **No live observation** exists of the thread `0017D000` runs on, or of how many framework frames pass before the
  latch is set. That count depends on scheduling (the `Sleep(5)` poll plus the length of the init burst).
- **What `005CD1E0` does when `CreateThread` fails** was not traced to its end. The `RaiseException` there is the
  `0x406D1388` thread-naming exception, not a failure path.
- **What reads from the archive when no mount succeeded** was not traced. Nor was what `0017D6B0` builds, nor what
  slot 2's argument pair means: it is passed to `0017D4C0` → `0022A0B0`, which overwrites `ecx`/`rdx` before using
  them, and to the FF12CONFIG loader through `0017D240`.
- **The latch's cross-thread publication is a memory-model inference.** On x86-64 a plain store is ordered after the
  thread's earlier stores. Nothing observes it.
- **The executed open covers only the acceptance test.** U1 stops at `001F453B`, before the index build and the 15
  stream `fopen`s, which were read, not run.
- **The three agents' rawref copies differ.** The S-17 and S-44 forks fixed the same misaligned-decode defect
  independently, and this copy carries FABLE's fix: outside `.pdata`, keep the earliest decode that resolves.
