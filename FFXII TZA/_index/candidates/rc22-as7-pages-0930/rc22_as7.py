"""rc22_as7.py - RC-22..RC-25: the .as7 page subformat, the tailOff block, the offsets[] walker and char_silhouette's
page use. ORACLE, 2026-09-30. Static: shipping image + the 18 shipped .as7 files read from FFXII_TZA.vbf.

Code facts are read from the image and asserted (each is a control: if the bytes differ, the script fails):
  W  0024AA00(file, dst, first, n)  the ONLY walker: count = file[2]*256+file[3] (0024AA0A-0024AA2A), rejects
     first >= count (0024AA2E), n = 0 or n > count -> n = count (0024AA4E-0024AA5A), dict = file + be32(file+4)
     (tailOff, 0024AA5E-0024AA97), resets the output cursor 02091090 = 0 and the output base 02090788 = dst, then for
     each page p: payload = file + be32(file + 8 + 4p) (0024AAC0-0024AAF1), 00248500(payload, dict).
  D  00248500(payload, dict)  dict[0] = mode, dict[1] = b; modes 0 and 3 decode, 1 and 2 return 0 (0024855D-00248564);
     mode <= 2 takes the output length from be16(dict+2) and the dictionary body starts at dict+4; mode 3 takes it
     from be16(payload) (payload += 2) and the body starts at dict+2. Tokens: c >= 0x80 -> copy (c & 0x7F) + 1
     literal bytes; else len = ((2c) >> (8 - b)) + 3, off = (c*256 + next) & (0xFFFF >> (b + 1)), copy len bytes
     from body[off..] (the source index is not re-masked). Stop when the page's output count reaches the length.
The script re-implements W+D and decodes every page of every file. Controls:
  C1  every page's token stream ends exactly at the next payload offset (tailOff for the last) - the decoder is right
      and the payloads carry nothing else;
  C2  item_gra pages decode to 6,144 bytes = the 64 x 96 of 01E0C470 / 01E0C474 that 00292390 copies one byte per
      texel; char_silhouette pages to 1,024 bytes, and 0x102 of them = the 0x40800 buffers 002CEFD0 allocates;
  C3  the code facts above (bytes of the image);
  C4  callers: 0024AA00 is called only at 00292768, 002CF2B4, 002CF2CE; 00248500 only from 0024AAF4; no data qword
      holds either address.
"""
import collections, struct, sys
import arc
img = arc.img
FAILS = []


def check(ok, name):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def be16(b, o):
    return struct.unpack(">H", b[o:o + 2])[0]


def be32(b, o):
    return struct.unpack(">I", b[o:o + 4])[0]


def decode_page(f, poff, tail):
    """00248500 on file f, payload at poff, dict at tail. Returns (out bytes, payload bytes consumed, dict refs)."""
    mode, bits = f[tail], f[tail + 1]
    body = tail + 2
    if mode <= 2:
        outlen = be16(f, body); body += 2
    if mode not in (0, 3):
        return None, 0, []
    p = poff
    if mode == 3:
        outlen = be16(f, p); p += 2
    mask = 0xFFFF >> (bits + 1)
    out = bytearray()
    refs = []
    while len(out) < outlen:
        c = f[p]
        if c & 0x80:
            n = (c & 0x7F) + 1
            out += f[p + 1:p + 1 + n]
            p += 1 + n
        else:
            n = ((2 * c) >> (8 - bits)) + 3
            off = ((c << 8) + f[p + 1]) & mask
            refs.append((off, n))
            for k in range(n):
                out.append(f[body + ((off + k) & 0xFFFF)])
            p += 2
    return bytes(out), p - poff, refs


