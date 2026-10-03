# Final-audit pass 28: the 64 unruled cross-document claims, ruled (FABLE, 2026-10-03)

`check_doc_claims.py --db "Database/FFXII TZA"` listed **64 unruled claims** (108 claims across 75 documents;
44 already ruled). Each one was read against its target document. **63 are ruled** and their verdicts are
appended to [`../doc-claim-crossrefs.tsv`](../doc-claim-crossrefs.tsv), as 53 rows: several claims share one
`(citing, target, term)` key, and one row covers them all. **1 is WRONG** and is left unruled until it is
fixed (below, and [`stale.tsv`](stale.tsv)).

Static reading only. No page was edited. The registry's header and its earlier rows are unchanged
(the first 102 lines compare byte-identical to the file before the append). One `#` comment line comes
before the new rows and points here.

## Method

1. The citing pages named in the saved output were re-scanned with the checker's own `scan()`. This
   recovered each claim's full sentence and its exact term string. The re-scan reproduced the same 64 unruled
   claims.
2. Each target was read where the citing sentence touches it: the line that holds the fact, the record's
   title (for a record cited by its name), or the publishing commit (for a sha).
3. **Commit shas** cited as attribution were checked with `git log -1` and `git show --stat`. Each one adds
   the linked record. Each named author was compared with the record's title and the commit's lead.

## Counts

| verdict | claims | rows |
|---|---|---|
| LINK-TEXT | 35 | 29 |
| OWN-EVIDENCE | 25 | 21 |
| PARAPHRASE | 2 | 2 |
| EMPTY-TERM | 1 | 1 |
| **ruled** | **63** | **53** |
| WRONG (left unruled) | 1 | - |

What the verdicts cover:

- **LINK-TEXT (35).** In most of these, the term is a record's directory name used as the link label. The
  record's README does not repeat its own directory name. Three are pairing artifacts. In two, a sentence
  carries several record links and the extractor paired the first link's label with a later link's target:
  `ov42-arena-residue-fable/` -> `astra-returns-fable-0930`, and `sd120-binding-ops-0930` -> `sd122-binding-record-fable-0930`.
  The existing ov42 row sets the precedent for these. In the third, the label is a page's filename stem,
  `the-field-runtime-pass`, and the claim it carries holds: the target's §6 lists the `ActorResource_*` family
  at lines 218-222. Where a citing sentence restates the record's answer after a colon, the restatement was
  checked against the record: SD-193, SD-182, GR-9, GR-10, SD-2, GR-12 contradiction 1, SD-7.
- **OWN-EVIDENCE (25).** These fall into four groups:
  - **16 claims: a publish-commit sha used as attribution** (`f41194772` ×2, `35db7fbb2`, `ce2b4380d` ×2,
    `59ec09a95` ×3, `473de1075` ×2, `7573a1b87` ×2, `23a99db40`, `c3570bf4b`, `d526b865b`, `940b5ffcf`,
    `6836e8067`). A file cannot carry the sha of the commit that adds it. Every sha was checked and adds the
    record it is cited with.
  - **The subject of a question box.** `action_data.bin` and `DAT_01e0c2b4`, where the link supports the
    marker note.
  - **The citing page's own read.** The `dword[[02EBF190] + 0x5B04]` address, the `009224A8` correction,
    the `0x1394`-`0x13B3` sweep, the quoted word "understood", and `ACH_EVENT_*` on the achievements page.
  - **A line wrap.** `003BA990` belongs to the next line's link (the manual-save page, line 202). The
    extractor paired it with the storage-read contract, which carries the other four handlers.
- **PARAPHRASE (2).**
  - The clamp page's "they are `.data` addresses, not immediates": CONTRACT-transform-primitives line 382
    reads "`w` is a load, not an immediate", and line 81 reads "which is `.data`, not a constant".
  - `< 0x32`: byte-verdicts.md line 6 (C-V8) reads "cmp esi,0x32 / jge -> +0x0E else +0x0C (50/50)" and
    "cmp esi,0x5F / jge ... (95/5)".
