# SWE2-AUDIT-SPEC review of SD-67 (sd67-stream-bindings-type-0930 at aac0f6798): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Reviewed: OPUS's
`aac0f6798` (the record's only commit), [README](../sd67-stream-bindings-type-0930/README.md) and
`sd67_stream_bindings.py`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD67-0930 | sd67-stream-bindings-type-0930 | `aac0f6798` | ACCEPT |

**Re-run.** [rerun_sd67_stream_bindings.out](rerun_sd67_stream_bindings.out) is identical to the committed `.out`
(ignoring CR), F1-F3 PASS, `FAILS 0`. The record directory stayed clean.

**Re-derived independently** ([sd67_rederive.py](sd67_rederive.py) / [.out](sd67_rederive.out)).
- **One registration.** The file holds exactly one NUL-terminated copy of the name `m_streamBindings`, and the
  substring `streamBindings` occurs once. Its string at `00D4A1C0` has 1 rip reference across ALL `.text`
  (`005E6848` in `005E67C0`) and no stored pointer. So the registration is unique, not only unique within listed code.
- **Argument mapping into `00632A10`, re-derived from the frame.** The prologue is `push rdi; sub rsp, 0x40`, a 0x48
  frame, so the caller's stack arguments at `+0x20/+0x28/+0x30/+0x38` arrive at `+0x70/+0x78/+0x80/+0x88`.
  - The caller stores 0x38, 0, 4 and 8 there (`005E6840`/`005E6838`/`005E6830`/`005E6828`).
  - `[rsp+0x80]` (the 4) goes through `ebx` to `+0x5C` (`00632A4D`).
  - `[rsp+0x88]` (the 8) goes to `+0x58` (`00632A5F`).

  So the kind is 4 and the element size is 8, in the field order F2 states. The checker matches these as literal
  operand text; I verified the frame arithmetic behind them.
- **Width 16.** In `005EFE60`, `r15` is set once (`xor r15d, r15d` at `005EFE9E`) before the `00632D80` call, so
  `lea r9d, [r15+0x10]` passes 0x10. `00632D80` is frameless and stores `r9d` at `+0x38` and its 5th argument
  (`[rsp+0x28]` = 8) at `+0x3C`. That gives descriptor size 0x10 and alignment 8.
- **Descriptor and vtable.** The vtable (`lea` resolving to `00D4DD98`) is stored at `005EFF10` into `02CEC990`, the
  static descriptor.
- **RTTI.** My own locator walk (signature 1) gives
  `.?AV?$PClassDescriptorAbstract@V?$PSharray@PEBVPMeshInstanceSegmentStreamBinding@PRendering@Phyre@@@Phyre@@@Phyre@@`
  for `00D4DD98` and `.?AVPClassDataMemberArray@Phyre@@` for `00D58100`. `PEBV` = pointer (64-bit) to const class,
  so the elements are 8-byte pointers, consistent with the element size 8.

**Controls.** F1-F3 are literal-operand matches at fixed addresses. They are sensitive to a different argument value
or field, but they would not see a second registration elsewhere. My string-copy count and whole-image rip sweep rule
that out.

**Stated limit** (the internal layout of the 16-byte PSharray) is correctly left open. The kind-4 = PSharray mapping
rests on UQ-281 and was not re-reviewed here.

**Correction wording:** none needed.
