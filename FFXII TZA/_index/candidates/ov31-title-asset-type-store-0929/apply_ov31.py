"""Idempotent patch: OV-31 type-store results into _types, the page and the register.

SWE2-STRUCT, 2026-09-29.  Cell-wise, EOL-preserving (splitlines(keepends=True)); each edit is
guarded by a marker so a second run changes nothing.

    python apply_ov31.py          # apply
    python apply_ov31.py --check  # report what would change, write nothing
    python apply_ov31.py --section-only  # _types + page section 8 only; box and register left alone
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TYPES = os.path.join(DB, "_types", "types.tsv")
FIELDS = os.path.join(DB, "_types", "fields.tsv")
PAGE = os.path.join(DB, "16-UI", "Widget-Object-Model",
                    "the-title-asset-singleton-and-its-distinct-consumer.md")
REG = os.path.join(DB, "_index", "OPEN-QUESTIONS.md")
MARK = "OV-31 2026-09-29 (SWE2-STRUCT"
REC = "_index/candidates/ov31-title-asset-type-store-0929"
T = "WidgetSingleton02AEE4C0"
CHECK = "--check" in sys.argv
changed = []


def load(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read().splitlines(True)


def save(p, lines):
    if CHECK:
        return
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write("".join(lines))


def split_row(line):
    body = line.rstrip("\r\n")
    return body.split("\t"), line[len(body):]


# ---------------------------------------------------------------- types.tsv
ALLOC = ("MIXED - POOL FIRST, HEAP FALLBACK (" + MARK + "). 00244F50 at 003944A4 with `mov ecx, 0xD8` "
         "(0039449F): 0xD8 <= 0x120 passes 00244F77, so the 112-slot pool at *(0208EA58) (stride 0x120) "
         "is scanned and the first slot with +0x40 bit14 clear and +0xA2 zero is taken (00244F90, "
         "00244F99; pooled=1 at 00244FEC). Only when all 112 slots are busy does it fall through to "
         "HEAP 002497B0(0xD8) at 00244FB2 (pooled=0 at 00244FBA). Which class an instance gets depends "
         "on pool occupancy at construction; both paths forward to 002465F0. Was: HEAP - 00244F50 at "
         "003944A4 with `mov ecx, 0xD8`, which allocates (or takes a pooled 0x120 slot from the "
         "0x70-entry pool at 0208EA58) and forwards to 002465F0.")
CTOR_ADD = (" || " + MARK + "): message 1 (003940F2) also sets channel0 bit21 (0039410B, 00394112: "
            "002E1C20(0, 0x15)) and attaches self to UI root *(0208EA28) through the widget contract's "
            "attach entry 00244960 (00394117-00394121), which links it under that root via 00248220 when "
            "+0x10 is null. Every message other than 1, 16 and 18 goes to 005C5230, which is `xor eax,eax; "
            "ret`: per-frame {2}, draw {3,4,5}, pre-destroy {15} and post-release {24} are no-ops here.")
DTOR_NEW = ("RELEASED FROM OUTSIDE THROUGH THE COMMON WIDGET DESTROY 00244F00 (the Widget row's dtor); "
            "the type's own code never passes itself to 00244F00 (" + MARK + "). Direct release sites, "
            "from all nine references to 02AEE4C0 (data_xref_scan, control 02AEE4D0 passes): 00394400 "
            "(`mov rcx,[02AEE4C0]; test; jne 00244F00`, a conditional tail-jump), whose one call is "
            "00582EB5 in the message-18 arm 00582E81 of the 0x5A0 widget handler 00582860 (jump table "
            "00582899/005828A0), taken when that widget's +0xC4 bit 0x10 is set and its byte +0x598 is "
            "zero, behind the nonnull predicate 00394520 (00582EAC); and the 0xF0 sibling "
            "WidgetSingleton02AEE4D0's handler 00394130, whose message-18 arm loads 02AEE4C0 at 00394155 "
            "and calls 00244F00 at 00394161 when nonnull. On 00244F00's immediate path (+0x40 & 0x21 != "
            "0x21) the asset receives {15} (a no-op here), then 00245020 sends {18} at 0024505A to the own "
            "arm 00394097 (0024A680(+0xC8,1); +0xD0 released via 003697F0 and cleared; channel0 bit21 "
            "cleared; 02AEE4C0 zeroed), then 002482E0 returns a pooled slot (+0x40 bit14: bit cleared, "
            "+0xA2 zeroed) or frees via 003697F0 (CONTRACT-widget-object.md section 16). A release site "
            "is not an ownership proof. NOT ESTABLISHED: release through a teardown of the parent root "
            "*(0208EA28) (roots' lifetimes are open on the Widget contract); whether the asset takes the "
            "deferred branch 00244DD0 (+0x40 & 0x21) or 00245020's +0x40 bit 0x20 deferral, which "
            "00248271 copies from the parent root at attach. The +0xC0/+0xC8 values survive in a pooled "
            "slot until the next occupant's 002465F0 memset. The load batch that 00249580 takes records "
            "self at batch+8 (002495B7); its three owner-notify sites (00249456, 0024953B, 0024960B) read "
            "only owner+0x00 and send {16}; nothing in it releases the asset. || (SECTION-04 2026-09-22, "
            "kept) ")
EVID_ADD = (" || " + MARK + ", " + REC + "/ov31_title_asset.py S P J X C O K): COMMON-HEADER "
            "INTEGRATION COMPLETE - +0x00..+0xBF is the embedded Widget row (OPUS 2026-09-27), and every "
            "sub-0xC0 access reached from the cell lies in common widget code on the 00244F00 destroy "
            "chain (00244830, 00244DD0, 00244F00, 00245020, 002448D0, 002473F0, 002482E0), and from the "
            "own-handler seed only the attach entry 00244960 (+0x10). TYPE AREA +0xC0..+0xD7 fully "
            "declared: 4+4+8+8 = 0x18 bytes, the last QWORD ending at the 0xD8 extent; a census widened "
            "to 0x1000 finds no type-specific access at or beyond +0xD8 on either seed. The sentence "
            "above ('Remaining common-header/interior and service/lifetime obligations ...') is narrowed "
            "to the named residue: +0xC4 unread (bounded, positive control passes), parent-root release "
            "and deferral applicability (dtor cell), and real IO timing (OV-29). Readiness left at "
            "SIGNATURE RESOLVED: raising it is the independent-acceptance decision (OV-32).")


def patch_types():
    L = load(TYPES)
    for i, ln in enumerate(L):
        if ln.startswith(T + "\t"):
            c, eol = split_row(ln)
            if len(c) != 13:
                sys.exit("types row has %d cells" % len(c))
            if MARK in c[10]:
                return
            c[4] = ALLOC
            c[5] = c[5] + CTOR_ADD
            c[6] = DTOR_NEW + c[6]
            c[10] = c[10] + EVID_ADD
            L[i] = "\t".join(c) + eol
            save(TYPES, L)
            changed.append("types.tsv " + T)
            return
    sys.exit("type row not found")


# ---------------------------------------------------------------- fields.tsv
F = {
    "0x0000": (None, None,
               " || " + MARK + "): integration checked from the other side - every sub-0xC0 access "
               "reached from the asset's cell or own handler is common widget code (the 00244F00 destroy "
               "chain and the attach entry 00244960); the type-specific bodies 00394070, 00393FF0, "
               "00394500 and the consumer's asset reads (00393A98, 00393AA5) touch nothing below +0xC0."),
    "0x00C0": (None,
               " || " + MARK + "): WIDTH - both writers are DWORD (003940FC `mov dword` 0; 003940E3 "
               "`or dword` 1); the readers are a BYTE test of bit0 (00393A98) and a DWORD load masked to "
               "bit0 (0039450D, 00394513 `and eax,1`). SECOND CONSUMER, SCRIPT-FACING: 00394500 returns 0 "
               "when 02AEE4C0 is null, else +0xC0 & 1; its only reference found (E8/E9, abs64, rva32 "
               "sweep) is 00511EC4 in 00511EC0, the poll of script verb 7055 fsttl_initialize (begin "
               "00511EA0 tail-jumps the creator 00394460), which returns 1 - the durative running flag - "
               "while 00394500 returns 0 (00511ECD sete). So fsttl_initialize holds the script until bit0 "
               "is set: bit0 means the title asset's resources are ready. BITS 1-31: no enumerated writer "
               "sets them (the memset zero, store 0 and OR 1 are the only writes on the cell, own-handler "
               "and batch-owner paths) and no enumerated reader tests them - a bound over those paths, not "
               "a proof about all code.",
               " || " + MARK + ", " + REC + "/ov31_title_asset.py S X C O; "
               "01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv row 7055 and "
               "members/scriptvm-verb-adapter-callbacks.tsv 00511EC0 poll -> 00394500): FALSIFIER looked "
               "for - a write of another bit or width, or a reader of another bit, on any enumerated "
               "receiver path. None found."),
    "0x00C4": ("u8[4]",
               " || " + MARK + "): STILL UNREAD, NOW BOUNDED. No access at +0xC4 on any enumerated "
               "receiver path: the nine references to 02AEE4C0 (control 02AEE4D0 passes), the cell-seeded "
               "fixpoint (13 functions, converged, extent widened to 0x1000), the own-handler seed "
               "SEED=ctor 00394070 ARGREGS=1 (4 functions, converged) and the three batch owner-notify "
               "sites (owner+0x00 only). POSITIVE CONTROL: the same tool on the sibling cell 02AEE4C8 "
               "reports +0xC4 accesses (0039435C, 0039436A, 003944E0), so this zero is not the filter. "
               "The only write is the 002465F0 memset. The position is exactly where natural alignment "
               "puts four bytes between a uint32 at +0xC0 and a pointer at +0xC8 - a structural reading, "
               "not proven padding. Retyped u8[4] (README: a declared gap span is u8[n]). Not excluded: an "
               "access through the UI-root child link made at attach, whose generic walkers were not "
               "individually read.",
               " || " + MARK + ", " + REC + "/ov31_title_asset.py X C O K): FALSIFIER looked for - any "
               "[asset+0xC4] access on the enumerated paths. None found; control K passes."),
    "0x00C8": (None,
               " || " + MARK + "): BOTH ENDS ENUMERATED - after the memset, exactly one writer (00394033, "
               "QWORD) and one reader (00394097, QWORD) on all enumerated paths; the cell seed reaches no "
               "+0xC8 access, so neither the consumer 003939B0 nor the fsttl predicates read it. After the "
               "own message-18 arm and 002482E0's pool return the stale value stays in the slot until the "
               "next occupant's memset.",
               " || " + MARK + ", " + REC + "/ov31_title_asset.py S C O): FALSIFIER looked for - any other "
               "+0xC8 access on the cell, own or batch-owner paths. None found."),
    "0x00D0": (None,
               " || " + MARK + "): BOTH ENDS ENUMERATED - writers 00394050 (store) and 003940B9 (clear), "
               "readers 003940A8 (own message 18) and 00393AA5 (consumer, the only cross-type reader), all "
               "QWORD. This is the type's last field: +0xD0 + 8 = 0xD8, the requested extent.",
               " || " + MARK + ", " + REC + "/ov31_title_asset.py S C O): FALSIFIER looked for - any other "
               "+0xD0 access on the enumerated paths, or any access at or beyond +0xD8. None found."),
}


def patch_fields():
    L = load(FIELDS)
    seen = set()
    dirty = False
    for i, ln in enumerate(L):
        if not ln.startswith(T + "\t"):
            continue
        c, eol = split_row(ln)
        if len(c) != 9 or c[1] not in F:
            continue
        seen.add(c[1])
        if MARK in c[8] or MARK in c[5]:
            continue
        ctype, madd, eadd = F[c[1]]
        if ctype is not None:
            c[4] = ctype
        if madd:
            c[5] = c[5] + madd
        c[8] = c[8] + eadd
        L[i] = "\t".join(c) + eol
        dirty = True
        changed.append("fields.tsv %s %s" % (T, c[1]))
    if seen != set(F):
        sys.exit("field rows missing: %s" % sorted(set(F) - seen))
    if dirty:
        save(FIELDS, L)


# ---------------------------------------------------------------- page
BOX_OLD = ("*NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an "
           "independent-acceptance/process item, carried by board task "
           "FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE. Register OV-31.*")
BOX_NEW = ("*ANSWERED 2026-09-29 (SWE2-STRUCT), section 8: every field's receiver, width, both ends, "
           "allocation class and the common release chain are recorded in `_types`; named residue: "
           "+0xC4 unread (bounded, positive control passes), parent-root release and deferral "
           "applicability, real IO timing (OV-29). Earlier: NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) "
           "under the class-2 ruling, carried by board task FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE. "
           "Register OV-31.*")
SEC_ANCHOR = "## Cross-subsystem neighbours"
SEC_HEAD = "## 8. Type-store integration, OV-31 (SWE2-STRUCT, 2026-09-29)"
SECTION = SEC_HEAD + """

