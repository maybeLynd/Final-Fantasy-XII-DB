"""apply_items.py [--apply] - 18-Audio readiness-map items 16-18 (RE repo docs/readiness/18-audio.md, the SFID
contradictions), settled on the pages (OPUS, 2026-10-02; control items_check.py).

16 pan axes: SFID calls pan / frpan / udpan three axes; UQ-242 (answered 2026-09-18) reads pan as an azimuth, frpan as
   a distance factor, and udpan as carried and unused.
17 volume ceiling: SFID calls DAT_01cebba8 a configurable global; it is the float 1.0 that no instruction writes.
18 output channels: the REQ geometry lists rings for two, six and eight outputs; 02EAD34C's one writer stores 8.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
SFID = "18-Audio/sead-function-identification.md"
REQ = "18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md"
EDITS = [
    (SFID, "indicates\n**three panning axes**, not one: left/right, front/rear, and up/down.",
     "indicates\n~~**three panning axes**, not one: left/right, front/rear, and up/down.~~ three ranges, but not three axes: "
     "the driver turns `pan` into an azimuth and `frpan` into a distance factor, and carries `udpan` down to `007B8430` "
     "without using it *(corrected 2026-10-02, OPUS, from UQ-242's dated answer - the request page's geometry)*."),
    (SFID, "The upper bound is a global (`DAT_01cebba8`), not a literal — so the volume ceiling is\nconfigurable rather than hardcoded.",
     "The upper bound is a global (`DAT_01cebba8`), not a literal — ~~so the volume ceiling is\nconfigurable rather than "
     "hardcoded.~~ but that global is the float constant 1.0, which no instruction writes (1,488 reads), so the ceiling "
     "is fixed at 1.0 *(corrected 2026-10-02, OPUS, at the bytes)*."),
    (SFID, "The summary is accurate in substance — the function does handle three panning axes —",
     "The summary is accurate in substance — the function does handle three panning ~~axes~~ ranges *(only two are "
     "used; see §2, corrected 2026-10-02, OPUS)* —"),
    (REQ, "and those plus 90 and 270 for eight ([pan_speaker_tables.py](members/pan_speaker_tables.py), [pan-speaker-tables.tsv](members/pan-speaker-tables.tsv))",
     "and those plus 90 and 270 for eight ([pan_speaker_tables.py](members/pan_speaker_tables.py), [pan-speaker-tables.tsv](members/pan-speaker-tables.tsv)) "
     "*(2026-10-02, OPUS: in this build the count is always 8 - `02EAD34C` has one writer, the device init `007AEF30`, "
     "which stores the literal 8 - so only the eight-output ring is used and the two- and six-output rows are not "
     "reached)*"),
]


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
