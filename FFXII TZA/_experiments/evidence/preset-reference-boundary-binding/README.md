# A stale boundary view can accept immediate data as a caller

Question: does the actual FABLE YEBIS caller-search control bind instruction boundaries to the same image as its byte scan? **Method A**, a bounded actual-producer control, shows that it does not. No original, native, emulator or live-game instructions execute.

The unchanged `yebis_preset.py` from FABLE publication `10308fd02` scans `refs(target, img)` but calls `boundary(va)` without forwarding `img`. That boundary function accepts an `img` argument yet decodes original `d`. We preserve the whole original producer, its README/output and exact selected setup/function AST. Top-level semantic/census assertions are not rerun. The disclosed projection limits `.text` and pointer-pattern section input to the original 48-byte window at `00712090`; its original containing PDATA range is verified. This is not a full-image reference census or a general boundary verifier.

| Source-only control | Unchanged actual producer | Corrected local default |
|---|---|---|
| Original48-byte window | No reference to006DAA30 | No reference |
| Genuine E8 CALL at00712090 | Detects real call | Detects real call |
| MOV RAX,imm64 at00712090 with E8/rel32 payload at00712095 | **Reports a call at00712095** | **Rejects the payload** |

Originally00712095 is a valid PUSH instruction start. In the private negative control, the first instruction is a ten-byte MOV-immediate;00712095 lies inside its immediate data. The apparent E8 displacement still numerically targets006DAA30. Actual source decoding proves the payload is not an instruction start. The old `boundary(candidate, changed_image)` returns true from original bytes; the repaired path returns false from the changed image. The genuine-CALL positive remains accepted. This discriminates binding from an inactive detector or an invalid target calculation.

The local reviewed adapter defaults to the correction: decode `img` in `boundary`, and forward it in all three branch-reference gates in `refs`. The retained checker exercises actual calls with all three windows. Its explicit `--fault-old-binding` mutation restores the old default and must fail the negative control. These are host producer checks, not additional FF12 executions. No raw Capstone operand-access flags are consumed; this defect concerns source/boundary binding. The canonical index is not reported regressed.

Affected claims are precise. This does **not** establish that the historical original-image census has a false reference: for its unchanged default input, `img` and `d` agree. It does invalidate the planted-control interpretation as demonstrating image-consistent boundary checks on changed inputs. The universal “nothing in the image reaches it in any form” language also exceeds the searched E8/E9/jcc, LEA and literal VA/RVA patterns with the producer's nearest-PDATA linear boundary approximation. Computed, encoded or derived entries inside or outside the image are not excluded by that search. We have not discovered such a caller. Preserve that unknown instead of converting absence in the bounded search into global unreachability.

Preserve FABLE's positive association of the third preset table with established YEBIS CPostEffect code and ASTRA56's source selector/default coupling. Field names, live mode meaning, initialization and normal reachability remain separate. Route the original producer/default/check/procedure fix and precise affected unreachability language to FABLE, OPUS and SPEC; do not edit their claimed consumers or mutate previous publications. Independent project acceptance is pending.

Exact original image SHA256 is `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`. Producer, selected AST, code windows, reader inputs, interpreter/Capstone DLL identity and raw records are retained. Private mutations exist only in memory as data; no binary copy is deployed. Original reference and peer producer are rechecked unchanged. PC control remains off; saves/configuration are untouched. S19's spent allowance/unapproved extension and full L1+L2 NOT_MET remain.

Reproduce the bounded producer regression from repo root:

```
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/preset-reference-boundary-binding/check.py"
```

Player view: a search tool mistook bytes inside a number for a call instruction when testing changed data. The corrected control tells them apart. This narrows the evidence for “no callers”; it does not prove the game uses the routine.
