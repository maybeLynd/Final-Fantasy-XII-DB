"""sd62_registry_lists.py - what the lists headed in 01F2E330 and the structure at 01F2E780 chain (SWE2-ORACLE, 2026-09-30;
register SD-62, follow-up to OPUS's sd62-static-array-elements-0930). Static, over the certified image, through
Database/Tools/analysis-kit/gfz-scripts/retool.py. Nothing is executed.

Checks (each prints PASS/FAIL; the last line is FAILS n):
  L1  the link writer 00639160 (owner = rcx, descriptor = rdx) splices descriptor +0x50 into owner +0x10
  L2  every walker of root +0x10 turns a node back into a descriptor by subtracting 0x50 (element = class descriptor)
  L3  00639160 links a non-root owner's own +0x00 node into root +0x28, and skips the root itself
  L4  every image store to 01F2E330 / 01F2E338 (root +0x00 / +0x08) stores the root's own address (self-link only)
  L5  01F2E780 is a 0x30-byte tree header: its initialisers write exactly 01F2E780..01F2E7A8, all = 01F2E780
  L6  01F2E7B0 is a separate record (own initialiser 00635B80, own exit destructor 008AF430) holding the PWorld
      descriptor and "getInstanceCount" at its +0x10 / +0x18 - the regression that rejects reading those two
      slots as 01F2E780 +0x40 / +0x48
  L7  the tree's elements are class descriptors: insert 006388C0 keys descriptor +0x20 = hash(name), +0x28 = name,
      node = descriptor +0x08; remove 00638F00 passes descriptor +0x08; find 006311D0 reads node - 8 + 0x20
  L8  the name hash is the one 0059B430 / 00636280 use: seed 0x7B5, h = h*33 + (c & 0x1F)
  C1  control: the +0x50 link-writer scan finds 00639160 (the scan is sensitive to the shape it claims)
"""
import os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SC, SZ = T.R, T.scan(), T.sizes()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, " ".join(i.op_str.split()))


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def rip_target(i):
    for op in i.operands:
        if op.type == 3 and op.mem.base == T.RIP:
            return i.address + i.size + op.mem.disp
    return None


def has(a, s):
    return txt(a) == s


# L1 - 00639160(owner, desc): desc +0x50 goes after the parent's node when the parent (+0x78) has the same owner,
#      else before owner+0x10 (tail of the owner's list)
check("L1", all(has(a, s) for a, s in [
    (0x00639173, "mov rdi, rdx"), (0x00639179, "mov rbx, rcx"), (0x006391C2, "lea r14, [rbx + 0x10]"),
    (0x006391FF, "mov rdx, qword ptr [rdi + 0x78]"), (0x00639208, "cmp qword ptr [rdx + 0x70], rbx"),
    (0x00639212, "lea r8, [rdi + 0x50]"), (0x0063921A, "add rdx, 0x50"), (0x00639225, "mov qword ptr [r8 + 8], rdx"),
    (0x00639229, "mov qword ptr [rdx], r8"),
    (0x0063922E, "mov rcx, qword ptr [r14]"), (0x00639231, "lea rdx, [rdi + 0x50]"),
    (0x00639240, "mov qword ptr [rdx + 8], r14"), (0x00639244, "mov qword ptr [r14], rdx")]),
    "00639160 splices descriptor+0x50 into owner+0x10 (after the base class's node when the base has the same owner)")
cal = sorted(SC["calls"].get(0x00639160, ()))
print("      00639160 call sites: %d  %s" % (len(cal), " ".join("%08X@%08X" % tuple(x[:2]) for x in cal)))

