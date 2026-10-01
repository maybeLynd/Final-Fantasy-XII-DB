"""sd182_nav_transform_pair.py - SD-182: is a nav shape subrecord's +0x10 / +0x50 transform pair authored data, or built
at load or per query? (SWE2-ORACLE, 2026-09-30)

Evidence classes, printed with their tag:
  S*  static  decoded instructions / image data of the certified FFXII_TZA.exe (img.py, capstone)
  D*  data    the shipped map packs in FFXII_TZA.vbf: every .mpk's slot-8 YM00 section (the map-ctrl pack page; the
              chunk walk is gen_ym00_census.py's, proved there against 002F6AB0), its nav chunks (tags 0x1F and 0x11),
              their type-4 sub-chunk = the subrecord array the nav table's +0x18 points at
Nothing here is executed and nothing is observed at run time.
Run: python sd182_nav_transform_pair.py > sd182_nav_transform_pair.out
"""
import collections, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))                   # Database/FFXII TZA
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DB, "03-World-Area-Field", "Map-Pack", "members"))
sys.path.insert(0, os.path.abspath(os.path.join(DB, "..", "..", "agent_flow", "tools")))
import img  # noqa: E402
import numpy as np  # noqa: E402
import vbfextract  # noqa: E402
import gen_ym00_census as Y  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_REG  # noqa: E402

VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
FAILS = []
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]


def check(tag, ok, msg):
    print("%s  %-4s %s" % ("PASS" if ok else "FAIL", tag, msg))
    if not ok:
        FAILS.append(tag)


def txt(a):
    x = img.dis(a, 16)[0]
    return ("%s %s" % (x.mnemonic, x.op_str)).strip()


def jt(base_rva, n):
    return [0x00120000 + struct.unpack("<i", img.rd(0x00120000 + base_rva + 4 * t, 4))[0] for t in range(n)]


# ============================================================== static: where the nav table's +0x18 points
check("S1", txt(0x0026E50C) == "mov eax, 0x3a8" and txt(0x0026E511) == "mov edx, 0x3b0" and txt(0x0026E516) == "lea rcx, [rip + 0x1e2bdb3]"
      and txt(0x0032223C) == "mov qword ptr [rip + 0x2b9f135], rax" and txt(0x00322259) == "mov qword ptr [rip + 0x2b9f118], rax",
      "0026E500(n) returns q[0209A678] (n == 0) or q[0209A680] (n != 0); 00322220 stores 0026E500(2), else 0026E500(1/0), "
      "at 02EC1378 = the `tab` of the nav walks")
check("S2", txt(0x0026E966) == "mov qword ptr [rip + 0x1e2bd03], rcx" and txt(0x0026E9C0) == "imul r8, rdx, 0x68"
      and txt(0x0026E9C4) == "add r8, 0x40" and txt(0x0026E9F1) == "mov qword ptr [r10 + rdx*8], r8" and txt(0x0026E7B1) == "call 0x2f6ab0"
      and txt(0x0026E7B9) == "call 0x26e960",
      "0026E960 (after 002F6AB0 built the object) stores &obj[0x40 + 0x68 k] at 0209A678 + 8 k for k = 0, 1: tab is one of the "
      "object's two 0x68-byte nav tables")
T = jt(0x1D72F8, 0x22)
check("S3", txt(0x002F6C94) == "mov r14d, ecx" and txt(0x002F6CA1) == "shl r14, 4" and txt(0x002F6CA7) == "add r14, rbx"
      and txt(0x002F6C69) == "add rbx, 0x10" and T[0x1F] == 0x002F6DB7 and T[0x11] == 0x002F6DC8
      and txt(0x002F6DB7) == "mov rdx, r14" and txt(0x002F6DBA) == "lea rcx, [rsi + 0x40]" and txt(0x002F6DBE) == "call 0x232380"
      and txt(0x002F6DC8) == "lea rcx, [rsi + 0xa8]" and txt(0x002F6DD2) == "call 0x232380",
      "002F6AB0 walks the YM00 index (chunk = file + 0x10 + off * 16); tag 0x1F -> 00232380(obj + 0x40, chunk), "
      "tag 0x11 -> 00232380(obj + 0xA8, chunk)")
T2 = jt(0x112470, 6)
stores = [x for x in img.fn_ins(0x00232380) if x.operands and x.operands[0].type == X86_OP_MEM and not x.mnemonic.startswith(("cmp", "test", "nop"))]
check("S4", T2[4] == 0x0023242F and txt(0x00232432) == "add r8, 0x10" and txt(0x00232436) == "mov qword ptr [r9 + 0x18], r8"
      and txt(0x0023243A) == "mov dword ptr [r9 + 0x44], eax" and txt(0x002323C0) == "shl r8, 4" and txt(0x002323C4) == "add r8, rbx"
      and all(x.reg_name(x.operands[0].mem.base) in ("r9", "rsp") for x in stores),
      "00232380 walks the nav chunk's own index (sub-chunk = chunk + off * 16) and for sub-type 4 stores tab+0x18 = "
      "sub-chunk + 0x10 and tab+0x44 = its first dword (the count); its %d stores all go to the table (r9) or the stack: "
      "the subrecords are the file's bytes, rebased by pointer, not copied" % len(stores))
