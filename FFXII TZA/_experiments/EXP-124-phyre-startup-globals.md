---
experiment: EXP-124
title: Phyre default buffers and parent descriptors at the ordinary title menu
status: PARTIAL
contract: ../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md
tool: evidence/phyre-startup-globals/observe.py
method: C - ordinary startup and read-only process observation
live_game: true
evidence_class: original-process-observation
execution_scope: One verified FF12 process at title; no save load, debugger, memory writes or native calls
contract_coverage: Sampled registered defaults and parent links; initialization timing, four descriptor mappings and seven unprepared defaults remain open
date_designed: 2026-09-19
date_run: 2026-09-19
---

# EXP-124 — prepared defaults, unprepared zeros, and a root descriptor

The requested 173 default-buffer spans were captured from the actual game at its
title menu. They contain **34,392 bytes**. Each passed the supplied class-name,
instance-size and registered `+C0` pointer controls. These are sampled values;
the native object-copy operation was not executed or traced by this experiment.

| Observation | Classes |
|---|---:|
| Preparation flag `+FC` bit31 set | 166 |
| Bit31 clear; buffer entirely zero | 7 |
| Nonzero buffer | 140 |
| Bit31 set; buffer entirely zero | 26 |
| Entire buffer is `A5`, with bit31 and bit1 set | 7 |

The seven unprepared classes are `POccluderGeometryInstance`,
`POccluderGeometryObject`, `PQuarryComponent`, `PScriptableComponent`, `PTrigger`,
`PTriggerReceiverComponent` and `PTriggerReceiverTypeCallbackData`. Their initialized
default values remain unknown. A zero value sampled before preparation cannot
be substituted for the eventual default. The meaning of the preparation flag
comes from OPUS's original-code analysis; this experiment observes its value and
does not trace the write that set it.

The seven all-`A5` buffers belong to `PAnimationDataSource`, `PCameraProjection`,
`PDynamicMesh`, `PInputSource`, `PParameterBufferBase`, `PPhysicsShapeBase` and
`PRenderTargetBase`. This agrees with the documented bit1-gated poison-fill arm,
but is not a trace of that arm or proof that a normal allocation copies these
classes. Bit31 alone must not be read as a guarantee of a usable zero default.

## Parent links and the mapping failure

All 70 explicitly populated static parent addresses match the live `+78` reads.
The other 103 requested classes point to `02CF8270`, whose observed name is
**`PBase`**, size is zero and parent pointer is null. The pinned static table leaves
these parent-address cells empty and calls them root/no-parent. That convention
must not be interpreted as a sampled null pointer. Seven additional ancestor
descriptors were read, producing an acyclic 180-node observed graph; no observed
parent size exceeds its child's. A parent link is not a subobject offset, a full
ownership proof or an answer for every abstract type.

The original 177-sized-class attempt **failed its first identity control**.
The supplied address `02CF6678` for `CD3D11_BLEND_DESC` yields `0x10` at the expected
name-pointer offset `+30`; reading it fails. The complete raw header and failure
are preserved in [title-full.json](evidence/phyre-startup-globals/title-full.json).
No class from that invalid attempt contributes to the successful census.

The observation was revised explicitly to the 173 default-buffer request, whose
three-class pilot had passed. The four non-default rows remain unresolved:
`CD3D11_BLEND_DESC`, `CD3D11_DEPTH_STENCIL_DESC`, `CD3D11_RASTERIZER_DESC` and
`D3D11_RENDER_TARGET_BLEND_DESC`. Only the first was attempted; the other three
were not observed. OPUS must reconcile their mappings/layouts before another
hierarchy capture. These are open coverage gaps, not removed database scope.

## Method, reference and controls

The design and revision are in the [evidence README](evidence/phyre-startup-globals/README.md)
and [scope revision](evidence/phyre-startup-globals/scope-revision.json). Static
evidence explains construction recipes but cannot provide the current contents
or determine which lazy preparations occurred. No isolated-code run was needed.

PID **34568** was launched from the designated Steam installation, executable
SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, base
`00120000`. The full 7,996,981-byte mapped `.text` matched before and after each
successful capture, SHA256
`5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`.
The 102-module path inventory was unchanged across the successful capture.
This records loaded names and main-image bytes; it does not certify every DLL,
IAT entry or heap byte. Tool source hashes and pinned target-table bytes are retained.

The existing `runtime_probe` query/read path returned the nonzero LUAC control
`19930d0a1a0a` at `01CCD300` before/after and rejected address zero. Full-length
reads are required; failed reads are not zero-filled. No debugger was present.
The three-class pilot matched names, sizes, pointers and prepared nonzero buffers.
Every one of the 173 successful header brackets matched; the entire census lasted
about 0.225 seconds. Calls are sequential, not an atomic snapshot, and equal
brackets cannot exclude an intervening write. Buffer contents were read once
per class in the census; the three pilot classes also have earlier samples.

The first sandboxed attempt could not enumerate modules and stopped before any
class read. It remains INVALID in [title-pilot.json](evidence/phyre-startup-globals/title-pilot.json).
The same read-only observer succeeded with the permitted process-query access;
this is not evidence of a game-state change. The pre-scope observer is preserved
so both earlier hashes remain reproducible.

## Raw evidence, interpretation and cleanup

- [Successful raw census](evidence/phyre-startup-globals/title-defaults.json):
  ordered reads, timestamps, identities, controls, descriptors and ancestor bytes.
- [Normalized spans](evidence/phyre-startup-globals/defaults.tsv) and
  [concatenated bytes](evidence/phyre-startup-globals/defaults.bin): exact offsets
  and hashes for OPUS's per-field interpretation. Runtime pointers inside the
  buffers remain process-specific observed bytes, not portable literal defaults.
- [Offline reconciliation](evidence/phyre-startup-globals/review.json), generated
  by [review.py](evidence/phyre-startup-globals/review.py), re-derives names, fields,
  bytes and links from raw reads and preserves invalid runs outside the census.
- [Title before](evidence/phyre-startup-globals/title-before.jpg) and
  [title after](evidence/phyre-startup-globals/title-after.jpg) prove visible state.
  No save was loaded or combat command issued. Screenshots do not establish
  internal semantics or continuous responsiveness.
- [Cleanup](evidence/phyre-startup-globals/cleanup.json): all query/read handles
  closed; ordinary Alt+F4 produced an exit dialog. An indexed click was rejected
  by the UI cache; re-observation and Return accepted the default OK action, then
  process exit was verified. No force termination. PC control was reset afterward.
  All 26 originals and backup hashes match; the sole `LUIDLow` change was preserved
  and restored, and the reference executable was rehashed. Steam Cloud was visibly
  off before launch and was not changed.

Affected consumers are OPUS's Phyre class/default-buffer maps, class-descriptor
contract and gap-value rows. Integration and independent review are pending;
this record does not close seven unprepared defaults, four unresolved mappings,
native copy reachability or the full database goal.

Player version: the engine has real starting values beyond zeros. Some classes
had not prepared those values yet at the title screen. The game is closed and
your saves/settings are restored while the team checks how these bytes fit the
database's object definitions.
