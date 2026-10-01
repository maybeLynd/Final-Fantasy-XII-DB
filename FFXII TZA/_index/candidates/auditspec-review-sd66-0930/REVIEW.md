# SWE2-AUDIT-SPEC review of SD-66 (sd66-attach-slot-writers-0930 at ba2580021): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS.
Reviewed: `ba2580021`. Record: [sd66-attach-slot-writers-0930](../sd66-attach-slot-writers-0930/README.md). Static.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD66-0930 | sd66-attach-slot-writers-0930 | ba2580021 | ACCEPT |

**Re-run.** `sd66_attach_slot.py` from its own directory: F1-F3 PASS, `FAILS 0`, identical to the committed `.out`
ignoring CR ([rerun_sd66_attach_slot.out](rerun_sd66_attach_slot.out)). The record directory stayed clean.

**Re-derived independently** ([sd66_rederive.py](sd66_rederive.py) / [.out](sd66_rederive.out),
[sd66_rederive2.py](sd66_rederive2.py) / [.out](sd66_rederive2.out)). The author's scan has three blind spots: it walks
only catalogued functions, sees only `call`, and drops a static whose vtable its lea→mov pattern cannot find. My sweep
avoids all three. It decodes every byte position in `.text` as `call` or `jmp qword ptr [reg + 0x40]`, with any register,
with or without REX, and ignores the function list. It then walks back up to 8 instructions for how the register was loaded.
- 169 such sites exist in `.text`.
- 19 load the register from a static (`mov reg, [rip → G]`). They go through exactly the five statics the record
  names, from exactly the five bodies:
  - `02CF8580` ×11 (`006349B0`);
  - `02CF8370` ×3 (`00634540`);
  - `02CF8680` ×2 (`006352A0`);
  - `02CF9530` ×2 (`00635DC0`);
  - `02CF8880` ×1 (`006357E0`).

  None of them is a route.
- The second form, `lea rX, [static]` then `mov reg, [rX]`, occurs at **0** sites. No `jmp [reg+0x40]` goes
  through a static.
- The other 150 sites take their object through a pointer, which is the record's stated limit.

**Class identity by a second route.** For each static I followed `lea rcx, [G]` into its constructor call. All five
constructors store vtable `00D581C0`, RTTI `Phyre::PClassDescriptor`. That is the base class; the author's
`static_vt` finds the derived template vtables, which F3 pins for `02CF8580` (`00D56ED0`, slot `+0x40` =
`0062EFD0`). So the five statics are class descriptors by both routes. Only 006349B0..00635DC0 load them. At
`00634A9C` the vtable is read from `[02CF8580]` and `rcx` is the descriptor object, so `+0x40` is a vtable slot of
the descriptor, as the record reads it.

**Controls.** F1 asserts the exact per-body counts, so it is sensitive to any added or lost site within its scan
domain. The raw sweep above shows that the domain was not missing anything reachable in the static-loaded forms.
F2 checks the class names by RTTI, and F3 checks one slot and one inline member build.

**Limits stand as written.** 150 `[reg+0x40]` calls reach an object through a pointer or argument. They are not
classified here or in the record. They include the five routes' own dispatches. A registration that reaches a
descriptor through a pointer, outside the routes, is therefore not excluded.

**Verdict.** ACCEPT. "Five bodies / 19 calls, all Phyre's own metaclasses (`PClassDataMemberDynamic`,
`PClassDescriptorDynamic`, `PClassMember`, `PClusterDependencyList`, `PSharray<PString>`)" holds against a sweep that is
independent of the function list.
