# Three-agent inbox — evidence and handoff rules

**Current authority: [TEAM.md](TEAM.md) and [TEAM.json](TEAM.json).** Exactly FABLE, OPUS, ASTRA.
The old six-helper/coordinator model is retired; old inboxes and [assignments](ASSIGNMENTS.md)
remain historical evidence. Cross-account messaging failed in the earlier workflow, so durable
file-based claims and returns remain the handoff authority.

## Rules for all three agents

1. **GZF mutation remains serialized and gated.** Any of the three may temporarily claim
   publication and the affected outputs per TEAM.md; all other analysis stays read-only.
   Stage candidate manifest rows in your inbox until the unchanged mutation fence can be run.
2. **Your own Ghidra project and outputs.** Use an agent-specific absolute ProjectDir, a unique
   ProjectName and explicit OutDir. Never touch another agent's project.
3. **The person who read the function writes the document.** Category determines where it goes,
   not who may write it. Claim the semantic scope and files first. Scratch stays in
   Tools/work/ID/. On overlap, split the work explicitly or stage a handoff; never strand a read
   merely because another specialty usually owns that category.

3b. **Re-run the coverage checks AFTER writing, not only before.**
   `check_located_not_read.py` and `check_source_hygiene.py` before a block tell you what you are
   walking into; the same two after it tell you **what you left behind**. They are different checks.

   *Added 2026-09-03.* A session produced the exact false positive it had characterised two blocks
   earlier — a function read in full, cited only at its entry — **in the document about it**, and
   caught it only because it re-ran the check after writing. **Cite an interior address for every claim you
   make about a function you read** — not one per function. **And cite an address for every function
   your document's claims rest on, even when you name it** — `check_named_not_cited.py` finds the ones
   you did not. A *passing reference* to another document's function needs no anchor; **a function your
   own argument depends on does.**

   *Added 2026-09-03 after the pair census reported an offset as uncompared when a document had
   compared both its touchers at length — in pseudocode, by name, with no address inside either.*
   **426 named-but-uncited mentions exist across 82 documents.** An instruction anchor is what
   distinguishes a read from a mention for every instrument this project has, but *"at least one"*
   only clears the instrument; **it does not make the document checkable.** A prologue constant, a
   stride, a loop bound and a state write are four different claims and each needs its own.

3c. **If you explain an authored-data registry slot, declare it in frontmatter.** The scored
   dimension `registry_explained` (63 slots, `0x02EBF008`–`0x02EBF1F8`) counts **declarations**,
   not mentions:

   ```yaml
   registry_slots:
     - "0x02EBF0C0"
   ```

   **One owner per slot.** `check_formats.py` reports a slot claimed by two documents as a
   collision, under the same rule that forbids describing an address two ways. Declare it only
   where your document establishes **what the slot holds** — `0x02EBF138` is mentioned in ten
   documents and explained in one, which is exactly why the numerator is declared rather than
   scraped from prose.

   **Do not declare a slot on a count match.** The `st2e` document showed `action_data.bin` with
   543 records against the registry's 543 ids and **downgraded that binding to a lead** (open
   question `AY-6`) on its own falsification pass. *A count match is suggestive, not deciding.*

   For a container format — a save image, an archive, a config file — use `container_format: <name>`
   instead. Those are **counted and not scored**: no censused universe of container formats exists,
   so a percentage would be invented.

   The optional section shape for either is `## 4b. The loader contract` in
   [`_templates/SYSTEM.md`](../../_templates/SYSTEM.md). **Section 4 says what the bytes are; 4b
   says what the code does with them** — including which fields nothing reads, which is the column
   a modder actually needs and the one a file-corpus reading cannot produce.

4. **Claim shared manual files before editing and serialize publication per TEAM.md.**
   Otherwise append a return to `_index/_inbox/FABLE.md`, `OPUS.md` or `ASTRA.md` under the
   headings below. Any of the three may integrate it under a publication claim; annotate the
   consumed section with its destination and commit, rather than deleting its evidence.

```markdown
## COVERAGE
## OPEN-QUESTIONS      (new IDs as PROPOSED-<session>-n; closures name the existing ID)
## AUDIT-LOG
## CALL-CHAINS / ADDRESS-INDEX
```

**Never pick a question-id prefix by eye.** Two collisions happened on 2026-09-02 — six sections
opened on prefixes that were free as *section headers* but already in use as *row ids* inside other
sections (23 duplicate ids), and then two sessions independently claiming `BL` in the same hour. Ask
the tool:

```powershell
python Database\Tools\analysis-kit\gfz-scripts\next_question_id.py --db "Database\FFXII TZA" --list
python Database\Tools\analysis-kit\gfz-scripts\next_question_id.py --db "Database\FFXII TZA" --check BS
```

`--check` exits non-zero if the prefix is taken, so it can gate a merge. It refuses to answer at all
if its row parse finds no two-letter ids, because a "free" answer from a parser that saw nothing is
worthless. **Propose IDs as `PROPOSED-<AGENT>-<TASK>-n`** (including the task avoids the recorded
cross-round collision). The publication owner assigns the real prefix under the OPEN-QUESTIONS
file claim, immediately re-checking the tool at merge time.

5. **Report in the board and your durable inbox** when a package lands or blocks. State what
   native behaviour was learned. Requests in TEAM.json name their recipient; messaging is optional.
6. The mission, evidence hierarchy, banned-evidence list and writing standard bind all three.
   `.pdata` / `.xdata` / unwind / EH maps are **never** semantic evidence.

## The gates are not atomic against concurrent edits

With several sessions writing at once, `check_consistency.py` and the other gates read files that may
be mid-write. On 2026-09-03 a `NAME` disagreement appeared on one run and was gone on the next; a
session had been writing the second document while the first was scanned.

**A single red gate result is not evidence until it is re-run.** Re-run before acting, and never
"correct" a document to satisfy a gate you have seen red only once — that is the token-satisfaction
failure in a new costume, and it damages a document that was already right.

## A status field must record what it was checked against

`crossref_clean` was machine-checked for the first time on 2026-09-03. **45 documents disagreed with
the checker, in both directions**, and the two directions are not the same defect:

- **21 claimed clean while carrying findings.** The dangerous one: the AUDITED bar rests on this
  field, and those documents were being treated as audited when they were not.
- **24 claimed dirty with no findings — and that is mostly not their fault.** Three fixes landed in
  `audit_crossrefs.py` the same night (substrate excluded as a subject, a measured fan-in hub
  threshold, alias merging across taxonomies), and every one of them legitimately removes findings.

> **A status field that was honest when written and is stale through someone else's improvement is
> the same class as a remainder that goes stale on another session's success.** Correcting the 24 as
> though they were errors would be the token-satisfaction failure again.

**So the fix is the same in both cases: record what the field was checked against, and when.** A bare
`crossref_clean: true` is a claim with no provenance, and provenance is the only thing that
distinguishes *"this was clean"* from *"this is clean"*.

```yaml
audit:
  crossref_clean: true
  crossref_checked: 2026-09-03          # when
  crossref_report: audit_m55_fresh.json # against what
```

Same rule as the scorer, which now prints the mtime and identity of all three of its inputs, and the
same rule as a census: **a figure without its population is a number that agrees with itself.**
