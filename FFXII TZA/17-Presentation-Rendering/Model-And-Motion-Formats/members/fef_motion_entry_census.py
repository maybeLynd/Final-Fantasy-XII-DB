"""@FEF / @FMC / @FMN / @FMW / @FRM entry census — SWE2-DATA, UQ-218 residue.

Runs over every .cm in the archive: entry-tag inventory, @FEF header fields
(0x30 record + embedded EFX0010), and motion-tag presence. Prints checks.

    FF12_VBF=<archive> python fef_motion_entry_census.py
"""
import sys, os, io, struct, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
from census_format_magics import load_index

BLOCK = 0x10000
f = io.open(os.environ["FF12_VBF"], "rb")
names, blocks = load_index(f)

def read_all(p):
    sb, size, off = names[p]
    n = (size + BLOCK - 1) // BLOCK
    out = b""
    f.seek(off)
    for i in range(n):
        cs = blocks[sb + i] or BLOCK
        exp = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        c = f.read(cs)
        if cs != exp:
            c = zlib.decompress(c)
        out += c
    return out

def entries(p):
    d = read_all(p)
    var, clen, cnt = struct.unpack_from("<III", d, 4)
    base = 0x40 if var == 1 else 0x30
    for i in range(cnt):
        o = base + struct.unpack_from("<I", d, base + i * 4)[0]
        yield d[o:o + 4], o, d

tag_counts = collections.Counter()        # .cm tags
fef_files = 0
fef_hdr = collections.Counter()           # (kind, len-ok)
fef_magic_off = collections.Counter()     # offset of embedded EFX0010
fef_field = collections.defaultdict(collections.Counter)
motion = collections.Counter()            # files carrying each motion tag
fmc = {"kind": collections.Counter(), "len": collections.Counter(),
       "name": collections.Counter(),
       "pay": collections.defaultdict(collections.Counter),
       # @FMC payload grammar (executor 0041E000 / init 0041CD30):
       # records at +0x30: {u8 kind, u8, u8, u8 subCount, u16 byteLen};
       # sub-records: {u16 key, u16 {cmdCount:6, byteLen:10}};
       # commands: {u16 {opcode:7, byteLen:9}}.
       "rec_kind": collections.Counter(), "sub_key": collections.Counter(),
       "op": collections.Counter(),
       "walk_bad": 0, "sub_bad": 0, "cmd_bad": 0, "rec1_per_entry": 0}
fmn = {"kind": collections.Counter(), "len": collections.Counter(),
       "name": collections.Counter(), "f60": collections.Counter(),
       "nrec": collections.Counter(), "adv": collections.Counter(),
       "mask_bad": 0, "walk_bad": 0, "ca": 0}
fmw = {"kind": collections.Counter(), "len": collections.Counter(),
       "arm": collections.Counter(), "base": collections.Counter()}
fails = []

