# S-19: the movement body pool executed with no stubbed predicate (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-19's runtime cell says that
`CONTRACT-movement-body-pool`'s invariants *"rest on EXP-087's stubbed guards"*. EXP-087 patched two predicates reached
by consumer 2, `00265680` and `0037C860`, to `ret` with scripted returns. This harness is written from scratch and
runs everything as shipped:
- the creator `002E3500`;
- the allocator and release;
- all five consumers;
- **both predicates**.

## What was run

`check.py` is standalone. It maps the whole SHA-asserted image.
- **No application stub, no stop boundary.** Every IAT slot is a trap.
- **Imports.** Exactly three are bridged by name with their library semantics: `memset`, `cosf` and `sinf`. Any other
  import fails the case.
- **Allowed set.** The static closures of the creator and the five consumers, plus the tail-jump targets the graph
  lacks: `00303EC0` (from `0037C860`), `0030D9A0`, `00377C20` and `002681E0`. That is 35 functions; entering anything
  else fails the case.

**Planted data only:**
- a context, an actor and a param block;
- the real pool array `02B4E4C0` (128 × `0x130`, self index at `+4`, chains through `+0` / `+2`), with its heads
  `02B57CC4` (free) and `02B57CC0` (active);
- the battle state block behind `[02EBF190]` (zeroed), read by `0037C860` → `00303EC0`'s ladder;
- manager slot 0's flags `02098E20`, read by `00265680`.

**5 / 5 pass, and `result.json` is byte-identical over two runs** (md5 `76b75b4b8b107454f31e70e157b7f9fe`).

| case | contract item | observed |
|---|---|---|
| `K1_null_actor_returns_before_allocation` | precondition (`002E3506`–`002E3513`) | with `ctx+0xC0` null the creator returns: no allocation, heads unchanged, no consumer entered, no pool write |
| `K2_fresh_create_attaches_body0_and_runs_all_consumers` | postcondition | 4 free bodies: `+0x138` = body 0, free head 1, active head 0; all five consumers run |
| `K3_one_body_per_record_release_then_re_pop` | invariant: at most one body per record | body 120 already attached and active: create releases it and the allocator re-pops the same body. `+0x138` = body 120, active head 120, free head unchanged |
| `K4_exhausted_null_stored_untested_every_consumer_guards` | postcondition + the central universal | pool exhausted: the allocator's NULL is **stored untested** (`+0x138` = 0). **All five consumers still run.** Consumer 2 is on its predicate arm (`actor+0x152` = 0), **and `00265680` and `0037C860` execute as shipped.** Nothing faults, nothing writes the pool, and nothing writes `actor+0x153` |
| `K5_each_consumer_guards_null_body_and_null_actor` | every consumer guards each hop | each of the five, called alone with the body null and again with the actor null, returns without a fault or a pool write |

## Not covered

- consumer 2's shape-code values on each arm (EXP-087's per-arm cases, now with real predicates available);
- a live game.

## Receipt (re-verified 2026-09-26, OPUS)

Recorded because a truncated sibling draft existed (`s19-opus-replay-body-pool-guards/`, 15 lines, never committed). It
is now moved out of the candidates tree and labelled WIP in `Tools/work/OPUS/drafts/`. This directory is the delivered
candidate, and this is its receipt:

| item | value |
|---|---|
| source | `check.py`, 236 lines, parses; sha256 `0140d2e1a6ac8d20a3d5a354ba3e826f09825a8f6b1a385cde8d09c1b55aa17a` (HEAD blob = worktree) |
| command | `python check.py` in this directory; exit 0 |
| result | 5 / 5 cases PASS; both predicates executed (`pred_00265680`, `pred_0037C860`) |
| result.json as written on Windows (CRLF) | md5 `76b75b4b8b107454f31e70e157b7f9fe` (the md5 above), sha256 `5203628f8ad6bba85b4453d5acac01c04418de285b343f0dbb9ac36f71f8993c` |
| result.json as committed (LF-normalised blob) | md5 `7d0b0cc85d20964c438ff02d5a81fc84`, sha256 `07ebc74cb8d287c8f9ee136f11bde91db1b3dc875971987d30e88f3fbf69334b`. The content is identical: removing CR from the written file gives this md5 |
| reproduction | re-run 2026-09-26 from the committed source, which reproduced md5 `76b75b4b…` byte for byte |

The sealed-receipt check that should bind source and result is `FRONTIER-REQ-ORACLE-EXP201-RECEIPT-SEALING` (SWE2-ORACLE).
It is not yet built. This block does not replace it, and should be re-checked through it once it exists. **Note for that
check:** a receipt hash must name its EOL form, because this repository normalises `result.json` to LF on commit.
