# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-phyre-to-bullet-rigid-body-materializati-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-PHYRE-TO-BULLET-RIGID-BODY-MATERIALIZ-4AEEC` · Package: `_index/candidates/opus-phyre-to-bullet-rigid-body-materializati-ee-1003/` (reviewed at HEAD `f227ff3da`) · Page: `23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The package has 6 rows. All 6 were read clause by clause against a raw capstone decode of the certified image. This session checked the image hash: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Five rows are exact. In `008382D0`, one clause calls two vectors "max" and "min", but no instruction in the body orders them. The narrowing below replaces those labels with the offsets the bytes use. The row's anchors are unchanged.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 6 functions, 30 anchors` / `ALREADY` / `FAILS 0` and exited 0. The rows are already in the page block `## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)`, line 682.
- **Counts.** There are 6 rows with 5 anchors each, 30 anchors in total. Every listing ends in `ret` before int3 padding, so no body was cut off by the dump window.
- **Constants and thunks read from the image.** `01CEBB60` is the float 9.9999997e-05 (bytes `17b7d138`), which matches the row's "0.0001". `01CEBBA8` is 1.0 (bytes `0000803f`). `00861F14` is `jmp [008C2BB8]`, and that IAT slot is api-ms-win-crt-math `sqrtf`.

Per row:

- **`00832590`** (`00832590`-`0083280A`): exact.
  - `008325A0`: inc dword `[rcx+0x68]`.
  - `008325B3`-`008325CD`: the 64 bytes at `rdx` are loaded into xmm6-xmm9 before the first call (`008325E4`).
  - `008325A6`: `t` = dword `[r8+8]`.
  - `m`: the return of slot +0x50 is copied from xmm0 to xmm10 at `008325FA`.
  - `008325FE`: slot +8 gets (`rbx` = the entry `rdx`, `rsp+0x20`, `rsp+0x30`).
  - Min/max updates (`0083260C`-`0083266E`): each is a `comiss` followed by `jbe` skip. An unordered compare sets CF=ZF=1 and skips, so a NaN changes nothing.
  - `00832673`-`008326A0`: `p` = `008410B0([rdi+0x60], rsp+0x50, movsxd [rdi+0x1C])`. The call is guarded by `test`/`je`, and `rbp` = 0 otherwise.
  - Growth (`008326B2`-`00832795`):
    - It grows when count == capacity and capacity < 2·count (1 for 0), compared signed with `jge`.
    - The new block is `0085E680(0x60·n, 0x10)` (`008326EA`).
    - Bytes +0..+0x57 are copied, and a null destination is skipped (`00832714`).
    - The old block is freed with `0085E710` only when it is non-null and the byte at +0x30 is set (`00832770`/`00832776`).
    - `00832785`/`00832791`/`00832795` store the data qword, the owner byte and the capacity.
  - Store: `008327B5` skips a null slot, `008327B7`-`008327D9` write the fields, and `008327DD` increments the count.
- **`00833440`** (`00833440`-`0083370B`): exact.
  - `00833478` calls `00831D30`, and `00833485` stores the vtable `01CCD938`.
  - `00833488`-`008334A0`: byte +0x98 = 1, qword +0x90 = 0, and the qword at +0x84 = 0 (clearing dwords +0x84 and +0x88), then dword +8 = 4.
  - Negative `n` jumps from `008334B0` to `0083358A`, which stores +0x84, and both loops are skipped (`00833595`, `00833694`).
  - Positive `n`:
    - `008334D5` allocates `0085E680(16n, 0x10)`.
    - `00833539`-`00833547` store the owner byte, the array and the capacity.
    - The fill loop `00833570`-`00833588` stores xmmword `[rbp-0x10]`, with a null test at `0083357A`. The body first writes that stack slot at `008335C4`, later in the code, so the filled value is uninitialised.
  - Per-point stores (`008335C0`-`008336E6`, unrolled by 4 with a remainder loop): floats `[rsi]`, `[rsi+4]` and `[rsi+8]` plus the dword 0 at `[rbp-4]` (`0083359E`/`00833696`). Each store goes to `[rax+rdx]` with no test, and the stride is `movsxd r12d`. `r12d` is reloaded from the r9 home slot at `0083354E`.
  - `008336EB` calls `00832290(rbx)`, and `rax` = `rbx`.
