"""OV-31 type-store evidence for WidgetSingleton02AEE4C0 (the 0xD8 title-asset widget).

SWE2-STRUCT, 2026-09-29.  Re-runnable, read-only, shipping image only (sha256 73461D08...).

    python ov31_title_asset.py            # all checks (census runs take a few minutes)
    python ov31_title_asset.py --quick    # instruction/pdata/table checks only, no census
    python ov31_title_asset.py --self-test

Checks
  S  every cited instruction decodes to the recorded text at the recorded address
  P  each cited site lies in the .pdata chain ROOT named for it (never the first fragment)
  J  00582860's jump-table arm for message 18 is 00582E81 (the arm that destroys the asset)
  X  the cell 02AEE4C0 is referenced at exactly nine sites, control 02AEE4D0 must be nonzero
  C  receiver census, cell seed, extent widened to 0x1000: type-area sites are exactly
     {00393A98 +C0/1B r, 0039450D +C0/4B r, 00393AA5 +D0/8B r}; nothing at +0xC4 or >= +0xD8
  O  receiver census, SEED=ctor 00394070 ARGREGS=1, extent 0x1000: type-area sites are exactly
     the seven own-handler sites; nothing at +0xC4 or >= +0xD8; below +0xC0 only the widget
     contract's attach entry 00244960 (+0x10 parent link, common header)
  K  POSITIVE CONTROL for the +0xC4 zero: the same tool on the sibling cell 02AEE4C8 does see
     +0xC4 accesses (0039435C, 0039436A, 003944E0), so a zero at +0xC4 is not the filter
--self-test flips one expectation per check family and requires the family to fail.
"""
import json
import os
import struct
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GFZ = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, GFZ)
import kit_paths as KP  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

EXE = KP.EXE
FUNCS = os.path.join(KP.WORK, "graph", "functions.tsv")
D = open(EXE, "rb").read()
PE = struct.unpack_from("<I", D, 0x3C)[0]
OPT = PE + 24
BASE = struct.unpack_from("<Q", D, OPT + 24)[0]
SOH = struct.unpack_from("<H", D, PE + 20)[0]
NSEC = struct.unpack_from("<H", D, PE + 6)[0]
SECS = [struct.unpack_from("<IIII", D, OPT + SOH + i * 40 + 8) for i in range(NSEC)]
MD = Cs(CS_ARCH_X86, CS_MODE_64)


def r2o(rva):
    for vs, va, rs, ro in SECS:
        if va <= rva < va + max(vs, rs):
            return ro + rva - va
    raise ValueError(hex(rva))


def insn(va):
    o = r2o(va - BASE)
    i = next(MD.disasm(D[o:o + 16], va))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


