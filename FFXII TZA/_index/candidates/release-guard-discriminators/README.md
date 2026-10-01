# The two release guards of EXP-230, branch by value (FABLE, Claude Opus 5.5, 2026-09-28)

**Claim corrected.** EXP-230 (ORACLE) describes `00325A00` as calling the deeper release `003DC780` "only when
`ecx` ∉ {0,1} (`ecx==1` also passes through)". Its boundary list gives "gated: `ecx` ∉ {0,1} required", and the
auto-status contract's §13am repeats "`ecx` ∉ {0,1} → `3DC780`". The bytes say otherwise:

```
00325A00  test ecx, 0x7FFFFFFE   ; any of bits 1..30 set -> tail call
00325A06  jne  003DC780 (via 00325A0D)
00325A08  cmp  ecx, 1            ; left: 0, 1, 0x80000000, 0x80000001
00325A0B  jne  ret               ; 1 -> tail call; the other three return
00325A0D  jmp  003DC780
```

- **Only 0, 0x80000000 and 0x80000001 skip the deeper release, and `ecx == 1` takes the tail call.**
- `00317EC0`'s stated guard, "`ecx` ∉ {0, −1}", is correct: `lea eax,[rcx+1]`, `cmp eax,1`, `ja 0042FCC0`.

**Discriminators** ([`guard_branches.py`](guard_branches.py), [output](guard_branches.out)), run verified at 5ce3754a0, FAILS 0:
- **G1:** unicorn runs `00325A00`'s 19 original bytes on eleven values. It returns for exactly 0, 0x80000000 and
  0x80000001, and leaves for `003DC780` otherwise, including for 1.
- **G2:** the same for `00317EC0`. It returns for exactly 0 and 0xFFFFFFFF.
- **C:** controls. A planted `ret` reports RETURN, a planted `jmp` reports the target, and a stray fetch reports ERROR.

**Scope.** This executes the guards' branch only. The deeper releases `003DC780` and `0042FCC0` are never
entered: the harness stops at their entry. Static guard truth, and this execution of the guard, do not execute the
deeper release or say what it does. EXP-230's own suite observed `cl=0` and `0x27` rows, where `d[+0x28]` and
`d[+0x24]` are 0. Those rows skip under either reading, so **no EXP-230 case changes**. The error is in the
description, not the verdicts.

**Why these values.** `0030C970`'s row reset writes `d[+0x28] = 0x80000000` and `d[+0x24] = 0xFFFFFFFF` (EXP-230's
own reset list). Each is its guard's skip value, so a freshly reset row releases nothing through either guard.

| consumer | states | agreement |
|---|---|---|
| `_experiments/EXP-230-mode-byte-clear-30C970-exec.md` line 28 and its boundary list (ORACLE's receipt) | `ecx` ∉ {0,1} | routed-to-ORACLE (FABLE-REQ-ORACLE-EXP230-325A00-GUARD), as a dated annotation; the receipt is not rewritten |
| `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md` §13am | the same | routed-to-ORACLE: the section sits in an uncommitted overlay on that file |
| `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` 1147 | lists the instructions only | agrees |
| `_experiments/EXP-231-detach-siblings-exec.md` 45 | "×0 checks" of the deeper arms | agrees: counts, not a guard description |