This section records the type-store work for the 0xD8 asset (`WidgetSingleton02AEE4C0` in `_types`).
Each representation fact below comes from an instruction. Meaning is stated separately and only where
a consumer establishes it. Checks: [`ov31_title_asset.py`](../../_index/candidates/ov31-title-asset-type-store-0929/ov31_title_asset.py)
(`S` exact instructions, `P` .pdata chain roots, `J` jump-table arm, `X` cell references, `C`/`O`
receiver census, `K` positive control); record [`README.md`](../../_index/candidates/ov31-title-asset-type-store-0929/README.md).

**Receiver and extent.** The receiver is direct: the object pointer is held in the cell `02AEE4C0`
and passed in RCX to its own handler. The extent is fixed at `0xD8`, set by `0039449F`. `+0x00`..`+0xBF` is the
embedded common widget header (OPUS, 2026-09-27). From this type's side, every access below `+0xC0`
reached from the cell or the own handler is in common widget code: the `00244F00` destroy chain, and the
attach entry `00244960`. The type area `+0xC0`..`+0xD7` is fully declared. A census widened to
`0x1000` finds no type-specific access at or beyond `+0xD8`.

| Offset | Width proof | Writers | Readers | Meaning evidence |
|---|---|---|---|---|
| `+0xC0` u32 | `003940FC` mov dword, `003940E3` or dword; reads `00393A98` byte test, `0039450D` dword | memset, `003940FC` (0), `003940E3` (bit 0) | `00393A98` (consumer gate), `0039450D` (`00394500`) | script verb `fsttl_initialize` polls `00394500` through `00511EC0` and holds until bit 0 is set. Bit 0 means the resources are ready. No enumerated path writes or reads bits 1-31. |
| `+0xC4` u8[4] | none | memset only | none on any enumerated path | none. It sits in the alignment position before a pointer, which is a reading, not proof. |
| `+0xC8` ptr | `00394033`, `00394097` QWORD | `00394033` | `00394097` only | resource-entry result, passed to `0024A680(ptr, 1)` on message 18 |
| `+0xD0` ptr | `00394050`, `003940A8`, `003940B9`, `00393AA5` QWORD | `00394050`, `003940B9` (clear) | `003940A8`, `00393AA5` | loaded block that the consumer passes to `003946B0` |

