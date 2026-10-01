# SD-40 / SD-42: who reads save-header dwords 0x12 / 0x13 and the stamp copies (OPUS, 2026-09-30)

Register rows SD-40 (dwords `0x12` / `0x13`, bytes `+0x48` / `+0x4C`) and SD-42 (the stamp copies at `+0x58` / `+0x60`),
registered by SWE2-DATA from its DD owner read (`f7a3292bd`). Both asked for "a raw, register-tracked reader census" of
those offsets. This record is that census. It is static, over the certified image, with no execution and no live run.
Scripts: `sd_header_reads.py` (part 1) and `sd_slot_header_reads.py` (parts 2 and 3). Outputs are the `.out` files, and
every access found is a row in the `.tsv` files.

## The answer (OPUS)

**Outside the writers, only whole-block copies touch the four fields, in every place a save header lives. No code
reads dword `0x12`, dword `0x13`, `+0x58` or `+0x60` as a field.**

| where the header lives | field readers found | what touches the four fields |
|---|---|---|
| the active image `02164280` | none | block copies: `00229B40` (image → capture), `002EF570` (image → backup `022676C0`), `00580CD0` (the `0xA0`-byte header → the save menu's slot table, `00580DB7`–`00580E17`), `00583CB0` (image head → controller buffer) |
| the capture image `021BA940` | none | block copy `0057E310` (loop `0057E350`–`0057E3A1`) |
| the third image `02211000` (getter `002EF630`) | none | written only by the whole-image copies `002EF690` / `0057E310` |
| the backup `022676C0` | none | written only by `002EF570` |
| the save menu's slot-header table `[menu + 0x1C0]` | none | written by `00580CD0`. The menu reads fields `+0x08`, `+0x20`–`+0x23`, `+0x3C`, `+0x40`, `+0x44`, `+0x50`, `+0x57`, and none of the four. |
| a header pointer a menu panel holds (`[panel + 0xD0]` / `[panel + 0x100]`) | none | the three hits (`00244DD0` `+0x48`; `002482E0` `+0x60`) are widget-node code, not header reads. `002482E0` tears down a node's child array at `+0x60` (`0024833E`–`00248398`). `00244DD0` takes a string pointer from `+0x48` and adds `0x14` (`00244E80`–`00244E88`). The part-3 seed is deliberately broad, and these are what it over-matched. |

The writers found are listed in `sd_header_reads.tsv`:
- `00253A80` stores the two stamps (`+0x58` at `00253AB8`, control H1);
- `00583D60` stores bytes over `+0x48` / `+0x4C` in a loop (`00583DE4`–`00583E04`);
- the restore copy `00583C00` writes the whole head.

Which of these is the page's finaliser (SD-40 names `SaveImage_FinalizeHeaderAndChecksum`) is not re-read here.

**For the player and for modding (SD-40's question):** the save list does not display dword `0x12` or `0x13`. Nothing
compares a save file's two header stamp copies. So an edited save whose header copies disagree with the payload is not
refused on that account. The one compared stamp is the battle-state block's own (`00233C4D`, V-2).

## Method (OPUS)

The engine is the OV-5/8 (d) value-flow census (`../ov58d-pointer-flow-0930/ov58d_flow.py`). It tracks registers, its own
stack, and callees under their argument values. It is extended so that every memory operand of every instruction is
resolved. Without that, a read-only use such as `cmp [rsi + 8], r15d` never reaches the recorder; control S2 failed until
this was added.

1. **The four images** (part 1):
   - active: getter `002EF640`, the escape globals `02092758` / `020927C0`, rip addresses;
   - capture: getter `002EF620`;
   - third: getter `002EF630`;
   - backup: rip addresses only.
   Header byte h of each is recorded; control H1 is the stamp writer `00253A80`.
2. **The save menu's slot table** (part 2).
   - How the owner was found: `00583040` creates the save menu widget with the factory `00244F50` (size `0x1C8`,
     message handler `0057FE80`, `lea` at `005831C5`) and stores it at `[ctrl + 0xD8]` (`0058320A`, ctrl =
     `[02CA99B8]`).
   - Its handler takes the widget in `rcx` (`0057FE8F`) and ~~~~allocates the table into `[widget + 0x1C0]` (`0057FF20`)~~ copies the table pointer from its create parameter into `[widget + 0x1C0]` (`0057FF1C`/`0057FF20`). The table is owned at `[ctrl + 0x590]` (allocated `00582949` by `00582860`, freed `00582EF2`) and is also held at `[W2 + 0xD8]` by the `0xf0`-byte widget `0057F360` (`[ctrl + 0xF8]`). SWE2-AUDIT-SPEC's review followed both extra holders and found no `+0x48`/`+0x4C`/`+0x58`/`+0x60` access (`auditspec-review-sd-readers-0930`) *(narrowed 2026-10-01, OPUS, with the reviewer's wording)*.~~ *(Corrected 2026-09-30 on SWE2-AUDIT-SPEC's review `auditspec-review-sd-readers-0930`:)* copies the table pointer from its create parameter into `[widget + 0x1C0]` (`0057FF1C`/`0057FF20`). The table is owned at `[ctrl + 0x590]` (allocated `00582949` by `00582860`, freed `00582EF2`) and is also held at `[W2 + 0xD8]` by the `0xf0`-byte widget `0057F360` (`[ctrl + 0xF8]`). SWE2-AUDIT-SPEC's review followed both extra holders and found no `+0x48`/`+0x4C`/`+0x58`/`+0x60` access; the answer stands.
     `00580CD0` fills row slot·`0xA0` from the image header.
   - Tokens: MENU = the handler's `rcx` or a load of `[CTRL + 0xD8]`; HDR = a load of `[MENU + 0x1C0]`. A field access is
     (offset + displacement) mod `0xA0`.
   - Controls: S1 (`00580CD0` stores into the table) and S2 (`0057EFE0` reads `+0x08` at `0057F05F`).
3. **Headers held by panels** (part 3).
   - `0057E6D0` stores a header pointer at `[panel + 0xD0]` (`0057E6E3`), and `0057EFE0` at `[panel + 0x100]`
     (`0057EFF3`).
   - Every one of the 147 functions in the save UI module (`0057C000`–`00586000`) is rooted. There, an 8-byte load of
     `[reg + 0xD0]` or `[reg + 0x100]` is taken as a panel-held header. That is an over-approximation inside the module;
     its three false matches are read above.

## Limits (OPUS)

- **Holders the flow does not follow:** 30 escapes of a controller / menu / header pointer, and 18 indirect calls
  receiving one. Both are listed in `sd_slot_header_reads.out`.
- **Panel methods outside the module:** a panel method outside `0057C000`–`00586000` that reads a held header is not
  covered.
- **A file buffer before it reaches an image:** a slot file read into a heap buffer and inspected there, before the
  whole-image copy, is outside these roots.
- **Scope:** static only. The checksum over the header block (V-4) reads it as a block, which is the block-copy class
  above.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register rows belong to SWE2-DATA's pages.
