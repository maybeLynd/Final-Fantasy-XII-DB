# Consumer check: 22-Phyre contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-22-VALUES-1002. Cloud wave 4 mapped `22-Middleware-PhyreEngine/` from a text snapshot
(session `session_01NqcVVFsta7oaQ6z4swFnL2`; report `cloud-reports/re-readiness/22-phyre.md` in
maybeLynd/Final-Fantasy-XII-DB, ce22721b; rated NOT YET). Its 101 value items were page-text only. A local read-only
pass decided them at the shipping image or the generated data; two cannot be decided statically. OPUS re-checked the
deciding instructions (`phyre_check.py`).

What the bytes show:
- Slot 7 runs before slot 4 (`0079C26B`, then `0079C2D6`).
- The flag clear is an AND-mask (`003A20B0`).
- The offset test is `offset >= 4` on `r9w` (`001E3619`).
- Descriptor `+0xF4` is the running sum of `+0xF0` up the parent chain, not zero (`0063E43B`).
- `PFXAA` is built in code (`0018CFD5`).
- The slot-4 tick returns 0 or 9 (`0017CDB2`).
- `006388C0` returns a bool (`006389A1`).
- The descriptor destructor stamps `PClassDescriptor`, then `PType` (`006333BC`, `00633568`).
- `00617810` registers `PShaderComputeProgramD3D11`; it is not a digit slip for `00167810`.

The pass drafted 181 strike edits (`apply_22phyre.py`). OPUS applies the 86 on its own lines across 14 pages
(`apply_by_owner.py OPUS`). The rest go to their owners as requests:
- 70 to SWE2-EC7. The frame page should wait for SWE2-AUDIT-SPEC's ACTIVE OPUS-REQ-AUDITSPEC-TWOFRAMES-INTERIOR-1001.
- 18 to FABLE.
- 5 to SWE2-DATA, which also gets two type-row notes for `PhyreClassDescriptor` `+0xC8`/`+0xD0` (byte masks) and
  `+0xF4`/`+0xF8` (running sums).
- 1 to FRONTIER.
- 1 to SWE2-CONTRACT.

- **Affected:** 22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md, 22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md, 22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md, 22-Middleware-PhyreEngine/Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md, 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md, 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md, 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md, 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md, 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/phyre-class-instance-sizes-and-alignments.md, 22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md, 22-Middleware-PhyreEngine/Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md, 22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md, 22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md, 22-Middleware-PhyreEngine/the-camera-state-snapshot.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the fourteen OPUS-led and shared 22 pages (OPUS lines) | revised-here |
  | EC7's application, header, post-frame and frame pages and its lines | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 70 edits; the frame page after SPEC's TWOFRAMES audit) |
  | the README, the post-effect page and FABLE's lines | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 18 edits) |
  | DATA's lines and the two `PhyreClassDescriptor` type rows | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 5 edits, plus the type-row notes) |
  | FRONTIER's and SWE2-CONTRACT's lines | routed-to-SWE2-FRONTIER and routed-to-SWE2-CONTRACT (1 edit each) |
  | RE repo `docs/readiness/22-phyre.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-phyre-readiness-fixes-1002/phyre_check.py, verified at 31f29775a: 10 instructions decode as cited, FAILS 0 ([`phyre_check.out`](phyre_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (86), FAILS 0.
