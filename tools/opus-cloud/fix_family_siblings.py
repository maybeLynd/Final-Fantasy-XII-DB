"""fix_family_siblings.py - make the drafter's family-sibling rows self-contained (OPUS, 2026-10-03).

The drafter wrote siblings as "... of its family base (see family)", naming the base only in a note ingest drops, so the
row could not be read on the page. Each sibling is checked at the bytes to have the base's instruction form (mnemonics
equal; operands equal except rip targets, branch targets and the family's varying immediates), its own values are read
from its body, and its row becomes the base's full sentence with those values. Idempotent: rows no longer carrying the
"(see family)" marker are left alone."""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import listing as L  # noqa: E402
import cloudlib as cl  # noqa: E402
sys.path.insert(0, cl.KIT)
import retool  # noqa: E402
R = retool.R

C = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "FFXII TZA", "_index", "candidates"))


def body(f):
    return list(R.md.disasm(R.at(f, L.sizes()[f]), f))


def rip(i):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+|\d+)\]", i.op_str)
    if not m:
        return None
    d = int(m.group(2), 0)
    return i.address + i.size + (d if m.group(1) == "+" else -d)


def shape(f):
    out = []
    for i in body(f):
        op = re.sub(r"\[rip [+-] (0x[0-9a-f]+|\d+)\]", "[rip+X]", i.op_str)
        if i.mnemonic.startswith("j") or i.mnemonic == "call":
            op = "T"
        op = re.sub(r"\b0x[0-9a-f]+\b", "N", op)
        out.append((i.mnemonic, op))
    return out


def same_form(a, b):
    return shape(a) == shape(b)


def tag_values(f):
    """tag dword address + text, and the pointer stored to [rdx] (both stores name it)."""
    b = body(f)
    t = next(i for i in b if i.mnemonic == "mov" and i.op_str.startswith("r11d, dword ptr [rip"))
    ta = rip(t)
    txt = R.at(ta, 4).decode("ascii")
    st = {rip(i) for i in b if i.mnemonic == "lea" and i.op_str.startswith("rax, [rip")}
    assert len(st) == 1, ("%08X" % f, st)
    return ta, txt, st.pop()


def walk_values(f):
    b = body(f)
    call = next(i for i in b if i.mnemonic == "call")
    step = next(i for i in b if i.mnemonic == "add" and i.op_str.startswith("rsi, "))
    return int(call.op_str, 16), int(step.op_str.split(", ")[1], 0)


TAG_BASE = 0x007AD9A0
WALK_BASE = 0x00220DE0


def tag_text(f):
    ta, txt, st = tag_values(f)
    return ("with `h` = qword `[rcx]`, scans byte `[h+8]` 16-byte entries starting at `h` + word `[h+6]` for the first "
            "whose dword `+0` equals the tag `%s` (dword `%08X`); stores `%08X` to qword `[rdx]` and, to qword `[rdx+8]`, "
            "`h` + dword `+8` of the matching entry, or 0 when none matches; returns `rdx`" % (txt, ta, st))


def walk_text(f):
    callee, step = walk_values(f)
    return ("returns without work when byte `[rcx+0x90]` is non-zero or `edx` is zero; otherwise it calls `%08X(rcx, edx)`, "
            "reads the byte at `rsp+0x50` once (the body's own `rcx` home slot, before the loop writes it), then `edx` "
            "times stores `p` = qword `[rcx]` + `i` (with `i` stepping by 0x%X) to that slot and calls "
            "`00199DB0(rcx+0x20, rsp+0x20, &slot, that byte)`; finally it re-reads byte `[rcx+0x90]` and stores 1 there "
            "when it is zero, 0 otherwise" % (callee, step))


NODE_BASE = 0x005850F0


def node_values(f):
    b = body(f)
    t = lambda i: rip(i)
    node = t(next(i for i in b if i.mnemonic == "lea" and i.op_str.startswith("rdi, [rip")))
    guard = t(next(i for i in b if i.mnemonic == "cmp" and i.op_str.startswith("dword ptr [rip")))
    calls = [int(i.op_str, 16) for i in b if i.mnemonic == "call" and i.op_str.startswith("0x")]
    k1, k2 = calls[1], calls[2]          # calls[0] is 008092FC
    v28 = t(next(i for i in b if i.mnemonic == "lea" and i.op_str.startswith("rax, [rip")))
    leas_rcx = [t(i) for i in b if i.mnemonic == "lea" and i.op_str.startswith("rcx, [rip")]
    atexit = next(x for x in leas_rcx if x not in (guard,))
    tree = t(next(i for i in b if i.mnemonic == "lea" and i.op_str.startswith("rbx, [rip")))
    root = t(next(i for i in b if i.mnemonic == "lea" and i.op_str.startswith("r10, [rip")))
    assert calls[0] == 0x8092FC and 0x808B90 in calls and 0x80929C in calls and calls[-1] == 0x67F700, calls
    return node, guard, k1, k2, v28, atexit, tree, root


def node_text(f):
    node, guard, k1, k2, v28, atexit, tree, root = node_values(f)
    return ("when dword `%08X` is above the epoch dword at `+4` of this thread's TLS block (index dword `02EAED3C`) it "
            "runs `008092FC(%08X)` and, when `%08X` is then -1, fills the node at `%08X`: qwords `+0`/`+8`/`+0x10` = the "
            "node, qword `+0x18` = the `%08X()` result and `+0x20` = the `%08X()` result (called first), qword `+0x28` = "
            "`%08X`, registers `00808B90(%08X)` and closes with `0080929C(%08X)`; on every path it then sets bit `0x1` of "
            "qword `+0x10`, sets `+0`/`+8` to `%08X`, and walks the tree from the root qword `%08X` comparing (qword "
            "`+0x18`, qword `+0x20`) with each node's pair: an equal pair returns without linking; otherwise the node "
            "becomes child `+0` (smaller) or `+8` (larger) of the last node visited (or the root when the tree is empty), "
            "its qword `+0x10` = that parent + 1, and it calls `0067F700(%08X, node)`"
            % (guard, guard, guard, node, k2, k1, v28, atexit, guard, tree, root, tree))


def fix(rec, fams):
    p = os.path.join(C, rec, "rows.json")
    d = json.load(io.open(p, encoding="utf-8"))
    changed = []
    for r in d["rows"]:
        f = int(r["fn"], 16)
        for base, mk in fams:
            if f != base and "(see family)" not in r["text"]:
                continue
            if f == base or (same_form(base, f) and "(see family)" in r["text"]):
                new = mk(f)
                if f != base and new != r["text"]:
                    r["text"] = new
                    changed.append(r["fn"])
                break
    if changed:
        d.setdefault("corrections", []).append({"fn": ", ".join(changed), "why": "OPUS re-read: family-sibling rows "
            "referred to an unnamed 'family base'; each sibling checked at the bytes to share the base's instruction form "
            "and rewritten as a self-contained sentence with its own values (fix_family_siblings.py)"})
        json.dump(d, io.open(p, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
    left = [r["fn"] for r in d["rows"] if "(see family)" in r["text"]]
    print(rec, "rewritten", len(changed), changed, "still marked", left)


if __name__ == "__main__":
    fix("opus-sead-win-config-ee-1003", [(TAG_BASE, tag_text), (WALK_BASE, walk_text)])
    fix("opus-the-lua-loader-and-what-it-accepts-ee-1003", [(NODE_BASE, node_text)])