# L2 - walkers of root+0x10 subtract 0x50 and use descriptor fields
check("L2", all(has(a, s) for a, s in [
    (0x008AF49A, "mov rbx, qword ptr [rip + 0x167ee9f]"), (0x008AF4B2, "add rbx, -0x50"),
    (0x008AF4C0, "mov rbx, qword ptr [rbx + 0x50]"), (0x008AF4E7, "call qword ptr [rax + 0x38]"),
    (0x00637AAA, "mov rbx, qword ptr [rip + 0x18f688f]"), (0x00637AD4, "lea rdx, [rbx - 0x50]"),
    (0x00637B11, "mov rax, qword ptr [rax + 0x78]"), (0x00637B45, "mov rdx, qword ptr [rdx + 0x50]"),
    (0x00638D00, "mov rax, qword ptr [rip + 0x18f5639]"), (0x00638D19, "lea rdi, [rax - 0x50]"),
    (0x00638D22, "mov rbx, qword ptr [rdi + 0x70]"),
    (0x00632D83, "lea rax, [rcx + 0x50]"), (0x00632D87, "mov qword ptr [rax], rax"), (0x00632DD6, "mov qword ptr [rcx + 0x70], rdx")])
      and all(rip_target(next(R.md.disasm(R.at(a, 16), a, 1))) == 0x01F2E340 for a in (0x008AF49A, 0x00637AAA, 0x00638D00)),
      "008AF490 / 00637A70 / 00638C90 walk [01F2E340] (root+0x10) as node-0x50 = descriptor (+0x70 owner, +0x78 base, vt+0x38)")

# L3 - owner's own +0x00 node into root+0x28, never the root
check("L3", all(has(a, s) for a, s in [
    (0x0063924C, "test rbp, rbp"), (0x00639256, "call 0x6373d0"), (0x0063925B, "cmp rbx, rax"),
    (0x00639265, "mov rcx, qword ptr [rax + 0x28]"), (0x00639269, "add rax, 0x28"), (0x0063926D, "mov qword ptr [rbx], rcx"),
    (0x00639270, "mov qword ptr [rbx + 8], rax"), (0x00639274, "mov qword ptr [rax], rbx"),
    (0x00638D6B, "cmp rbx, rbp"), (0x00638D86, "mov qword ptr [rbx], rbx")]),
    "a non-root owner whose descriptor list was empty is linked by its +0x00 node into root+0x28; 00638C90 unlinks it again")

# L4 - rip stores to root+0x00 / +0x08 carry only the root's own address
bad, n4 = [], 0
for f in SZ:
    ins = body(f)
    lea = {}
    for i in ins:
        t = rip_target(i)
        if i.mnemonic == "lea" and t is not None:
            lea[i.op_str.split(",")[0]] = t
        if i.mnemonic == "mov" and t in (0x01F2E330, 0x01F2E338) and i.op_str.startswith("qword ptr [rip"):
            n4 += 1
            src = i.op_str.split(", ")[-1]
            if lea.get(src) != 0x01F2E330:
                bad.append("%08X" % i.address)
check("L4", n4 >= 20 and not bad, "%d rip stores to 01F2E330/01F2E338, all of the root's own address (bad: %s)" % (n4, bad))

# L5 - 01F2E780: six qwords, all self
ini = [(a, txt(a)) for a in (0x00638F73, 0x00638F7A, 0x00638F81, 0x00638F88, 0x00638F8F, 0x00638F96)]
tg = sorted(rip_target(next(R.md.disasm(R.at(a, 16), a, 1))) for a, _ in ini)
st = struct.unpack("<6Q", R.at(0x01F2E780, 48))
check("L5", tg == [0x01F2E780 + 8 * k for k in range(6)] and all(s.endswith(", rdi") for _, s in ini)
      and has(0x00638F13, "lea rdi, [rip + 0x18f5866]") and set(st) == {0x01F2E780},
      "00638F00 initialises exactly 01F2E780..01F2E7A8, all = 01F2E780 (image bytes agree)")

