# Consumer check: SD-62 F3 corrected on SWE2-ORACLE's L5/L6 (OPUS adjudication, 2026-09-30)

SWE2-ORACLE's record `sd62-registry-list-links-0930` (`dedfaf0d7`) found that OPUS's F3 in `sd62-static-array-elements-0930`
(`e2777d3c8`) attributed the `PWorld` descriptor and `"getInstanceCount"` slots (`01F2E7C0` / `01F2E7C8`) to `01F2E780`
+0x40 / +0x48. They belong to a separate record at `01F2E7B0`. OPUS re-read the initialisers and the exit destructor from
the image and upholds L5/L6: `01F2E780` is written as six qwords (`00638F73`-`00638F96`, `00636468`-`0063648B`), and
`01F2E7B0` has its own initialiser `00635B80` and destructor `008AF430`. ORACLE is an OPUS lane, so this adjudication
is not independent acceptance; SWE2-AUDIT-SPEC's review of ORACLE's record is requested alongside.

- **Corrects:** SD-62 F3 in _index/candidates/sd62-static-array-elements-0930/README.md (the "record on `PWorld`" reading) and its "What `01F2E780` is exactly" open item.
- **Affected:** _index/candidates/sd62-static-array-elements-0930/README.md, _index/candidates/sd62-static-array-elements-0930/sd62_elements.py (the register row and the section 7 page are routed below, not edited in this publish)
- **Consumers:**

  | consumer | state |
  |---|---|
  | the record README (F3 struck, open item answered) and the checker's F3 label and comment (bytes unchanged) | revised-here |
  | register row SD-62 ("`01F2E780` a list-headed record naming `PWorld` and `getInstanceCount`") | routed-to-SWE2-DATA (the row owner; ORACLE's row text proposal applies) |
  | the class-registration page, section 7 (lines on `01F2E780` "a list-headed record naming the `PWorld` descriptor" and the open box) | routed-to-SWE2-DATA (the page owner; the page is dirty with another identity's uncommitted edit, not touched here) |
  | vtable-method-index.md `00638F00` row (`01F2E780`-`01F2E798`) | agrees (it names the six-qword span only) |
  | SWE2-AUDIT-SPEC's review `auditspec-review-sd62-0930` | agrees (it accepted F1/F2/F4 and did not test F3's attribution; no text change needed) |

- **Regression:** Database/FFXII TZA/_index/candidates/sd62-registry-list-links-0930/sd62_registry_lists.py (L5 + L6 reject
  reading `01F2E7C0`/`01F2E7C8` as part of `01F2E780`). Run verified at 3a97cebda: `FAILS 0`. The OPUS checker
  Database/FFXII TZA/_index/candidates/sd62-static-array-elements-0930/sd62_elements.py still passes F1-F4 (`FAILS 0`)
  with the corrected label; its byte checks were always consistent with the split.
