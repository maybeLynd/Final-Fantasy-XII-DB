"""UQ-218 pass 18: the @FOR record's per-part tail lists and the @FDM descriptor +0x08 bytes, under the reader's own
decoding (SWE2-DATA 2026-09-30).  Static reader: the draw builder 0053AB50 (certified image 73461d08...).

Code (checked below, instruction by instruction):
  0053C166-0053C193  list = recordBase + word[rec + 8 + 2*part], count = word[rec + 0x10 + 2*part];
                     on the flag-1 pass (arg 6, rbp+0x86F8 != 0): word[rec + 0xE] / word[rec + 0x16]
  0053C222-0053C2E4  packing kind = byte[rec + 2 + part] (flag-1 pass: byte[rec + 1]):
                     3 -> 4 bytes {d, s, a, b}; 2 -> 3 bytes {d, s, a:4 | b:4}; 1 -> 2 bytes {d:5 | s:3, a:4 | b:4}
  0053C305-0053C331  d -> descriptor = fdm + word[fdm + dword[fdm + 0x34 + 4*part] + 4 + 2*d]; s -> sub-record =
                     fdm + word[desc + 0xC + 2*s]; a / b -> rbp+0x120 / rbp+0x124, handed to 0053D140 with the sub-record
  0053C403 -> 0053D4B0(.., r9 = desc): s8 desc+8 (0053D585) and s8 desc+9 (0053D592) into the VU1 packet, with desc+4
                     bit 0, bits 1-7, bit 28, bit 29.
  0053B29D-0053B30E  records / lists come from the rcx argument's @FOR, the @FDM from the rdx argument's.
  0053D780           a class-'h' object (byte [obj+0xC] == 0x68, 0053D8C9) is drawn twice: (rcx = rbx, rdx = rdi, flag 0),
                     then (rcx = rbx, rdx = rbx, flag 1); every other object once with rcx = rdx = the object.
Corpus: every shipped .cm with @FOR + @FDM in the full extract.  High models (obj_finish/in/high/h<name>_NN.cm) are
checked on the flag-0 pass against their base model <name>.cm's @FDM (the rdx partner; which file the partner index
names is inferred from the data fit, not traced) and on the flag-1 pass against their own.
"""
import collections, glob, os, re, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d as IMG, off  # noqa: E402  (SHA-256-checked image)
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract/ps2data/obj_finish"
md = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0


def check(name, ok, detail=""):
    global fails
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    fails += 0 if ok else 1


def ins_at(a):
    o = off(a)
    x = next(md.disasm(IMG[o:o + 16], a))
    return "%s %s" % (x.mnemonic, x.op_str)


EXPECT = {
    0x0053C16B: "movzx eax, word ptr [rbx + r15*2 + 8]",
    0x0053C173: "movzx eax, word ptr [rbx + 0xe]",
    0x0053C17A: "add eax, dword ptr [rbp + 0xc8]",
    0x0053C187: "movzx eax, word ptr [rbx + r15*2 + 0x10]",
    0x0053C18F: "movzx eax, word ptr [rbx + 0x16]",
    0x0053C227: "movzx eax, byte ptr [r15 + rbx + 2]",
    0x0053C22F: "movzx eax, byte ptr [rbx + 1]",
    0x0053C2BF: "shr r9d, 5",
    0x0053C2CA: "and r10d, 0x1f",
    0x0053C308: "mov ecx, dword ptr [r8 + r15*4 + 0x34]",
    0x0053C320: "add ecx, 0xc",
    0x0053CDF3: "add r14, 4",
    0x0053CDFB: "add rdx, 3",
    0x0053CE02: "add r8, 2",
    0x0053D585: "movsx edx, byte ptr [rbp + 8]",
    0x0053D592: "movsx edx, byte ptr [rbp + 9]",
    0x0053D8C9: "cmp byte ptr [rsi + 0xc], 0x68",
    0x0053DA4E: "mov dword ptr [rsp + 0x28], 0",
    0x0053DA81: "mov dword ptr [rsp + 0x28], 1",
}
bad = ["%08X: %s" % (a, ins_at(a)) for a, t in EXPECT.items() if ins_at(a) != t]
check("S the reader instructions", not bad, "%d sites%s" % (len(EXPECT), "" if not bad else " - " + "; ".join(bad)))

WIDTH = {1: 2, 2: 3, 3: 4}


def ents(dd):
    var, _c, cnt = struct.unpack_from("<III", dd, 4)
    base = 0x40 if var == 1 else 0x30
    e = {}
    for i in range(cnt):
        v = struct.unpack_from("<I", dd, base + i * 4)[0]
        if var == 1 and v == 0:
            continue
        e[dd[base + v:base + v + 4]] = base + v
    return e


def fdm_lists(dd, fd):
    out = []
    for part in range(3):
        lo = struct.unpack_from("<I", dd, fd + 0x34 + 4 * part)[0]
        out.append(None if lo == 0xFFFFFFFF else (fd + lo + 4, struct.unpack_from("<I", dd, fd + lo)[0]))
    return out


def elements(dd, lst, n, kind):
    w = WIDTH[kind]
    for k in range(n):
        e = lst + w * k
        if kind == 3:
            yield dd[e], dd[e + 1], dd[e + 2], dd[e + 3]
        elif kind == 2:
            yield dd[e], dd[e + 1], dd[e + 2] & 0xF, dd[e + 2] >> 4
        else:
            yield dd[e] & 0x1F, dd[e] >> 5, dd[e + 1] & 0xF, dd[e + 1] >> 4


