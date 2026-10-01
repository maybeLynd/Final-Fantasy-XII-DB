# Consumer check: falsification passes on three REOPENED pages (SWE2-STRUCT for OPUS, 2026-10-01)

The 2026-10-01 falsification passes (this folder's README) corrected claims on the three pages and struck the old
text in place.

- **Corrects:**
  - in vbf-archive-and-st2e-tables.md: the lede's "`action_data.bin` is the file behind the action definition table"; section 3's "This is very probably the file that fills it"; section 2's struct comments "32" (headerSize), "headerSize + count*recordSize, or 0 when the table carries no heap" (heapOffset) and "0 in all 407 shipped files" (reservedB, reservedC); and section 8's directory row "2, 8: the 40-entry battle manifest";
  - in the-file-schema-against-the-runtime-schema.md: section 1's "When those two disagree, an asset does not load.";
  - in third-party-middleware-inventory.md: the lede's "totalling 801 tagged functions"; section 2's "the true total to 802" (twice), the bare-name rows "EASTL 72" and "Subtotal 111", and the corrected-totals rows "EASTL 72" and "Total 111 / 802"; section 5's call-chain entries "libxml2" and "linked; not proven to encode the save container"; section 7's CF-2 conclusions "libvorbis is linked and reached by nothing" and "libvorbis is dead weight carried by the link"; and section 8's evidence row "Twelve libraries, 801 functions".
- **Affected:** 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md, 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md, 23-Third-Party-Libraries/third-party-middleware-inventory.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the three pages' own sections; each page's new section "Falsification pass 2026-10-01 (SWE2-STRUCT for OPUS)" | revised-here |
  | vbf page, *Open questions* AY-3 / AY-11 box (FABLE 2026-09-15: `+0x18` / `+0x1C` non-zero in 4 + 4) | agrees: the struct correction carries this box's correction up to section 2 |
  | CONTRACT-authored-table-row-lookup.md section 7 (the registrar rebases `+0x0C`, `+0x10`, `+0x18`, `+0x1C`) | agrees |
  | vbf page front matter, `archive_formats` st2e row ("headerSize 32, 0, heapOffset, 0, 0") | stale; routed to OPUS (front matter), replacement text in the README |
  | 02-Resource-And-Asset-Pipeline/README.md line 28 ("`action_data.bin` is the file behind registry slot `0x02EBF138`") | stale; routed to the category owner |
  | CONTRACT-authored-table-row-lookup.md (slot `02EBF138` written by `00237FC0`) | agrees |
  | 07-Combat-Action/Action-Definition-Row/the-action-definition-row.md (rows read from `battle_pack.bin` directory `+0x3C`) | agrees on the binding; its line 135 "`action_data.bin` per language" is stale against section 12's four-language census, routed to its owner |
  | register row AY-7 ("at slots 2 and 8 the 40-entry battle manifest") | stale; routed to OPUS (register) |
  | authored-data-table-registry.md (named by pass 7 as a possible inheritor of the 40-entry extent) | agrees: it cites no 40-table extent |
  | the-cluster-header-and-what-the-loader-rejects.md (what the loader refuses) | agrees; now linked from section 1 of the schema page |
  | schema page front matter, `archive_formats` phyre row ("with 22 classes still unresolved") | stale; routed to OPUS (front matter), replacement text in the README |
  | 23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md line 430 ("twelve libraries, 801 functions") | stale; routed to its owner |
  | _index/COVERAGE.md line 159 ("12 libraries, 801 functions") | stale; routed to OPUS |
  | embedded-lua-and-phyre-object-bindings.md and where-the-games-memory-comes-from.md ("Lua … 111 functions") | agree: Lua's 111 re-measures (N2, N3) |
  | register row CF-2 ("libvorbis … linked, unreached") | stale against register row G-23 (2026-09-16); routed to OPUS (register) |
  | 18-Audio/sead-engine-identity-and-diagnostics.md and the inventory's own libvorbis family row (FABLE-CONTRA-LIBVORBIS-IS-REACHED-BY-THE-MOVIE-PLAYER) | agree |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2struct-reopened3-0930/p1_vbf_st2e.py (34 checks),
  Database/FFXII TZA/_index/candidates/swe2struct-reopened3-0930/p2_route4.py (14 checks),
  Database/FFXII TZA/_index/candidates/swe2struct-reopened3-0930/p3_inventory.py (10 checks).
  run: p1_vbf_st2e.py at b0524530f (FAILS 0); run: p2_route4.py at b0524530f (FAILS 0); run: p3_inventory.py at b0524530f (FAILS 0)
