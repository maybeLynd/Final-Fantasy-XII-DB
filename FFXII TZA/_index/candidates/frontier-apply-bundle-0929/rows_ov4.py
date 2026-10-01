# rows_ov4.py IN OUT - mark register rows OV-17, OV-34, OV-35, OV-36 ANSWERED (FABLE, Claude Opus 5.5, 2026-09-29).
# Replaces the status cell that starts " | **OPEN**" on each row, keeping the old status as struck history.
# Refuses unless each row is found exactly once and still OPEN.
import sys
NEW = {
 "OV-17": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): the tables live exactly as long as the bound payload (the actor-request page section 7); every shipped PUSHI/PUSHF constant (10.3M), variable-descriptor (16.9M) and jump (9.35M) operand is in range, though only jumps are bounded natively.** Evidence `_index/candidates/ov17-constant-bounds-fable/` (constant_bounds.py, var_bounds.py, jump_bounds.py), a4bd85536 and c714a1f01.",
 "OV-34": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): no dispatcher exists; a state1 owner leaves state1 only by deletion.** Evidence `_index/candidates/ov34-state1-owner-fable/state1.py` A D G C, d0362ab82.",
 "OV-35": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): the metadata is the manager's .mot PKFL directory; selector = recorded resource-set index; mode = group-to-namespace mapping; indices g 0-3, i 0-15.** Evidence `_index/candidates/ov35-source-metadata-fable/metadata.py` S K M.",
 "OV-36": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): a queue slot delivers its callback at most once and an owner has one live request; reentrancy universality stays under OV-2's limit.** Evidence `_index/candidates/ov36-callback-delivery-fable/delivery.py` D P H O R.",
}
def apply(t):
    lines = t.split("\n"); hits = {q: 0 for q in NEW}
    for i, l in enumerate(lines):
        for q, new in NEW.items():
            if not l.startswith("| %s |" % q): continue
            cr = "\r" if l.endswith("\r") else ""
            body = l.rstrip("\r")
            k = body.rfind(" | **OPEN**")
            if k < 0 or not body.endswith(" |"): continue
            old = body[k + 3:-2].strip()
            lines[i] = body[:k] + " | " + new + " *Previous status, kept as history:* ~~" + old.replace("~~", "") + "~~ |" + cr
            hits[q] += 1
    bad = {q: n for q, n in hits.items() if n != 1}
    if bad: sys.exit("REFUSE: %s" % bad)
    return "\n".join(lines)
if __name__ == "__main__":
    t = open(sys.argv[1], encoding="utf-8", newline="").read()
    open(sys.argv[2], "w", encoding="utf-8", newline="").write(apply(t)); print("ok")