# ---------- C3: the code facts ----------
w = {x.address: (x.mnemonic, x.op_str) for x in img.fn_ins(0x0024AA00)}
d = {x.address: (x.mnemonic, x.op_str) for x in img.fn_ins(0x00248500)}
check(w.get(0x0024AA0A) == ("movzx", "r10d, byte ptr [rcx + 2]") and w.get(0x0024AA26) == ("movzx", "eax, byte ptr [rdi + 3]")
      and w.get(0x0024AA2E) == ("cmp", "bx, r10w"), "C3a 0024AA00 reads count = file[2]*256 + file[3] and rejects first >= count")
check(all(w.get(a, ("",))[1].startswith("eax, byte ptr [rdi + %d]" % k) or w.get(a, ("",))[1] == "ebp, byte ptr [rdi + 4]"
          for a, k in ((0x0024AA5E, 5), (0x0024AA62, 4), (0x0024AA70, 6), (0x0024AA7F, 7)))
      and w.get(0x0024AA97) == ("add", "rbp, rdi"), "C3b 0024AA00 builds dict = file + be32(file+4), the tailOff")
check(w.get(0x0024AAC3) == ("movzx", "ecx, byte ptr [rdi + rax*4 + 8]") and w.get(0x0024AAF1) == ("add", "rcx, rdi")
      and w.get(0x0024AAF4) == ("call", "0x248500"), "C3c 0024AA00 walks offsets[] as be32 at file+8+4p and calls 00248500")
check(d.get(0x0024855D) == ("test", "dl, dl") and d.get(0x00248561) == ("cmp", "dl, 3")
      and d.get(0x002485B6) == ("jns", "0x2485fd") and d.get(0x002485B8) == ("and", "cl, 0x7f"),
      "C3d 00248500: modes 0/3 only; literal run when c & 0x80")
dims = struct.unpack("<ii", img.rd(0x01E0C470, 8))
sil_tab = list(struct.unpack("<4i", img.rd(0x00917160, 16))) + [4, 5]
s = {x.address: (x.mnemonic, x.op_str) for x in img.fn_ins(0x002CEFD0)}
check(s.get(0x002CEFF7) == ("mov", "dword ptr [rsp + 0x40], 4") and s.get(0x002CEFFF) == ("mov", "dword ptr [rsp + 0x44], 5")
      and s.get(0x002CF249) == ("imul", "ebp, dword ptr [rsp + rax*4 + 0x30], 0x204")
      and s.get(0x002CF2A0) == ("mov", "r14d, 0x102") and s.get(0x002CF25A) == ("mov", "edx, 0x40800")
      and s.get(0x002CF2C0) == ("lea", "r8d, [r14 + rbp]"),
      "C3e 002CEFD0: first page = 0x204 * T[ch] with T = 00917160[0..3] + {4, 5}; two walks of 0x102 pages into 0x40800 buffers")
print("    T = %s ; 01E0C470/01E0C474 = %s" % (sil_tab, dims))
st = {x.address: (x.mnemonic, x.op_str) for x in img.dis(0x002CEE00, 0x50)}
check(st.get(0x002CEE1A) == ("mov", "byte ptr [r8 + 0x10d], cl") and st.get(0x002CEE21) == ("cmp", "ecx, 5")
      and st.get(0x002CEE45) == ("and", "dl, 0xfd"),
      "C3f the .pdata-less setter 002CEE00(id, flags) stores ch = id at +0x10D and clears the decode request (bit 1) for id > 5 unsigned")

# ---------- C4: callers ----------
def callers(t):
    return sorted((a, k) for a, k in img.calls_to(t))
cw, cd, cs = callers(0x0024AA00), callers(0x00248500), callers(0x002CEE00)
dq = [va for name, start, size, raw, rawsz in img.SECS if name in (".data", ".rdata")
      for va in range(start, start + rawsz - 7, 8)
      if struct.unpack("<Q", img.blob[raw + va - start:raw + va - start + 8])[0] in (0x0024AA00, 0x00248500, 0x002CEE00)]
