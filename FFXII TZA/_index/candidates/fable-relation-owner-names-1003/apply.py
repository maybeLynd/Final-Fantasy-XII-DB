"""apply.py [--apply] - FABLE names the four CharacterRenderRecord relation owner-block bytes +0x65C..+0x65F
(OPUS-REQ-FABLE-RELATION-OWNER-BLOCK-NAMES-1003, 2026-10-03). Name column only, plus one dated NAMED note appended to
each row's evidence; OPUS's meaning text (its 2026-10-03 representation clauses) is untouched.

Refuses a content-dirty _types/fields.tsv (git diff --ignore-cr-at-eol), keeps line endings, idempotent.
Prints PATCHED / ALREADY / WOULD PATCH per row and FAILS n last."""
import io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
REL = "Database/FFXII TZA/_types/fields.tsv"
P = os.path.join(ROOT, REL)
TASK = "OPUS-REQ-FABLE-RELATION-OWNER-BLOCK-NAMES-1003"
RENAMES = [  # (type, offset cell, old name, new name, why)
    ("CharacterRenderRecord", "0x65C", "relationEventFlag", "relationListHead",
     "the head slot index of the record's relation-cache list (00512F30+0x23 starts the walk from it, +0x160 tests it "
     "for 0xFF, +0x16B sets it)"),
    ("CharacterRenderRecord", "0x65D", "embeddedBlockByte65D", "relationListTail",
     "the tail slot index (00512F30+0x158 and +0x16F read it, +0x191 sets it to the new slot)"),
    ("CharacterRenderRecord", "0x65E", "stateByte65E", "relationListCount",
     "the slot count (00512F30+0x10D increments it, 00512CD0+0x97 decrements it with no test, 00512EE0+0xA zeroes it)"),
    ("CharacterRenderRecord", "0x65F", "nibbleByte65F", "inlineRelationKindNibble",
     "the LOW NIBBLE is the inline relation's kind (3 at 00512F30+0x1B9/+0x1BE, 1 at +0x200/+0x205, 0 at +0x1E0 and "
     "00512EE0); the name says nibble because the high nibble is not written by these bodies"),
]


def note(new, why):
    return (" || NAMED %s 2026-10-03 (FABLE, on %s): %s. The names describe the representation only; they say "
            "nothing about natural reachability, and UQ-147's live half stays open." % (new, TASK, why))


def main():
    apply = "--apply" in sys.argv
    fails = 0
    d = subprocess.run(["git", "diff", "--ignore-cr-at-eol", "--name-only", "--", REL], cwd=ROOT,
                       capture_output=True, text=True).stdout.strip()
    if d and apply:
        print("REFUSE: %s is content-dirty" % REL)
        print("FAILS 1")
        return 1
    raw = io.open(P, "rb").read()
    crlf = b"\r\n" in raw[:4000]
    lines = raw.decode("utf-8").split("\r\n" if crlf else "\n")
    changed = False
    for typ, off, old, new, why in RENAMES:
        hits = [k for k, l in enumerate(lines) if l.split("\t")[:2] == [typ, off]]
        if len(hits) != 1:
            print("FAIL %s %s: %d rows" % (typ, off, len(hits))); fails += 1; continue
        c = lines[hits[0]].split("\t")
        if c[3] == new and ("NAMED %s 2026-10-03 (FABLE" % new) in c[8]:
            print("ALREADY %s %s %s" % (typ, off, new)); continue
        if c[3] != old:
            print("FAIL %s %s: name is %r, expected %r" % (typ, off, c[3], old)); fails += 1; continue
        others = [l for l in lines if l.split("\t")[:1] == [typ] and l.split("\t")[3:4] == [new]]
        if others:
            print("FAIL %s: %s already used in the type" % (off, new)); fails += 1; continue
        c[3] = new
        c[8] = c[8] + note(new, why)
        lines[hits[0]] = "\t".join(c)
        changed = True
        print("%s %s %s: %s -> %s" % ("PATCHED" if apply else "WOULD PATCH", typ, off, old, new))
    if changed and apply and not fails:
        io.open(P, "wb").write(("\r\n" if crlf else "\n").join(lines).encode("utf-8"))
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
