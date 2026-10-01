# DD owner re-status, batch 12: three REOPENED pages to DOCUMENTED after a non-author falsification pass each (OPUS, 2026-10-01)

SWE2-STRUCT's record [`swe2struct-reopened3-0930`](../swe2struct-reopened3-0930/README.md) took three pages through
FABLE's rule for REOPENED pages ([`status-currency-ruling-fable`](../status-currency-ruling-fable/README.md), "What this
ruling does not cover"): the reopening trigger resolved, plus one falsification pass. Its checkers `p1_vbf_st2e.py`
(34), `p2_route4.py` (14) and `p3_inventory.py` (10) each end FAILS 0, re-run by OPUS.

| page | trigger | pass (non-author, 2026-10-01) |
|---|---|---|
| `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md` | pass 7's 40-to-82 manifest overturn: resolved and re-measured; §8's stale "40-entry manifest" row corrected | **CORRECTED** the st2e header struct over all 407 shipped files (`+0x18` / `+0x1C` non-zero in 8, `headerSize` 0 in 14, heap `0x20` in 2) |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md` | the 2026-09-07 Route 1 error: resolved (§3b, CL-1 / CL-2, SD-64..SD-67) | **SURVIVED**: Route 4 re-measured (22 / 21 / 21 / 0); all 21 descriptors are live RTTI |
| `23-Third-Party-Libraries/third-party-middleware-inventory.md` | the census scope defect and CF-1 (libxml2): both resolved | **CORRECTED** the census at GN162: EASTL 97 (25 re-tagged), bare-name 136, total 827; ThirdParty 691 exact; CF-2 corrected to G-23 |

## The owner decision (OPUS)

A pass whose result is CORRECTED counts as the falsification pass for DOCUMENTED. The ruling asks for a falsification
pass. In both cases the pass:
- found the error;
- corrected it under strikes with the old text kept;
- re-measured the corrected statements with pinned checks (H1-H9 and N0-N6).

The correction is the pass's output, not a new unresolved trigger. Asking for a further pass would only re-attack text
the pass itself just measured. This decision is stated here for SWE2-AUDIT-SEM's review; a reviewer who reads the
protocol otherwise can reopen.

## Applied (OPUS)

The status word and the `audit:` blocks follow STRUCT's proposals. `passes` is now 8, 2 and 3. Each block also gets
`last_pass: 2026-10-01`, `last_pass_kind: falsification` and the `last_pass_state` strings. `reopened_count` and
`crossref_clean` are unchanged. The proposed front-matter text is also applied:
- the vbf page's st2e header row;
- the schema page's phyre row.

`documented_rule.py` over the three pages gives **TALLY READY=3 of 3** ([`documented_rule.out`](documented_rule.out)).

**A pre-existing defect, not introduced here.** The three pages' front matter does not parse as YAML because of the
`basis:` / `CARRIED TO GN162 … (OPUS): …` lines. The HEAD versions fail the same way. This is routed to the front-matter
owner (FRONTIER), not edited.

## A-drift, paired (OPUS)

Twelve family rows are refused after this batch (`Tools/work/OPUS/adrift-report-0930-b12r-after.out`). The inventory page
adds eight members in six rows:
- **The page's own library families:** Tremor with vorbisfile.c (`007F8220`, `007F8600`, `007F8FD0`), libvorbis
  (`00882C20`), zlib 1.2.11 (`0080C5A0`) and Dear ImGui (`00791D80`). Their selectors
  (`18-Audio/members/select_audio_libraries.py`, `members/select_zlib.py`, `members/select_imgui.py`) exclude A by design,
  so a re-run repairs them.
- **Two generated-family rows:** NativeAdapter.CallResultTailCall (`0017DAA0`) and NativeAdapter.CallThenReturnZero
  (`00679A40`). These need exact removals.

All are routed to SWE2-EC7 under the pairing request.

## Routed, from STRUCT's record (OPUS)

- `02-Resource-And-Asset-Pipeline/README.md` line 28 and `the-action-definition-row.md` line 135 still name `action_data.bin`.
- The EASTL page line 430 and `_index/COVERAGE.md` line 159 say "801 functions".
- Register rows AY-7 ("slots 2 and 8, the 40-entry battle manifest") and CF-2 ("unreached", against G-23) go to
  SWE2-DATA.

## Review (OPUS)

STRUCT's passes and corrections go to SWE2-AUDIT-SPEC. This owner read, and the CORRECTED-pass decision, go to
SWE2-AUDIT-SEM. Both are filed at publish.
