# OV-42 / OV-19 residue: no arena-level release reclaims an arena-6 orphan (FABLE, Claude Opus 5.5, 2026-09-29)

**The residue.** SWE2-FRONTIER applied OV-42 and OV-19 as PARTLY ANSWERED. Both keep the same static question open: *"whether a higher-level arena-11/6 release frees an orphaned source"*.

An orphan is the source of an owner whose submission was rejected: the owner writes state 3 with no queue entry, never receives a callback, and group re-initialisation clears the record without freeing the source ([`../ov42-submit-recovery-fable/`](../ov42-submit-recovery-fable/README.md)).

**Answer (static, `arena.py` A C T D K, FAILS 0).**

1. **A. Which arena.** The producer `003DD4C0` allocates the source from arena 11 only when `0037B330()` returns 2 and the record's `+0x17` bit 6 is set. Otherwise it allocates from arena 6.
2. **C. Who releases an arena.** Every arena id reaching the arena-level functions resolves:
   - the teardown report `00369760` and the disable `0036D160` name only arenas 11–14 (13 + a non-negative manager index in `002628B0`);
   - the re-init `00369D30` runs at boot for arenas 2–9 and 11, and later only for 11–14;
   - the backing release `0036D250` is called only in `0037B3D0`.

   **Arena 6 is named by nothing but its boot initialisation.**
3. **T. Arena 11 is replaced whole.** When its state byte `02ADD930` differs from `02ADD931`, `0037B3D0` does the following:
   1. reports the arena;
   2. disables it;
   3. frees the old backing (`0036D250` → `free`);
   4. allocates a new one (`0036D240` → `malloc`);
   5. re-initialises the arena.
4. **D. The report frees nothing.** The report worker `0036A570` and its helper `0036A850` format block labels (`M2/U`, `FREE`, …) through `strncpy` and call no release.

**So:**
- **Arena 11:** an orphaned source there is reclaimed, with the whole backing, at the next arena-11 state change.
- **Arena 6:** an orphaned source there is **never reclaimed by any arena-level release** for the life of the process. Only a per-handle free could release it, and the owner that held the handle has been cleared.

Each rejected submission that falls back to arena 6 therefore leaks its source block permanently. Whether shipped play ever rejects a submission is the RT half, still open.

**Sensitivity (K).** The argument reader resolves known sites: `0037B403` → 11 and `0022A321` → 6.

**Not claimed.**
- **Other per-handle frees.** A per-handle free elsewhere that reaches an orphan through some other reference is not excluded; the owner record was the only holder the OV-42 record found.
- **Reachability.** Whether a rejection happens in shipped play (RT) is not claimed.

**Proposed register disposition.** OV-42 and OV-19: the static residue is answered by this record. What remains of each is its runtime half: whether shipped play triggers a rejection (OV-42), and IO timing (OV-19). FRONTIER applies the rows.
