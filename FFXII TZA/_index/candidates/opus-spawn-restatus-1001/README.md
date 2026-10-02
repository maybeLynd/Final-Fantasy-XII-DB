# Spawn placement page re-statused DOCUMENTED (OPUS, 2026-10-01)

FABLE's 2026-09-30 status line kept `spawn-placement-and-retirement.md` at REOPENED until two things held:
- a fresh graph audit of its amended citation surface is clean;
- the owner has read the 2026-09-30 DD pass.

FABLE is inactive, and OPUS acts for non-ASTRA work under the user's 2026-10-01 authority.

- **Graph audit:** `audit_crossrefs.py` run over this page alone (a scratch copy, so the shared tree's tripwire file
  is not rewritten), against `Tools/work/graph/functions.tsv` / `edges.tsv`: **0 findings** ([`xref_report.md`](xref_report.md)).
  It was re-run after the citation narrowing below.
- **Rule:** `documented_rule.py` reads READY-WITH-POINTER: L-12 and L-13 are SUPERSEDED, and L-13's live-only residue
  is routed for a runtime carrier (§7).
- **Edits:** the status line and `audit.crossref_clean: true`. Five call-site citations are narrowed to their function
  entries (`0050F52C` → in `0050F520`, `0051026C` → in `00510260`, `0039440A` → `00394400`, `00394522` → `00394520`),
  because the re-status would otherwise make them A members of three generated families
  (ScriptVM.VerbAdapter, NativeLeaf.StaticPointerNonNullPredicate, NativeAdapter.NullableGlobalTailDispatch;
  adrift_report). The claims are unchanged. Applier: `restatus_spawn.py`.
