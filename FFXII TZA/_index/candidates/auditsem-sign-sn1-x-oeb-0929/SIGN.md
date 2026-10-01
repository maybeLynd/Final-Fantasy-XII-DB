# OEB signature — SN-1 q3 head word X (SWE2-AUDIT-SEM, 2026-09-29)

*Provenance: this SWE2-AUDIT-SEM record was kept only in the gitignored `Database/Tools/work/SWE2-AUDIT-SEM/SIGN-SN1-X-OEB-2026-09-29.md`, which closed register rows cite (found by the DD-rule T review, `auditsem-review-ddrule-t-0930`). Published here unchanged by SWE2-AUDIT-SEM so the evidence is tracked; each `##` heading now names SWE2-AUDIT-SEM.*

Request: `OPUS-REQ-AUDITSEM-SIGN-SN1-X-OEB`. Package:
`_index/candidates/sn1-x-oeb-package/sn1_x_oeb.py` (OPUS). Non-author signature:
OPUS authored the package, FABLE authored `x_negatives.py`; this signature is `SWE2-AUDIT-SEM`.

**Outcome: SIGNED.**

Executed evidence (all run by this auditor, non-author):

- `sn1_x_oeb.py` → `FAILS 0` (P1, P2a, P2b, PC, P3a, P3b, P3c).
- Negative run directly, outside the composer: `sn1-q3-page-map/x_negatives.py` → `FAILS 0`
  (N1 N2 N3 C; C is the E-recovery control — the same search that fails to explain X recovers
  q2's `ceil(instructions/32)` count law in 50 of 50, so the instrument is proven sensitive).
- Second negative run directly: `sn1-layouts/sn1_q3_x_content.py` → `FAILS 0` (Q X G P B N C;
  its C likewise recovers `E = ceil(codeBytes/32)` in 50 of 50).

The four signed parts:

1. **The excluded artefact is the ATEL compiler** — P1: the shipped `.sbn` sources of `btlctrl`
   (7), `evctrl` (6) and `mapctrl` (5) include headers through `${ATEL_HEADERPATH}`; `ctrl` (0)
   does not. The compiler that emitted each `.ebp`/`.dbg` pair is the excluded tool.
2. **No admitted source carries it** — P2a: no companion reader in the certified image
   (`sn1_residue_boundary.py` B1/B2/R1/P as a checked prerequisite). P2b: 89,414-file walk of the
   extract finds no PE (`MZ`+valid `PE\0\0`) and no ELF — no toolchain ships to produce or read
   the artefact. Control PC proves the walker sees what it claims not to find: a planted PE and a
   planted ELF in scratch are both found (1/1).
3. **The negatives hold** — P3a/b/c executed as checked prerequisites, and (1)/(2) above
   re-executed by this auditor directly. X resists every admitted explanation tried: best simple
   formula reaches 33/50, module-global grid 26/50, line-pages 11, byte-value pages 27 — while the
   same search machinery recovers the known laws in 50/50.
4. **Independent execution** — this signature is issued by `SWE2-AUDIT-SEM`, a non-author, on
   re-run output rather than the committed `.out` files.

Not claimed: what X counts. The residue text stays — OEB-closed for the gate, unanswered in fact.
That is the correct shape of this signature.

Signature: SWE2-AUDIT-SEM · 2026-09-29 · controls executed on certified inputs
(image SHA-256 `73461D08…21F8`; extract `D:/FFXII_TZA_extract`).
