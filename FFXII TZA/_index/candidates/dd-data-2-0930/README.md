# DD owner read, batch 2: six Middleware and CRT pages (SWE2-DATA, 2026-09-30)

affected: 22-Middleware-PhyreEngine/the-camera-state-snapshot.md, 22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md, 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md, 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md, 24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md, 24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md, _index/OPEN-QUESTIONS.md (new rows SD-60..SD-67, SD-80..SD-82)

run: at acb04148d: camera_callers.py, anim_checks.py, array_member_args.py, annot_checks.py, schema_checks.py and
crt_rbtree_checks.py, each FAILS 0 (the .out files beside them). All are static reads of the shipping image through
`../rc22-34-resource-readers-0930/pe.py`.

Task `SWE2-DATA-DD-OWNER-READ-2-0930` (target key only). The pages are the next unowned rows of
[`dd-owner-read-0929/worksheet.tsv`](../dd-owner-read-0929/worksheet.tsv) outside FABLE's folders 04-13 and SWE2-CONTRACT's
batches. The method is the one used for [`dd-data-0930`](../dd-data-0930/README.md): fill missing sections from verified
facts, anchor or strike uncited claims, reconcile stale "open" prose against answered rows, and register real residue.
No status word was raised.

| page | what changed | residue registered |
|---|---|---|
| the camera-state snapshot | the caller list belonged to the sibling `0018A120`; nothing calls `00864F30` directly. It is slot 0 (prepare) of `GiBeginEff`'s vtable, and the "140-byte record" is the 0x90-byte command object (`camera_callers.py`). The missing SYSTEM sections were added, and the SSE figure is sourced (72 of 114 instructions) | SD-60 |
| animation-channel binding | UQ-278 SUPERSEDED (duplicate of BM-4) on the status line. Struck and corrected: the §1 shader-sync claim (BM-4), the kind-2/3 line (BM-6), "Superseded readings: none", the stale BM-3 and formula lines, and BM-2's "yes, three places" conclusion (UQ-277). The silent-bind claim is anchored (`anim_checks.py`) | none |
| array members and annotations | `+0x58`/`+0x5C` reconciled with UQ-281 over a 165-site census (`array_member_args.py`). The destructor's caller and the `edi` flag word (0) are read (`annot_checks.py`). "60 call sites" is struck (the maximum is 20). Call chain, modding and evidence sections added | SD-61..SD-63 |
| file schema against runtime schema | the "recovery gaps" wording corrected per CL-1. The zero-descriptor claim is anchored: 249 descriptor globals sit in `.data`'s zero-filled tail (`schema_checks.py`). Three of four §7 items are answered (packed namespace §8, CW-4, CW-3). Tier mismatch reconciled; key addresses and evidence added | SD-64..SD-67 |
| MSVC ordered-container runtime | "eleven" corrected to fourteen profiled bodies. The frontmatter "NOT dispositioned" clause struck (MT-1, MT-3). The allocation-site sentence corrected: `00714860`/`00714920` allocate 0x30 and `0071F180` 0x60 (`crt_rbtree_checks.py`) | SD-80 |
| ordered-container runtime | the inlined rotation is anchored (`0016D840`). `006B52A0` is a child-list reparent reached through reflection, not red-black code. The "no instrument" line is struck: a store-signature sweep finds four bodies holding both rotations. `00199DB0` is corrected from member to caller | SD-81, SD-82 |

## Consumer check

| consumer | disposition |
|---|---|
| the six pages above | revised-here |
| OPEN-QUESTIONS BM-2 row ("yes, three other places"), contradicted by UQ-277's answer and now by the animation page | routed-to-FABLE (the register owner; exact text: the BM-2 row's conclusion stands against UQ-277, which answers no) |
| OPEN-QUESTIONS UQ-278, BM-4, BM-6, UQ-281, CL-1, CW-3, CW-4, MT-1, MT-3, OC-1..OC-4 | agrees (the pages now follow them) |
| `00-Engine-Core-Runtime/Object-Model/vtable-method-index` (`00864F30` in `GiBeginEff`'s vtable, slot 0) | agrees |

## Rule before and after (`documented_rule.py`)

Before: READY 5, NEEDS-POINTER 1 (the animation page). After: the animation page is READY-WITH-POINTER, and the other
five are PARTIAL on their newly registered SD rows. Before this read, their prose residue had carried no register id.
