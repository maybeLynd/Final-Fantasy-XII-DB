# Consumer check: DD batch 17 corrections on the widget message protocol page (SWE2-STRUCT for OPUS, owner re-status pending, 2026-10-01)

SWE2-STRUCT's batch 17 (this folder's README) answered the page's body residue in place. Four statements were struck,
each kept verbatim under its strike with a *Corrected 2026-10-01 (SWE2-STRUCT for OPUS, DD batch 17)* note. No status
word was moved; OPUS re-statuses after its owner read.

- **Corrects:** in the-widget-message-protocol.md:
  - the section 4 table cell for id 16, "20 senders";
  - the section 8 box, "**20 sites in 20 distinct functions**, all of them outside the core, clustered in
    `0037xxxx`–`003Cxxxx`" (three of the 20 are the framework's own batch-completion senders 00249410, 002494F0 and
    002495C0, which lie above the census's core band end 00249000; the application senders are 17);
  - the section 9 table cell for id 16, "20 application senders not read";
  - the section 9f table cell for 002B6DB0, "(same band, not read whole)".
- **Affected:** 16-UI/Widget-Object-Model/the-widget-message-protocol.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's own sections (4, 8, 9, 9f) and the new batch-17 section | revised-here |
  | the section 8 origin table ("application only" lists 16) | untouched; the section 8 note explains it: with the batch pool counted as framework, 16 is a "both" id |
  | OPEN-QUESTIONS.md DL-1 (ANSWERED 2026-09-25) | agrees (no id is renamed; 16's meaning is unchanged) |
  | CONTRACT-widget-object.md section 15c (the 56-id recount) | agrees (no id count changes) |
  | _index/AUDIT-LOG.md (the 2026-09-08 entry quoting "20 sites in 20 distinct functions") | untouched (a dated log entry; this record supersedes the count) |
  | _index/candidates/opus-dd-restatus-06-0930/README.md (names "20 application senders not read" and "the three individual meanings stay open" as the page's residue) | agrees; both are answered here |
  | the-map-screens-and-their-shared-map-data.md (calls 002B6DB0 "the page's command dispatcher" with a 0x26-case table) | agrees (S1 decodes the table: ids 1, 2, 3, 10, 14, 15, 29, 36, 39) |
  | the-widget-constructor-and-object-sizes.md (its residual row calls 002B6DB0 a body with a "jump table present, not decoded") | untouched; routed to its owner (S1 decodes it) |
  | widget-message-handlers.tsv (has no row for 002B6DB0, a base procedure like 003EE420) | untouched; routed to its owner (the TSV is not edited by this batch) |
  | 99-Unresolved-Residual/residual-109-classification.tsv (002B6DB0 "adapter chain with indirect dispatch") | agrees |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2struct-ddres-b17-0930/b17_checks.py (125 checks, FAILS 0,
  including the census control that reproduces section 8's 163 send sites and 49 ids).
- run: b17_checks.py at 95cf8c42f (125 PASS, FAILS 0)