check("S5", txt(0x0022D54C) == "lea r10, [rax + rax*8]" and txt(0x0022D550) == "shl r10, 4" and txt(0x0022D554) == "add r10, qword ptr [r15 + 0x18]"
      and txt(0x00381ED0) == "lea rdx, [rcx + 0x50]" and txt(0x00380FC0) == "add rdx, 0x50" and txt(0x0038103E) == "lea rdx, [r14 + 0x10]",
      "the walks index a subrecord as q[tab+0x18] + (si - 0x4000) * 144 (D4B0); EB0 and FA0 transform through +0x50 "
      "(to the unit frame) and FA0 maps back through +0x10")
# every function that forms a 144-byte subrecord pointer from +0x18, and whether it ever stores through that register
sites = []
for r in sorted(img.ROOTS):
    try:
        ins = img.fn_ins(r)
    except Exception:
        continue
    for k, x in enumerate(ins[:-2]):
        if x.mnemonic == "lea" and "*8]" in x.op_str and ins[k + 1].mnemonic == "shl" and ins[k + 1].op_str.endswith(", 4") \
                and ins[k + 2].mnemonic == "add" and ins[k + 2].op_str.endswith("+ 0x18]"):
            reg = ins[k + 2].reg_name(ins[k + 2].operands[0].reg)
            st = [y.address for y in ins if y.operands and y.operands[0].type == X86_OP_MEM and y.operands[0].mem.base
                  and y.reg_name(y.operands[0].mem.base) == reg and not y.mnemonic.startswith(("cmp", "test", "prefetch"))]
            sites.append((r, x.address, reg, st))
check("S6", [s[0] for s in sites] == [0x0022CC50, 0x0022D4B0, 0x0022D7E0, 0x0022DE60, 0x0022F8B0] and all(not s[3] for s in sites),
      "the 144-byte index is formed in exactly %s; none stores through its subrecord register"
      % ", ".join("%08X (%s at %08X)" % (s[0], s[2], s[1]) for s in sites))
fa0 = [x for x in img.fn_ins(0x00380FA0) if x.operands and x.operands[0].type == X86_OP_MEM and x.reg_name(x.operands[0].mem.base) == "r14"
       and not x.mnemonic.startswith(("cmp", "test"))]
eb0 = [x for x in img.fn_ins(0x00381EB0) if x.operands and x.operands[0].type == X86_OP_MEM and x.reg_name(x.operands[0].mem.base) not in ("rsp", "rbp")
       and not x.mnemonic.startswith(("cmp", "test"))]
check("S7", txt(0x00380FC0) == "add rdx, 0x50" and not fa0 and not eb0,
      "FA0 (the shape in r14) and EB0 (the shape in rcx/rbx) never store through the shape pointer: the pair is read only")

# ============================================================== data: the shipped subrecords
f = open(VBF, "rb")
names, blocks = vbfextract.load_index(f)
packs = sorted(n for n in names if n.lower().endswith(".mpk"))
stat = collections.Counter()
worst = collections.defaultdict(float)
types = collections.Counter()
ident = collections.Counter()
neg_hits = neg_total = 0
per = {}
prev_M = prev_N = None
for p in packs:
    b = Y.slot9(vbfextract.read_entry(f, names, blocks, p), 8)
    if b is None or b[:4] != b"YM00":
        continue
    stat["ym00"] += 1
    n = U32(b, 0x10)
    ents = [U32(b, 0x14 + 4 * i) for i in range(n + 1)]
    for i, e in enumerate(ents[:-1]):
        tag = e >> 24
        if tag not in (0x1F, 0x11):
            continue
        ch = 0x10 + (e & 0xFFFFFF) * 16
        if (ents[i + 1] & 0xFFFFFF) == (e & 0xFFFFFF):        # 002F6CB5-002F6CB7: a zero-size chunk is skipped
            stat["empty_navchunk_%02X" % tag] += 1
            continue
        sub = [U32(b, ch + 4 + 4 * j) for j in range(U32(b, ch))]
        four = [s for s in sub if s >> 24 == 4]
        stat["navchunk_%02X" % tag] += 1
        if len(four) != 1:
            stat["navchunk_without_one_type4"] += 1
            continue
        sc = ch + (four[0] & 0xFFFFFF) * 16
        cnt = U32(b, sc)
        stat["subrecords_%02X" % tag] += cnt
        for k in range(cnt):
            rec = sc + 0x10 + 144 * k
            if rec + 144 > len(b):
                stat["overrun"] += 1
                break
            typ = U32(b, rec)
            types[(tag, typ)] += 1
            M = np.frombuffer(b[rec + 0x10:rec + 0x50], "<f4").reshape(4, 4).astype(np.float64)
            N = np.frombuffer(b[rec + 0x50:rec + 0x90], "<f4").reshape(4, 4).astype(np.float64)
            isid = np.array_equal(M, np.eye(4)) and np.array_equal(N, np.eye(4))
            ident[(tag, isid)] += 1
            err = float(np.abs(M @ N - np.eye(4)).max())
            # float32 rounding scale of the product: unit roundoff 2^-24 times the largest |M| |N| term sum
            scale = float((np.abs(M) @ np.abs(N)).max()) * 2.0 ** -24
            ratio = err / scale if scale else 0.0
            worst[tag] = max(worst[tag], err)
            worst["ratio_%02X" % tag] = max(worst["ratio_%02X" % tag], ratio)
            stat["inverse_ok_%02X" % tag] += ratio < 64
            stat["affine_%02X" % tag] += bool(np.allclose(M[:, 3], [0, 0, 0, 1]) and np.allclose(N[:, 3], [0, 0, 0, 1]))
            if prev_N is not None and not isid and float(np.abs(prev_M - M).max()) > 1e-2:
                neg_total += 1
                s2 = float((np.abs(M) @ np.abs(prev_N)).max()) * 2.0 ** -24
                neg_hits += float(np.abs(M @ prev_N - np.eye(4)).max()) / s2 < 64
            if not isid:
                prev_M, prev_N = M, N
            key = (p, "%02X" % tag)
            agg = per.setdefault(key, [0, collections.Counter(), 0.0, 0, 0])
            agg[0] += 1
            agg[1][typ] += 1
            agg[2] = max(agg[2], ratio)
            agg[3] += isid
            agg[4] += ratio < 64
