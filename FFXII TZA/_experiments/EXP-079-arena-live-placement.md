---
experiment: EXP-079
title: Live arena placement at title and after loading The Stepping
status: COMPLETE
contract: ../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md
tool: evidence/arena-live-placement/review_capture.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-12
date_run: 2026-09-12
---

# EXP-079 — sampled live placement and an enabled-arena exception

**Result:** one actual FF12 process was observed at its title menu and after
ordinary loading of The Stepping. Every enabled record's backing pointer was
below 2 GiB in both samples of each state. Base was zero and the map was the
identity map. Loading enabled arena 14 and changed arena 11's backing pointer.
Arena 7 was enabled but its sampled purported headers were all zero. These are
bounded live observations, not proof of a general allocator invariant or lifetime.

## Claim, method and reference

The existing task recorded competing hypotheses before setup: actual backings
fit the observed decoder window, or some do not. EXP-077/078 already establish
initializer width and consecutive-allocation consequences in supplied isolated
states. Neither can establish shipping-game placement. Method C was necessary
for this observation; an ordinary launch/load and read-only existing probe were
sufficient. No debugger, native call, hook, emulator or reconstruction ran here.
No allocation experiment was repeated to increase a live-test count.

The designated process was PID `38032`, launched from the verified Steam
`x64/FFXII_TZA.exe` with SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Its observed image base was `00120000`. Before each state's arena reads, all
7,996,981 bytes of the disk `.text` virtual extent at `00121000` matched live
memory, SHA-256
`5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`.
The [environment receipt](evidence/arena-live-placement/environment.json) records
the selected reference installation and leaves the separately modded clients alone.

Both [title](evidence/arena-live-placement/title-memory.json) and
[loaded](evidence/arena-live-placement/loaded-memory.json) receipts retain the
complete 101-module inventory, identical between these observations. It includes
Steam's overlay, Windows, NVIDIA and Defender modules. The tool's `clean` label
means its watched-name check passed; it is not proof that every DLL, IAT slot or
heap byte is pristine. No instrument was deployed or attached by ASTRA.

The wrapper [observe.py](evidence/arena-live-placement/observe.py) imports the
existing `runtime_probe.py` and `ffxii_runtime.py`, preserving their source hashes
in each capture. It sets pointer-sized Windows handle signatures locally and
opens query/read access only. The nonzero `LUAC_TAIL` control at `01CCD300`
returned `19930d0a1a0a`; an address-zero read returned failure, not fabricated
zero bytes. The reader rejects short reads. Both read handles closed successfully.

## Actual trigger, initialized state and observations

Screenshots bracket each memory capture. The title menu visibly selected Load
Game. A single Return produced no visible menu transition; the later mouse
confirm did. The selected autosave visibly identified **Dalmasca Estersand /
The Stepping**, play time `000:08:42`, level 1, gil 150. Its ordinary load reached
the visible Load Complete screen and then Vaan in the area with HP `103/103`,
MP `33`. No injected initializer or manufactured process state supplied this
sequence. Mouse confirmation is recorded as accepted input, without claiming a
particular menu hit-test implementation.

Primary visual records: [title before](evidence/arena-live-placement/title-before.jpg),
[title after](evidence/arena-live-placement/title-after.jpg),
[selected save](evidence/arena-live-placement/selected-save.jpg),
[load complete](evidence/arena-live-placement/load-complete.jpg),
[loaded before](evidence/arena-live-placement/loaded-before.jpg), and
[loaded after](evidence/arena-live-placement/loaded-after.jpg).
Screenshot sidecars record receipt time, not a hardware-synchronized exposure.
Window size changed during the session without an attributed cause; it is not
used as evidence of a specific initialization event or continuous UI control.

Each state has two samples separated by approximately 0.25 seconds. Each sample
reads base `01F83530`, selector/map bytes at `022D89A8`, all fifteen `A8`-byte
records at `022D7FD0`, then 64 bytes at each nonzero enabled-record pointer in
`+08/+38/+90/+98`. Base and selector are reread afterward. Their bracketing bytes
agree; the two complete arena-record arrays also agree within each state.
These sequential calls are **not an atomic snapshot** and do not prove every
instant or the lifetime of a decoded target.

