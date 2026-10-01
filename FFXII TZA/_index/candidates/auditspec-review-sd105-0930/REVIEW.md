# SWE2-AUDIT-SPEC review of SD-105 (sd105-reveal-inputs-0930, OPUS, f2f55938a): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `f2f55938a` (the record's only commit), [README](../sd105-reveal-inputs-0930/README.md) and `sd105_inputs.py`,
measured at HEAD `b58c633f7`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD105-0930 | sd105-reveal-inputs-0930 | `f2f55938a` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_sd105_inputs_b58c633f7.out](rerun_sd105_inputs_b58c633f7.out) is identical to the committed `.out`
(CR ignored), V1-V4 PASS, `FAILS 0`. The earlier worker's [rerun_sd105_inputs.out](rerun_sd105_inputs.out) was identical
too. Package dir clean after re-run: yes.

**Re-derived independently** (lane `b8dis.py` / `ov31_indep.py`; [sd105_census.py](sd105_census.py) / [.out](sd105_census.out),
[basefill_dis.out](basefill_dis.out), [af960_dis.out](af960_dis.out), [nested_dis.out](nested_dis.out),
[b43c0_dis.out](b43c0_dis.out), and the parser dump `../auditspec-review-sd100-0930/parser_dis.out`).
- **V1 / V3.**
  - `002AC1E0` clears 0xD0 bytes (`002AC1E8`, `002AC1F1` = `memset`), so it leaves `+0x50` = 0.0. It then sets `+0x9E` = 8
    (`002AC232`), and also the speed `+0x9C` = 0x1E and the step `+0xA0` = 1.
  - `002B32D0` calls it (`002B32F0`) before either builder. Both builder paths reach `002B33B1` with no return in
    between: `002B3354` → `002B3382 jmp` / `002B3377 je`, and `002B3384` → fall-through / `002B33A5 je`. So V3 holds on
    every path, not only in address order.
- **The `+0x50` / `+0x90` / `+0x9E` writer census** (linear decode of all 336 `.pdata` ranges rooted in
  `0029E000`..`002B6000`, so disp8 forms are seen; controls `002B33F0`, `002A48C5`, `002B33DC`, `002B3CF8`, `002B3DB4`
  and `002AC232` all PASS).
  - **A second computed writer of `+0x50`.** The markup parser's `"` tag (`0F 22`) handler in `002A8C50`, at `002A9442
    cmp al, 0x22`:
    - `002A944A lea r8, [rsi+0x9e]` and `002A9456 call 003FFEE0` set **`+0x9E` = tag byte 2 & 0x1F** (`003FFEF2`..`003FFEF8`).
    - `002A945B`..`002A947A` then store **`+0x50` = 1.0 / (s8)`+0x9E`**. `xmm6` is 1.0 from `002A8D54`.
    - When the tag sits at text position 0 (`002A94AB test r14d, r14d`), it also sets `+0x9D` = 0 and **`+0x90` =
      −(s8)`+0x9E`** (`002A94B4`..`002A94C1`). `r13d` is 0 from `002A8C87`.
  - The other `+0x50` writes in the cluster are whole-element `movups` copies, 33 of them (`002A48C5` among them), plus
    unrelated structures. Examples: `0029F130`'s word stores are a type-7 node, and `002A9F00` / `002AAE40` write at
    `rbp` frame offsets.
- **`002AF960`** stores `+0x10D8` = `+0x8C`, `+0x10DC` = `+0x90` and `+0x10E4` = (s8)`+0x9D` x `+0x50`
  (`002AFB05`..`002AFB4C`). The two statements the README makes without a checker line hold.
- **V4, `[rbp−0x70]`.** It is not built by a builder. `002AD495`..`002AD52E` copies the 0xD0-byte current element `r14`
  into it. `002B43C0` is then called on the copy with the inserted text, NUL-terminated in place (`002AD548`..`002AD555`),
  and its `ax` goes to `[rbp+0x1C]` = the copy's `+0x8C` (`002AD569`).
  - `002B43C0` copies the element to its stack twice, sets the copy's `+0x8C` to `strlen(text)` (`002B446D`..`002B447A`),
    installs a one-byte stop string {`r8b`, 0} at `[0209CC40]+0x10C8` (`002B43D3`, `002B43DB`, `002B4466`; `r8b` = 0 at
    both `002AC5F0` calls), and returns `002AF340`'s `eax` (`002B451B`..`002B4536`).
  - SWE2-DATA's page §4 reads that value as the characters laid out plus the token counts. So "the nested run's count" is
    supported statically, conditioned on that reading. I did not trace how the empty stop string behaves.
  - The scaling and the min are as stated (`002AD653`..`002AD6CD`).
- **Direct builder calls (a stated limit).** `002A1B00` fills its element `[rsp+0x40]` with a 0xD0-byte copy of the
  element at `r14` (`002A1B34`..`002A1BCB`) before `002B3C30` (`002A1C86`). Its `+0x50` is therefore the source
  element's value. `002A3250`'s `rdi` element was not traced.

**Controls.**
- **Defect found in my own instrument.** capstone 5.0.7 marks the memory destination of `movups` (and of `movq`, `movlps`
  and `movhps`) as READ. `movaps` / `movdqu` / `movss` / `movsd` are marked WRITE. A census filtered on `CS_AC_WRITE`
  silently drops every `movups` store. The positive control `002A48C5` failed first
  ([sd105_census_v1-capstone-movups-blind.out](sd105_census_v1-capstone-movups-blind.out)). All four of this session's
  censuses now also treat a mov-family instruction with a memory first operand as a store, and were re-run. SD-100's
  cluster result did not change, but its image-wide `+0xB0` write count went from 861 to 931.
- The `"` tag writer is outside the builders the README names. The census found it only because it decodes the parser
  body linearly, which a builder-only reading does not.

