#!/usr/bin/env python3
"""emit_seeded_census.py - write a standard *-accesses.tsv for a type whose route is NOT seedable.

WHY IT EXISTS. `gen_route_seeded_census.py` writes the artifact, but only for a route it models
(PTR / FN / STATIC). Three of the render-root types are `EMBED` and a fourth shares its `FN`
route with a sibling, so none of them can produce an artifact that way - and without one,
`project_embed_census.py` reports `parent has no census` and every child stays unprojectable.
That is how five types I declared today ended up with no artifacts at all.

THE SEEDS ARE THE CONTRACT. Each type here is censused from functions PROVED to receive it as
argument 0, and the proof is named in `WHY` beside the seeds rather than left to the reader.
This is the same restriction that makes these safe where the bare `FN 0x002ED570+0x0` route is
not: that route reaches three different element types and names one, so a census seeded from it
conflates them (43 offsets against 26, measured). A census seeded from proven entry points does
not, and the emitted file says which seeds produced it.

    emit_seeded_census.py --list
    emit_seeded_census.py --type RenderStrideC0Bank
"""
import argparse
import collections
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ROOT = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
os.chdir(_ROOT)
sys.path.insert(0, HERE)

import gen_route_seeded_census as RC  # noqa: E402
import check_default_instance_writers as W  # noqa: E402
import kit_paths as KP  # noqa: E402