- **`008382D0`** (`008382D0`-`008385FE`): **narrowed**, one clause. Everything else is exact:
  - Stack args: `[rsp+0x90]`/`0x98`/`0xA0`/`0xA8` are entry `rsp`+0x28/0x30/0x38/0x40 after five pushes and `sub 0x40`.
  - Null `c`:
    - `00838358`/`0083835B` call `0085E680(0x80, 0x10)`.
    - `00838375`/`0083837A`/`0083837F` store the return of `00847E60`, or 0 from `0083837C`.
    - `00838386` sets byte +0x98 = 1.
  - `f` == 0:
    - The `q` block is `0085E680(0x28, 0x10)` (`008383A3`), with the stores at `008383B7`-`008383D5`.
    - The `r` block is `0085E680(0xE0, 0x10)` (`008383EF`). It is passed to `00849B30` with `[rbx+0xA8]` re-read (`00838406`).
    - `00838421` writes byte `[rax+0xDD]` with no test.
  - Quantisation: `0083842C`/`00838434` copy the vectors at `rdx` and `r8` to +0x10/+0x20. `00838457`-`00838494` compute the word +0xA as float divided by the per-axis differences, with 0 at +0x3C.
  - Handle array:
    - `0083834D`: `inc di` is a 16-bit wrap.
    - `0083849D`-`008384B6`: `mul` by 0x60 with `cmovo` -1, then `0085E680`.
    - `008384E0`/`008384E3` zero the qwords.
    - The fields are set at `008384F6`-`00838509`.
    - The k-loop is `00838520`-`00838539`, and entry `n`-1 is cleared at `0083854E`.
    - The three `0085E680(8n, 0x10)` results are each stored at both +0x58+8j and +0x70+8j (`0083857D`/`00838581`).
    - `00838592` writes `[h]`, and the j-loop is `008385A0`-`008385E1`.
  - None of the stores through `h` after `008384F6` is preceded by a test of `h`. The only jcc there are the loop compares at `00838516`, `00838539`, `0083858C` and `008385E1`.
- **`00838650`** (`00838650`-`0083871F`): exact.
  - `00838673` stores the vtable `01CCE2A0`, and `00838676`/`0083867E` gate on qword +0xA0.
  - The +0xA8 object gets slot 0 with `edx`=0 (`0083868C`) and no null test, then `0085E710` with the qword re-read (`0083868F`/`00838696`). The +0xA0 object gets the same at `0083869C`-`008386B2`.
  - The `0085E710` loop covers +0x80, +0x78 and +0x70 (`008386B8`-`008386D5`: `edi`=2 down to 0 with `jns`), then +0x48 at `008386DB`.
  - `008386E1` gates on byte +0x98, and the +0x88 object gets slot 0 then `0085E710` (`008386F6`/`00838700`).
  - `0083870D` stores the vtable `01CCE1A8`.
- **`0083AA80`** (`0083AA80`-`0083AB52`): exact.
  - `0083AAAC` stores the vtable `01CCE610`.
  - The loop compare is signed (`jle` at `0083AAB9`, `jl` at `0083AB13`) against dword +0xC. The array qword +0x18 is re-read on every pass (`0083AAC0`).
  - `0083AADB`: `w`'s slot +0x48 is called with only `rcx` set.
  - `0083AAEC`: the result's slot +0x48 gets (`p`, `[rbx+0x28]`).
  - `0083AAF1`-`0083AAFF`: `w` is re-read, and its slot +0x10 gets (`p`, `[rbx+0x28]`).
  - `0083AB03` nulls `[o+0xC8]`.
  - The tail is `0083AB15`-`0083AB36`: a null test, then `0085E710` gated on byte +0x20, then byte +0x20 = 1, qword +0x18 = 0, and the qword at +0xC = 0.
