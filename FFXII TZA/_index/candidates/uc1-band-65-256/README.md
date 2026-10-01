# UC-1, the 65–256 B band: per-row evidence with the byte-table test (OPUS, 2026-09-28)

**State: EVIDENCE for a ruling. Nothing here moves the population.** The band is ruled by FABLE and given GO by
FRONTIER, as the 1–64 B band was.

**Why.** FABLE's band ruling (`../uc1-band-ruling-fable-2026-09-25.md` §4) held this band **not yet**. Its "next step"
was a per-row review of the rows that pass every signal, with a byte-table test added before any vote. The body-shape
gate tests code against data, but it cannot see an MSVC switch's byte-index or dword table, which decodes as code.

**Method** ([`uc1_band_65_256.py`](uc1_band_65_256.py)). The 120 `body` rows of 65–256 B are taken from
`unlisted-body-admissions.tsv`.
- **FABLE's signals, reused from her instrument's own definitions:**
  - the gate (`decodes_to_end`);
  - `aligned16` and `referenced`;
  - `multi` (more than one straight-line body);
  - `pred_branch`.
- **The byte-table test (new):**
  - **BT1:** a listed body's memory operand targets the block's *interior*, either rip-relative or as an image-base RVA
    displacement (`[reg + index*scale + rva]`, MSVC's switch-table form).
  - **BT2:** a u32 image-base RVA in one of the 431 classified `table` rows lands in the block, so the block is a
    switch arm of another body.
  - **BT3:** a rip-relative `lea` into the interior, meaning an interior entry or embedded data.
  - **BT4:** a direct `call` / `jmp` / `jcc` into the interior, meaning an alternative entry. Its sources are the listed
    bodies and the unlisted body blocks themselves, i.e. the frontier bodies of both bands.

**Controls.**

| check | result |
|---|---|
| **C1** sensitivity | indexed image-base-RVA operands reach **431 of 431** classified `table` rows |
| **C2** specificity on accepted bodies | the 1–64 B rows with an interior hit are exactly `00253BF5`, `007298DD`, `00809D65` (held ambiguous), `007C2A29` and `007C9BF8` (extend-predecessor). All five are rows FABLE did not admit, and she admitted none of them |
| **C3** extent collision (the `007EE7F0` class) | no clean row overlaps a listed body |

**Result** ([`uc1-band-65-256-rows.tsv`](uc1-band-65-256-rows.tsv), one row per block):

| outcome | rows |
|---|--:|
| clean: gate, one body, no predecessor branch, aligned or referenced, **no byte-table hit** | **100** |
| gate failure | 15. 9 of them carry BT1 hits, so the byte-table test explains them as data or tables (e.g. `0013B5D0`, `00208628`, `003A9350`) |
| `multi` | 2 (`00148BB3`, `001491CE`) |
| unaligned and unreferenced | 3 (`001492FF`, `00158C97`, `003222C2`; the last also BT1) |

The "unaligned and unreferenced" count here is 3 where FABLE's table has 10 (8.3 %). This table counts each row once,
at the first test it fails, and several unaligned rows fail the gate first.

**Alternative entries, checked.** No direct branch and no rip-relative operand from any listed or unlisted body
lands inside a clean block (BT1 / BT3 / BT4). The one alternative-entry class this cannot see is an entry reached
only through a computed pointer: a vtable slot or a stored function pointer into the interior.

**Not checked here, and needed before any vote.**
- **Original-byte extents:** ASTRA's check found the 007EE7C0 truncated store.
- **The blocks' tail padding.**
- **Whether each clean block is one function or a fragment of a listed one** reached only by computed jumps. BT2 covers
  the classified tables only.

**Run receipt.** Run verified at fc97fb934: `uc1_band_65_256.py --write` C1 / C2 / C3 PASS, FAILS 0 (BT4 added in the second publication).
