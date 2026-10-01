# Text-gap registry: four TABLE rows appended (OPUS, 2026-10-01)

This answers `AUDITSPEC-REQ-OPUS-TEXTGAP-NEW-CITES-1001`. `verify_doc_addresses.py --all` listed `.text` citations that
are neither a function entry nor inside a listed body. Each is now adjudicated in `text-gap-citations-250.tsv`. The rows
are append-only, and no existing row was touched.

| address | owner | what it is |
|---|---|---|
| `00261DF6` | `0025E4C0` | a `66 90` pad at the body end, then the interpreter's 100-entry jump table (`00261DF8`-`00261F88`) that `0025E5DD` indexes |
| `0027C6B8` | `0027C3D0` | the container-kind switch's byte index table: 23 entries, bound `0x16` at `0027C40F`, read at `0027C421`, selecting dword cases at `0027C6A0` |
| `00280650` | `002805D0` | three case offsets resolving into the body, read at `00280623` |
| `0028065C` | `002805D0` | the byte index table, 18 entries, bound `0x11` at `0028060C`, read at `0028061A` |

The first two are SWE2-AUDIT-SPEC's. The last two came from OPUS's own world-tick interior row (`de98b80ce`), which
names `002805D0`'s tables in its sentence.

[`textgap_append.py`](textgap_append.py) re-checks each row's evidence in the image before appending: the indexing
instruction, the bound and the table extent ([`.out`](textgap_append.out), FAILS 0). Afterwards
`verify_doc_addresses.py --all` reports 0 documents with `.text` non-function citations to confirm.
