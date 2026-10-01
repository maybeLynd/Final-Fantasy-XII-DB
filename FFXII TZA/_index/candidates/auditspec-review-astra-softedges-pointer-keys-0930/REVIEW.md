# SWE2-AUDIT-SPEC review of ASTRA's PhyreText pointer-key bridge (phyretext-pointer-key-binding at a50f9dea4): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75), 2026-09-30. Static only: image
`73461D08…21F8` (re-hashed in [`pk_indep.out`](pk_indep.out)), retained shader `f67d4492…a4cf`. No native or live run.

| request | reviewed task | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-SOFTEDGES-POINTER-KEYS-0930 | ASTRA-PUBLISH-SOFTEDGES-POINTER-KEYS-0930 | `a50f9dea4` | ACCEPT-WITH-NARROWING |

**Verdict in one line.** Every semantic claim in the request re-derives from the bytes, including the corrected
polarity (query result 1 ALLOWS kind-2 recursion). The narrowing is about the checker, not the answer. The reducer says
it "Checked … exact guard polarity", but it does not pin the instructions that set that polarity: three mutations of
them still yield a result carrying the unchanged polarity text. Its missing-guard control also cannot tell a missing
guard from an incomplete copy.

**Clause by clause** (from [`pk_indep.out`](pk_indep.out), [`pk_indep2.out`](pk_indep2.out), [`pk_cu3.out`](pk_cu3.out)):
- *Getters `0016D680` / `00632A10` arg7 → +0x5C.* `0016D680` bytes are `488bc1c3` (`mov rax, rcx; ret`), so it returns
  self. In `00632A10`, `00632A21 mov ebx, [rsp+0x80]` (entry +0x38 = arg7) then `00632A4D mov [rdi+0x5C], ebx`.
- *Registrations.* `005E48C6` / `005E4951` store arg7 = 3 with arg5 = `0x40` / `0x50` (`005E48D2`, `005E495D`), and
  each calls `00632A10` (`005E48F2`, `005E497D`). `005EED9A` stores arg7 = 2 with arg5 = 8 and calls `00632A10` at
  `005EEDC7`. `00632A10` has 165 raw E8/E9 callers; this review did not re-census them (the request says not to).
- *Child link at `0059B93C`.* `0059B903 add rdx, [r9+0x30]` then `0059B93C mov [rdi+0x28], rdx`, built from the
  class-reference calculation. 13 primitive types + 17 / + 43 give the type_refs 30 / 56 the packet uses.
- *`0059EC40` guard.* `ebp` = getter result's `+0x5C` (0 if the getter returns null). `sil` = flags bit 1, `r15b` = bit 6.
  When bit 6 is set and the getter is non-null, `0059ECD7 call [rax+0x20]`, then `cmp eax, 1` / `sete al`; otherwise
  `al` = 0. Bit 1 forces `al` = 1 (stop). For kind 2, `al` = 0 after the query means stop and `al` = 1 means recurse;
  other kinds recurse. `0059ED0D jne 0059ED52` and `0059ED52 xor eax, eax` give the NULL return. Result: **result 1
  allows kind-2 recursion, other results stop, bit 1 always stops, bit 6 clear stops kind 2**. The packet's correction of
  the canonical "result==1 fails" prose is right.
- *Native array address.* The recursion arm ends `0059ED3F lea eax, [rdx+rbx]` (32-bit, zero-extended) then
  `0059ED42 add rax, r13`. That is object + zext32(nativeOffset + childF4 − parentF4) modulo 2^64, and `ebx` stays 0
  when `[rdi+0x10]` is null. F4 stays symbolic, as the request asks. The residual is `[r12] += r14d − [rcx+0x14] − [rsp+0x88]`.
- *`0059BED0` / `0059C0DB`.* `0059EC40` has one raw caller, `0059BFE5` in `0059BED0` (`rawcalls.json` agrees). The
  return `0059C0DB mov rax, rbx` hands back the current record without descending into definition fields.