**Enumerated receiver paths.** The zeros above apply only to these paths:

- all nine references to `02AEE4C0`, found by an image-base-aware scan whose control `02AEE4D0` passes;
- the cell-seeded fixpoint, which reaches 13 functions and converges;
- the own-handler seed `00394070`, run with argument registers, which reaches 4 functions and converges;
- the load batch's three owner-notify sites. The batch records `self` at `+8` (`002495B7`), and the
  notify sites read only the handler slot at `+0x00`.

The `+0xC4` zero has a positive control: the same tool on the sibling cell `02AEE4C8` does see
`+0xC4` accesses.

**Allocation is pool-or-heap, not heap.** `0xD8` is at most `0x120`, so `00244F50` takes the first
free slot of the 112-slot pool. It falls back to `002497B0` only when every slot is busy
(`00244FB2`). The store's class is now `MIXED`.

**Release is external and common.** The asset never destroys itself. Two sites pass it to the widget
destroy `00244F00`:

- `00394400` is called only from the message-18 arm of the `0x5A0` widget handler `00582860`
  (`00582EB5`, behind the nonnull predicate `00394520`);
- the `0xF0` sibling's handler `00394130` does so in its own message-18 arm (`00394161`).

The common chain then delivers message 18 to this type's cleanup arm at `0024505A`. After that,
`002482E0` returns the slot to the pool or frees it. A release site is not an ownership proof.

