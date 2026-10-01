"""render_primitive.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
The object at RenderContext02CC0410 +0x18C0 is a PrimitiveRendererD3D11, and it bounds the context's extent.

  V  006C8750 (called by the context constructor at 00615B57 with rcx = this + 0x18C0) stores vtable 00D86960 at +0 and
     00D86AD0 at +8. Their complete-object locators name .?AVPrimitiveRendererD3D11@@ (offsets 0 and 8) with the hierarchy
     PrimitiveRendererD3D11 : PrimitiveRenderer (+0), IBatchMergerEvent (+8). It then default-constructs four
     PShaderPassStateD3D11 (00615ED0) at +0x208 / +0x398 / +0x528 / +0x6B8, and hands this + 0x880 and this + 8 (its
     IBatchMergerEvent) to 006DA450, which stores the event pointer at [+0x880], clears +0x888 and the word at +0x8890
  E  extent: census_receiver_fixpoint from the vtable (SEED=vtable 0x00D86960) reaches +0x20934 (4 bytes) as its highest
     access, so the class is at least 0x20938 bytes; the context's getter seed (SEED=call 0x00624670) reaches nothing past
     +0x18C0 + 0x20938 = +0x221F8. 005FD050 constructs the context at 02CC0410 and guards it with the dword at 02CE2610
     (005FD07A), 0x22200 bytes later, so the context is at most 0x22200 bytes and the renderer at most 0x20940
  W  REGRESSION (FAILS before): PrimitiveRendererD3D11 is a type (AT LEAST 0x20938) with its two vptr rows and the four
     pass states; the context embeds it at +0x18C0 and declares AT LEAST 0x221F8 / AT MOST 0x22200
Not claimed: what the spans between the typed rows hold, and the type of the object at +0x880 beyond 006DA450's three stores.
Usage: python render_primitive.py [--patch]
"""
import hashlib, json, os, struct, subprocess, sys, tempfile
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
KIT = os.path.join(ROOT, "Tools", "analysis-kit", "gfz-scripts")
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
def cstr(va): o = off(va); return d[o:d.index(b"\0", o)].decode("latin-1")
def col(vt):
    c = struct.unpack_from("<Q", d, off(vt - 8))[0] - IB + B
    sig, o, cdo, td, chd = struct.unpack_from("<5I", d, off(c))
    nb, arr = struct.unpack_from("<2I", d, off(chd + B + 8))
    bases = []
    for i in range(nb):
        bcd = struct.unpack_from("<I", d, off(arr + B + 4 * i))[0]
        btd, nc, mdisp = struct.unpack_from("<3I", d, off(bcd + B))
        bases.append((cstr(btd + B + 0x10), mdisp))
    return o, cstr(td + B + 0x10), bases
HIER = [(".?AVPrimitiveRendererD3D11@@", 0), (".?AVPrimitiveRenderer@@", 0), (".?AVIBatchMergerEvent@@", 8)]
rip = lambda a, n, disp: a + n + disp
check("V", has(0x615B50, 0x615B5C, [(0x615B50, ("lea", "rcx, [rbp + 0x18c0]")), (0x615B57, ("call", "0x6c8750"))])
      and has(0x6C8750, 0x6C886B, [(0x6C876B, ("mov", "rdi, rcx")), (0x6C8768, ("mov", "qword ptr [rcx], rax")), (0x6C877B, ("mov", "qword ptr [rcx + 8], rax")),
                                   (0x6C880A, ("add", "rcx, 0x208")), (0x6C8811, ("call", "0x615ed0")), (0x6C8816, ("lea", "rcx, [rdi + 0x398]")), (0x6C881D, ("call", "0x615ed0")),
                                   (0x6C8822, ("lea", "rcx, [rdi + 0x528]")), (0x6C8829, ("call", "0x615ed0")), (0x6C882E, ("lea", "rcx, [rdi + 0x6b8]")), (0x6C8835, ("call", "0x615ed0")),
                                   (0x6C883A, ("lea", "rcx, [rdi + 0x880]")), (0x6C8841, ("lea", "rdx, [rdi + 8]")), (0x6C8845, ("call", "0x6da450"))])
      and rip(0x6C8761, 7, 0x6BE1F8) == 0xD86960 and rip(0x6C876E, 7, 0x6BE35B) == 0xD86AD0
      and col(0xD86960) == (0, ".?AVPrimitiveRendererD3D11@@", HIER) and col(0xD86AD0) == (8, ".?AVPrimitiveRendererD3D11@@", HIER)
      and has(0x6DA450, 0x6DA463, [(0x6DA452, ("mov", "qword ptr [rcx], rdx")), (0x6DA455, ("mov", "dword ptr [rcx + 8], eax")), (0x6DA458, ("mov", "word ptr [rcx + 0x8010], ax"))]),
      "006C8750: vptrs 00D86960 / 00D86AD0 (PrimitiveRendererD3D11 : PrimitiveRenderer, IBatchMergerEvent @8); 4 pass states from +0x208; 006DA450(this + 0x880, this + 8)")
def census(seed, cell, extent):
    t = tempfile.NamedTemporaryFile(suffix=".json", delete=False); t.close()
    env = dict(os.environ, SEED=seed, CAP="800", EMIT_JSON=t.name)
    subprocess.run([sys.executable, os.path.join(KIT, "census_receiver_fixpoint.py"), cell, "0", extent], env=env, capture_output=True, cwd=os.path.dirname(DB))
    j = json.load(open(t.name)); os.unlink(t.name)
    return max(int(k.split(":")[0]) + int(k.split(":")[1]) for k in j["sites"])
