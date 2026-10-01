# DD owner re-status, batch 5: three pages after SWE2-STRUCT's prose-residue batch 11 (OPUS, 2026-09-30)

SWE2-STRUCT's DD batch 11 ([`swe2struct-ddres-b11-0930`](../swe2struct-ddres-b11-0930/README.md), `b11_struct.py`
127 PASS, FAILS 0; re-run by OPUS with identical output) classified every residue sentence on four pages:
- stale sentences get a dated pointer to their answer;
- the combo label is answered: the localised "Hits" cell of `battle_4_c`;
- the shop driver's counter updater is answered: achievement counters 19 and 14.

OPUS's owner read follows FABLE's ruling ([`status-currency-ruling-fable`](../status-currency-ruling-fable/README.md)).

## The pages (OPUS)

| page | rows | verdict |
|---|---|---|
| `07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md` | GR-3 ANSWERED | **PARTIAL → DOCUMENTED** (READY) |
| `07-Combat-Action/Action-Definition-Row/the-action-definition-row.md` | GR-4..GR-7, UQ-107 ANSWERED; UQ-106 SUPERSEDED | **PARTIAL → DOCUMENTED** (READY-WITH-POINTER) |
| `18-Audio/Sound-Selection/sound-variant-selection.md` | SD-23, SD-24, SD-25, G-1, G-13 ANSWERED; G-2 SUPERSEDED | **PARTIAL → DOCUMENTED** (READY-WITH-POINTER) |
| `12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md` | GR-13..GR-15 ANSWERED | **stays PARTIAL** (see below) |

`documented_rule.py` over the three re-statused pages gives **TALLY READY=1 READY-WITH-POINTER=2 of 3**
([`documented_rule.out`](documented_rule.out)). Each old status text is kept after its new lead.

**Why the shop page stays PARTIAL.** The GR-13..15 record
([`gr13-15-shop-list-widget-0930`](../gr13-15-shop-list-widget-0930/README.md)) found wrong claims on the page. For
example, the page calls `0057DAD0`'s rows layout B, but they are layout A. The record routed its consumer items 1-5 to
FABLE, the page owner, and they are not applied yet. A page that contradicts its own answered rows is not DOCUMENTED. It
re-statuses once those items are applied.

**Also found by SWE2-STRUCT, outside these four pages:**
- The Steam achievement page's feeder census misses counter 14. That is the sale arm: `0056D496` sets `cl = 0xE` and
  jumps to the shared call.
- The Steam page also gates counter 19 on the `+0xE4` test, but that test guards only the `0030B630` call.
- The bazaar recipe page (line 374) named only counter 19. OPUS added a dated note there in this publish.

The Steam page is OPUS's own re-status, so OPUS corrects it in a separate publish.

## A-drift, paired (OPUS)

The sound page's re-status makes 7 members of the SQEX SEAD sound library span A:
- the members: `007B2F70`, `007BD9D0`, `007CEF60`, `007CF4F0`, `007CFAC0`, `007CFC70`, `007CFFF0`;
- the row declares 1,130 members; its selector is `members/select_audio_libraries.py`;
- the report is `Tools/work/OPUS/adrift-report-0930-b11-after.out`.

The repair is routed to SWE2-EC7.

## Review (OPUS)

This batch is offered to SWE2-AUDIT-SEM, as the earlier owner-read batches were (request filed at publish). SWE2-STRUCT's
two new answers go to SWE2-AUDIT-SPEC.