for p in names:
    if not p.lower().endswith(".cm"):
        continue
    tags = []
    for tag, off, d in entries(p):
        t = tag.decode("latin-1")
        tag_counts[t] += 1
        tags.append(t)
        kind, elen = struct.unpack_from("<II", d, off + 4)
        if tag == b"@FMC":
            fmc["kind"][kind] += 1
            fmc["len"][elen] += 1
            fmc["name"][d[off + 0x10:off + 0x30].split(b"\0")[0].decode("latin-1", "replace")] += 1
            for fo in range(0x30, min(elen, 0x50), 2):
                fmc["pay"]["+%02x" % fo][struct.unpack_from("<H", d, off + fo)[0]] += 1
            # grammar walk — event records tile [+0x30, +elen) via word[+4]
            rend = off + elen
            ro, ri, rec1 = off + 0x30, 0, 0
            rcount = struct.unpack_from("<I", d, off + 0x0C)[0]
            while ro + 6 <= rend and ri < rcount:
                rkind, subc = d[ro], d[ro + 3]
                rlen = struct.unpack_from("<H", d, ro + 4)[0]
                fmc["rec_kind"][rkind] += 1
                if rkind == 1:
                    rec1 += 1
                if rlen < 6 or ro + rlen > rend:
                    fmc["walk_bad"] += 1
                    break
                so = ro + 6
                for _ in range(subc):
                    if so + 4 > ro + rlen:
                        fmc["sub_bad"] += 1
                        break
                    skey, w2 = struct.unpack_from("<HH", d, so)
                    fmc["sub_key"][skey] += 1
                    ccnt, slen = w2 & 0x3F, w2 >> 6
                    co = so + 4
                    for _ in range(ccnt):
                        if co + 2 > so + slen:
                            fmc["cmd_bad"] += 1
                            break
                        cw = struct.unpack_from("<H", d, co)[0]
                        fmc["op"][cw & 0x7F] += 1
                        cl = cw >> 7
                        if cl == 0:
                            fmc["cmd_bad"] += 1
                            break
                        co += cl
                    if co != so + slen:
                        fmc["cmd_bad"] += 1
                    so += slen
                if so != ro + rlen:
                    fmc["sub_bad"] += 1
                ro += rlen
                ri += 1
            if ro != rend:
                fmc["walk_bad"] += 1
            if rec1 == 1:
                fmc["rec1_per_entry"] += 1
        if tag == b"@FMN":
            fmn["kind"][kind] += 1
            fmn["len"][elen] += 1
            fmn["name"][d[off + 0x10:off + 0x30].split(b"\0")[0].decode("latin-1", "replace")] += 1
            fmn["f60"][struct.unpack_from("<4f", d, off + 0x60)] += 1
            # tail grammar (walker 0041C0xx): u32 +0x0C = record count; kind
            # bits select the +0xF0 tail base (00409190). Records are the
            # 22-byte {u16 nodeKey, u16 {chMask:9, len:6, flag:1}, u16
            # chIdx[9]} — mask bit i set iff chIdx[i] < 0x8000 (else 0x8000|n
            # = absent), advance = len field bytes.
            fmn["nrec"][struct.unpack_from("<I", d, off + 0x0C)[0]] += 1
            ro = off + 0xF0
            for _ri in range(struct.unpack_from("<I", d, off + 0x0C)[0]):
                w2 = struct.unpack_from("<H", d, ro + 2)[0]
                mask, adv = w2 & 0x1FF, (w2 >> 9) & 0x3F
                chans = struct.unpack_from("<9H", d, ro + 4)
                fmn["adv"][adv] += 1
                for ci in range(9):
                    if bool((mask >> ci) & 1) == bool(chans[ci] & 0x8000):
                        fmn["mask_bad"] += 1
                ro += adv
            if ro > off + elen:
                fmn["walk_bad"] += 1
        if tag == b"@FMW":
            fmw["kind"][kind] += 1
            fmw["len"][elen] += 1
            fmw["base"][struct.unpack_from("<I", d, off + 0x30)[0]] += 1
            fmw["arm"][struct.unpack_from("<I", d, off + 0x34)[0]] += 1
        if tag == b"@FEF":
            fef_files += 1
            unk = struct.unpack_from("<I", d, off + 0xC)[0]
            name = d[off + 0x10:off + 0x30].split(b"\0")[0]
            fef_field["kind"][kind] += 1
            fef_field["name==basename"][name.decode("latin-1", "replace") == os.path.splitext(os.path.basename(p))[0]] += 1
            # find embedded EFX0010
            e = d.find(b"EFX0010", off, min(len(d), off + elen))
            fef_magic_off[e - off if e >= 0 else -1] += 1
            for fo in range(0x30, 0x50, 4):
                fef_field["+0x%02X" % fo][struct.unpack_from("<I", d, off + fo)[0]] += 1
    for mt in ("@FMC", "@FMN", "@FMW", "@FRM"):
        if mt in tags:
            motion[mt] += 1

# ---- .ca variant-1 positional slot tables -----------------------------------
# Every nonzero slot is a blob-relative entry offset; the table is banded:
# sparse @FMC first (holes = motions with no command track), then contiguous
# @FMN, contiguous @FMW of the same length, and @FRM in the last slot.
v1 = {"files": 0, "frm_only": 0, "bad_tag": 0, "bad_band": 0,
      "frm_last": 0, "fmn_eq_fmw": 0, "hdr": collections.Counter(),
      "fmc_band80": 0, "fmn_total": 0}
