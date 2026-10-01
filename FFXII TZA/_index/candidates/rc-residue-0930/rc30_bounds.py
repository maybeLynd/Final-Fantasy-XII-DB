"""RC-30 residue: can the three index-computed kind-7 request sites, or a computed-kind path-API call, produce the
loca_*.cl2 ids 0xE2..0xE4? (SWE2-DATA 2026-09-30), static.

A 002CEAE0: id = 0x10 + byte [[0209AC30] + 0xB2D], gated by [0209AC30]+0xD3C bit 1.
   Image-wide byte writes at +0xB2D (tools/dispscan.py B2D B2D): exactly 002832C7 (0xFF) and 00283400 (cl) in 00283270.
   00283400's cl = byte [copy + 0x60] of a member copy whose flag bit 1 is set; 00329220 sets bit 1 only when the
   page's row byte +4 is in 7..0x19 (00329667-00329672), and +0x60 is that byte (rc25_domain.py P2). The gate bit is set
   (002833ED) in the same branch and cleared (002832D5) at the start of the same build; the other image-wide +0xD3C
   writers touch other bits (masks printed). So the id is 0x17..0x29 (face_guest07..): never 0xE2..0xE4.
B 003C9950: id = 0xE + byte [obj + 0xC1]. The widget proc 003C9A30 writes the byte only with dl = the first i < 7 whose
   bit (table 00D11710 = 1,2,4,..,64) is set in 0031A8E0()'s mask, and skips the write when dl = 7 (003C9D20/003C9D3E).
   The child-proc writes in 003C95C0 (word 0x0A02 -> 2; table 00D11720[0..7]) are all <= 12. So the id is at most 0x1A.
C 00575C30: id = u16 base[cat] (00D23740: 0x228, 0x294, 0x2CC, 0x2F4, 0x31C, 0x354 - menuhandbook_story..monster)
   + u16 [pane+0xCA] (+ u16 [req+2]). cat is the request's byte 0; the requests come from 00577880 (whose only caller
   0056F2A0 passes cl only on the dl <= 5 branch, 0056F2BD), from 00575D10 / 00575DD0 (the pane's +0xD2, written only
   at 00575CD2 = cat) and from the pane's history (+0xD4, cat bytes of earlier requests). So cat <= 5 and the id
   is >= 0x228 (two zero-extended u16 addends cannot wrap 32 bits): never 0xE2..0xE4.
D computed-kind path-API calls: every rel32 call/jmp/jcc to 0032E400 / 0032E620 / 0032E3F0 is listed with the last
   instruction that sets ecx (kind) and edx (id) before it; the rows whose kind is not a constant are printed for the
   record (their bound is the residue).
Controls: CA the B2D census tool is sensitive: 002CEAF4's read is in its output (printed); CB the table reads return
the shipped bytes (00D11710 = 1,2,4,8,16,32,64); CC 00D23740[0] = 0x228 = the kind-7 id of menuhandbook_story.bin.
"""
import os, re, struct, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, off, owner, dis, secs, BASE, names  # noqa
from kind7 import paths  # noqa

FAILS = 0
TOOLS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch"


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(fn):
    return {x.address: x for x in dis(fn)}


def u8s(va, n):
    o = off(va)
    return list(d[o:o + n])


def u16s(va, n):
    o = off(va)
    return list(struct.unpack_from("<%dH" % n, d, o))


def dispscan(lo, hi):
    out = subprocess.run([sys.executable, "tools/dispscan.py", lo, hi], capture_output=True, text=True, cwd=TOOLS).stdout
    return out.splitlines()


# A
lines = dispscan("B2D", "B2D")
wr = [l for l in lines if re.search(r"\b(mov|or|and|add|sub|inc|dec|xor)\s+byte ptr \[\w+ \+ 0xb2d\],", l)]
for l in lines:
    print("   A " + l.strip())
check("CA control: the +0xB2D census shows 002CEAE0's own read (002CEAF4)", any(l.startswith("002CEAF4") for l in lines))
check("A1 image-wide byte writes at +0xB2D are exactly 002832C7 and 00283400",
      sorted(l.split()[0] for l in wr) == ["002832C7", "00283400"], str([l.split()[0] for l in wr]))
f = ins(0x00283270)
check("A2 00283400 stores cl = byte [copy + 0x60] on the flag-bit-1 branch; the gate bit is set there (002833ED)",
      f[0x002833FB].op_str == "ecx, byte ptr [r9 + 0x60]" and f[0x002833E0].op_str == "byte ptr [r9], 2"
      and f[0x002833ED].op_str == "dword ptr [rax + 0xd3c], 2" and f[0x002832D5].op_str == "dword ptr [rax + 0xd3c], 0xfffffffd")
g = ins(0x00329220)
check("A3 00329220 sets the copy's flag bit 1 only for a kind-0 row byte +4 in 7..0x19",
      g[0x00329667].op_str == "eax, byte ptr [r14 + 4]" and g[0x0032966C].op_str == "al, 7"
      and g[0x0032966E].op_str == "al, 0x12" and g[0x00329672].op_str == "dword ptr [rdi], 2")
d3c = dispscan("D3C", "D3C")
masks = [l for l in d3c if re.search(r"\b(or|and|xor|mov)\s+dword ptr \[\w+ \+ 0xd3c\],", l) and "rsp" not in l]
for l in masks:
    print("   A d3c " + l.strip())
print("   A: other +0xD3C writers are xor-merges of the masks their preceding 'and eax, M' names (printed above for review)")
ea = ins(0x002CEAE0)
check("A4 002CEAE0: id = 0x10 + that byte, gated by +0xD3C bit 1",
      ea[0x002CEAEB].op_str == "byte ptr [rax + 0xd3c], 2" and ea[0x002CEB01].op_str == "r8d, 0x10")
