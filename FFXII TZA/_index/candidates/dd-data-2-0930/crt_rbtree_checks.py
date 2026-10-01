"""DD batch 2 checks for the two ordered-container pages (SWE2-DATA 2026-09-30), static, the shipping image.

MSVC std::_Tree page:
  M1 the node allocations: the three _Buynode bodies call the CRT allocator (the one beside the free 00210EB0) with
     ecx = 0x30 (00714860, 00714920) and 0x60 (0071F180), and each is reached from a find-or-create path that then
     calls the matching insert wrapper (006F1F60 -> 00712E60 -> 00714860, then 00713210 -> 00712F60; 006F1E00 ->
     00712F20 -> 00714920, then 007134D0; 0071CE10 -> 0071E3E0 -> 0071F180, then 0071EA80 -> 0071E500)
  M2 each insert's max_size constant is (2^64-1) // node_size - 1, the node size M1 allocates
EASTL rbtree page:
  E1 the insert 0016D840 makes no call, and holds inline copies of both rotations: the store-displacement signature of
     RBTreeRotateLeft 0016D780 (0, +0x10, +0x10, ..., +8, +0x10) and of RBTreeRotateRight 0016D7E0 (+8, +0x10, +0x10,
     ..., 0, +0x10) each occurs in it
  E2 00199DB0 is a caller of the family (it calls RBTreeDecrement 0016D720 and RBTreeInsert 0016D840), not one of the
     six member bodies
  E3 006B52A0 is not red-black code: it walks a singly linked child list from [parent+0x10] through [node+0],
     unlinks the node, stores the new parent at [node+8] and pushes the node on the new parent's list (a reparent over
     parent / first-child / next-sibling links). No rel32 call, jump or jcc reaches it and no qword or RVA holds it;
     its one reference is the lea at 006B49FF in the PScene::PNode reflection registrar 006B41A0, which stores it into
     the method-caller object at 02E51D60 (vtable 00D80700, RTTI PMethodCallerConcrete<PNode, void, PNode&>) right
     after the guarded block that registers the method name "addChild" (lea r8 at 006B4985) - PNode::addChild, called
     only through reflection
  E4 image-wide (bodies up to 20,000 bytes), only four bodies hold both rotation signatures: 0016D840, 0016DA60 and
     Phyre's own red-black tree 0067F700 / 0067F9D0; the insert is the one inlined EASTL copy outside the rotations
Controls:
  C1 the rotation-signature matcher finds RotateLeft in 0016D780 itself (positive) and nothing in 006B52A0 (negative)
  C2 the reference sweep finds the genuine lea at 006B4AD4 to its target (positive)
"""
import os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
import pe  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(fn):
    return {x.address: x for x in pe.dis(fn)}


def calls(fn):
    return [x.op_str for x in pe.dis(fn) if x.mnemonic == "call"]


ALLOC = 0x00210EC0
ok = True
for bn, size in ((0x00714860, 0x30), (0x00714920, 0x30), (0x0071F180, 0x60)):
    xs = pe.dis(bn)
    k = [i for i, x in enumerate(xs) if x.mnemonic == "call" and x.op_str == hex(ALLOC)]
    ok &= bool(k) and xs[k[0] - 1].op_str == "ecx, %s" % hex(size)
chain = ins(0x006F1F60), ins(0x006F1E00), ins(0x0071CE10)
ok &= "0x714860" in calls(0x00712E60) and "0x714920" in calls(0x00712F20) and "0x71f180" in calls(0x0071E3E0)
ok &= chain[0][0x006F21CB].op_str == "0x712e60" and chain[0][0x006F21E7].op_str == "0x713210"
ok &= chain[1][0x006F1EFA].op_str == "0x712f20" and chain[1][0x006F1F17].op_str == "0x7134d0"
ok &= chain[2][0x0071D07D].op_str == "0x71e3e0" and chain[2][0x0071D096].op_str == "0x71ea80"
ok &= "0x712f60" in calls(0x00713210) and "0x712f60" in calls(0x007134D0) and "0x71e500" in calls(0x0071EA80)
check("M1 the three _Buynode bodies allocate 0x30 / 0x30 / 0x60 and feed the matching inserts", ok)
c30 = ins(0x00712F60)[0x00712F6D].op_str
c60 = ins(0x0071E500)[0x0071E50D].op_str
check("M2 max_size constants = (2^64-1)//size - 1 for 0x30 and 0x60",
      int(c30.split(", ")[1], 16) == (2 ** 64 - 1) // 0x30 - 1 and int(c60.split(", ")[1], 16) == (2 ** 64 - 1) // 0x60 - 1,
      "%s / %s" % (c30, c60))


def qstores(fn):
    out = []
    for x in pe.dis(fn):
        m = re.match(r"qword ptr \[(\w+)(?: \+ (0x[0-9a-f]+|\d+))?\], \w+$", x.op_str)
        if x.mnemonic == "mov" and m:
            out.append(int(m.group(2), 0) if m.group(2) else 0)
    return out


def rot_hits(seq, first, last):
    n = 0
    for i in range(len(seq) - 4):
        if tuple(seq[i:i + 3]) == first:
            tail = seq[i + 3:i + 7]
            if any(tuple(tail[j:j + 2]) == last for j in range(len(tail) - 1)):
                n += 1
    return n


