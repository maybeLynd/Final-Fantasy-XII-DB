"""render_batch.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
PrimitiveRendererD3D11's middle: the batch merger at +0x880 and the two staging blocks after it, from the methods that fill
and reset them. Receivers come from the class vtable 00D86960 (entry rcx = this).

  M  slots 4 (006C8C50) and 5 (006C8BF0) move rcx to rbx and call 006DA5A0 / 006DA470 with rcx = rbx + 0x880. Both
     merger routines: the kind argument maps 0 / 1 to itself, 2..4 to 2 and anything else to 6; when the word at +0x8010
     is non-zero and the kind differs from +0xC, [[+0]] slot 0 is called (the IBatchMergerEvent sink flushes), then +0xC =
     the kind; the batch is also flushed while the word at +0x8010 plus the new vertex count exceeds 0x2AA (and, in
     006DA470, while +8 plus the new index count exceeds 0x4000). Indices are uint16 at +0x10 + 2 * (+8) (006DA470 copies
     the caller's and adds the vertex base; 006DA5A0 writes base + i), +8 grows by their count; vertices are 0x30 bytes
     each, copied to +0x8020 + 0x30 * (+0x8010), and the word at +0x8010 grows by their count. So the object is 0x10000:
     +0x10 + 2 * 0x4000 = +0x8010 and +0x8020 + 0x30 * 0x2AA = +0x10000
  S  slot 0 (006CA760): +0xB8 = this + 0x10880 + [+0x18860] * 0x7FE0, then [+0x18860] = 0 - a 0x7FE0-byte (0x2AA x 0x30)
     vertex block at +0x10880 whose counter sits right after it; slot 2 (006CA650): +0xC0 = this + 0x18864 +
     ([+0x20864] << 15), then [+0x20864] = 0 - a 0x8000-byte (0x4000 x uint16) index block at +0x18864, counter after it
  W  REGRESSION (FAILS before): BatchMerger6DA450 exists and tiles; the renderer's rows name the merger, both staging blocks,
     both counters and the two write pointers, and still tile to 0x20938
Usage: python render_batch.py [--patch]
"""
import hashlib, os, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
    return all(A.get(a) == v for a, v in pairs)
slot = lambda i: struct.unpack_from("<Q", d, off(0xD86960 + 8 * i))[0] - IB + B
check("M", [slot(i) for i in (0, 2, 4, 5)] == [0x6CA760, 0x6CA650, 0x6C8C50, 0x6C8BF0]
      and has(0x6C8C50, 0x6C8C9F, [(0x6C8C6C, ("mov", "rbx, rcx")), (0x6C8C74, ("lea", "rcx, [rbx + 0x880]")), (0x6C8C83, ("call", "0x6da5a0"))])
      and has(0x6C8BF0, 0x6C8C35, [(0x6C8C0C, ("mov", "rbx, rcx")), (0x6C8C19, ("lea", "rcx, [rbx + 0x880]")), (0x6C8C30, ("call", "0x6da470"))])
      and has(0x6DA470, 0x6DA597, [(0x6DA491, ("mov", "edi, 6")), (0x6DA4A4, ("mov", "edi, 2")), (0x6DA4AD, ("cmp", "word ptr [rcx + 0x8010], 0")), (0x6DA4B7, ("mov", "dword ptr [rcx + 0xc], edi")),
                                   (0x6DA4BC, ("cmp", "edi, dword ptr [rcx + 0xc]")), (0x6DA4C1, ("mov", "rcx, qword ptr [rcx]")), (0x6DA4C7, ("call", "qword ptr [rax]")),
                                   (0x6DA4D1, ("movzx", "edi, word ptr [rbx + 0x8010]")), (0x6DA4D8, ("mov", "esi, dword ptr [rbx + 8]")), (0x6DA4E0, ("cmp", "edi, 0x2aa")),
                                   (0x6DA4E8, ("cmp", "esi, 0x4000")), (0x6DA505, ("add", "rax, 8")), (0x6DA50C, ("lea", "rcx, [rbx + rax*2]")), (0x6DA537, ("add", "word ptr [rcx], ax")),
                                   (0x6DA556, ("mov", "dword ptr [rbx + 8], esi")), (0x6DA560, ("lea", "rcx, [rax + rax*2]")), (0x6DA564, ("shl", "rcx, 4")), (0x6DA568, ("add", "rcx, 0x8020")),
                                   (0x6DA581, ("mov", "word ptr [rbx + 0x8010], di"))])
      and has(0x6DA5A0, 0x6DA6A0, [(0x6DA609, ("cmp", "eax, 0x2aa")), (0x6DA656, ("add", "cx, word ptr [rbx + 0x8010]")), (0x6DA661, ("mov", "word ptr [rbx + rax*2 + 0x10], cx")),
                                   (0x6DA66A, ("add", "dword ptr [rbx + 8], edi")), (0x6DA687, ("add", "rcx, 0x8020")), (0x6DA696, ("add", "word ptr [rbx + 0x8010], di"))]),
      "vtable slots 4 / 5 pass this + 0x880 to the merger; indices uint16 from +0x10 (count +8, cap 0x4000), 0x30-byte vertices from +0x8020 (count word +0x8010, cap 0x2AA)")
