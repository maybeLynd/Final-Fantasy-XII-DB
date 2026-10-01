# OV-42 (and OV-19's recovery half): the owner protocol has no recovery for a rejected submission (FABLE, Claude Opus 5.5, 2026-09-29)

**Boxes:**
- **OV-42** (`02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md` §"Remaining
  obligations"): "Held-state1 submission and outer service-error/callback-reuse recovery."
- **OV-19**'s recovery half (the owner-lifetime page): "outer recovery after owner state3/5 outlives a queue entry".

[`recovery.py`](recovery.py) runs Q, S, N and I: FAILS 0 ([output](recovery.out)). Static.

**Held state1 is never submitted.** OV-34 ([`ov34-state1-owner-fable`](../ov34-state1-owner-fable/README.md)) shows it: no
dispatcher or transition moves a prepared state-1 owner, and only deletion ends it.

**Outer service-error recovery: none inside the owner protocol.**
- **Q.** The queue requester ~~fails in two ways. A negative, WORD-narrowed file index returns −1, and a failed queue insert
  returns 0.~~ *(Corrected 2026-09-29, FABLE, on reading the insert for OV-45: `ov45-owner-reload-fable/reload.py` Q.)* rejects
  a negative, WORD-narrowed file index (−1). The insert does not fail for a full queue: it waits, running the pump, until
  a slot frees. The zero test after it would need a slot pointer whose low 32 bits are 0, which is not shown impossible
  but is not a queue-full path.
- **S.** The submitter ignores the return and writes owner state 3 anyway.
- **N.** Without a queue entry, the completion callback never runs: its only carrier is the entry. The owner never reaches
  state 4 (ready). Deleting it writes state 5, and state 5 is also resolved only by that callback.
- **I.** The group initialiser zeroes the handle, state and route and calls nothing. So if a group is re-initialised while
  such an owner exists, the record forgets its pinned backing without unpin or free.

**For a reimplementation.** Within the owner protocol, a rejected submission leaves a pinned source that no owner path frees, and
whoever waits on it never sees ready. The page's §5 table already shows the state-3 half ("does not recreate the missing queue
request"). This record adds that no path in the owner code (the submitter, deleters, initialisers or callback) recovers it.

**Not claimed: a game-level leak or hang.** The source is a tagged allocation in arena 11 or 6 (the page's §4). A higher-level
release, such as an arena reset at area change, would free it without the owner code. That is not read here, so this record
does not overturn the page's own caution ("a protocol boundary requiring a higher-level recovery explanation, NOT a proved
permanent game leak or hang"). It narrows the explanation to that level.

**Residue.**
- Whether shipped play ever feeds a negative narrowed index or fills the queue (runtime or data).
- Whether an arena reset or other higher-level release frees an orphaned source (static; the next thing to read).

run: recovery.py at f145d442f, FAILS 0.
