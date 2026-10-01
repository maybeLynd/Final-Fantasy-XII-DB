# S-47: "make a container current" (`0024ED80`) executed as shipped code inside the EFX rebase driver (OPUS, 2026-09-25, block 289)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** This was executed by OPUS on a **copy** of EXP-084's
harness. The published `_experiments/evidence/efx-rebase-execution/check.py` is untouched. This is not an ORACLE EXP.
It is offered to ORACLE for adoption and to SWE2-AUDIT-SEM for scoring.

## What was run

`check_patched.py` (SHA-256 `ecd2c6af…8a5a620c`) is EXP-084's `check.py` plus two things.

**1. Block 265's staged patch** (`../s47-oracle-harness-patch/pending_oracle_s47_24ed80_case.py`):
- a `sec340` fixture key;
- the case `drv-rdx-390-differs-ed80-real`: the driver `003B3480`'s `rdx != 0` path, with `0024ED80` **not** stubbed and
  `q[SEC+0x340] = CTX`.

**2. The real chain of `0024ED80`, loaded from the EXE** (`add_ed80_chain.py`, SHA-asserted image). EXP-084 never loaded
`0024ED80`'s bytes, because it stubbed it with a `ret`. Block 265 called it a "call-free leaf", which **was wrong**: it
ends with `jmp 0024FCF0`.
- The chain is `0024ED80` (0x84 B) → `0024FCF0` (162 B) → `003A2B20` (53 B, a leaf).
- The four data pages they touch are mapped: `02096000`, `022D8000`, `02AEE000`, and `.rdata` `01CEB000`, which holds
  1.0f at `01CEBBA8`.

**Result: 53 / 53, identical over three runs.** That is all 52 EXP-084 cases plus the new one.

## The new case, observed

- **Returned cleanly.** Non-volatile registers were preserved and there was no fault.
- **Visited:** `0024ED80`, `0024FCF0`, `003A2B20` (both its entry and its `ret`) and `0024D940`. **Not visited:** `0024D970`.
- **Write set:**
  - `02F97340` / `02F97348`: context and container (`EfxCurrentContext02F97340`).
  - `02EBEF70` / `78` / `88` / `90` / `98` / `A0` / `A8` / `B0`: the eight published pointers
    (`EfxPublishedPointers02EBEF70`). `+0x10`, the walk's current instance, is not written by this path, as expected.
  - `0024FCF0`'s block `02096800`..`02096843`.
  - `003A2B20`'s stores to `022D8F30` and `022D92E0`..`022D92FF` (the EE/VU0 bank).
  - `02AEE7F4`.
  - `SEC + 0x390`, rebased to `FX + 0x1040`.

This is the static prediction of blocks 244 and 265. The driver's `+0x390`-differs arm runs `0024D940` over the roots
that `0024ED80` has just published.

## What it establishes for S-47

The row's runtime cell is MIXED because EXP-084 stubbed `0024ED80`, which was the one exposure the per-invariant
analysis named (`../s47-runtime-per-invariant-exposure.md`). That body has now executed as shipped code, together with
its whole tail chain, and nothing is scripted on that path. Whether this discharges the row is **AUDIT-SEM's call**.
The row's binding-gap text ("types PARTIAL ... nothing executed") is stale against its own cells: types is MET and
runtime is MIXED.
