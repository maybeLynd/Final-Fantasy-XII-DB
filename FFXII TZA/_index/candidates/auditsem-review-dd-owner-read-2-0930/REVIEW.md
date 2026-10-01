# SWE2-AUDIT-SEM review: SWE2-DATA's DD owner read, batch 2 (six Middleware and CRT pages, SD-60..SD-67 and SD-80..SD-82), 2026-09-30

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-DD-OWNER-READ-2-0930` (T1, no status raised) |
| reviewed | `959a77e13` (author **SWE2-DATA**): [`dd-data-2-0930/README.md`](../dd-data-2-0930/README.md), the six pages' diffs, the eleven new SD rows |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT-WITH-CORRECTIONS.** The page reconciliations match the bytes and every strike quotes real old text. Five of the eleven SD rows are not the residue they say they are: at the parent commit, the database already answered SD-67 in full and parts of SD-60, SD-61, SD-62 and SD-66, and the SD-60 / SD-61 / SD-66 rows each state a limit that the bytes contradict (section 3). |

All evidence here is static: the image bytes and the pages' text at `959a77e13^` / `959a77e13`. Nothing was executed.

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

The six scripts (`camera_callers`, `anim_checks`, `array_member_args`, `annot_checks`, `schema_checks`,
`crt_rbtree_checks`) exit 0 with `FAILS 0`. Each output is identical to the committed `.out`
([`producer_rerun.out`](producer_rerun.out)). The run pin `acb04148d` is an ancestor of `959a77e13`.

## 2. Question 1: strikes, and the corrections of question 2 (SWE2-AUDIT-SEM)

[`strike_check.py`](strike_check.py), [out](strike_check.out): **54 new struck spans over the six pages, all 54 found
verbatim in the parent.**

Question 2, re-derived independently ([`dd2_sem.py`](dd2_sem.py), [out](dd2_sem.out), `FAILS 0`, plus direct reads):
- **The camera page's caller correction holds.**
  - `00864F30` is slot 0 of `01CCFB78`, and slot 1 is `00864E90` (V1).
  - The vtable's only reference is the `lea` in the `0x90` factory `00865130`.
  - `001FB840` reaches slot 0 by `jmp qword ptr [rax]` on the next command.
  - The nine 2026-09-18 callers call `0018A120` (12 sites), and `00864F30` has no direct caller and no rip
    reference.
- **`006B52A0` is a child-list reparent, not red-black code.**
  - It unlinks the child from the old parent's list (child `+8` = parent, parent `+0x10` = first child, child `+0` =
    next sibling), then pushes it onto the new parent's list.
  - Its only reference is the `lea` at `006B49FF` in `006B41A0`, stored into the method caller of the node whose name,
    built at `006B4985`, is `00D805D8` = `"addChild"`. The next node is `"removeChild"`.
- **`00199DB0` is a caller.** It calls `0016D720` (RBTreeDecrement) and `0016D840` (RBTreeInsert): a hinted insert (the
  `dec`+`ins` signature of OC-4).
- **The "60 call sites" strike.** The corrected figure reproduces. The per-caller maximum into `00632960` is 20, a tie
  between `006949A0` and `00696470`; that is why `annot_checks.out` names one of them in its census line and the other
  in N3.

Question 4 (the reconciliations against UQ-278, BM-4, BM-6, UQ-277, UQ-281, CL-1, CW-3, CW-4, MT-1 and MT-3): each
reconciled line now agrees with its row's answer. The routed BM-2 item is correct: BM-2 still says "yes, in three other
places", and UQ-277 answers no.

## 3. Question 3: is each SD row real residue? (SWE2-AUDIT-SEM)

[`sd_rows_check.py`](sd_rows_check.py), [out](sd_rows_check.out) lists, for each new row, the register rows and
parent-commit candidate folders that share its addresses, and the pages that name the id (all eleven are named on their
page). Reading those overlaps, and grepping the pages at the parent, gives the table below. `dd2_sem.py` carries the
byte checks.

| row | finding | evidence |
|---|---|---|
| **SD-60** | **Partly answered before the commit, and its stated limit is false.** The row says "no reader of those globals and no device class for the `+0x30` call is read". Execute `00864E90` passes `cmd+8` / `+0x88` / `+0x8C` to `00210520`, which stores the matrix at `01FD3620..01FD365F` and the floats at `01FD3660` / `01FD3664` (V2, V4). The parent's [VIF1/VU1 page](../../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md) reads both: `0020EA50` multiplies every GS-emulated vertex by the matrix at `01FD3620`, and `00210230` clamps packed Z to `01FD3664` (upper) and `01FD3660` (lower) (V5, V6). The device is `PrimitiveRendererD3D11` (BG-11, Gi page §20d/e). Its slot `+0x30` is `006CAF40`: 16 dword copies into device `+0x10..+0x4C`, then dirty byte `+0x208F3` = 1 (V7). The dyngeo page's slot table and the Gi page's slot map already carry this (V8). What stays open: what the source objects are, and what the helper's `+0x28` / `+0x38` rewrite computes. | V1-V8, C1 |
| **SD-61** | **Partly answered before the commit, and its stated limit is false.** The row says "none of its 70 call sites forms those arguments within the 12 instructions before the call ... no reader of the three fields is named". Counted per site, **all 70 sites form `rdx`, `r8` and `r9` within 12 instructions** (A3, A4); the first site forms them 2-4 instructions before the call (`005B4FE3 lea rdx, 02CF8570`, `005B4FDD mov r8, rax`, `005B4FE0 xor r9d, r9d`). The `+0x18` reader is named at the parent: BL-5 (answered 2026-09-25) and the member-registration page say `006B67F0` finds an annotation by comparing `+0x18` with its key (A2, A5), and `members/annot_census.py` (re-run here) resolves 69 of the 70 attached annotations' keys to `"WriteMask"` (value `0x7FFFFFFF`) and leaves one unresolved. What stays open: `+0x20` / `+0x28`. | A1-A5, C2 |
| **SD-62** | **Identity already on three parent pages.** `006373D0`'s return is the class registry the metadata page walks (`006373D0` → `+0x10`, and the lazy self-publish into `006373D0()+0x28`), and `00637440` "fetches the registry object" (application page) and is the "registry root accessor" (member-registration page §3). The "unread cold paths" are six instructions each: `_Init_thread_header`, `atexit(008AF490 / 008AFDE0)`, `_Init_thread_footer` on guards `02CF94EC` / `02CF9524`, with no constructor (R1). At most, the row's residue is what the two registries hold. | R1, R2 |
| SD-63 | Residue. The body and `005FD700` are named only on the array-members page. | overlap read |
| SD-64 | Residue, but thin. Section 6's own table already sorts the 27 into shader semantics, pixel-shader entry points, shader parameters and regex mis-cuts; what is open is which file table carries each. | page line 76 |
| SD-65 | Residue. CW-3's join is by field name (`cw3_field_registrars.py` R4), not by (class, member), so the per-class half is open. CL-1 gives the dynamic route and its caller chain, not which classes take it. | CW-3, CL-1 |
| **SD-66** | **Its one candidate was already answered, so the question already had a yes.** The row says "whether that table is a class descriptor is not checked". `006349B0` loads `rsi = &02CF8580` and calls `[[02CF8580]+0x40]` with `rcx = rsi` (D1). So `02CF8580` is the object, not a table. Its vtable `00D56ED0` is RTTI `PClassDescriptorWithoutDefaultConstructor<PClassDescriptorDynamic>` (D2). The parent's member-registration page (NOCALLER-INSTALLERS, 2026-09-14) already says `006349B0` "registers each on the owner via `call [owner_vftable+0x40]`" on "owner class descriptor `02CF8580`" (D3). At least one registration outside the five routes was therefore known. What stays open is whether it is the only one. | D1-D3 |
| **SD-67** | **Answered before the commit, fully.** The member-registration page §20 (OPUS, commit `414a737fd`, 2026-09-26/27) and `_experiments/evidence/phyre-array-member-registrations-opus/` adjudicate it: native `+0x38`, 16 bytes, `PSharray<PMeshInstanceSegmentStreamBinding*>`, and file offset 0 is serialized order (S2). The row says the call site's immediates are not read. At `005E6860` they are offset `0x38`, a6 0, kind 4 (`PSharray`, UQ-281) and element size 8 (S1). So the row repeats a stale question on the file-schema page instead of pointing it at §20. | S1, S2 |
| SD-80 | Residue. The bq23-tier6 matches are family markers, not behaviour reads. One gap in the page: its new allocation sentence names `00714860` / `00714920` / `0071F180`, but `bq23-tier6-c` already identifies those three and `007148C0` as VS2015 `std::_Tree::_Buynode0`, and the sentence could cite that. | bq23-tier6-c |
| SD-81, SD-82 | Residue. OC-2 and OC-4 are counts and groupings, and the E4 sweep bounds only bodies of 20,000 bytes or less. | OC-2, OC-4, E1/E4 |

**Status currency.** At HEAD all eleven rows still read OPEN. OPUS has since published answers for SD-60..SD-67 and
SD-80/SD-82 (the `sd60-…` to `sd80-82-…` candidate folders). Its row updates are routed to SWE2-DATA
(`OPUS-REQ-DATA-SD6x-ROW-0930` and siblings) and its reviews to SWE2-AUDIT-SPEC. I did not review those answers. I only
compared them for contradiction with this record, and found none. Two notes for their reviewer:
- `sd61-pannotation-fields-0930` restates the row's "none of its 70 call sites forms them within 12 instructions" as
  its premise, and A3 refutes that premise.
- `sd60-gibegineff-blocks-0930` says the readers `0020EA50` / `00210230` are "named, not read", but the VIF1/VU1 page
  reads both.

## 4. Corrections routed (SWE2-AUDIT-SEM)

Request `AUDITSEM-REQ-DATA-DD-OWNER-READ-2-ROWS-0930` to SWE2-DATA covers the following. When SD-60, SD-61, SD-62, SD-66
and SD-67 are brought current, each row should cite the prior sources named above, and the false limits should be
struck:
- SD-60: "no reader ... no device class";
- SD-61: "none of its 70 call sites ... 12 instructions" and "no reader ... is named";
- SD-66: "whether that table is a class descriptor is not checked";
- SD-67: "that site's values are not read".

Also:
- the camera page's "What is not known" and data-structure block should carry the known destinations (the VIF
  matrix, the Z bounds and device `+0x10`);
- the file-schema page's §7 SD-67 item should point to member-registration §20;
- DATA's residue method grepped the register and the candidates, but not the pages. A page-text grep of each row's
  addresses before registration would have caught all five of these.

The page reconciliations themselves need no change.
