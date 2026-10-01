"""falsify_context_switch.py - falsification pass 1 on 22-Middleware-PhyreEngine/Shader-Variant-Selection/
the-context-switch-axes-and-the-variant-key.md (OPUS, 2026-09-30). Static; reads only the shipping image.

The expected values are the page's own prose (§2-§4); nothing is taken from its generated members table. Every value is
re-derived from the image: the object's name pointer and word count in .data, the vtable its installer stores, slot 2 of
that vtable, the deleting destructor's free size, the CRT initializer slots, the registrar's returns and each
evaluator's distinguishing constant.

X1 §2 eight singletons: +0x08 names the switch, +0x20 is its word count (3 for NUM_LIGHTS, 1 otherwise)
X2 §2 the object is 0x28 bytes: each vtable's slot 0 (deleting destructor) frees 0x28
X3 §3 the CRT initializer table 008C43E8-008C4420 holds the eight installers, and each installer calls the registrar
   006B8D20, adds the word count to 02E522E0 only on a zero return, installs its vtable and tail-jumps
X4 §3 006B8D20 walks the head 02E522D0 comparing +0x08, returns 0x11 with no name and 0x12 on a duplicate
X5 §3 the budget: the eight word counts sum to 10
X6 §4 each class's slot-2 evaluator is the address the page names; LOW_RES_PARTICLES inherits the base's, which reads +0x24
X7 §4 the evaluators' constants: SKINNING <= 0x78; INDICES_16BIT byte +0x4C == 0x0C; ORTHO float +0x6C >= 0.01;
   NUM_LIGHTS reads effect +0x00/+0x04/+0x70; SHADER_LOD_LEVEL reads +0x74; LOD_BLEND reads +0x40/+0x20/+0x30
X8 §4 NUM_LIGHTS packs (10n + 35) >> 5 << 2 bytes
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402
from capstone import x86 as X  # noqa: E402

at, md, ext = R.at, R.md, R.ext
results = []
PAGE = [  # object, name, words, evaluator (from §2's table and §4's list)
    (0x01F2EBC8, "NUM_LIGHTS", 3, 0x006B9120), (0x01F2EBF0, "LOD_BLEND", 1, 0x006B90A0),
    (0x01F2EC18, "INSTANCING_ENABLED", 1, 0x006B9070), (0x01F2EC40, "SHADER_LOD_LEVEL", 1, 0x006B93D0),
    (0x01F2EC68, "ORTHO_CAMERA", 1, 0x006B9410), (0x01F2EC90, "INDICES_16BIT", 1, 0x006B93A0),
    (0x01F2ECB8, "SKINNING_ENABLED", 1, 0x006B9450), (0x01F2ECE0, "LOW_RES_PARTICLES", 1, None)]
BASE_VT = 0x00D80EA8


def check(cid, ok, what):
    results.append((cid, ok))
    print("%-4s %-9s %s" % (cid, "SURVIVES" if ok else "BROKEN", what))


def u32(a):
    return struct.unpack("<I", at(a, 4))[0]


def u64(a):
    return struct.unpack("<Q", at(a, 8))[0]


def cstr(a):
    return at(a, 64).split(b"\0")[0].decode("latin-1")


def rip(i):
    for op in i.operands:
        if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def body(f, n=None):
    return list(md.disasm(at(f, n or ext.get(f, 0x100)), f))


def imm0(i):
    return i.operands[0].imm if i.operands and i.operands[0].type == X.X86_OP_IMM else None


# X3 (first: it yields the vtables and the word counts). The CRT slots, and each installer's four steps. The word
# count is not authored in .data (+0x20 is 0 there): the installer writes it, next to the budget add, on the zero branch
slots = [u64(0x008C43E8 + 8 * k) for k in range(8)]
inst, words = {}, {}
x3_bad = []
for k, (o, n, w, _) in enumerate(PAGE):
    f = slots[k]
    b = body(f, 0x80)
    b = b[:next((j for j, i in enumerate(b) if i.mnemonic == "jmp"), len(b) - 1) + 1]
    ix = {i.address: j for j, i in enumerate(b)}
    reg = next((j for j, i in enumerate(b) if i.mnemonic == "call" and imm0(i) == 0x006B8D20), None)
    zero = reg is not None and b[reg + 1].mnemonic == "test" and b[reg + 2].mnemonic in ("jne", "jnz")
    skip = imm0(b[reg + 2]) if zero else None
    branch = [i for i in b if zero and b[reg + 2].address < i.address < skip]
    add = [i for i in branch if rip(i) == 0x02E522E0 and i.mnemonic in ("add", "inc")]
    wr = [i for i in branch if rip(i) == o + 0x20 and i.mnemonic == "mov"]
    added = (add[0].operands[1].imm if add and add[0].mnemonic == "add" else 1) if add else None
    words[o] = wr[0].operands[1].imm if wr else None
    vt = [rip(i) for i in b if i.mnemonic == "lea" and rip(i) and 0x00D80000 <= rip(i) < 0x00D90000]
    store_vt = any(i.mnemonic == "mov" and rip(i) == o for i in b)
    inst[o] = vt[0] if vt else None
    if not (zero and add and wr and added == words[o] and vt and store_vt and b[-1].mnemonic == "jmp"):
        x3_bad.append((n, zero, bool(add), words[o], added, vt, store_vt))
check("X3", slots == [0x001670F0, 0x001670A0, 0x00167050, 0x001671E0, 0x00167230, 0x00167190, 0x00167280, 0x00167140] and not x3_bad,
      "slots %s; each installer: call 006B8D20, then only on a zero return add the word count to 02E522E0 and write it to "
      "+0x20; store its vtable over +0x00; tail-jump: %s" % (" ".join("%08X" % s for s in slots), "all eight" if not x3_bad else x3_bad))

# X1: names and the base vtable from .data; word counts as the installers write them
got = [(cstr(u64(o + 8)), words[o]) for o, *_ in PAGE]
data_vt = set(u64(o) for o, *_ in PAGE)
data_words = set(u32(o + 0x20) for o, *_ in PAGE)
check("X1", got == [(n, w) for _, n, w, _ in PAGE] and data_vt == {BASE_VT},
      "names (.data) and installer-written words %s; .data vtables %s (the base's is 00D80EA8); .data +0x20 %s" % (
          got, " ".join("%08X" % v for v in data_vt), sorted(data_words)))

# X2
dt = []
for o, n, *_ in PAGE:
    vt = inst.get(o)
    d = u64(vt) if vt else 0
    b = body(d, 0x60) if d else []
    frees28 = any(i.mnemonic == "mov" and i.op_str in ("edx, 0x28", "rdx, 0x28") for i in b)
    dt.append((n, "%08X" % d, frees28))
check("X2", all(x[2] for x in dt), "slot 0 (deleting destructor) passes 0x28: %s" % dt)

# X4: 0x11 is `lea eax, [r10 + 0x11]` right after `test r10, r10` on the name (so it is 0x11 exactly); 0x12 on a match
rb = body(0x006B8D20)
rx = {i.address: j for j, i in enumerate(rb)}
null_name = [i for i in rb if i.mnemonic == "lea" and i.op_str == "eax, [r10 + 0x11]"]
name_tested = any(i.mnemonic == "mov" and i.op_str == "r10, qword ptr [rcx + 8]" for i in rb) and any(i.op_str == "r10, r10" for i in rb)
dup = [i for i in rb if i.mnemonic == "mov" and i.op_str == "eax, 0x12"]
head = [i for i in rb if rip(i) == 0x02E522D0]
links = any(i.mnemonic == "mov" and i.op_str.startswith("qword ptr [r11 + 0x10]") for i in rb)
check("X4", null_name and name_tested and dup and len(head) >= 2 and links,
      "006B8D20: `test r10, r10` on +0x08 then `lea eax, [r10 + 0x11]` = 0x11 %s; `mov eax, 0x12` on a name match %s; "
      "head 02E522D0 read and written %d; links at +0x10 %s" % (bool(null_name), bool(dup), len(head), links))

# X5
check("X5", sum(words.values()) == 10, "installer-written word counts sum to %d" % sum(words.values()))

# X6
ev = []
base_ev = u64(BASE_VT + 16)
for o, n, w, e in PAGE:
    vt = inst.get(o)
    s2 = u64(vt + 16) if vt else None
    ev.append((n, "%08X" % (s2 or 0), (s2 == e) if e else (s2 == base_ev)))
base_reads24 = any("+ 0x24]" in i.op_str for i in body(base_ev, 0x30))
check("X6", all(x[2] for x in ev) and base_reads24, "slot 2 per class %s; base evaluator %08X reads +0x24: %s" % (ev, base_ev, base_reads24))


def txt(f):
    return " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in body(f))


# X7
sk, ix16, orth, lig, slod, lod = (txt(0x006B9450), txt(0x006B93A0), txt(0x006B9410), txt(0x006B9120), txt(0x006B93D0), txt(0x006B90A0))
orth_const = [u32(rip(i)) for i in body(0x006B9410) if rip(i) and i.mnemonic.startswith(("comiss", "ucomiss", "movss"))]
k = {
    "SKINNING 0x78": "0x78" in sk,
    "INDICES_16BIT +0x4C == 0x0C": "+ 0x4c], 0xc" in ix16,
    "ORTHO +0x6C vs 0.01": "+ 0x6c]" in orth and struct.unpack("<f", struct.pack("<I", 0x3C23D70A))[0] and 0x3C23D70A in orth_const,
    "NUM_LIGHTS effect +0x00/+0x04/+0x70": "+ 0x70]" in lig and "+ 4]" in lig,
    "SHADER_LOD +0x74": "+ 0x74]" in slod,
    "LOD_BLEND +0x40/+0x20/+0x30": all(x in lod for x in ("+ 0x40]", "+ 0x20]", "+ 0x30]")),
}
check("X7", all(k.values()), "%s (ORTHO's float constants %s)" % (k, [hex(c) for c in orth_const]))

# X8: (10n + 35) >> 5 << 2 in NUM_LIGHTS
pk = ("0x23" in lig) and ("shr" in lig) and (("lea" in lig and "*4" in lig) or "shl" in lig)
check("X8", pk, "NUM_LIGHTS carries +35 (0x23), a right shift and a x4: %s" % pk)

broken = [c for c, ok in results if not ok]
print("BROKEN %d: %s" % (len(broken), " ".join(broken) or "none"))
sys.exit(0)
