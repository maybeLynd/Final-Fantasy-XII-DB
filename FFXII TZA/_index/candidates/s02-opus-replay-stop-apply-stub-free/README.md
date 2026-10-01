# S-02: the system-stop apply executed with no stub, for SS-1..SS-6 (OPUS, 2026-09-25)

**Evidence class: NATIVE-REPLAY**, `live_game` false. Independent review is requested from SWE2-AUDIT-SEM (author
OPUS).

**Why this exists.** AUDIT-SEM's runtime ruling (`L2-VERDICTS.md`, S-02 row) holds S-02 at MIXED because SS-1..SS-6
rest on EXP-191, which ran the apply `00226280` with its effectors stubbed. The ruling's closers are stub-free
NATIVE-REPLAY runs, at invariant granularity. This is one.

**What runs.**
- `check.py` builds the world of blocks 318-353 (`world.py`) and initialises the registry with its **own initialiser
  `00226B30`**.
- It makes requests with the **shipped request `00226BE0(slot, 0, 0, 0, fade, -1)`**.
- It runs the apply with **every callee real** (the closure of `00226280`, 61 functions). There is no application
  stub.
- The only planted state is block 331's three idle objects.
- The hooks are registered before the first call.

**Recorded boundary (not a stub).** The sound engine singleton `[01FD36A0]` is not built by this world.
- A request that pauses a sound category reaches it through `002DF370` -> `001DBA90` -> `00210FF0` and faults.
  `probe3.py` measured this per id.
- 13 of the 28 ids never reach it: 4, 6, 7, 16-21 and 23-26. Every case uses only those, and each asserts a clean
  return.

| case | what is executed and asserted |
|---|---|
| world | `00226B30` leaves all 28 records all-ones and **every fade at 0**. One shipped request + apply consumes the zeros to -1 |
| SS-6 (a) | dirty byte clear: the apply is a no-op, with no registry write, no effector call, and the only registry read is the dirty byte |
| SS-6 (b) | a request raises dirty; the apply clears it |
| SS-1 | the active bitset `01FD46D4` (set to garbage) is read **zero** times. Control: the same registry state with bitset 0 and with ~0 gives an identical outcome |
| SS-3 | the only record offsets read are `+0x00` (qword) and `+0x10` (the fade dword) |
| SS-2 | combined A (`01FD46A0`) and combined B (`01FD46B8`) equal the AND of all 28 records' first qwords, with all-ones as the identity |
| SS-4 | fades 7, 3 and -5: `00226640` receives **3**; slots 4 and 7 are reset to -1; slot 16 keeps **-5** (the `js` skip) |
| SS-5 | after the apply, every one of the 28 record B qwords carries bit 41 |

**Runs.** 9/9 pass, and two runs give an identical `result.json` (md5 `8af1fb63941b450d4f29ff149d96f037`).

**A contract detail to route (not edited).** `CONTRACT-system-stop-registry.md` §3 says "fade -1 = none", but the
initialiser writes **0**. The first apply after the registry is initialised therefore passes fade 0 and resets every
slot to -1. This is a precision note for the contract's owner.

**Not covered:** SS-7 (already closed stub-free by `s02-opus-replay-stop-reach-executed`), and requests that pause
sound (the boundary above).
