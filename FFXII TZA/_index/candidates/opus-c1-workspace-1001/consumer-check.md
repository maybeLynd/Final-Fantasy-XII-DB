# Consumer check: CharacterRenderRecord +0x0C1 producers and accounting use, and +0x2FC's workspace handle, from three ASTRA packets (OPUS, 2026-10-01)

Consumes ASTRA-REQ-OPUS-RENDER-C1-NIBBLE-PRODUCERS-1001, ASTRA-REQ-OPUS-SKELETON-WORKSPACE-FACTORY-1001 and the
C1-row part of ASTRA-REQ-OPUS-ACCOUNTING-DISPATCH-INDEX-1001. OPUS re-read every cited instruction
(`c1_workspace_check.py`, 21 instructions).

- **Store rows changed:** the type store's fields table only.
  - CharacterRenderRecord `+0x0C1`: both writers store a source byte's upper nibble (0..15). The factory's `movsx`
    read forwards it as the accounting index (`0041F340` → `003AB910` → `0036C5D0`, array `022D8E10`).
  - CharacterRenderRecord `+0x2FC`: the factory stores the encoded kind-1 workspace handle here. Its size relation
    holds only conditionally, and the failed bank-slot path reads address 4.
- **Not done here:** the allocator page's OPUS-CONTRA-ARENA-ACCOUNTING-ARRAY section, which ASTRA's
  accounting-dispatch-index refutes as a range argument. That page carries another lane's uncommitted edits, so it
  waits; the request stays open on the board.
- **Consumers:**

  | consumer | state |
  |---|---|
  | fields.tsv CharacterRenderRecord `+0x0C1` and `+0x2FC` | revised-here |
  | fields.tsv RenderStrideC0Element `+0x094` (the rig inside the workspace, a73cdc0cf) | agrees |
  | the-external-source-owner-and-borrowed-view-lifetime.md (FABLE's ownership and lifetime page) | routed-to-FABLE (a notice: the failed-slot read and the conditional size relation) |
  | the allocator page's OPUS-CONTRA-ARENA-ACCOUNTING-ARRAY range argument | routed-to-OPUS (pending: its page is held dirty by another lane) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-c1-workspace-1001/c1_workspace_check.py, verified at a73cdc0cf: 21 instructions decode as cited, FAILS 0 ([`c1_workspace_check.out`](c1_workspace_check.out)).
