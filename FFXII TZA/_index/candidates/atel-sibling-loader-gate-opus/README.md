# The ATEL sibling loader returns at its first size query (OPUS, 2026-09-28)

affected: _index/candidates/atel-sibling-loader-gate-opus/ (this record only; the pages are routed to their owner)

**Question.** The companions page ([`the-ctrl-module-debug-companions.md`](../../../01-Script-VM-Native-Bridge/ATEL-Control-Modules/the-ctrl-module-debug-companions.md)
§9, "Not claimed") leaves two items open about `003306E0`:
- whether its size queries can reach a kind other than `0xFF` on some other path, since only the `0xFF` call sites were read;
- what `00330E35 cmp esi, 0x10` bounds.

**Discriminator.** Read every `0032E400` call in the whole body, not a sample, and bind control flow from the first
query to the rest of the body.

**Answer.** [`sibling_gate.py`](sibling_gate.py) ([output](sibling_gate.out)), static on the certified image: FAILS 0.

- **Q: every query is kind `0xFF`.** The body has 14 direct `0032E400` call sites, one of them inside a 16-pass loop.
  Each loads `ecx = 0xFF` just before the call. For kind `0xFF`, `0032E400` returns −1 before it reads `rdx`.
- **G: the first query gates everything after it.** It asks the size of the manager's own path (`rbp − 0x50`). Its
  result goes to `r15d` (`00330E58`), and nothing else writes `r15` before `00330F7A test r15d, r15d`. Then
  `00330F7D jle` goes to `003315E7`, the epilogue.
- **E: nothing enters past the gate.**
  - One pdata range covers the body, `003306E0..0033160A`.
  - Inside the body, no jump from before the gate lands after it, and no jump is indirect.
  - No rel32 call, jmp or jcc from outside lands in `00330F7E..003315E7`.
  - The body's one rel32 caller is `00330029`.
- **D: the `.dbg` and `.sbn` names are built, then dropped.** The names at `rbp + 0x720` (`dbg`) and `rbp + 0x830` (`sbn`)
  reach only the queries at `00330E5B` and `00330E6C`. The next query overwrites each result before anything reads it.
- **M: the `0x10` loop names sixteen files.** `esi` runs 0 to 15. Each pass formats `m%02d` (`00D109CC`) into the
  extension and appends `.mld` (`00D109D4`), giving `<stem>.mNN.mld` 0x104 bytes apart from `rbp + 0xD80`. The sixteen
  sizes go to `rsp + 0x60 + 4i`. What the files hold is not claimed.
- **T: the strings after `vld`.** The page asks whether the nine strings after `vld` belong to the same consumer. Eight
  do, and one does not. The body's rip-relative references into `00D10990..00D10A14` run in order:
  - the extensions `bin` to `vld` (16 references, 14 strings), then `m%02d`, `.mld` and its terminator, all before the gate;
  - the six tags `CAMDAT`, `CAMCTL`, `SHKDAT`, `SHKCTL`, `CHRMDL`, `LGTDAT`, all after the gate, each following an
    `atelload.c` allocation tag.

  The ninth, `PREFIX` (`00D10A0C`), is not referenced from this body. Its reference is `0032F67C`, the tag of another
  loader's buffer. That loader's size query `0032F617` is kind 8, index `0x350`: its loop counts `rdi` to 0, then
  `lea ecx, [rdi + 8]`. The data does not mark where the group ends, and neither does the code: the group is simply what
  this body references.
- **C: control.** The same kind reader reads kind `0x20` at another `0032E400` call (`002E61A8`), so Q does not return
  `0xFF` by construction.

**So in this build `003306E0` returns without registering anything.** None of the registration blocks after the gate runs
(`CAMDAT`, `CAMCTL`, `SHKDAT`, `SHKCTL`, `LGTDAT` and the rest), so no stream is bound through this route. This
strengthens the pages' "dead route" statements. It does not reverse them. The container walker (`003304A0`) is a
separate route and is not touched here.

**Not claimed:** whether `00330029` is reached, what the other `0032E400` kinds mean, or how any file behaves on a
build where kind `0xFF` resolves.

| consumer | action | agreement |
|---|---|---|
| `the-ctrl-module-debug-companions.md` §9 "Not claimed" (kinds other than `0xFF`; what `cmp esi, 0x10` bounds) | answered: all 14 sites are `0xFF`, the first gates the body; the loop names 16 `<stem>.mNN.mld` files | routed-to-SWE2-DATA |
| `the-ctrl-module-debug-companions.md` §9 "Where the fourteen end" ("whether the nine strings after `vld` belong to the same consumer") | answered: eight are this body's; `PREFIX` is `0032F67C`'s kind-8 loader tag | routed-to-SWE2-DATA (note on the request) |
| `the-ctrl-module-debug-companions.md` §3 ("every sibling in this route reports no file") | the same result, now with the whole-body gate | agrees |
| `section-009.md` line 148 ("That path is dead in the shipped build") and the key-address row for `0x003306E0` | the path is dead, and so is every other registration in the body | agrees |
| `section-010.md` line 295 and `section-011.md` line 327, key-address rows ("`atelload` registration — pairs tag, callback and mask bit") | the registration never runs in this build; the rows do not say so | routed-to-SWE2-DATA |
| `section-008.md` line 58 and `section-010.md` line 43 (BY-5: "gates each stream on its own lookup") | true of the code after the gate; the whole body sits behind the first query's gate | agrees (a qualifier routed with the above) |

This is OPUS's own check; independent acceptance is requested separately.