EXC_RVA, EXC_SZ = struct.unpack_from("<II", D, OPT + 112 + 3 * 8)
_eo = r2o(EXC_RVA)
PDATA = [struct.unpack_from("<III", D, _eo + 12 * i) for i in range(EXC_SZ // 12)]


def chain_root(va):
    rva = va - BASE
    hit = [e for e in PDATA if e[0] <= rva < e[1]]
    if not hit:
        return None
    e = hit[0]
    while True:
        uo = r2o(e[2])
        flags = D[uo] >> 3
        cnt = D[uo + 2]
        if not (flags & 4):
            return BASE + e[0]
        e = struct.unpack_from("<III", D, uo + 4 + ((cnt + 1) & ~1) * 2)


# (address, exact decoded text) - the cited instructions, widths included
SITES = [
    (0x0039448B, "cmp qword ptr [rip + 0x275a02d], 0"),        # creator guards 02AEE4C0
    (0x0039449F, "mov ecx, 0xd8"),                              # requested extent
    (0x003944A4, "call 0x244f50"),                              # widget allocator
    (0x00244F77, "cmp ecx, 0x120"),                             # pool eligibility
    (0x00244F90, "test dword ptr [rbx + 0x40], 0x4000"),        # pool slot busy bit
    (0x00244FB2, "call 0x2497b0"),                              # heap fallback after 112 busy slots
    (0x003940F5, "mov qword ptr [rip + 0x275a3c4], rbx"),       # msg1 publishes self
    (0x003940FC, "mov dword ptr [rbx + 0xc0], 0"),              # +C0 dword store
    (0x003940E3, "or dword ptr [rbx + 0xc0], 1"),               # +C0 dword OR 1 (msg16)
    (0x00393A98, "test byte ptr [rdx + 0xc0], 1"),              # consumer byte test
    (0x0039450D, "mov eax, dword ptr [rax + 0xc0]"),            # fsttl_initialize poll path
    (0x00394513, "and eax, 1"),
    (0x00394033, "mov qword ptr [rdi + 0xc8], rax"),            # +C8 qword store
    (0x00394097, "mov rcx, qword ptr [rbx + 0xc8]"),            # +C8 qword read (msg18)
    (0x00394050, "mov qword ptr [rdi + 0xd0], rax"),            # +D0 store
    (0x003940A8, "mov rcx, qword ptr [rbx + 0xd0]"),            # +D0 read (msg18)
    (0x003940B9, "mov qword ptr [rbx + 0xd0], 0"),              # +D0 clear
    (0x00393AA5, "mov rdx, qword ptr [rdx + 0xd0]"),            # consumer +D0 read
    (0x00394092, "jmp 0x5c5230"),                               # default arm
    (0x005C5230, "xor eax, eax"),                               # default stub body
    (0x005C5232, "ret"),
    (0x00394400, "mov rcx, qword ptr [rip + 0x275a0b9]"),       # destroy-if-present
    (0x0039440A, "jne 0x244f00"),
    (0x00394522, "cmp qword ptr [rip + 0x2759f97], rax"),       # present predicate
    (0x00582EAC, "call 0x394520"),
    (0x00582EB5, "call 0x394400"),
    (0x00394155, "mov rcx, qword ptr [rip + 0x275a364]"),       # 0xF0 sibling msg18 arm
    (0x00394161, "call 0x244f00"),
    (0x00511EC4, "call 0x394500"),                              # fsttl_initialize poll
    (0x00511ECD, "sete cl"),
    (0x0024505A, "call rax"),                                   # 00245020 sends {18}
    (0x00249456, "mov rcx, qword ptr [rcx + 8]"),               # batch owner notify sites
    (0x0024953B, "mov rcx, qword ptr [rcx + 8]"),
    (0x0024960B, "mov rcx, qword ptr [rdi + 8]"),
    (0x002495B7, "mov qword ptr [rax + 8], rcx"),               # batch records owner
]

ROOTS = {0x00393A98: 0x003939B0, 0x00393AA5: 0x003939B0, 0x003940E3: 0x00394070,
         0x00394097: 0x00394070, 0x00394033: 0x00393FF0, 0x00394155: 0x00394130,
         0x00582EB5: 0x00582860, 0x0024505A: 0x00245020, 0x0024960B: 0x002495C0,
         0x0024953B: 0x002494F0, 0x00511EC4: 0x00511EC0}

CELL_REFS = {0x00393A88, 0x003940D2, 0x003940F5, 0x00394155, 0x00394400,
             0x0039448B, 0x00394500, 0x00394522, 0x00394543}

CELL_TYPE_AREA = {(0xC0, 1, "00393A98"), (0xC0, 4, "0039450D"), (0xD0, 8, "00393AA5")}
OWN_TYPE_AREA = {(0xC0, 4, "003940E3"), (0xC0, 4, "003940FC"), (0xC8, 8, "00394033"),
                 (0xC8, 8, "00394097"), (0xD0, 8, "00394050"), (0xD0, 8, "003940A8"),
                 (0xD0, 8, "003940B9")}
CONTROL_C4 = {"0039435C", "0039436A", "003944E0"}
# Below +0xC0 the own seed may reach only the widget contract's own "attach to the manager"
# entry 00244960 (12 B, `cmp qword ptr [rdx+0x10], 0` = header parent link), entered with self
# in rdx from 00394121. That is common-header access, not a type-specific field.
OWN_HEADER_OK = {(0x10, 8, "00244960")}


def check_sites(sites):
    bad = [(a, t, insn(a)) for a, t in sites if insn(a) != t]
    for a, t, got in bad:
        print("  S FAIL %08X want %r got %r" % (a, t, got))
    return not bad


def check_roots(roots):
    bad = [(a, r, chain_root(a)) for a, r in roots.items() if chain_root(a) != r]
    for a, r, got in bad:
        print("  P FAIL %08X want root %08X got %s" % (a, r, got and "%08X" % got))
    return not bad


def check_jump(expect=0x00582E81):
    # 00582899 lea rcx,[image base]; 005828A0 mov eax,[rcx+rax*4+0x462F54]; index = msg-1
    tbl = BASE + 0x462F54
    arm = BASE + struct.unpack_from("<I", D, r2o(tbl + 4 * 17 - BASE))[0]
    ok = arm == expect and insn(0x005828A0) == "mov eax, dword ptr [rcx + rax*4 + 0x462f54]"
    if not ok:
        print("  J FAIL arm18 %08X" % arm)
    return ok


def run(cmd, env):
    e = dict(os.environ)
    e.update(env)
    return subprocess.run([sys.executable] + cmd, cwd=GFZ, env=e, capture_output=True, text=True).stdout


def check_xrefs(expect):
    out = run(["data_xref_scan.py", "--exe", EXE, "--funcs", FUNCS, "--addr", "0x02AEE4C0",
               "--control", "0x02AEE4D0", "--show", "100"], {})
    if "control passes" not in out:
        print("  X FAIL control did not pass")
        return False
    got = set()
    for ln in out.splitlines():
        p = ln.split()
        if len(p) > 2 and "[fn" in ln and len(p[0]) == 8:
            got.add(int(p[0], 16))
    if got != expect:
        print("  X FAIL refs", sorted("%08X" % g for g in got ^ expect))
    return got == expect


def census(cell, env):
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    env = dict(env, EMIT_JSON=path)
    run(["census_receiver_fixpoint.py", cell, "0", "0x1000"], env)
    d = json.load(open(path, encoding="utf-8"))
    os.remove(path)
    rows = set()
    for k, sites in d["sites"].items():
        dp, w = (int(x) for x in k.split(":"))
        for s in sites:
            rows.add((dp, w, s))
    return d["converged"], rows


def check_census(expect_cell, expect_own, control):
    ok = True
    conv, rows = census("0x02AEE4C0", {})
    area = {r for r in rows if r[0] >= 0xC0}
    if not conv or area != expect_cell:
        print("  C FAIL cell seed", conv, sorted(area ^ expect_cell))
        ok = False
    conv, rows = census("0x00394070", {"SEED": "ctor", "POLY": "0", "ARGREGS": "1"})
    area = {r for r in rows if r[0] >= 0xC0}
    below = {r for r in rows if r[0] < 0xC0} - OWN_HEADER_OK
    if not conv or area != expect_own or below:
        print("  O FAIL own seed", conv, sorted(area ^ expect_own), sorted(below))
        ok = False
    conv, rows = census("0x02AEE4C8", {})
    c4 = {s for dp, w, s in rows if dp == 0xC4}
    if not conv or not control <= c4:
        print("  K FAIL positive control +C4 on 02AEE4C8:", sorted(c4))
        ok = False
    return ok


def main():
    quick = "--quick" in sys.argv
    if "--self-test" in sys.argv:
        fired = {
            "S": not check_sites([(0x003940FC, "mov byte ptr [rbx + 0xc0], 0")]),
            "P": not check_roots({0x00393AA5: 0x00393A88}),
            "J": not check_jump(0x005828AC),
        }
        if not quick:
            fired["X"] = not check_xrefs(CELL_REFS - {0x00394400})
        print("self-test:", fired)
        sys.exit(0 if all(fired.values()) else 1)
    res = {"S": check_sites(SITES), "P": check_roots(ROOTS), "J": check_jump()}
    if not quick:
        res["X"] = check_xrefs(CELL_REFS)
        res["C/O/K"] = check_census(CELL_TYPE_AREA, OWN_TYPE_AREA, CONTROL_C4)
    for k, v in res.items():
        print("%-5s %s" % (k, "PASS" if v else "FAIL"))
    sys.exit(0 if all(res.values()) else 1)


if __name__ == "__main__":
    main()