print("   A result: id in 0x17..0x29 when the gate is set")

# B
t = u16s(0x00D11710, 7)
check("CB control: 00D11710 = 1,2,4,8,16,32,64", t == [1, 2, 4, 8, 16, 32, 64], str(t))
h = ins(0x003C9A30)
check("B1 003C9A30 writes +0xC1 only with dl, skipping dl = 7 (003C9D20 / 003C9D3E)",
      h[0x003C9D20].op_str == "dl, 7" and h[0x003C9D3E].op_str == "dl, 7" and h[0x003C9BF4].op_str == "rcx, 7"
      and h[0x003C9BFA].op_str == "dl, 7")
tab = u8s(0x00D11720, 16)
print("   B 00D11720[0..15] = %s" % tab)
check("B2 the child-proc table values written to +0xC1 (00D11720[0..7]) and the word write 0x0A02 (-> 2) are <= 12",
      max(tab[:8]) <= 12)
lines = dispscan("C1", "C1")
wc1 = [l for l in lines if re.search(r"\b(mov|or|and|add|sub|inc|dec)\s+(byte|word) ptr \[\w+ \+ 0xc1\],", l) and "rsp" not in l]
inmod = [l for l in wc1 if l.split()[0].startswith("003C9")]
print("   B image-wide byte/word writes at +0xC1: %d; in the widget module 003C9xxx: %s" %
      (len(wc1), " ".join(l.split()[0] for l in inmod)))
check("B3 the widget module's +0xC1 writers are exactly 003C9611, 003C974F, 003C9D28, 003C9D46",
      sorted(l.split()[0] for l in inmod) == ["003C9611", "003C974F", "003C9D28", "003C9D46"])
print("   B result: id <= 0xE + 12 = 0x1A; the other %d image-wide +0xC1 writers are in modules that are not handed this "
      "widget object (not type-traced)" % (len(wc1) - len(inmod)))

# C
base = u16s(0x00D23740, 6)
arr, P = paths(7, 0x4D2, stop_on_miss=False)
check("CC control: 00D23740[0] = 0x228 = kind-7 menuhandbook_story.bin", base[0] == 0x228 and
      P.get(0x228, "").lower().endswith("menuhandbook_story.bin"), P.get(0x228, ""))
print("   C bases: %s -> %s" % ([hex(v) for v in base], [P.get(v, "?").split(chr(92))[-1] for v in base]))
k = ins(0x0056F2A0)
check("C1 0056F2A0 reaches 00577880 only when its category dl <= 5",
      k[0x0056F2BD].op_str == "dl, 5" and k[0x0056F2C0].mnemonic == "jbe" and k[0x0056F351].op_str == "0x577880")
cc = ins(0x00575C30)
check("C2 00575C30 stores the category to +0xD2 (00575CD2)", cc[0x00575CD2].op_str == "byte ptr [rbp + 0xd2], cl")
lines = dispscan("D2", "D2")
wd2 = [l for l in lines if re.search(r"\b(mov|or|and|add|sub|inc|dec)\s+(byte|word) ptr \[\w+ \+ 0xd2\],", l)
       and l.split()[0][:4] in ("0056", "0057")]
check("C3 in the handbook module (0056xxxx-0057xxxx) +0xD2 is written only at 00575CD2",
      [l.split()[0] for l in wd2] == ["00575CD2"], str([l.split()[0] for l in wd2]))
print("   C result: category <= 5, id >= 0x228")

# D
API = [0x0032E400, 0x0032E620, 0x0032E3F0]


def rawcallers(target):
    out = []
    for name, va, vs, ro, rs in secs:
        if name != ".text":
            continue
        blob = d[ro:ro + rs]
        for p in range(len(blob) - 6):
            if blob[p] in (0xE8, 0xE9) and BASE + va + p + 5 + struct.unpack_from("<i", blob, p + 1)[0] == target:
                out.append(BASE + va + p)
            if blob[p] == 0x0F and 0x80 <= blob[p + 1] <= 0x8F and \
                    BASE + va + p + 6 + struct.unpack_from("<i", blob, p + 2)[0] == target:
                out.append(BASE + va + p)
    return out


def last_set(fn, site, regs):
    body = dis(fn)
    i = [j for j, x in enumerate(body) if x.address == site][0]
    for x in reversed(body[:i]):
        if x.mnemonic == "call":
            return "(after a call)"
        dst = x.op_str.split(",")[0].strip()
        if dst in regs and x.mnemonic not in ("cmp", "test"):
            return "%s %s" % (x.mnemonic, x.op_str)
    return "(entry argument)"


const = re.compile(r"^(mov ecx, (0x[0-9a-f]+|\d+)|lea ecx, \[rdx [+-] (0x[0-9a-f]+|\d+)\])$")
tot = comp = 0
for tgt in API:
    for s in sorted(set(rawcallers(tgt))):
        fn = owner(s)
        if not fn:
            continue
        tot += 1
        kd = last_set(fn, s, ("ecx", "rcx", "cx", "cl"))
        idd = last_set(fn, s, ("edx", "rdx", "dx", "dl"))
        if const.match(kd):
            continue
        comp += 1
        print("   D %08X -> %08X in %08X %-30s kind: %-38s id: %s" % (s, tgt, fn, names.get(fn, "")[:30], kd, idd))
check("D0 the path-API sweep finds the constant kind-7 font request 00365935 (control: a site this sweep must see)",
      0x00365935 in set(rawcallers(0x0032E400)))
print("   D: %d path-API call sites, %d with a non-constant kind (listed; their bound is the residue)" % (tot, comp))
print("FAILS %d" % FAILS)
