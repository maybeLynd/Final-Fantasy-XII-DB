# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-how-a-sound-fades-the-ramp-and-its-six-c-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-HOW-A-SOUND-FADES-THE-RAMP-AND-ITS-SIX-C-EE` · Package: `_index/candidates/opus-how-a-sound-fades-the-ramp-and-its-six-c-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `18-Audio/Audio-Boundary/how-a-sound-fades-the-ramp-and-its-six-curves.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 4 rows were checked clause by clause against the bytes; the package has fewer than 15 rows. 4 of 4 are exact.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify only).** `interior_applier.py` without `--apply` writes nothing. Run under the analysis venv with `-B`: `VERIFY 4 functions, 20 anchors` / `ALREADY` / `FAILS 0`, identical to the committed `.out`.
- **Live page.** Each function has exactly one interior-table row. Its text equals `rows.json` byte for byte, and all of its anchors appear in the row.
- **Anchors.** All 20 are instruction boundaries with the recorded mnemonic. Each lies on its clause.
- **Strings read from the image.** `01CB44B0` = "[sead][!!error!!]Category::InitializeRefCategory referenced category is not initialized( or reference is looping )!", which has no format directive, so the unset `r9` is never read. `01CB5BF8` = "[sead][!warn!]Sound::SetPitch failed range over %f".

| fn | verdict | decisive bytes |
|---|---|---|
| `007A9D30` | exact | `movsxd rdi,[rcx+0x7c]`/`jle` (`007A9D3A`, `007A9D51`); start 1.0 from `01CEBBA8` (`007A9D46`). `rbx` = `[rcx+0x40]`+0x14, stride 0x30 (`007A9D5C`/`007A9D66`/`007A9DA8`), so `[rbx]`=`+0x14`, `[rbx-8]`=`+0xc`, `[rbx-4]`=`+0x10`, `[rbx+8]`=`+0x1c`, `[rbx-0xc]`=`+0x8` (`007A9D73`..`007A9DA3`). Product `mulss` (`007A9DAC`), ×`[rcx+0x4c]` (`007A9DB6`). The count ≤ 0 path is 1.0×`[rcx+0x4c]` (`007A9DDE`). |
| `007A9F40` | exact | The same body with `[rcx+0x78]`, `[rcx+0x38]` and `[rcx+0x48]` (`007A9F4A`, `007A9F6C`, `007A9FC6`, `007A9FEE`). |
| `007AA320` | exact | Word `[[rdx+8]+4]`, `neg dx`, `test`/`jle` → 0 (`007AA33B`..`007AA34C`, `007AA3BA`). `movsx ecx,dx` → `007AAA20` (`007AA34E`/`007AA351`). Stored to `[rcx+0x58]` (`007AA356`). `cmp dword [rax+0x10],0`/`jne` → 0 (`007AA35A`). `0019C5D0(rsp+0x20, 0x100, 01CB44B0)` (`007AA360`..`007AA371`). Length ≥ 0xff (signed `jl`) → −2 (`007AA376`..`007AA37D`); 0xa at len (`007AA385`); terminator index `jae 0x100` → `00809728` (`007AA38D`/`007AA394`/`007AA3D5`). Import `008C2120` with `rsp+0x20` (`007AA3A0`); `007A5570(2, rsp+0x20)` (`007AA3A6`..`007AA3B0`); −1 (`007AA3B5`). Cookie `00808C40`. |
| `007BE8A0` | exact | `comiss xmm1,[008C5B30]` (0x3b000000 = 0.001953125)/`jb` and `comiss xmm1,[01CEBC08]` (2.0)/`ja` (`007BE8B9`..`007BE8C9`). In range: `rcx+=0x188`, byte `[rsp+0x20]`=0 (fifth argument), `r9d`=0, `007CA560`, result returned (`007BE8CB`..`007BE8F6`). Else `cvtss2sd`→`r9` (`007BE901`/`007BE90F`), `0019C5D0(rsp+0x30, 0x100, 01CB5BF8, double)` (`007BE914`), the same 0xa/terminator/`00809728` handling (`007BE919`..`007BE937`), `008C2120` (`007BE943`), `007A5570(1, rsp+0x30)` (`007BE953`), −1. |

## SWE2-AUDIT-SPEC narrowing / notes

None blocking. README "Missing: 3" (`007A7010`, `007BDBB0`, `007BEAF0`) is outside this spot-check.
