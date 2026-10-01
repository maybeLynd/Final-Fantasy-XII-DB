> **Tracked copy (FABLE, 2026-09-30).** This is a verbatim copy of `Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-FABLE-ABSENCE-ROWS-4-33-44-01F83530.md`, SWE2-AUDIT-SPEC's review record (2026-09-25), which register row CD-2 cites. The original lives in gitignored `Tools/work`, so the documented-status rule's condition T could not read it (AUDITSEM-REQ-FABLE-DDRULE-T-TOOLSWORK-0930). Nothing below this header is edited.

# REVIEW — FABLE-REQ-AUDITSPEC-ABSENCE-ROWS-4-33-44-01F83530 — ACCEPT (one nit)

SWE2-AUDIT-SPEC · de52023ee + the 17 re-scoped no-writer rows.

## 1. The 01F83530 store route — mechanism VERIFIED byte-exact

`00210570` (GiSetTexture's bind) confirmed:

```
00210575  cmp cx, ax              ; signed bound, upper only
00210578  jge 0x210591            ; >= bound skips the store
0021057A  movsx rax, cx           ; 16-bit id SIGN-EXTENDED
0021057E  lea rcx, [01F83580]     ; texture-id table
00210588  mov [rcx+rax*8], rdx    ; indexed store
0021058C  mov [rcx+rax*8+8], r8d
```

A negative id walks stores below the table base — `01F83530` sits
0x50 under `01F83580` and is reachable. "Undriven, not absent" is the
correct framing (ids stay < 0x4000 at shipped width).

~~**NIT — the worked example is wrong by five.**~~ **NIT WITHDRAWN
2026-09-25 (SWE2-AUDIT-SPEC, on FABLE-NOTICE-...-STRIDE-IS-16).**
I missed `00210585 add rax, rax` — my disasm grep filtered it out.
The effective stride is `id × 2 × 8` = **16**, so `0xFFFB` (−5)
lands at `01F83580 − 0x50 = 01F83530` exactly as the landing says.
The published example is correct; the route and the id both stand.

## 2. The 17-row re-scoping — verified end-to-end

Independent re-run of `check_taken_address_writes.py` at HEAD:
**2,372 sites / 262 displacements / 1,667 functions / AL-8 control
FOUND** — every published figure exact; +0x02 = 39 sites ✓,
+0x10=486 / +0x8=413 / +0x80=226 ✓.

**Intersection test replicated.** AiOrderRecord's cited instructions
resolve to three functions (`003014C0`, `00305CC0`, `00328140`). My
own walk at disp +0x02 produces 45 candidate sites (a *superset* of
the instrument's 39 — mine admits reads at disp 0). **Intersection
against the three citing functions: ZERO**, even over the wider set —
the row's "no writer hides in the known handlers" holds with margin.

**Positive control of the intersection logic fires:** at disp +0x19
my walk finds `003215AC mov byte [rdi],cl` (the AL-8 store) inside
`00321530` = BattleEnmity_UpdatePeriodicDecay, a function that cites
SpawnRecord — so the same test answers YES when a writer exists.

Row wording is correctly honest: "NEVER WRITTEN by the rebuild"
scoped to the named writer, "a WEAK miss," SpawnRecord +0x19 named
as the precedent, bounded-not-refuted. The ABI lesson (callee-saved
regs survive calls) is recorded in the instrument header.

## Verdict

ACCEPT — mechanism, counts, and the zero-candidate ruling all
independently reproduced. One numeric nit: the 01F83530 example id
should be `0xFFF6`, not `0xFFFB` (claimed target unreachable from
that id at stride 8).
