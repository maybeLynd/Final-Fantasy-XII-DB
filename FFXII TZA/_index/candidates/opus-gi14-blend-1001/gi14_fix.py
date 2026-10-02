"""gi14_fix.py [--apply] [--register] - GI-14 answered, and OPUS's own 518a7f2d8 reading re-corrected (OPUS, 2026-10-01).

518a7f2d8 said the line emitter's blend value sits at the GiPrim command's +0x30 and reaches the device's vtable +0x40.
It does not: 008642A0 returns the new GiPrim object PLUS 8 (008642F8), so the emitters' `[ptr + 0x30]` store is object
+0x38 and their `[ptr + 0x44] = 1` is object +0x4C. GiPrim 00863D80 (this = the object) tests +0x4C and, when set, hands
+0x38 to 001EE650, the GS ALPHA -> D3D11 blend translator (BC-1), then applies the result through the device's slot
+0x78. The page's original "record +0x38" was right. The dword at object +0x30 that reaches slot 8 is another field.

Page edits always; the register cell only with --register (the register rides in another publish until it commits).
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PAGE = "17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md"
REG = "_index/OPEN-QUESTIONS.md"

PAGE_EDITS = [
    ("the value sits at the GiPrim command's `+0x30` and GiPrim hands it to its render context's vtable `+0x40` - the GI-14 section, corrected 2026-10-01, OPUS**",
     "~~the value sits at the GiPrim command's `+0x30` and GiPrim hands it to its render context's vtable `+0x40` - the "
     "GI-14 section, corrected 2026-10-01, OPUS~~ record `+0x38` is right: `GiPrim` translates it through the GS ALPHA "
     "translator `001EE650` - the GI-14 section, re-corrected 2026-10-01, OPUS**"),
    ("in mode 6 - at the command's\n`+0x30`, and closes the list (`0020E670`). It is the line twin of the point emitter `0039D970`, which stores the\nblend value at the same command offset (`0039DAAC`).",
     "in mode 6 - at ~~the command's\n`+0x30`~~ `+0x30` of the pointer `008642A0` returns, which is the GiPrim object plus 8, so object `+0x38`; it also "
     "sets that pointer's `+0x44`, object `+0x4C`, to 1 *(re-corrected 2026-10-01, OPUS)*. It closes the list (`0020E670`). "
     "It is the line twin of the point emitter `0039D970`, which stores the\nblend value at the same offset (`0039DAAC`)."),
    ("**Where the blend value goes.** The value the section above calls record `+0x38` is the `GiPrim` command's `+0x30`.\n`GiPrim` (`00863D80`) reads it as a dword (`00863FF9`) and passes it as the fifth argument of its render context's\nvtable `+0x40` call (`00864029`). **Still open (GI-14, narrowed):** which class implements that slot, and so how the\nGS-ALPHA-shaped value becomes the actual blend state.",
     "~~**Where the blend value goes.** The value the section above calls record `+0x38` is the `GiPrim` command's `+0x30`.\n`GiPrim` (`00863D80`) reads it as a dword (`00863FF9`) and passes it as the fifth argument of its render context's\nvtable `+0x40` call (`00864029`). **Still open (GI-14, narrowed):** which class implements that slot, and so how the\nGS-ALPHA-shaped value becomes the actual blend state.~~\n\n"
     "**Where the blend value goes (re-corrected 2026-10-01, OPUS - the paragraph above was off by 8).** `008642A0` "
     "returns the new `GiPrim` object plus 8 (`lea rax, [rbx + 8]`), and both emitters address the command through that "
     "pointer. So their `+0x30` store is object `+0x38`, the record `+0x38` the section above names, and their "
     "`+0x44 = 1` is object `+0x4C`. `GiPrim` (`00863D80`, called with the object itself) tests `+0x4C`. When it is set, "
     "`GiPrim` passes `+0x38` to `001EE650`, the GS ALPHA to D3D11 blend translator of BC-1 (81-entry table `00902750` "
     "indexed `27·A + 9·B + 3·C + D`; [the BC-1 record](../../_index/candidates/bc1-selector-enum/README.md)). It "
     "then applies the result through the device's slot `+0x78`. So the value is a PS2 GS ALPHA register, and the port "
     "turns it into blend state as the GS would. The dword at object `+0x30` that `GiPrim` passes to the device's slot 8 "
     "(`PrimitiveRendererD3D11`, `006CAEB0`, stored at renderer `+0x208FC`) is a different field. **GI-14 is answered.**"),
]
# citation form only: the interior range inside family member 0044BA80 would refuse its generated family once the page
# is DOCUMENTED (adrift_report); the claim is unchanged
PAGE_EDITS.append(("whose return goes to `+0x458` (`0044BA9B`–`0044BAA5`) |",
                   "whose return goes to `+0x458` (in `0044BA80`'s tail) |"))
STATUS_PREFIX = 'status: "PARTIAL — GI-14 registered 2026-10-01'
STATUS_TAG = 'status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS'
REG_TAG = "**ANSWERED 2026-10-01 (OPUS, static)** — the six tail helpers and the line emitter"
REG_CELL = ("| " + REG_TAG + " `0039D6C0` read (the element-types page's GI-14 section). The blend value is object "
            "`+0x38` of the `GiPrim` command (`008642A0` hands the emitters the object plus 8), and `GiPrim` `00863D80` "
            "translates it through the GS ALPHA translator `001EE650` when `+0x4C` is set. *(The 518a7f2d8 cell's "
            "command `+0x30` and vtable `+0x40` reading was off by 8 and is withdrawn.)* `0044A180` (`0x05`) and "
            "`0044C850` (`0x0A`) were covered by GI-11's tail reads (A5/B1). |")


def main():
    apply = "--apply" in sys.argv
    do_reg = "--register" in sys.argv
    fails = 0
    p = os.path.join(DB, PAGE)
    t = open(p, "rb").read().decode("utf-8")
    for i, (old, new) in enumerate(PAGE_EDITS, 1):
        if new.replace("\n", "\r\n") in t or new in t:
            print("ALREADY", i); continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", i); fails += 1; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        t = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + str(i))
    if do_reg:
        r = open(os.path.join(DB, REG), "rb").read().decode("utf-8")
        lines = r.split("\n")
        idx = [k for k, l in enumerate(lines) if l.startswith("| GI-14 |")]
        if "|" in REG_CELL[1:-1]:
            print("REFUSING pipe in cell"); fails += 1
        elif len(idx) != 1:
            print("REFUSING GI-14 rows", len(idx)); fails += 1
        elif REG_TAG in lines[idx[0]]:
            print("ALREADY register")
        else:
            row = lines[idx[0]]
            cr = "\r" if row.endswith("\r") else ""
            body = row.rstrip("\r")
            cut = body.rfind("| **OPEN** — static.")
            if cut < 0:
                print("REFUSING: GI-14 last cell is not OPEN"); fails += 1
            else:
                lines[idx[0]] = body[:cut] + REG_CELL + cr
                r = "\n".join(lines)
                print(("PATCHED " if apply else "WOULD PATCH ") + "register")
        # the page re-status follows the register
        ls = t.split("\n")
        st = [k for k, l in enumerate(ls) if l.startswith(STATUS_PREFIX)]
        if any(l.startswith(STATUS_TAG) for l in ls):
            print("ALREADY status")
        elif len(st) != 1:
            print("REFUSING status", len(st)); fails += 1
        else:
            old = ls[st[0]].rstrip("\r")
            cr = "\r" if ls[st[0]].endswith("\r") else ""
            rest = old.split("are live. ", 1)[1] if "are live. " in old else old[len(STATUS_PREFIX):]
            ls[st[0]] = (STATUS_TAG + "; documented_rule READY): GI-14 answered 2026-10-01 (OPUS, static - the six tail "
                         "helpers, the line emitter and the blend value's consumer read, see the GI-14 section; review "
                         "requested from SWE2-AUDIT-SEM). History: PARTIAL on GI-14 from 2026-10-01 (SWE2-FRONTIER, on "
                         "SWE2-AUDIT-SEM's REJECT of c97af7156, record dd-restatus-gi-0930). " + rest) + cr
            t = "\n".join(ls)
            print(("PATCHED " if apply else "WOULD PATCH ") + "status")
    if apply and not fails:
        open(p, "wb").write(t.encode("utf-8"))
        if do_reg:
            open(os.path.join(DB, REG), "wb").write(r.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
