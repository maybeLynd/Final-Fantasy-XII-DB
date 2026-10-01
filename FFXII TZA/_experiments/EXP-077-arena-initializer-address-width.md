---
experiment: EXP-077
title: Original arena initializer retains high backing addresses
status: COMPLETE
contract: ../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md
tool: evidence/resource-arena-backing/initializer_probe.py
method: B - isolated original-code execution
live_game: false
date_designed: 2026-09-12
date_run: 2026-09-12
---

# EXP-077 — initialization does not impose a low-address ceiling

**Result:** six original controls passed on first execution; one private pointer
truncation mutant was detected. ASTRA, 2026-09-12. These are isolated original-code
executions with one explicit no-write formatter stub. No game process, native
CRT allocator, boot sequence or later allocation operation was executed.

## Question and reference boundary

The [resource lifetime evidence](../02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md)
establishes an arena layer in the resource loader. Its boot backing comes through
an imported `malloc` path. Does the original initializer reject or truncate a
backing pointer above 2 GiB or 4 GiB? This experiment resolves that narrow point,
not the address placement of a running game or the safety of subsequent links.

The checker verifies EXE SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base
`00120000`, and extracts the following complete original bodies:

| Entry | Bytes | SHA-256 |
|---|---:|---|
| `00369D30` initializer | 707 | `16466da32c47e02ad79cf15b1952c26a44d66eecfb4fb0a269fb74fa85ca5beb` |
| `0036A490` initial block-header writer | 215 | `4eb5360d3d81b7710459f22743602534e00d028a0ea6edda3f52510a539da830` |
| `0020E620` pointer encoder | 9 | `9f88dce71d7cce301096aa6ab93885acc0103d2d044dbfad741262336cffd7d7` |

The only substituted target is `0017D2E0`, currently identified as `sprintf`.
Its stub records the four register arguments, returns zero, writes no memory,
and clobbers every volatile general register and the full XMM0–5 registers.
Native formatting effects are **not** evidence from this probe. Original code
executes the header writer and its nine encoder calls; their results are not
substituted. All nine encoder inputs are zero in these fixtures.

## Initialized state and controls

Every run starts in a fresh Unicorn 2.1.4 instance. The entire arena-global region
`022D7000..022D8FFF` is zero, the qword decoder base at `01F83530` is zero, and
one MiB of backing storage is filled with `A5`. The checker rereads these initial
bytes and records their hashes before execution. Stack memory is mapped at
`60000000..60002FFF`; entry RSP is `60001808`, with return sentinel `70000000`.
DF is clear, EFLAGS is 2 and MXCSR is `1F80`. Eight nonvolatile general registers
and the full 128 bits of XMM6–15 receive distinct initialized values.

Arguments are `ECX=id`, `RDX=backing`, `R8D=0x100000`, `R9D=16`. All addresses
below are hexadecimal. Each valid control has a mapped, writable high or low
backing region; the high case is not a test against missing input memory.

| Control | Backing address | Id | Observed original result |
|---|---|---:|---|
| Low positive control | `40010000` | 2 | Returned; full pointer layout retained |
| Above 2 GiB | `80010000` | 2 | Returned; full pointer layout retained |
| Above 4 GiB | `100010000` | 2 | Returned; full pointer layout retained |
| Last valid id | `40010000` | 14 | Returned; corresponding arena record initialized |
| First invalid id | `40010000` | 15 | Returned without calls or non-stack writes |
| Negative id | `40010000` | -1 | Returned without calls or non-stack writes |

Valid runs restore the stack and every initialized nonvolatile register, leave
the decoder base unchanged, make one formatter call with `(P, format, id, P)`,
and then make nine original encoder calls with zero. Invalid ids take the
unsigned `id > 14` rejection to the original epilogue in 17 instructions. Their
entire initialized global and backing fixtures remain unchanged. No meaning is
assigned to a return register on this void-like path.

## Observed layout and mutation

For these aligned one-MiB fixtures, record `022D7FD0 + id*0xA8` contains:

| Qword field | Exact expected and observed value |
|---|---|
| `+08` | `P` |
| `+20` | `P+40` |
| `+28` | `P+80` |
| `+30`, `+40` | `P+180` |
| `+38`, `+90`, `+98` | `P+280` |

These fields are checked individually. The initial free-block header is at
`P+280`, starts with word `FF12`, and contains dword payload length `FFD40` at
`+18`. Record `+5C` is `FFD80`. Every non-stack write is constrained to the mapped
global region or the first `2C0` bytes of backing. The raw receipt includes all
191 such writes per valid run, the final complete `A8`-byte arena record, the
first `2C0` backing bytes, every visited instruction and every call. Unwritten
padding retains its initialization bytes; this is not a blanket zero-fill claim.

The private mutant changes only `00369D44` from bytes `4C 8B F2`
(`mov r14,rdx`) to `44 8B F2` (`mov r14d,edx`). With backing `100010000`, it stores
`10000` in record `+08`, then faults at `00369E4C` on the first backing write to
unmapped `10000`. The unmodified high-address control had already returned with
the expected layout. This establishes a meaningful detection of pointer
truncation. Mutant stack/nonvolatile checks fail because execution faults before
the epilogue; those failures are not counted as original controls.

## Evidence, cleanup and remaining obligations

The [sealed raw result](evidence/resource-arena-backing/initializer-result.json),
[checker source](evidence/resource-arena-backing/initializer_probe.py),
[static instruction receipt](evidence/resource-arena-backing/primary.json) and
[manifest](evidence/resource-arena-backing/manifest.json) preserve the run. The
[lossless review helper](evidence/resource-arena-backing/review_results.py) prints
the full first case and every differing leaf of all remaining cases, including
complete arrays when their length changes. All results and source were reviewed;
sealing did not rerun the experiment. The source retains its original repo-relative
scratch output path `Database/Tools/work/ASTRA/arena-init-result.json`; the sealed
copy is immutable evidence, not the output target for a later reproduction.

Emulation instances ended with the checker process. No live process, save,
configuration, allocator hook or shared native laboratory was changed.

This disproves an initializer-level low-address rejection for the tested inputs.
It does not establish native formatter effects, arbitrary sizes/counts, exhaustion,
reclamation, selector remapping, or later allocator safety. Size computations and
encoded links elsewhere still use 32-bit arithmetic. Zero decoder base is an
explicit fixture value, not a new process-lifetime observation. Contract/type and
semantic consumer review is routed to OPUS/FABLE; citation or a completed local
experiment does not close those consumers or the L1/L2 database goal.
