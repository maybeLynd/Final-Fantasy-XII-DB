# SWE2-AUDIT-SEM review — GI-8 to GI-11: effect-element answers, the census re-walk and nine corrections (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30; this claim was
taken over from an earlier session of the same identity that ended without working it.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-GI-EFFECTS` |
| reviewed | `4e32dd8df` (author **FABLE**) — [`gi-0929-effects/consumer-check.md`](../gi-0929-effects/consumer-check.md) and its scripts; `members/type_census.py` |
| image / data | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`; `D:/FFXII_TZA_extract` |
| **verdict** | **ACCEPT**, scoped: the census re-walk (correction 1) and corrections 2, 3, 4, 5 and 9 are re-derived independently; the GI-9/10/11 per-type semantic readings are accepted on the producer's re-run checks only (§3). |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`gi_effects_checks.py` (K1–K18), `d0_selector_census.py`, `gi10_cores_check.py` (139 checks), `gi10names.py` and
`members/type_census.py` (C1–C7) all end `FAILS 0` and match their committed outputs ([`producer_rerun.out`](producer_rerun.out)).

## 2. Independent re-derivation (SWE2-AUDIT-SEM)

**Correction 1, the census** ([`efx_own_census.py`](efx_own_census.py), [out](efx_own_census.out)). My own walker, not
`type_census.py` and not its embedded-file list: every `.efx`, `.efb`, `.cm` and `.mpk` in the extract (3,288 / 410 /
1,066 / 550 files) byte-searched for the three EFX magics at any offset; a stream counts only if its chunk walk ends
exactly at the header `+0xC` size (0 hits refused). Result: **4,229 streams (3,288 `.efx`, 410 `.efb`, 144 `.cm`, 387
`.mpk` — 531 embedded), 48,868 `0xA00` records, 55 distinct element types, `0x8B` the only type authored once**,
`0x04` = 173, `0xA3` = 447, `EFX0009` ×1, `EFX0008` ×7. Every published number reproduces. Limit: extensions other than
those four were not scanned; the claim that only `.cm` / `.mpk` embed streams rests on the producer's full-extract search.

**Image corrections** ([`gi_eff_image.py`](gi_eff_image.py), [out](gi_eff_image.out)):
- **2** — `002F3BC0` has exactly one direct site, `00441E71`, in a fragment of `00441B30` (the element creation path the
  page names); the update `002F3910` has two (`0043EFBA`, `00442354`). A step called once per element is a birth.
- **3** — `00454890` is not a `.pdata` start, not an instruction boundary in its fragment `00454480`–`004548AA`, and has no
  rel32 site or qword; `00452C70` is a function start with two callers (`004524A6`, `004524DB`).
- **4** — `0054C6B0` / `0054E040` are each called once from the birth bodies (`0052D82C`, `0052E9A2`); `0054C440` /
  `0054DD30` are tail-jumped from `0052E270` / `0052F400`, as the corrected text says.
- **5** — `0045F600` has two direct callers (`0045FD96`, `00529252`); consistent with a shared gate, not a per-type tail.
- **9** — covered by the census: `EFX0009` ships exactly once.

## 3. Not re-derived here (SWE2-AUDIT-SEM)

The per-type draw walks of `0x00`–`0x0A`, the `0x40`/`0x41`/`0x42`/`0xD0`/`0xD1`/`0xAB` semantics, the `0x60`–`0x74` and
`0x80`–`0x97` tails beyond the corrections above, and corrections 6–8 rest on the producer's K-checks and the 139 core
checks, re-run green but not independently rebuilt. The kind-`0x54` re-walk and the UQ-204 note are routed by the
record and not reviewed here.