JOBS = {
    "RenderStrideC0Bank": dict(
        size=0x90, out="17-Presentation-Rendering/render-stride-c0-bank-accesses.tsv",
        seeds=[0x0046E250, 0x0046E4B0, 0x0046E3E0, 0x0046E0F0, 0x0046E640, 0x0046E1B0],
        why=("every one is called on [render root +0xD98]; 0046E250 and 0046E4B0 from 0041E3A0, "
             "0046E0F0 from its only caller 0041E340, and 0046E640/0046E1B0 found by an "
             "independent enumeration of the 65 functions that load a bank from that slot"),
        control={0x60}),
    "RenderResourceEntryBank": dict(
        size=0x60, out="17-Presentation-Rendering/render-resource-entry-bank-accesses.tsv",
        seeds=[0x00409F10, 0x00409F70, 0x00409F80],
        why=("00409F10 is the initialiser called on [render root +0xD90] at 0041E439/0041E442, "
             "00409F70 is that slot's refresh handler and 00409F80 its constructor"),
        control={0x48, 0x4C}),
    "PresentationEntryReferenceContainer": dict(
        size=0xC30,
        out="17-Presentation-Rendering/presentation-entry-reference-container-accesses.tsv",
        seeds=[0x0051BA20, 0x0051B9F0, 0x0051B9D0, 0x0051B970],
        why=("all four are called on [render root +0xDA8]: 0051BA20 is the constructor and "
             "0051B9D0 the initialiser, both from 0041E3A0 (0041E42F, 0041E469); 0051B9F0 is "
             "that slot's refresh handler, called from 0041E500 at 0041E536; 0051B970 is "
             "called on the same slot from 0041E340 at 0041E364"),
        control={0x10, 0x14}),
    # NOT a render type, and it is here because its route is SLOTPTR - which no census tool
    # models - and its 8-slot registry at 0209C4D0 is reached by `lea` (18 address-takings in
    # 16 functions) rather than by indexed load, so a displacement scan sees nothing. THE SEEDS
    # WERE DERIVED FROM THE TYPE'S OWN CITATIONS: 63 distinct addresses cited across its rows,
    # mapped to their containing functions, ranked by citation weight. The top two were
    # Widget's constructor and factory - which is how this type was identified as a widget -
    # and these four are the record-taking remainder.
    "MessageWindowRecord": dict(
        size=0x410, out="16-UI/message-window-record-accesses.tsv",
        seeds=[0x002A6190, 0x002A4830, 0x002A38C0],
        why=("derived from the type's own 63 cited addresses by containing function: 002A6190 "
             "is the handler installed at construction and the store's declared ctor (50 "
             "citations), 002A4830 has 10 and 002A38C0 has 2. 002A2C00 cited 44 times was "
             "SEEDED AND THEN DROPPED: it contributed eight sub-0xC0 accesses - four signed "
             "WORDS at +0x08/+0x0A/+0x0C/+0x0E where Widget declares an 8-byte pointer - so "
             "its arg0 is not this record and the taint reached a foreign object. Widget's ctor "
             "002465F0 and factory 00244F50 cite higher still but take a widget generically, "
             "so they are excluded as seeds"),
        control={0x1A8, 0x3E8, 0x3F0}),
    "BattleMenuWidget2DC0": dict(
        size=0x2DC0, out="16-UI/battle-menu-widget-2dc0-accesses.tsv",
        seeds=[0x002778C0, 0x00275440, 0x002753F0, 0x00249C60, 0x0027B430,
               0x00244960, 0x002470D0, 0x002470C0, 0x005C5230],
        why=("002778C0 is the REGISTERED HANDLER - passed in r8 at 00276DE6 beside "
             "`mov edx, 0x2DC0` and `call 00245000` with storage `lea rcx, [rdi+0x220]` - so "
             "its rcx is this object BY CONSTRUCTION, which is this kit's own admissibility "
             "rule for widget arg0. The other eight are the functions that handler passes the "
             "object to in rcx, the same one-level rule scan_widget_one_level uses; 00244960 is "
             "already a CORE function in gen_widget_census, which is independent corroboration "
             "that the object is a widget"),
        control={0xC4, 0xD0, 0x2DB6}),
    "BattleMenuPanelWidget3010": dict(
        size=0x3010, out="16-UI/battle-menu-panel-widget-3010-accesses.tsv",
        seeds=[0x00276D30, 0x00275440, 0x00247930, 0x00244F00, 0x00247560,
               0x00277300, 0x00276F80],
        why=("00276D30 is the REGISTERED HANDLER of the 0x3010 widget built at 0027A42D "
             "(`mov edx, 0x3010` ; `lea rcx, [rbx+0xC0]` ; `call 00245000`), so its rcx is the "
             "object by construction; the rest are functions it passes the object to in rcx. "
             "0x3010 is also the child stride the-widget-constructor-and-object-sizes.md "
             "derives arithmetically for this parent, so the extent is corroborated twice"),
        control={0x98, 0x100, 0x2FF8}),
    "RenderResourceEntry": dict(
        size=0x50, out="17-Presentation-Rendering/render-resource-entry-accesses.tsv",
        seeds=[0x00409710, 0x00409A60, 0x00409A30, 0x00409600],
        why=("00409FE0 resolves an entry at 0040A055 and does `mov rdi, rax` at 0040A05D, then "
             "passes that rdi to 00409710, 00409A60 and 00409A30; 00409600 is the store's own "
             "ResourceEntry_GetResolvedBasePointer. NOTE these seeds are DELIBERATELY not the "
             "declared `FN 0x002ED570+0x0` route, which is shared with RenderStrideC0Element "
             "and conflates three banks"),
        control={0x04, 0x30, 0x38}),
    # Added 2026-09-20 (OPUS). THE SEEDS ARE A VTABLE, which is the strongest arg0 proof this
    # file can have: every one of the 31 slots at 00903B68 is a virtual method of this object,
    # so each receives it in rcx BY DEFINITION rather than by a dataflow argument. All 31 land
    # in .text. Plus the constructor and destructor the store already names.
    # WHY IT MATTERS: CharacterRenderObject is a HEAP type with NO route - `heap; allocated in
    # FUN_001BD4A0 at 001BD527` - so no route-seeded census can reach it at all, and it carried
    # 894 of its 1640 bytes in six `unobserved` rows. It was the largest unobserved byte range
    # of any non-Phyre routeless type in the store.
    # THE CONTROL IS THE STORE'S OWN DESTRUCTOR READING, not a guess: the type row records that
    # 001F51E0 clears +0x28, destroys an interior sub-object at +0x3E0 and reads +0x390. The
    # destructor is in the seed set, so all three MUST appear or the walk is broken.
    "CharacterRenderObject": dict(
        size=0x668,
        out="17-Presentation-Rendering/Character-Rendering/character-render-object-accesses.tsv",
        seeds=[0x001F4DA0, 0x001F51E0,
               0x001F52F0, 0x001F89B0, 0x001F6E70, 0x001F6D60, 0x001FB070, 0x001F86E0,
               0x001F9FF0, 0x001FB080, 0x001F9B20, 0x001F9A80, 0x001F8C00, 0x001F8BE0,
               0x001F8C70, 0x001FB120, 0x001FA0A0, 0x001F9A60, 0x001FA3D0, 0x001F5C10,
               0x001FAFB0, 0x001F8D10, 0x001FA0E0, 0x001FA810, 0x001F9FE0, 0x001F9A70,
               0x001FA1A0, 0x001FAD40, 0x001FAA10, 0x001F86D0, 0x001F6E50, 0x00848340,
               0x001FA820],
        why=("the 31 slots of the vtable at 00903B68, read out of the image (all 31 in .text), "
             "plus the constructor 001F4DA0 and destructor 001F51E0 the store's own columns "
             "name. A vtable slot takes the object in rcx by definition - this is the one seed "
             "set that needs no dataflow argument. Slot 29 (00848340) sits far from the 001Fxxxx "
             "cluster and may be a shared thunk; the emitter's own `exposed` marking is left to "
             "say so rather than dropping it by hand"),
        control={0x28, 0x390, 0x3E0}),
}


