"""Byte-check every '## SWE2-EC7-<n> update ... `HEAD`' section in the database tree.

For the section's head function (a listed entry), disassemble the listed extent linearly and test:
  (1) every `call XXXXXXXX` the section names is a direct call/jmp target of the body;
  (2) every 8-hex address the section cites inside [head, head+size) is an instruction boundary.
A section that fails either is reported. Controls: the same two tests over sections NOT written by that
lane (any '## ' section whose title carries a `HEAD` address) give the false-alarm rate of the instrument.
"""
import re, os, struct, collections, sys
import capstone

REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
DB = REPO + r"\Database\FFXII TZA"
ROOT = REPO + r"\Database\Tools\work"
d = open(ROOT + r"/exe/FFXII_TZA.exe", "rb").read()
_pe = struct.unpack_from("<I", d, 0x3C)[0]
_secs = []
_o = _pe + 24 + struct.unpack_from("<H", d, _pe + 20)[0]
for _i in range(struct.unpack_from("<H", d, _pe + 6)[0]):
    _vs, _va, _rs, _ro = struct.unpack_from("<IIII", d, _o + 8)
    _secs.append((_va, _ro, _rs))
    _o += 40


def off(va):
    rva = va - 0x120000
    for a, ro, rs in _secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None
sizes = {}
for line in open(ROOT + r"\graph\functions.tsv", encoding="utf-8", errors="replace"):
    p = line.split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError):
        pass
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def facts(a):
    n = sizes[a]
    bounds, targets = set(), set()
    for x in md.disasm(d[off(a):off(a) + n], a):
        bounds.add(x.address)
        if x.mnemonic in ("call", "jmp") or x.mnemonic.startswith("j"):
            try:
                targets.add(int(x.op_str, 16))
            except ValueError:
                pass
    return bounds, targets


HEAD_RE = re.compile(r"^## (.*)$")
res = {"ec7": collections.Counter(), "other": collections.Counter()}
bad = []
for dp, dn, fn in os.walk(DB):
    if "_inbox" in dp or "_index" in dp:
        continue
    for f in fn:
        if not f.endswith(".md"):
            continue
        text = open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
        parts = re.split(r"(?m)^(?=## )", text)
        for sec in parts:
            title = sec.split("\n", 1)[0]
            m = re.search(r"`([0-9A-F]{8})`", title)
            if not m:
                continue
            a = int(m.group(1), 16)
            if a not in sizes or off(a) is None or sizes[a] > 6000:
                continue
            kind = "ec7" if re.search(r"SWE2-EC7-\d+ update", title) else "other"
            bounds, targets = facts(a)
            claimed = {int(t, 16) for t in re.findall(r"`call ([0-9A-F]{8})`", sec)}
            # only calls attributed to this head: keep targets not themselves heads of another body cited with a site
            interior = {int(t, 16) for t in re.findall(r"\b([0-9A-F]{8})\b", sec)}
            interior = {t for t in interior if a < t < a + sizes[a]}
            c = res[kind]
            c["sections"] += 1
            miss_calls = {t for t in claimed if t not in targets}
            miss_bound = {t for t in interior if t not in bounds}
            c["claimed calls"] += len(claimed)
            c["claimed calls absent from the body"] += len(miss_calls)
            c["interior cites"] += len(interior)
            c["interior cites off an instruction boundary"] += len(miss_bound)
            if miss_calls or miss_bound:
                c["sections failing"] += 1
                if kind == "ec7":
                    bad.append((os.path.relpath(os.path.join(dp, f), DB), "%08X" % a, len(claimed), len(miss_calls),
                                len(interior), len(miss_bound)))
for k, c in res.items():
    print("#", k, dict(c))
print("page\thead\tcalls_claimed\tcalls_absent\tinterior_cited\tinterior_off_boundary")
for b in sorted(bad):
    print("\t".join(str(x) for x in b))
