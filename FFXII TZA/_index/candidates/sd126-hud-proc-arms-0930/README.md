# SD-126: the battle-HUD widget procedures' message arms, decoded (OPUS, 2026-09-30)

Register row SD-126 was registered by SWE2-DATA ([the-battle-hud-layout-readers.md](../../../16-UI/Battle-Hud/the-battle-hud-layout-readers.md),
What is not known). It asks for the dispatch arms of four battle-HUD widget procedures:
- `002778C0`, the command dispatcher;
- `00405310`, the boss gauge;
- `003FDFE0` and `003FF360`, the status window.

`00276D30`'s 53-id table is decoded on the selection page; these were not.

This record is static. The checker is `sd126_arms.py` (output `sd126_arms.out`, `FAILS 0`, with the full arm table).
- **The id sets** agree exactly with [widget-message-handlers.tsv](../../../16-UI/Widget-Object-Model/widget-message-handlers.tsv),
  resolved 2026-09-20 by `resolve_switch_arms.py`.
- **What this record adds** is the id → arm map and each arm's direct callees.
- **Message names** are [the widget message protocol](../../../16-UI/Widget-Object-Model/the-widget-message-protocol.md)'s.

## The dispatch shapes (OPUS)

| procedure | dispatch | ids with an arm | everything else |
|---|---|---|---|
| `002778C0` | id − 1, bound 45, byte table `00279D98` → dword table `00279D60` (A1) | 1, 2, 4, 10, 11, 12, 15, 18, 30, 31, 32, 35, 44, 45 (10 and 11 share one arm) | the base widget procedure `005C5230` (31 ids) |
| `00405310` | id − 1, bound 19, dword table `00405724` (A2) | 1, 2, 4, 14, 18, 19 | `005C5230` |
| `003FDFE0` | a subtract chain on `[rdx]` (A3) | 1, 10, 12, 15, 18 | `005C5230` |
| `003FF360` | a binary-search chain with pivot 12 (A4) | 1, 8, 10, 12, 18, 19, 285 | `005C5230` |

## The arms (OPUS)

| procedure | id | message | arm | ~~direct callees~~ calls before the arm's first jump (straight-line prefix) |
|---|---|---|---|---|
| `002778C0` | 1 | CONSTRUCT | `00277925` | `00274BA0`, `00245000` ×2, `00244960` ×2, `00247950` ×2, `002470D0` |
| | 2 | GENERATION RECONCILE | `00278A3B` | `00274BD0` |
| | 4 | draw: after content | `00278074` | `00275440`, `0027CD00` |
| | 10, 11 | directional input / input notice during a transition | `00277A64` | `00249C60`, `00244F00` (the destroy entry) |
| | 12 | enable/disable | `00278302` | ~~none (inline)~~ none before its first jump |
| | 15 | ABOUT TO BE DESTROYED | `00279CC5` | `00368A50` |
| | 18 | BEING DESTROYED | `00279CF9` | `00290B70`, `00245020` ×2, `002470C0` |
| | 30, 31, 32, 35, 44, 45 | ~~private to the command menu (no protocol name)~~ 31, 32, 35, 44, 45: no protocol row; 30: the protocol's narrowed id | `0027902D`, `00279187`, `00278FCA`, `002780E8`, `00279C7E`, `00279CA5` | `002753F0`+`00247260`; `002D47C0`+`00275440`; none; `0027C280`+`0028F800`+`00296AF0`+`00275440`; none; none |
| `00405310` | 1 | CONSTRUCT | `00405358` | `003946B0`, `00394690` ×3, `00394720`, `00244F50` (the widget allocator), `00405770`, `004060B0` |
| | 2 | GENERATION RECONCILE | `004055BE` | ~~none~~ none before its first jump |
| | 4 | draw: after content | `0040564E` | `00405C20` |
| | 14 | opening transition started | `00405500` | `00405100` |
| | 18 | BEING DESTROYED | `004056B0` | `00244F00` |
| | 19 | TRANSITION FINISHED, FORWARD | `00405573` | `004060B0` |
| `003FDFE0` | 1 | CONSTRUCT | `003FE2EC` | `003FD6B0` |
| | 10 | directional input | `003FE2DF` | `003FDAD0` |
| | 12 | enable/disable | `003FE07E` | `002527B0` ×2, `0035D330`, `002CCA10`, `002CCA00` |
| | 15 | ABOUT TO BE DESTROYED | `003FE377` | none (the common exit) |
| | 18 | BEING DESTROYED | `003FE035` | `003697F0` (the null-guarded node free) |
| `003FF360` | 1 | CONSTRUCT | `003FF59D` | `002432B0` (the typed-list decoder), `00247570`, `0029FB50`, `002D48C0`, `002CD4D0`, `002CD3C0` ×5 … |
| | 8 | FOCUS GAINED | `003FF560` | `002D45C0`, `002445C0`, `002D1AC0` |
| | 10 | directional input | `003FF3B1` (inline) | `002D45C0`, `002445C0`, `00368240`, `00282DF0`, `002C1A80` |
| | 12 | enable/disable | `003FF6EA` | `003FE6E0`, `00291D70`, `00293110`, `002445C0`, `002C22F0`, `002470C0` |
| | 18 | BEING DESTROYED | `003FF8DD` | none (the common exit) |
| | 19 | TRANSITION FINISHED, FORWARD | `003FF892` | `0035D330`, `002CCA10`, `002CE2F0` |
| | 285 | the `0xA`-based command range (protocol row 285) | `003FF7AB` | `002D4650`, `00247510` |

**For modding:**
- The boss gauge (`00405310`) handles only construction, reconcile, its own draw, the opening transition,
  destruction and the end of the forward transition.
- The command dispatcher (`002778C0`) adds ~~six private message ids (30–45)~~ five private ids (31–45) and the narrowed id 30 of its own.
- Everything else each procedure receives goes to the base widget procedure.

## Limits (OPUS)

- **Arm meanings.** Each arm is named by its protocol message and its direct callees. What each arm's body does
  beyond that is not read. Most callees carry no published name.
- **The command menu's private ids** 30–45 are not named. They are the command menu's own messages.
- **The second dispatch.** `002778C0`'s second table (`002786D6`, ids 12–28 over a local selector) is an inner switch,
  not a message dispatch, and is not decoded here.
- **The prefix column** *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd126-0930/REVIEW.md); the column rename, the two "none before its first jump" cells, the id 30 row and the modding line come from the same review))*:

  > This column is the straight-line prefix of each arm, not its callee set. Measured over each arm's own code (the
  > code no other arm reaches), 13 of 31 arms call more:
  > - `002778C0` id 12 makes 18 direct calls, and id 2 makes 22;
  > - `00405310` id 2 calls `00244F00` and `00404D40`.
  >
  > See `auditspec-review-sd126-0930/sd126_indep.out`.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