check([a for a, _ in cw] == [0x00292768, 0x002CF2B4, 0x002CF2CE] and [a for a, _ in cd] == [0x0024AAF4] and not dq,
      "C4 walker call sites %s, decoder %s, data refs %d" % (["%08X" % a for a, _ in cw], ["%08X" % a for a, _ in cd], len(dq)))
print("    setter 002CEE00 call sites: %s" % ["%08X (%s, in %08X)" % (a, k, img.owner(a) or 0) for a, k in cs])

# ---------- the files ----------
files = sorted(arc.find(".as7"))
digests = {}
mism = []
summary = collections.OrderedDict()
for path in files:
    f = arc.get(path)
    n, tail = be16(f, 2), be32(f, 4)
    offs = [be32(f, 8 + 4 * i) for i in range(n)] + [tail]
    mode, bits = f[tail], f[tail + 1]
    body = tail + 4 if mode <= 2 else tail + 2
    outs, maxref, lit, cpy = set(), 0, 0, 0
    vals = collections.Counter()
    for p in range(n):
        out, used, refs = decode_page(f, offs[p], tail)
        if out is None or used != offs[p + 1] - offs[p]:
            mism.append((path, p, used, offs[p + 1] - offs[p]))
            continue
        outs.add(len(out))
        vals.update(out)
        for o, k in refs:
            maxref = max(maxref, o + k)
    key = path.split("/")[-1]
    h = hash(f)
    dup = digests.get(h)
    digests.setdefault(h, path)
    summary[path] = (key, n, len(f), tail, mode, bits, be16(f, tail + 2) if mode <= 2 else None, len(f) - body,
                     sorted(outs), maxref, min(vals) if vals else None, max(vals) if vals else None, dup)
check(not mism, "C1 every page of all %d files decodes and ends exactly at the next offset (mismatches: %s)" % (len(files), mism[:5]))
item = [v for k, v in summary.items() if "item_gra" in k]
sil = [v for k, v in summary.items() if "char_silhouette" in k]
odd = sorted(set(v[0] for v in item if v[8] != [dims[0] * dims[1]]))
check(odd == ["item_gra07.as7"] and all(v[8] == [1024] for v in sil) and 0x102 * 1024 == 0x40800,
      "C2 item_gra00..06 pages = %d x %d = %d bytes (item_gra07 is the one exception: %s); char_silhouette pages = 1,024 "
      "bytes; 0x102 x 1,024 = 0x40800" % (dims[0], dims[1], dims[0] * dims[1], [v[8] for v in item if v[0] == "item_gra07.as7"][0]))

print("\nfile  count  size  tailOff  tail: mode bits outlen  dict-body-bytes  page-bytes  max-dict-extent-used  texel-min..max")
for path, v in summary.items():
    print("  %-40s %5d %8d %8X  %d %d %5s  %5d  %s  %5d  %s..%s%s" % (path.split("myoshiok/")[-1], v[1], v[2], v[3], v[4], v[5],
          v[6], v[7], v[8], v[9], v[10], v[11], ("  (= %s)" % v[12].split("myoshiok/")[-1]) if v[12] else ""))

# ---------- RC-25: which char_silhouette pages any path indexes ----------
cnt = be16(arc.get([p for p in files if "char_silhouette" in p][0]), 2)
covered = collections.Counter()
per_id = {}
for ch in range(6):
    base = 0x204 * sil_tab[ch]
    pages = list(range(base, base + 0x102)) + list(range(base + 0x102, base + 0x204))
    per_id[ch] = (base, base + 0x203)
    covered.update(pages)
print("\nchar_silhouette: count %d; id -> pages %s" % (cnt, {k: "%d..%d" % v for k, v in per_id.items()}))
check(sorted(covered) == list(range(cnt)) and max(covered.values()) == 1,
      "C5 ids 0..5 index disjoint 516-page blocks covering all %d pages exactly once; ids > 5 (and -1) decode none" % cnt)
print("\nFAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
