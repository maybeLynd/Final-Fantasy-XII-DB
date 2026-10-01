# Affected-consumer check: the `@FDM` composite key's group part starts at bit 16 (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `fdm_composite_key.py` beside this file (9 checks, FAILS 0). It has three parts:
- a static decode;
- an **executed original-code window**: `005210A6`–`005210BB` run under Unicorn for all 65,536 `w4` values, with a
  `shl 0x0C` mutant that the checks catch;
- the archive key census.

The window proves the arithmetic only. It is not rendering, and it is not authored reachability.

**The defect.** The page's worked example read `0xBCD3` as `(2 << 14) | 0x3CD3`, "group 2, item `0x3CD3`". The
bridge `00521050` builds `((w4 & 0xFFFC) << 14) | w2`, which is `((w4 >> 2) << 16) | w2`.
- Group 2 / item `0x3CD3` is therefore `0x23CD3`.
- `0xBCD3` has no group part; it is `w2` alone.
- The mutant with a shift of 12 is the one that produces `0xBCD3`, and C2e catches it.

Two more statements on the same lines were unsupported:
- "walks 8-byte authored records … for each": `00521050` takes one command-`0x14` record per call;
- "`+0x2F2` is the same axis `@FOR` keys select on": `+0x2F2` is the substitute-record flag, and `00504840` takes the
  `@FOR` key from `u8[modelRec+0x5C]`.

The formula `((w4 & 0xFFFC) << 14) | w2` itself was always right, and so was the census.

| consumer | what it said | state |
|---|---|---|
| `17-Presentation-Rendering/Model-And-Motion-Formats/fdm-and-for-entries.md`, key-table paragraph | "`0xBCD3` decodes as `(2 << 14) \| 0x3CD3` … group 2, item `0x3CD3`" | revised-here (struck; correction block with the bit-16 placement, `0x23CD3`, and the key census) |
| same page, `00521050` bullet | "walks 8-byte authored records … for each"; "`+0x2F2` (a variant/state word — the same axis `@FOR` keys select on)" | revised-here (struck; one command-`0x14` record per call; `+0x2F2` = substitute-record flag per the command-handler page) |
| same page, summary paragraph | "authored names `(group << 14) \| part`"; record source listed as open residue | revised-here (struck; `((w4 >> 2) << 16) \| w2`; record source answered) |
| same page, new "What the shipped data reaches" paragraph | — | added: `w4` ∈ {3, 2} over 7,193 commands, so the key is exactly `w2`. Reachability in play and `w2` ∈ entity table are marked not established |
| same page, frontmatter `audit.note` and Evidence list | "the source of the w2/w4/w6 records" unread | revised-here |
| `17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md`, command `0x14` | "`word+4 & 0xFFFC` is 0 for both authored values, so the packed id reduces to plain `word[cmd+2]`" | agrees (this is the census reused here; not re-run) |
| `17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md` evidence line | cites `00521050` with "see" | agrees (no key arithmetic stated) |
| `_index/OPEN-QUESTIONS.md` UQ-218, the 2026-09-26 SWE2-DATA narrowing | "`((flags&0xFFFC)<<14)\|w2` (or a bare ordinal)" | agrees (the formula is correct; the bare-ordinal arm exists in code and is never authored). The row is PARTIAL on other entries and is not changed |
| `_index/AUDIT-LOG.md` SWE2-DATA-UQ218-FDM-FOR entry; `_inbox/SWE2-DATA.md` | residue "the `w2/w4/w6` record source" | historical receipts; left immutable |

**Independent acceptance.** I co-authored this repair on SWE2-DATA's page, so acceptance is routed to SWE2-DATA, the
page owner.