for p in names:
    if not p.lower().endswith(".ca"):
        continue
    d = read_all(p)
    var, clen, cnt = struct.unpack_from("<III", d, 4)
    if var != 1:
        continue
    v1["files"] += 1
    v1["hdr"][struct.unpack_from("<II", d, 0x30)] += 1
    base = 0x40
    seq = []
    for i in range(cnt):
        v = struct.unpack_from("<I", d, base + i * 4)[0]
        t = d[base + v:base + v + 4] if v else None
        if v == 0:
            seq.append(None)
        elif t in (b"@FMC", b"@FMN", b"@FMW", b"@FRM"):
            seq.append(t)
            if t == b"@FMN":
                # same tail grammar as the .cm walk above, on .ca entries
                fmn["ca"] += 1
                eo = base + v
                ro = eo + 0xF0
                for _ in range(struct.unpack_from("<I", d, eo + 0x0C)[0]):
                    w2 = struct.unpack_from("<H", d, ro + 2)[0]
                    mask, adv = w2 & 0x1FF, (w2 >> 9) & 0x3F
                    chans = struct.unpack_from("<9H", d, ro + 4)
                    fmn["adv"][adv] += 1
                    for ci in range(9):
                        if bool((mask >> ci) & 1) == bool(chans[ci] & 0x8000):
                            fmn["mask_bad"] += 1
                    ro += adv
                if ro > eo + struct.unpack_from("<I", d, eo + 8)[0]:
                    fmn["walk_bad"] += 1
        else:
            seq.append(b"?")
            v1["bad_tag"] += 1
    if seq.count(b"@FMN") == 0 and seq.count(b"@FMW") == 0 \
            and seq.count(b"@FMC") == 0:
        v1["frm_only"] += 1
    if seq[-1] == b"@FRM":
        v1["frm_last"] += 1
    nfmn = seq.count(b"@FMN")
    v1["fmn_total"] += nfmn
    if nfmn == seq.count(b"@FMW"):
        v1["fmn_eq_fmw"] += 1
    # band order: no @FMC may follow the first @FMN; FMN/FMW/FRM contiguous
    first_n = seq.index(b"@FMN") if b"@FMN" in seq else cnt
    # the @FMC zone is dword[+0x30]=80 slots per group times dword[+0x34]
    # groups (1 or 3); @FMN starts at 80*groups, and in @FRM-only files the
    # @FRM occupies the first slot after the FMC zone.
    zone = 80 * struct.unpack_from("<I", d, 0x34)[0]
    if first_n == zone or (b"@FMN" not in seq and seq[zone] == b"@FRM"):
        v1["fmc_band80"] += 1
    tail = seq[first_n:]
    if any(t == b"@FMC" or t is None for t in tail):
        v1["bad_band"] += 1
    elif [t for t in tail if t is not None] != \
            sorted(tail, key=lambda t: (b"@FMN", b"@FMW", b"@FRM").index(t)):
        v1["bad_band"] += 1

print("variant-1 .ca files:", v1["files"], "| @FRM-only:", v1["frm_only"],
      "| @FRM last:", v1["frm_last"], "| FMN==FMW:", v1["fmn_eq_fmw"],
      "| bad tags:", v1["bad_tag"], "| bad bands:", v1["bad_band"])
print("variant-1 header (+0x30 band-stride, +0x34 group-count):",
      dict(v1["hdr"]))
print("variant-1 FMC-band==80 slots:", v1["fmc_band80"])

print("== .cm tag inventory ==")
for t, c in tag_counts.most_common():
    print("  %-6s %d" % (t, c))
