"""sq1_dword0.py - SQ-1: the SeSep dword0 consumer the page names (00213140) is a UI font-text draw, not audio code
(FABLE, Claude Opus 5.5, 2026-09-28). Static.

  A1  00213140 is referenced once in the image: the qword at 00906DD0, slot 1 of DynGeoFontTextInstance's vtable 00906DC8.
      That vtable is installed only by 002130E0 (constructor) and 00213110 (slot 2), and the constructor's only caller is
      001E91F3. The +0x40..+0x4C that 00213140 passes to vft[+0x100] are four dwords that 00213520 copies in at
      001E924E from [r14 + 0x13A0]. DynGeoTextureInstance's slot 1 (001FB8E0) makes the same vft[+0x100] call on its rdx
      argument, so the call is the DynGeo family's interface
  A2  the SepAudioBank element (vtable 00907B48, stride 0x68) that the SeSep binder writes has a packed
      {u32 +0x40, u8 +0x44, u32 +0x45, u8 +0x49} block. Its fill 002190B0 copies +0x30/+0x34/+0x38/+0x3C as dwords, so
      they are not pointers. 00213140 reads +0x40/+0x44/+0x48/+0x4C as four dwords, which is a different shape
  A3  the unaligned dword at +0x45 is accessed at exactly 8 sites in the image: the binder's store 00222E53 and 7 in the
      bank copy / fill / insert family. None consumes it
  A4  in 00210000-00224000 every non-stack 32-bit read of [reg + 0x40] is either 00213140's (A1) or an element copy whose
      register is stored straight back to memory (SepAudioBank's 002190B0/00219170/00219240/002196A0, ShoutAudioBank's
      0021B8F0/0021BA60/0021BB20/0021BBF0/0021BFD0)
  A5  no SepAudioBank vtable slot (0-10) reads dword +0x40 or takes its address
  C1  control for A3/A4: the sweeps find the binder's own stores 00222E45 / 00222E53 and 00213140's read at 0021318A
  C2  control for A1: the raw scan finds the known slot-10 entry 00223540 at 00907B98
  P   population: image-wide 32-bit register reads of [reg + 0x40]; the 359 outside the region are not classified here (sq1_dword0.out)
"""
import os, re, struct, sys, collections
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []; o = pe + 24 + opt
for i in range(nsec):
    name = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); secs.append((name, va, rs, ra)); o += 40
def f2va(off):
    for name, va, rs, ra in secs:
        if ra <= off < ra + rs: return name, 0x120000 + va + off - ra
    return None, None
def rd(v, n):
    r = v - 0x120000
    for name, va, rs, ra in secs:
        if va <= r < va + rs: return d[ra + r - va: ra + r - va + n]
def qrefs(t):
    p = struct.pack("<Q", t); out = []; i = d.find(p)
    while i != -1:
        out.append(f2va(i)); i = d.find(p, i + 1)
    return out
body = collections.defaultdict(list); rows = []
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) == 3:
        a = int(p[0], 16); body[p[1]].append((a, p[2])); rows.append((a, p[1], p[2]))
for f in body: body[f].sort()
def calls_to(t): return sorted((f, a) for a, f, s in rows if re.match(r"(call|jmp) 0x%x$" % t, s))
# A1
r1 = qrefs(0x00213140)
vt_refs = sorted({f for a, f, s in rows if "=>00906DC8" in s})
setter = [s for a, s in body["00213520"]]
site = [s for a, s in body["001E8580"] if 0x001E9244 <= a <= 0x001E924E]
ok("A1", r1 == [(".rdata", 0x00906DD0)] and vt_refs == ["002130E0", "00213110"] and calls_to(0x2130E0) == [("001E8580", 0x001E91F3)]
   and calls_to(0x213520) == [("001E8580", 0x001E924E)] and setter[:8:2] == ["mov eax, dword ptr [rdx]", "mov eax, dword ptr [rdx + 4]", "mov eax, dword ptr [rdx + 8]", "mov eax, dword ptr [rdx + 0xc]"]
   and site[0] == "lea rdx, [r14 + 0x13a0]",
   "00213140's only qword reference: %s (DynGeoFontTextInstance vtable 00906DC8 slot 1); vtable installed by %s; ctor called at 001E91F3; +0x40..+0x4C from 00213520 at 001E924E, source [r14 + 0x13A0]" % (["%s %08X" % x for x in r1], vt_refs))
tex = [s for a, s in body["001FB8E0"]]
ok("A1b", any(re.match(r"call qword ptr \[r\w+ \+ 0x100\]$", x) for x in tex) and (".rdata", 0x00906DD0) in r1,
   "DynGeoTextureInstance slot 1 (001FB8E0) also calls vft[+0x100] on its argument")
