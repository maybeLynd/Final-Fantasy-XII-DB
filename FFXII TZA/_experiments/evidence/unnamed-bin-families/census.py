"""The .bin families whose file names occur nowhere in the executable.

Read-only over FFXII_TZA.vbf (set FF12_VBF) and the executable (set FF12_EXE).
A family is a .bin directory with the language segment folded and digit runs folded to '#'. A family is "named" when
the executable holds its file name right after a path separator ('\\' or '/'), with each '#' matched as a digit run,
case-insensitively, in ASCII or in UTF-16LE. Reports the families that are not named, with their files, sizes and
first four bytes, and how many named families share their directory.
Positive controls: battle_message.bin, menumap_sub#.bin, npcdic.bin and musicctrl.bin must be named.
FABLE, 2026-09-13.
"""
import sys, os, io, re, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../Tools/analysis-kit/gfz-scripts"))
from census_format_magics import load_index

BLOCK = 0x10000
f = io.open(os.environ["FF12_VBF"], "rb")
names, blocks = load_index(f)
exe = open(os.environ["FF12_EXE"], "rb").read()


def head(path, n=4):
    sb, size, off = names[path]
    f.seek(off)
    csize = blocks[sb] or BLOCK
    chunk = f.read(csize)
    expected = BLOCK if size > BLOCK else size
    if csize != expected:
        chunk = zlib.decompress(chunk)
    return chunk[:n], size


LANGS = "ch|cn|de|es|fr|in|in_sdver|it|jp|kr|us|uk"
fam = collections.defaultdict(list)
for p in names:
    if p.lower().endswith(".bin"):
        folded = re.sub(r"/(%s)/" % LANGS, "/<lang>/", p.lower())
        d, b = folded.rsplit("/", 1)
        fam[(d, re.sub(r"\d+", "#", b))].append(p)

SEP = re.escape("\\") + "|/"


def named(base):
    parts = [re.escape(x) for x in base.split("#")]
    ascii_rx = "(?:" + SEP + ")" + r"\d+".join(parts)
    if re.search(ascii_rx.encode("latin1"), exe, re.I):
        return True
    wide_parts = []
    for x in base.split("#"):
        wide_parts.append("".join(re.escape(c) + "\x00" for c in x))
    wide_rx = "(?:" + re.escape("\\") + "|/)\x00" + r"(?:\d\x00)+".join(wide_parts)
    return re.search(wide_rx.encode("latin1"), exe, re.I) is not None


print("control: .bin families:", len(fam), "; files:", sum(len(v) for v in fam.values()))
for ctl in ("battle_message.bin", "menumap_sub#.bin", "npcdic.bin", "musicctrl.bin"):
    print("control named:", ctl, named(ctl))
missing = [(k, v) for k, v in sorted(fam.items()) if not named(k[1])]
print("families whose file name follows no path separator in the executable (ASCII or UTF-16LE):", len(missing), "; files:", sum(len(v) for k, v in missing))
for (d, b), ps in missing:
    info = []
    for p in sorted(ps):
        h, sz = head(p)
        lang = [seg for seg in p.lower().split("/") if re.fullmatch(LANGS, seg)]
        info.append("%s %d %s" % (lang[0] if lang else "-", sz, h.hex()))
    named_siblings = sum(1 for (d2, b2), v in fam.items() if d2 == d and named(b2))
    print("  %s/%s: %d file(s); named families in the same directory: %d; %s" % (d, b, len(ps), named_siblings, "; ".join(info)))
