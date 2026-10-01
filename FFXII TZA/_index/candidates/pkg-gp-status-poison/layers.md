# PKG-GP-STATUS-POISON Q3: an inflicted Poison is not in the +0x68 layer (FABLE, Claude Opus 5.5, 2026-09-29)

[`layers.py`](layers.py) runs N, C and A: FAILS 0 ([output](layers.out)). Static.

**Not a contradiction: two namespaces share the word "status".**
- **The 32 battle statuses.** Poison is id 8. They live in the status words `+0x64` / `+0x3C`, and only the status write
  writes them (`CONTRACT-status-write.md` §1).
- **The 128-bit `+0x68` / `+0x78` layers** hold effect ids, from the table at `02EBF040`. Attacks reach them through the
  applier's step 14, which passes the result record's effect-id bytes to the layer mutator `0030E130`.

**N: the status write never calls that mutator.** The call at `0030E97F` sits right after the status write's two
fragments, but it belongs to `0030E970`, a separate 25-byte wrapper with its own `.pdata` entry. **C** lists all seven
call sites of the mutator. **A** shows the applier's two sites among them.

**The texts that invited the reading, clarified (not struck: each is right about its own namespace):**

affected: `10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md` (the call chain now says
"inflicts an effect id", and a paragraph states that an inflicted Poison never enters `+0x68`)

affected: `10-Status-Periodic-Terminal/CONTRACT-effect-layers.md` (§3, `+0x68`: "the effect ids spells and attacks inflict
… not the 32 battle statuses")

consumer: the status-write contract's "nothing else in the game sets or clears a status bit" is about the 32 statuses, and it
agrees.

consumer: the tick page's stage 3 reads both layers for the effect-slot timers (`+0x17C`), and it agrees. That is the
effect-id namespace.

run: layers.py at 6fdf6d290, FAILS 0.
