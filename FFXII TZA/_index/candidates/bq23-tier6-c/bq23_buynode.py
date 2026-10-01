r"""bq23_buynode.py [V140_INCLUDE] - BQ-23: six of the nine unmatched ContainerAllocatorSupport members are MSVC VS2015
STL node builders (FABLE, Claude Opus 5.5, 2026-09-27). Static; upstream = the VS2015 v140 headers (tier 6).

  B1 image: 00714860 / 007148C0 / 00714920 / 0071F180 call operator new 00210EC0 with a constant node size, test the
     result, call _invalid_parameter_noinfo_noreturn (IAT 008C2DA8) on null, and store the argument's head pointer
     into node +0 / +8 / +0x10 - _Tree::_Buynode0 (_Left, _Parent, _Right = _Myhead).
  B2 image: 0075EE00 / 00786980 do the same allocation and, when the next-pointer argument is null, point the node at
     itself before storing next / prev - _List::_Buynode0.
  B3 upstream (needs V140_INCLUDE): VS2015 _Allocate's normal block is '::operator new(_User_size);
     _SCL_SECURE_ALWAYS_VALIDATE(_Ptr != 0);', which in retail expands to _invalid_parameter_noinfo_noreturn(); xtree's
     _Buynode0 constructs _Left / _Parent / _Right from _Myhead(); list's _Buynode0 points at self when _Next is null.
  B4 sensitivity: EASTL's node creation (DoCopySubtree 001FC770) allocates through the allocator's virtual slot and
     never calls _invalid_parameter_noinfo_noreturn.
Exit 1 on any FAIL.
"""
import re, struct, sys, os
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
SIZES = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = l.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(f): return [x for x in cs.disasm(d[off(f):off(f) + SIZES[f]], f)]
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) if m else None
IPN = 0x8C2DA8
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
def alloc_fail_path(b):
    t = ["%s %s" % (x.mnemonic, x.op_str) for x in b]
    return any(re.fullmatch(r"mov ecx, 0x[0-9a-f]+", s) for s in t) and "call 0x210ec0" in t \
        and any(x.mnemonic == "call" and rip(x) == IPN for x in b)
def tree_node(b):
    t = ["%s %s" % (x.mnemonic, x.op_str) for x in b]
    return "mov qword ptr [rdx], rax" in t and "lea rcx, [rdx + 8]" in t and "lea rcx, [rdx + 0x10]" in t
T = [0x714860, 0x7148C0, 0x714920, 0x71F180]; L = [0x75EE00, 0x786980]
check("B1 the four _Tree::_Buynode0 bodies", all(alloc_fail_path(body(f)) and tree_node(body(f)) for f in T),
      str([(hex(f), alloc_fail_path(body(f)), tree_node(body(f))) for f in T]))
def list_node(b):
    t = ["%s %s" % (x.mnemonic, x.op_str) for x in b]
    return "test rbx, rbx" in t and "mov rbx, rax" in t and "mov rdi, rax" in t and "mov qword ptr [rax], rbx" in t
check("B2 the two _List::_Buynode0 bodies", all(alloc_fail_path(body(f)) and list_node(body(f)) for f in L),
      str([(hex(f), alloc_fail_path(body(f)), list_node(body(f))) for f in L]))
I = sys.argv[1] if len(sys.argv) > 1 else None
if I:
    x0 = open(os.path.join(I, "xmemory0"), encoding="latin-1").read(); yv = open(os.path.join(I, "yvals.h"), encoding="latin-1").read()
    xt = open(os.path.join(I, "xtree"), encoding="latin-1").read(); li = open(os.path.join(I, "list"), encoding="latin-1").read()
    check("B3 VS2015 headers: _Allocate validates the new'd pointer; _Buynode0 bodies match",
          re.search(r"_Ptr = ::operator new\(_User_size\);\s*_SCL_SECURE_ALWAYS_VALIDATE\(_Ptr != 0\);", x0) is not None
          and "_SCL_SECURE_INVALID_ARGUMENT_NO_ASSERT" in yv
          and re.search(r"_Buynode0\(\)[\s\S]{0,400}_Left\(_Pnode\)\), _Myhead\(\)\)[\s\S]{0,120}_Parent\(_Pnode\)\), _Myhead\(\)\)[\s\S]{0,120}_Right\(_Pnode\)\), _Myhead\(\)\)", xt) is not None
          and re.search(r"_Buynode0\(_Nodeptr _Next,\s*_Nodeptr _Prev\)[\s\S]{0,300}if \(_Next == _Nodeptr\(\)\)[\s\S]{0,120}_Next = _Pnode;\s*_Prev = _Pnode;", li) is not None)
else:
    print("SKIP  B3 (no V140_INCLUDE)")
e = body(0x1FC770)
check("B4 sensitivity: EASTL DoCopySubtree allocates through the allocator slot and never calls the invalid-parameter import",
      any(x.op_str == "qword ptr [rax + 0x10]" and x.mnemonic == "call" for x in e) and not any(x.mnemonic == "call" and rip(x) == IPN for x in e))
print("FAILS", fails); sys.exit(1 if fails else 0)
