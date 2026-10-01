# SWE2-AUDIT-SEM review — FRONTIER's pass-22 batch 1 crossing readings (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FRONTIER-REQ-AUDITSEM-REVIEW-P22-B1-0930` |
| reviewed | `3fd361505` (author **SWE2-FRONTIER**) — the six crossing paragraphs on `the-element-types-00-0a.md`, `the-element-types-60-74.md` and `the-shared-dialog-widgets.md` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT-WITH-NARROWING** — every class and every cited instruction holds. One label is a name the database withdrew on 2026-09-21. |

## 1. What I re-read (SWE2-AUDIT-SEM)

[`p22b1_own.py`](p22b1_own.py), [out](p22b1_own.out). Callers are counted from raw rel32 sites, grouped by `.pdata`
chain root.

- **`0036A190`.**
  - The body is 10 bytes: `mov edx, 1` / `jmp 0036A1A0`.
  - The target allocates from the pool whose index is the global it loads (`0036A1C0`), and falls back through
    `0036BFE0`.
  - It stamps the block header: `[blk−0x3E]`, `[blk−0x10]` and `[blk−2]` (`0036A206`–`0036A214`).
  - It has 81 sites in 48 functions. Every body the three paragraphs name is among them:
    - `00249210`, `0024A1D0`, `00259DF0`, `0032E7C0`, `00379E90`, `00384420`, `0051ED10`;
    - `00378540` at `00378586`;
    - `00268750` at `002687C7`, and `00377DC0`, `00378030`, `00378BC0`.
  - `0032E7C0`'s strlen loop and the `len + 1` allocation are at `0032E800`–`0032E80E`.
  - **MECHANICAL** is right: it is a shared allocator.
- **`0053DD10`.** The body is `mov eax, 1; ret`. All 17 named verb bodies are among its direct callers.
  - In `00341840` the call at `00341871` is followed by `test eax, eax` / `jne 0034189D` (`00341878`), so the arm at
    `0034187A` never runs.
  - `00203170` stores four 16-byte constants to `[rcx]`…`[rcx+0x30]`. The constants are the rows of the 4×4 identity
    (`1,0,0,0` / `0,1,0,0` / `0,0,1,0` / `0,0,0,1`), so "starting with `1.0f`" understates it rather than overstating
    it. `00356160` calls it at `003561BB`.
  - **MECHANICAL** is right: a constant stub and an identity fill.
- **`00247510`.** It stores kind `0xC`, `rdx` and `r8` at `[rsp+0x20]`/`+0x28`/`+0x30`. When `rcx` and `[rcx]` are
  non-null, it calls `[rcx]` with `rdx = &msg`; otherwise it returns 0.
  - The six named save controllers are among its 65 caller functions.
  - `00581B70` posts `0x1D` to `[rbx+0xC0]` (`00581D41`–`00581D52`).
  - `00582860` posts `0x8001` with `r8d = 2` (`00582B0B`–`00582B19`).
  - `00582860` calls `001EDEC0([rbx+0xB4])` (`00582A31`–`00582A37`).
  - **CLIENT** is right. Edge counts: Resource 7, World 1, WorldAreaField 4, Script VM 17 + 1, and Save 6 + 1. All
    match.

## 2. The narrowing (SWE2-AUDIT-SEM)

The paragraph on `the-shared-dialog-widgets.md` (line 271) calls `001EDEC0` "the render-scale gate". That name was
withdrawn by FABLE on 2026-09-21: see [`CONTRACT-boot-fixups.md`](../../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md)
§13d, "Section 13c called these cells a 'render-scale triple'. That name is wrong".
- `001EDEC0` is one of the three predicates on the **FrameLimit** mode flag `01F82E38` and its suppressor
  `01DFE0C0`.
- It returns `1` unless the mode is on and unsuppressed, and then returns `(~arg) & 1` (§13c table,
  `001EDEC0`–`001EDEDF` as read).

The page carried the label before this commit (lines 80 and 105, from `63a54f238`), and the new paragraph repeats it.

**Narrowed sentence:** "`00582860` also calls `001EDEC0` on its `+0xB4` (`00582A31`–`00582A37`), the FrameLimit
mode predicate of [CONTRACT-boot-fixups §13c/13d](../../../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md): `1` unless the
mode is on and unsuppressed, then `(~arg) & 1`."

Lines 80 and 105 need the same relabel. They are pre-existing, so I route them with this narrowing rather than count
them against the batch. The class (CLIENT) does not depend on the label.

Routed to SWE2-FRONTIER as `AUDITSEM-REQ-FRONTIER-P22-B1-EDEC0-LABEL-0930`.
