"""replay_lines.py BASE_DIR NEW_DIR LIVE_DIR LIST [--apply] - replay the line-level change BASE -> NEW (both read with
CR stripped) onto LIVE, keeping every untouched live line byte-for-byte and giving each new line the ending of the live
line it replaces (or of its live neighbour, else the file's majority). Refuses a file whose live content, CR-stripped,
is not the BASE content. Prints per file: lines removed / added. Writes only with --apply."""
import difflib, io, os, sys

base_d, new_d, live_d, lst = sys.argv[1:5]
apply = "--apply" in sys.argv


def rd(p):
    return io.open(p, encoding="utf-8", newline="").read()


def split_keep(t):
    out = t.split("\n")
    return [l + "\n" for l in out[:-1]] + ([out[-1]] if out[-1] else [])


fails = 0
for rel in [l.strip() for l in io.open(lst, encoding="utf-8") if l.strip()]:
    b = [l.rstrip("\r\n") for l in split_keep(rd(os.path.join(base_d, rel)))]
    n = [l.rstrip("\r\n") for l in split_keep(rd(os.path.join(new_d, rel)))]
    lp = os.path.join(live_d, rel)
    live = split_keep(rd(lp))
    lc = [l.rstrip("\r\n") for l in live]
    if lc != b:
        print("REFUSE (live differs from base):", rel); fails += 1; continue
    crlf = sum(l.endswith("\r\n") for l in live)
    major = "\r\n" if crlf * 2 > len(live) else "\n"
    out = []
    rem = add = 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, b, n, autojunk=False).get_opcodes():
        if op == "equal":
            out.extend(live[i1:i2]); continue
        ref = live[i1:i2] or live[max(i1 - 1, 0):i1] or [major]
        for k, j in enumerate(range(j1, j2)):
            r = ref[min(k, len(ref) - 1)]
            end = "\r\n" if r.endswith("\r\n") else ("\n" if r.endswith("\n") else major)
            out.append(n[j] + end)
        rem += i2 - i1; add += j2 - j1
    # last line: keep the live file's final-newline state
    if out and live and not live[-1].endswith("\n"):
        out[-1] = out[-1].rstrip("\r\n")
    res = "".join(out)
    assert [l.rstrip("\r\n") for l in split_keep(res)] == n, rel
    print("%-100s -%d +%d%s" % (rel, rem, add, "" if apply else " (dry)"))
    if apply:
        io.open(lp, "w", encoding="utf-8", newline="").write(res)
print("FAILS %d" % fails)
