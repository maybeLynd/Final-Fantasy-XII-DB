# AppBootStatic01F7F490: census rows re-cut to what the code accesses (OPUS, 2026-10-03)

*repos-91, a local helper, surveyed the 1,441 "MEANING NOT CLAIMED" rows in `fields.tsv` against census2's
contract-named fields. In NOT MET systems only six placeholder fields are contract-named, and four of them are on this
static (S-37, S-43, S-39 and S-38).

Applied by [`apply_recuts.py`](apply_recuts.py) from [`recuts.json`](recuts.json): 20 rows out and 19 in. OPUS's
census declared these rows on 2026-09-22. OPUS checked that every one of the 191 code addresses cited in the new rows
is an instruction start, and re-read the size and byte-use anchors. The full research is in
[`appboot_research.json`](appboot_research.json) and [`research.json`](research.json).*

## The base: SWE2-STRUCT's ruling, then this re-cut (OPUS)

This record was first drafted against `AppBootStatic01F7F480`. Its first 0x10 bytes are GameApplication's tail: the
single GameApplication instance at `01F7E350` is 0x1140 bytes. The slot-0 destructor frees 0x1140 at `0017CCB0`, and
the methods use `[this+0x113C]` (`0017D074`) and `[this+0x113D]` (`0017CD1E`).

Moving a type boundary is the type store owner's call, so OPUS routed it (OPUS-REQ-STRUCT-GAMEAPPLICATION-TAIL-1003).
SWE2-STRUCT ruled in `81a9fa56d`: GameApplication is declared at 0x1140, and the boot static is re-based to
`AppBootStatic01F7F490`. This record was then re-based onto that store, so every offset below is 0x10 lower than in
the first draft. It applied after STRUCT's commit, from a clean store.

## Applied (OPUS)

- **`+0x80 platformLock` u8[40]** replaces byte0090 and unobservedSpan0091. It is an embedded 0x28 recursive lock:
  ctor `005CC8A0` (the event is created on first use), lock `005CD380`, unlock `005CD7D0`. Five `lea` instructions
  pass the whole object.
- **Ctype fixes:**
  - `+0x20 frameDelta` becomes double, because every access is `movsd`: it is the per-frame pump's delta (`0017D6E0`).
  - `+0xAC` becomes float (`movss`): the console pair swaps it with `02CB8138`.
- **Contract-named meanings:**
  - `+0x30 ringAllocator` (S-37);
  - `+0x100 blockBankIndex`, which takes (i+1) AND 3 (S-43);
  - `+0x104 aoRanLatch` (S-39, I-7);
  - `+0x108 perFrameSingletonCell`, BootSingleton01F7F598's cell, set up by Ensure `00189000` (S-38).
- **Named from their writers and readers:**
  - `+0x28 frameResetFlag`;
  - `+0x50 debugScopeObject`;
  - `+0x58 queryDefault58`;
  - `+0x59 speedKeyEdgeLatch`;
  - the `+0x60`/`+0x64`/`+0x68`/`+0x70` gate set that `0017F6B0` tests;
  - `+0x6C readyFlag6C`;
  - `+0xA8 pokeStatusA8` and `+0xB0 pokeGate70Once`;
  - `+0x110 renderPassCounter`.

  Where a writer alone states what a field holds, the row says so and claims no more.

The row-loss guard (`check_record_rows_present.py`) reads the 20 retired census rows as this record's declared
replacement. It reports 0 missing.
