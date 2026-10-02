"""gi19_apply.py [--apply] [--register] - GI-19 answered on the oscillator page (OPUS, 2026-10-01).

Page edits always; the register cell and the page re-status only with --register. Exact substrings, each once;
tag-guarded; dry run unless --apply; FAILS n.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PAGE = "17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md"
REG = "_index/OPEN-QUESTIONS.md"
G = " *(GI-19 section, OPUS 2026-10-01)*"
PAGE_EDITS = [
    ("| `+0x08` | u32 | id → an object whose `+0x00` id resolves to the skeleton's `0x290`-stride bone array, read by `0040DBB0` (`0040DC6B`–`0040DC79`; added 2026-10-01, OPUS) |",
     "| `+0x08` | u32 | id → an object whose `+0x00` id resolves to the skeleton's `0x290`-stride bone array, read by `0040DBB0` (`0040DC6B`–`0040DC79`; added 2026-10-01, OPUS). Not authored: `003E1C50` sets it to the rig's own slot `+0x78`, which holds the bone array's id" + G + " |"),
    ("| `+0x08` | u32 | id → sub-object whose `+0x28`-array / `+4`-count the heavy stages walk |",
     "| `+0x08` | u32 | id → sub-object whose `+0x28`-array / `+4`-count the heavy stages walk. `0040EEA0` relocates it as the authored A array (`0x40`-byte records, entry `+0x00` of them), which `0040DBB0` walks; the `+0x28` / `+4` reading is not reconciled here" + G + " |"),
    ("and a second 4×4 at `[sub-obj + 0x150]`–`+0x180`",
     "and a second 4×4 at ~~`[sub-obj + 0x150]`–`+0x180`~~ the same bone's `0x290` row `+0x150`–`+0x180` *(corrected 2026-10-01, OPUS: `rdi` is the bone array plus the index × `0x290`, `0040DDB5` / `0040DDC5`)*"),
    ("only the class names of the three intermediate objects remain open.)*",
     "only the class names of the three intermediate objects remain open.)* *(Answered 2026-10-01, OPUS: they are the rig's slot `+0x78` and the authored A and B arrays - the GI-19 section.)*"),
]
EXTRA = [("00-Engine-Core-Runtime/CONTRACT-transform-primitives.md",
          "`[sub-obj + 0x150]`–`+0x180` straight into rows 5–8",
          "~~`[sub-obj + 0x150]`–`+0x180`~~ the bone's `0x290` row `+0x150`–`+0x180` *(corrected 2026-10-01, OPUS - "
          "the oscillator page's GI-19 section)* straight into rows 5–8")]
HEAD = "## GI-19: the sway section's layout and the chain's objects (OPUS, 2026-10-01)"
ANCHOR = "## Falsification pass"
STATUS_PREFIX = 'status: "PARTIAL — GI-19 registered 2026-10-01'
STATUS_TAG = 'status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS'
REG_TAG = "**ANSWERED 2026-10-01 (OPUS, static)** — the chain's objects are named"
REG_CELL = ("| " + REG_TAG + ": the record is controller 0's authored sub-block of `@FCP` section 2, relocated by "
            "`0040EEA0`. Its `+0x08` is not authored: `003E1C50` points it at the rig's own slot `+0x78`, which holds "
            "the encoded bone array (`00421D20`, the resource entry's `+0x84`). The entry's `+0x08` is the authored A "
            "array (`0x40`-byte records), and each A's `+0x04` is the authored B array (`0x50`-byte link records, u16 "
            "bone index at `+0x00`). The page's second 4x4 is the bone row's `+0x150`, not a sub-object's. See the "
            "oscillator page's GI-19 section. |")


def main():
    apply = "--apply" in sys.argv
    do_reg = "--register" in sys.argv
    fails = 0
    p = os.path.join(DB, PAGE)
    t = open(p, "rb").read().decode("utf-8")
    eol = "\r\n" if "\r\n" in t else "\n"
    for i, (old, new) in enumerate(PAGE_EDITS, 1):
        if new in t:
            print("ALREADY", i); continue
        if t.count(old) != 1:
            print("REFUSING", i, t.count(old)); fails += 1; continue
        t = t.replace(old, new, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + str(i))
    if HEAD in t:
        print("ALREADY section")
    else:
        sec = io.open(os.path.join(HERE, "gi19_section.md"), encoding="utf-8").read().strip("\n").replace("\n", eol)
        k = t.find(eol + ANCHOR)
        if k < 0 or t.count(eol + ANCHOR) != 1:
            print("REFUSING section anchor"); fails += 1
        else:
            t = t[:k] + eol + sec + eol + t[k:]
            print(("PATCHED " if apply else "WOULD PATCH ") + "section")
    r = None
    if do_reg:
        r = open(os.path.join(DB, REG), "rb").read().decode("utf-8")
        lines = r.split("\n")
        idx = [k for k, l in enumerate(lines) if l.startswith("| GI-19 |")]
        if "|" in REG_CELL[1:-1]:
            print("REFUSING pipe"); fails += 1
        elif len(idx) != 1:
            print("REFUSING GI-19 rows", len(idx)); fails += 1
        elif REG_TAG in lines[idx[0]]:
            print("ALREADY register")
        else:
            row = lines[idx[0]]
            cr = "\r" if row.endswith("\r") else ""
            body = row.rstrip("\r")
            cut = body.rfind("| **OPEN** — static.")
            if cut < 0:
                print("REFUSING: last cell not OPEN"); fails += 1
            else:
                lines[idx[0]] = body[:cut] + REG_CELL + cr
                r = "\n".join(lines)
                print(("PATCHED " if apply else "WOULD PATCH ") + "register")
        ls = t.split("\n")
        st = [k for k, l in enumerate(ls) if l.startswith(STATUS_PREFIX)]
        if any(l.startswith(STATUS_TAG) for l in ls):
            print("ALREADY status")
        elif len(st) != 1:
            print("REFUSING status", len(st)); fails += 1
        else:
            old = ls[st[0]].rstrip("\r")
            cr = "\r" if ls[st[0]].endswith("\r") else ""
            rest = old.split("are unnamed. ", 1)[1] if "are unnamed. " in old else old[len(STATUS_PREFIX):]
            ls[st[0]] = (STATUS_TAG + "; documented_rule READY): GI-19 answered 2026-10-01 (OPUS, static - the sway "
                         "section's layout and the chain's objects, see the GI-19 section; review requested from "
                         "SWE2-AUDIT-SEM). History: PARTIAL on GI-19 from 2026-10-01 (SWE2-FRONTIER, on SWE2-AUDIT-SEM's "
                         "REJECT of c97af7156, record dd-restatus-gi-0930). " + rest) + cr
            t = "\n".join(ls)
            print(("PATCHED " if apply else "WOULD PATCH ") + "status")
    extra = {}
    for rel, old, new in EXTRA:
        x = extra.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in x:
            print("ALREADY", rel); continue
        if x.count(old) != 1:
            print("REFUSING", rel, x.count(old)); fails += 1; continue
        extra[rel] = x.replace(old, new, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel)
    if apply and not fails:
        for rel, x in extra.items():
            open(os.path.join(DB, rel), "wb").write(x.encode("utf-8"))
        open(p, "wb").write(t.encode("utf-8"))
        if do_reg and r is not None:
            open(os.path.join(DB, REG), "wb").write(r.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
