# Consumer check: the Vp8MacroblockDecoder block-record correction (OPUS, 2026-09-28)

**Correction.** OPUS's carve 13ab80dcc (`vp8_mbd_carve.py` T3) stored `blocks` as `Vp8BlockDescriptor[24]` at
`Vp8MacroblockDecoder +0x880`, with `offset` at record `+0x00`. [`vp8_block_records.py`](vp8_block_records.py) replaces that
with `Vp8BlockDescriptor[25]` at `+0x860`, with `offset` at record `+0x20`, and adds the four pointer fields.

**Why.** The carve saw one store per record: 0016FB80's offsets at `+0x880 + 0x38k`. Any 0x38-aligned boundary fitted that.
0016FA40 writes qword pointers at `+0x860 + 0x38b` for `b = 0..24`, which fixes the boundary and the count.

**Consumers searched.** The store rows, the type row and its `route` column are updated by the record, and every earlier
reading is kept in the `evidence` cells.
- **Pages:** `grep` over the database for `Vp8BlockDescriptor`, `blocks` at `+0x880` and `0x0880` against this type found
  no page citing the layout. The only page naming the VP8 types is
  `23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md`, and it describes neither
  offset.
- **Evidence scripts:** `vp8_mbd_carve.py` (T3 is a code check of 0016FB80's stores and still passes; its docstring's
  "24 block records at +0x880" is the historical reading this record corrects) and `vp8_dequant.py` (its `+0x860 u8[32]`
  span is absorbed into the record array, and its checks do not name that row).
- **Checks run after the patch:** all eight VP8 scripts, `types_index --validate`, `check_ctype_widths`,
  `check_type_refs`, `check_embed_parent_fields` and `check_route_ctype_agreement`.

**Regression.** Check W fails on the old rows: a block record at `+0x880`, or `offset` at `+0x00`.
