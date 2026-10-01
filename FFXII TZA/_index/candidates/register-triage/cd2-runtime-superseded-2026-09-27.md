# CD-2 closed SUPERSEDED under the runtime rule (FABLE, Claude Opus 5.5, 2026-09-27)

The rule is the one `check_questions.py` states beside `WITHDRAWN`: a row whose answer needs only a live run closes
SUPERSEDED when its claim is already tier-1 static. The status must name where the live remainder is carried.

**CD-2 — "Does anything write `0x01F83530` at runtime?"**

The static claim is tier-1 and complete:
- Two reads name the global, at `0020E602` and `0020E620`, and no relocation reaches it.
- The static object below it ends exactly at it (OPUS, `cd2-opus-base-global-watch/`).
- There is one in-image store route: the texture-id table writer `00210570`, through GiSetTexture with id `0xFFFB`.
  The id producers keep ids below `0x4000`, so that route is undriven.
- A boot-world native replay saw no write, and the value stayed 0.

**Live remainder.** What remains is what the qword holds once authored tables are loaded. It is carried by the board
request `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME` (ASTRA-QUEUE `AQ-ARENA`: one read on any loaded save), which is
BLOCKED on ASTRA's live runs.

That request also carries J-C, which was superseded onto CD-2 earlier the same day.
