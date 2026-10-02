"""gi15_apply.py [--apply] - GI-15: the authored-commands page's per-site helpers, read (OPUS, 2026-10-01).

Strikes each "not read (GI-15)" passage with a pointer to the new GI-15 section, corrects the readings the section
refutes (`0x34`'s float, the `0x3F` field sources, `+0x2F2`'s "placeholder", the `0x2A` floats), re-statuses the page
and appends the section. It also carries four corrections to other pages: the fades page's flags bit 8, the FTR link
bits 0-11, the group-wipe page's priority map address, the FCP section-5 reader, and the oscillator page's swapped
`0x3F` words (that page rides in OPUS-PUB-GI-STATIC-ROWS-1001, so the last two edits run after it commits).

Exact substrings, each once (CRLF or LF inside multi-line edits); every new text carries a tag, so a re-run reads
ALREADY. Dry run unless --apply; FAILS n.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
AC = "17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md"
FADES = "17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md"
FTR = "17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md"
FCP = "17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md"
OSC = "17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md"
GW = "05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md"
R = " *(read 2026-10-01, OPUS: the GI-15 section at the end of this page)*"
C = " *(corrected 2026-10-01, OPUS: the GI-15 section)*"

# (path, old, new) - plain replacements
EDITS = [
    (AC, "what each subtype means to the handler is the battle side's and was not read here (GI-15).",
     "~~what each subtype means to the handler is the battle side's and was not read here (GI-15).~~ Each subtype's arm "
     "in `00325260` is now read (the GI-15 section, OPUS 2026-10-01)."),
    (AC, "What it does with the section was not read (GI-15).*",
     "~~What it does with the section was not read (GI-15).~~ The `0x09` section below reads it (GI-15, OPUS 2026-10-01).*"),
    (AC, "**Not read here (GI-15):** the seven arms past their first store; the `0x80` arm's nested switch; what `003AFC10` builds;\nwhich of `+0x1C`–`+0x55` mean what to the shadow pools.",
     "~~**Not read here (GI-15):** the seven arms past their first store; the `0x80` arm's nested switch; what `003AFC10` builds;\nwhich of `+0x1C`–`+0x55` mean what to the shadow pools.~~" + R),
    (AC, "| `byte[+0x1C]` = `byte+3`; when that is 0 or 1, also a float from `dword[cmd + 4]` |",
     "| `byte[+0x1C]` = `byte+3`; ~~when that is 0 or 1, also a float from `dword[cmd + 4]`~~ a ramp - the float "
     "`dword[cmd + 4]` is used in every case: set at once when `byte+3` is 0 or 1, else approached over `byte+3` steps" + C + " |"),
    (AC, "an index at `+0x14`, `word+2 & 0xFFF` at `+0x16`, `word+2 >> 15` at `+0x18`;",
     "~~an index at `+0x14`, `word+2 & 0xFFF` at `+0x16`, `word+2 >> 15` at `+0x18`~~ a bone at `+0x14`, a preset at "
     "`+0x16` and a flag at `+0x18`, filled from different words by the two commands" + C + ";"),
    (AC, "| the block's `+0x14` index | `word[cmd + 0x10] & 0xFFF`, **used directly**, zeroed when it equals the masked `word+2` (`00520560`–`00520567`) |",
     "| the block's `+0x14` index | ~~`word[cmd + 0x10] & 0xFFF`, **used directly**, zeroed when it equals the masked `word+2`~~ "
     "`word[cmd + 2]`, **used directly**; `word[cmd + 0x10]` fills the preset `+0x16`, zeroed when `word[cmd + 2]` is "
     "`0xFFFF` (`00520560`–`00520567`)" + C + " |"),
    (AC, "`0xFFFF` back zeroing the field (`00520630`, `0052065E`–`00520663`) |",
     "`0xFFFF` back zeroing ~~the field~~ the preset `+0x16`, which comes from `word[cmd + 2]`" + C + " (`00520630`, `0052065E`–`00520663`) |"),
    (AC, "That is the whole difference: **one addresses the oscillator by index, the other by name.**",
     "~~That is the whole difference: **one addresses the oscillator by index, the other by name.**~~ The difference: "
     "`0x3F` gives the bone by index and the preset from `word+0x10`; `0x48` finds the bone by name key and takes the "
     "preset from `word+2`, which is 0 (sway off) in 5,167 of 5,771" + C + "."),
    (AC, "**Not read here (GI-15):** `00372800`'s lookup beyond its `0xFFFF` contract; what name key `29` is; why `0x3F` zeroes its\nindex when it matches the masked `word+2`.",
     "~~**Not read here (GI-15):** `00372800`'s lookup beyond its `0xFFFF` contract; what name key `29` is; why `0x3F` zeroes its\nindex when it matches the masked `word+2`.~~" + R),
    (AC, "**Not read here (GI-15):** `00423790`.", "~~**Not read here (GI-15):** `00423790`.~~" + R),
    (AC, "built with no key**. That is a placeholder: the record exists, but nothing was resolved for it.",
     "built with no key**. ~~That is a placeholder: the record exists, but nothing was resolved for it.~~ That is attach "
     "code `0x7FFF`, the whole-skeleton bind; the bind still runs, with bone -1" + C + "."),
    (AC, "**Leaving that state restores three fades.**",
     "~~**Leaving that state restores three fades.**~~ *(Corrected 2026-10-01, OPUS: both paths reach the bit-26 test, "
     "and the no-key path has just set bit 26, so `003E5D30` runs on that path itself; nothing read clears bit 26 - the "
     "GI-15 section.)*"),
    (AC, "**Not read here (GI-15):** `004219C0`, the sibling writer, beyond confirming its two stores match; what the key argument\n*names*; `00372760` and `0046E590` beyond their return contracts.",
     "~~**Not read here (GI-15):** `004219C0`, the sibling writer, beyond confirming its two stores match; what the key argument\n*names*; `00372760` and `0046E590` beyond their return contracts.~~" + R),
    (AC, "**Not read here (GI-15):** `00373060` (read only for its shape — it resolves two image pointers and indexes a `0x292`-stride\ntable) and `005048A0` beyond its `-1` contract; what `word[+0x2F2]` *is*, beyond being the field `0x13` gates on and\n`0x14` filters by.",
     "~~**Not read here (GI-15):** `00373060` (read only for its shape — it resolves two image pointers and indexes a `0x292`-stride\ntable) and `005048A0` beyond its `-1` contract; what `word[+0x2F2]` *is*, beyond being the field `0x13` gates on and\n`0x14` filters by.~~" + R),
    (AC, "**Not read here (GI-15):** what `word[+0x2F2]` counts",
     "~~**Not read here (GI-15):** what `word[+0x2F2]` counts~~ *(read 2026-10-01, OPUS: a 0/1 flag, not a count - the GI-15 section)*"),
    (AC, "scale, not of a position offset* — but nothing read here consumes the floats, so they are recorded as three floats",
     "scale, not of a position offset* — ~~but nothing read here consumes the floats, so they are recorded as three floats~~ "
     "*(2026-10-01, OPUS: they are the camera-shake source's intensity, time rate and radius scale - the GI-15 section)* "
     "and earlier they were recorded as three floats"),
    (AC, "**Not read here (GI-15):** what the pool's slots are for (`003D8300`, the release, and the slot's own `+0x30`/`+0x40` were\nread only for their shape); the `02B4D7A2` gate; the table at `02B4E3D0` the kind-2 path indexes with the request's\nclamped word.",
     "~~**Not read here (GI-15):** what the pool's slots are for (`003D8300`, the release, and the slot's own `+0x30`/`+0x40` were\nread only for their shape); the `02B4D7A2` gate; the table at `02B4E3D0` the kind-2 path indexes with the request's\nclamped word.~~" + R),
    (AC, "**Not read here (GI-15):** what a \"sub-resource variant\" is on the model side (`RenderModelInstance_RemoveSubresourceVariantBinding`\n`00504610` and the `003E7210` table walk were read only for their shape); which slot each of the five indices is.",
     "~~**Not read here (GI-15):** what a \"sub-resource variant\" is on the model side (`RenderModelInstance_RemoveSubresourceVariantBinding`\n`00504610` and the `003E7210` table walk were read only for their shape); which slot each of the five indices is.~~" + R),
    (AC, "> *Not read (GI-15):* `0041B650`, `00409190` and `003AB7F0`, and the tail past the loop.",
     "> ~~*Not read (GI-15):* `0041B650`, `00409190` and `003AB7F0`, and the tail past the loop.~~" + R),
    # other pages
    (FADES, "with `dword[+4] & 0x100` clear returns its index",
     "with `dword[+4] & 0x100` ~~clear~~ **set** returns its index *(corrected 2026-10-01, OPUS: `003737C0` takes the "
     "record when bit 8 is set - the authored-commands page's GI-15 section)*"),
    (GW, "| sign-extended byte fetch from the `01E6B410` priority map (`movsx eax, byte[rcx + 01E6B410]`) |",
     "| sign-extended byte fetch from the ~~`01E6B410`~~ `01F00410` priority map (~~`movsx eax, byte[rcx + 01E6B410]`~~ "
     "`lea rax, 01F00410` then `movsx eax, byte [rcx + rax]`; corrected 2026-10-01, OPUS) |"),
    (GW, "class-2 → the `01E6B410` byte-map compare",
     "class-2 → the ~~`01E6B410`~~ `01F00410` byte-map compare *(corrected 2026-10-01, OPUS; the `arg4` above is the "
     "third argument, `r8` = `word[rec + 0x3B4]`)*"),
    (FCP, "| `+0x0A` | 5 | **none** — present in 7 blocks, unread |",
     "| `+0x0A` | 5 | ~~**none** — present in 7 blocks, unread~~ inline in `003E7210`, the palette-binding walk of "
     "authored command `0x16` - present in 7 blocks *(corrected 2026-10-01, OPUS: the authored-commands page's GI-15 "
     "section; the scans above missed the `[record + 0x400]` load)* |"),
    # the oscillator page (apply only after OPUS-PUB-GI-STATIC-ROWS-1001 has committed - that publish carries the page)
    (OSC, "with a **preset** (command word\n`+2`; `0xFFFF` clears the id), an id and a flag (word `+0x10`: low twelve bits, bit 15)",
     "with ~~a **preset** (command word\n`+2`; `0xFFFF` clears the id), an id and a flag (word `+0x10`: low twelve bits, bit 15)~~ "
     "a **bone** (command word `+2`; `0xFFFF` zeroes the preset), a **preset** and a flag (word `+0x10`: low twelve "
     "bits, bit 15) *(corrected 2026-10-01, OPUS: the two words were swapped - the authored-commands page's GI-15 "
     "section)*"),
    (OSC, "- `+0x3C` := the id, `+0x3F` bit 3 := the flag,",
     "- `+0x3C` := ~~the id~~ the bone, which the heavy stage `0040FF30` reads *(corrected 2026-10-01, OPUS)*, `+0x3F` bit 3 := the flag,"),
]
FTR_ANCHOR = "                   27,561/27,561"
FTR_LINES = ["                   [CORRECTED 2026-10-01, OPUS: bits 0..11 are not unread -",
             "                   00409250 returns them as the record key when +0x04",
             "                   bit 30 is clear; the tag search 003737C0 uses it]"]
STATUS_PREFIX = 'status: "PARTIAL — GI-15 registered 2026-10-01'
SECTION_HEAD = "## GI-15: the per-site helpers read (OPUS, 2026-10-01)"


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}

    def get(rel):
        if rel not in texts:
            texts[rel] = open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        return texts[rel]

    for i, (rel, old, new) in enumerate(EDITS, 1):
        t = get(rel)
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", i); continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING %d (%s): %s" % (i, rel.split("/")[-1], [t.count(old), t.count(old.replace("\n", "\r\n"))]))
            fails += 1; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + str(i))
    t = get(FTR)
    if FTR_LINES[0] in t:
        print("ALREADY ftr")
    else:
        lines = t.split("\n")
        k = [j for j, l in enumerate(lines) if l.rstrip("\r") == FTR_ANCHOR]
        if len(k) != 1:
            print("REFUSING ftr anchor", len(k)); fails += 1
        else:
            cr = "\r" if lines[k[0]].endswith("\r") else ""
            lines[k[0] + 1:k[0] + 1] = [x + cr for x in FTR_LINES]
            texts[FTR] = "\n".join(lines)
            print(("PATCHED " if apply else "WOULD PATCH ") + "ftr")
    t = get(AC)
    lines = t.split("\n")
    st = [j for j, l in enumerate(lines) if l.startswith(STATUS_PREFIX)]
    if any(l.startswith('status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS') for l in lines):
        print("ALREADY status")
    elif len(st) != 1:
        print("REFUSING status", len(st)); fails += 1
    else:
        old = lines[st[0]].rstrip("\r")
        cr = "\r" if lines[st[0]].endswith("\r") else ""
        tail = old[len(STATUS_PREFIX):]
        # keep the rest of the history after the GI-15 clause
        rest = tail.split("live. ", 1)[1] if "live. " in tail else tail
        lines[st[0]] = ('status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; '
                        'documented_rule READY): GI-15 answered 2026-10-01 (OPUS, static - every per-site helper read, '
                        'see the GI-15 section; what remains is content, not code; review requested from SWE2-AUDIT-SEM). '
                        'History: PARTIAL on GI-15 from 2026-10-01 (SWE2-FRONTIER, on SWE2-AUDIT-SEM\'s REJECT of '
                        'c97af7156, record dd-restatus-gi-0930). ' + rest) + cr
        texts[AC] = "\n".join(lines)
        print(("PATCHED " if apply else "WOULD PATCH ") + "status")
    t = texts[AC]
    if SECTION_HEAD in t:
        print("ALREADY section")
    else:
        eol = "\r\n" if "\r\n" in t else "\n"
        sec = io.open(os.path.join(HERE, "gi15_section.md"), encoding="utf-8").read().strip("\n").replace("\n", eol)
        if not t.endswith(eol):
            t += eol
        texts[AC] = t + eol + sec + eol
        print(("PATCHED " if apply else "WOULD PATCH ") + "section")
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
