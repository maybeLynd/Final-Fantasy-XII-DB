"""apply_26pkfl.py [--apply] - 26-PKFL-Package-Container readiness map (re-readiness/26-pkfl.md), section 3.1 value
items X-1..X-15 and the section 3.2 stale / banner items the image or the shipped packages settle (OPUS, 2026-10-02).

Each edit strikes the side the shipping image or the shipped data REFUTES only and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)*, or answers a stale "open / not read" line with *(answered: see ...; 2026-10-02,
OPUS)*. The data: every .mot / .snd / .vpc / .vpcjp entry of FFXII_TZA.vbf read through ff12_content.vbf_load_index
(block 0 of each, header and directory) under the {u32 offset, u32 size} reading: 10,314 packages, 40,203 present
pairs, offsets and sizes all 0x10-aligned, offsets ascending in slot order in all 10,287 non-empty packages, the
smallest offset 0x800 in every one, each payload starting at the next 0x800 boundary after the one before, no two slots
sharing an offset. Deciding instructions are in the scratch verdicts-26.md; every address inside a function is cited as
entry+offset.
Left without an edit: X-15 (10,045 is every .ebp in the archive, 1,115 the us root - both right, different scopes),
PK:245's 14,337 (the .snd count; all four extensions give 14,373), the sections already under a 2026-09-11 banner except
where a figure there is re-measured here, B-1 .. B-4, B-6, B-9, B-11 .. B-20. The frozen
Tools/work/formats/pkfl-container-census.tsv is generated (four-byte word indices) and goes to SWE2-DATA, not edited.
Every ~~ span opens and closes on one line; multi-line text is struck line by line. The one front-matter edit is a
trailing `# <- corrected` YAML comment (its OLD includes the line end, so NEW never contains OLD). No heading changes.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "26-PKFL-Package-Container/"
RM = F + "README.md"
PK = F + "Container/pkfl-package-container.md"

PAIR = "re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages"
READERS = ("`0032F260` / `0032F290` read the `.mot` table and `0032F2C0` / `0032F2F0` / `0032F3A0` the `.snd` one; "
           "`0032F320` / `0032F360` read only the two 64-slot tables, picked by `r8d`")

EDITS = [
    # X-3: slots in use are 0-15 (16-slot) and 0-13 (64-slot), every index in those ranges used somewhere.
    (PK, "| occupied slot indices | **0–27**, densely — no index in that range is ever unused |",
     "| occupied slot indices | ~~**0–27**, densely — no index in that range is ever unused~~ **0–15** in `.mot` / "
     "`.snd` and **0–13** in `.vpc` / `.vpcjp`, each index in those ranges used somewhere *(corrected 2026-10-02, "
     "OPUS: " + PAIR + "; §7's 2026-09-18 closures)* |"),

    # X-4: the frozen census TSV is the four-byte reading - 10,314 rows agree with it, 27 with the pair reading.
    (PK, "**10,314 common paths,\n10,314 agree, 0 differ.**",
     "~~**10,314 common paths,~~\n~~10,314 agree, 0 differ.**~~ 10,314 common paths, which agree only because both "
     "parses used the withdrawn four-byte entry *(corrected 2026-10-02, OPUS: the TSV's `present` column is the "
     "four-byte word indices of `census_pkfl_container.py`'s `read_dir`; " + PAIR + ", 27 of its 10,314 rows agree - "
     "the empty packages; a re-freeze is SWE2-DATA's)*."),
    (PK, "| occupancy agrees with the independent frozen census | **10,314 / 10,314, zero differences** |",
     "| occupancy agrees with the independent frozen census | ~~**10,314 / 10,314, zero differences**~~ 10,314 / "
     "10,314 under the four-byte reading only, **27 / 10,314** under the pair reading *(corrected 2026-10-02, OPUS: "
     + PAIR + ")* |"),
    (PK, "agrees with the frozen census on **10,314 of 10,314 paths, zero differences.**",
     "agrees with the frozen census on ~~**10,314 of 10,314 paths, zero differences.**~~ 10,314 of 10,314 paths "
     "under the four-byte entry both used, and on 27 under the pair reading *(corrected 2026-10-02, OPUS: " + PAIR +
     ")*."),

    # X-7 + X-8: offsets ascend in slot order in every non-empty package; lengths are stored; no slot shares an offset.
    (PK, "> over all 10,314 files in §5: offsets are **not** ascending in slot order; the first payload is\n> **not** at "
         "the directory end; and a slot's length is **not** reliably the distance to the next\n> slot's offset, because "
         "slots may share one.",
     "> over all 10,314 files in §5: ~~offsets are **not** ascending in slot order;~~ the first payload is\n> **not** at "
     "the directory end; ~~and a slot's length is **not** reliably the distance to the next~~\n> ~~slot's offset, "
     "because slots may share one.~~ *(corrected 2026-10-02, OPUS: two of the three are four-byte-reading artefacts - "
     + PAIR + ", offsets ascend in slot order in all 10,287 non-empty packages, no two slots share an offset, and a "
     "slot's length is its stored size, which `0032F360` reads at `+0xC + 8k`)*"),
    (PK, "\"Offsets are not\n> ascending in slot order\" was not re-measured and is not asserted.",
     "~~\"Offsets are not~~\n> ~~ascending in slot order\" was not re-measured and is not asserted.~~ *(answered: "
     "re-measured 2026-10-02 - offsets ascend in slot order in all 10,287 non-empty packages, the first at `0x800` in "
     "every one and each later payload at the next `0x800` boundary after the one before; 2026-10-02, OPUS)*"),
    (PK, "**1. Offsets are not ascending in slot order — only 4,833 of 10,314.** Slot index is an identity,\nnot a "
         "position. Anything that computes a slot's length by walking slot indices in order is wrong in\nmore than half "
         "the corpus; lengths must be derived after sorting by offset.",
     "~~**1. Offsets are not ascending in slot order — only 4,833 of 10,314.**~~ Slot index is an identity,\nnot a "
     "position. ~~Anything that computes a slot's length by walking slot indices in order is wrong in~~\n~~more than "
     "half the corpus; lengths must be derived after sorting by offset.~~ *(corrected 2026-10-02, OPUS: four-byte-"
     "reading figures; under the pair reading offsets ascend in slot order in all 10,287 non-empty packages and a "
     "length is the stored size)*"),
    (PK, "| Are offsets really not ascending? | **4,833 / 10,314 ascending in slot-index order.**",
     "| Are offsets really not ascending? | ~~**4,833 / 10,314 ascending in slot-index order.**~~ **All 10,287 "
     "non-empty packages ascend** under the pair reading; 4,833 is the four-byte reading's figure *(corrected "
     "2026-10-02, OPUS: " + PAIR + ")*."),
    (PK, "so **no reading makes the\ndirectory ordered**, and §5's conclusion is stronger than the single figure carrying "
         "it.",
     "so ~~**no reading makes the~~\n~~directory ordered**, and §5's conclusion is stronger than the single figure "
     "carrying it.~~ *(corrected 2026-10-02, OPUS: the pair reading makes it ordered - offsets ascend in slot order in "
     "all 10,287 non-empty packages; " + PAIR + ")*"),

    # X-1 + X-2: smallest offset 0x800 in every non-empty package; gap 1,912 (16-slot) / 1,528 (64-slot).
    (PK, "The gap is 1,976 bytes in 4,356 files and\n1,784 in 3,573 — the first payload usually sits at `0x800`. And in "
         "**2,268 files the smallest\npresent offset is `0x40`, which is *before* the 16-slot directory ends at `0x48`.**",
     "The gap is ~~1,976 bytes in 4,356 files and~~\n~~1,784 in 3,573 — the first payload usually sits at `0x800`.~~ "
     "1,912 bytes in every non-empty 16-slot package and 1,528 in every non-empty 64-slot one, the first payload "
     "sitting at `0x800` in all 10,287 *(corrected 2026-10-02, OPUS: " + PAIR + "; the old gaps were measured from "
     "`0x48` / `0x108`)*. ~~And in **2,268 files the smallest~~\n~~present offset is `0x40`, which is *before* the "
     "16-slot directory ends at `0x48`.**~~"),
    (PK, "In a 16-slot package the directory runs\n`+0x08 .. +0x48`, so slot 14's offset word lives at `+0x40` and slot "
         "15's at `+0x44`.",
     "In a 16-slot package the directory runs\n~~`+0x08 .. +0x48`, so slot 14's offset word lives at `+0x40` and slot "
     "15's at `+0x44`.~~ `+0x08 .. +0x88`, and `+0x40` / `+0x44` are slot 7's offset and size *(corrected 2026-10-02, "
     "OPUS: the pair `{offset, size}` of slot `k` sits at `+8 + 8k`, which every reader indexes, e.g. "
     "`0032F260+0x1B`)*."),
    (PK, "| smallest offset `0x40`, 16-slot files | 2,268 | **2,268** |",
     "| smallest offset `0x40`, 16-slot files | ~~2,268~~ 0 | ~~**2,268**~~ **0** - the smallest offset is `0x800` in "
     "all 10,287 non-empty packages *(corrected 2026-10-02, OPUS: " + PAIR + ")* |"),
    (PK, "| offsets ascending in slot order | 4,833 / 10,314 | **4,833** |",
     "| offsets ascending in slot order | ~~4,833 / 10,314~~ 10,287 / 10,287 non-empty | ~~**4,833**~~ **10,287** "
     "*(corrected 2026-10-02, OPUS: " + PAIR + ")* |"),
    (PK, "**Every checkable claim reproduced.**",
     "**Every checkable claim reproduced** - under the same withdrawn four-byte entry *(corrected 2026-10-02, OPUS: "
     "under the pair reading 40,203 pairs are present, the smallest offset is `0x800` and offsets ascend in every "
     "non-empty package, and no two slots share an offset; §5's banner)*."),

    # X-5 + X-6: the repeated 0x40 is a size; the second word of a pair is the slot's size.
    (PK, "and the shared value `0x40` is independently explained: it is the byte offset of slot 14's own directory entry "
         "in a 16-slot package, and the bytes there are the slot-14/15 offset words.",
     "and ~~the shared value `0x40` is independently explained: it is the byte offset of slot 14's own directory entry "
     "in a 16-slot package, and the bytes there are the slot-14/15 offset words.~~ the repeated `0x40` is a size - "
     "14,337 `.snd` pairs have size `0x40` - and `+0x40` of a 16-slot package is slot 7's offset word *(corrected "
     "2026-10-02, OPUS: " + PAIR + ")*."),
    (PK, "**It fails in 2,349 files**, where the odd halves\nalias one location — so the pairing is a directory-level "
         "invariant and not a content-level one.",
     "~~**It fails in 2,349 files**, where the odd halves~~\n~~alias one location — so the pairing is a "
     "directory-level invariant and not a content-level one.~~ *(corrected 2026-10-02, OPUS: the odd halves are "
     "sizes, so equal values are equal sizes, not a shared location - under the pair reading no two slots of any "
     "package share an offset)*"),
    (PK, "The even/odd pairing is described structurally and **no reading of \"even = data, odd = descriptor\"\n  is "
         "asserted**, though the aliasing evidence is consistent with it.",
     "~~The even/odd pairing is described structurally and **no reading of \"even = data, odd = descriptor\"~~\n  ~~is "
     "asserted**, though the aliasing evidence is consistent with it.~~ The second word of each pair is the slot's "
     "size, not a descriptor *(corrected 2026-10-02, OPUS: `0032F360+0x2E` reads `[table + 8k + 0xC]` as the size; "
     "the 2026-09-11 correction in §8)*."),

    # X-13: 74,340 is the four-byte word count; under the pair reading 40,203 pairs, offsets and sizes all 0x10-aligned.
    (PK, "**Invariants — every one measured over all 10,314 packages and all 74,340 present offsets.**",
     "**Invariants — every one measured over all 10,314 packages and all ~~74,340 present offsets~~ 74,340 non-zero "
     "words of the four-byte reading.** *(corrected 2026-10-02, OPUS: under the pair reading 40,203 pairs are "
     "present; the banner below)*"),
    (PK, "| every present offset is **`0x10`-aligned** | **74,340 / 74,340** |",
     "| every present offset is **`0x10`-aligned** | ~~**74,340 / 74,340**~~ **40,203 / 40,203** pairs, offset and "
     "size alike *(corrected 2026-10-02, OPUS: " + PAIR + ")* |"),
    (PK, "**Occupancy is dense and perfectly paired:**\n",
     "~~**Occupancy is dense and perfectly paired:**~~ **The four-byte reading's word occupancy, withdrawn below:** "
     "*(corrected 2026-10-02, OPUS: under the pair reading `.mot` slots 0-15 hold 1,539, 3,186, 1,737, 1,134, 774, "
     "540, 378, 270, 108, 54, 54, 36, 36, 27, 18, 18 packages and `.snd` slots 0-15 hold 2,304 for 0-7, then 9, "
     "1,809, 324, 225, 153, 99, 45, 18; " + PAIR + ")*\n"),

    # X-9: byte 0 is read by every slot reader (cmp byte ptr [buf], 0 -> -1); bytes 1-3 by nothing.
    (PK, "| `+0x00` magic | — | — | — | **yes — `PKFL` occurs 0 times in the whole image, so no memory-operand comparison "
         "is possible either** |",
     "| `+0x00` magic | ~~—~~ byte 0 only, by the seven slot readers (`0032F260+0x13` `cmp byte ptr [rcx], 0` and its "
     "six twins) | ~~—~~ byte 0 zero: every slot read returns -1 | — | ~~**yes — `PKFL` occurs 0 times in the whole "
     "image, so no memory-operand comparison is possible either**~~ **bytes 1-3 yes, byte 0 no** - nothing compares "
     "the magic, which occurs 0 times in the image *(corrected 2026-10-02, OPUS: §7's 2026-09-18 closure)* |"),
    (PK, "Corrupting the first four bytes of a package is\nexpected to change nothing — see §6 for the limit on that "
         "expectation.",
     "~~Corrupting the first four bytes of a package is~~\n~~expected to change nothing — see §6 for the limit on that "
     "expectation.~~ Corrupting bytes 1-3 changes nothing, and so does any non-zero byte 0; a zero byte 0 makes "
     "every slot read of the package return -1 *(corrected 2026-10-02, OPUS: the seven slot readers test only "
     "`cmp byte ptr [buf], 0`, e.g. `0032F260+0x13`; §7's 2026-09-18 closure)*."),

    # X-10: seven readers; 0032F320 / 0032F360 read only the 64-slot tables.
    (PK, "finds exactly six slot readers,",
     "finds exactly ~~six~~ seven slot readers *(corrected 2026-10-02, OPUS: the list names seven; a grep of every "
     "reference to the four tables finds these seven, the allocator `0032F430` and the walker `0032FCA0`)*,"),
    (PK, "`0032F320` for the offset, `0032F360` for the\n> size —",
     "~~`0032F320` for the offset, `0032F360` for the~~\n> ~~size~~ the slot readers *(corrected 2026-10-02, OPUS: "
     + READERS + ")* —"),
    (PK, "`0032F320` /\n`0032F360` (offset / size of slot `k`),",
     "`0032F320` /\n`0032F360` (offset / size of slot `k` in the two 64-slot tables *(corrected 2026-10-02, OPUS: "
     + READERS + ")*),"),
    (RM, "> indexes pairs by slot (`0032F320` / `0032F360`);",
     "> indexes pairs by slot (~~`0032F320` / `0032F360`~~ seven readers *(corrected 2026-10-02, OPUS: " + READERS +
     ")*);"),

    # X-11: four completions, each clearing its own pending bit (12-15) of 022C6E48[manager].
    (PK, "the two completions clear a pending bit in the manager's state\n  word (`022C6E48`, bits 14 and 15) and never "
         "touch the buffer.",
     "~~the two completions clear a pending bit in the manager's state~~\n  ~~word (`022C6E48`, bits 14 and 15)~~ the "
     "four completions each clear one pending bit of the manager's state word `022C6E48` - `003302B0` bit 13 "
     "(`.mot`), `00331760` bit 12 (`.snd`), `00331820` bit 15 (`.vpc`), `003317C0` bit 14 (`.vpcjp`) *(corrected "
     "2026-10-02, OPUS: `003302B0+0x20` `btr rbx, 0xd` and its three twins; the walker sets the same bits, "
     "`0032FCA0+0x20A`, `+0x277`, `+0x2E2`, `+0x34E`)* - and never touch the buffer."),
    (PK, "Static, tier 1: the walker, the allocator, the six readers and the two completions read in full.",
     "Static, tier 1: the walker, the allocator, the ~~six~~ seven readers and the ~~two~~ four completions read in "
     "full *(corrected 2026-10-02, OPUS: as above)*."),

    # X-12: 0032E620 takes five arguments; the voice loader's file offset is the record's first dword.
    (PK, "the voice loader `003E9EF0` issues `0032E620(kind, packId, dest, size)` with that offset as the request's file "
         "offset |",
     "the voice loader `003E9EF0` issues ~~`0032E620(kind, packId, dest, size)` with that offset as the request's file "
     "offset~~ `0032E620(kind, packId, dest, size, &record)` with that offset as the record's first dword *(corrected "
     "2026-10-02, OPUS: `003E9EF0+0x36` stores the `0032F320` result at `[rsp + 0x30]`, `003E9EF0+0x64` passes "
     "`rsp + 0x30` as the fifth argument, and `0032E620+0x3D` loads it to copy the record)* |"),

    # B-7 / B-8: the magic row was closed by the 2026-09-18 body read.
    (PK, "**It is still weaker than a body read**, which is why §7 keeps it open. |",
     "~~**It is still weaker than a body read**, which is why §7 keeps it open.~~ *(answered: §7 closed it 2026-09-18 "
     "by a body read of every directory reader; 2026-10-02, OPUS)* |"),
    (PK, "`PKFL_Bind` and the slot-consumer functions were not\nread, so the *\"magic never validated\"* row still rests on "
         "the whole-image scan the sheet itself\nflags as the weaker instrument in §7.",
     "~~`PKFL_Bind` and the slot-consumer functions were not~~\n~~read, so the *\"magic never validated\"* row still "
     "rests on the whole-image scan the sheet itself~~\n~~flags as the weaker instrument in §7.~~ *(answered: the "
     "magic row rests on a body read since 2026-09-18 - §7, every directory reader; the loader contract itself is "
     "still unaudited; 2026-10-02, OPUS)*"),

    # B-5: the 2026-09-04 parse used the withdrawn four-byte entry.
    (PK, "corpus_validated: \"10,314 / 10,314 shipped packages, every header and directory re-parsed from FFXII_TZA.vbf "
         "2026-09-04\"\n",
     "corpus_validated: \"10,314 / 10,314 shipped packages, every header and directory re-parsed from FFXII_TZA.vbf "
     "2026-09-04\" # <- corrected 2026-10-02, OPUS - that parse read the withdrawn four-byte entry; re-parsed under "
     "the pair reading 2026-09-11 (section 5) and 2026-10-02\n"),

    # README X-1 / X-8 / X-3 / X-14.
    (RM, "Two further corrections from the same re-parse: **offsets are not ascending in slot order** (unlike\nEBP), "
         "and **the first payload is not at the directory end** — in 2,268 files the smallest offset is\n`0x40`, "
         "*before* the 16-slot directory ends at `0x48`.",
     "Two further corrections from the same re-parse: ~~**offsets are not ascending in slot order** (unlike~~\n~~EBP),~~ "
     "and **the first payload is not at the directory end** ~~— in 2,268 files the smallest offset is~~\n~~`0x40`, "
     "*before* the 16-slot directory ends at `0x48`.~~ *(corrected 2026-10-02, OPUS: under the pair reading offsets "
     "ascend in slot order in all 10,287 non-empty packages and the first payload is at `0x800` in every one, 1,912 "
     "or 1,528 bytes past the directory; re-parsed from `FFXII_TZA.vbf`)*"),
    (RM, "**36 of the 64 declared slots are never used in any of the 3,618 64-slot files.** Nothing above\nindex 27 is "
         "ever occupied.",
     "**~~36~~ 50 of the 64 declared slots are never used in any of the 3,618 64-slot files.** Nothing above\nindex "
     "~~27~~ 13 is ever occupied *(corrected 2026-10-02, OPUS: under the pair reading the 64-slot packages use slots "
     "0-13; the container sheet's 2026-09-18 closure)*."),
    (RM, "**2,952 files do not fill their pairs contiguously from 0.**",
     "**~~2,952~~ 4,761 files do not fill their pairs contiguously from 0.** *(corrected 2026-10-02, OPUS: 2,952 is "
     "the four-byte reading's count; " + PAIR + ")*"),
    (RM, "Pairs per file range 0–14; 4,212 files carry exactly one pair, 2,331 carry eight, and",
     "Pairs per file range ~~0–14~~ 0–15; 4,212 files carry exactly one pair, ~~2,331~~ 558 carry eight *(corrected "
     "2026-10-02, OPUS: " + PAIR + "; 0-14 and 2,331 are the four-byte reading's)*, and"),
]


# Pass-22 neighbours (2026-10-02, OPUS): functions of other layers are named by role in NEW text, so the page
# takes on no unaccounted crossing (check_publish_neighbours.py refused the address form).
ROLE_NAMES = [
    ('`0032F260` / `0032F290` read the `.mot` table',
     'two readers read the `.mot` table'),
]
_rn = lambda s: __import__('functools').reduce(lambda a, p: a.replace(p[0], p[1]), ROLE_NAMES, s)
EDITS = [(e[0], _rn(e[1])) if len(e) == 2 else (e[0], e[1], _rn(e[2])) + tuple(e[3:]) for e in EDITS]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
