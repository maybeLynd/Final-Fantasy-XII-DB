"""DD residue batch 10 (SWE2-CONTRACT, 2026-09-30): the checks behind the residue answered on six pages.

Run: python -B b10_checks.py   (last line FAILS n; must be FAILS 0)
Inputs: the certified image through retool.py (sha 73461d08...); the game extract D:/FFXII_TZA_extract (every .efx, .efb
and .cm file); the installed FFXII_TZA.vbf ($FF12_VBF, else the Steam path below), used only for control X1: a sample of
extract files re-decoded from the archive, byte for byte.

Page 1  16-UI/Widget-Object-Model/the-widget-message-protocol.md
  W1  the handler table today: 264 exact rows, 3 unparsed, no upper-bound row (the status line's "24 UNPARSED" is the
      2026-09-15 census's count)
  W2  the three unparsed rows: 005C5230 is `xor eax, eax / ret`; 0017CDE0 jumps to it; 002985C0 jumps to 003EE420
  W3  003EE420's id chain answers 1, 2 and 4 and sends every other id to 005C5230; positive controls: the same decoder
      gives the table's ids for 002D2DB0 and 0027AD70 (whose 18 arm tail-jumps 003EE420)
  W4  message 26: 002D2DB0 forwards it to its +0xC8 delegate and returns the delegate's answer (0 without one);
      005691E0 hands it to 00568FE0, which returns 0 on both exits
Page 2  17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md
  E1  every .efx opened: magic, +0x08 = 1.0f, +0x0C = the file's own size, and the chunk walk ends exactly there
  E2  every chunk's +4 is 0x100 in the .efx corpus
  E3  four of the six EFX-loader callers pass dword [efx + 0xC] as the size argument
  E4  every .efb: EFB0002, u16 +8 blob count, u16 +0xA row count, u32 +0xC = 0; every blob carries an EFX magic
  E5  004FF270 dispatches on record +0xC2 (the 0x700 chunk's byte +2): 0..3 to four relocators, others return
  E6  the four relocators: fixed record sizes 0x160 / 0x200 / 0x280 / 0x300; each stored dword gains low32(record) +
      the chunk's +8 dword (02EBB738) through 0020E600 / 0020E620
  E7  corpus: every 0x700 chunk has subtype 0..3, its +8 dword equals that subtype's fixed size, its length covers it,
      and every relocated dword plus the +8 bias lands inside the chunk
  E8  00333C80 rewrites an EFX0009 / EFX0008 0x600 record into the EFX0010 layout and then sets +0x16's high nibble to
      the index of the last non-zero lane byte of +0x0A..+0x14; the loader's +0x2C..+0x9F reset is 29 dwords
  E9  corpus: every 0x600 chunk's +8 dword is 0xA0; authored +0x16 high nibble vs the recomputed one (count)
  E10 the EFB buffer: 00377DC0 allocates 0x43D170 bytes (= the largest shipped .efb) and requests the file; 003788F0
      parses it (mode 1) or 0053DD10 (a `mov eax, 1 / ret` stub) takes it (mode 0); failure releases it; success
      publishes it at 02ADD088
  E11 the release: only 00378230 frees 02ADD088, after 0026FF50 (0024C550(2): every kind-2 context through 0024F410)
      and 0026F420; 0026FB90 disposes the previous EFB's contexts first
  E12 the handlers' retention: 0x600 records go into the context's +0x38 table, 0x700 records into its +0x840 table,
      and 0024F410 hands both tables to their teardowns
Page 3  17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md
  T1  the bodies that form an @FTE / @FCT entry pointer (a dword +0x218 / +0x21C read beside a +0x1F8 read) in the
      render-record code are 005044D0, 00504D30 and 0053AB50, plus the writer 00504F00
  T2  @FCT record fields read: 00504D30 +0x02; 005044D0 +0x02, +0x0C; 0053AB50 +0x00, +0x02, +0x04, +0x05, +0x06 -
      none reads +0x08
  T3  @FTE record fields: 0053AB50 reads +0x00 and +0x1C and hands the record to 00504520, which copies every field but
      +0x10; +0x10 is 0 in every shipped record
  T4  the texture cache: 005210F0 returns a live slot for a known key and bumps its count; 00504520 then writes this
      record's fields over the slot; 0053B70E skips the rebind while the model's slot already holds the key
  T5  corpus: 87 keys in more than one file; 80 with identical pixels, 85 with an identical descriptor
  T6  the +0xBA page: 00504D20's three sites all pass 00428CD0's second argument; the 23 sites of 00428CD0 pass 0, 2
      or 3 as constants, and one passes the 0xD0 effect instance's byte +0x235 = definition +0x146 (gated by
      definition +0x144 bit 2)
  T7  corpus: 0xD0 definitions with the gate set carry 2 or 3; none carries 1 (page 1 is never selected)
  T8  sub-index choice: 003E7210 passes byte +0x3D3 / word +0x3F8 and, for 0xFFFF, walks every sub of the list at
      [record+0x400]; the fields are written only by command 0x16's handler 00520BD0
Page 4  17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md
  M1  op 0x12: 005207C0 -> 003E29F0(obj, 4, byte[cmd+2] != 0), whose kind-4 arm sets bit 7 of the record's +0x1C
Page 5  17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md
  R1  the flag word is tested only for 0x100 by the binder 00372820, and by the copiers for bits 30, 31, 21 (+0x100),
      22, 23-25, 26-28; bit 21 in 004094D0 reads exactly sixteen u16 -> sixteen dwords
  R2  corpus: every non-last record's length is 8 + 2 x (b30 + b31 + 16 b21 + b22 + b23..b29), padded to 4 (so bit 29
      also carries a u16, which neither copier reads); which bits are set (bits 31 and 22 included)
  R3  runtime consumers located: 0041C260 and 00373860 stride 0x290; 00373860 calls 00372610
Page 6  06-Movement-And-Navigation/the-unit-shape-distance-primitives.md
  S1  the box primitive's face table 00D11200: six unit planes, +x -x +y -y +z -z with w = 1; margin 1.001 at 00D112A4
  S2  the sign mask 01CEBDA0: four 0x80000000 dwords
  S3  the sibling bodies: sizes, plant sites, callees (0022D7E0, 0022DE60, 00230790, 0022E7D0, 003810B0, 00381D90,
      00382020)
Control
  X1  extract files equal their archive entries (one .efx, one .efb, one .cm)
"""
import collections, hashlib, os, struct, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

