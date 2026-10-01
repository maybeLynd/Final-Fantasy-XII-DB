"""rc26_fonts.py - RC-26 (.btm texel packing), RC-27 (which file supplies the font_stf glyph tables), RC-28 (glyphs per
font_stf face against the 1,237 kerning pairs). ORACLE, 2026-09-30. Static: shipping image + FFXII_TZA.vbf.

Code facts asserted from the image (C1):
  00365810(n, flag): id = 00D10C98[n-1] (12 ids {130..135, 218..223}); buffer -> [022CBE00] + 0x110 + (n-1)*8.
  Its only caller is the staff-roll setup 0053EB90: a loop n = 7..12 (0053EC90-0053ECA4). So ids 130..135 are never
  requested.
  003643A0 (completion of the fontpack_fs.bin request 003658F0, kind 7 id 0xD2): [022CBE00]+8 = pack + dword[pack+0],
  then 00366080 walks that header: word count of tables, table 0 at +4, table k+1 = table k + dword[table k]; each
  table pointer -> [022CBE00] + 0x10 + k*8. It also fills pixel slots 0/2/3/4 from pack dwords 2/4/5/6 when empty.
  00364210(code, font): searches table [022CBE00+0x10+font*8] (count at +4, 12-byte records at +0x10) and takes the
  cell at [022CBE00+0x110+font*8] + record.pixelOffset (+8); rounds the cell width/height up to 8/16/32/64/128.
Data (C2..C4):
  kind-7 rows for ids 130..135, 218..223 and 0xD2 in all 13 region arrays (ResourcePath_Init replay of
  ../rc6-console-map-codes-0930/rc5_paths.py);
  every fontpack_fs.bin: its tables; for tables 6..11 the extent of the last cell at 4 bits and at 8 bits per texel
  (pow2-rounded cell) against the size of the .btm its region's row names;
  the d3d11 font_stf_{a,as,b,bs,c,cs}.dat glyph records (0x28 header, 0x24 records {key, utf8, ...,
  kernCp at +0x20}) and .ker pairs {first, second, adjust}.
"""
import collections, contextlib, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-as7-pages-0930"))
import arc  # noqa: E402
img = arc.img
sys.path.insert(0, os.path.join(HERE, "..", "rc6-console-map-codes-0930"))
with contextlib.redirect_stdout(io.StringIO()):
    import rc5_paths as R  # noqa: E402
FAILS = []


def check(ok, name):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def ops(f, n=None):
    ins = img.fn_ins(f) if n is None else img.dis(f, n)
    return {x.address: (x.mnemonic, x.op_str) for x in ins}


# ---- C1 code facts ----
ids = list(struct.unpack("<12i", img.rd(0x00D10C98, 48)))
a = ops(0x00365810)
b = ops(0x0053EB90)
c = ops(0x00364210)
p = ops(0x003643A0)
q = ops(0x00366080, 0x8A)
check(ids == [130, 131, 132, 133, 134, 135, 218, 219, 220, 221, 222, 223]
      and a.get(0x00365856) == ("movsxd", "rbp, dword ptr [rax + rdi*4]")
      and a.get(0x003658B5) == ("mov", "qword ptr [rax + rdi*8 + 0x110], r8"),
      "C1a 00365810: id = 00D10C98[n-1] = %s; buffer to +0x110 + (n-1)*8" % ids)
callers = [(ad, img.owner(ad)) for ad, k in img.calls_to(0x00365810)]
check(callers == [(0x0053EC9A, 0x0053EB90)] and b.get(0x0053EC92) == ("lea", "ecx, [rbx + 7]")
      and b.get(0x0053EC9F) == ("inc", "ebx") and b.get(0x0053ECA1) == ("cmp", "ebx, 6") and b.get(0x0053EC90) == ("xor", "ebx, ebx"),
      "C1b the only call of 00365810 is 0053EC9A in the loop n = 7..12 (0053EB90); ids 130..135 (n = 1..6) are never requested")
check(c.get(0x00364276) == ("mov", "rax, qword ptr [r11 + rbx*8 + 0x10]") and c.get(0x0036427B) == ("mov", "rdi, rbx")
      and c.get(0x00364346) == ("mov", "rdx, qword ptr [r11 + rdi*8 + 0x110]") and c.get(0x00364353) == ("mov", "eax, dword ptr [rcx + 8]"),
      "C1c 00364210 pairs glyph table +0x10+font*8 with pixel sheet +0x110+font*8 and adds record +8 (pixelOffset)")
check(p.get(0x003643BC) == ("mov", "qword ptr [r11 + 8], rax") and p.get(0x003643CD) == ("call", "0x366080")
      and q.get(0x003660A6) == ("mov", "qword ptr [r10 + 0x10], rdx") and q.get(0x003660E3) == ("mov", "qword ptr [rax - 8], r8"),
      "C1d 003643A0 sets +8 = pack + dword[pack]; 00366080 fixes table k into +0x10 + 8k")
dd = ops(0x003658F0)
check(dd.get(0x00365926) == ("mov", "edx, 0xd2") and dd.get(0x00365957) == ("mov", "qword ptr [r8], rax"),
      "C1e 003658F0 requests kind 7 id 0xD2 into [022CBE00]")

# ---- C2 kind-7 rows ----
rows = {}
for reg in range(13):
    arr = R.regions[reg][0].get(7)
    rows[reg] = {i: (R.row(arr, i) if arr else None) for i in list(range(130, 136)) + list(range(218, 224)) + [0xD2]}