print("@FEF files:", fef_files)
print("@FEF kind:", dict(fef_field["kind"]))
print("@FEF name==basename:", dict(fef_field["name==basename"]))
print("@FEF embedded-EFX0010 offset:", dict(fef_magic_off))
for k in sorted(fef_field):
    if k.startswith("+"):
        vals = fef_field[k]
        if len(vals) <= 6:
            print("  @FEF %s: %s" % (k, dict(vals)))
        else:
            print("  @FEF %s: %d distinct" % (k, len(vals)))
print("motion tags in .cm:", dict(motion))
print("@FMC kinds:", dict(fmc["kind"]))
print("@FMC lens:", dict(sorted(fmc["len"].items())))
print("@FMC names:", dict(fmc["name"].most_common(12)))
print("@FMC record kinds:", dict(fmc["rec_kind"]))
print("@FMC sub-record keys:", fmc["sub_key"].most_common(10))
print("@FMC opcodes used:", len(fmc["op"]), "distinct;",
      fmc["op"].most_common(12))
print("@FMC grammar violations: walk=%d sub=%d cmd=%d" %
      (fmc["walk_bad"], fmc["sub_bad"], fmc["cmd_bad"]))
print("@FMC payload u16 histogram (+0x30..0x4F):")
for k in sorted(fmc["pay"]):
    vals = fmc["pay"][k]
    if len(vals) <= 8:
        print("   %s: %s" % (k, dict(vals.most_common(8))))
    else:
        print("   %s: %d distinct" % (k, len(vals)))
print("@FMN kinds:", dict(fmn["kind"]))
print("@FMN lens:", dict(sorted(fmn["len"].items())))
print("@FMN names:", dict(fmn["name"].most_common(12)))
print("@FMW kinds:", dict(fmw["kind"]))
print("@FMW lens:", dict(sorted(fmw["len"].items())))
print("@FMW +0x30 (stream base):", dict(fmw["base"].most_common(6)))
print("@FMW +0x34 (format arm):", dict(fmw["arm"]))
print("@FMN +0x60 f32x4:", dict(fmn["f60"].most_common(6)))
print("@FMN tail: .ca entries=%d rec-counts=%s adv=%s mask_bad=%d walk_bad=%d"
      % (fmn["ca"], dict(fmn["nrec"].most_common(6)),
         dict(fmn["adv"].most_common(6)), fmn["mask_bad"], fmn["walk_bad"]))

# ---- checks --------------------------------------------------------------
def check(name, ok, detail):
    print(("PASS " if ok else "FAIL ") + name + " " + str(detail))
    if not ok:
        fails.append(name)

check("cm-files", len(tag_counts) > 0, "")
check("fef-magic-off", fef_magic_off == {0x30: fef_files}, dict(fef_magic_off))
check("fef-kind", fef_field["kind"] == {0: fef_files}, dict(fef_field["kind"]))
check("fef-name==basename", fef_field["name==basename"] == {True: fef_files},
      dict(fef_field["name==basename"]))
check("fmc-kind", fmc["kind"] == {1: sum(fmc["kind"].values())}, dict(fmc["kind"]))
# Executor-confirmed grammar (0041E000 / init 0041CD30): event records tile
# exactly, kinds only {0,1}, exactly one kind-1 record per entry, commands and
# sub-records stay inside their parents, and every used opcode lands inside the
# 76-entry dispatch table 01EFFAF0.
_fmc_total = sum(fmc["kind"].values())
check("fmc-grammar", not (fmc["walk_bad"] or fmc["sub_bad"] or fmc["cmd_bad"]),
      "walk=%d sub=%d cmd=%d" % (fmc["walk_bad"], fmc["sub_bad"], fmc["cmd_bad"]))
check("fmc-rec-kinds", set(fmc["rec_kind"]) <= {0, 1}, dict(fmc["rec_kind"]))
check("fmc-rec1-per-entry", fmc["rec1_per_entry"] == _fmc_total,
      "%d/%d" % (fmc["rec1_per_entry"], _fmc_total))
check("fmc-opcodes-bounded", max(fmc["op"] or {0}) <= 0x4B,
      "max op 0x%02X" % max(fmc["op"] or {0}))