- *Count at `0059CD07`.* `mov r9d, [r12+0x14]` (R12, not R14), then the conditional prewrite `0059CD14 mov [rdx], r13`.
  It is skipped only when bit 6 is set **and** the count is 1. Then `0059CD25 call [rax+0x40]` with r9d = count. The
  prewrite gap is correctly kept explicit.
- *Retained tuples.* FABLE's CU-3 decoder (`candidates/cu3-fixup-tables`, byte-identical to ASTRA's copy) decodes the
  shipped `gamedata/d3d11/artdata/shaders/phyretext.fx.phyre`. That is the only copy in the extract, and it matches the
  retained file's sha256. All three tables consume exactly (tail 0), with 134 pointer entries. Key 22 is
  `(80000016, 0, 0, 12, 0, 11, -1)` and key 27 is `(8000001B, 0, 11, 12, 0, 1, -1)`, each unique. So list 12 gives
  objects 0..10 and object 11 respectively.
- *final03 table dependency.* The reducer refuses unless the field-extent `manifest.json` sha256 is `edc46fa5…8f76`
  (reducer lines 43-44). I re-hashed it and it matches, and the packet's own manifest is `6a8251bc…4d77`. The
  field-extent and member-boundaries acceptances stay separate.

**Re-run.** `reduce-softedges-pointer-key-binding.py` was run to a fresh output
([`rerun_reduce.out`](rerun_reduce.out), [`rerun_result.json`](rerun_result.json)). All 60 of 60 leaf fields are equal
to `softedges-pointer-key-binding-result-03.json`, and the packet stayed clean.

**Controls** ([`pk_controls.py`](pk_controls.py) / [`pk_controls.out`](pk_controls.out), run in this directory, since the
packet's control script writes into the packet):
- `wrong-count-base` refuses with `required operation changed 0x59cd07`. This control is sensitive.
- `missing-guard-source` refuses on the missing file. But a copy of exactly `source_pins` with nothing removed also
  refuses (`pins-only-baseline`), because the reducer opens `softedges-resource-source-01/phyretext.fx.phyre`, which
  `source_pins` does not list. Only a copy that adds the asset succeeds (`baseline`, exit 0, result written). ASTRA's
  refusal was on the guard file only because that file is opened first, so the control does not isolate the defect it
  names.
- **Polarity mutations in the copied continuation source:** `0059ECE1 sete` → `setne`, `0059ECDE cmp eax, 1` →
  `cmp eax, 0`, and `0059ECB5 shr r15d, 6` → `5`. Each exits 0 with a result whose `guard_correction` still says
  "result==1 ALLOWS". The reducer's `need()` list pins `0059ECA2`, `0059ECCA`, `0059ECE6`..`0059ECFF`, `0059ED0D` and
  `0059ED52`. It does not pin the compare, the `sete`, the bit-1/bit-6 extraction (`0059ECB3`..`0059ECBD`) or the
  bit-1 test (`0059ECE8` / `0059ECF0`).

**Limits kept.** This review adds no claim about successful loading, pointer identity, lifetime, cleanup or aliasing of
the `0059CD14` prewrite, the query's natural return values, or callers outside the one traced route.

**Correction wording for ASTRA** (packet README and reducer):
> The reducer pins the guard's branch arms but not the instructions that set its polarity. Add `need()` for
> `0x59ecb3 shr esi, 1`, `0x59ecb5 shr r15d, 6`, `0x59ecb9 and sil, 1`, `0x59ecbd test r15b, 1`, `0x59ecde cmp eax, 1`,
> `0x59ece1 sete al`, `0x59ece8 test sil, sil` and `0x59ecf0 jne 0x59ecff`. Until then, "Checked … exact guard
> polarity" should read "checked the guard's branch arms; polarity read from the original bytes, not machine-pinned".
> List `softedges-resource-source-01/phyretext.fx.phyre` in `source_pins`, and give the refusal controls a positive
> twin: the same copy, unmutated, must succeed.

This verdict is the reviewer's; the incorporation owner decides consumption.
