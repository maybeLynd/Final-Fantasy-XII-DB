# SWE2-AUDIT-SPEC review of DD residue batch 6, the `02` top-level pages (SWE2-CONTRACT, `acfaf396a`): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
SWE2-CONTRACT's `acfaf396a` (the record [README](../swe2contract-ddres-b6-0930/README.md), `b6_typed_list.py`,
`b6_request_queue.py`, `b6_section_addressing.py` and their outputs, and the three page diffs), measured at HEAD
`17a959c94`. Static, certified image (sha256 `73461d08…`, asserted by every script here).

| request | record | commit | verdict |
|---|---|---|---|
| SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B6-0930 | swe2contract-ddres-b6-0930 | `acfaf396a` | ACCEPT-WITH-NARROWING |

Independence: the author is SWE2-CONTRACT at 2026-09-30T18:42Z, which is a reviewable lane.

**Re-run.**
- [rerun_b6_typed_list.out](rerun_b6_typed_list.out), [rerun_b6_request_queue.out](rerun_b6_request_queue.out) and
  [rerun_b6_section_addressing.out](rerun_b6_section_addressing.out) are identical to the committed `.out` files
  (ignoring CR). All three end `FAILS 0`.
- `documented_rule.py` (FABLE's gate) re-run at HEAD gives `TALLY READY=1 READY-WITH-POINTER=2 of 3`, `FAILS 0`, the same
  as committed ([rerun_documented_rule_at_head.out](rerun_documented_rule_at_head.out)).
- SWE2-DATA's `pf_env_checks.py` ([rerun_pf_env_checks.out](rerun_pf_env_checks.out)) passes everything. One line
  differs from the copy in the package: the informational "pages citing 0026D910" count is 20 at HEAD, not 22 (the page
  set has moved since). No check depends on that count.
- The package and its dependency dirs are clean after the re-runs: `git status --porcelain` shows nothing under
  `swe2contract-ddres-b6-0930/`, `rc22-34-resource-readers-0930/`, `dd-data-4-0930/` or `status-currency-ruling-fable/`.
  `CONTRACT-resource-request-queue.md` was already ` M` with a peer's edits, and I did not touch it.

**Re-derived independently.** My tools use pefile and capstone only:
- [ind.py](ind.py) loads the image and provides `.pdata` roots, a raw E8/E9/`0F 8x` call index, DIR64 relocations, and
  rip-relative and image-base-relative scans.
- [textcache.py](textcache.py) decodes all 1,892,789 `.text` instructions linearly, covering the `.pdata` ranges and the
  leaf gaps. It writes its TSV to the session scratchpad, so run `python textcache.py` first when reproducing.
- **Bit 7 (B1–B8)** ([bit7_rederive.py](bit7_rederive.py) / [.out](bit7_rederive.out),
  [bit7_names.py](bit7_names.py) / [.out](bit7_names.out), [dump_bit7.txt](dump_bit7.txt)):
  - The mask is `0024A733 mov ebx,0xE0` / `0024A73B bts ebx,ecx` / `0024A75F movsxd rax,ebx`, and the test is
    `0024A790` `mov rcx,[r14]` / `and` / `cmp` / `jne 0024A9B1`.
  - The loop is a do-while: `0024A778 mov r12d,0x3F` … `0024A9B5 sub r12d,1` / `0024A9B9 jne`, stride `add r14,0x48`,
    starting at `0208F5B8` (slot 0 `+0x38`). That is 63 iterations, so slot 63 is never visited.
  - The descriptor is stored at `0024A99C mov [r14-8],rcx` (slot `+0x30`).
  - Its fields are packed in GS `TEX0`-register order: base and buffer width `<<14`, then 6 / 6 / 4 bits, and
    `0x80000010`. That fits the name "texture-memory layout pass". What `0024AF50` emits is still not claimed, correctly.
  - Callers: 8 E8 sites, no jcc, no relocated pointer. `ecx` is 1 at six sites, `xor ecx,ecx` at `0025290D` and 2 at
    `00252965`, as the page says.
  - `0024A5A0` returns `xor eax,eax` on a miss (`0024A5E4`) and `mov rax,r9` on a hit. `0024A610` returns an index.
  - **Widened writer sweep, image-wide** (any base, any width, `and`/`or`/`bts`/`btr`/`mov` immediates):
    - There are 54 read-modify-write writes of bit 7 at `+0x38`: the page's 29 inside `0027F5D0`–`002D7600`, 22 more
      outside it, and 3 in `0033A720`.
    - The 22 outside are in `003F4E70`, `00558FB0` (`lic_4_c`, `maru_c`, …), `00560910`, `005755D0` and `0057B800`.
      Every one of them also follows a `0024A5A0` call.
    - The 3 in `0033A720` (`0033B59F`, `0033B5B8`, `0033B5D3`) act on a different object, `rax = [r15+0x100]`, where
      bits 6 and 7 are used as a pair. They are not atlas writers.
    - **No** immediate `test`/`bt` of bit 7 at `+0x38` exists anywhere. The only reader seen is `0024A710`'s register
      mask. So the page's scope ("in `0027F5D0`–`002D7600`") and its blind spot (immediates only; "not claimed: that no
      other code reads the bit") are both correct as written.
  - The names come from `mov rcx,[rip+X]` pointer cells (all relocated).
    - The shared arm clears the five cells `01E0C1F0`, `01E0C230`, `01E0C1E0`, `01E0C270`, `01E0C278`, and message 18
      sets the same five (`0027F7DA`…, `battle_4_p` first).
    - The config screen `00280DE0` also clears the same five, and `00281E00` (its message-18 arm, by the config-screen
      page §7.1) sets them. `002D70F0` clears two of them.
- **E / S / R / C** ([typed_rederive.py](typed_rederive.py) / [.out](typed_rederive.out)):
  - The emitter keeps `r8` in `rsi` (`002D93CF`) and reads `[rsi+0x30]` at 7 sites and `[rsi+0x38]` twice.
  - Every S pin reproduces. Type 7 stores the fields at `+0x4C`/`+0x4E`/`+0x50`/`+0x52`, and byte 7 at `+0x44`.
  - `002A0060` has 5 sites, whose owners are `001D7150`, `0029F130` and `0029F4C0`. `0024A610` has 2 sites, in
    `0029F130` and `002A0060`. No drawer is among the owners.
  - `002432B0` has 113 E8 sites in 108 `.pdata` owners, with no relocated pointer.
  - L1 decodes to x 122, y 100, 28 × 28, `0x0B`.
- **K1–K3 without `kind7.py`** ([kind7_indep.py](kind7_indep.py) / [.out](kind7_indep.out)):
  - `002DF9A0` stores kind 7 exactly once (`002DFF7F`, array `01EDD7E0`), so there is no second language arm.
  - The relocated cells give id `0x6F` = `…\Mrp_Menu\save_load.mrp`, id `0x7F` = `…\Tm2_Menu\DataFace_c.tm2`, and the
    control id `0xBF` = `…\Mrp_Menu\Loca.mrp`.
- **Request slot `+0` / `+0x50` and the escape argument** ([queue_escape.py](queue_escape.py) /
  [.out](queue_escape.out), [queue_escape2.py](queue_escape2.py) / [.out](queue_escape2.out),
  [module_listing.txt](module_listing.txt), [cancel_callers_and_3eb050.out](cancel_callers_and_3eb050.out)). The
  module is `0032E000`–`0032ED80`, 885 instructions.
  - **P (references).** 33 rip-relative operands point into `022C31C0`–`022C51F0`, and all of them are in the module.
    None addresses a fixed slot's `+0` except the `lea` pool bases.
    - The two image-base-relative dwords (`00371733`, `006179FB`) straddle instructions.
    - No relocated pointer points into the range.
    - The control (the jump-table displacement `0x20E2D0` at `0032E0B4`) is found.
  - **D (displacement-0 operands).** I counted every displacement-0 operand at any width, with or without an index, on
    any non-`rsp` base. Only four touch a slot: `0032E153 add [rbx],rax`, `0032E229`, `0032E725` and `0032E97C` (the
    stores of 0).
    - The others are the size-override table, the bitsets, the caller's descriptor (`[rsp+0x90]`, `[rsp+0x60]`), the
      path copy, and padding `nop`s.
    - No slot `+1`..`+7` access exists. This is wider than Z1 (qword, no index) and gives the same answer.
  - **`+0x50`.** It is stored only as `r14` (`0032E6FF`, `r14` zeroed at `0032E670` on the only path in) and as 0
    (`0032E959`). It is read only at `0032E3B4`. The pool lies in `.data`'s zero-initialised tail, so the slot starts at
    0.
  - **Direct calls out.** Z3 does not machine-check these. There are 42 sites to 28 targets. For every target that
    reads an argument register before writing it, the register holds one of: a slot field (`+0x24`, `+0x28`, `+0x2C`,
    `+0x38`), 0, a kind/size integer, or the caller's own argument. None holds a slot pointer.
  - **Stale `rcx`.** A stale slot pointer can sit in `rcx` at two places:
    - `0032E29B` / `0032E2A0`, after the null-callback `0032E3B0` return.
    - `0032EA99`, where `0032E450` leaves slot 63 `+0x68`.

    The callees there, `003EADD0`, `0046DD50` and `003EB050`, all write `rcx` before reading it.
  - **Return values.**
    - `0032E450` returns `022C31C0` only to `0032EA90`, which is in the module.
    - `0032E990` returns the popped slot only to `0032E870`, also in the module.
    - `0032E590`'s stale-id path returns with `rax = 022C31C0` (`0032E5A1` … `0032E5B7 jne` → `ret`). Its four external
      callers (`002FC426`, `003B13AF`, `003B17BD`, `003B199D`) never read `rax` after the call.
  - **Stores.** Every rip-relative store of a pointer lands inside the pool, list or gap range.

  So slot `+0` and `+0x50` have no reader outside the queue module, and no route by which one could get a slot pointer.
  This closes the page's stated limit.
- **Six asking sites (A0–A6)** ([ask_sites.py](ask_sites.py) / [.out](ask_sites.out),
  [ask_34db30_tail.out](ask_34db30_tail.out)):
  - `0032E520` has 27 sites (E8/E9) and no relocated pointer. `ecx` is 1 at `0022B73C`, `0022B83C`, `0031460E`,
    `0050E1E9`, `lea ecx,[rax+1]` at the four `0032E4D0`-gated sites, `edi` at `0034DBD9` and `ebx` at `0050D131`. It
    is 0 at the rest.
  - `0034DB30` keeps `edi = 1` on every path that reaches `0034DBD7`. `xor edi,edi` at `0034DB98` returns.
  - `0050D0C0` keeps `ebx = 1` through `0050D12F`. `0050D14E xor ebx,ebx` comes after the ask.
- **Gap (G1).** It is referenced only by the qword stores at `022C51E0` (`0032EAA7`, `0032EAE0`). Nothing touches
  `022C51E8`. `0032EAE0`'s only caller is `0022A3D5`, which is in the boot hub `0022A0B0`.
- **Section addressing (C1, F1)** ([sec_rederive.py](sec_rederive.py) / [.out](sec_rederive.out)):
  - `002ED570` has 115 sites (111 E8, 4 E9) in 87 owners: 85 `.pdata` roots plus 3 leaf-gap sites in 2 gaps. So 87 is
    exact.
  - `004096C0` has a null test and a `cmp ebx,-1`, then `call 00409600`, then an unguarded `004096DF add eax,ebx` /
    `004096E1 cdqe`.

**Controls.**
- The bit-7 sweep's control is `0027F7DA`, and it is found. The sweep is sensitive to a writer on a different object:
  it isolated `0033A720`.
- The escape census has three controls: `0032E153` for D, `0032E0F1` → `0046E030` for X, and the jump-table
  displacement for P. Each is sensitive to its defect: a missed reader, a missed call and a missed image-base form.
- The one blind form, a register-held mask like `0024A710`'s, is named on the page.

**Citations checked.**
- **SECTION-10 acceptance.** `source-REVIEW-0929-FINAL-BATCH.md` §S69 says: reviews OV-28 and OV-44 SECTION-10
  `ACCEPT`; `run_review.py` Linux-gated and UNMEASURED; acceptance on byte-exact bodies plus a semantic re-read. That is
  what the page says.
  - The review was done by SWE2-AUDIT-SPEC on 2026-09-29, 17:10–17:25Z, per the board task. That is before this lane's
    FABLE-session window, so it is an independent dependency.
  - The durable copy was committed by the ratification `a95c664bf`, a FABLE-session executor. It is verbatim: its 546
    lines are the first 546 of the `work/` original, and S69 is identical.
- **Type store (the `0x50` / `0xC0` families).**
  - `types.tsv` declares `RenderResourceEntry 0x50`, `RenderResourceEntryBank 0x60`, `RenderStrideC0Element 0xC0` and
    `RenderModelInstance 0x260`, so T1 holds.
  - **The attribution is wrong.**
    - `aa3470a36` adds `RenderResourceEntryBank` (0x60), and `0cca6e0f0` only edits the `RenderStrideC0Bank` row.
      `RenderResourceEntry` (0x50) was declared at `8c13cfe3f` (OPUS, 2026-09-19).
    - `RenderStrideC0Element` was declared by OPUS at `4fee674b9` (2026-09-19). "FABLE 2026-09-26, J-4" is the date of
      the answer that read it from the type store.
    - Both citations name a neighbouring fact. Hence the narrowing below.
- **Other citations.** EW-6 and EO-3 are SUPERSEDED on the register, as `documented_rule` K reads them. The AUDIT-LOG
  live-read citation (`7593db615`) is a cited observation, marked `live`/OBSERVED in §10, and is not re-derived.
- **Not independently reviewed.** K1–K3 rely on SWE2-DATA's `kind7.py` (`1261e2044`, 2026-09-30T04:05Z). That is
  FABLE-session-window work, so I re-derived it above without that tool.

**Correction wording.**
1. **Required.** In `resource-section-addressing.md`, in the 2026-09-30 superseded note under "The `0x260` family is now
   declared", replace
   "`RenderResourceEntry` (OPUS, with `RenderResourceEntryBank` at `0x60`, `aa3470a36` / `0cca6e0f0`), and the `0xC0`
   family is `RenderStrideC0Element` (FABLE 2026-09-26, J-4, the box above)"
   with
   "`RenderResourceEntry` (declared by OPUS at `8c13cfe3f`, 2026-09-19; its bank `RenderResourceEntryBank`, `0x60`, at
   `aa3470a36`), and the `0xC0` family is `RenderStrideC0Element` (declared by OPUS at `4fee674b9`, 2026-09-19; read
   from the type store as J-4's answer by FABLE on 2026-09-26, the box above)".
2. **Required, also from this batch.** The two typed-list §10 rows that `acfaf396a` rewrote have five cells in a
   four-column table, and "live" is not a tier. The exact replacement rows are in
   [the restatus review](../auditspec-review-dd-02-restatus-0930/REVIEW.md), correction 1.
3. **Optional.**
   - On `the-resource-request-queue.md`, the "Limit: the module's direct calls out … are not machine-checked" can now
     cite this record: "checked in `_index/candidates/auditspec-review-ddres-b6-0930/queue_escape.py` (no direct call,
     return or store passes a slot pointer out of the module)".
   - On the typed-list §5d answer, "until message 18 sets it again" can add "(the fullscreen proc's arm at `0027F7DA`,
     or the config screen's `00281E00`; `00280DE0` and `002D70F0` also clear some of the five)".
