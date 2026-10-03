# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-time-stop-and-system-stop-registry-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-TIME-STOP-AND-SYSTEM-STOP-REG` · Package: `_index/candidates/fable-home-the-time-stop-and-system-stop-registry-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package is unmodified in the working tree) · Page: `00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 5 rows are exact against the bytes, and every caller is one of this page's own functions.

- The two walks `002FD060` and `003B1000` are the clear-side twins of the rate-0.0 set walks `002FD090` and `003B1050` that the page reads (lines 226-229). They run from the per-frame stepper `0024BFD0`, which the page names (line 211).
- The other three are each entered from a function cited in the page's own text.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 5 functions, 22 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 876 and the five rows (lines 882-886) match `rows.json` byte for byte.
- **rows.json.** 5 rows, 22 anchors. Rejected 2 (`00182610`, `0029D210`, both "already cited by" this page; the page does cite them), skipped 0, missing 0.
- **`001986B0` (0x12 B).** `movzx eax, byte [rcx+0x3A]` / `test al, 1` / `jne ret` / `or al, 1` / `mov byte [rcx+0x3B], 1` / `mov [rcx+0x3A], al`. Exact. Entered by the tail `jmp` at `00182CF0` + 0x10 (`00182D00`) with `rcx` = `InputManager_GetSingleton()`. It is the only transfer (raw index).
- **`002FD060` (0x2B B).** Head `02EC3D60` with `je ret` on null, `[rax+0x10]` with a null skip, `and word [rcx+0x368], 0xFFFB`, next `[rax+0x28]`, `jne`. Exact. Entered at `0024BFD0` + 0x67 (`0024C037`).
- **`003B1000` (0x44 B).** `lea rax, [02EBEC08]`, `cmp dword [rax-8], 0` / `je ret`, a null-qword skip, a bit-4 test on `word [rdx+0x368]` followed by `and`/store, then `add rax, 0x18` / `cmp ecx, 0x24` / `jl`. Exact. Entered at `0024BFD0` + 0x6C (`0024C03C`). Both `0024BFD0` sites run only when `byte 020926E5 & 3 == 2`, after the frame count reaches zero.
- **`003C8B20` (0x22 B).** It returns `dword [02B47730 + 0xC8]` on the live-and-bit-4 path, and 0 otherwise (also when that dword is 0, which the sentence's "returns dword" covers). Exact.
- **`003C9590` (0x21 B).** The same gate, then `cmp dword [rcx+0xC8], 0` / `setne al`. Exact.
- **entered_from for the last two.** `00252E30` + 0x0 and `00252E50` + 0x0 are the 5-byte thunks `jmp 003C8B20` / `jmp 003C9590`. The raw index gives the thunks' only callers as `003D9E20` (`003D9E52`, `003D9E39`).
- **Host fit.**
  - `0024BFD0` is the page's dim-triple stepper (line 211), and the two walks undo the bit-4 marks that its rate-0.0 arm sets.
  - `00182CF0` is cited in §3.1 as the tail jump taken for stop id 17 in the `00227680` record build (lines 91-93).
  - `00252E30`/`00252E50` are cited in the `003D9E20` paragraph (line 782, "the registry's armed-mode flip").
  - Apart from `_index/ADDRESS-INDEX.md`, no other page cites any of the five bodies.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- `001986B0` sets bit 0 of the input manager's `+0x3A` and arms the `+0x3B` one-shot. Its bit-2 sibling `00198670` is homed on `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md` (line 1616). What `+0x3A`/`+0x3B` mean is still open on `15-Input/Binding-Profiles/CONTRACT-binding-profiles.md` (line 509). A cross-reference would join the pair.
- The `02B47730` accessor family (`003C8950`, `003C93E0`, `003C9550`, `003C9570`, and now these two) is spread across caller hosts. This page does not otherwise discuss `02B47730`.
