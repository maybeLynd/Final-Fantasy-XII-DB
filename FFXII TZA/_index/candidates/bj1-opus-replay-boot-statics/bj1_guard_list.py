"""bj1_guard_list.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The input a READ-ONLY live snapshot
needs to answer BJ-1 (which of the 1,681 lazily-built statics a normal boot constructs).

  G1 the population, by probe.py's own rule: every `call 008092FC` (_Init_thread_header) and the guard its preceding
     `lea rcx, [rip + guard]` passes - 1,732 sites, 1,681 guards
  G2 the reading rule, from the bytes: the header stores -1 into a guard that is 0 (00809312 / 00809317); the footer
     stores ++epoch (008092B2 / 008092C5 inc / 008092C7 / 008092CD), the epoch being the .data dword 01F44850, 0x80000000 in the image.
     So in a live process a guard reads 0 = not built, 0xFFFFFFFF = being built, 0x80000001.. = built, and its value
     minus 0x80000000 is its build ORDER; and [01F44850] - 0x80000000 is how many thread-safe statics have been built
  G3 the replay's 19 attributions (result.json) are joined onto the list as the known lower bound
Writes bj1-guards.tsv with --write: guard_va, section, header_sites, replay_step (blank if the replay did not build it).
"""
import collections, hashlib, json, os, re, struct, sys
import capstone
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0").decode(),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def sec(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + max(vs, rs): return nm, (v - B - va + ro if v - B - va < rs else None)
    return "?", None
# a MAPPED image (virtual layout), as probe.py's B.img is: file offsets are not VA - base
size_img = struct.unpack_from("<I", d, pe + 24 + 56)[0]
img = bytearray(size_img); img[:0x1000] = d[:0x1000]
for nm_, vs_, va_, rs_, ro_ in SECS: img[va_:va_ + min(vs_, rs_)] = d[ro_:ro_ + min(vs_, rs_)]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
# G1 - probe.py's rule, verbatim in effect (image offsets = VA - 0x120000 for .text in this image)
text = next(s for s in SECS if s[0] == ".text"); tlo, thi = B + text[2], B + text[2] + text[3]
sites_of = collections.Counter(); sites = 0
for off in range(tlo - B, thi - B - 5):
    if img[off] == 0xE8 and off + 5 + struct.unpack_from("<i", img, off + 1)[0] + B == 0x8092FC:
        sites += 1; a = off + B
        for back in range(7, 60):
            ins = list(md.disasm(bytes(img[a - back - B:a - B]), a - back))
            if ins and ins[-1].address + ins[-1].size == a:
                for i in reversed(ins):
                    m = re.match(r"rcx, \[rip \+ (0x[0-9a-f]+)\]", i.op_str)
                    if i.mnemonic == "lea" and m:
                        sites_of[i.address + i.size + int(m.group(1), 16)] += 1
                        break
                break
check("G1", sites == 1732 and len(sites_of) == 1681, "%d header sites, %d guards" % (sites, len(sites_of)))
at = lambda a: next(md.disasm(bytes(img[a - B:a - B + 16]), a))
h1, h2, f1, f2, f3 = at(0x809312), at(0x809317), at(0x8092B2), at(0x8092C7), at(0x8092CD)
ep = f1.address + f1.size + int(re.search(r"0x[0-9a-f]+", f1.op_str).group(0), 16)
nm, eo = sec(ep)
check("G2", (h1.mnemonic, h1.op_str) == ("cmp", "dword ptr [rbx], 0") and (h2.mnemonic, h2.op_str) == ("or", "dword ptr [rbx], 0xffffffff")
      and f2.mnemonic == "mov" and f2.op_str.endswith("eax") and (f3.mnemonic, f3.op_str) == ("mov", "dword ptr [rbx], eax")
      and ep == 0x1F44850 and nm == ".data" and struct.unpack_from("<I", d, eo)[0] == 0x80000000,
      "header -1 while building; footer stores ++[%08X] (.data, image value 0x80000000)" % ep)
rep = json.load(open(os.path.join(HERE, "result.json"), encoding="utf-8"))
built = {int(k, 16): v[0] for k, v in rep["results"].get("guards", {}).items()}
check("G3", len(built) == 19 and all(g in sites_of for g in built), "the replay's %d built guards are all in the population" % len(built))
if "--write" in sys.argv:
    with open(os.path.join(HERE, "bj1-guards.tsv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("guard_va\tsection\theader_sites\treplay_step\n")
        for g in sorted(sites_of):
            fh.write("%08X\t%s\t%d\t%s\n" % (g, sec(g)[0], sites_of[g], built.get(g, "")))
    print("wrote bj1-guards.tsv")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
