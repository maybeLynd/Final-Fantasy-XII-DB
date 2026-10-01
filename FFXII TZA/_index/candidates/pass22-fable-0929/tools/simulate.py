"""Apply a page's draft (<basename>.crossing.md) to the page text, in memory only.

Draft blocks:
  <!-- INSERT heading="<exact heading line>" -->  ...text...  <!-- END INSERT -->
      appended at the end of that section (before the next line that starts with 1-3 '#' and a space)
  <!-- REPLACE -->  <!-- OLD -->  ...  <!-- NEW -->  ...  <!-- END REPLACE -->
      exact replacement of OLD by NEW; OLD must occur exactly once
Nothing is written to disk.
"""
import io, os, re

INS = re.compile(r'<!-- INSERT heading="(.*?)" -->\n(.*?)\n<!-- END INSERT -->', re.S)
REP = re.compile(r'<!-- REPLACE -->\n<!-- OLD -->\n(.*?)\n<!-- NEW -->\n(.*?)\n<!-- END REPLACE -->', re.S)


def draft_path(rel, draftdir):
    return os.path.join(draftdir, os.path.basename(rel)[:-3] + ".crossing.md")


def insert(rel, text, draftdir):
    p = draft_path(rel, draftdir)
    if not os.path.isfile(p):
        return text
    draft = io.open(p, encoding="utf-8").read().replace("\r\n", "\n")
    nl = "\r\n" if "\r\n" in text else "\n"
    t = text.replace("\r\n", "\n")
    for old, new in REP.findall(draft):
        n = t.count(old)
        if n != 1:
            raise SystemExit("REPLACE old text found %d times in %s" % (n, rel))
        t = t.replace(old, new)
    for heading, body in INS.findall(draft):
        lines = t.split("\n")
        idx = [i for i, ln in enumerate(lines) if ln.rstrip() == heading]
        if len(idx) != 1:
            raise SystemExit("heading %r found %d times in %s" % (heading, len(idx), rel))
        end = len(lines)
        for j in range(idx[0] + 1, len(lines)):
            if re.match(r"#{1,3} ", lines[j]):
                end = j
                break
        k = end
        while k > idx[0] + 1 and lines[k - 1].strip() == "":
            k -= 1
        lines = lines[:k] + [""] + body.split("\n") + [""] + lines[end:] if end < len(lines) \
            else lines[:k] + [""] + body.split("\n") + [""]
        t = "\n".join(lines)
    return t.replace("\n", nl)