def resolves(dd, fd, lists, part, elems):
    L = lists[part]
    fdlen = struct.unpack_from("<I", dd, fd + 8)[0]
    for dx, sx, _a, _b in elems:
        if L is None or dx >= L[1]:
            return False
        desc = fd + struct.unpack_from("<H", dd, L[0] + 2 * dx)[0]
        if desc + 0x10 > fd + fdlen:
            return False
        sub = fd + struct.unpack_from("<H", dd, desc + 0xC + 2 * sx)[0]
        if not fd <= sub < fd + fdlen:
            return False
    return True


files = sorted(glob.glob(os.path.join(ROOT, "**", "*.cm"), recursive=True))
base_by_name = {os.path.basename(p).lower(): p for p in files if "/high/" not in p.replace("\\", "/")}
st, kinds = collections.Counter(), collections.Counter()
dbytes = collections.Counter()
for p in files:
    dd = open(p, "rb").read()
    if len(dd) < 0x40:
        continue
    e = ents(dd)
    if b"@FOR" not in e or b"@FDM" not in e:
        continue
    high = "/high/" in p.replace("\\", "/")
    st["files high" if high else "files normal"] += 1
    fo, fd = e[b"@FOR"], e[b"@FDM"]
    own = fdm_lists(dd, fd)
    partner = None
    if high:
        nm = re.sub(r"_\d+\.cm$", ".cm", re.sub(r"^h", "", os.path.basename(p).lower()))
        q = base_by_name.get(nm)
        if q:
            d2 = open(q, "rb").read()
            e2 = ents(d2)
            if b"@FDM" in e2:
                partner = (d2, e2[b"@FDM"], fdm_lists(d2, e2[b"@FDM"]))
        st["high with a base-model partner" if partner else "high WITHOUT a partner"] += 1
    forlen = struct.unpack_from("<I", dd, fo + 8)[0]
    rbase = fo + struct.unpack_from("<H", dd, fo + 0x38)[0]
    for r in range(dd[fo + 0x30]):
        rec = rbase + r * 0xE0
        for part in range(3):
            kind = dd[rec + 2 + part]
            n = struct.unpack_from("<H", dd, rec + 0x10 + 2 * part)[0]
            kinds[kind] += 1
            if n == 0:
                st["empty part list (kind %d)" % kind] += 1
                continue
            if kind not in WIDTH:
                st["non-empty list, kind outside 1..3"] += 1
                continue
            lst = rbase + struct.unpack_from("<H", dd, rec + 8 + 2 * part)[0]
            if lst + WIDTH[kind] * n > fo + forlen:
                st["list overruns @FOR"] += 1
                continue
            el = list(elements(dd, lst, n, kind))
            st["elements"] += len(el)
            if not high:
                st["normal flag-0 list resolves in own @FDM" if resolves(dd, fd, own, part, el) else "normal flag-0 list FAILS"] += 1
            elif partner:
                st["high flag-0 list resolves in partner @FDM" if resolves(partner[0], partner[1], partner[2], part, el)
                   else "high flag-0 list FAILS in partner"] += 1
                if not resolves(dd, fd, own, part, el):
                    st["high flag-0 list would fail in its own @FDM (control)"] += 1
        an = struct.unpack_from("<H", dd, rec + 0x16)[0]
        if an:
            akind = dd[rec + 1]
            alst = rbase + struct.unpack_from("<H", dd, rec + 0xE)[0]
            ok = akind in WIDTH and resolves(dd, fd, own, 0, list(elements(dd, alst, an, akind)))
            st[("high" if high else "normal") + " flag-1 list resolves in own @FDM part 0" if ok else "flag-1 list FAILS"] += 1
    for L in own:
        if L is None:
            continue
        for k in range(L[1]):
            desc = fd + struct.unpack_from("<H", dd, L[0] + 2 * k)[0]
            dbytes[dd[desc + 8:desc + 0xC].hex()] += 1

print("stats:", dict(sorted(st.items())))
print("part packing kinds (all records x 3 parts):", dict(sorted(kinds.items())))
print("descriptor bytes +8..+0xB:", dict(dbytes))
check("C1 no non-empty list has a kind outside 1..3 or overruns its @FOR entry",
      st["non-empty list, kind outside 1..3"] == 0 and st["list overruns @FOR"] == 0)
check("C2 normal models: every flag-0 list resolves in its own @FDM",
      st["normal flag-0 list FAILS"] == 0 and st["normal flag-0 list resolves in own @FDM"] > 0,
      "%d lists" % st["normal flag-0 list resolves in own @FDM"])
check("C3 high models: every flag-0 list resolves in the base model's @FDM",
      st["high flag-0 list FAILS in partner"] == 0 and st["high WITHOUT a partner"] == 0,
      "%d lists; %d of them would fail in the high model's own @FDM" % (
          st["high flag-0 list resolves in partner @FDM"], st["high flag-0 list would fail in its own @FDM (control)"]))
check("C4 every flag-1 list is a high model's and resolves in its own @FDM part 0",
      st["flag-1 list FAILS"] == 0 and st["normal flag-1 list resolves in own @FDM part 0"] == 0,
      "%d high" % st["high flag-1 list resolves in own @FDM part 0"])
check("C5 descriptor bytes +8..+0xB are zero in every shipped descriptor", set(dbytes) == {"00000000"},
      "%d descriptors" % sum(dbytes.values()))
print("FAILS %d" % fails)
