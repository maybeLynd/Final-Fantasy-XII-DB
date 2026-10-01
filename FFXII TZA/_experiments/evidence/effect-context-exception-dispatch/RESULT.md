# Effect-context local exception-dispatch boundary

Producer-checked Method A result; independent acceptance and OPUS canonical
consumption are pending. No game session or machine-code execution occurred.

## Question and result

Does the local exception metadata for the three already-proven call
continuations in `003B3CA0` name a language handler that could clean up a
temporarily published effect context on abnormal exit? H1 names a handler;
H2 ends at a handler-free chained root.

The shipping image supports H2 for precisely these continuations:

| Original call | Target | Continuation |
|---|---|---|
| `003B3CE0` | `0024ED80` | `003B3CE5` |
| `003B3CE7` | `003A9490` | `003B3CEC` |
| `003B3CFD` | `0024ED80` | `003B3D02` |

All three select the directory record with RVA interval `00293CC8..00293D0C`
and unwind VA `01D7F124`. Its version-1 CHAININFO record contains
`211104001174070005340600a03c2900c83c290080f3c601`, pointing to the record
with RVA interval `00293CA0..00293CC8` and unwind VA `01D8F380`. That root's
raw bytes are `0106020006320260`: version 1, flags 0, two code slots,
and no language-handler field. These intervals are metadata selection
facts; they are **not evidence of normal function extents**.

## Original identity and controls

Reference EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
image base `00120000`. The prior `heading-list-identity` manifest pins the
normal 114-byte instruction body to
`ddc1c159ea5183895a6eb5cc7592a0b999823feff36dbed5ed11636b969bf869`.
The three E8 instruction bytes and targets are independently checked against
that image. No normal call identities are inferred from exception metadata.

The focused decoder verifies raw-backed spans, flags/version, padded code
slots, chain bounds/cycles and a finite eight-record budget. The pinned
pefile decoder supplies PE section mapping; its exception-directory entries,
selected headers and complete chained triple agree with the explicit byte
decoder. This is a cross-check, not two entirely independent PE loaders.

The actual shipping entry beginning at VA `00121F40` is the positive control:
both readers identify flags 3 and handler VA `00808BA8`. A **private,
non-shipping** copy of the selected chain redirected to this entry produces
that handler instead of the no-handler result. A private self-cycle is
refused. Raw records, source/driver hashes and normalized observations are
in `result.json`; `terminal.json` records the checked invocation exit 0.
The final run adds full chained-triple/header cross-checks to the development
probe. It is the frozen receipt, not an extra gameplay sample.

Reproduce from repository root with:

```powershell
& 'Collaboration/Tools/analysis/venv/Scripts/python.exe' 'Database/FFXII TZA/_experiments/evidence/effect-context-exception-dispatch/check.py'
```

## Meaning, limits and consumers

This local metadata does not name a language handler at the selected
continuations. It cannot support a claim that this caller has a local
metadata-dispatched restoration handler there. It also cannot establish
that the global remains unrestored: outer handlers, callee behavior,
other code and actual exception occurrence remain unmeasured.

The FINAL-AUDIT-PROTOCOL pass-6 ruling dated 2026-09-16 admits claims about
the dispatcher mechanism, while banning metadata as proof of what the
normal program executes. FABLE must independently review this boundary;
OPUS owns effect-context/ABI contract incorporation after acceptance.
The prior normal-path publication/restore evidence stays valid separately.
Initialized object identity, lifetime/reuse, scheduling, class effects,
normal gameplay reachability and presentation remain OPEN. This package
does not close CON-172 or UQ-207 and supplies no live-default guarantee.

The reference hash is unchanged after capture. No FF12 launch, control,
attachment, save/config write or experimental reference modification was
performed. Private mutation bytes exist only in Python memory. All invoked
checks are terminal. No full audit/mutation campaign or L1/L2 award.

Player version: the nearby exception records do not name a local recovery
handler for this effect operation. That narrows where recovery could happen;
it does not prove a crash or an unrecovered effect during actual play.
