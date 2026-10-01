# Consumer check: falsification pass 1 on CONTRACT-actor-storage-record-initialisation (OPUS, 2026-09-29)

corrects: 04-Actor-Entity/CONTRACT-actor-storage-record-initialisation.md (AR-4 and §3: the index is not the first field written)
corrects: 04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md (the same sentence)

## What was corrected

- **The ordering.** `mov word ptr [rbx], r10w`, the index store, is at `002665EB`. Before it the routine:
  - makes six record stores, `and byte [rbx+0x14], 0x7f` first, then `+0xEC`, `+0xF5` and others;
  - calls `00266AD0` and `00266BD0` with the record.

  The record still stores its own index, so AR-4's point about a record knowing where it lives stands. `CON-168`.
- **What survives.** AR-1 (the caller's memset), AR-3 (`+0x03` only read), AR-5 (the extent and the two untouched spans), and
  the sole caller.

## Current consumers

- consumer: [the-record-behind-every-actor.md](../../../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md): revised-here.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-168`).
- consumer: the type store's `ActorStorageRecord.selfIndex` row agrees. It records the field and its writer, not its order.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_actor_storage_init.py`, checks S0-S4. S3 fails unless the index
store follows the `+0x14` mask and the two calls, which rejects "the first field written".

run: verified at abc1a9b94 (BROKEN 0), against the certified image `73461d08…`.
