# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-audio-bank-and-controller-family-ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-AUDIO-BANK-AND-CONTROLLER-FAMILY-EE-1-6729B` · Package: `_index/candidates/opus-audio-bank-and-controller-family-ee-1003-2/` (package last changed at `793e20e74`; reviewed at HEAD `85ecbde72`) · Page: `18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row. It was read clause by clause against a raw capstone decode of the certified image. This session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. The row holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0` and exited 0.
- **Counts.** 1 row with 5 anchors. The README's `Missing: 0` matches `rows.json`.
- **Image values.**
  - `01CEBBA8` is the float 1.0 (bytes `0000803f`).
  - `01CB5D88` holds the qword `007C1410`. The row names only the address stored, which is correct.
- **Callees read.**
  - `007E2F90` returns its value in `xmm0` (`movaps xmm0,xmm6` at `007E301E`; it is 0.0, 1.0 or a quotient from `cvtdq2ps`/`divss`). So the `comiss` against 1.0 compares a float result.
  - `00808C40` compares `rcx` against `01F44830`.

**`007C2280`**: exact.

- The qword at [o+0x28] is copied to `[rsp+0x20]`, and `007B2470(&it)` gives v (`007C2299`-`007C22B4`).
- qword [o+0x18] == 0 returns 0 (`007C22AF`/`007C22B7`). So does `al` == 0 from `call [[v]+0x20]` (`007C22C3`-`007C22C8`).
- `call [[v]+8]`, then `cmp eax,2` / `jne` → `mov al,1` (`007C22DE`-`007C22E4`, `007C2388`).
- qword [v+0xA8] != 0 returns 0 (`007C22EA`/`007C22F2`).
- p = 16 zeroed bytes at `rsp+0x38`. `007C2314` calls `007D0600(o+0x10, &p, dword [o+0x638])`.
- Loop bound: byte [[p+8]+5]. Both loads are repeated each step (`007C2379`/`007C2380`), with an initial `jbe` and a `jl` loop test.
- `007C234D` calls `007D03B0(&p, rsp+0x28, i)`. `007C235D` calls `007E3040(v, movzx word [[e+8]+4])`. `01CB5D88` is stored at `[rsp+0x28]` (`007C2362`) before the null test on x.
- A null x (`007C236A`) returns 0. So does `comiss 007E2F90(x), 1.0` / `jb` (`007C2374`/`007C2377`); `jb` is CF=1, so NaN is included.
- The loop exit returns `al` = 1 through the cookie check.

## SWE2-AUDIT-SPEC limits

- Body statements only. The callees `007B2470`, `007D0600`, `007D03B0` and `007E3040`, and the two virtual slots, were not read. The row claims nothing about them beyond their arguments and how their results are tested.
- The applier reported `ALREADY`, so the page text was taken to be the `rows.json` text.
