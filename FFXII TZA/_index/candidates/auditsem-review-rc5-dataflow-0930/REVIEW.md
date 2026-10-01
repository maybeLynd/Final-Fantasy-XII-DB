# SWE2-AUDIT-SEM review — FABLE's RC-5 operand dataflow (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-RC5-DATAFLOW-0929` |
| reviewed | `63f4b8f89` (author **FABLE**) — [`rc5-operand-dataflow-fable-0929/README.md`](../rc5-operand-dataflow-fable-0929/README.md), `rc5_constprop.py` |
| image / data | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`; the `us` decompile under `Tools/work/FABLE/pub140-scratch/corpus/us` |
| **verdict** | **ACCEPT-WITH-NARROWING** — the propagation is sound for what it models, but two of its premises do not hold everywhere: it does not model a second function stepping the same counter while the first waits (97 of the 346 "exact" sites), and native code **does** write file-class storage, at manager initialisation (§2, §3). The `debug_eventload`, `+0x24` action-word and FST items are not affected. |

## 1. Producer checker re-run (SWE2-AUDIT-SEM)

`rc5_constprop.py`: exit 0, `FAILS 0`, output identical to the committed one — 405 sites, the 20 constant controls
reproduced, no unsound file ([`producer_rerun.out`](producer_rerun.out)).

## 2. Question 1 and 2 — soundness, and what the controls cover (SWE2-AUDIT-SEM)

The design is as described: file variables only, a pure-expression backward parser, `0x52`–`0x57` and `0x5A`–`0x5C`
taking both edges, non-convergence to TOP. One property is not modelled. **Other functions' stores are merged only at
function entries** (`entry[k]` in the loop at lines 141–200). Inside a function, a value computed after a store stays
exact across every wait on the path. A file variable is shared by every actor of the file, so a counter that another
function also steps can change while this one is suspended.

My own parse of the decompile ([`rc5_interleave.py`](rc5_interleave.py), [out](rc5_interleave.out)) finds 12 files
where a `startscene(file_var_…)` counter is also assigned by a second function. In 8 of them, the producer reports
**97 exact sites** (dgl_g0100 50, gil_c0201 8, grm_c0101 8, hne_b0100 6, hne_b0101 7, mrm_c0100 7, mrm_c0101 7,
rui_c0100 4). **The concrete case is the record's own example:** in `dgl_g0100` the request-entered function at `+0x408`
does `var = var + 1; startscene(var)`, which the record calls the open fact. Yet the main function's 50 sites, each
`var = var + 1; startscene(var)` with waits between steps, are reported as the exact values 8, 9, … 47. If the `+0x408`
function runs between two of those steps, every later value shifts. The 20 constant-site controls test the evaluator on
constants and cannot see this. The all-reached control is about coverage, not interference.

## 3. Question 3 — "native code never writes file-class variables" (SWE2-AUDIT-SEM)

The storage-class page's §3 ("Key addresses") does not say this, and the image contradicts it. `0026D3E0`, which
`0026CE60` calls at `0026D300` during manager initialisation, walks the list at `[manager + 0x78]` and dispatches each
entry by class `(desc >> 24) & 7` ([`patcher_class.py`](patcher_class.py), [out](patcher_class.out)). **Class 1
(file) goes to `0026D491 mov rax, [r14 + 0x40]`** — the file block the page assigns to class 1. The entry is then
`memcpy`-ed to `block + (desc & 0xFFFFFF)` at `0026D4D5`. So native code writes file-class storage from authored
initial-value entries at load.

That matters for the two results that rest on initial values:
- the entry state `{0} ∪ stores`;
- the **13 `eventread_e8` sites read as set id 0** from the file home's initial bytes.

Whether any shipped entry of `ctrl.ebp` / `evctrl.ebp` targets those arrays is not checked here.

## 4. Narrowings (exact wording; FABLE applies them) (SWE2-AUDIT-SEM)

- **N1 — the result table and "The 341 + 5 exact sites are constants in effect".** Replace with: *"249 sites are exact:
  their counter is assigned in one function only. 97 more (in dgl_g0100, gil_c0201, grm_c0101, hne_b0100, hne_b0101,
  mrm_c0100, mrm_c0101, rui_c0100) are exact along their own function's path, provided no other function of the file
  steps the same counter between steps. That is the same request-order fact as the 40 unbounded sites."* The RC-5
  handoff "346 of 386 … exact" becomes "249 exact, 97 exact under no interleaving, 40 unbounded".
- **N2 — Limits, "Native writes", and the eventread_e8 paragraph.** Replace "The model assumes native code does not
  write file-class variables … It rests on the storage-class page's section 3" with: *"Native code writes file-class
  storage once, at manager initialisation, through `0026D3E0` (class 1 → `[manager+0x40]`, `memcpy` at `0026D4D5`) from
  authored initial-value entries. The model takes initial values from the file home's bytes, so the 13 set-id-0 sites
  are 0 only if no such entry targets their arrays (not checked)."*

## 5. Not reviewed here (SWE2-AUDIT-SEM)

The `debug_eventload` census (274 constant sites), the `+0x24` action-word enumeration, the FST `-1` sets and the
loader skips were read, but not re-derived.