with open(os.path.join(HERE, "sd182-subrecord-pairs.tsv"), "w", encoding="utf-8", newline="\n") as t:
    t.write("pack\tnav_tag\tsubrecords\ttype0_sphere\ttype1_cylinder\ttype2_box\tinverse_ok\tidentity_pairs\t"
            "worst_error_in_float32_roundings\n")
    for (pk, tg), a in sorted(per.items()):
        t.write("%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%.2f\n" % (pk, tg, a[0], a[1][0], a[1][1], a[1][2], a[4], a[3], a[2]))
print("empty (zero-size, skipped by 002F6AB0) nav chunks: tag 1F %d, tag 11 %d" % (stat["empty_navchunk_1F"], stat["empty_navchunk_11"]))
print("corpus: %d YM00 sections; non-empty nav chunks tag 1F %d, tag 11 %d; subrecords tag 1F %d, tag 11 %d; overruns %d; chunks without one "
      "type-4 sub-chunk %d" % (stat["ym00"], stat["navchunk_1F"], stat["navchunk_11"], stat["subrecords_1F"], stat["subrecords_11"],
                               stat["overrun"], stat["navchunk_without_one_type4"]))
print("types: " + ", ".join("tag %02X type %d: %d" % (k[0], k[1], v) for k, v in sorted(types.items())))
print("identity pairs: " + ", ".join("tag %02X %s: %d" % (k[0], "identity" if k[1] else "non-identity", v) for k, v in sorted(ident.items())))
total = stat["subrecords_1F"] + stat["subrecords_11"]
okn = stat["inverse_ok_1F"] + stat["inverse_ok_11"]
check("D1", stat["ym00"] == 461 and stat["navchunk_1F"] + stat["empty_navchunk_1F"] == 461
      and stat["navchunk_11"] + stat["empty_navchunk_11"] == 461 and not stat["overrun"] and not stat["navchunk_without_one_type4"] and total > 0
      and txt(0x002F6CB5) == "sub edx, eax" and txt(0x002F6CB7) == "je 0x2f6f19",
      "every shipped YM00 section (461) indexes both nav chunks; %d / %d are zero-size (skipped by the loader); every "
      "non-empty one has exactly one type-4 sub-chunk; %d subrecords in all"
      % (stat["empty_navchunk_1F"], stat["empty_navchunk_11"], total))
check("D2", okn == total,
      "in the file bytes, +0x50 is the inverse of +0x10 for %d of %d subrecords: |M10 M50 - I| stays under 64 float32 "
      "roundings of the product (worst %.1f for tag 1F, %.1f for tag 11; absolute %.2e / %.2e): the pair is authored"
      % (okn, total, worst["ratio_1F"], worst["ratio_11"], worst[0x1F], worst[0x11]))
check("D3", sorted(set(t for _, t in types)) <= [0, 1, 2] and stat["affine_1F"] + stat["affine_11"] == total,
      "the type dword is 0 / 1 / 2 (sphere / cylinder / box) and both matrices are affine (last column 0, 0, 0, 1) in every subrecord")
check("D4", neg_total > 1000 and neg_hits == 0,
      "negative control: pairing each non-identity forward matrix with the inverse of the previous record whose forward "
      "matrix differs by more than 0.01 passes the same test "
      "(%d of %d), so the test discriminates" % (neg_hits, neg_total))
print("FAILS %d" % len(FAILS))
