# Reconstruction readiness, pass 2: 07-Combat-Action

- **System folder:** `FFXII TZA/07-Combat-Action/` (slug `07-action`)
- **Stream:** R2, for FABLE (brief `docs/cloud-briefs/re-readiness-r2.md`, part A: pass 1 mapped this system)
- **Pass 1:** `cloud-reports/re-readiness/07-action.md` (2026-10-02, cut from `main` at `c3aec14d`)
- **This pass:** 2026-10-03, against the snapshot at `b23bdddd` (synced from XIIOnline `f9d9053b9`)
- **Method:** text only. Every pass-1 gap was re-read against the current pages and `FFXII TZA/_index/OPEN-QUESTIONS.md`.
  The folder's pages were also diffed against `c3aec14d` to find what changed since pass 1. Nothing here was checked
  against the executable.

## How to read the citations

A citation `page:line` gives the path **below `FFXII TZA/07-Combat-Action/`** and the line number at `b23bdddd`.
Pages in other folders are given **below `FFXII TZA/`** and start with their folder number (`00-…`, `04-…`, `09-…`).
Register rows are cited by id, with the state cell quoted. "Not stated" means no page says it.

Verdicts (brief, part A.2): **CLOSED**, **NARROWED**, **OPEN**, **WRONG-IN-PASS-1**. Classes for OPEN and NEW gaps
(brief, Rules): **STATIC**, **RUNTIME**, **DATA**, **DOC**.

## 1. Summary

**Pass-1 gaps: 94** (§2.1: 20, §2.2: 10, §2.3: 11, §2.4: 53).

| verdict | §2.1 open items | §2.2 structural | §2.3 fields | §2.4 contradictions | total |
|---|---:|---:|---:|---:|---:|
| CLOSED | 0 | 1 | 0 | 47 | **48** |
| NARROWED | 5 | 5 | 1 | 1 | **12** |
| OPEN | 14 | 2 | 5 | 5 | **26** |
| WRONG-IN-PASS-1 | 1 | 2 | 5 | 0 | **8** |
| **total** | 20 | 10 | 11 | 53 | **94** |

The §2.4 column breaks down by group:
- A, value-changing: 17 of 17 CLOSED.
- B, counts and caller sets: 5 CLOSED, 1 NARROWED, 3 OPEN.
- C, stale claims: 22 of 22 CLOSED.
- D, banners: 3 CLOSED, 2 OPEN.

**Class of the 38 pass-1 gaps still OPEN or NARROWED**, by each gap's main residue: STATIC 27, RUNTIME 7, DOC 4, DATA 0.
One of them, §2.1-15, also has a DATA half.

**New gaps: 14.** STATIC 6, RUNTIME 1, DATA 0, DOC 7.

**Rating:** pass 1 gave **NOT YET**, with the core at MOSTLY. Pass 2 gives **NOT YET**, unchanged, with the core now
close to READY (§4).

What moved since pass 1:
- **On 2026-10-02 OPUS corrected the pages against every value-changing contradiction pass 1 listed** (A1–A17), and
  struck or annotated all 22 stale claims (C1–C22). Examples: the band-two commit, the `+0x770` latch, the combo table
  and its draw count, the `+0x01` recipe, the steal rule, and the `022C1DB8` byte.
- **New contract text arrived:**
  - the post-result events, in `CONTRACT-apply-result-to-target.md` §8a (FABLE, 2026-10-03);
  - the presentation-slot ABI, in `CONTRACT-native-command-seam.md:158-169`;
  - fourteen dated OV-42 subsections on the availability page (`Action-Availability/…:698-1457`).

  These answer the effective action id, most of the special-sequence routine `00306760`, the slot walker's path, the
  event ring's reset and the message realiser.
- **Eight pass-1 gaps were already answered at pass-1 time**, on pages outside this folder or in the register. Among
  them:
  - frame order: `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` and the battle-unit
    field map;
  - the 24-byte order record: `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`;
  - the 64-byte record's second half: GR-8;
  - `+0x760` / `+0x764`: FW-2.

  The folder still lacks pointers to these answers. Those missing pointers are counted below as DOC gaps.

What still decides the rating:
- the per-target execution step `Battle_ProcessActionTarget` (`00307300`) has no page;
- three order handlers are undecoded;
- the text engines' escape grammar is unread;
- no part of the system has live evidence.
