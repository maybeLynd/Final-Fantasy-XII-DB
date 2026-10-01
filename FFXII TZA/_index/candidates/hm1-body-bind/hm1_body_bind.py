"""HM-1 (OPUS, 2026-09-27): how hc1006_03 gets a parent - it is c1006's replacement BODY, not an actor a script attaches.

  B1 data: highmodelreplace.bin's record c:3 (c1006) has key (-1,-1) and one pair C:22 at threshold 0; C:22 is
     hc1006_03 (entry 22 of the PS2 file list's kind 15) - so 0037CB90(c1006, b, c) returns hc1006_03 for every b, c
     and every non-negative story progress.
  B2 the bind poll 003409F0 (bindp 0x0C; the bindp2 family through 00342330 jmp 003409F0) asks 0037CB90 (00340A7F);
     a result < 0 leaves the request at mode 1 (00340A8A), a replacement goes to mode 2 and, once loaded, mode 3 (00340B03).
  B3 the result 00342640 (bindp; the bindp2 family through 00343760 jmp 00342640) sends mode 3 to 002E3110 with k = 4
     (003426B5 lea edx, [r8 + 4], r8 = 0); bindhoff 003460F0 does the same after its own 0037CB90 call (0034618A).
  B4 002E3110 k = 4 attaches the new body record as CHILD of the unit's own record with code 0x7FFF (002E3195 mov ebp,
     0x7fff; k = 2 likewise at 002E3219; 002E33E4..002E33EE -> 002EDAA0, which swaps its arguments into 0042F310(child, parent, code)), then sets
     binding state 1 on the own record (002E3466 lea edx, [r14 - 3]) and 2 on the +0x90 body record (002E3484 mov edx, 2).
  B5 002EDF90 is the only writer of +0x6C8 besides the reset, it is called only from 002E3110, and it is a state
     machine: 0 -> the request (002EDFCE); release 1 -> 3, 2 -> 4 (002EDFF9, 002EE00C); re-bind 3 -> 1, 4 -> 2.
  B6 the dirty pass 004215A0 turns code 0x7FFF into 004219C0(parent, -1, child) (00421664..0042166A), which reaches the
     bank wrapper 0046E640 (00421AC1) - the element's +0x08 / +0x0C parent writers.
  B7 003703A0 takes the mapped pose path only when the element's record has +0x6C8 == 2 (00370634) and +0xB0 != -1
     (00370647), and its second skeleton is the record reached through the element's +0x0C (00370512).
  B8 CharacterRenderRecord_ResetDefaults stores 0 (0041F775 xor esi, esi; esi not written again before 0041FB78).
  B9 the bind verb's model argument: the begin handler 0033F330 pops three values and resolves the third (0033F371 ->
     0033F378 call 002E9A60); 002E9A60 sends an id >= 0x1000000 to 00263F80, which indexes the table at [ctx + 0x100]
     (EBP section 12, the manifest) by id & 0xFFFFFF (00263F87, 00263F97). With PUSHI reading the int constant pool, this is
     how hm1-parent-writer/c22_bind.py resolves the four maps' bind arguments (it asserts the c:3 finding).
Every check is re-run on a mutant; the run fails unless each mutant is rejected. Static bytes + shipped data, not execution.
Usage: python hm1_body_bind.py [exe] [ps2data root]
"""
import copy, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
ROOT = Path(sys.argv[2] if len(sys.argv) > 2 else r"D:/FFXII_TZA_extract/ps2data")
BASE = 0x120000
FUNCS = {0x3409F0: 340, 0x342640: 163, 0x343760: 5, 0x342330: 5, 0x3460F0: 179, 0x2E3110: 997, 0x2EDAA0: 141,
         0x42F310: 151, 0x2EDF90: 179, 0x4215A0: 754, 0x4219C0: 0x200, 0x3703A0: 1262, 0x41F730: 1208,
         0x33F330: 222, 0x2E9A60: 46, 0x263F80: 35}


def load():
    d = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
    off = lambda v: next(v - BASE - va + ro for vs, va, rs, ro in secs if BASE + va <= v < BASE + va + rs)
    cs = Cs(CS_ARCH_X86, CS_MODE_64); ins = {}
    for a, size in FUNCS.items():
        for x in cs.disasm(d[off(a):off(a) + size], a):
            ins[x.address] = [x.mnemonic, x.op_str]
    # every rel32 call / jmp to 002EDF90 in .text, for B5
    text = [s for s in secs if s[1] == 0x1000][0]
    blob = d[text[3]:text[3] + text[2]]; tb = BASE + text[1]; sites = []
    for i in range(len(blob) - 5):
        if blob[i] in (0xE8, 0xE9) and tb + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] == 0x2EDF90:
            sites.append(tb + i)
    return ins, sites


