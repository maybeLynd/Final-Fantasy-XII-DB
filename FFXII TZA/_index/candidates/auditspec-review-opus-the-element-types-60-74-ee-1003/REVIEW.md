# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-element-types-60-74-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-ELEMENT-TYPES-60-74-EE-1003-4FFC6` · Package: `_index/candidates/opus-the-element-types-60-74-ee-1003/` (reviewed at HEAD `a028be1b9`) · Page: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-60-74.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 5 rows. All 5 were read clause by clause against a raw capstone decode of the certified image. This session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every row holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 5 functions, 25 anchors` / `ALREADY` / `FAILS 0` and exited 0.
- **Counts.** There are 5 rows with 5 anchors each, 25 anchors in total. The README's `Missing: 12` matches the length of the `missing` list in `rows.json`.
- **Constants read from the image.**
  - `01CEBBA8` is the float 1.0 (bytes `0000803f`). It is the "1" in `t1`, `t2` and `t`.
  - `01CEBDA0` is four copies of the dword `0x80000000` (bytes `00000080` x4). `xorps` with it is the sign flip behind the "-(...)" in `0054DD30`.

Per row:

- **`0034B8D0`**: exact.
  - `0034B8DF`/`0034B8E7`: `a` = `002E97B0(rdx)`.
  - `0034B8EC`-`0034B8F6`: `00263A30(byte [e+0x15], word [e])`.
  - The null checks on `a` and on `s` = `[a+8]` are at `0034B8FE` and `0034B907`.
  - `0034B90C`-`0034B920`: `002E4C30(s, 002E9C00(e))`, then `jle` (signed, greater than 0).
  - `0034B922` calls `002EAC90(e)`. `0034B927`/`0034B92B`: `cmp byte [e+0xD],0x80` / `jb`, so the `002EB380(e)` call at `0034B930` happens when the byte is 0x80 or more (unsigned).
  - The else path is `0034B937`-`0034B94C`: `002E9C00` is called again, there are two `js` tests, and `00314D40(1)` is called with `ebx` = 1, which returns 1 through `0034B95F`.
  - Every other path reaches `0034B961`. A non-zero `0053DD10()` returns `ebx` = 0 (`0034B987`). Otherwise `0016D6A0(1)` is called (`lea ecx,[rax+1]` with `eax` = 0) and the function returns 1.
- **`0052E270`**: exact.
  - `d` = `[rcx+0x20]` (`0052E27F`) and `s` = `rcx`+0x230 (`0052E283`).
  - `dword [rcx+0x44]` is re-read before each of the 13 calls.
  - The order of stores matches the sentence:
    - F/V pairs at s+0x58/0x80, s+0x5C/0x70, s+0x90/0xB0 and s+0x94/0xA0, from offsets 0x1D0/0x1E0, 0x220/0x230, 0x270/0x280 and 0x2C0/0x2D0.
    - Single floats at s+0xC0, 0xC4, 0xFC, 0x3C and 0x9C, from offsets 0x320 to 0x360.
  - `0052E3E2` is `jmp 0054C440` with `rcx` = `s`.
  - `004309C0` was read: it returns its value in `xmm0` (`00430A07`), so it does return a float.
- **`0052F400`**: exact.
  - It has the same shape as `0052E270`.
  - The stores are s+0xA8/0x100, 0xAC/0xF0, 0xB4/0x120 and 0xB8/0x110, then floats at s+0xBC, 0xC0 and 0xD8 from offsets 0x320, 0x330 and 0x340.
  - `0052F550` is `jmp 0054DD30` with `rcx` = `s`.
- **`0054C440`**: exact.
  - `t1`/`t2` are computed at `0054C468`-`0054C495`.
  - The loop guard is `cmp si, word [rcx+0x52]` / `jae` (`0054C49A`), and the loop end re-reads the word (`0054C67E`-`0054C68D`). The stride is 0xA0 from `[c+0x108]`.
  - The `[p+0x30]` == `p` test is at `0054C4A4`.
  - Set A (`0054C5B8`) is taken by `jae` from either `a` >= `[p+0xC]` or `b` >= `[p+0x98]`.
  - Set B (`0054C4E8`) is taken by `t1` >= `[p+0xC]` (`jae`) or `t2` >= `[p+0x98]`. Otherwise `jb` skips.
  - `comiss` sets CF on an unordered result, so a NaN fails every test.
  - The field sets match the code: A uses +0x58/+0x80/+0x84/+0x88/+0x70..78/+0x5C, and B uses +0x90/+0xB0/+0xB4/+0xB8/+0xA0..A8/+0x94.
  - Each arithmetic clause follows the `mulss`/`subss`/`addss` order: the `[p+0x24]` subtract and the three adds to +0x74, +0x78 and +0x70, then V.j·`[p+0x10+4j]`·D added into `[p+4j]` for j = 0 to 2.
  - Both sets reach `0054C679`, which calls `0046D560(p+0x40)`.
- **`0054DD30`**: exact.
  - `t` is computed at `0054DD60`-`0054DD7B`.
  - The loop compares unsigned against `dword [c+0xA4]`: `jbe` at `0054DD85` and `jb` at `0054E00A`. The stride is 0xA0 from `[c+0x190]`.
  - Set A is the fall-through of `jb` at `0054DDB0`. Set B is the fall-through of `jb` at `0054DED0`, and otherwise the element is skipped. NaN fails both tests.
  - The `[p+0x24]` add is `[c+0x68]`·`[p+0x7C]`, negated by `xorps` with `01CEBDA0`, then ·`[c+0xBC]`·K·M1.
  - The vector `v` is stored at `rsp+0x20`/`0x24`/`0x28` from K·`[p+0x20]`·M0, K·(new `[p+0x24]`)·M1 and K·`[p+0x28]`·M2.
  - `test byte [c+0x9C],2` / `je` gates `00202B90(rsp+0x20, c+0x150, rsp+0x20)` (`0054DE42`), and `v` is reloaded afterwards.
  - `00202B90` was read: it reads three floats from `r8` and twelve from `rdx`, and writes the products to `[rcx]`..`[rcx+0xC]`. So "passed through" holds.
  - Then come the adds into `[p+0x70..0x78]`, the V.j terms with D = +0xAC or +0xB8, and `0046D560(p+0x40)` at `0054DFF6`.
  - The cookie `01F44830` is checked by `00808C40` (`0054E01D`).
  - The field sets match the code: A uses +0xA8/+0x100/+0x104/+0x108/+0xF0..F8/+0xAC, and B uses +0xB4/+0x120/+0x124/+0x128/+0x110..118/+0xB8.

## SWE2-AUDIT-SPEC limits

- These are body statements, not meanings. The review does not test what the element types or the float fields mean.
- `00202B90` also writes a fourth float at `[rcx+0xC]` (that is, `rsp+0x2C` in the caller). The sentence does not mention it, and it does not contradict any clause.
- The callees `002E97B0`, `00263A30`, `002E4C30`, `002E9C00`, `002EAC90`, `002EB380`, `002EB9D0`, `00314D40`, `0053DD10`, `0016D6A0`, `00430B90`, `0054C440`'s callee `0046D560` and the tail targets are cited by their call sites only. No row claims what they do.