top_r = census("vtable", "0xD86960", "0x100000"); top_c = census("call", "0x624670", "0x100000")
guard = has(0x5FD07A, 0x5FD0A6, [(0x5FD07A, ("cmp", "dword ptr [rip + 0x26e5590], eax")), (0x5FD097, ("lea", "rbx, [rip + 0x26c3372]")), (0x5FD0A1, ("call", "0x615840"))]) \
        and rip(0x5FD07A, 6, 0x26E5590) == 0x2CE2610 and rip(0x5FD097, 7, 0x26C3372) == 0x2CC0410
check("E", top_r == 0x20938 and top_c <= 0x18C0 + 0x20938 and guard,
      "the renderer's highest access ends at +0x%X; the context's getter census ends at +0x%X; the guard 02CE2610 bounds the context at 0x22200" % (top_r, top_c))

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/render-context-02cc0410/render_primitive.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RC, PR, PS = "RenderContext02CC0410", "PrimitiveRendererD3D11", "PShaderPassStateD3D11"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag): return "CARVED 2026-09-28 (OPUS, %s %s). %s" % (REC, tag, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, w=5): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag)]
RSIZE = "AT LEAST 0x20938 - its methods' highest access (vtable census) ends at +0x20938; embedded last in RenderContext02CC0410, whose static is bounded by the guard at 02CE2610, so AT MOST 0x20940"
PRROWS = [r(PR, 0x00000, 8, "vptr", "void*", "the class vtable 00D86960 (PrimitiveRendererD3D11, primary base PrimitiveRenderer), stored by 006C8750", P, "V"),
          r(PR, 0x00008, 8, "vptrBatchMergerEvent", "void*", "the IBatchMergerEvent base's vtable 00D86AD0 (complete-object offset 8); this address is the event sink 006C8750 gives the object at +0x880", P, "V"),
          r(PR, 0x00010, 504, "unobservedSpan00010", "u8[504]", "read and written by the class's methods (vtable census) and partly cleared by 006C8750; not typed here", U, "V E"),
          r(PR, 0x00208, 1600, "passStates", PS + "[4]", "four PShaderPassStateD3D11 default-constructed by 006C8750 (00615ED0 at +0x208 / +0x398 / +0x528 / +0x6B8); the methods copy them 16 bytes at a time", P, "V"),
          r(PR, 0x00848, 56, "unobservedSpan00848", "u8[56]", "read and written by the methods; not typed here", U, "E"),
          r(PR, 0x00880, 131044, "unobservedSpan00880", "u8[131044]", "from +0x880 the object 006DA450 builds: [+0x880] = this + 8 (the IBatchMergerEvent sink), +0x888 cleared, the word at +0x8890 cleared; the methods touch +0x8890, +0x18860 and the run from +0x20864, so its end is not fixed here", U, "V E"),
          r(PR, 0x20864, 212, "unobservedSpan20864", "u8[212]", "read and written by the methods up to the last access at +0x20934; not typed here", U, "E")]
NEWT = [PR, RSIZE, "17-Presentation-Rendering", "one at RenderContext02CC0410 +0x18C0 (built by 006C8750)", "EMBEDDED in RenderContext02CC0410", "006C8750", "not read here", P[0], P[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s V E). RTTI .?AVPrimitiveRendererD3D11@@ with bases PrimitiveRenderer (+0) and IBatchMergerEvent (+8). %s" % (REC, EXE),
        "17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md", "EMBED RenderContext02CC0410 +0x18C0"]
CSIZE = ("AT LEAST 0x221F8 - the PrimitiveRendererD3D11 at +0x18C0 reaches +0x221F8 (render_primitive.py E); AT MOST 0x22200, the distance to 005FD050's init guard 02CE2610")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == PR for l in fl):
        idx = max(i for i, l in enumerate(fl) if cells(l)[0] == RC)
        fl[idx + 1:idx + 1] = ["\t".join(r(RC, 0x18C0, 0x20938, "primitiveRenderer", PR, "a PrimitiveRendererD3D11 built in place by 006C8750; it ends the context", P, "V E", w=4)) + eol] + ["\t".join(x) + eol for x in PRROWS]
    open(FI, "wb").write("".join(fl).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]; out = []
    for l in tl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == RC and c[1].startswith("AT LEAST 0x18C0"):
            c[10] += " || EXTENT 2026-09-28 (OPUS, %s E): was '%s'" % (REC, c[1]); c[1] = CSIZE; out.append("\t".join(c) + e); continue
        out.append(l)
    if not any(cells(l)[0] == PR for l in out):
        ti = max(i for i, l in enumerate(out) if cells(l)[0] == RC); out[ti + 1:ti + 1] = ["\t".join(NEWT) + te]
    open(TY, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
PRr = {int(c[1], 16): c for c in F if c[0] == PR}
RCr = {int(c[1], 16): c for c in F if c[0] == RC}
check("W", PR in T and T[PR][1].startswith("AT LEAST 0x20938") and sum(int(c[2]) for c in PRr.values()) == 0x20938
      and PRr.get(0x208, [0] * 5)[4] == PS + "[4]" and PRr.get(8, [0] * 4)[3] == "vptrBatchMergerEvent"
      and RCr.get(0x18C0, [0] * 5)[3:5] == ["primitiveRenderer", PR] and T[RC][1].startswith("AT LEAST 0x221F8")
      and sum(int(c[2]) for c in RCr.values()) == 0x221F8,
      "PrimitiveRendererD3D11 (AT LEAST 0x20938) tiles to its reach; the context embeds it at +0x18C0 and its rows reach +0x221F8")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