def run(name, job):
    img = W.Image()
    c = RC.Census(img, job["size"])
    c.rule_text = "seeded on proven entry points: %s" % ", ".join(
        "%08X" % s for s in job["seeds"])
    acc = collections.defaultdict(set)
    for e in job["seeds"]:
        if e not in img.sizes:
            print("  !! seed %08X unknown to this image" % e)
            continue
        fwd = set()
        c.walk(e, {W.ARG_REGS[0]: 0}, acc, fwd, None)
        for g in sorted(fwd):
            if g[0] in img.sizes:
                # SLOTS 5 AND UP ARRIVE ON THE STACK and have no register to seed. The walk
                # started emitting them on 2026-09-20; this loop indexed ARG_REGS blindly and
                # raised IndexError the first time a seeded function passed the object as a
                # fifth argument. Same dispatch as gen_route_seeded_census.run.
                if g[1] <= len(W.ARG_REGS):
                    c.walk(g[0], {W.ARG_REGS[g[1] - 1]: g[2]}, acc, set(), None)
                else:
                    c.walk(g[0], {}, acc, set(), None, stack_seed=(g[1], g[2]))
    missing = job["control"] - set(acc)
    print("  offsets %d, highest 0x%X, control %d/%d%s"
          % (len(acc), max(acc) if acc else 0,
             len(job["control"]) - len(missing), len(job["control"]),
             "" if not missing else "  MISSING " + ", ".join("0x%X" % m
                                                             for m in sorted(missing))))
    if missing:
        print("  ** CONTROL FAILED - refusing to write. **")
        return None
    over = [d for d in acc if d >= job["size"]]
    if over:
        print("  ** %d access(es) at or beyond the declared 0x%X - refusing to write. **"
              % (len(over), job["size"]))
        return None
    return c


def emit(name, job, c):
    path = os.path.join(KP.DB, *job["out"].split("/"))
    names = {}
    fp = os.path.join(KP.WORK, "graph", "functions.tsv")
    for line in io.open(fp, encoding="utf-8", errors="replace"):
        p = line.rstrip("\n").split("\t")
        if len(p) > 1:
            try:
                names[int(p[0], 16)] = p[1]
            except ValueError:
                pass
    hdr = ["function", "name", "site", "disp", "kind", "instruction", "route", "note"]
    out = [hdr]
    for r in sorted(c.rows, key=lambda x: (x[2], x[1])):
        out.append(["%08X" % r[0], names.get(r[0], ""), "%08X" % r[1], "0x%X" % r[2],
                    r[4], r[5], c.rule_text, ""])
    body = "\n".join("\t".join(x) for x in out) + "\n"
    io.open(path, "w", encoding="utf-8", newline="\n").write(
        "# %s - emitted by emit_seeded_census.py\n"
        "# SEEDS AND WHY: %s\n"
        "# The declared route is not used: see the type row. A census seeded from proven\n"
        "# entry points is restricted where a shared route would conflate siblings.\n"
        "%s" % (name, job["why"], body))
    print("  wrote %s (%d rows)" % (job["out"], len(out) - 1))
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.list or not (a.type or a.all):
        print("types this script can emit:")
        for k, v in sorted(JOBS.items()):
            print("  %-26s size 0x%-5X -> %s" % (k, v["size"], v["out"]))
        return 0
    todo = sorted(JOBS) if a.all else [a.type]
    rc = 0
    for name in todo:
        if name not in JOBS:
            print("%s: not a type this script knows" % name)
            rc = 2
            continue
        print("%s:" % name)
        c = run(name, JOBS[name])
        if c is None:
            rc = 2
            continue
        emit(name, JOBS[name], c)
    return rc


if __name__ == "__main__":
    sys.exit(main())
