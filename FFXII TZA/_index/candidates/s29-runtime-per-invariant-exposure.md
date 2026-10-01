# S-29 runtime: per-invariant stub exposure for EXP-064 (OPUS, 2026-09-25, block 301)

*Drafted by a delegated OPUS pass and reviewed before publication (block 301): its concrete address claims were spot-checked against the image; see the block-301 inbox entry for which.*

**Row:** S-29 inventory and equipment. Runtime **MIXED** — *"EXP-064 executes the original execution-resource
preparation (five-arg inventory request at `003008A0`, pointer resolver) under isolated original-code replay … no
per-invariant stub-exposure analysis yet"*. Binding gap: *"runtime only — types re-scored MET 2026-09-25 after block
217's VARIABLE stride rule; nothing executed — runtime is ASTRA/ORACLE's gap"*. Contracts (column 6 of
`important-subsystems.tsv`), both under `12-Items-Equipment-Shops-License/`:
- `CONTRACT-inventory-class-storage.md`: §4 has two preconditions, one invariant and one postcondition;
- `CONTRACT-equipment-compatibility.md`: EQ-1..EQ-8.

Evidence class: isolated original-code replay (Unicorn, `live_game: false`). This note scores nothing.

**What the record is about.** EXP-064's subject is `0030EF20`, the item-use / gil **preparation** routine (205 B,
`ret` at `0030EFEC`). **No contract in the database lists `0030EF20`** (grep of every `CONTRACT-*.md`). The record
names `CONTRACT-inventory-class-storage.md` in its front matter because `0030EF20` calls that contract's ±1 entry
`003008A0`. **That call is a no-effect stub.** The record's own `contract_coverage` says so: *"inventory is a
no-effect stub, so native class storage and item deduction are untested"*.

## Substitutions per record

Read from `_experiments/evidence/EXP-064-resource-payer-controls/check.py` (lines 30–79) and its `disassembly.txt`.

| record | runs as shipped | substituted |
|---|---|---|
| **EXP-064** (`evidence/EXP-064-resource-payer-controls/check.py`) | `0030EF20` whole (205 B); `0020E600` pointer resolver (10 B: `mov eax,ecx` / `add rax,[01F83530]` / `ret`) | **Application stubs** (no-effect; log args; clobber `rcx`/`rdx`/`r8`–`r11` to `0xBAD0BAD0`; `eax` = configured cost, gil, or `0xAABBCCDD`): **`003008A0` inventory ±1 entry — a listed entry of `CONTRACT-inventory-class-storage.md`**; `00309060` gil cost; `00253690` gil getter; `00254EE0` gil setter. **Fixtures:** registry slot `02EBF138` → synthetic header (`+0xC` = `0x10000`, `+8` stride), codec base `01F83530`, synthetic unit / stats (`+0x698`, `+5` kind, `+0xDC8`, `+0xE58`) and action row (`+0x1E` category, `+0x22` item). **Mutant:** `0030EF9D` `je` → `jne` (detected). **No import bridges** — `0030EF20` makes no IAT call |