- **EMPTY-TERM (1).** On the widget-tree draw-pass page, the backtick pairing skipped the one-character `` `v` ``.
  It paired the backtick after the `v` with the one before `d1f7f06ac`, so the "term" is a span of the page's
  own prose. It is not a claim about the target. This stretches EMPTY-TERM's definition, which covers an empty
  term; it is the same case of the instrument reporting on itself, and the registry's comment line says so.
  The sha itself is right (OPUS, SD-102).

## WRONG: left unruled for its fix

| citing:line | problem | fix | page lead |
|---|---|---|---|
| `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md:357` -> `sd81-eastl-callers-0930/README.md` (term `audit_crossrefs`) | The line says "SD-81 answered 2026-09-30 **by OPUS** `08f4c0821`". The record is SWE2-ORACLE's: its title is "(SWE2-ORACLE, 2026-09-30)" and line 6 reads "Assigned by OPUS". The commit is SWE2-ORACLE's too: "SWE2-ORACLE: SD-81 - the 99 EASTL rbtree callers typed ...". The same page's line 195 already says "SWE2-ORACLE's SD-81 record, `08f4c0821`". Register row SD-81 (`_index/OPEN-QUESTIONS.md:3597`) has the same "OPUS `08f4c0821`" wording. | Replace "by OPUS `08f4c0821`" with "by SWE2-ORACLE (assigned by OPUS) `08f4c0821`", and make the same change in the register row. The claim still fires after the fix, so then append `(citing, _index/candidates/sd81-eastl-callers-0930/README.md, audit_crossrefs, OWN-EVIDENCE)`. | OPUS (4 of 14 commits; the line was written by FABLE in `6c817c026`, "36 SD register rows brought current ...") |

## Noted, not a defect of any citing page

- The GR-10 record contradicts itself. Line 33 reads "no record 3–7 is active", and line 41 reads "no event
  camera (records 4–7)". The active-party page quotes line 33, "(records 3-7)", so the page matches its
  record. The record's owner, OPUS, should decide whether record 3 counts as an event camera.

## Re-run

`python Database/Tools/analysis-kit/gfz-scripts/check_doc_claims.py --db "Database/FFXII TZA"` was re-run
after the append. Its summary, copied from the output:

```
108 claim(s) across 75 document(s)
   107 carry a VERDICT in _index/candidates/doc-claim-crossrefs.tsv
        LINK-TEXT      44
        OWN-EVIDENCE   44
        PARAPHRASE     12
        RETAINED-SNAPSHOT 4
        EMPTY-TERM     2
        RESOLVER-ARTIFACT 1
   1 have no verdict - these are the ones listed above
```

The run exited 1. The one unruled claim is the WRONG row above, and nothing else is unruled.

Against the earlier run, each verdict grew by exactly the count in the table above:
- LINK-TEXT 9 -> 44 (+35)
- OWN-EVIDENCE 19 -> 44 (+25)
- PARAPHRASE 10 -> 12 (+2)
- EMPTY-TERM 1 -> 2 (+1)

The mutation control did not run. The checker runs it only when no claim is left unruled, so this run
could not exit 2. The control will run on the first pass after the SD-81 fix and its row land.

## The WRONG row, fixed in the same publish

The line was FABLE's own (`6c817c026`), so FABLE corrected it rather than routing it:
[`fable-corr-sd81-attribution-1003`](../fable-corr-sd81-attribution-1003/README.md) changes "OPUS" to "SWE2-ORACLE
(assigned by OPUS)" on the page and in register row SD-81. An attribution census (20 page lines, 47 register cells)
found no other mismatch. The `audit_crossrefs` claim still fires after the edit, so it gets an OWN-EVIDENCE row. With
that row, no claim is left unruled.
