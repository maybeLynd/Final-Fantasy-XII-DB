# NavRunStateBlock: the copy's release, and a window where the global dangles (OPUS, 2026-09-28)

**The question.** The type row for `NavRunStateBlock`, the navigation dataset root held at `02AEDFB0`, left the heap
copy's own release OPEN: "not found on this pass ... a tagged arena reset would free it".

**Check:** [`navrun_lifetime.py`](navrun_lifetime.py) (STATIC, certified image only; A1, B1, R1, R2, C1, P1 and S).

| check | observation |
|---|---|
| A1 | The pack loader copies the nav section into a fresh block and stores it in the pack slot `02ADCFE8` (`00378D4C`). |
| B1 | **Bind.** `00378120` moves the slot into the ACTIVE slot `02ADD008` and publishes it through `00384160` into `02AEDFB0`. |
| R1 | **Release.** `00378230` frees `[02ADD008]` through `003697F0` (`003782BB`), the loader's free for the pack original. It zeroes the slot and calls `00384160(0)`. The release is an explicit free, not an arena reset. |
| R2 | `00384160` ignores a null argument (`test rcx, rcx / je` to its epilogue). **The teardown does not clear `02AEDFB0`: the global keeps the freed address.** |
| C1 | The only clear is `Navigation_ClearDataset` `00383A20`, a qword store of 0, whose callers are `002341C0` and `002368D0` (`BattleStorage_InitializeWorkArrays`). The next bind also overwrites the global. |
| P1 | The readiness predicate `00383C80` compares the pointer with 0 only, so it cannot tell a freed block from a live one. |
| S | Regression: the type row records the release, the window, and the setter qualified as the sole NON-NULL setter. S FAILED on the pre-patch row. |

**Kept apart.**
- **Physical access:** the free is at `003782BB`, and the global is not cleared at `003782C9`.
- **Representation:** the pointer is the block's address, unchanged.
- **Meaning:** no claim is made about what a query would read.

**Not claimed.** Whether any navigation query runs between the release and the clear or next bind. The call order
across `002628B0` / `00378A60` (the teardown's callers) and the reset paths is not established here, and nothing was
observed live. Until that order is settled, a reconstruction must clear or overwrite the global together with the free.

No page changes. The navigation page (`how-a-unit-finds-its-way-across-the-navigation-mesh.md`, line 37) already
says `00383A20` clears the pointer, which agrees.

**Ordering: what the direct-call graph says, bounded.** The graph omits indirect calls, so this is not proof of
absence.
- **The `002628B0` route closes the window.** It frees at `00262CC5` (`00378230`), then calls `002695A0` at
  `00262CEF`. That call reaches the clear unconditionally: `002695A0` has no conditional branch before its call to
  `002341C0`, and `002341C0` calls `00383A20` second. None of the seven calls in between (`002E0670`, `0017E7D0`,
  `003DFA50`, `003EAA00`, `002E06F0`, `003DF5B0`, `00358B40`) reaches a `02AEDFB0` reader within depth 8.
- **The `00378A60` route leaves it open.** After its teardown call (`00378ACF` / `00378AF5`), none of its own later
  calls reaches a reader, a clear or a rebind. The window extends into whatever its callers (`00331990`, `0050D4D0`) do
  next, and that is not traced here.
  - **One level up (2026-09-28, later).** Both callers are wrappers that return right after the teardown:
    - `00331990` (52 B, World/Area/Field) calls `00378A60` twice;
    - `0050D4D0` (31 B, script-VM native bridge) calls it once.

    Neither clears the global or rebinds a dataset. So on this route, statically, the window stays open until whatever
    runs next binds a new dataset. That is a runtime ordering question. A reconstruction should clear `02AEDFB0`
    together with the free.

| consumer | action | agreement |
|---|---|---|
| `_types/types.tsv` NavRunStateBlock, instance and release cells | "sole setter" qualified; release found; dangling window stated; old text struck | revised-here |
| the navigation page, line 37 | `00383A20` clears the pointer | agrees |

**Run receipt.** Run verified at e5106fe3c: `navrun_lifetime.py` FAILS 0; `types_index.py --validate` 0 errors.