L = ((0, 0x10, 0x10), (8, 0x10))
R = ((8, 0x10, 0x10), (0, 0x10))
s_ins = qstores(0x0016D840)
nl, nr = rot_hits(s_ins, *L), rot_hits(s_ins, *R)
check("E1 0016D840 makes no call and holds inline RotateLeft and RotateRight copies",
      calls(0x0016D840) == [] and nl >= 1 and nr >= 1, "left-shaped %d, right-shaped %d" % (nl, nr))
check("C1 control: the matcher finds RotateLeft in 0016D780 and RotateRight in 0016D7E0, and nothing in 006B52A0",
      rot_hits(qstores(0x0016D780), *L) >= 1 and rot_hits(qstores(0x0016D7E0), *R) >= 1
      and rot_hits(qstores(0x006B52A0), *L) + rot_hits(qstores(0x006B52A0), *R) == 0)
MEMBERS = {0x0016D6D0, 0x0016D720, 0x0016D780, 0x0016D7E0, 0x0016D840, 0x0016DA60}
cs = calls(0x00199DB0)
check("E2 00199DB0 calls RBTreeDecrement and RBTreeInsert and is not a member",
      "0x16d720" in cs and "0x16d840" in cs and 0x00199DB0 not in MEMBERS)

# E3: 006B52A0
lo, hi, _ = pe.text_range()
d = pe.d
o0 = pe.off(lo)
T = 0x006B52A0
rel = []
for i in range(o0, o0 + (hi - lo) - 6):
    b = d[i]
    if b in (0xE8, 0xE9) and lo + (i - o0) + 5 + struct.unpack_from("<i", d, i + 1)[0] == T:
        rel.append(lo + i - o0)
    if b == 0x0F and 0x80 <= d[i + 1] <= 0x8F and lo + (i - o0) + 6 + struct.unpack_from("<i", d, i + 2)[0] == T:
        rel.append(lo + i - o0)
qh = d.count(struct.pack("<Q", T))
rh = d.count(struct.pack("<I", T - pe.BASE))
cands = pe.raw_rip_refs(T, T + 1)
genuine = []
for a, mn, op, tgt in cands:
    o = pe.owner(a)
    if o and a in ins(o):
        genuine.append(a)
body = pe.dis(T)
shape = (any(x.mnemonic == "cmp" and x.op_str == "rax, rdx" for x in body)
         and any(x.op_str == "rax, qword ptr [rax]" for x in body)
         and any(x.op_str == "qword ptr [rdx + 8], r9" for x in body)
         and any(x.op_str == "qword ptr [r9 + 0x10], rdx" for x in body)
         and not any(x.mnemonic == "call" for x in body))
def rtti(vt):
    col = struct.unpack_from("<Q", d, pe.off(vt - 8))[0]
    td = pe.BASE + struct.unpack_from("<I", d, pe.off(col + 12))[0]
    o = pe.off(td + 16)
    return d[o:d.index(bytes(1), o)].decode()


reg = ins(0x006B41A0)
name = pe.cstr(0x00D805D8)
check("E3 006B52A0 is a child-list reparent, reached only as PNode's reflected addChild (lea 006B49FF)",
      shape and rel == [] and qh == 0 and rh == 0 and genuine == [0x006B49FF]
      and reg[0x006B4985].op_str.startswith("r8, [rip") and name.startswith("addChild")
      and rtti(0x00D80700).startswith(".?AV?$PMethodCallerConcrete@VPNode@PScene@Phyre@@XAEAV123@@"),
      "rel32 %d, qword %d, rva %d, rip candidates %d (genuine %d)" % (len(rel), qh, rh, len(cands), len(genuine)))
ctl = [c for c in pe.raw_rip_refs(0x006B5CB0, 0x006B5CB1) if c[0] == 0x006B4AD4]
check("C2 control: the reference sweep finds the genuine lea at 006B4AD4", len(ctl) == 1 and 0x006B4AD4 in ins(0x006B41A0))
# E4: image-wide sweep for bodies holding BOTH rotation signatures (children +0/+8, parent +0x10). Bodies over
# 20,000 bytes are skipped (declared); the MSVC layout (parent +8) does not match this signature by construction.
both = []
for f, sz in pe.funcs.items():
    if sz > 20000:
        continue
    try:
        s = qstores(f)
    except Exception:
        continue
    if rot_hits(s, *L) and rot_hits(s, *R):
        both.append(f)
both.sort()
print("   bodies with both rotation shapes: " + ", ".join("%08X" % f for f in both))
check("E4 image-wide, only four bodies hold both rotation shapes: the EASTL insert 0016D840 and erase 0016DA60, and "
      "Phyre's own red-black tree 0067F700 / 0067F9D0 (parent-and-colour word at +0x10)",
      both == [0x0016D840, 0x0016DA60, 0x0067F700, 0x0067F9D0] and 0x0016D840 in both, "%d bodies" % len(both))
print("RESULT MSVC node sizes 0x30 / 0x60 corroborated at the allocation; the EASTL insert inlines both rotations; "
      "00199DB0 is a caller; 006B52A0 is PScene::PNode::addChild (a child-list reparent reached by reflection), not red-black code")
print("FAILS %d" % FAILS)
