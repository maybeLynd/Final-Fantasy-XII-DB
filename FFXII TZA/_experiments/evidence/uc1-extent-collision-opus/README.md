# UC-1 extent collision: `007EE7C0` against the listed `007EE7F0` (OPUS, 2026-09-27)

This answers `ASTRA-RETURN-OPUS-UC1-EXTENT-COLLISION` as the **owner adjudication**. It is not
independent acceptance: review is routed to SWE2-AUDIT-SPEC. No denominator, function-list
row or generated table is changed by this package.

**Ruling: the listed `FUN_007ee7f0` (9 B) is a FALSE entry.** It is the last seven bytes of the
unlisted leaf body at `007EE7C0`, decoded from one byte inside a REX-prefixed store. The
complete body is **`007EE7C0`–`007EE7F9`, 57 B**. It is **not a deliberate alternate entry**.

## Question and discriminators, fixed before the run

- **The question:** is `007EE7F0` a deliberate alternate entry, or an entry the list invented
  inside the real body?
- **D1, instruction extent.** Does the reachable path from `007EE7C0` own an instruction that
  covers `007EE7F0`?
- **D2, producers.** Does *any* image-level producer name `007EE7F0`? The producers scanned
  are:
  - a `rel8`/`rel32` branch or call;
  - a RIP-relative operand;
  - a DIR64 relocation;
  - an absolute qword;
  - an image-relative dword;
  - a `.pdata` begin;
  - an export.

  A deliberate alternate entry needs at least one producer. A false entry has none.
- **Controls:**
  - the known LEA `007EC4F1` → `007EE7C0`;
  - the `.pdata` begins of the listed neighbours `007EE730` and `007EE800`;
  - a planted `rel32` call to `007EE7F0` in a copy of the image (a mutant), which the scan
    must find.

## Result (`check.py`, exit 0; `result.json`)

| Discriminator | Observation |
|---|---|
| D1 | The mode-2 arm reaches `007EE7EF 41 89 89 38 01 00 00  mov [r9+0x138],ecx` (7 B). `007EE7F0` is byte 2 of it, **not** a reachable boundary. The 57-B walk has no problems and three `ret` exits; the 48-B walk fails. |
| D1, as listed | From `007EE7F0` the bytes decode as `mov [rcx+0x138],ecx; xor eax,eax; ret`. That stores the **receiver pointer's own low dword**, where the reached path stores the computed `[[rcx+0x60]+0x18] - edx` through `r9 = rcx`. It is a different instruction, not an entry into the same one. |
| D2 | **`007EE7F0`: zero producers** of every kind. `007EE7EF`: zero. |
| Controls | `007EE7C0`: the LEA is found. `007EE730` and `007EE800`: their `.pdata` begins and their LEAs from `007EBAD0` are found. The mutant's planted call is found. |
| D2, `.rdata` value | One further `007EE7C0` hit, a dword `0x006CE7C0` at `00D8A838`, is recorded, not hidden. It sits in a 16-slot run with an 8-byte stride, and **none of the other 15 values is a listed entry**. That is a coincidental value, not a code table. |

**Why the candidate measured 48 B.**
- `007EE730`'s `ret` sits at `007EE7BD`, followed by `cc cc`.
- The gap measurement ran from `007EE7C0` to the next listed entry. That was the false
  `007EE7F0`: 0x30 = 48 B.
- So **the false entry is what truncated the candidate.** The two defects are one defect.

**Why the absence of a `.pdata` entry does not discriminate.**
- `007EE7C0` is a frameless leaf (no stack adjustment and no saved registers). x64 leaf functions carry no
  RUNTIME_FUNCTION.
- The same absence therefore holds for the real body and for the false entry alike.
- The decision rests on D1 plus D2.

**Prior independent observation.** SWE2-AUDIT-SPEC's shadow audit (inbox, 2026-09-14) already
recorded:
- "Listed `FUN_007ee7f0` (9 B) lands mid-instruction inside a coherent unlisted body at
  `007EE7C0`; no .text callers …, no .pdata, no pointer refs";
- `the-code-the-function-list-does-not-contain.md` names it among the "phantoms" the instrument
  correctly emits no row for.

This package extends that observation in three ways:
- it widens the producer classes (DIR64, absolute qwords, image-relative dwords, `rel8`,
  exports);
- it adds live controls and a mutant;
- it binds the extent at 57 B.

## `007C2A29`: code and inline data kept apart (ASTRA's second point)

The 47-B block after `007C23C0` (1,641 B listed, ending at `007C2A29`) is laid out as follows:

| Span | Bytes | What it is |
|---|---|---|
| `007C2A29`–`007C2A2F` | 6 | Code: `call 00809728` (`__report_rangecheckfailure`), then `int3`. |
| `007C2A2F` | 1 | Pad: `nop`. |
| `007C2A30`–`007C2A58` | 40 | Inline data: ten image-relative dwords, every one targeting the predecessor. The predecessor's own `007C27F2 mov ecx,[rdx+rax*4+0x6A2A30]` reads them. |

The compiler's `.pdata` chain for `007C23C0` runs `007C23C0`…`007C2A23`–`007C2A58`, so its
**native unwind extent ends after the table**.

**Extent convention (owner ruling):** extend the predecessor, and add no body. Record two
extents:
- the **instruction extent** `[007C23C0, 007C2A2F)`;
- the **native (unwind) extent** `[007C23C0, 007C2A58)`, whose last 41 B are owned pad and
  inline table data.

Instruction censuses slice the instruction extent. Byte-coverage accounting may use the native
extent, but never counts the table bytes as instructions.

## Wrong interpretations rejected (the regression)

`check.py` asserts against each of these. They cannot re-enter without the check failing:

- **W1** — `007EE7C0` is a 48-B body.
- **W2** — `007EE7F0` is an independent or alternate entry.
- **W3** — all 47 B at `007C2A29` are executable tail.

## Limits

- The check is static only. It proves no runtime reachability or call frequency for `007EE7C0`.
  The LEA at `007EC4F1` shows that `007EBAD0` takes its address, which is an address reference,
  **not** an invocation or a stored-pointer lifetime.
- Indirect routes stay **unknown**, not absent. A computed address (base plus offset) would evade
  every producer class above.
- That computed-address caveat applies to any entry in the image. Against it stands the
  instruction-overlap fact: an MSVC-emitted entry never shares bytes with a preceding
  instruction.
- The 9-B listed row's 1,583-character GZF comment and its Audio ownership tags are not read
  here. They belong to the Audio owner's consumer update.

## Consumer propagation state: PENDING REVIEW, then PENDING PROPAGATION

Record: `_index/candidates/uc1-extent-collision-consumer-check.md`. Nothing below is applied
before AUDIT-SPEC accepts the ruling.

## Reproduce

```
python "Database/FFXII TZA/_experiments/evidence/uc1-extent-collision-opus/check.py"
```

The check needs `pefile` and `capstone`, and the certified EXE at `Tools/work/exe/FFXII_TZA.exe` (sha256 `73461d08…21f8`).
Exit 0 means every assertion held; `result.json` is rewritten deterministically. Inputs and
outputs are sealed in `manifest.json`.

**DB_GOAL=NOT_MET.**