- **`0084AB40`** (`0084AB40`-`0084AD93`): exact. The frame has `rbp` = `rsp`+0x100, so `X` = `rsp+0x40`, `S` = `rsp+0x70`, `O` = `rsp+0x30`, `B` = `rbp+0xC0` and `R` = `rbp-0x10`.
  - `0084AB94` calls `00831D90(&S)`. `0084ABA0`/`0084ABA5` store the vtable `01CCECC0` and dword `S+8` = 1.
  - `0084ABAD`-`0084ABC2` copy the 48 bytes to `rbp-0x40` (= `X`+0x80).
  - `0084ABCF` writes `X`+0x70 = `[rcx+0xD4]`.
  - `0084ABD4` writes `B`+0x140 = 0x38D1B717, and `0084ABE3` ANDs `B`+0x160 with 0xFFF0.
  - `0084AC15` calls `0084BDF0` with 5 args. I read `0084BDF0`: it reads its fifth argument from entry `[rsp+0x28]` at `0084BDFE`.
  - `R` is set up at `0084AC22`-`0084AC45` (1.0 = 0x3F800000).
  - `0084AC71` calls `0084BED0` with 6 args, `rdi+0x90` in both `r9` and `[rsp+0x20]`. I read `0084BED0`: its prologue reads entry `[rsp+0x28]` and `[rsp+0x30]` as `[rbp+0x3D0]` and `[rbp+0x3D8]`.
  - Gates: `0084AC78` tests al. `0084ACB6`/`0084ACBD` compare the squared length with `jbe`, and `0084ACC7`/`0084ACCE` compare `[rcx+0xD0]` with `R`+0xB0 using `jbe`, so a NaN fails both.
  - Normalisation is `0084ACD3`-`0084ACFC`: 1.0/`sqrtf`.
  - `0084AD2A` calls its own slot +0x10 with (`rbp+0x80` = `R`+0x90, `rbp+0x90` = `R`+0xA0, xmm3 = `R`+0xB0, `esi` = `r8d`, `r14d` = `r9d`).
  - Teardown is at `0084AD2E`-`0084AD5A`.

**5 of 6 exact; 1 narrowed.** All 30 anchors were checked.

## SWE2-AUDIT-SPEC narrowing

**`008382D0`: in rows.json and in the page's 2026-10-03 block, line 690.** The divisors come from `00838439`-`00838452`:

- xmm4 = float `[rbx+0x20]` - float `[rbx+0x10]`
- xmm3 = `[rbx+0x24]` - `[rbx+0x14]`
- xmm0 = `[rbx+0x28]` - `[rbx+0x18]`

Fields +0x10 and +0x20 are plain copies of the 16 bytes at `rdx` and at `r8` (`0083842C`, `00838434`). No compare, `minss` or `maxss` orders them, so the body does not establish which one is a maximum. The words "max" and "min" are undefined in the sentence and are labels from outside the bytes.

Replace:

> +0x30 = (`s` as float / (max - min) per x/y/z, 0)

with:

> +0x30 = (`s` as float / (float at +0x20 - float at +0x10) per x/y/z, 0)

The anchors are unchanged, and the rest of the row stands.

## SWE2-AUDIT-SPEC limits

- Body statements were checked against the bytes. Meanings were not reviewed, including the class names the page gives these constructors and labels such as "point array" and "shape".
- Callee behaviour was read only where a row depends on it. That covers the arity of `0084BDF0` and `0084BED0` and the IAT name behind `00861F14`. Callees that a row names only as calls are opaque here: `00831D30`, `00831D90`, `00832290`, `00847E60`, `00849B30`, `008410B0`, `0084B280`, `00830C40`, `0085E680` and `0085E710`.
- Signed and unsigned readings follow the jcc at each site as listed above.
- Two package records were cut short, and neither is part of a row. In `rows.json` `corrections`, the `008382D0` text ends mid-list ("0x28-byte q layout, "), and README.md's second correction bullet stops at the same point. This does not affect any row.
- README.md records 6 entry-cited functions as missing (`0083B780`, `0083E7E0`, `0083FD10`, `00846710`, `00857970`, `008585E0`). They are outside this review.
- This review is a non-author read. It does not replace a live check of any behaviour.