ROOT = "D:/FFXII_TZA_extract"
VBF = os.environ.get("FF12_VBF", r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf")
FAILS = 0
PASSES = 0


def check(name, ok, detail=""):
    global FAILS, PASSES
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if ok:
        PASSES += 1
    else:
        FAILS += 1


def ins(a):
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def pin(name, a, text):
    got = ins(a)
    check(name, text in got, "%08X  %s" % (a, got))


SZ = T.sizes()


def body(f):
    return list(T.R.md.disasm(T.R.at(f, SZ[f]), f))


def rng(a, b):
    return [i for i in T.R.md.disasm(T.R.at(a, b - a), a) if i.address < b]


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")
SC = T.scan()


def callers(f):
    return sorted(SC["calls"].get(f, ()))


def u32(a):
    return struct.unpack("<I", T.R.at(a, 4))[0]


# ============================================================ page 1: the widget message protocol
TSV = os.path.join(DB, "16-UI", "Widget-Object-Model", "widget-message-handlers.tsv")
rows = [l.rstrip("\r\n").split("\t") for l in open(TSV, encoding="utf-8").read().splitlines()[1:] if l.strip()]
kinds = collections.Counter(r[5] for r in rows)
check("W1 handler table: 267 rows = 264 exact + 3 unparsed, no upper-bound row", len(rows) == 267 and kinds == {"exact": 264, "unparsed": 3},
      str(dict(kinds)))
unp = sorted(r[0] for r in rows if r[5] == "unparsed")
check("W2 the unparsed rows are 0017CDE0, 002985C0, 005C5230", unp == ["0017CDE0", "002985C0", "005C5230"], str(unp))
check("W2 005C5230 is xor eax, eax / ret", T.R.at(0x005C5230, 3) == b"\x33\xc0\xc3")
pin("W2 0017CDE0 jumps to 005C5230", 0x0017CDE0, "jmp 0x5c5230")
pin("W2 002985C0 jumps to 003EE420", 0x002985C0, "jmp 0x3ee420")
check("W2 002985C0 is planted by lea in 00298250", "lea" in ins(0x0029848B) and
      0x0029848B + 7 + struct.unpack("<i", T.R.at(0x0029848B + 3, 4))[0] == 0x002985C0, ins(0x0029848B))


def chain_ids(f):
    """decode a sub/dec/cmp + je/jne id chain on the register loaded from dword [rdx]"""
    ids, cum, reg, pend = [], 0, None, None
    for i in T.R.md.disasm(T.R.at(f, 0x80), f):
        m, o = i.mnemonic, i.op_str
        if reg is None:
            if m == "mov" and o.endswith("dword ptr [rdx]"):
                reg = o.split(",")[0]
            continue
        if m == "sub" and o.startswith(reg + ","):
            cum += int(o.split(",")[1], 0)
            pend = cum
        elif m == "dec" and o == reg:
            cum += 1
            pend = cum
        elif m == "cmp" and o.startswith(reg + ","):
            pend = cum + int(o.split(",")[1], 0)
        elif m == "je" and pend is not None:
            ids.append(pend)
            pend = None
        elif m == "jne" and pend is not None:
            ids.append(pend)
            break
        elif m.startswith("mov") and reg not in o.split(",")[0] and pend is None:
            continue
        else:
            break
    return sorted(ids)


tsv_ids = {r[0]: r[6] for r in rows}
for f in (0x002D2DB0, 0x0027AD70):
    got = ",".join(map(str, chain_ids(f)))
    check("W3 control: the chain decoder reproduces %08X's table ids" % f, got == tsv_ids["%08X" % f], got)
check("W3 003EE420 answers 1, 2, 4", chain_ids(0x003EE420) == [1, 2, 4], str(chain_ids(0x003EE420)))
pin("W3 003EE420: every other id goes to the no-op", 0x003EE452, "jmp 0x5c5230")
check("W3 0027AD70 tail-jumps 003EE420 (it is also a base procedure)", (0x0027AD70, 0x0027ADBF) in callers(0x003EE420), str(callers(0x003EE420)))
check("W3 003EE420 is not a row of the handler table", "003EE420" not in tsv_ids)
pin("W4 002D2DB0: id 26 arm (after -1,-1,-2,-1: cmp 0x15)", 0x002D2DFF, "cmp ecx, 0x15")
pin("W4 002D2DB0: the delegate +0xC8", 0x002D2E11, "mov rcx, qword ptr [rbx + 0xc8]")
pin("W4 002D2DB0: no delegate -> 0", 0x002D38C9, "xor eax, eax")
pin("W4 002D2DB0: calls the delegate's handler (rdx = the message)", 0x002D2E29, "call rax")
pin("W4 002D2DB0: returns its answer", 0x002D2E2B, "mov edi, eax")
check("W4 005691E0's jump-table arm for 26 is 00569ED4", 0x00120000 + u32(0x00120000 + 0x449F1C + 25 * 4) == 0x00569ED4)
pin("W4 005691E0 arm 26 calls 00568FE0", 0x00569EDC, "call 0x568fe0")
rets = [i for i in body(0x00568FE0) if i.mnemonic == "ret"]
tails = [i for i in body(0x00568FE0) if i.mnemonic == "jmp" and i.op_str.startswith("0x") and not (0x00568FE0 <= int(i.op_str, 16) < 0x00568FE0 + SZ[0x00568FE0])]
check("W4 00568FE0 has two exits and no tail jump", [r.address for r in rets] == [0x0056903A, 0x005691D4] and not tails)
for x, r in ((0x0056902E, 0x0056903A), (0x005691C8, 0x005691D4)):
    seg = rng(x, r)
    check("W4 00568FE0 exit %08X returns 0" % r, "xor eax, eax" in ins(x) and not any(("eax" in i.op_str.split(",")[0] or "rax" in i.op_str.split(",")[0]) for i in seg[1:] if "," in i.op_str))

# ============================================================ page 2: EFX / EFB containers
efx, efb, cms = [], [], []
for dp, dn, fn in os.walk(ROOT):
    for fname in fn:
        l = fname.lower()
        p = os.path.join(dp, fname)
        if l.endswith(".efx"):
            efx.append(p)
        elif l.endswith(".efb"):
            efb.append(p)
        elif l.endswith(".cm"):
            cms.append(p)
check("E1 population: 3,288 .efx, 410 .efb, 1,066 .cm", (len(efx), len(efb), len(cms)) == (3288, 410, 1066), str((len(efx), len(efb), len(cms))))
hdr = collections.Counter(); walk_ok = 0; flags = collections.Counter()
FIX = {0: 0x160, 1: 0x200, 2: 0x280, 3: 0x300}


def reloc_offsets(st):
    def af0(b):
        return [b, b + 4, b + 0x10, b + 0x14, b + 0x20, b + 0x24]

    def p4f0(b):
        return [b, b + 4]

    def e4a0(b):
        return p4f0(b) + p4f0(b + 0x10) + p4f0(b + 0x20)
    base = af0(0) + af0(0x40) + af0(0x80)
    if st == 0:
        return base + af0(0xD0)
    if st == 1:
        return base + p4f0(0xD0) + af0(0xE0) + af0(0x170)
    if st == 2:
        return base + af0(0xD0) + af0(0x160) + e4a0(0x1F0) + p4f0(0x270)
    return base + af0(0xD0) + af0(0x160) + e4a0(0x1F0) + e4a0(0x270) + p4f0(0x2F0)


c700 = collections.Counter(); sub700 = collections.Counter(); rel_bad = 0; rel_n = 0; c600 = collections.Counter(); nib = collections.Counter()
for p in efx:
    b = open(p, "rb").read()
    f8, sz = struct.unpack_from("<fI", b, 8)
    hdr[(b[:8], f8, sz == len(b))] += 1
    cur = 0x10
    while cur + 8 <= sz:
        ln, fl, ty = struct.unpack_from("<IHH", b, cur)
        if ln < 8 or cur + ln > sz:
            break
        flags[fl] += 1
        if ty == 0x700:
            st, bias = b[cur + 0xE], struct.unpack_from("<i", b, cur + 8)[0]
            c700[(st in FIX, st in FIX and bias == FIX[st], st in FIX and ln - 0x10 >= FIX[st])] += 1
            sub700[st] += 1
            if st in FIX:
                for o in reloc_offsets(st):
                    rel_n += 1
                    v = struct.unpack_from("<I", b, cur + 0x10 + o)[0]
                    if not (0 <= v + bias <= ln - 0x10):
                        rel_bad += 1
        if ty == 0x600:
            c600[struct.unpack_from("<i", b, cur + 8)[0]] += 1
            if b[:7] == b"EFX0010":
                rec = cur + 0x10
                lanes = b[rec + 0xA:rec + 0x15]
                last = max([k for k in range(11) if lanes[k]] or [0])
                nib[b[rec + 0x16] >> 4 == last] += 1
        cur += ln
    walk_ok += cur == sz
check("E1 every .efx: magic EFX0010 (3,284) or EFX0008 (4), +0x08 = 1.0f, +0x0C = file size",
      hdr == {(b"EFX0010\0", 1.0, True): 3284, (b"EFX0008\0", 1.0, True): 4}, str(dict(hdr)))
check("E1 every .efx chunk walk ends exactly at +0x0C", walk_ok == 3288, "%d of 3,288" % walk_ok)
check("E2 every chunk's +4 word is 0x100", set(flags) == {0x100}, "%d chunks" % sum(flags.values()))
for site, text in ((0x003B073F, "mov edx, dword ptr [rbx + 0xc]"), (0x003B226A, "mov edx, dword ptr [rcx + 0xc]"),
                   (0x003B2A6F, "mov edx, dword ptr [rbx + 0xc]"), (0x003B39B0, "mov edx, dword ptr [rdi + 0xc]")):
    pin("E3 size argument = dword [efx + 0xC]", site, text)
pin("E3 the EFB loader passes the blob header's size instead", 0x0026FCE2, "movsxd rbp, dword ptr [r14]")
check("E3 003EDAD0 has exactly six direct callers", len(callers(0x003EDAD0)) == 6, str(callers(0x003EDAD0)))
check("E3 003EDAD0 and 0026FB90 have no rip reference; 0026FB90's one caller is the thunk 0026FF90, called from 003788F0",
      not SC["refs"].get(0x003EDAD0) and not SC["refs"].get(0x0026FB90) and callers(0x0026FB90) == [(0x0026FF90, 0x0026FF90)]
      and callers(0x0026FF90) == [(0x003788F0, 0x0037893E)] and not SC["refs"].get(0x0026FF90))
check("E3 control: the rip-reference scan sees 003788F0's plant in 00377DC0", (0x00377DC0, 0x00377F26, "lea") in SC["refs"].get(0x003788F0, ()))
eh = collections.Counter(); blobs_ok = 0; blob_sz = collections.Counter()
for p in efb:
    b = open(p, "rb").read()
    n, rows_, x = struct.unpack_from("<HHI", b, 8)
    eh[(b[:8], x)] += 1
    cur, ok = 0x10, True
    for k in range(n):
        s = struct.unpack_from("<I", b, cur)[0]
        ok &= b[cur + 0x10:cur + 0x17] in (b"EFX0010", b"EFX0009", b"EFX0008")
        blob_sz[s == struct.unpack_from("<I", b, cur + 0x10 + 0xC)[0]] += 1
        cur += 0x10 + s
    blobs_ok += ok
check("E4 every .efb: EFB0002 and u32 +0x0C = 0", eh == {(b"EFB0002\0", 0): 410}, str(dict(eh)))
check("E4 every blob of every .efb carries an EFX magic", blobs_ok == 410)
check("E4 each blob's size word equals its EFX's own +0x0C", set(blob_sz) == {True}, str(dict(blob_sz)))
pin("E5 004FF270 reads record +0xC2", 0x004FF270, "movzx r8d, byte ptr [rcx + 0xc2]")
for a, t in ((0x004FF2A2, "jmp 0x537c80"), (0x004FF29D, "jmp 0x537fa0"), (0x004FF298, "jmp 0x538350"), (0x004FF293, "jmp 0x5387b0"),
             (0x004FF28F, "mov rax, rcx")):
    pin("E5 dispatch", a, t)
pin("E5 003A7E80 stores the chunk's byte +2 at record +0xC2", 0x003A7E9F, "mov byte ptr [rcx + 0xc2], al")
pin("E5 and passes low32(record) + [02EBB738]", 0x003A7EC1, "add edx, ecx")
for f, end in ((0x00537C80, "lea rax, [rdi + 0x160]"), (0x00537FA0, "lea rax, [rdi + 0x200]"), (0x00538350, "lea rax, [rdi + 0x280]"),
               (0x005387B0, "lea rax, [rdi + 0x300]")):
    b_ = body(f)
    check("E6 %08X returns record + its fixed size" % f, any(end == "%s %s" % (i.mnemonic, i.op_str) for i in b_), end)
    check("E6 %08X calls 004FF230 first" % f, [i for i in b_ if i.mnemonic == "call"][0].op_str == "0x4ff230")
pin("E6 004304F0 decodes the dword", 0x00430501, "call 0x20e600")
pin("E6 adds the delta", 0x00430506, "lea rcx, [rbx + rax]")
pin("E6 re-encodes it", 0x0043050A, "call 0x20e620")
pin("E6 0020E600 = zero-extended + [01F83530]", 0x0020E602, "add rax, qword ptr [rip + 0x1d74f27]")
pin("E6 0020E620 = low32 - [01F83530]", 0x0020E620, "sub ecx, dword ptr [rip + 0x1d74f0a]")
pin("E6 02EBB738 = the chunk's +8 dword", 0x003EDF76, "movsxd rax, dword ptr [rdi + 8]")
pin("E6 (stored)", 0x003EDF7C, "mov qword ptr [rip + 0x2acd7b5], rax")
pin("E6 handler gets chunk + 0xC", 0x003EDF93, "lea rcx, [rdi + 0xc]")
check("E7 every 0x700 chunk: subtype 0..3, +8 = the fixed size, length covers it", set(c700) == {(True, True, True)}, str(dict(c700)))
check("E7 0x700 chunks by subtype: 8,029 / 472 / 60 / 64", dict(sub700) == {0: 8029, 1: 472, 2: 60, 3: 64}, str(dict(sub700)))
check("E7 every relocated dword + bias lands inside its chunk", rel_bad == 0 and rel_n > 100000, "%d dwords, %d outside" % (rel_n, rel_bad))
pin("E8 00333C80 reads the EFX version global", 0x00333CA1, "mov ecx, dword ptr [rip + 0x1bcb709]")
pin("E8 version 9 arm", 0x00333CA7, "cmp ecx, 9")
pin("E8 version 8 arm", 0x00333DFE, "cmp ecx, 8")
pin("E8 v9: lanes +0x0A..+0x11 from +6..+0xD", 0x00333D5A, "mov qword ptr [r9 + 0xa], rcx")
pin("E8 v8: 11th lane cleared", 0x00333F0C, "mov byte ptr [r9 + 0x14], al")
pin("E8 an old nibble of 0xF", 0x00333FA2, "cmp cl, 0xf0")
pin("E8 clears +0x16 bit 1", 0x00333FA7, "and dl, 0xfd")
pin("E8 v9 and v8: +0x1C..+0x23 zeroed", 0x00333DDC, "mov qword ptr [r9 + 0x1c], rax")
pin("E8 (+0x24)", 0x00333DE0, "mov word ptr [r9 + 0x24], ax")
pin("E8 v8: lanes byte by byte from +6 (first)", 0x00333EAD, "movzx ecx, byte ptr [rsp + 6]")
pin("E8 all versions: lane loop over +0x0A", 0x00333FB0, "lea rdx, [r9 + 0xa]")
pin("E8 last non-zero lane", 0x00333FC7, "cmovne eax, ecx")
pin("E8 eleven lanes", 0x00333FCC, "cmp ecx, 0xb")
pin("E8 into +0x16's high nibble", 0x00333FD9, "or byte ptr [r9 + 0x16], al")
pin("E8 returns record + 0xA0", 0x00333FDD, "lea rax, [r9 + 0xa0]")
pin("E8 003A79C0 resets 29 dwords", 0x003A79E0, "mov edi, 0x1d")
pin("E8 from record + 0x2C", 0x003A79E8, "lea rbx, [rsi + 0x2c]")
check("E9 every 0x600 chunk's +8 dword is 0xA0", set(c600) == {0xA0}, str(dict(c600)))
check("E9 authored +0x16 high nibble equals the recomputed one in 3,209 of 5,359 EFX0010 records (the engine's is the loader's)",
      nib == {True: 3209, False: 2150}, str(dict(nib)))
maxefb = max(os.path.getsize(p) for p in efb)
pin("E10 00377DC0 allocates a fixed 0x43D170-byte block (mode 1)", 0x00377F41, "mov ecx, 0x43d170")
pin("E10 (mode 0)", 0x00377FB2, "mov ecx, 0x43d170")
check("E10 0x43D170 = 4,444,528 = the largest shipped .efb", maxefb == 0x43D170, "%d" % maxefb)
pin("E10 mode-1 completion 003788F0", 0x00377F26, "lea rax, [rip + 0x9c3]")
pin("E10 buffer at 02ADD050", 0x00377F6F, "mov qword ptr [rip + 0x27650da], rbx")
pin("E10 the read request", 0x00377F82, "call 0x32e7b0")
pin("E10 mode-0 completion 003789A0", 0x00377F97, "lea rax, [rip + 0xa02]")
pin("E10 mode-0 buffer at 02ADD098", 0x00377FE0, "mov qword ptr [rip + 0x27650b1], rbx")
pin("E10 003788F0 parses through the EFB loader", 0x0037893E, "call 0x26ff90")
pin("E10 0026FF90 is jmp 0026FB90", 0x0026FF90, "jmp 0x26fb90")
pin("E10 publishes it at 02ADD088", 0x0037895B, "mov qword ptr [rip + 0x2764726], rax")
pin("E10 failure: released", 0x00378975, "call 0x3697f0")
pin("E10 and forgotten", 0x00378981, "mov qword ptr [rip + 0x27646c4], 0")
pin("E10 mode 0 hands it to 0053DD10", 0x003789EE, "call 0x53dd10")
check("E10 0053DD10 is mov eax, 1 / ret", T.R.at(0x0053DD10, 6) == b"\xb8\x01\x00\x00\x00\xc3")
pin("E10 mode 0 publishes it at 02ADD088 too", 0x00378A0B, "mov qword ptr [rip + 0x2764676], rax")
pin("E10 003697F0 is the null-safe release", 0x003697F7, "jmp 0x369860")
refs088 = [(a, t) for a, t in (
    (0x00377D3A, "W"), (0x003783E0, "R"), (0x003783F3, "R"), (0x003783FF, "W"), (0x0037895B, "W"), (0x00378A0B, "W"))]
for a, t in refs088:
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    tgt = a + i.size + i.operands[-1 if t == "R" else 0].mem.disp if t == "W" else a + i.size + [o for o in i.operands if o.type == 3][0].mem.disp
    check("E11 %08X references 02ADD088" % a, tgt == 0x02ADD088, ins(a))
pin("E11 teardown: if a current EFB", 0x003783E0, "cmp qword ptr [rip + 0x2764ca1], rsi")
pin("E11 dispose its contexts", 0x003783E9, "call 0x26ff50")
pin("E11 then 0026F420", 0x003783EE, "call 0x26f420")
pin("E11 then release the buffer", 0x003783FA, "call 0x3697f0")
check("E11 00378230's callers", callers(0x00378230) == [(0x002628B0, 0x00262CC5), (0x00378A60, 0x00378ACF), (0x00378A60, 0x00378AF5), (0x0050D5D0, 0x0050D5D5)],
      str(callers(0x00378230)))
pin("E11 0026FF50: only when an EFB was parsed", 0x0026FF54, "cmp byte ptr [rip + 0x2d1f2dd], 0")
pin("E11 0026FF50 disposes kind 2", 0x0026FF5D, "mov ecx, 2")
pin("E11 (0024C550)", 0x0026FF62, "call 0x24c550")
check("E11 0024C550's jump table sends kind 2 straight to the list walk", 0x00120000 + u32(0x0024C5DC + 4) == 0x0024C599)
pin("E11 walks the per-kind list 020910A0[kind]", 0x0024C599, "lea rsi, [rbx + 0x1f710a0]")
pin("E11 each context through 0024F410", 0x0024C5B4, "call 0x24f410")
pin("E11 0024F410 runs the 0x800 run teardown", 0x0024F49B, "call 0x3a9600")
pin("E11 and the 0xA00 run teardown", 0x0024F4AE, "call 0x3a9950")
pin("E11 then frees the context", 0x0024F4BE, "call 0x3697f0")
pin("E11 0026F420 frees kind 2's second list", 0x0026F429, "call 0x24c460")
pin("E11 0026FB90 disposes the previous EFB first", 0x0026FBBB, "call 0x24c550")
pin("E11 (when one was parsed)", 0x0026FBAE, "cmp byte ptr [rip + 0x2d1f683], r15b")
pin("E11 the parsed flag is set on success", 0x0026FD56, "mov byte ptr [rip + 0x2d1f4db], 1")
pin("E12 retention: the 0x600 table 02EBEFA8 is the context's +0x38 (EFB loader)", 0x0026FCAD, "lea rcx, [rax + 0x38]")
pin("E12 the 0x700 table 02EBEFA0 is the context's +0x840", 0x0026FCB8, "lea rcx, [rax + 0x840]")
pin("E12 003A79C0 registers the 0x600 record there", 0x003A7A10, "mov qword ptr [rax + rcx*8 + 8], rsi")
pin("E12 003A7E80 registers the 0x700 record there", 0x003A7EB7, "mov qword ptr [r8 + r9*8], rcx")
pin("E12 0024F410 points the teardowns at +0x38", 0x0024F46A, "lea rax, [rbx + 0x38]")
pin("E12 (003A75B0)", 0x0024F475, "call 0x3a75b0")
pin("E12 and at +0x840", 0x0024F47A, "lea rax, [rbx + 0x840]")
pin("E12 (003A7D30)", 0x0024F488, "call 0x3a7d30")

# ============================================================ page 3: @FTE / @FCT
REND = [f for f in SZ if 0x00500000 <= f < 0x00540000]
formers = []
for f in REND:
    b_ = body(f)
    a = any(("dword ptr [" in i.op_str) and (" + 0x218]" in i.op_str or " + 0x21c]" in i.op_str) and "rsp" not in i.op_str for i in b_)
    c = any(" + 0x1f8]" in i.op_str for i in b_)
    if a and c:
        formers.append(f)
check("T1 bodies in 00500000..0053FFFF that read +0x218 / +0x21C beside +0x1F8", sorted(formers) == [0x005044D0, 0x00504D30, 0x00504F00, 0x0053AB50],
      " ".join("%08X" % f for f in sorted(formers)))
pin("T1 00504F00 is the writer (+0x218)", 0x00504FF4, "mov dword ptr [rbx + 0x218], eax")
pin("T1 (+0x21C)", 0x0050500A, "mov dword ptr [rbx + 0x21c], eax")
pin("T2 00504D30 reads record +0x02 (0x30 + 2)", 0x00504DA7, "movzx r8d, word ptr [rcx + rax*8 + 0x32]")
pin("T2 005044D0 reads +0x02", 0x005044F8, "movzx edx, word ptr [rax + rcx*8 + 0x32]")
pin("T2 005044D0 reads +0x0C", 0x00504508, "add eax, dword ptr [r9 + rcx*8 + 0x3c]")
pin("T2 0053AB50: the FCT entry kept at [rbp+0x50]", 0x0053B30A, "mov qword ptr [rbp + 0x50], rax")
pin("T2 0053AB50 reads +0x00 ((idx+3) x 16)", 0x0053B62F, "movzx eax, word ptr [rdi + rax*8]")
pin("T2 0053AB50: record = FCT + (idx + 3) x 16", 0x0053BB59, "add rbx, qword ptr [rbp + 0x50]")
fct_reads = sorted({i.op_str.split("[rbx")[1].split("]")[0] for i in rng(0x0053BB5D, 0x0053BDF7) if "[rbx" in i.op_str})
check("T2 0053AB50's reads through that record until rbx is reused (0053BDF7): +0, +2, +4, +5, +6", fct_reads == ["", " + 2", " + 4", " + 5", " + 6"], str(fct_reads))
check("T2 ... and rbx is not handed to a callee there", not any(i.mnemonic == "mov" and i.op_str.endswith(", rbx") for i in rng(0x0053BB5D, 0x0053BDF7)))
fte_reads = sorted({i.op_str.split("[r14")[1].split("]")[0] for i in rng(0x0053B6CB, 0x0053B7A0) if "[r14" in i.op_str})
check("T3 0053AB50 reads the @FTE record at +0 and +0x1C only", fte_reads == ["", " + 0x1c"], str(fte_reads))
pin("T3 record = FTE + (idx + 2) x 32", 0x0053B6CB, "add r14, r12")
pin("T3 handed to 00504520", 0x0053B71C, "call 0x504520")
got = sorted({i.op_str.split("[rbx")[1].split("]")[0] for i in body(0x00504520) if "[rbx" in i.op_str})
check("T3 00504520 reads every record field except +0x10", got == ["", " + 0x14", " + 0x18", " + 0x1c", " + 0xa", " + 0xc", " + 0xe", " + 4", " + 6", " + 8"], str(got))
fte10 = collections.Counter(); keys = collections.defaultdict(list)
for p in cms:
    b = open(p, "rb").read()
    i = b.find(b"@FTE")
    if i < 0:
        continue
    cnt = struct.unpack_from("<I", b, i + 0xC)[0]
    for k in range(cnt):
        r = b[i + 0x40 + k * 0x20:i + 0x60 + k * 0x20]
        fte10[struct.unpack_from("<I", r, 0x10)[0]] += 1
        off, ub = struct.unpack_from("<II", r, 0x18)[0], struct.unpack_from("<I", r, 0x14)[0]
        keys[struct.unpack_from("<I", r, 0x1C)[0]].append((p, r[:0x18] + r[0x1C:], hashlib.md5(b[i + off:i + off + ub]).digest(), r[0x18:0x1C]))
check("T3 @FTE record +0x10 is 0 in all 2,127 records", fte10 == {0: 2127}, str(dict(fte10)))
pin("T4 005210F0: a live slot with the key", 0x00521136, "cmp dword ptr [rax + 4], esi")
pin("T4 ... gains a reference", 0x00521193, "inc word ptr [rax + 0x24]")
pin("T4 256 slots", 0x0052113F + 2, "cmp ecx, 0x100")
pin("T4 00504520 acquires by the record's key", 0x0050454F, "mov ecx, dword ptr [rbx + 0x1c]")
pin("T4 then writes this record's payload offset into the slot", 0x00504575, "mov dword ptr [rax + 0x10], ecx")
pin("T4 and its VRAM size", 0x0050457A, "mov dword ptr [rax + 8], ecx")
pin("T4 the builder skips the rebind when the slot already holds the key", 0x0053B70E, "cmp dword ptr [rbx + 4], eax")
multi = {k: v for k, v in keys.items() if len({x[0] for x in v}) > 1}
check("T5 87 keys occur in more than one file", len(multi) == 87, str(len(multi)))
check("T5 80 of them with identical pixels", sum(1 for v in multi.values() if len({x[2] for x in v}) == 1) == 80)
check("T5 85 of them with an identical descriptor (all fields but the payload offset)", sum(1 for v in multi.values() if len({x[1] for x in v}) == 1) == 85)
check("T5 15 of them with an identical descriptor and offset", sum(1 for v in multi.values() if len({(x[1], x[3]) for x in v}) == 1) == 15)
diff = sorted(sorted({os.path.basename(x[0]) for x in v})[0] for v in multi.values() if len({x[2] for x in v}) > 1)
check("T5 the seven with different pixels are the hc1024/1029/1030/1042 x2/1044 variant sets and w0020/w2133", diff ==
      ["hc1024_01.cm", "hc1029_01.cm", "hc1030_01.cm", "hc1042_01.cm", "hc1042_01.cm", "hc1044_01.cm", "w0020.cm"], str(diff))
check("T6 00504D20 has three sites, all in 00428CD0 / 0042E4F0", callers(0x00504D20) == [(0x00428CD0, 0x00428D3C), (0x00428CD0, 0x00428D82), (0x0042E4F0, 0x0042E520)])
pin("T6 00428CD0 keeps its mode argument", 0x00428CF1, "mov dword ptr [rsp + 0x40], edx")
pin("T6 site 1 passes it", 0x00428D35, "mov edx, dword ptr [rsp + 0x40]")
pin("T6 site 2 passes it", 0x00428D7B, "mov edx, dword ptr [rsp + 0x40]")
pin("T6 0042E4F0 passes its context's +0x20 (= 00428CD0's rsp+0x40)", 0x0042E51A, "mov edx, dword ptr [rbx + 0x20]")
pin("T6 (the context is rsp+0x20)", 0x00428D91, "lea r8, [rsp + 0x20]")
vals = collections.Counter()
for f, site in callers(0x00428CD0):
    bb = body(f)
    k = [j for j, i in enumerate(bb) if i.address == site][0]
    last = next((i for i in reversed(bb[max(0, k - 60):k]) if "," in i.op_str and i.op_str.split(",")[0].strip() in ("edx", "dl", "rdx")), None)
    v = "0" if last is not None and last.mnemonic == "xor" and last.op_str == "edx, edx" else (last.op_str.split(",", 1)[1].strip() if last is not None else "?")
    vals[v] += 1
check("T6 the 23 sites of 00428CD0 pass 0, 2, 3 or the effect byte +0x235", sum(vals.values()) == 23 and set(vals) == {"0", "2", "3", "byte ptr [rdi + 0x235]"},
      str(dict(vals)))
pin("T6 the effect instance's +0x235 = definition +0x146", 0x004650E5, "movzx eax, byte ptr [r9 + 0x146]")
pin("T6 (store)", 0x004650ED, "mov byte ptr [rbx + 0x235], al")
pin("T6 r9 is the instance's definition [+0x20]", 0x00464F38, "mov r9, qword ptr [rbx + 0x20]")
pin("T6 the gate: definition +0x144 bit 2 -> instance +0x232 bit 10", 0x004650D3, "shl cx, 0xa")
pin("T6 00465CD0 tests the gate", 0x00465F11, "test word ptr [rdi + 0x232], ax")
pin("T6 (bit 10)", 0x00465F0C, "mov eax, 0x400")
pin("T6 0xA00 definition = chunk + 0x10: type written at +0x44", 0x003A9A8F, "mov byte ptr [rcx + 0x44], al")
d0 = collections.Counter()
EMB = os.path.join(DB, "17-Presentation-Rendering", "Effect-File-Formats", "members", "efx-embedded-stream-files.txt")
emb = [os.path.join(ROOT, l.strip()) for l in open(EMB) if l.strip()]
for p in efx + efb + emb:
    b = open(p, "rb").read()
    for m in (b"EFX0010", b"EFX0009", b"EFX0008"):
        i = b.find(m)
        while i >= 0:
            sz = struct.unpack_from("<I", b, i + 0xC)[0]
            end = i + sz if 0x10 <= sz and i + sz <= len(b) else len(b)
            cur = i + 0x10
            while cur + 8 <= end:
                ln, fl, ty = struct.unpack_from("<IHH", b, cur)
                if ln < 8 or cur + ln > end or fl != 0x100:
                    break
                if ty == 0xA00 and b[cur + 0xE] == 0xD0 and ln >= 0x157:
                    d0[((b[cur + 0x10 + 0x144] >> 2) & 1, b[cur + 0x10 + 0x146])] += 1
                cur += ln
            i = b.find(m, i + 1)
tc = open(os.path.join(DB, "17-Presentation-Rendering", "Effect-File-Formats", "members", "type_census.out"), encoding="utf-8").read()
check("T7 control: the walk finds as many 0xD0 chunks as the published type census (1,437)", sum(d0.values()) == 1437 and "0xD0 main chunks  1437" in tc,
      str(sum(d0.values())))
check("T7 0xD0 definitions: gate clear -> 0 (1,407); gate set -> 2 (24) or 3 (6); never 1", d0 == {(0, 0): 1407, (1, 2): 24, (1, 3): 6}, str(dict(d0)))
pin("T8 00427FF7's caller passes byte +0x3D3", 0x00427FEE, "movzx edx, byte ptr [rbx + 0x3d3]")
pin("T8 and word +0x3F8", 0x00427FE6, "movzx r8d, word ptr [rbx + 0x3f8]")
pin("T8 003E7210: 0xFFFF walks every sub", 0x003E722F, "cmp ebx, 0xffff")
pin("T8 the list at [record+0x400]", 0x003E723B, "mov r8, qword ptr [rsi + 0x400]")
pin("T8 one bind per sub", 0x003E7314, "call 0x504d30")
pin("T8 an explicit sub binds one", 0x003E73A9, "jmp 0x504d30")
pin("T8 0042B550 tail-jumps 003E7210 when +0x3D2 is set", 0x0042B566, "jne 0x3e7210")
pin("T8 00520BD0 writes +0x3F8 from the command word +4", 0x00520BF1, "mov word ptr [rcx + 0x3f8], ax")
w3 = collections.defaultdict(set)
for f, n in SZ.items():
    try:
        for i in T.R.md.disasm(T.R.at(f, n), f):
            if "," in i.op_str and i.mnemonic in ("mov", "or", "and", "xor", "add", "sub", "inc", "dec"):
                dst = i.op_str.split(",")[0]
                if dst.startswith("word ptr [") and dst.endswith(" + 0x3f8]"):
                    w3["3F8"].add(f)
                if dst.startswith("byte ptr [") and dst.endswith(" + 0x3d3]"):
                    w3["3D3"].add(f)
                if dst.startswith("byte ptr [") and dst.endswith(" + 0xba]"):
                    w3["0BA"].add(f)
    except Exception:
        pass
check("T8 image-wide, the only body storing a word at +0x3F8 or a byte at +0x3D3 (any base) is 00520BD0",
      w3["3F8"] == {0x00520BD0} and w3["3D3"] == {0x00520BD0}, str({k: sorted("%08X" % x for x in v) for k, v in w3.items() if k != "0BA"}))
check("T8 control: the same store census finds the +0xBA setter 00504D20", 0x00504D20 in w3["0BA"], "%d bodies store a byte at +0xBA" % len(w3["0BA"]))
pin("T8 (+0x3D3 = word +2 >> 1)", 0x00520BE7, "mov byte ptr [rcx + 0x3d3], al")

# ============================================================ page 4: @FEF / motion entries
pin("M1 005207C0 -> 003E29F0 kind 4", 0x005207D6, "mov edx, 4")
pin("M1 flag = byte[cmd+2] != 0", 0x005207DB, "cmp byte ptr [rbx + 2], r8b")
pin("M1 (setne)", 0x005207E2, "setne r8b")
pin("M1 kind 4 = (after -1, -1) cmp 2", 0x003E2A45, "cmp esi, 2")
pin("M1 clears bit 7 of +0x1C", 0x003E2A4E, "and byte ptr [rax + 0x1c], 0x7f")
pin("M1 and sets it from the flag", 0x003E2A56, "or byte ptr [rax + 0x1c], bpl")
pin("M1 (flag << 7)", 0x003E2A52, "shl bpl, 7")

# ============================================================ page 5: @FTR
tests = collections.Counter()
for f in (0x00409300, 0x004094D0):
    for i in body(f):
        if i.mnemonic == "bt" and i.op_str.startswith("edx") or i.mnemonic == "bt" and i.op_str.startswith("ecx"):
            tests[int(i.op_str.split(",")[1], 0)] += 1
check("R1 bits tested by bt in the copiers: 21, 22, 26, 27, 28, 30", sorted(tests) == [0x15, 0x16, 0x1A, 0x1B, 0x1C, 0x1E], str(sorted(tests)))
for a, t in ((0x00409358, "and eax, 0x200100"), (0x00409368, "test edx, edx"), (0x00409392, "test dword ptr [rbx + 4], 0x800000"),
             (0x004093A9, "test dword ptr [rbx + 4], 0x1000000"), (0x004093C0, "test dword ptr [rbx + 4], 0x2000000"), (0x004094F5, "test edx, edx")):
    pin("R1 flag test", a, t)
b_ = body(0x00372820)
ft = [i for i in b_ if i.mnemonic == "test" and i.op_str.startswith("dword ptr [r14 + 4]")]
check("R1 the binder tests the authored flag word only for 0x100", [i.op_str for i in ft] == ["dword ptr [r14 + 4], 0x100"] * 2)
check("R1 ... and touches [r14 + 4] nowhere else (no copy into the runtime record)",
      [i.address for i in b_ if "[r14 + 4]" in i.op_str] == [i.address for i in ft], str([hex(i.address) for i in b_ if "[r14 + 4]" in i.op_str]))
pin("R1 004094D0 bit 21: sixteen u16 -> sixteen dwords, loop from 6", 0x00409509, "mov edx, 6")
pin("R1 (step 0x10)", 0x0040957D, "add rdx, 0x10")
pin("R1 (to 0x26: two passes of eight)", 0x00409589, "cmp rdx, 0x26")
bits = collections.Counter(); lens = collections.Counter(); nrec = 0; flset = set()
Bt = lambda v, k: v >> k & 1
for p in cms:
    d = open(p, "rb").read()
    if d[:4] != b"@FRP":
        continue
    var, clen, cnt = struct.unpack_from("<III", d, 4)
    base = 0x40 if var == 1 else 0x30
    for e in range(cnt):
        o = base + struct.unpack_from("<I", d, base + e * 4)[0]
        if d[o:o + 4] != b"@FTR":
            continue
        n = struct.unpack_from("<I", d, o + 0xC)[0]
        aux = struct.unpack_from("<I", d, o + 0x34)[0]
        offs = sorted(struct.unpack_from("<I", d, o + 0x40 + 4 * k)[0] >> 12 for k in range(n))
        for j, ro in enumerate(offs):
            fl = struct.unpack_from("<I", d, o + ro + 4)[0]
            nrec += 1
            flset.add(fl)
            for k in range(32):
                bits[k] += Bt(fl, k)
            pr = 8 + 2 * (Bt(fl, 30) + Bt(fl, 31) + 16 * Bt(fl, 21) + Bt(fl, 22) + sum(Bt(fl, k) for k in range(23, 30)))
            if j + 1 < n:
                lens["fits" if offs[j + 1] - ro == (pr + 3) // 4 * 4 else "no"] += 1
            else:
                lens["last fits" if pr <= aux - ro < pr + 16 + 4 else "last no"] += 1
check("R2 27,561 records", nrec == 27561, str(nrec))
check("R2 2,151 distinct flag words", len(flset) == 2151, str(len(flset)))
check("R2 every record's length = 8 + 2 x (b30 + b31 + 16 b21 + b22 + b23..b29), padded to 4 (the last one to the pool)",
      lens == {"fits": 27561 - 1066, "last fits": 1066}, str(dict(lens)))
setb = sorted(k for k in range(32) if bits[k])
check("R2 bits never set: 3..7 and 20", [k for k in range(32) if not bits[k]] == [3, 4, 5, 6, 7, 20])
check("R2 bits in every record: 0, 8, 21, 30 (control: the page's census has 0x100 in 27,561 / 27,561)",[k for k in range(32) if bits[k] == nrec] == [0, 8, 21, 30])
check("R2 bit 31 in 11,243 records, bit 22 in 23,694, bit 29 in 1,953", (bits[31], bits[22], bits[29]) == (11243, 23694, 1953),
      str((bits[31], bits[22], bits[29])))
pin("R3 0041C260 strides 0x290", 0x0041C2E5, "imul rbx, rax, 0x290")
pin("R3 ... row +0xC0", 0x0041C2EF, "lea rdx, [rbx + 0xc0]")
pin("R3 ... row +0x120", 0x0041C2F6, "lea rcx, [rbx + 0x120]")
pin("R3 ... +0xF0 copied down", 0x0041C302, "mov eax, dword ptr [rbx + 0xf0]")
pin("R3 ... to +0x130", 0x0041C30F, "mov dword ptr [rbx + 0x130], eax")
pin("R3 00373860's second stride", 0x00373974, "imul rbx, rax, 0x290")
pin("R3 00373860 strides 0x290", 0x003738BE, "imul rbx, rcx, 0x290")
pin("R3 00373860 calls 00372610", 0x00373B85, "call 0x372610")

# ============================================================ page 6: the unit-shape primitives
face = struct.unpack("<24f", T.R.at(0x00D11200, 0x60))
want = (1, 0, 0, 1, -1, 0, 0, 1, 0, 1, 0, 1, 0, -1, 0, 1, 0, 0, 1, 1, 0, 0, -1, 1)
check("S1 00D11200: six planes +x -x +y -y +z -z, w = 1", face == tuple(float(x) for x in want), str(face))
pin("S1 the box primitive takes the table", 0x003814FF, "lea rdi, [rip + 0x98fcfa]")
pin("S1 and its +4 column", 0x003814F0, "lea rbx, [rip + 0x98fd0d]")
pin("S1 margin from 00D112A4", 0x003814F7, "movss xmm6, dword ptr [rip + 0x98fda5]")
check("S1 00D112A4 = 1.001", abs(struct.unpack("<f", T.R.at(0x00D112A4, 4))[0] - 1.001) < 1e-6)
check("S2 01CEBDA0 = four 0x80000000 dwords", T.R.at(0x01CEBDA0, 16) == b"\x00\x00\x00\x80" * 4)
pin("S2 A1D30 takes |x| with the f64 abs mask 01CEBD80", 0x003A1D37, "andps xmm1, xmmword ptr [rip + 0x194a042]")
check("S2 control: its neighbour 01CEBD80 = two 0x7FFFFFFFFFFFFFFF qwords, not a sign mask", T.R.at(0x01CEBD80, 16) == (b"\xff" * 7 + b"\x7f") * 2)
SIB = {0x0022D7E0: (1659, ["0022E7D0", "00230790", "003810B0", "00381D90"]),
       0x0022DE60: (1240, ["0022EAC0", "003810B0", "00381D90"]),
       0x00230790: (688, ["00202C70", "00202D50", "00202D70", "00203170"]),
       0x0022E7D0: (740, ["00202E10"]),
       0x003810B0: (923, ["00202B70", "00381450"]),
       0x00381D90: (288, ["00202B70", "00380800", "00380E00", "00380EB0"]),
       0x00382020: (94, [])}
for f, (n, cs) in SIB.items():
    got = sorted({"%08X" % int(i.op_str, 16) for i in body(f) if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x")
                  and not (f <= int(i.op_str, 16) < f + SZ[f])} - {"00808C40", "00861F14"})
    check("S3 %08X: %d B, callees (beside the cookie check and sqrtf) %s" % (f, n, ",".join(cs) or "none"), SZ[f] == n and got == cs, "%d %s" % (SZ[f], got))
for site, tgt in ((0x002316B7, 0x0022D7E0), (0x00232B22, 0x0022D7E0), (0x00230EB1, 0x0022DE60), (0x0023126A, 0x0022DE60)):
    i = next(T.R.md.disasm(T.R.at(site, 16), site, 1))
    check("S3 %08X plants %08X by lea" % (site, tgt), i.mnemonic == "lea" and site + i.size + i.operands[1].mem.disp == tgt, ins(site))
check("S3 00381D90's callers: the two callbacks and 00232160", callers(0x00381D90) == [(0x0022D7E0, 0x0022D96B), (0x0022DE60, 0x0022DF6A), (0x00232160, 0x00232193)])
check("S3 00382020's callers: the cylinder primitive twice and 0046DB50", callers(0x00382020) == [(0x00381630, 0x003819C5), (0x00381630, 0x003819D1), (0x0046DB50, 0x0046DCC0)])

# ============================================================ control: extract == archive
f = open(VBF, "rb")
magic, hl, cnt, hi32 = struct.unpack("<4sIII", f.read(16))
f.seek(0)
H = f.read(hl)
ent = 16 + cnt * 16
st = ent + cnt * 32
slen = struct.unpack_from("<I", H, st)[0]
bl = st + slen
E = [struct.unpack_from("<IIQQQ", H, ent + i * 32) for i in range(cnt)]
Bk = struct.unpack_from("<%dH" % ((hl - bl) // 2), H, bl)
strs = H[st + 4:st + slen]
idx = {strs[e[4]:strs.index(b"\0", e[4])].decode(): e for e in E}
nb = lambda s: (s >> 16) + (1 if s & 0xFFFF else 0)


def decode(e):
    out, pos = bytearray(), e[3]
    n = nb(e[2])
    for k in range(n):
        s = Bk[e[0] + k]
        last = k == n - 1
        flag = 0 if (s == 0 or (last and e[2] & 0xFFFF and s == e[2] & 0xFFFF)) else 1
        f.seek(pos)
        dd = f.read(s or 0x10000)
        out += zlib.decompress(dd) if flag else dd
        pos += s or 0x10000
    return bytes(out)


for rel in ("ps2data/effect_finish/jp/chara/h0026.efx", "ps2data/efb/alc0201.efb", "ps2data/obj_finish/in/monster/m11/m1132/m1132.cm"):
    ok = rel in idx and decode(idx[rel]) == open(os.path.join(ROOT, rel), "rb").read()
    check("X1 extract == archive: " + rel, ok)
f.close()
print("PASSES %d" % PASSES)
print("FAILS %d" % FAILS)