empty = all(rows[r][i] is None for r in rows for i in range(130, 136))
check(empty, "C2 ids 130..135 name no path in any of the 13 region arrays")
print("    id 0xD2 per region: %s" % {r: (rows[r][0xD2] or "-").split("\\")[-3] for r in rows})
btm_dir = {r: sorted(set((rows[r][i] or "-").split("\\")[-2] + "/" + (rows[r][i] or "-").split("\\")[-3] for i in range(218, 224))) for r in rows}
print("    ids 218..223 per region: %s" % {r: v for r, v in btm_dir.items()})


# ---- C3 fontpack tables against the .btm sheets ----
def p2(v):
    r = 8
    while r < v:
        r *= 2
    return min(r, 128)


def tables(d):
    h = struct.unpack("<I", d[:4])[0]
    n = struct.unpack("<h", d[h:h + 2])[0]
    t, out = h + 4, []
    for k in range(n):
        nxt, cnt = struct.unpack("<ii", d[t:t + 8])
        recs = [struct.unpack("<HBBBBBBI", d[t + 16 + 12 * j:t + 28 + 12 * j]) for j in range(cnt)]
        out.append(recs)
        t += nxt
    return out


btm = {}
for n in arc.find(".btm"):
    btm[n.lower()] = len(arc.get(n))
exact4 = exact8 = over = 0
print("\n  pack (region dir)  table  glyphs  extent@4bpp  extent@8bpp  sheet  sheet bytes")
for lang in sorted(set(n.split("/")[-3] for n in arc.find("packfiles/fontpack_fs.bin"))):
    d = arc.get("ps2data/image/ff12/myoshiok/%s/packfiles/fontpack_fs.bin" % lang)
    T = tables(d)
    for k in range(6, 12):
        recs = T[k]
        e4 = max(r[7] + p2(r[1]) * p2(r[2]) // 2 for r in recs)
        e8 = max(r[7] + p2(r[1]) * p2(r[2]) for r in recs)
        sheet = ["font_stf_a_normal", "font_stf_a_shadow", "font_stf_b_normal", "font_stf_b_shadow", "font_stfc_normal",
                 "font_stf_c_shadow"][k - 6]
        size = btm["ps2data/image/ff12/myoshiok/in/exfont/%s.btm" % sheet]
        exact4 += e4 == size
        exact8 += e8 == size
        over += e4 > size
        print("  %-4s %6d %7d %12d %12d  %-18s %6d%s" % (lang, k, len(recs), e4, e8, sheet, size,
                                                      "   4bpp exact" if e4 == size else ("   OVERRUNS the sheet by %d" % (e4 - size) if e4 > size else "")))
langs = sorted(set(n.split("/")[-3] for n in arc.find("packfiles/fontpack_fs.bin")))
# which glyphs of the 127-glyph tables lie past the 'in' sheet, and do their first 78 match the 78-glyph tables
din, dus = tables(arc.get("ps2data/image/ff12/myoshiok/in/packfiles/fontpack_fs.bin")),     tables(arc.get("ps2data/image/ff12/myoshiok/us/packfiles/fontpack_fs.bin"))
for k, sheet in ((8, "font_stf_b_normal"), (10, "font_stfc_normal")):
    size = btm["ps2data/image/ff12/myoshiok/in/exfont/%s.btm" % sheet]
    past = [r for r in dus[k] if r[7] + p2(r[1]) * p2(r[2]) // 2 > size]
    same = sum(1 for r in dus[k] if r in din[k])
    print("  us table %d: %d of %d glyphs end past the %d-byte sheet (codes %s); %d of its records equal an 'in' table-%d record; "
          "codes only in 'us': %s" % (k, len(past), len(dus[k]), size, "".join(chr(r[0]) for r in past), same, k,
                                     "".join(sorted(chr(r[0]) for r in dus[k] if r[0] not in set(x[0] for x in din[k])))))
check(exact8 == 0 and exact4 >= 6, "C3 4-bit cells: the last cell ends exactly at the sheet's end in %d of %d (table, pack) pairs; "
      "at 8 bits never (%d)" % (exact4, 6 * len(langs), exact8))

# ---- C4 the d3d11 font_stf faces and their .ker ----
print("\n  d3d11 face  glyphs(header+4)  records  kerned cps  ker pairs  pairs with both cps kerned  pairs with both cps present")
for lang in ("us", "jp"):
    for face in ("a", "as", "b", "bs", "c", "cs"):
        base = "gamedata/d3d11/artdata/font/%s/font_stf_%s" % (lang, face)
        d = arc.get(base + ".dat")
        cap = struct.unpack("<I", d[4:8])[0]
        n = (len(d) - 0x28) // 0x24
        recs = [struct.unpack("<9i", d[0x28 + 0x24 * j:0x4C + 0x24 * j]) for j in range(n)]
        present = set()
        for r in recs:
            u = r[1] & 0xFFFFFFFF
            bts = u.to_bytes(4, "little").rstrip(b"\0")
            try:
                present.add(ord(bts.decode("utf-8")))
            except Exception:
                pass
        kerned = set(r[8] for r in recs if r[8] != -1)
        k = arc.get(base + ".ker")
        pairs = [struct.unpack("<iii", k[12 * j:12 * j + 12]) for j in range(len(k) // 12)]
        both_k = sum(1 for f, s, _a in pairs if f in kerned and s in kerned)
        both_p = sum(1 for f, s, _a in pairs if f in present and s in present)
        print("  %s/%-3s %8d %8d %8d %8d %8d %8d" % (lang, face, cap, n, len(kerned), len(pairs), both_k, both_p))
print("\nFAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
