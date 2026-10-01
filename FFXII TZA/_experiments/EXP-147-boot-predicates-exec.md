---
experiment: EXP-147
title: Boot-fixups §13c predicate layer executed — the four
  01F82E38/01DFE0C0 predicates, suppressor writer and gate,
  singleton getter, and the 0022BDF0 argv/-nologo +
  settings-row-18 selector on shipped bytes
contract: 00-Engine-Core-Runtime/CONTRACT-boot-fixups.md
method: B
live_game: false
tool: evidence/boot-predicates-exec/check.py
---
# EXP-147 — boot-predicates-exec

**Status:** complete · **44 cases, zero failures, stable ×3**
**Evidence:** `evidence/boot-predicates-exec/` (`check.py`,
`result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base
`0x120000`

## Objective

`CONTRACT-boot-fixups.md` §13c statically describes the four
predicates that publish the `01F82E38` mode flag, the
`01DFE0C0` suppressor and its gate `00184960`, and the
`0022BDF0` selector — none executed. This experiment runs all
of them on shipped bytes.

## Executed behaviour

### The four predicates

- **`001EDDA0`** (27 B): suppressor `01DFE0C0` tested **first**,
  then flag `01F82E38`; returns `0` iff flag set AND
  unsuppressed, else `1`. Nonzero non-1 flag counts as on
  (`mut-flag-neg`: `0xFFFFFFFF → 0`).
- **`001EDEC0(arg)`** (40 B): reads the **same pair in the
  opposite order** — flag first, then suppressor — a detail
  §13c's table flattens ("the same pair"). Returns `1` unless
  the mode is on and unsuppressed, then `(~arg) & 1`
  (args 0→1, 1→0, 2→1, 3→0 all executed).
- **`001EDE70`** (7 B): returns the flag **verbatim** —
  `0x7F → 0x7F`, not bool-normalised.
- **`001EDE80`** (61 B): flag then suppressor; `1` unless on —
  then `0022A080() + 0022A030()`, two real leaves returning
  `d[02064AD8]` and `d[02064AA8]`; sum is 32-bit (`e80-wrap`:
  `0xFFFFFFFF + 2 = 1`, `mut-e80-sign`: `0x80000000`).

### The suppressor chain

- **`001EDEF0(ecx)`** (7 B): `d[01DFE0C0] = ecx` verbatim —
  `0x7F` written as `0x7F`, no bool normalisation.
- **`00184960(mode)`** (123 B) — executed truth, refining
  §13c's prose ("cleared unless mode==1 and byte==0"):

  ```
  supp = 1                                    (via 001EDEF0)
  if flag == 0:        -> tail, ebx = mode    (mode/byte never read)
  if mode != 1:        -> supp = 0            (cleared)
  if d[02092748] != 0:                        (gate cell — NOT in §13c)
      if 00229EA0() != mode: -> supp = 0      (movsx b[02064AD3])
      -- byte check BYPASSED entirely
  if b[001EBA40() + 0x118] == 0: -> tail      (stays 1)
  else:                -> supp = 0
  tail: 00798E90(ebx)  clamp [1,3] -> d[01F3DA18]
        00189120()     -> q[01F7F598]
        nonzero -> tail jmp 005FEA50(rcx=q[rax+8], rdx=0017ECB0,
                                     r8=ebx)
  ```

  **Executed divergence from §13c:** `g-m1-gatefail-byte0`
  (flag=1, mode=1, gate set, `b[02064AD3]=2`, **byte=0**)
  clears the suppressor anyway — the `00229EA0` gate is a
  force-clear that bypasses the byte check entirely, and
  `flag==0` keeps the suppressor set regardless of mode/byte.
  The `ebx` handed to the tail is the **original mode** on the
  `flag==0` path but `1` on every cleared path.

### `001EBA40` singleton getter

`q[01F82E18]` nonnull → returned directly. Null →
`00210EC0(0x2E0)` alloc → `001EB190(ptr)` init → writeback to
`01F82E18` → returned (lazy path executed with alloc/init
scripted, order `eba40 → x10ec0 → xb190`).

### `0022BDF0` selector + `-nologo` scan

`ecx=argc, rdx=argv`. `ebp = (0017D8F0()==1)` — the settings
getter is a real leaf reading `d[q[01F82D20]+0x48]` (row 18).
Then the argv loop compares **exactly 8 bytes** per argument
against `"-nologo\0"` at `00908BD8` — executed: `"-nologo"`
matches, `"-nologo2"`, `"-nologoextra"`, `"-nolo"` do not
(byte 7 must be NUL — it is an exact-match, not a prefix);
`argc==0` skips the loop; mid-array match works. On match,
`00314DE0(1)` (real) writes `d[022C2528]=1`. Tail `jmp
001EDDC0` hands `ecx=ebp` — recorded at entry as `0` or `1`
(`001EDDC0` itself is EXP-142's executed scope and is
intercepted here).

## Evidence classes and boundaries

**NATIVE-REPLAY** on shipped bytes (hash-verified image,
Unicorn): all nine named bodies plus leaves `0022A080`,
`0022A030`, `00229EA0`, `0017D8F0`, `00314DE0`, `00798E90`,
`00189120` executed as shipped.

**Scripted boundaries, disclosed:** `001EDDC0` (ecx recorded,
not re-run — EXP-142 owns it), `005FEA50` registry vtable
dispatch (args recorded), `00210EC0` allocator (planted heap
return), `001EB190` singleton init (intercepted). Fixture
globals are MODEL-PROVEN; all branch outcomes, call orders,
stored values and the gate-divergence finding are
NATIVE-REPLAY.
