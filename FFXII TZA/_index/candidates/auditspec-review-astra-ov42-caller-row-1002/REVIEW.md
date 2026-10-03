# SWE2-AUDIT-SPEC review: ASTRA OV-42 caller-row preconditions

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; independent of ASTRA and FABLE) ·
2026-10-03 · Task: `ASTRA-REQ-SPEC-OV42-CALLER-ROW-1002` · Package: `_experiments/evidence/ov42-caller-row-preconditions/`
(publisher commit `103aa3123`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped exactly as the package states. This is a local, static, conditional proof. It does not show the two IDs
disagree, and it does not establish natural owner/row/kind coherence, initialized bindings or whole-OV42 closure.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- `00304850` (`BattleUnit_AdvanceStandardActionState`): `movzx r13d, word [rcx+6B0h+64h]` at `0030488D` latches
  WORD `unit+714` at entry.
  - R15 is that ID's row pointer, built from the `02EBF138` descriptor (`20E600` base + `word [desc+8]` × ID). It is
    built with a **32-bit** `add r15d,ecx` (`00304934`), which is the producer's "64-bit add" countercontrol site.
- The phase switch reads byte `unit+6B4` (≤ 0Ch). Its image-base-relative table at `00305044` was decoded from the
  image:
  - phase 8 lands at `00304EB3` and phase 9 at `00304EBE`;
  - both are past `30CFB0` (`00304E24`) and `30CA80` (`00304E3E`), so neither entry reruns acquisition or readiness
    in this invocation;
  - both reach `387090` → `movzx edx,ax` (`00304EDC`) → `30D160`, then `movzx edx,r13w` → `305430`, whose EAX is
    overwritten untested by `movabs rax,400000000000h` at `00304EF3`;
  - after that, `306760` receives `rdx = r15` (`00304F47`).
- `00305430`, for IDs 511..534 (`1FFh..216h`):
  - `cmp dx,115h / ja` → `sub ax,116h / cmp ax,108h / ja` (unsigned 16-bit), so these IDs take the 278..542 arm.
  - Under a non-null descriptor and resolver result, that arm makes the two `20E600` calls and then
    `test byte [row+2Ch],40h`. When the bit is clear it goes to `00305609`, where `cmp di,113h` fails, so it returns
    0 with no own non-stack store.
  - The target-mutating `311F70` call is only on the bit-set side.
- Retained US table `action_data_us.st2e`, parsed independently:
  - header `st2e`, count 543, stride 60, offset 32;
  - byte `+2Ch` is `00` for every ID 511..534;
  - inside 278..542 only IDs 325, 326, 416, 417, 436 and 455 have bit 6 set.
  - The table's provenance is the prover's Git-blob check. It is not a fresh extract: no US copy sits under
    `D:/FFXII_TZA_extract` by that name.

## SWE2-AUDIT-SPEC reproduction (disposable copy, run from the repository root as the README requires)

- `prove.py` re-run: exit 0, stdout identical, result **byte-identical** to `result-01.json`. A subdirectory cwd
  fails `git ls-tree` with a cwd-relative pathspec, which is correct fail-closed behaviour.
- `control.py` re-run: exit 0, stdout identical. The four actual CLI negatives (extent failure, capture failure,
  missing caller, zero ranges) all exit 1 with no exception. The four countercontrols (64-bit row add, builder using
  the latched ID, signed helper bound, row 511 bit 6 set) all refuse.

## SWE2-AUDIT-SPEC notes (premises, no correction required)

- `305430` dereferences `[row+2Ch]` even when the descriptor or resolver is null (`rbx`=0). The package's
  "stable readable descriptor/resolver binding" premise is therefore load-bearing, not decorative.
- Natural ID coherence, `unit+714`/phase writer continuity, global owner-kind persistence and `30D160`/`306760`
  callee effects stay OPEN, as the package says.