# A2
fill = {a: s for a, s in body["002190B0"]}
want = {0x00219105: "mov eax, dword ptr [rdi + 0x30]", 0x0021910B: "mov eax, dword ptr [rdi + 0x34]", 0x00219111: "mov eax, dword ptr [rdi + 0x38]",
        0x00219117: "mov eax, dword ptr [rdi + 0x3c]", 0x0021911D: "mov eax, dword ptr [rdi + 0x40]", 0x00219123: "movzx eax, byte ptr [rdi + 0x44]",
        0x0021912A: "mov eax, dword ptr [rdi + 0x45]", 0x00219130: "movzx eax, byte ptr [rdi + 0x49]"}
draw = [s for a, s in body["00213140"] if 0x00213179 <= a <= 0x0021318A]
ok("A2", all(fill.get(a) == s for a, s in want.items()) and any("=>00907B48" in s for a, s in body["002196A0"])
   and draw == ["mov eax, dword ptr [rbx + 0x4c]", "mov rcx, rsi", "mov r10, qword ptr [rsi]", "mov r9d, dword ptr [rbx + 0x48]", "mov r8d, dword ptr [rbx + 0x44]", "mov edx, dword ptr [rbx + 0x40]"],
   "SepAudioBank block {u32 +0x40, u8 +0x44, u32 +0x45, u8 +0x49}, +0x30..+0x3C copied as dwords (002190B0); 00213140 reads four dwords +0x40/+0x44/+0x48/+0x4C")
# A3
s45 = [(a, f, s) for a, f, s in rows if re.search(r"dword ptr \[r\w+ \+ 0x45\]", s)]
COPY = {"00218F40", "00219000", "002190B0", "00219170", "00219240", "002196A0"}
ok("A3", len(s45) == 8 and [(a, f) for a, f, s in s45 if f not in COPY] == [(0x00222E53, "00222DC0")] and all(s.startswith("mov") for a, f, s in s45),
   "dword +0x45 sites: %s" % ["%08X %s" % (a, f) for a, f, s in s45])
# A4
SHOUT = {"0021B8F0", "0021BA60", "0021BB20", "0021BBF0", "0021BFD0"}
reg = [(a, f, s) for a, f, s in rows if 0x00210000 <= int(f, 16) < 0x00224000 and re.match(r"mov (e\w+|r\d+d), dword ptr \[r(?!sp)\w+ \+ 0x40\]$", s)]
def stored_back(f, a, s):
    r = re.match(r"mov (\w+),", s).group(1); ins = body[f]; i = next(k for k, (x, y) in enumerate(ins) if x == a)
    return any(re.match(r"mov dword ptr \[.*\], %s$" % r, y) for x, y in ins[i + 1:i + 3])
cls = collections.Counter("fonttext" if f == "00213140" else ("sep" if f in COPY else ("shout" if f in SHOUT else "OTHER")) for a, f, s in reg)
ok("A4", cls["OTHER"] == 0 and cls["fonttext"] == 1 and all(stored_back(f, a, s) for a, f, s in reg if f != "00213140"),
   "%d non-stack 32-bit reads of [reg + 0x40] in 00210000-00224000: %s; every copy read is stored back within two instructions" % (len(reg), dict(cls)))
# A5
slots = ["%08X" % struct.unpack_from("<Q", rd(0x00907B48 + 8 * k, 8))[0] for k in range(11)]
hits = [(f, s) for f in slots for a, s in body[f] if re.search(r"(dword ptr|lea r\w+,) \[r\w+ \+ 0x40\]", s) and "rsp" not in s]
ok("A5", slots[10] == "00223540" and not hits, "SepAudioBank slots %s: no dword +0x40 access or lea (%s)" % (slots, hits))
# controls
allw = {a for a, f, s in rows if re.search(r"ptr \[r\w+ \+ 0x4[05]\]", s)}
ok("C1", {0x00222E45, 0x00222E53, 0x0021318A} <= allw and any(a == 0x0021318A for a, f, s in reg), "the sweep finds the binder's stores 00222E45 / 00222E53 and 00213140's read 0021318A")
ok("C2", (".rdata", 0x00907B98) in qrefs(0x00223540), "the raw scan finds slot 10 (00223540) at 00907B98")
pop = [1 for a, f, s in rows if re.match(r"mov (e\w+|r\d+d), dword ptr \[r(?!sp)\w+ \+ 0x40\]$", s)]
print("P    population: %d non-stack 32-bit reads of [reg + 0x40] image-wide; %d in the region, %d outside not classified" % (len(pop), len(reg), len(pop) - len(reg)))
print("FAILS", fails); sys.exit(1 if fails else 0)
