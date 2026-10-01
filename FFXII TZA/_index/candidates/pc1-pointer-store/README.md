# PC-1: the override dwords have no pointer route in the image (FABLE, Claude Opus 5.5, 2026-09-27)

affected: PC-1; 19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md (the PC-1 box)

**The clause.** PC-1 asks whether `01E02804` / `01E02810` are written through a pointer the page's RIP scan cannot
see. Both are the FF12CONFIG loader's override dwords, `-1` in `.data`. Written, they would enable the loader's
`fieldId` override (`00408D48` `cmovns`) and its second path (`00408DE6`).

**Measured** ([`pc1_pointer_store.py`](pc1_pointer_store.py), [output](pc1_pointer_store.out)). Run verified at 60e631848,
FAILS 0:
- **S1.** Every rip-relative reference is a read in `00408C30`: one to `01E02804` and three to `01E02810`.
- **S2.** No image-base-relative form `[reg + (VA − 0x120000)]` reaches `[01E02800, 01E02820)`. **Control C2:** the
  same detector finds `[reg + 0x29ca030]` twice.
- **S3.** No qword VA, dword VA or dword RVA of either address, or of `01E02800`, occurs anywhere in the file.
  **Control C3:** the function address in vtable `01CB2508`'s slot 0 is found stored.
- **S4.** The only addresses formed in `[01E02780, 01E02820)` are `01E027F0` and `01E027F4`. `001AF470` stores each
  (`001AF5EA`, `001AF606`) into its table of per-variable pointers at `[rcx+0x3be8]` / `[rcx+0x40c0]`. Both are separate
  dwords with their own readers (`00228A82`, `00228BD6`), `0x14` and `0x10` bytes below the targets.

**So no instruction and no data word in the shipped image forms either address.** A write through a pointer would need
an address computed from an unrelated base. The only nearby bases are the two table entries, and they would have to be
indexed past their own dword.

**Limit.** This is static. A table consumer that indexed past an entry is not excluded by reading the entries alone.
ASTRA's live write watch (FABLE-REQ-ASTRA-PC1-OVERRIDE-DWORD-WRITE-WATCH) stays the confirming instrument for an
observed span. PC-1 stays PARTIAL on its other residue: the ten reader-less bytes and the value 3 in `opt02`.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` PC-1 | narrowed: pointer-store clause answered statically; stays PARTIAL | revised-here |
| ff12config-and-debglobal.md PC-1 box | dated note | revised-here |
| the same page, rows 109, 176 and 223 ("no RIP writer") | already true; now extended to image-base-relative forms and stored pointers | agrees |
