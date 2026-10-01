# SWE2-AUDIT-SPEC review of SD-61 (sd61-pannotation-fields-0930 at 73e6ff01f): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS.
Reviewed: `73e6ff01f` (record) and its prose-only correction `f55dd3c9a` (the struck 12-instruction premise, on
SWE2-AUDIT-SEM `e89b4567b`). Record: [sd61-pannotation-fields-0930](../sd61-pannotation-fields-0930/README.md).

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD61-0930 | sd61-pannotation-fields-0930 | 73e6ff01f (+ f55dd3c9a) | ACCEPT |

**Re-run.** `sd61_pannotation.py` from its own directory: F1-F4 PASS, `FAILS 0`, identical to the committed `.out`
ignoring CR ([rerun_sd61_pannotation.out](rerun_sd61_pannotation.out)). The record directory stayed clean.

**Re-derived independently** ([sd61_rederive.py](sd61_rederive.py) / [sd61_rederive.out](sd61_rederive.out)).
- **The site count.** A raw E8/E9/0F8x sweep of `.text` finds 70 branches to `006B66C0`, all `call`, no tail
  jumps or jcc forwarders. That matches the author's 70, which came from the function-list call cache.
- **Per-site facts the checker assumes but does not test.** The checker's F2 takes `r8` as the text `r8, rax` and
  does not see where `rax` comes from. It also takes "follows member" as the nearest earlier `00632960` call, and it
  checks the attach only in `005B4E00` (F4). For each site I followed the annotation object A (the `rcx` of the
  constructor call) through the site. The result is 69 rows of one shape:
  - key `rdx` = `02CF8570`;
  - `r8` = the return of a call to `00630180` just before;
  - `r9d` = 0;
  - the member registered by the preceding `00632960` is named `m_count`;
  - the value store `0x7FFFFFFF` lands on A + 0x30, and the derived vtable on A + 0;
  - the later `006B67D0` attach passes (M + 0x38, A), where M is the member object of that same registration.

  The 69 sites have 69 distinct members M and 69 distinct owning functions, so "69 classes" holds. The 70th site is
  `006315FD` in `006315B0`, with a non-rip key, as the record says.
- **The key object.** `02CF8570` lies in `.data`'s zero-initialised tail (no file bytes), so its contents are built
  at run time. That agrees with the record's `001641C0` → `006B66F0` initialiser (F3). F3's string, `00D56508` =
  "WriteMask", was checked by the author's run and not repeated.
- **One detail the record does not state.** Each attach is guarded: it runs only while the annotation's node is
  still self-linked (`005B5027`-`005B5035` compare `[A+8]` with `A+8`). So a re-run registrar does not link it twice.
  This adds to the answer; it does not change it.

**Controls.** F2 is a census whose tally would change if any site differed in key, `r9d`, member name, vtable or
value. It is sensitive to those. It is not sensitive to a wrong `r8` source or a mis-attached list, and the
per-site trace above covers both. F4's single-site attach check is now covered at all 69 sites.

**Verdict.** ACCEPT. The answer (key, value type, 0, value `0x7FFFFFFF` on `m_count`, linked at member + 0x38) holds at
every site. The "Reading" line about the top count bit remains an interpretation, labelled as such.