**The script-facing consumer.** Script verb 7055 `fsttl_initialize` has two handlers. Its begin
`00511EA0` runs the creator. Its poll `00511EC0` returns the running flag while `00394500` is zero.
So a script waits for bit 0 of `+0xC0`. That bit is set only by the batch's message 16.

**Residue, named rather than smoothed:**

1. `+0xC4` has no reader on any enumerated path. An access through the UI-root child link that
   `00248220` makes at attach time is not excluded, because those generic walkers were not read one by one.
2. Release through a teardown of the parent root `*(0208EA28)` is not established.
3. Whether the asset ever takes `00244F00`'s deferred branch, or `00245020`'s `+0x40` bit `0x20`
   deferral, is not established. `00248271` copies that bit from the parent at attach time.
4. Real IO timing and lifetime remain OV-29.
5. Type readiness is left for independent acceptance (OV-32).

"""


def patch_page():
    # The section and the box are separate edits: the box flips only in the commit that
    # publishes the register row (--section-only leaves the box alone).
    L = load(PAGE)
    s = "".join(L)
    s0 = s
    eol = "\r\n" if "\r\n" in L[0] else "\n"
    if SEC_HEAD not in s:
        if SEC_ANCHOR not in s:
            sys.exit("page section anchor not found")
        s = s.replace(SEC_ANCHOR, SECTION.replace("\n", eol) + SEC_ANCHOR, 1)
        changed.append("page section 8")
    if "--section-only" not in sys.argv and BOX_NEW not in s:
        if BOX_OLD not in s:
            sys.exit("page box anchor not found")
        s = s.replace(BOX_OLD, BOX_NEW, 1)
        changed.append("page box")
    if s != s0 and not CHECK:
        with open(PAGE, "w", encoding="utf-8", newline="") as f:
            f.write(s)


# ---------------------------------------------------------------- register
REG_OLD = ("| **NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: type-store work "
           "routed to SWE2-STRUCT via FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE.** |")
REG_NEW = ("| **ANSWERED 2026-09-29 (SWE2-STRUCT): every field of WidgetSingleton02AEE4C0 now carries "
           "its receiver, width proof, writers and readers; the common widget header is integrated from "
           "both sides; allocation corrected to MIXED (pool first, heap fallback); release is external "
           "through the common destroy 00244F00 from 00394400 and 00394130; +0xC0 bit0 gains the "
           "script-facing consumer fsttl_initialize (poll 00511EC0 via 00394500).** Named residue: "
           "+0xC4 unread on every enumerated path (bounded, positive control passes); release through a "
           "parent-root teardown and deferred-destroy applicability not established; real IO timing "
           "stays OV-29; readiness stays for OV-32. Page section 8; evidence "
           "`" + REC + "/`. *Earlier:* NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the "
           "class-2 ruling, routed via FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE. |")


def patch_reg():
    L = load(REG)
    for i, ln in enumerate(L):
        if ln.startswith("| OV-31 |"):
            if "ANSWERED 2026-09-29 (SWE2-STRUCT)" in ln:
                return
            if REG_OLD not in ln:
                sys.exit("register cell changed under us")
            L[i] = ln.replace(REG_OLD, REG_NEW, 1)
            assert L[i].count("|") == ln.count("|")
            save(REG, L)
            changed.append("OPEN-QUESTIONS OV-31")
            return
    sys.exit("OV-31 row not found")


patch_types()
patch_fields()
patch_page()
if "--section-only" not in sys.argv:
    patch_reg()
print(("WOULD CHANGE: " if CHECK else "CHANGED: ") + (", ".join(changed) if changed else "nothing"))
