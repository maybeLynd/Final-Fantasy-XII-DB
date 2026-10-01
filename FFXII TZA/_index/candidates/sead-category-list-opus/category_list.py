"""category_list.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only; nothing executed.
SQEX::Sd::Driver::Category (0x88): its +0x08..+0x37 is an embedded FixedList<0, SeadHandle> (a second base, not a node list
at +0x10 / +0x18), and its +0x60 / +0x70 are written by the initialiser. The store rows called +0x10 / +0x18 a node list's
head / tail, citing the config page, and +0x20..+0x37 unobserved.

  R  RTTI (complete-object locator -> type descriptor): 01CB4490 = Category@Driver@Sd@SQEX, 01CB4480 =
     FixedList<0, SeadHandle@Sd@SQEX>, 01CB4470 = SeadObject<0, 7>, 01CB4530 = FixedList<0, SeadHandle>::NODE
  K  THE CONSTRUCTOR 007A96F0 installs 01CB4490 at +0x00 and 01CB4480 at +0x08: +0x08 is a second base subobject
  D  DESTRUCTION: the list's own scalar deleting destructor (01CB4480 slot 0, 007A98E0) frees with size 0x30 (so the list is
     0x30 bytes), array-deletes its node array at list +0x10 through the element's vector deleting destructor (flag 3, count
     cookie at -8), and zeroes list +0x10..+0x28 and the dword at list +0x0C; Category's destructor 007A9760 does the same
     inline at Category +0x18..+0x30 / +0x14 after re-stamping +0x08 with 01CB4480, then stamps 01CB4470 on both vptrs
  I  INIT 007AA010 (this = the list): frees any old array, stores the capacity at +0x08, array-allocates capacity x 0x28 + 8
     with the count cookie, stamps every node {vtable 01CB4530, +0x08 0, +0x10 0, +0x18 -1, +0x1C 0, +0x20 0}, stores the
     array at +0x10 and calls the reset 007B6AA0
  S  RESET 007B6AA0 and INSERT 007AF380 (the same template's code; the reset is called by I): reset makes +0x18 the free head
     (= +0x10), gives node i index i (+0x18) and doubly links the free chain through +0x08 / +0x10 up to the capacity, and
     clears +0x20 / +0x28 / +0x0C; insert pops the free head, prepends the node to the active list (+0x20 head, +0x28 tail),
     ORs 1 into node +0x1C, stores the payload at node +0x20, increments +0x0C and returns node +0x18
  C  THE INITIALISER 007AA110 (this = Category): +0x60 = edx, +0x70 = a pointer into the ctgr element (element + its u16 at +2
     for version >= 2, element + 0x10 for version 1, else 0), +0x78 = r9 + 1 volume ramps, +0x7C = 2 pitch ramps, then
     Init(element u16 +4) on Category + 0x08 (007AA2EF lea rcx, [rbx + 8]); its caller 007AAA40 passes edx = ebx, the loop
     index over the table slots (007AAB5F), so +0x60 is the Category's own table index
  U  USERS (added the same day, before publication; the first draft would have written +0x64 as an unobserved span): 007AA680
     increments the dword +0x64 and on 0 -> 1 calls handle slot +0x18 on every listed handle whose category byte equals +0x60,
     storing its float at +0x68; 007AA3E0 decrements it clamped at 0 (1 -> 0 calls slot +0x20); 007A9A10 (this = rcx, kept in
     rdi / [rsp+0x58]) replays slot +0x18 with +0x68 while +0x64 > 0; 007AA770 counts +0x68 down to 0.0 and consumes the bytes
     +0x50 / +0x51, which 007AA540 / 007AA530 set with the volume / pitch masters. Every walk starts at Category +0x28, the
     list's active head, and follows node +0x10 while node +0x1C bit 0 is set - an independent read of the list layout
  W  REGRESSION (FAILS before): SeadFixedListSeadHandle30 (0x30) and SeadFixedListSeadHandleNode28 (0x28) in the store; Category
     +0x08 one embedded list row replacing four; +0x50 split into two bytes; +0x60 split (categoryIndex60 + int32 +0x64); +0x68
     float; +0x70 the element pointer
Not claimed: the SeadHandle payload's encoding (the page reads {u8 kind, u16 nodeIdx, u32 serial} on other lists), what
Category +0x70 is read for, who inserts into a Category's list, what handle slots +0x18 / +0x20 do, or +0x68's units.
Usage: python category_list.py [--patch]
"""
import hashlib, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def dis(lo, hi): return {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
def has(lo, hi, pairs):
    A = dis(lo, hi); miss = [hex(a) for a, v in pairs if A.get(a) != v]
    if miss: print("   missing", miss)
    return not miss
def rip(a, size, disp): return a + size + disp
def rtti(vt):
    col = struct.unpack_from("<Q", d, off(vt - 8))[0]; td = struct.unpack_from("<I", d, off(col + 0xC))[0]
    o = off(B + td + 0x10); return d[o:d.index(b"\0", o)].decode()
names = {v: rtti(v) for v in (0x1CB4490, 0x1CB4480, 0x1CB4470, 0x1CB4530)}
check("R", names == {0x1CB4490: ".?AVCategory@Driver@Sd@SQEX@@", 0x1CB4480: ".?AV?$FixedList@$0A@VSeadHandle@Sd@SQEX@@@Sd@SQEX@@",
                     0x1CB4470: ".?AV?$SeadObject@$0A@$07@Sd@SQEX@@", 0x1CB4530: ".?AUNODE@?$FixedList@$0A@VSeadHandle@Sd@SQEX@@@Sd@SQEX@@"},
      "RTTI: %s" % names)
check("K", has(0x7A96F0, 0x7A9752, [(0x7A96F0, ("lea", "rax, [rip + 0x150ad99]")), (0x7A96F7, ("mov", "qword ptr [rcx], rax")),
                                   (0x7A96FA, ("lea", "rax, [rip + 0x150ad7f]")), (0x7A9701, ("mov", "qword ptr [rcx + 8], rax"))])
      and rip(0x7A96F0, 7, 0x150AD99) == 0x1CB4490 and rip(0x7A96FA, 7, 0x150AD7F) == 0x1CB4480,
      "Category's constructor: +0x00 = 01CB4490, +0x08 = 01CB4480")
check("D", has(0x7A98E0, 0x7A9977, [(0x7A98F9, ("mov", "rcx, qword ptr [rcx + 0x10]")), (0x7A9902, ("cmp", "qword ptr [rcx - 8], 0")),
                                   (0x7A990C, ("mov", "edx, 3")), (0x7A9911, ("call", "qword ptr [rax]")), (0x7A9920, ("mov", "qword ptr [rbx + 0x10], rax")),
                                   (0x7A992C, ("mov", "qword ptr [rbx + 0x28], rax")), (0x7A9930, ("mov", "dword ptr [rbx + 0xc], eax")),
                                   (0x7A995F, ("mov", "edx, 0x30")), (0x7A9964, ("call", "0x16d6a0"))])
      and struct.unpack_from("<Q", d, off(0x1CB4480))[0] == 0x7A98E0
      and has(0x7A9760, 0x7A9816, [(0x7A97BD, ("mov", "rcx, qword ptr [rbx + 0x18]")), (0x7A97C1, ("lea", "rax, [rip + 0x150acb8]")),
                                   (0x7A97C8, ("mov", "qword ptr [rbx + 8], rax")), (0x7A97EF, ("mov", "qword ptr [rbx + 0x18], rax")),
                                   (0x7A97FB, ("mov", "qword ptr [rbx + 0x30], rax")), (0x7A97FF, ("mov", "dword ptr [rbx + 0x14], eax")),
                                   (0x7A9809, ("mov", "qword ptr [rbx + 8], rax")), (0x7A980D, ("mov", "qword ptr [rbx], rax"))])
      and rip(0x7A97C1, 7, 0x150ACB8) == 0x1CB4480 and rip(0x7A9802, 7, 0x150AC67) == 0x1CB4470,
      "the list's deleting destructor frees 0x30 and array-deletes +0x10; Category's destructor does it inline at +0x18..+0x30 / +0x14")
check("I", has(0x7AA010, 0x7AA106, [(0x7AA075, ("mov", "dword ptr [rdi + 8], ebx")), (0x7AA087, ("mov", "eax, 0x28")), (0x7AA08C, ("mul", "rbx")),
                                   (0x7AA093, ("add", "rax, 8")), (0x7AA0AB, ("mov", "qword ptr [rax], rbx")), (0x7AA0BA, ("lea", "rdx, [rip + 0x150a46f]")),
                                   (0x7AA0C1, ("mov", "qword ptr [rax], rdx")), (0x7AA0C4, ("mov", "qword ptr [rax + 8], rbp")), (0x7AA0C8, ("mov", "qword ptr [rax + 0x10], rbp")),
                                   (0x7AA0CC, ("mov", "dword ptr [rax + 0x18], esi")), (0x7AA0CF, ("mov", "dword ptr [rax + 0x1c], ebp")),
                                   (0x7AA0D2, ("mov", "qword ptr [rax + 0x20], rbp")), (0x7AA0D6, ("lea", "rax, [rax + 0x28]")),
                                   (0x7AA0E5, ("mov", "qword ptr [rdi + 0x10], rcx")), (0x7AA0EC, ("call", "0x7b6aa0"))])
      and rip(0x7AA0BA, 7, 0x150A46F) == 0x1CB4530,
      "Init: capacity at +0x08, capacity x 0x28 + 8 with the cookie, nodes {01CB4530, 0, 0, -1, 0, 0}, array at +0x10, then reset 007B6AA0")
check("S", has(0x7B6AA0, 0x7B6AFA, [(0x7B6AA0, ("mov", "rax, qword ptr [rcx + 0x10]")), (0x7B6AAA, ("mov", "qword ptr [rcx + 0x18], rax")),
                                   (0x7B6AB1, ("cmp", "dword ptr [rcx + 8], edx")), (0x7B6AC4, ("mov", "dword ptr [r9 + rax + 0x18], edx")),
                                   (0x7B6AD0, ("mov", "qword ptr [r10 + 8], r8")), (0x7B6AD9, ("mov", "qword ptr [r8 + 0x10], r10")), (0x7B6ADF, ("add", "r9, 0x28")),
                                   (0x7B6AEB, ("mov", "qword ptr [rcx + 0x20], r11")), (0x7B6AF1, ("mov", "qword ptr [rcx + 0x28], r11")), (0x7B6AF5, ("mov", "dword ptr [rcx + 0xc], r11d"))])
      and has(0x7AF416, 0x7AF481, [(0x7AF416, ("mov", "rax, qword ptr [r9 + 0x10]")), (0x7AF41A, ("mov", "qword ptr [rcx + 0x18], rax")),
                                   (0x7AF426, ("mov", "qword ptr [rcx + 0x28], r9")), (0x7AF44C, ("mov", "qword ptr [rcx + 0x20], r9")),
                                   (0x7AF450, ("or", "dword ptr [r9 + 0x1c], 1")), (0x7AF455, ("mov", "qword ptr [r9 + 0x20], r8")),
                                   (0x7AF459, ("inc", "dword ptr [rcx + 0xc]")), (0x7AF461, ("mov", "eax, dword ptr [r9 + 0x18]"))]),
      "reset: free head = nodes, index i, free chain through +0x08/+0x10, head/tail/count cleared; insert: pop, prepend, flags |= 1, payload +0x20, count++")
check("C", has(0x7AA110, 0x7AA313, [(0x7AA128, ("mov", "dword ptr [rcx + 0x60], edx")), (0x7AA13E, ("movzx", "eax, word ptr [rcx + 2]")),
                                   (0x7AA149, ("lea", "rax, [rcx + 0x10]")), (0x7AA156, ("mov", "qword ptr [rbx + 0x70], rax")),
                                   (0x7AA15E, ("mov", "dword ptr [rbx + 0x7c], 2")), (0x7AA165, ("mov", "dword ptr [rbx + 0x78], eax")),
                                   (0x7AA2E3, ("movzx", "ecx, word ptr [rax + 4]")), (0x7AA2EF, ("lea", "rcx, [rbx + 8]")), (0x7AA2F3, ("call", "0x7aa010"))])
      and has(0x7AAB50, 0x7AAB8A, [(0x7AAB5F, ("mov", "edx, ebx")), (0x7AAB65, ("call", "0x7aa110")), (0x7AAB7D, ("inc", "ebx")), (0x7AAB7F, ("add", "rdi, 8"))]),
      "007AA110: +0x60 = edx (007AAA40's slot index ebx), +0x70 = element pointer, +0x78 / +0x7C ramp counts, Init(element +4) on +0x08")
check("U", has(0x7AA680, 0x7AA76B, [(0x7AA686, ("cmp", "dword ptr [rcx + 0x64], 0")), (0x7AA695, ("jne", "0x7aa75b")), (0x7AA6AE, ("mov", "rbx, qword ptr [rbx + 0x28]")),
                                   (0x7AA6C0, ("mov", "rax, qword ptr [rbx + 0x20]")), (0x7AA718, ("cmp", "eax, dword ptr [rsi + 0x60]")), (0x7AA72A, ("call", "qword ptr [rax + 0x18]")),
                                   (0x7AA72D, ("test", "byte ptr [rbx + 0x1c], 1")), (0x7AA733, ("mov", "rbx, qword ptr [rbx + 0x10]")),
                                   (0x7AA741, ("inc", "dword ptr [rsi + 0x64]")), (0x7AA74B, ("movss", "dword ptr [rsi + 0x68], xmm6")), (0x7AA75B, ("inc", "dword ptr [rcx + 0x64]"))])
      and has(0x7AA3E0, 0x7AA4C5, [(0x7AA3E6, ("cmp", "dword ptr [rcx + 0x64], 1")), (0x7AA48A, ("call", "qword ptr [rax + 0x20]")),
                                   (0x7AA4A6, ("add", "dword ptr [rsi + 0x64], -1")), (0x7AA4B7, ("cmovs", "eax, ecx")), (0x7AA4BA, ("mov", "dword ptr [rsi + 0x64], eax"))])
      and has(0x7A9C74, 0x7A9CC1, [(0x7A9C74, ("mov", "rdi, qword ptr [rsp + 0x58]")), (0x7A9CA8, ("cmp", "dword ptr [rdi + 0x64], 0")), (0x7A9CAC, ("jle", "0x7a9cc1")),
                                   (0x7A9CB6, ("movss", "xmm1, dword ptr [rdi + 0x68]")), (0x7A9CBE, ("call", "qword ptr [rax + 0x18]"))])
      and has(0x7A9A3B, 0x7A9A43, [(0x7A9A3B, ("mov", "rdi, rcx")), (0x7A9A3E, ("mov", "qword ptr [rsp + 0x58], rcx"))])
      and has(0x7AA79A, 0x7AA880, [(0x7AA79A, ("movzx", "r15d, byte ptr [rcx + 0x50]")), (0x7AA79F, ("xor", "r12d, r12d")), (0x7AA7A5, ("mov", "byte ptr [rcx + 0x50], 0")),
                                   (0x7AA805, ("movzx", "r14d, byte ptr [rsi + 0x51]")), (0x7AA80D, ("mov", "byte ptr [rsi + 0x51], r12b")),
                                   (0x7AA865, ("movss", "xmm1, dword ptr [rsi + 0x68]")), (0x7AA86D, ("subss", "xmm1, xmm2")), (0x7AA874, ("movss", "dword ptr [rsi + 0x68], xmm1")),
                                   (0x7AA87B, ("mov", "dword ptr [rsi + 0x68], r12d"))])
      and has(0x7AA530, 0x7AA54C, [(0x7AA530, ("movss", "dword ptr [rcx + 0x4c], xmm1")), (0x7AA537, ("mov", "byte ptr [rcx + 0x51], 1")),
                                   (0x7AA540, ("movss", "dword ptr [rcx + 0x48], xmm1")), (0x7AA547, ("mov", "byte ptr [rcx + 0x50], 1"))]),
      "users: 007AA680 increments the dword +0x64 (0 -> 1 calls handle slot +0x18 on each listed handle of this category and stores its float at +0x68), "
      "007AA3E0 decrements it clamped at 0 (1 -> 0 calls slot +0x20), 007A9A10 replays slot +0x18 with +0x68 while +0x64 > 0, 007AA770 counts +0x68 down to 0.0; "
      "+0x50 / +0x51 are separate bytes set by 007AA540 / 007AA530 with the masters and consumed by 007AA770; the walks start at Category +0x28 (the list's active head)")
REC = "_index/candidates/sead-category-list-opus/category_list.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
PV, PB, DU = ("TYPE RESOLVED", "PROVEN"), ("TYPE RESOLVED", "PROBABLE"), ("DISCOVERED", "UNKNOWN")
TL, TN = "SeadFixedListSeadHandle30", "SeadFixedListSeadHandleNode28"
NEW = [(TL, 0x00, 8, "vtable", "void*", "01CB4480 (RTTI FixedList<0, SeadHandle>); slot 0 = 007A98E0, the scalar deleting destructor, sized free 0x30", PV),
       (TL, 0x08, 4, "capacity", "int32", "the node count Init (007AA010) allocates; the reset walks node i < capacity (007B6AB1)", PV),
       (TL, 0x0C, 4, "count", "int32", "active nodes: insert increments it (007AF459), reset and Init clear it", PV),
       (TL, 0x10, 8, "nodes", TN + "*", "the node array, capacity x 0x28 after an 8-byte count cookie (Init 007AA0AB..007AA0E5); array-deleted by the destructor through the element's vector deleting destructor", PV),
       (TL, 0x18, 8, "freeHead", TN + "*", "the free chain head: reset sets it to nodes (007B6AAA), insert pops it (007AF416 / 007AF41A)", PV),
       (TL, 0x20, 8, "activeHead", TN + "*", "the active list head: insert prepends here (007AF44C); reset clears it", PV),
       (TL, 0x28, 8, "activeTail", TN + "*", "the active list tail: set when the first node is inserted (007AF426); reset clears it", PV),
       (TN, 0x00, 8, "vtable", "void*", "01CB4530 (RTTI FixedList<0, SeadHandle>::NODE), stamped by Init (007AA0C1); the array delete calls its slot 0", PV),
       (TN, 0x08, 8, "prev", TN + "*", "previous node: free chain links (reset 007B6AD0) and active list links (insert)", PV),
       (TN, 0x10, 8, "next", TN + "*", "next node: free chain (reset 007B6AD9, insert pops through it) and active list (insert 007AF440)", PV),
       (TN, 0x18, 4, "index", "int32", "-1 at Init (007AA0CC), the node's own array index after the reset (007B6AC4); insert returns it (007AF461)", PV),
       (TN, 0x1C, 4, "flags", "uint32", "0 at Init; insert ORs 1 (007AF450). Other bits not established", PB),
       (TN, 0x20, 8, "payload", "uint64", "the SeadHandle the node carries (RTTI of the template argument); insert stores its r8 here (007AF455). Its encoding is not read here", PB)]
TROWS = [[TL, "0x30", "18-Audio", "one embedded in each SQEX::Sd::Driver::Category at +0x08 (the only instantiation using vtable 01CB4480)",
          "EMBEDDED - Category +0x08 (a second base subobject)", "Category's constructor 007A96F0 installs the vtable; Init 007AA010 builds the nodes",
          "Category's destructor 007A9760 (inline) and the list's own scalar deleting destructor 007A98E0 (sized free 0x30)", PV[0], PV[1], "L1",
          "CARVED 2026-09-28 (OPUS, %s R K D I S). RTTI FixedList<0, SeadHandle@Sd@SQEX>. The config page's list descriptors 02EAD540 / 02EAD570 / 02EAD490 have the same template layout (sead-win-config.md); their instantiations are not this one. %s" % (REC, EXE),
          "18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md", "EMBEDDED - Category +0x08"],
         [TN, "0x28", "18-Audio", "capacity x per SeadFixedListSeadHandle30, in its node array (stride 0x28)", "HEAP - array-new in Init 007AA010 (count cookie at -8)",
          "Init 007AA010 stamps every node", "the list's destructor array-deletes the nodes (vector deleting destructor, flag 3)", PV[0], PV[1], "L1",
          "CARVED 2026-09-28 (OPUS, %s R I S). RTTI FixedList<0, SeadHandle>::NODE. %s" % (REC, EXE),
          "18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md", "HEAP - SeadFixedListSeadHandle30.nodes"]]
CAT_LIST = ("THE CATEGORY'S SOUND-HANDLE LIST (embedded FixedList<0, SeadHandle>, a second base subobject; %s K D C): the constructor installs "
            "its vtable 01CB4480 here, the initialiser 007AA110 runs Init(capacity = the ctgr element's u16 +4) on Category + 0x08 (music 4, se 48, voice 8 "
            "per the config page), and the destructor 007A9760 destroys it inline. The former rows: +0x08 secondaryVtable (the list's vptr), +0x10 "
            "nodeListHead (really capacity +0x10 and count +0x14), +0x18 nodeListTail (really the node array), +0x20..+0x37 unobservedSpan0020 (the free "
            "head, active head and tail)" % REC)
M60 = "the Category's own index in the Category table: 007AA110 stores its edx here (007AA128), and 007AAA40 passes the table slot index ebx (007AAB5F) (%s C)" % REC
M70 = ("a pointer into the Category's ctgr config element, stored by 007AA110 (007AA156): element + its u16 at +2 for version >= 2, element + 0x10 for version 1, "
       "else null - the config page reads +2 as the element's name (%s C)" % REC)
M64 = ("a signed nesting count on the category (%s U): 007AA680 increments it, and on 0 -> 1 first calls vtable slot +0x18 (float argument, r8d = -1) on every "
       "handle in the list at +0x08 (the referenced category's list when +0x58 is set) whose category byte (handle slot +0xC0) equals +0x60; 007AA3E0 decrements it "
       "clamped at 0, calling slot +0x20 on the same handles when it was 1; 007A9A10 calls slot +0x18 with +0x68 on a newly attached handle while it is > 0. "
       "The config page's macro actions 0xA8 / 0xA9 reach 007AA680 / 007AA3E0. What slots +0x18 / +0x20 do is not claimed" % REC)
M68 = ("the float 007AA680 stores on the 0 -> 1 transition of +0x64 (its xmm1 argument, the value passed to handle slot +0x18); 007AA770 subtracts its own "
       "xmm1 argument each call and clamps at 0.0 (007AA865..007AA87B); 007A9A10 passes the remaining value to a newly attached handle (007A9CB6) (%s U). "
       "Units not established" % REC)
M50 = ("set to 1 by 007AA540 whenever it writes the volume master +0x48; 007AA770 reads and clears it (007AA79A / 007AA7A5) and, when it was 1 or a volume ramp "
       "moved, pushes 007A9F40's product through handle slot +0x28 (%s U)" % REC)
M51 = ("set to 1 by 007AA530 whenever it writes the pitch master +0x4C; 007AA770 reads and clears it (007AA805 / 007AA80D) and, when it was 1 or a pitch ramp "
       "moved, pushes 007A9D30's product through handle slot +0x30 (%s U)" % REC)
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); e = fl[1][len(fl[1].rstrip("\r\n")):]
    out, was, first = [], [], None
    for l in fl:
        c = cells(l); ee = l[len(l.rstrip("\r\n")):]
        if c[0] == "Category" and c[1] in ("0x008", "0x010", "0x018", "0x0020"):
            was.append("%s %s %s %s: %s [%s %s]" % (c[1], c[2], c[3], c[4], c[5], c[6], c[7]))
            if first is None: first = (len(out), ee)
            continue
        if c[0] == "Category" and c[1] == "0x060" and c[3] == "qword0060":
            old = "%s %s %s %s: %s" % (c[1], c[2], c[3], c[4], c[5])
            out.append("\t".join(["Category", "0x060", "4", "categoryIndex60", "uint32", M60, PV[0], PV[1],
                                  "SPLIT 2026-09-28 (OPUS, %s C): was %s. %s" % (REC, old, EXE)]) + ee)
            out.append("\t".join(["Category", "0x064", "4", "holdCount64", "int32", M64, PV[0], PV[1],
                                  "SPLIT 2026-09-28 (OPUS, %s C U) from the former qword0060 (the constructor zeroes +0x60..+0x67 with one qword store, 007A972B). %s" % (REC, EXE)]) + ee)
            continue
        if c[0] == "Category" and c[1] == "0x068" and c[3] == "dword0068":
            old = "%s %s %s %s: %s" % (c[1], c[2], c[3], c[4], c[5]); c[3], c[4], c[5] = "holdArgument68", "float", M68; c[6], c[7] = PV
            c[8] += " || RETYPED 2026-09-28 (OPUS, %s U): was %s" % (REC, old); out.append("\t".join(c) + ee); continue
        if c[0] == "Category" and c[1] == "0x050" and c[3] == "word0050":
            old = "%s %s %s %s: %s" % (c[1], c[2], c[3], c[4], c[5])
            out.append("\t".join(["Category", "0x050", "1", "volumeMasterChanged50", "uint8", M50, PV[0], PV[1],
                                  "SPLIT 2026-09-28 (OPUS, %s U): was %s (the constructor zeroes both bytes with one word store, 007A9723). %s" % (REC, old, EXE)]) + ee)
            out.append("\t".join(["Category", "0x051", "1", "pitchMasterChanged51", "uint8", M51, PV[0], PV[1],
                                  "SPLIT 2026-09-28 (OPUS, %s U) from the former word0050. %s" % (REC, EXE)]) + ee)
            continue
        if c[0] == "Category" and c[1] == "0x070" and c[3] == "qword0070":
            c[3], c[4] = "configElement70", "void*"; old5 = c[5]; c[5] = M70; c[6], c[7] = PV
            c[8] += " || RETYPED 2026-09-28 (OPUS, %s C): was qword0070 void*: %s" % (REC, old5); out.append("\t".join(c) + ee); continue
        out.append(l)
    if first is not None:
        out.insert(first[0], "\t".join(["Category", "0x008", "48", "soundHandleList", TL, CAT_LIST, PV[0], PV[1],
                                        "RE-CUT 2026-09-28 (OPUS, %s K D C): four rows replaced by the embedded list; was: %s. %s" % (REC, " || ".join(was), EXE)]) + first[1])
    if not any(cells(l)[0] == TL for l in out):
        out += ["\t".join([t, "0x%02X" % o, str(n), nm, ct, m, rd[0], rd[1], "CARVED 2026-09-28 (OPUS, %s). %s" % (REC, EXE)]) + e for t, o, n, nm, ct, m, rd in NEW]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    for r in TROWS:
        if not any(cells(l)[0] == r[0] for l in tl): tl.append("\t".join(r) + te)
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
cat = {c[1]: c for c in F if c[0] == "Category"}
Tt = [cells(l)[0] for l in open(TY, "rb").read().decode("utf-8").splitlines() if cells(l)[0] in (TL, TN)]
check("W", sorted(Tt) == sorted([TL, TN]) and sum(int(c[2]) for c in F if c[0] == TL) == 0x30 and sum(int(c[2]) for c in F if c[0] == TN) == 0x28
      and cat.get("0x008", [""] * 5)[4] == TL and "0x010" not in cat and "0x018" not in cat and "0x0020" not in cat
      and cat.get("0x060", [""] * 5)[3] == "categoryIndex60" and cat.get("0x070", [""] * 5)[3] == "configElement70" and sum(int(c[2]) for c in cat.values()) == 0x88
      and cat.get("0x064", [""] * 5)[4] == "int32" and cat.get("0x068", [""] * 5)[4] == "float"
      and cat.get("0x050", [""] * 5)[2] == "1" and cat.get("0x051", [""] * 5)[4] == "uint8" and not any(c[3].startswith("unobserved") and c[1] in ("0x064", "0x0064") for c in cat.values()),
      "the list and node types tile; Category +0x08 is the embedded list; +0x50 / +0x51 bytes, +0x60 index, +0x64 int32 count, +0x68 float, +0x70 element pointer; Category still tiles 0x88")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
