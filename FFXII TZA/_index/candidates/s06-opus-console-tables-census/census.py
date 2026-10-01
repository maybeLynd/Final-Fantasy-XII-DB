"""S-06 I-6 / I-7 (OPUS, 2026-09-26): the authored-code table re-derived from the SHA-asserted image - a STATIC census, not an
execution. CONTRACT-developer-tuning-console.md files I-5..I-7 as STRUCTURAL (section 16).
 I6  the renderer's read at 001CDBF7 is `mov rax, [rsi + rdx*8 + 0x1CD6E68]` with rsi = the image base: the displacement is an
     RVA, so the table is at 0x1CD6E68 + 0x120000 = 01DF6E68 (in .data); the literal 01CD6E68 is also mapped, which is why
     reading it as an address does not fault.
 I7  the 294 entries (ids 0..293, stride 16): +0x08 == index + 1 for all; 111 code pointers are non-NULL and each points at
     an ASCII string of three letters and four digits; the prefixes occupy contiguous id bands; dst0104 appears twice.
Writes census.json next to this file.
"""
import hashlib, json, os, re, struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG = 0x120000
pe = struct.unpack_from("<I", raw, 0x3C)[0]
n, o = struct.unpack_from("<H", raw, pe + 6)[0], struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + o
for _ in range(n):
    nm = raw[off:off + 8].rstrip(b"\0").decode()
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((nm, va + IMG, vs, ra, rs))
    off += 40
def sec_of(a):
    for nm, v, vs, ra, rs in secs:
        if v <= a < v + max(vs, rs):
            return nm
def rd(a, k):
    for nm, v, vs, ra, rs in secs:
        if v <= a < v + rs:
            return raw[ra + a - v:ra + a - v + k]
ins = next(Cs(CS_ARCH_X86, CS_MODE_64).disasm(rd(0x1CDBF7, 16), 0x1CDBF7))
disp = int(re.search(r"0x([0-9a-f]+)\]", ins.op_str).group(1), 16)
table = disp + IMG
entries, codes = [], {}
for i in range(294):
    p, idx = struct.unpack("<QQ", rd(table + 16 * i, 16))
    s = None
    if p:
        b = rd(p, 16) or b""
        s = b.split(b"\0")[0].decode("latin1")
    entries.append([i, idx == i + 1, "%X" % p if p else None, s])
pop = [e for e in entries if e[2]]
form = all(re.fullmatch(r"[a-z]{3}[0-9]{4}", e[3] or "") for e in pop)
bands, prev = [], None
for e in pop:
    pre = e[3][:3]
    if not bands or bands[-1][0] != pre:
        bands.append([pre, e[0], e[0]])
    else:
        bands[-1][2] = e[0]
from collections import Counter
dup = [k for k, v in Counter(e[3] for e in pop).items() if v > 1]
out = {"instruction": "%08X %s %s" % (ins.address, ins.mnemonic, ins.op_str), "displacement": "%X" % disp, "table": "%X" % table,
       "table_section": sec_of(table), "literal_section": sec_of(disp), "index_plus_1_all": all(e[1] for e in entries),
       "populated": len(pop), "form_3letters_4digits": form, "prefix_bands": bands, "prefixes_contiguous": len(bands) == len({b[0] for b in bands}),
       "duplicates": {d: [e[0] for e in pop if e[3] == d] for d in dup}}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "census.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "prefix_bands"}, indent=1), len(bands))
