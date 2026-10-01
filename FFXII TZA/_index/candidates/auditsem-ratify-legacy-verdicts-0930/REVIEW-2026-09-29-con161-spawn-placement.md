# REVIEW — CON-161 + SPAWN-PLACEMENT-PASS1 · SWE2-AUDIT-SEM 2026-09-29

Regressions re-run non-author: `falsify_corridor_query.py` FAILS 0 (K0–K7),
`falsify_spawn_placement.py` FAILS 0 (P0–P8, P4b). Certified image `73461D08…21F8`.

## CON-161 (`3a02f30b6`) — corridor family *does* write a global — **ACCEPT**

Byte-verified: `0032A735 movdqu xmmword[022D91B0]` (RDEC, ends `ret`);
`00391302 mov rcx,[02AEE0B0]` → memset `call 00861EC0` at `0039130E` → OR loop → `ret` (BMASK).

Attacks:

1. **Register-borne store the rip census misses.** The address `022D91B0` never enters a register:
   **zero** `lea`s target `022D91B0`..`+0x10` image-wide, **zero** imm operands carry it, **zero**
   qword/dword data pointers hold it. It is reachable only by direct rip-relative ops. In the
   closure, the only rip-rel reference into the 16-byte range is RDEC's write itself — so no closure
   body reads vf1, and none could without taking its address, which no code ever does.
2. **Closure completeness.** My independent BFS reproduction gives **102 bodies**, identical to K0.
   Zero imm call/jmp targets fall outside the function table (no tail-jump escapes). **Residual:**
   20 indirect `call`/`jmp [ptr]` sites (CRT import thunks `00861Fxx`/`0087AF34`, IAT calls in
   `00809620`/`00809848`/`00216660`/`00383F10`, vtable calls `[rbx+28]`/`[rdi]`) cannot be followed
   statically — an indirectly-reached body could write a global the census can't see. That bounds the
   *write* side; the surviving claim — "no verdict reads an earlier call's write" — is established
   by the reader census, which the bound cannot undermine.
3. **Store-mnemonic coverage.** Zero closure rip-rel writes use mnemonics outside the checker's
   STORES list (`stos*`/`movnti`/`xchg`/`push`/`pop`/AVX forms all absent).

The correction's own narrow claim is exactly what the evidence supports: writes happen (RDEC→vf1,
BMASK→its buffer) but no verdict consumes them.

## SPAWN-PLACEMENT-PASS1 (`f2ab6f431`) — **ACCEPT** (no correction; pass survives)

**P4b attack first, as requested.** `003272A0` (leader getter, 54 B leaf) verified byte-exact:
`call 003590D0` (focus handle) → `test byte[02089340],0x10` → `003588B0` resolve → `00263E30`
record → `test byte[rax],8` → returns the record or 0. `003273B0` (the walk's slot test):
`call 003590D0; cmp eax,ebx; sete` — pure handle equality.

- **Other-than-focus unit? Impossible.** The getter returns `00263E30(003588B0(003590D0()))` or 0 —
  the gates can only zero it, never substitute.
- **Null while focus slot valid? Yes, four ways** (flag bit, resolve, record, byte&8) — but each
  funnel to "null leader → return 0", which I4 already claims, and none makes the band measure to a
  different slot. The walk's admission is by *handle equality* (`003273B0`), the getter's gates are
  *existence* conditions — the asymmetry is about when a leader exists, not which unit is consulted.
  The corrected I4 text ("the leader must also be one of those slots and pass their status gate")
  is accurate and keeps the struck original. I4 holds.

**Added facts byte-verified:** `0023A550 mov dword[02089358],0xB4` (arcDeg default 180); `00234AF0`
reads it via `mov r15d,[rip]`; area-mode draws `call 00328370` at `00234C43`/`00234C6C`; both
divisors unguarded — `00234C57 idiv ecx` (`cvttss2si` of `(max-min)*100` — a sub-0.01 band truncates
to 0 and faults even though the empty-band gate passed) and `00234C76 idiv r15d` (arcDeg=0 faults).
No `test` precedes either `idiv`.

## Verdict

**ACCEPT both.** Corrections precise, claims correctly narrowed, regressions survive non-author,
discriminating anchors independently byte-verified. Disclosed bounds: the corridor closure's 20
indirect edges (write-side only); no shipped-script verb census (capability claim unaffected).