# .ca variant-1 slot tables: positional entry offsets in tag-segregated bands
# (sparse @FMC, then contiguous @FMN/@FMW 1:1, @FRM last), corpus-verified.
check("v1-slots-clean", v1["bad_tag"] == 0 and v1["bad_band"] == 0,
      "tags=%d bands=%d" % (v1["bad_tag"], v1["bad_band"]))
check("v1-frm-last", v1["frm_last"] == v1["files"],
      "%d/%d" % (v1["frm_last"], v1["files"]))
check("v1-fmn-fmw-1to1", v1["fmn_eq_fmw"] == v1["files"],
      "%d/%d" % (v1["fmn_eq_fmw"], v1["files"]))
# 004090D0 resolves slot[80*group + index] with group < dword[+0x34]: corpus
# headers are exactly {(80,1),(80,3)} — one or three identical 80-slot
# command-track groups, then the shared @FMN/@FMW/@FRM bands.
check("v1-hdr-80x1or3", set(v1["hdr"]) <= {(80, 1), (80, 3)}, dict(v1["hdr"]))
check("v1-fmc-band-80g", v1["fmc_band80"] == v1["files"],
      "%d/%d" % (v1["fmc_band80"], v1["files"]))
check("fmn-kind", fmn["kind"] == {0x02001111: sum(fmn["kind"].values())}, dict(fmn["kind"]))
check("fmw-kind", fmw["kind"] == {0: sum(fmw["kind"].values())}, dict(fmw["kind"]))
check("fmn==fmw-count", sum(fmn["kind"].values()) == sum(fmw["kind"].values()),
      "%d vs %d" % (sum(fmn["kind"].values()), sum(fmw["kind"].values())))
check("frm-not-in-cm", "@FRM" not in tag_counts, "")
# 0041B650 selects on dword[fmw+0x34]: arm 1 = packed stream, arm 0 = table arm.
# Corpus: every @FMW is arm 1 except the lone 0x644-byte record (w0258.cm).
check("fmw-arm", fmw["arm"] == {1: 110, 0: 1}, dict(fmw["arm"]))
# +0x30 is the stream/table base offset the decoder passes to 00409150/00409170.
check("fmw-base-nonzero", all(v > 0 for v in fmw["base"]), dict(fmw["base"].most_common(4)))
# @FMN +0x60 is a corpus-uniform f32x4 = {20 deg, 20 deg, 60 deg, 60 deg} rad —
# a constant clamp block, not per-motion data (tolerance: two bit-variants exist).
import math
_fmn_f60_ok = all(len(vals) == 4 and
                  abs(vals[0] - math.pi / 9) < 1e-6 and abs(vals[1] - math.pi / 9) < 1e-6 and
                  abs(vals[2] - math.pi / 3) < 1e-6 and abs(vals[3] - math.pi / 3) < 1e-6
                  for vals in fmn["f60"])
check("fmn-f60-clamp-const", _fmn_f60_ok, dict(fmn["f60"].most_common(4)))
# @FMN tail grammar (walker 0041C0C2-0041C15C, base switch 00409190): u32
# +0x0C = record count; records are fixed 22-byte {u16 nodeKey, u16
# {chMask:9, len:6, flag:1}, u16 chIdx[9]}; mask bit i set iff chIdx[i] lacks
# the 0x8000 absent-marker; the stream must not overrun the entry. Corpus:
# 746,142 records across .cm + .ca, all adv=22, flag always 0.
check("fmn-tail-grammar", fmn["walk_bad"] == 0,
      "walk_bad=%d" % fmn["walk_bad"])
check("fmn-tail-adv22", set(fmn["adv"]) == {22}, dict(fmn["adv"].most_common(4)))
check("fmn-tail-mask-vs-8000", fmn["mask_bad"] == 0,
      "mismatches=%d" % fmn["mask_bad"])
# every @FMN slot the v1 band scan saw must have been walked (non-var-1 .ca
# files carry additional @FMN entries outside this census's slot scan).
check("fmn-tail-ca-count", fmn["ca"] == v1["fmn_total"],
      "walked=%d slots=%d" % (fmn["ca"], v1["fmn_total"]))
sys.exit(1 if fails else 0)