| Record | Title backing `+08` | Loaded backing `+08` |
|---:|---|---|
| 2 | `6CC90040` | `6CC90040` |
| 3 | `6EA67040` | `6EA67040` |
| 4 | `65F60040` | `65F60040` |
| 5 | `66079040` | `66079040` |
| 6 | `6F798040` | `6F798040` |
| 7 | `763A0040` | `763A0040` |
| 8 | `793B2040` | `793B2040` |
| 9 | `7B3CA040` | `7B3CA040` |
| 11 | `7C5D3040` | `7C5D2040` |
| 13 | `66127F80` | `66127F80` |
| 14 | Disabled | `6610EF40` |

The mask changes from `2BFC` to `6BFC`; selected arena remains 2, base remains
zero, and the fifteen map bytes remain `0..14` in all four samples. Arena 11's
backing change is consistent with the statically known replacement path in
`0037B3D0`, but no call trace identifies that path as the cause here. Free,
allocation, ownership and reuse order remain open. High-address faults in
EXP-078 remain isolated-fixture results; no such fault was observed live here.

All 154 requested 64-byte spans returned full data (37 per title sample, 40 per
loaded sample). At the sampled nonzero `+38/+90/+98` pointers, arenas other than
7 have an `FF12` word and matching arena-id byte. Their captured four 32-bit
link fields fit below 2 GiB; under the observed zero base, nonzero references
retain their numeric addresses. Most link destinations were **not** read. This
does not validate list topology, ownership, reclamation or all decoder consumers.

**Arena 7 is a concrete exception to interpreting enabled records as currently
usable block allocators.** Its backing starts with `EFX0010\0`, rather than the
`TKMALLOC EXECSPACE=07/...` annotation. Its three nonzero fields `+38/+90/+98`
all point to `763A2940`; each corresponding 64-byte span is zero in both states
and both samples. Other arenas' nonzero headers, the known-byte control and
the rejected null read distinguish this from an observer silently zero-filling
failed reads. The capture does not identify who wrote these bytes or why. Keep
the arena's present use and overwrite/reset sequence open; the magic alone does
not establish resource ownership or an effects-system contract.

Arena 9 supplies another boundary: it is enabled while `+90/+98` are both null.
Zero-count nested records 13/14 have null `+30/+38/+40`; their nonzero `+90/+98`
still supplied headers. Do not apply EXP-077's count-16 `+38` relationship to
every zero-count initialized record.

## Cleanup, saved review and remaining obligations

Before launch, all 26 save/configuration files were hashed and copied to the
preserved original backup; source and backup matched. Steam Cloud was already
OFF, confirmed [before](evidence/arena-live-placement/cloud-before.jpg) and
[after](evidence/arena-live-placement/cloud-after.jpg); no cloud switch changed.
The active save tree was the disposable working copy. No movement or combat
command was issued. After read handles closed, one ordinary confirm opened the
[command menu](evidence/arena-live-placement/responsive-menu.jpg), providing
a responsiveness control without selecting/executing Attack.

Alt-F4 opened the normal Exit Dialog; the intermediate
[exit check](evidence/arena-live-placement/exit-check.json) correctly says the
process had not exited. A subsequent tool user-input detection halted controls.
Only the user's explicit **Resume exit and cleanup** reply resumed the pending
dialog confirmation. No automatic restart occurred.

The first cleanup attempt stopped before any write because the expected six
changed display keys no longer matched the post-exit file. Inspection showed
five had reverted and only `LUIDLow` differed. The
[failed attempt](evidence/arena-live-placement/cleanup-first-attempt.json) and
its [original source](evidence/arena-live-placement/cleanup-first-attempt.py)
are preserved. The revised cleanup preserved that working config and restored
the original. The [successful receipt](evidence/arena-live-placement/cleanup.json)
proves all 26 original hashes match again, the backup is unchanged and no FF12
process remains. Saves themselves did not change.

The [saved-data reviewer](evidence/arena-live-placement/review_capture.py)
redecodes every scalar and field from the raw bytes, checks nonempty samples,
full span lengths, overlapping copies, identity controls and cleanup receipts,
and retains the arena-7 exception. An initial review assertion misspelled the
observed `START ADRS` annotation as `START ADDRS`; correcting that transcription
required no recapture. [Review result](evidence/arena-live-placement/review.json)
and [manifest](evidence/arena-live-placement/manifest.json) preserve the completed
check. This is capture reconciliation, not independent behavioral execution.

Peer review and consumer propagation are required before closing the new
architectural findings. Base/map all-time lifetime, arena-7 use, allocator cause
and reclamation, actor reuse, live resource ownership and integrated parity remain
open. This experiment's COMPLETE status applies only to this bounded package.
Full-database L1/L2 completion and required final reviews remain outstanding.