check("S", has(0x6CA760, 0x6CA789, [(0x6CA760, ("mov", "eax, dword ptr [rcx + 0x18860]")), (0x6CA766, ("imul", "rdx, rax, 0x7fe0")), (0x6CA76D, ("lea", "rax, [rcx + 0x10880]")),
                                     (0x6CA774, ("mov", "dword ptr [rcx + 0x18860], 0")), (0x6CA781, ("mov", "qword ptr [rcx + 0xb8], rax"))])
      and has(0x6CA650, 0x6CA675, [(0x6CA650, ("mov", "eax, dword ptr [rcx + 0x20864]")), (0x6CA656, ("shl", "rax, 0xf")), (0x6CA65A, ("add", "rax, 0x18864")),
                                   (0x6CA660, ("mov", "dword ptr [rcx + 0x20864], 0")), (0x6CA66D, ("mov", "qword ptr [rcx + 0xc0], rax"))])
      and 0x10880 + 0x7FE0 == 0x18860 and 0x18864 + 0x8000 == 0x20864 and 0x2AA * 0x30 == 0x7FE0,
      "slot 0: +0xB8 into the 0x7FE0 vertex block at +0x10880 (counter +0x18860); slot 2: +0xC0 into the 0x8000 index block at +0x18864 (counter +0x20864)")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/render-context-02cc0410/render_batch.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
PR, BM = "PrimitiveRendererD3D11", "BatchMerger6DA450"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "CARVED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was="-", w=5): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
NR = "not read by the routines cited here"
def cut(o, w):
    if o == 0x00010:
        return [r(PR, 0x00010, 168, "unobservedSpan00010", "u8[168]", NR, U, "S", w),
                r(PR, 0x000B8, 8, "vertexWritePtr", "void*", "reset by vtable slot 0 (006CA760) to vertexStaging + counter * 0x7FE0", P, "S", w),
                r(PR, 0x000C0, 8, "indexWritePtr", "void*", "reset by vtable slot 2 (006CA650) to indexStaging + (counter << 15)", P, "S", w),
                r(PR, 0x000C8, 320, "unobservedSpan000C8", "u8[320]", NR, U, "S", w)]
    if o == 0x00880:
        return [r(PR, 0x00880, 0x10000, "batchMerger", BM, "the index / vertex batch vtable slots 4 and 5 append to; its event sink is this + 8", P, "M", w),
                r(PR, 0x10880, 0x7FE0, "vertexStaging", "u8[32736]", "a 0x7FE0-byte vertex block (0x2AA x 0x30), the base of vertexWritePtr", P, "S", w),
                r(PR, 0x18860, 4, "vertexStagingCount", "uint32", "multiplied by 0x7FE0 into vertexWritePtr and cleared by slot 0", P, "S", w),
                r(PR, 0x18864, 0x8000, "indexStaging", "uint16[16384]", "a 0x8000-byte index block, the base of indexWritePtr", P, "S", w)]
    if o == 0x20864:
        return [r(PR, 0x20864, 4, "indexStagingCount", "uint32", "shifted by 15 into indexWritePtr and cleared by slot 2", P, "S", w),
                r(PR, 0x20868, 208, "unobservedSpan20868", "u8[208]", "read and written by the class's methods up to +0x20934; not typed here", U, "S", w)]
