"""BL-6: do any two registered Phyre type names collide under the registry's name hash?

The registry key is h = 0x7B5; h = h*0x21 + (c & 0x1F) over the name at descriptor +0x30 (006388C0,
32-bit). The name is stored by the two base constructors 00632C90 and 00632D80 (`mov [rcx+0x30], r8`).
This census takes every direct call to either, walks back at most 16 instructions for the last
`lea r8, [rip+X]`, reads the C string at X, and groups the distinct names by hash.
"""
import struct, collections
import capstone

ROOT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work"
EXE = ROOT + r"\exe\FFXII_TZA.exe"
FUNCS = ROOT + r"\graph\functions.tsv"
BASE = 0x120000
TARGETS = {0x00632C90, 0x00632D80}

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, vs, ro, rs))
    o += 40


def off(va):
    rva = va - BASE
    for a, s, ro, rs in secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None


def h(name):
    v = 0x7B5
    for c in name:
        v = (v * 0x21 + (c & 0x1F)) & 0xFFFFFFFF
    return v


md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
sites = 0
unresolved = []
names = collections.defaultdict(set)   # name -> call sites
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try:
        a = int(p[0], 16); n = int(p[2])
    except (ValueError, IndexError):
        continue
    fo = off(a)
    if fo is None or a in TARGETS:
        continue
    code = d[fo:fo + n]
    hit = False
    for i in range(len(code) - 4):
        if code[i] in (0xE8, 0xE9) and a + i + 5 + struct.unpack_from("<i", code, i + 1)[0] in TARGETS:
            hit = True
            break
    if not hit:
        continue
    ins = list(md.disasm(code, a))
    for k, x in enumerate(ins):
        if x.mnemonic not in ("call", "jmp"):
            continue
        try:
            t = int(x.op_str, 16)
        except ValueError:
            continue
        if t not in TARGETS:
            continue
        sites += 1
        got = None
        for y in reversed(ins[max(0, k - 16):k]):
            ops = y.op_str.split(",")
            if ops[0].strip() in ("r8", "r8d"):
                if y.mnemonic == "lea" and "rip" in y.op_str:
                    disp = y.operands[1].mem.disp
                    got = y.address + y.size + disp
                break
        so = off(got) if got else None
        if so is None:
            unresolved.append(x.address)
            continue
        s = d[so:so + 256].split(b"\0")[0]
        names[s].add(x.address)

# Second pass. The template getters pass a name they were handed in rcx (they park it in a .bss slot and
# store it to descriptor +0x30 after construction). Resolve those through the getter's direct callers.
funcs = []
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try:
        funcs.append((int(p[0], 16), int(p[2])))
    except (ValueError, IndexError):
        pass
funcs.sort()


def owner(addr):
    import bisect
    i = bisect.bisect_right(funcs, (addr, 1 << 40)) - 1
    return funcs[i][0] if i >= 0 and funcs[i][0] <= addr < funcs[i][0] + funcs[i][1] else None


getters = {owner(u) for u in unresolved} - {None}
via_getter = 0
still = set(getters)
for a, n in funcs:
    fo = off(a)
    if fo is None:
        continue
    code = d[fo:fo + n]
    hit = False
    for i in range(len(code) - 4):
        if code[i] in (0xE8, 0xE9) and a + i + 5 + struct.unpack_from("<i", code, i + 1)[0] in getters:
            hit = True
            break
    if not hit:
        continue
    ins = list(md.disasm(code, a))
    for k, x in enumerate(ins):
        if x.mnemonic not in ("call", "jmp"):
            continue
        try:
            t = int(x.op_str, 16)
        except ValueError:
            continue
        if t not in getters:
            continue
        for y in reversed(ins[max(0, k - 16):k]):
            ops = y.op_str.split(",")
            if ops[0].strip() in ("rcx", "ecx"):
                if y.mnemonic in ("lea", "mov") and "rip" in y.op_str:
                    so = off(y.address + y.size + y.operands[1].mem.disp)
                    if so is not None and y.mnemonic == "mov":
                        # an initialised .data pointer to the name
                        so = off(struct.unpack_from("<Q", d, so)[0])
                    if so is not None:
                        s = d[so:so + 256].split(b"\0")[0]
                        names[s].add(x.address)
                        via_getter += 1
                        still.discard(t)
                break
print("# template getters %d  names recovered through their callers %d  getters with no named caller %d"
      % (len(getters), via_getter, len(still)))

print("# getter with no named caller: " + " ".join("%08X" % g for g in sorted(still)))
print("# sample names: " + ", ".join(sorted(x.decode("latin1") for x in names)[:12]))
byhash = collections.defaultdict(list)
for s in names:
    byhash[h(s)].append(s)
coll = {k: v for k, v in byhash.items() if len(v) > 1}
print("# call sites %d  resolved %d  unresolved %d" % (sites, sites - len(unresolved), len(unresolved)))
print("# distinct names %d  distinct hashes %d  colliding hashes %d" % (len(names), len(byhash), len(coll)))
# control: the hash ignores bits 5-7, so a case-folded duplicate would collide by construction
low = collections.defaultdict(list)
for s in names:
    low[bytes(c & 0x1F for c in s)].append(s)
print("# names equal after masking every byte to 5 bits: %d group(s)" % sum(1 for v in low.values() if len(v) > 1))
FILE_ONLY = """PShaderVertexProgram PShaderFragmentProgram PShaderFragmentProgramD3D11 PShaderGeometryProgram
PShaderGeometryProgramD3D11 PShaderComputeProgram PShaderProgramBase PShaderPassParameterLocationTypesBase
PShaderPassParameterLocationTypesConstantBuffer PTexture2DD3D11 PTextureCubeMapD3D11 PSamplerStateD3D11
PStreamInputLayoutD3D11 PDataBlockBufferD3D11 PIndexDataBlockBufferD3D11 PBase PClassDescriptor PContextSwitch
PNodeContext PMaterialSet PMeshSegmentContext PMeshInstanceSegmentContext PChar PInt32 PUInt8 PUInt16 PUInt32
PString PMatrix4 PMatrix4x3 PLightType PLODBlendType PLODMetricType PRenderDataType PSceneRenderPassType
PShadowCasterType PTextureFormatBase""".split()
present = [n for n in FILE_ONLY if n.encode() in names]
print("# file-side names (the 37 on the file-schema page) constructed in the image: %d -> %s"
      % (len(present), " ".join(present)))
hs = {h(s): s for s in names}
clash = [(n, hs[h(n.encode())].decode("latin1")) for n in FILE_ONLY
         if n.encode() not in names and h(n.encode()) in hs]
print("# file-side names absent from the image whose hash equals a constructed name's: %d %s" % (len(clash), clash))
print("hash\tnames")
for k in sorted(coll):
    print("%08X\t%s" % (k, " | ".join(sorted(x.decode("latin1") for x in coll[k]))))
if unresolved:
    print("# unresolved sites: " + " ".join("%08X" % u for u in unresolved[:40]))
import sys
if "--names" in sys.argv:
    for s in sorted(names):
        print("%s\t%08X\t%s" % (s.decode("latin1"), h(s), " ".join("%08X" % a for a in sorted(names[s]))))