# L6 - 01F2E7B0 is its own record
q7 = struct.unpack("<4Q", R.at(0x01F2E7B0, 32))
check("L6", all(has(a, s) for a, s in [
    (0x00635BF7, "mov qword ptr [rip + 0x18f8bb2], rcx"), (0x00635BFE, "mov qword ptr [rip + 0x18f8bb3], rax"),
    (0x00635BF0, "lea rcx, [rip + 0x26c2f19]"), (0x00635C0F, "mov qword ptr [rip + 0x26c2f02], rcx"),
    (0x008AF43D, "mov rcx, qword ptr [rip + 0x167f36c]"), (0x008AF470, "mov rcx, qword ptr [rip + 0x167f351]"),
    (0x00635C16, "lea rcx, [rip + 0x279813]")])
      and rip_target(next(R.md.disasm(R.at(0x00635BF0, 16), 0x00635BF0, 1))) == 0x02CF8A80 + 0x90
      and rip_target(next(R.md.disasm(R.at(0x008AF470, 16), 0x008AF470, 1))) == 0x01F2E7C8
      and rip_target(next(R.md.disasm(R.at(0x00635C16, 16), 0x00635C16, 1))) == 0x008AF430
      and q7[2] == 0x02CF8A80 and T.cstr(q7[3]) == "getInstanceCount",
      "01F2E7B0 = {link, link, PWorld descriptor 02CF8A80, \"getInstanceCount\", flags}; 00635B80 links it into the PWorld "
      "descriptor's +0x90 list and registers 008AF430, which unlinks it and frees +0x18 - not part of 01F2E780")

# L7 - the tree's elements are descriptors, node at +0x08, key +0x20 (hash) / +0x28 (name)
check("L7", all(has(a, s) for a, s in [
    (0x006388CA, "mov rsi, qword ptr [rcx + 0x30]"), (0x006388F2, "call 0x637440"),
    (0x00638976, "mov dword ptr [rbp + 0x20], edi"), (0x0063897C, "mov qword ptr [rbp + 0x28], rsi"),
    (0x00638980, "call 0x6314b0"), (0x006314BE, "lea rbx, [rdx + 8]"),
    (0x00638F3A, "lea rdx, [rbx + 8]"), (0x00638F52, "jmp 0x67fe20"),
    (0x006311EB, "lea r8, [rax - 8]"), (0x00631203, "lea rdx, [r8 + 0x20]"), (0x00631226, "mov rdx, qword ptr [rdx + 8]"),
    (0x00632D8E, "lea rax, [rcx + 8]"), (0x00632D99, "mov qword ptr [rax + 0x10], rax")]),
    "006388C0 inserts descriptor+0x08 keyed by (+0x20 hash, +0x28 name = +0x30 copy); 00638F00 removes +0x08; 006311D0 compares hash then name")

# L8 - hash
check("L8", all(has(a, s) for a, s in [(0x006388FA, "mov edi, 0x7b5"), (0x00638920, "and ecx, 0x1f"),
                                     (0x00638923, "imul edx, edx, 0x21"), (0x00636390, "mov edx, 0x7b5"),
                                     (0x006363A0, "and ecx, 0x1f"), (0x006363A3, "imul edx, edx, 0x21")]),
      "name hash h0 = 0x7B5, h = h*33 + (c & 0x1F), shared by 006388C0 (insert) and 00636280 (replace)")

# C1 - control for the +0x50 link-writer shape: lea r,[x+0x50] followed by a store of r
hits = []
for f in SZ:
    if not 0x00630000 <= f < 0x00640000:
        continue
    ins = body(f)
    for k, i in enumerate(ins):
        m = re.match(r"(\w+), \[(\w+) \+ 0x50\]$", i.op_str)
        if i.mnemonic != "lea" or not m or m.group(2) in ("rsp", "rbp", "rip"):
            continue
        for c in ins[k + 1:k + 14]:
            mm = re.match(r"qword ptr \[(\w+)(?: \+ 0x[0-9a-f]+)?\], (\w+)$", c.op_str)
            if c.mnemonic == "mov" and mm and mm.group(2) == m.group(1) and mm.group(1) != m.group(1):  # not a self-link
                hits.append((f, c.address))
                break
            if m.group(1) in {R.md.reg_name(r) for r in c.regs_access()[1]}:
                break  # the node register was redefined
fs = sorted(set(f for f, _ in hits))
check("C1", 0x00639160 in fs, "reflection-range (00630000-0063FFFF) +0x50 link writers: %s" % " ".join("%08X" % f for f in fs))
print("FAILS %d" % fails)
