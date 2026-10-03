# SWE2-AUDIT-SPEC review: FABLE's SD-197 answer and SD-199 (fable-sd197-sd199-1003, fable-sd199-remainder-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud sessions) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-SD197-SD199-1003` · Records: `_index/candidates/fable-sd197-sd199-1003/`, `_index/candidates/fable-sd199-remainder-1003/` (both commit `0496d685f`) · Re-checked at HEAD `8b6ea9d2e`

## SWE2-AUDIT-SPEC verdict: ACCEPT

- **SD-197 ANSWERED: accepted.**
- **SD-199: accepted as ANSWERED.** The request asked about the PARTIAL narrowing. In the same commit, FABLE's remainder record settles that narrowing's open point at the bytes, and the register row already reads ANSWERED. I checked the remainder's claim independently: a failing vertex stores a zero first qword.

## SWE2-AUDIT-SPEC checks

**Checkers re-run with the system Python** (numpy 2.5.3, unicorn 2.1.4; the analysis venv has no numpy):
- `check_sd197.py` ends `FAILS 0`, with 214 `PASS` lines (counted with `grep -c "^PASS"`). Its last NOTE is `slots whose linear channel's first key frame is > 0 (time 0..first-1 would read the residue): 0`.
- `check_sd199.py` ends `FAILS 0`, with 152 `PASS` lines. Its class lines end `T transform choice 0039A150 / 00399B80 (both preps, three grid walks) DRAWN` and `register/stack allocation, ... BOOKKEEPING`.
- `check_sd199b.py` ends `FAILS 0`. Its controls C2 and C3 both PASS: C3 shows that the Z1 writer sweep is sensitive, because a patched image whose `0039A0F9` stores `r10` to `022D8F10` is reported as a writer.

**Evaluator decode, read at the bytes (`disr.py`):**
- `0020E600` is `mov eax, ecx` / `add rax, [01F83530]` / `ret`.
- `004309C0`:
  - reads the counts at `004309CA` (`byte [rcx+0xc]`) and `004309FF` (`byte [rbx+0xd]`);
  - reads the handles at `004309E6` (`dword [rcx]`) and `00430A1F` (`dword [rbx+4]`);
  - returns at `00430A19`;
  - tail-jumps to `004307C0` at `00430A56`.

**Combiner jump table, read from the image** at `004308B0` (the `lea rdx,[00120000]` + `0x3108B0`, just past the body's last `ret` at `004308AD`):

| m | arm |
|---|---|
| 0 | `004307FD` |
| 1 | `00430833` |
| 2 | `0043084E` |
| 3 | `0043086C` |
| 4 | `0043088F` |
| 5 | `004307F2` |

The guard `cmp eax,5; ja 0x4307fd` sends m 6..15 to `004307FD`, which returns a.

**The combiner's arms:**
- m1 `a + F(b)`;
- m2 `a − F(b)` (`subss xmm6, xmm0`);
- m3 `F(b+b) + a − b`;
- m4 `F(b)·a + a`;
- m5 `subss xmm7, xmm6` (b − a), then `jp/jne 0x430833` into `a + F(b − a)`, else a.

**The b = ±0 branch** (`ucomiss xmm7,0; jp/jne`): with `(m−4)==0`, m4 returns a; m5 falls into `004307F2`, so a non-zero a gives `F(−a) + a`; every other m returns a. All of this matches the README's table and its b = 0 sentence.

**Shipped census:**
- `sd197_planar_tracks.tsv` has 153 lines: a header and 152 slot rows.
- The README's class counts are 21 + 102 + 10 + 17 + 2 = 152.

**SD-199 anchors:**
- `0053DD10` bytes `b8 01 00 00 00 c3` (`mov eax,1; ret`). A-2's `jne` never skips.
- `[00D1247C]` = `1.149999976` (1.15f).

**Vertex transform, read independently (T3 and the remainder):**
- `00399B80`: `0039A0C6 cmp rcx, rax` / `0039A0C9 jne 0x39a122` leaves at the first unequal vertex.
- `0039A150`:
  - `0039A6C8 cmp rax, rcx` / `je 0x39a6f0`.
  - The unequal arm `0039A6CD mov [r11], rcx` stores `rcx`, which came from `0039A6B1 movq rcx, xmm4`. Its only load in the body is `0039A51A movups xmm4, [022D8F10]`, and `022D8F10` has no writer: that is the remainder's Z1 sweep, and C3 shows the sweep is sensitive.
  - The equal arm `0039A6F0`–`0039A712` stores `[022D8FB0] | [022D8FA0] | [022D8FC0]`.

So the failing arm writes a zero first qword, and the earlier narrowing's first reading ("the failing arm therefore writes a non-zero qword") had the arms swapped, as the superseding blockquote says. A-1 and B-1 therefore fire on every failing vertex.

**Dependencies and routing:**
- `fable-k54-residue-1003/k54_modes.tsv`, which `check_sd199.py` section P reads, is now tracked. The README's "for FABLE to decide" item 4 is satisfied.
- The §6 correction on `how-an-authored-number-gets-its-randomness.md` is applied: L401 reads `combiner tail ~~00430540~~ 004307C0`, corrected by SWE2-EC7 on FABLE's routing.

**Register rows:**
- `OPEN-QUESTIONS.md` SD-197 reads `ANSWERED 2026-10-03 (FABLE; …)`, stating "layers of ONE evaluator … not three track kinds". That is item 1 of FABLE's decision list.
- SD-199 reads `ANSWERED 2026-10-03`, citing both records.

## SWE2-AUDIT-SPEC notes

- Both records state their stubs. The `sqrtf` import thunk is replaced by a correctly rounded sqrt, and `00808C40` (the cookie check) by `ret`. `003D8E50` is recorded only in section E, and E8 runs it for real. No result depends on a stubbed body.
- These stay outside the rows, as the record states, and are not defects:
  - the unit of instance `+0x44`;
  - the concrete render-local draws of the 12 channel-1 slots, which are bounded, not fixed.
- Advisory, not a defect: the `fable-sd197-sd199-1003` README still carries its "Recommendation: NARROWED" heading and "For FABLE to decide" items 3–4, now historical. The supersession blockquote makes the current state clear.
- Limits: static plus the records' own Unicorn runs, re-executed here. No live capture.
