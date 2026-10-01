# RC-4: the capture machine's entry states have no writer in the image (OPUS, 2026-09-30)

Input for `RC-4` ([the 282-command parameter console](../../../00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md)
section 7). SWE2-CONTRACT registered the row, so it applies this. Static evidence only (shipping image `73461d08…`).

## The machine is self-driving, and it idles at 0

`00187860` returns at once unless the render object's `+0xDB8` is set. It then switches on `+0xDAC` through an
8-entry table at `001878D5`–`00187925`:

| state | arm | next state |
|---:|---|---|
| 0 | `001878DF`, return | 0: **it never leaves 0 by itself** |
| 1 | `00187891` | 3 (and `+0xDA8 = 6`) |
| 2, 5 | `001878D5` | 0 |
| 3 | `001878AB`: `00185FB0`, then | 4 (and `+0xDA8 = 6`) |
| 4 | `001878CD`: `001876E0`, then | 0 |
| 6 | `001878E5` | 7 |
| 7 | `001878F5`: `00185FB0` once (flag `01F7F5AC`), then `001876E0` + `00185FB0` on every later pass | 7 |

So a single capture is the sequence 1 → 3 → 4 → 0, and a series capture is 6 → 7 → 7 …. The press on row 4 or row 5
has to write **1** or **6**.

The frame routine `00187950` calls the machine at two sites with complementary gates. At `00187A2E` it runs when
`+0xDB8 ≠ 0` and `+0xDAC ∉ {3, 4}`; at `0018857C`–`00188598` it runs when `+0xDB8 ≠ 0` and `+0xDAC ∈ {3, 4}`. So once
`+0xDB8` is set, the machine runs every frame; no extra call is needed to reach it. `+0xDB8` is the constructor
`00184F20`'s byte argument (`0018502B`), passed down from `0017D000` → `00189000`, where `0017D056` loads the global
byte `01FD4A9C`.

## Nothing writes 1 or 6

A byte-pattern scan finds every instruction in `.text` whose displacement or immediate is `0xDAC`:
- **Render-object writes:** only the constructor (`00185020`, 0) and the machine's own four stores (`00187891` 3,
  `001878B3` 4, `001878D5` 0, `001878E5` 7).
- **Reads:** `00187873`, `00187A1D`, `00187714`, `00188281` and `00188587`.
- **Other objects:** `001CCE9A` is in the console menu's own constructor `001CCB20`, which clears *its* object's
  `+0xDAC`; `0047E4E7` writes another object's init; `0079F47A` is a read.

A second scan looks for any store starting at `+0xDA5`..`+0xDAB` that could cover `+0xDAC`. It finds only dword stores
at `+0xDA8`: the machine's `+0xDA8 = 6`, plus other objects (`0041E3A0`, `0041E550`, and stack arguments in
`0044EDD0`, `004518D0`, `00452540`). None of these is a qword or vector store over `+0xDAC`.

So no instruction writes the machine's entry states. By every write form a displacement or immediate scan can see, a
press on rows 4 and 5 cannot start a capture. That matches UQ-23: no caller presents ids below 12 to the dispatcher.

## Not excluded

- A write through a pointer derived from the render object at another offset, for example `lea rax, [obj + 0xD00]`
  then `mov [rax + 0xAC], 1`. The scans do not see that form. A census of pointers the render object hands out would
  close it.
- An external write (a debugger or a mod).

Neither exclusion needs a live session to test. The first is a static census, and the second is outside the shipped
code's behavior.

## The derived-pointer census (OPUS, 2026-09-30)

Two instruments beside this README answer the "Not excluded" item above: a write through a pointer the render object
hands out at another offset.

**`rc4_derived.py`: image-wide and per function.**
- Every function in the catalogue (38,161) runs through the value-flow engine of
  [`k14-closure-stores-0930/k14_actorflow.py`](../k14-closure-stores-0930/README.md). It is seeded with its entry
  registers and callee-saved registers as roots, and every pointer loaded from memory is a root of its own.
- A one-level getter summary carries `obj + K` across a call (114 getters in the image hand out `entry + K` with
  `0 < K ≤ 0xDAC`).
- It lists every store whose effective offset from its root covers `+0xDAC`. The direct form (the instruction's own
  displacement) includes the machine's four stores and the constructor's, which is the control.
- **Derived-offset stores (6 distinct sites image-wide):** none lies in a function that loads the object's global
  `01F7F598` or touches `+0xDAC` / `+0xDB8` directly. Output `rc4_derived.out` / `.tsv`.

**`rc4_flow.py`: interprocedural, following the object itself.**
- The object is `new(0xDD8)` (`00189034`–`00189039`), built by `00184F20` and published only in `01F7F598`
  (`00189067`).
- Roots: every function that loads `01F7F598`, plus every caller of a function whose return value is the object
  (the getter `00189120` and 160 more), to a fixpoint: 161 roots.
- The object is followed into callees under the arguments that carry it; 7,820 bodies are analysed.
- **Control, PASS:** the machine's four stores and the constructor's are found through the flow, from the global,
  through the frame routine, into the machine.

**Result.** No store through an object-derived pointer at a *known* offset writes `+0xDAC`, other than the five known
stores. What remains is the flow's own blind set, listed exactly (`rc4_flow.out`):

| residue class | count | what closing it needs |
|---|---:|---|
| stores through an object pointer whose offset is not known (pointer + index, or a loop cursor over a sub-array) that could cover `+0xDAC` | 66 sites. By value: 34 float or vector stores, 5 stores of a pointer, 1 pointer increment, 4 constants (0, `0x3F800000`), 16 dword stores of an unknown value, 6 qword stores of an unknown value | bound each index or cursor. An aligned pointer's low dword is a multiple of 8, and 0 / `1.0f` are not 1 or 6, so the **22 stores of an unknown integer value** are the ones that matter |
| the object storing pointers to its own sub-objects inside itself (`00184AF0`, `001897C0`, `00189CE0`) | 12 | model loads from those fields as object-derived |
| the object's pointer stored into another object (`001F1E80` → `+0x18`, `0060CE50` → `+0xA8`) | 2 | roots at the loads from those fields |
| virtual calls that receive the object (for example `00187950`'s `call [rax + 8]`) | 38 | resolve the vtables |

So RC-4 stays OPEN, now as a bounded static residue: 22 integer stores, 12 self-pointer fields, 2 escapes and 38
virtual calls. Each is a static question, and none needs a live session.
