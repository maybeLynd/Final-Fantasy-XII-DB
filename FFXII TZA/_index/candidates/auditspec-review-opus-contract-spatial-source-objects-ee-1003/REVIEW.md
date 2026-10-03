# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-contract-spatial-source-objects-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-SPATIAL-SOURCE-OBJECTS-EE-10-196AD` · Package: `_index/candidates/opus-contract-spatial-source-objects-ee-1003/` · Page: `18-Audio/CONTRACT-spatial-source-objects.md` (commit 6a9eb7555; reviewed at HEAD e8b1a961a, package and page unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row, fewer than 15, so I read it clause by clause against the full listing, including the three `.rdata` vectors it uses. All 5 anchors are correct. The sentence holds as written, including OPUS's correction of the shuffle count.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`, exit 0.
- `rows.json`: 1 row, 5 anchors; rejected 0, skipped 0, missing 0, corrections 1 (`007F74E0`).
- Constants resolved: `00D11570` = (1,1,1,0), `00D560A0` = (3,3,3,3), `00D22600` = (0.5,0.5,0.5,0.5).
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `007F74E0` correct.
    - `u` = `movaps [rdx]` - `[rcx]`, `v` = `movaps [r8]` - `[rdx]` (aligned).
    - Four `shufps`: `u` by 0xD2 (z,x,y,w) and 0xC9 (y,z,x,w) at `007F74F4`/`007F74F8`, then `v` by 0xC9 and 0xD2 at `007F74FF`/`007F7506`. This is the corrected count, and it holds.
    - Two products, `v.yzxw*u.zxyw` and `v.zxyw*u.yzxw`, then `subps` (`007F750D`). That gives `n.x = u.y*v.z - u.z*v.y` and the other lanes cyclically. The fourth lane is `u.w*v.w - v.w*u.w`, as stated.
    - `s`: `n*n`, mask (1,1,1,0) (`007F7516`), two `haddps`.
    - `r` = `rsqrtps(s)` (`007F7525`). One step: `(3 - s*r*r) * (0.5*r)` (`007F752B..45`). The result is multiplied by `n` in all lanes (`007F7548`), then lane 3 is replaced by `n.w` (`shufps 0xff`, `movss [rsp+0xc]`).
    - `movdqa [r9]` (`007F755D`) stores 16 aligned bytes. No value is returned.
- README count sentences checked against `rows.json`: "named 1 F-frontier functions", "1 applied with 5 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match. The one **OPUS corrections** bullet matches `rows.json` `corrections`.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): `007F74E0` is a member of `SQEX SEAD sound library span` (letter C), which `18-Audio/sead-function-identification.md` declares, not this page. It is not in scope here, so the base rule applies.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- The README title says "cloud-drafted", while its first paragraph and `rows.json` `session` name `local-ee-drafter` (a local agent, no cloud credit). It is a wording inconsistency only.