def load_data():
    fl = (ROOT / "image/ff12/ch/bin/filelistlocalin.bin").read_bytes()
    s = struct.unpack_from("<38I", fl, 0)[15]; c = struct.unpack_from("<I", fl, s)[0]
    kind15 = [fl[o:fl.index(b"\0", o)].decode("latin1") if o else "" for o in struct.unpack_from("<%dI" % c, fl, s + 4)]
    b = (ROOT / "add_motion/highmodelreplace.bin").read_bytes()
    w = struct.unpack_from("<%di" % (len(b) // 4), b, 0); i = 0; recs = {}
    while w[i] != -1:
        rid, bb, cc = w[i] & 0xFFFFFFFF, w[i + 1], w[i + 2]; i += 3; pairs = []
        while w[i] != -1:
            pairs.append((w[i] & 0xFFFFFFFF, w[i + 1])); i += 2
        i += 1; recs.setdefault(rid, (bb, cc, pairs))
    return {"kind15": kind15, "recs": recs}


def check(ins, sites, data):
    def at(pc, m, o):
        assert ins.get(pc) == [m, o], (hex(pc), ins.get(pc), m, o)
    # B1
    C = lambda letter, n: (ord(letter) << 16) | n
    bb, cc, pairs = data["recs"][C("c", 3)]
    assert (bb, cc) == (-1, -1) and pairs == [(C("C", 22), 0)], ("B1", bb, cc, pairs)
    assert data["kind15"][22].lower().endswith("hc1006_03.cm"), ("B1 kind15[22]", data["kind15"][22])
    # B2
    at(0x342330, "jmp", "0x3409f0")
    at(0x340A62, "mov", "rcx, rbp"); at(0x340A65, "mov", "word ptr [rsi + 0xa], di")
    at(0x340A7F, "call", "0x37cb90"); at(0x340A86, "test", "eax, eax"); at(0x340A88, "jns", "0x340aa7")
    at(0x340A8A, "mov", "word ptr [rsi + 0xa], di")
    at(0x340ACF, "mov", "eax, 2"); at(0x340AD8, "mov", "word ptr [rsi + 0xa], ax")
    at(0x340B03, "mov", "eax, 3"); at(0x340B08, "mov", "word ptr [rsi + 0xa], ax")
    # B3
    at(0x343760, "jmp", "0x342640")
    at(0x342685, "cmp", "ax, 3"); at(0x3426A4, "xor", "r8d, r8d"); at(0x3426B5, "lea", "edx, [r8 + 4]"); at(0x3426B9, "call", "0x2e3110")
    at(0x346140, "call", "0x37cb90"); at(0x346179, "xor", "r8d, r8d"); at(0x34618A, "lea", "edx, [r8 + 4]"); at(0x34618E, "call", "0x2e3110")
    # B4
    at(0x2E317E, "cmp", "ecx, 1"); at(0x2E3195, "mov", "ebp, 0x7fff"); at(0x2E3219, "mov", "ebp, 0x7fff")
    at(0x2E33E4, "movzx", "r8d, word ptr [rbx]"); at(0x2E33E8, "movzx", "edx, bp"); at(0x2E33EB, "movzx", "ecx, word ptr [rsi]")
    at(0x2E33EE, "call", "0x2edaa0")
    at(0x2EDAAF, "movzx", "edi, r8w"); at(0x2EDAB3, "movzx", "esi, dx"); at(0x2EDAB6, "movzx", "ebp, cx")
    at(0x2EDB0F, "movzx", "r8d, si"); at(0x2EDB13, "movzx", "edx, bp"); at(0x2EDB16, "movzx", "ecx, di"); at(0x2EDB28, "jmp", "0x42f310")
    at(0x42F382, "mov", "word ptr [rcx + 0x3ce], dx"); at(0x42F389, "mov", "word ptr [rcx + 0x3cc], r8w")
    at(0x2E3444, "cmp", "r14d, 4"); at(0x2E345F, "lea", "edx, [r14 - 3]"); at(0x2E3466, "call", "0x2edf90")
    at(0x2E3477, "add", "rax, 0x90"); at(0x2E3484, "mov", "edx, 2"); at(0x2E3489, "jmp", "0x2e34cb")
    at(0x2E34CF, "movzx", "ecx, word ptr [rax]"); at(0x2E34D2, "call", "0x2edf90")
    # B5
    assert sites and all(0x2E3110 <= s < 0x2E3110 + 997 for s in sites), ("B5 callers", [hex(s) for s in sites])
    at(0x2EDFC9, "test", "r8d, r8d"); at(0x2EDFCE, "mov", "dword ptr [rcx + 0x6c8], edx")
    at(0x2EDFF3, "cmp", "r8d, 1"); at(0x2EDFF9, "mov", "dword ptr [rcx + 0x6c8], 3")
    at(0x2EE003, "cmp", "dword ptr [rcx + 0x6c8], 2"); at(0x2EE00C, "mov", "dword ptr [rcx + 0x6c8], 4")
    at(0x2EE01F, "cmp", "r8d, 3"); at(0x2EE025, "mov", "dword ptr [rcx + 0x6c8], 1")
    at(0x2EE02F, "cmp", "dword ptr [rcx + 0x6c8], 4"); at(0x2EE038, "mov", "dword ptr [rcx + 0x6c8], 2")
    # B6
    at(0x42164D, "mov", "eax, 0x7fff"); at(0x421658, "cmp", "bp, ax"); at(0x421664, "or", "edx, 0xffffffff")
    at(0x421661, "mov", "r8, rdi"); at(0x421667, "mov", "rcx, rsi"); at(0x42166A, "call", "0x4219c0")
    at(0x421AC1, "call", "0x46e640")
    # B7
    at(0x370512, "mov", "ecx, dword ptr [r14 + 0xc]"); at(0x370516, "call", "0x20e600")
    at(0x370634, "cmp", "dword ptr [rsi + 0x6c8], 2"); at(0x37063B, "jne", "0x370659")
    at(0x370647, "cmp", "dword ptr [r14 + 0xb0], -1")
    # B8
    at(0x41F775, "xor", "esi, esi"); at(0x41FB78, "mov", "dword ptr [rbx + 0x6c8], esi")
    # B9
    at(0x33F35B, "call", "0x267e10"); at(0x33F366, "call", "0x267e10"); at(0x33F371, "call", "0x267e10")
    at(0x33F376, "mov", "ecx, eax"); at(0x33F378, "call", "0x2e9a60")
    at(0x2E9A68, "cmp", "ecx, 0x1000000"); at(0x2E9A6E, "jb", "0x2e9a84"); at(0x2E9A70, "call", "0x2640c0"); at(0x2E9A7F, "jmp", "0x263f80")
    at(0x263F80, "mov", "r8, qword ptr [rcx + 0x100]"); at(0x263F87, "and", "edx, 0xffffff")
    at(0x263F92, "cmp", "edx, dword ptr [r8]"); at(0x263F97, "mov", "eax, dword ptr [r8 + rdx*4 + 4]")
    assert not any(v[1].startswith(("esi,", "rsi,")) and v[0] not in ("cmp", "test") for a, v in ins.items()
                   if 0x41F777 <= a < 0x41FB78), "B8 esi rewritten"
    return True


def main():
    ins, sites = load(); data = load_data()
    check(ins, sites, data); print("PASS B1-B8")
    muts = {
        "B1 key (1,0)": lambda i, s, d: d["recs"].__setitem__((ord("c") << 16) | 3, (1, 0, d["recs"][(ord("c") << 16) | 3][2])),
        "B1 threshold 1570": lambda i, s, d: d["recs"].__setitem__((ord("c") << 16) | 3, (-1, -1, [((ord("C") << 16) | 22, 1570)])),
        "B2 no replacement stays mode 2": lambda i, s, d: i.__setitem__(0x340A8A, ["mov", "word ptr [rsi + 0xa], ax"]),
        "B3 bindp result k=2": lambda i, s, d: i.__setitem__(0x3426B5, ["lea", "edx, [r8 + 2]"]),
        "B4 body gets state 0": lambda i, s, d: i.__setitem__(0x2E3484, ["xor", "edx, edx"]),
        "B4 no argument swap": lambda i, s, d: i.__setitem__(0x2EDB16, ["movzx", "ecx, bp"]),
        "B5 another caller": lambda i, s, d: s.append(0x46E000),
        "B6 0x7FFF bone path": lambda i, s, d: i.__setitem__(0x42166A, ["call", "0x3e5ad0"]),
        "B7 gate on state 1": lambda i, s, d: i.__setitem__(0x370634, ["cmp", "dword ptr [rsi + 0x6c8], 1"]),
        "B8 reset value 1": lambda i, s, d: i.__setitem__(0x41F800, ["mov", "esi, 1"]),
        "B9 id used as is": lambda i, s, d: i.__setitem__(0x263F97, ["mov", "eax, edx"]),
    }
    bad = 0
    for name, mut in muts.items():
        i2, s2, d2 = copy.deepcopy(ins), list(sites), copy.deepcopy(data); mut(i2, s2, d2)
        try:
            check(i2, s2, d2); print("MUTANT SURVIVED:", name); bad += 1
        except (AssertionError, KeyError):
            print("rejected:", name)
    print("FAILS", bad); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