**Citations checked.** V1-V4 lines open to the instructions stated. V4's "a text element built on the frame" is a copy,
not a build. See the wording below.

**Runtime routing.** None needed. Whether shipped text uses the `"` tag, and with which bound, is a data question: the
`0F 22` byte pair in the text files. It is not a runtime one, and it was not checked here.

**Correction wording (the producer applies).**
1. V2: *"`+0x50` = 1.0 / (s8)`+0x9E`. Two code paths compute it: the wrapper `002B32D0` (`002B33F0`, after the base
   fill's `+0x9E` = 8, so 0.125), and the markup parser's `"` tag (`0F 22`) in `002A8C50`. That tag first sets `+0x9E`
   to its second payload byte & 0x1F (`003FFEE0` at `002A9456`), then stores `+0x50` (`002A947A`). At text position 0
   it also sets `+0x90` = −(s8)`+0x9E` and `+0x9D` = 0 (`002A94B4`..`002A94C1`). Element copies (`002A4830` and others)
   carry `+0x50` across unchanged."*
2. V4, first sub-bullet: *"`[rbp−0x70]` is a 0xD0-byte copy of the current element `r14` (`002AD495`..`002AD52E`), made
   for a nested run (the argument insertion). So `[rbp+0x1C]` is the copy's `+0x8C`."* Second sub-bullet: *"`002AD569`
   stores `002B43C0`'s result there. `002B43C0` lays the text out on a copy whose head `+0x8C` is `strlen(text)`, and
   returns `002AF340`'s character count (the SWE2-DATA page §4 reading)."*
3. Limits:
   - Replace "Authored overrides ... not checked" with *"**Authored overrides.** The `"` tag (`0F 22`) sets `+0x9E` per
     text (0-31). Whether shipped text uses it is not checked."*
   - In "Direct builder calls" add *"`002A1B00`'s element is a copy of the element at `r14` (`002A1B34`..`002A1BCB`), so
     it carries that element's `+0x50`. `002A3250`'s is not traced."*
