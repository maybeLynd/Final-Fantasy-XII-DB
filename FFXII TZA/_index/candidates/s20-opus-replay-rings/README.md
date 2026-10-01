# S-20: the command seam's two rings (CS-3) executed; their drains are not the same loop (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** CS-3 of `CONTRACT-native-command-seam.md` says the two
64-entry rings are structural twins that carry different transactions, *"the same resolve-then-act drain loop"*, the
action ring *"drained up to eight entries per call"*.

| ring | read / write index | entries | drain |
|---|---|---|---|
| action selection | `022BE980` / `022BE981` | `022BE984 + 8i` (dword handles) | `00313CD0` |
| presentation | `022BEDA0` / `022BEDA1` | `022BEDA4 + 8i` | `00313DB0` |

## What was run

`check.py` is standalone. It maps the whole SHA-asserted image.
- **No application stub, no bridged import.** Every IAT slot is a trap.
- **Allowed set:** both drains' closures, plus `00263E30`.
- **Planted data only:** the rings; the leader gate byte `[02089340]` (clear, so no handle resolves; bit `0x20` for case
  G); and the presentation drain's current-object cell `[02089350]` = 0.

The queued entries do not resolve, so no unit is acted on. What is measured is the drain loops themselves.

**3 / 3 pass, and `result.json` is byte-identical over two runs** (md5 `0756e6aa12232b37d2fa6db22936730d`).

| case | observed |
|---|---|
| `A_action_ring_drains_at_most_eight_per_call` | 10 queued: the read index goes 0 → **8** → 10 → 10 over three calls. 3 queued: 3 drained in one call. The loop is a fixed eight iterations (`00313CF7 mov edi, 8`) |
| `P_presentation_ring_stops_at_the_first_unresolved_entry` | 10 queued: the read index goes 0 → **1** → 2. The drain returns as soon as an entry fails to resolve (`00313E11 je 00313EAC`); only a resolved but unqualified unit sends it round again |
| `G_action_drain_skips_entirely_under_02089340_bit_0x20` | with `[02089340]` bit `0x20` set, nothing is drained (`00313CD4`) |

## What this adds to CS-3 (routed to FABLE, the contract's author)

The two rings are twins in shape, **but their drains are not the same loop.** The action drain pops a fixed eight
entries per call whatever they resolve to. The presentation drain pops until one resolves and qualifies, and **stops at
the first entry that does not resolve**. A port that shares one drain between them would either drain the
presentation ring eight at a time or stall the action ring on an unresolved entry.

CS-4 (the presentation ring's single producer) and CS-6 (the `+0x714` writer census) are census facts. They are put
to AUDIT-SEM as static structure.

## Not covered

- the act half of either drain on a resolving unit;
- a live game.
