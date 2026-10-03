# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-ui-request-router-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-UI-REQUEST-ROUTER-1002` · Package: `_index/candidates/fable-home-ui-request-router-1002/` · Page: `16-UI/Request-Router/ui-request-router.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 9 functions, 42 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 9 rows, 42 anchors; mechanically rejected 2, skipped 0, missing 0.
- Semantic pass: **all 9 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `00241940`: bit masks `0xFFFFFFF7` (bit 3), `test byte +0x3C4, 2` (bit 1), `or 0x40` (bit 6), `and 0x21; cmp al, 0x21` (bits 0 and 5), `0x400` (bit 10), `0x80` (bit 7). The call order matches the text.
- `0028D1C0`: `rdi` advances to the saved next pointer only when the removed node is the current head candidate (`cmp rdi, rcx; cmove rdi, rbx`), so the return is the first surviving node, or null.
- `002C98F0`: `and 0x3FF7FF` then `or (dx << 22)` then `bts 11` keeps bits 0-21 except bit 11, puts the low 10 bits of `dx` into 22-31, and sets bit 11. `0209AC30` is re-read after each store and call (`002C9930`, `002C9956`, `002C996A`). `jle` makes the `edx` test signed.
- `0035C660`: the 0x30-byte block at `rsp+0x20` is zeroed by six qword stores, then filled with `+0x28` word 0x102 (`rsp+0x48`) and `+0x2C` dword 0x4FB (`rsp+0x4C`); the call is `00241C90(0, &block)`.
- `002D54B0`, `00309E40`, `00290740`, `0028F5F0` and `003C8950`: offsets, re-reads and bit tests are as stated.
- Host: every caller (`00241D40` ConfirmCaption, `0028C4B0` open preamble, `002E0E30`, `002D5EB0` R12, `002C98C0` fade, `0035D6B0` request 24, `00253C70`) is read on the page.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