## Per invariant

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| inventory **precondition**: class `<= 14` (`00309F51`, `00309446`); index `< itemCount`, signed compare (`00309F80`–`00309F82`) | **not by EXP-064.** Neither `00309F30` nor `00309440` is called by `0030EF20`; in the direct-call graph (`Tools/work/graph/edges.tsv`), the only path toward them from any of the four stubs is `003008A0` → `00309F30` (→ `002FD970`), and `003008A0` is stubbed | coverage, not exposure. The stubbed entry stands where the validated path would start |
| inventory **precondition**: storage pointers `+0x08`/`+0x20`/`+0x30` bound; every handler null-tests | not executed | coverage, not exposure |
| inventory **invariant**: handler and the `+0x10 : +0x3C` ratio must agree | not executed. A static claim about the descriptor table `01EEBCC0` | coverage, not exposure |
| inventory **postcondition**: a mutate leaves the count `<= 99` (clamp `002FD204`–`002FD20F`) | **not executed.** `002FD150` would be reached only through `003008A0` → descriptor `+0x50`. The stub skips exactly this | coverage, not exposure. What the stub skips *is* the claimed behaviour |
| equipment **EQ-1..EQ-8** | not executed (the contract's own §13: "None. No experiment executes these bodies") | coverage, not exposure |

**What EXP-064 does measure on this row's contracts** is a caller-side fact, not a §4 claim. `0030EF20` calls the
contract entry `003008A0` with the argument vector `(item, -1, 0, 1, 0)`, the fifth dword at callee `RSP+0x28`.
It stores the reservation word `unit+0xDC8` **before** that call (`0030EF93`, then the call at `0030EFB0`). That is
an interface observation at the entry's boundary. No substitution can change it, because it is argument setup in
the real caller (`0030EF9F`–`0030EFAD`).

## Out-of-cell execution of this row's inventory contract (cross-row finding)

EXP-092 is S-30's record; its front matter names `CONTRACT-bazaar-unlock-and-purchase.md`. It runs **six of the
inventory contract's bodies as shipped bytes with zero application stubs and no IAT call**
(`evidence/bazaar-callees-exec/check.py`: `BODYSTUBS = []`, whole image mapped):
- `003008A0` (a listed entry), `00309F30`, `00309440` (a listed entry);
- `002FD8D0` and `002FD970` (listed entries);
- `002FD150` (a listed entry, the packed mutator).

Fixtures plant the family data pointers `fam+0x08` / `fam+0x20`, which are runtime-null in the image.

| inventory §4 item | EXP-092 case(s), read from `check.py` / `result.json` (not re-run) |
|---|---|
| postcondition ≤ 99, **at the contract's own cited site** `002FD204 cmp ecx,0x63` (the `r9 == 3` byte arm, `fam+0x20`) | `sg-byte-clamp`: `003008A0(0x1005, 5, 0, 3)` over byte `0x60` → stored `0x63`; mutant `mut-bclamp-63->62` at `002FD20A` detected. `sg-add-clamp99` drives the u16 arm's `0x63` clamp (`0x10 + 100` → `0x63`) |
| precondition: class `<= 14`, index bound | `famd-highnib` (`0xF001` → `-1`), `famd-oob` / `sg-oob` (`0x11A4` → `0` / `-1`), `famd-sentinel` (`0xFFFF`) |
| storage-bound precondition (null-test) | `tq-nohandler`, `tq-nohandler-tab` cover the handler-null arm of `0030ADC0`. Whether a case drives a **null `+0x08`/`+0x20`** through the handlers was **not read** |
| handler ↔ ratio invariant | not a runtime claim; not executed |

EXP-092's substitution set for these bodies is **fixtures only**. It is not named in S-29's cell.

## Findings and contradictions

- **The runtime cell's wording can be read as `003008A0` executing.** It says "five-arg inventory request at
  `003008A0`". What executes is the *request*, meaning the caller's argument setup; `003008A0` is a stub.
- **The binding gap's "nothing executed" is right about the §4 claims and loose elsewhere.**
  - Against the row's own runtime cell, EXP-064 does execute shipped code (`0030EF20`, `0020E600`), none of it a
    body of either contract.
  - `CONTRACT-inventory-class-storage.md` §13 records a differential pilot, `diff_inventory_query.py` (170
    commands, 0 mismatches), that runs three of its entries as shipped: `00309440`, `002FD8D0`, `002FD970`. That
    pilot is not an EXP record and is not named in the cell. Its substitutions were **not read** here, and the
    contract says the mutators, the clear-all and the ±1 entry did not run in it.
  - EXP-092 (above) runs the ±1 entry and the mutator stub-free. The inventory contract's own §13 lists only
    EXP-064 among the records that name it, and still says the mutators and the ±1 entry "did not" run. That was
    true of its pilot, but the corpus no longer supports it.
- **EXP-064's subject has no contract home.** `0030EF20` is named in no contract. The item page's prepare pseudocode
  is what the record corrects (the header/stride dependency precedes the null-unit guard).

## For the scorer

- EXP-064 substitutes **4 application stubs**, one of which is **the inventory contract's own entry `003008A0`**,
  plus **fixtures**. It has **no import bridges**.
- **Exposure: empty, because the record executes no invariant of either contract.** Every inventory §4 item and
  every EQ-1..EQ-8 is **unexecuted** by this row's record. This is coverage, not exposure.
- For the inventory **≤ 99 postcondition**, the unexecuted behaviour is precisely what the `003008A0` stub skips.
- The only contract-adjacent fact executed is the caller's argument vector into `003008A0`. It is outside every
  stub's reach.
- **Cross-row:** S-30's EXP-092 executes the inventory contract's bounds preconditions and its ≤ 99 postcondition
  at the cited site `002FD204` as shipped bytes, with **no application stub or import bridge** (fixtures only). The
  clamp constant mutant at `002FD20A` was detected. That record is not in S-29's cell; whether it may be credited
  here is the scorer's call.
- Contradictions: the cell's `003008A0` phrasing, and the binding gap's "nothing executed" (see above).
- `live_game` is false.
