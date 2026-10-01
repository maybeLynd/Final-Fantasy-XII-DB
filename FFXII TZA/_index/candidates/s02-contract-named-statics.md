# S-02 — the contract-named statics, measured for declaration (OPUS, 2026-09-24)

**Why.** S-02's types cell is PARTIAL (SWE2-AUDIT-SEM, 2026-09-22, under the ruled types-MET
criterion) because contract-named scalars and records sit outside `_types/`: the gate's enable word
`01E0C464`, the stop registry's records `01FD4160`/`01FD4400` and `01FD46A0..C8`/`01FD46D0`/`01FD46D4`,
and the tick's deferred pair `01EED060`/`01EED064`. This file is the measurement and the exact rows.
**DECLARED 2026-09-25 (OPUS)** once SWE2-DATA released `fields.tsv` and both files were clean at
HEAD: 5 types, 14 fields, `types_index --validate` 601/7,339/0/0, `check_storage_class` 0 hard
failures, no new data-span collision. `SystemStopRecord` is routed `EMBED SystemStopRegistry +0x0
stride=0x18 count=56 | EMBED SystemStopRegistry +0x540 stride=0x18 count=2` (an absolute `ARRAY`
route was first written and made the checker report the registry colliding with its own records). Evidence class **NATIVE/STATIC**, image `73461D08…21F8`; direction from the
repaired `reg_tracking.op_kind` (0 disagreements vs iced-x86), instrument
`gfz-scripts/s02_statics_refs.py` — every rip-relative reference in every listed body,
211 in the three windows.

## 1. `01E0C464` — the frame update gate's enable word

* **16 references image-wide, every one a `test` inside `0028E290`**; no writer, no `lea`, no other
  reader (agrees with CONTRACT-per-frame-update-gate §15). `.data` initialised: `FF FF FF FF`.
* **Width: 4 bytes, not 2.** Eight sites are `test byte ptr` (masks 0x01..0x80) and eight are
  `test dword ptr` (0x100..0x8000) — e.g. `0028E3FF test dword ptr [01E0C464], 0x1000`. A dword
  test physically reads bytes +2..+3, and MSVC does not emit a dword read of a 2-byte global. The
  contract's §3 argument proves *not uint8*; its table's `uint16` is a representation it does not
  prove. **Declared `uint32`, 15 live bits (0x0010 never tested), bits 16-31 never tested.**
  Routed to the contract owner as a representation note, not edited.
* Neighbours `01E0C444..01E0C484` are separate dword tunables whose addresses `001AF470` takes;
  **`01E0C464` is not among them**. Adjacency is not membership: not folded in.

## 2. `01EED060` / `01EED064` — the tick's deferred pair

* Both `i32`, both `.data`-initialised `0xFFFFFFFF` (the "-1 = none" sentinel is static, WT-4); only
  dword accesses.
* `01EED064` — **12 readers, 4 writers** (tick clear `003140BF`, stagers in `00314530`/`003145E0`,
  reset `00314970`), matching WT-4 under the corrected labels.
* `01EED060` — **2 readers, 3 writers**, and its value is **never used beyond its sign**: the tick
  (`0031407D`..`00314092`) loads it and `cmovns` writes back `-1` whenever it is non-negative; the
  one producer `00314410` (sole caller `0050D0C0`) stores its argument only when the cell is
  negative (first writer wins), after `call 0026A5F0(4)`; `00314970` resets it. MEANING NOT CLAIMED
  beyond that latch behaviour.
* Declared as **two scalars**, not one pair type: they share a reset function and nothing else.

## 3. `01FD4160` — the system-stop registry, one static of 0x578

The registry's own initialiser `00226B30` fixes the shape — its outer loop walks `rdx` from
`01FD46B4` by 0x18 while `< 01FD46E4` (two passes), and its inner loop walks `rax` from
`01FD4160` 28 times per pass **without resetting rax**:

```
+0x000  SystemStopRecord records[56]   01FD4160..01FD46A0  bank A = [0..27], bank B = [28..55]
                                                             (the contract's "record A / record B")
+0x540  SystemStopRecord combined[2]   01FD46A0..01FD46D0  written by the apply as movups+movsd
+0x570  u8   dirty                     01FD46D0  set 1 by 00225CD0/00225EB0/00226BE0, cleared by
                                                  the apply 0022660A and init 00226B30 (SS-6)
+0x571  u8   byte571                   01FD46D1  set 1 by 00227D30; compared/copied by the apply
                                                  (002264BC cmp sil, 002265C1 mov sil); init clears
+0x572  u8[2] unobserved
+0x574  u32  activeRequestBits         01FD46D4  and/or/test by start/stop; init zeroes; the apply
                                                  reads it zero times (SS-1)
```

`SystemStopRecord`, 0x18:

```
+0x00  u64  permissionMask   init all-ones (00226B80); the apply ANDs bank A's into bank B's
                             through the cursor (002262E0 [c-0x10], 002262E4 [c-0x2B0])
+0x08  u64  unobserved08     reached only as the high half of the combined record's 16-byte copy
+0x10  u32  dword10          init -1 (00226B6D, 00226010); the apply reads bank B's and writes -1
                             back (002262EE/00226301) - consumed once per apply
+0x14  u8   byte14           init 0 (00226B87, 00226003/00226008)
+0x15  u8[3] unobserved
```

**Outside the registry**: `01FD46D8`/`01FD46DC` are written only by `00227D40` (`=1`, `=arg`), read
by nothing, and not reset by the registry's init — adjacency, not membership. `01FD4100..01FD4158`
belongs to other code (`0015F590`, `0015FD10`, `001601C0`, `00222xxx`, `008A7xxx`). `01FD46F0+` is
`00228xxx`'s.

## 4. What this does to S-02

If these rows are applied, every scalar and record the S-02 contracts name is inside `_types/`.
That is the enumerable reason the cell gave for PARTIAL; **whether it becomes MET is the auditor's
ruling, not this file's**.