BMROWS = [r(BM, 0x0000, 8, "eventSink", "void*", "an IBatchMergerEvent (the renderer's this + 8): its slot 0 is called to flush the batch", P, "M", w=4),
          r(BM, 0x0008, 4, "indexCount", "uint32", "the indices in the batch; a batch that would pass 0x4000 is flushed first (006DA470)", P, "M", w=4),
          r(BM, 0x000C, 4, "primitiveKind", "uint32", "the caller's kind mapped 0 / 1 -> itself, 2..4 -> 2, else 6; a change with vertices pending flushes the batch", P, "M", w=4),
          r(BM, 0x0010, 0x8000, "indices", "uint16[16384]", "the batch's indices: 006DA470 copies the caller's and adds the vertex base, 006DA5A0 writes base + i", P, "M", w=4),
          r(BM, 0x8010, 2, "vertexCount", "uint16", "the vertices in the batch; a batch that would pass 0x2AA is flushed first", P, "M", w=4),
          r(BM, 0x8012, 14, "unobservedSpan8012", "u8[14]", NR, U, "M", w=4),
          r(BM, 0x8020, 0x7FE0, "vertices", "u8[32736]", "0x2AA vertices of 0x30 bytes, copied in by both append routines", P, "M", w=4)]
NEWT = [BM, "0x10000", "17-Presentation-Rendering", "one at PrimitiveRendererD3D11 +0x880", "EMBEDDED in PrimitiveRendererD3D11", "006DA450", "not read here", P[0], P[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s M). Named by its constructor (not polymorphic; no engine name). Extent 0x8020 + 0x2AA x 0x30 = 0x10000, the vertex capacity the append routines enforce; the renderer's next field starts there. %s" % (REC, EXE),
        "17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md", "EMBED PrimitiveRendererD3D11 +0x00880"]
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]; out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == PR and REC not in c[8] and c[3].startswith("unobservedSpan"):
            rows = cut(int(c[1], 16), "%s %s (%s)" % (c[3], c[4], c[5][:160]))
            if rows and sum(int(x[2]) for x in rows) == int(c[2]): out += ["\t".join(x) + e for x in rows]; continue
        out.append(l)
    if not any(cells(l)[0] == BM for l in out):
        idx = max(i for i, l in enumerate(out) if cells(l)[0] == PR); out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in BMROWS]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == BM for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == PR); tl[ti + 1:ti + 1] = ["\t".join(NEWT) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
R = {int(c[1], 16): c[3] for c in F if c[0] == PR}
check("W", BM in T and sum(int(c[2]) for c in F if c[0] == BM) == 0x10000
      and [R.get(o) for o in (0xB8, 0xC0, 0x880, 0x10880, 0x18860, 0x18864, 0x20864)] == ["vertexWritePtr", "indexWritePtr", "batchMerger", "vertexStaging", "vertexStagingCount", "indexStaging", "indexStagingCount"]
      and sum(int(c[2]) for c in F if c[0] == PR) == 0x20938,
      "BatchMerger6DA450 tiles 0x10000; the renderer names the merger, the staging blocks, their counters and write pointers, and still tiles to 0x20938")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
