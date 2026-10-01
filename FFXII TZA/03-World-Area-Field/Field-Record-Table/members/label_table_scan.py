"""label_table_scan.py: scan every shipped name/label table in FFXII_TZA.vbf
for a string bound to the field-record bit-15 action-permission flag
(UQ-82 / UQ-85, OPUS-REQ-SWE2-DATA-LABEL-TABLES-FOR-TWO-NAS-ROWS).

Reads the SRYK index, pulls the candidate table families, extracts all
printable strings, and reports any string carrying flag/field vocabulary.
Verdict (2026-09-18): NEGATIVE — no shipped table binds a label to bit 15.
Run: python label_table_scan.py [vbf-path]
"""
import re, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..',
                                '..', 'agent_flow', 'tools'))
import vbfextract

VBF = sys.argv[1] if len(sys.argv) > 1 else \
    r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"

FAMILIES = [
    ("us/bin name tables",      r"ps2data/image/ff12/us/bin/"),
    ("us binaryfile text",      r"ps2data/image/ff12/test_battle/us/binaryfile/"),
    ("us menu resource pkgs",   r"ps2data/image/ff12/myoshiok/us/(bin_menu|mrp_menu)/"),
    ("global common",           r"ps2data/image/ff12/common/"),
    ("{ch,in} common",          r"ps2data/image/ff12/(ch|in)/common/"),
    ("script symbol tables",    r"ps2data/image/ff12/(ch|in)/bin/.*\.(dbg|sbn|msb)$"),
    ("file lists / debglobal",  r"ps2data/image/ff12/(ch|in)/bin/filelistlocalin\.bin$|debglobal"),
]

FLAG_VOCAB = re.compile(
    rb'safe|peace|nonbattle|nobattle|no_battle|noncombat|permit|prohibit|forbid'
    rb'|navimap|safearea|safe_area|townflag|maptype|fieldtype|areatype'
    rb'|action_flag|fieldflag|field_flag|flag', re.I)
WORD = re.compile(rb'[a-zA-Z_][a-zA-Z0-9_]{2,}')

f = open(VBF, 'rb')
names, blocks = vbfextract.load_index(f)
print('VBF entries:', len(names))
for fam, pat in FAMILIES:
    hits, nstr = [], 0
    paths = [p for p in names if re.search(pat, p)]
    for p in paths:
        d = vbfextract.read_entry(f, names, blocks, p)
        nstr += len(re.findall(rb'[\x20-\x7e]{4,}', d))
        for m in WORD.finditer(d):
            if FLAG_VOCAB.search(m.group(0)):
                hits.append((p.split('/')[-1], m.group(0).decode()))
    print('%-24s %4d files %6d strings  %d flag-vocab strings'
          % (fam, len(paths), nstr, len(set(hits))))
    for h in sorted(set(hits))[:15]:
        print('     ', h)
