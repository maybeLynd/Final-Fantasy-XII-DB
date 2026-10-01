"""filter_tail.py - CV-3: what the unhandled-exception filter 0079AD50 does after the dump, in order (FABLE, Claude Opus 5.5,
2026-09-28). STATIC, certified image only; nothing executed. Consumes ASTRA 81 (native-exception-filter-tail) and 82
(native-filter-message-resource) and OPUS's native-filter-abi-opus, re-derived without their code.

  O  ORDER: GetCurrentThreadId; gate dword 01F40128 == 0 -> straight to return 1 (no dump, no box); else MiniDumpWriteDump
     (thunk 0080F2BC, type 0x1826) at 0079ADCA; CloseHandle(file) 0079ADD2; SysFreeString(NULL) 0079ADDA (a no-op free);
     text id 0x7837 through 0019A510 at 0079ADE5; if found, SysAllocStringLen(ptr + 2, u16 count) 0079AE00, else the text
     stays NULL; ShowCursor(1) 0079AE0E; MessageBoxW(NULL, text, caption, 0x10) 0079AE26; SysFreeString(text) 0079AE2F;
     mov eax, 1 / ret (0079AE35 / 0079AE3F). The text request comes BEFORE ShowCursor - the page's 2026-09-14 order
     (ShowCursor, then the text) is rejected by the addresses.
  I  IMPORTS: each call's IAT slot resolves to the named import (OLEAUT32 slots by ordinal: 6 SysFreeString, 4
     SysAllocStringLen, as pefile names them)
  S  STRINGS: the caption at 008F3DC0 is L"error"; string-table block 0x784 entry 7 (id 0x7837) is present in all nine
     language copies; English (0x409) is "Fatal error encountered." (24 code units)
  P  SELECTOR 0019A5B0 (ASTRA 83): walks (id & 0xF) counted entries - movzx eax, word [rbx] / lea rbx, [rbx + rax*2] /
     add rbx, 2 - comparing only the CURRENT pointer with the end (cmp rbx, rcx / jae before each step, jb after); then a
     zero count gives NULL (cmp word [rbx], 0 / cmove) and otherwise the pointer to the length prefix. No instruction adds
     the selected entry's 2 + 2*count to compare with the end. Model: a declared resource of 16 bytes whose entry 1 has a
     count of 1 at offset 14 returns offset 14 although its text would end at 18; a full-span model would return NULL.
  Not claimed: which language copy the lookup selects at run time, that the box is displayed, what the OS does after the
  filter returns EXCEPTION_EXECUTE_HANDLER (1), or the cause of any observed crash.
"""
import hashlib, os, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
raw = open(EXE, "rb").read()
if hashlib.sha256(raw).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXE)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
ins = {x.address: x for x in cs.disasm(raw[off(0x79AD50):off(0x79AE40)], 0x79AD50)}
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
imp = {}
for e in pe.DIRECTORY_ENTRY_IMPORT:
    for i in e.imports: imp[i.address] = i.name.decode() if i.name else "ord%d" % i.ordinal
def target(a):
    x = ins[a]
    if x.op_str.startswith("qword ptr [rip"):
        return imp.get(a + x.size + int(x.op_str.split("+ ")[1].rstrip("]"), 16))
    return x.op_str
ORDER = [(0x79AD59, "GetCurrentThreadId"), (0x79ADCA, "0x80f2bc"), (0x79ADD2, "CloseHandle"), (0x79ADDA, "SysFreeString"),
         (0x79ADE5, "0x19a510"), (0x79AE00, "SysAllocStringLen"), (0x79AE0E, "ShowCursor"), (0x79AE26, "MessageBoxW"),
         (0x79AE2F, "SysFreeString")]
got = [(a, target(a)) for a, _ in ORDER]
args = {0x79ADD8: "xor ecx, ecx", 0x79ADE0: "mov ecx, 0x7837", 0x79ADA8: "mov r9d, 0x1826", 0x79AE09: "mov ecx, 1",
        0x79AE14: "mov r9d, 0x10", 0x79AE24: "xor ecx, ecx", 0x79AD77: "je 0x79ae35", 0x79AE35: "mov eax, 1", 0x79AE3F: "ret",
        0x79ADF7: "je 0x79ae09", 0x79ADF9: "movzx edx, word ptr [rax]", 0x79ADFC: "lea rcx, [rax + 2]"}
argok = all(("%s %s" % (ins[a].mnemonic, ins[a].op_str)).strip() == s for a, s in args.items())
gate = ins[0x79AD5F]; gcell = 0x79AD5F + gate.size + int(gate.op_str.split("+ ")[1].split("]")[0], 16)
calls = [a for a in sorted(ins) if ins[a].mnemonic == "call"]
seq = [target(a) for a in calls]
old_order = seq.index("ShowCursor") < seq.index("0x19a510")   # the page's 2026-09-14 reading: ShowCursor, then the text
check("O", got == ORDER and argok and gcell == 0x1F40128 and "cmp dword ptr" in gate.mnemonic + " " + gate.op_str
      and [a for a in calls if a > 0x79ADCA] == [a for a, _ in ORDER if a > 0x79ADCA] and not old_order,
      "calls after the dump in address order %s; arguments/branches %s; gate cell %08X; ShowCursor-before-text reading %s"
      % ([t for a, t in got if a > 0x79ADCA], argok, gcell, "rejected" if not old_order else "holds"))
check("I", target(0x79ADDA) == target(0x79AE2F) == "SysFreeString" and target(0x79AE00) == "SysAllocStringLen",
      "OLEAUT32 slots: %s / %s / %s" % (target(0x79ADDA), target(0x79AE00), target(0x79AE2F)))
lea = ins[0x79AE1A]; cap = 0x79AE1A + lea.size + int(lea.op_str.split("+ ")[1].rstrip("]"), 16)
caption = raw[off(cap):off(cap) + 12].decode("utf-16le")
langs = {}
for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
    if t.id == 6:
        for n in t.directory.entries:
            if n.id == 0x784:
                for l in n.directory.entries:
                    data = pe.get_data(l.data.struct.OffsetToData, l.data.struct.Size); p = 0
                    for i in range(8):
                        c = struct.unpack_from("<H", data, p)[0]
                        if i == 7: langs[l.id] = (c, data[p + 2:p + 2 + 2 * c].decode("utf-16le"))
                        p += 2 + 2 * c
check("S", cap == 0x8F3DC0 and caption == "error\0" and len(langs) == 9 and langs.get(0x409) == (24, "Fatal error encountered."),
      "caption %08X %r; id 0x7837 in %d language copies; 0x409 = %r" % (cap, caption.rstrip("\0"), len(langs), langs.get(0x409)))
sel = {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(raw[off(0x19A5B0):off(0x19A64F)], 0x19A5B0)}
sz = {x.address: x.size for x in cs.disasm(raw[off(0x19A5B0):off(0x19A64F)], 0x19A5B0)}
def covered(lo, hi):
    a = lo
    while a < hi:
        if a not in sz: return False
        a += sz[a]
    return True
P_BYTES = {0x19A60A: "and edi, 0xf", 0x19A610: "cmp rbx, rcx", 0x19A613: "jae 0x19a62a", 0x19A615: "movzx eax, word ptr [rbx]",
           0x19A618: "lea rbx, [rbx + rax*2]", 0x19A61C: "add rbx, 2", 0x19A625: "cmp rbx, rcx", 0x19A628: "jb 0x19a62e",
           0x19A630: "cmp word ptr [rbx], ax", 0x19A633: "cmove rbx, rax", 0x19A637: "mov rax, rbx"}
cmps = [a for a, t in sel.items() if 0x19A605 <= a < 0x19A637 and t.startswith("cmp ") and "rcx" in t]
def sel_model(buf_len, counts, k, fullspan=False):
    o = 0
    for i in range(k):
        if o >= buf_len: return None
        o += 2 + 2 * counts[i]
    if o >= buf_len: return None
    if counts[k] == 0: return None
    if fullspan and o + 2 + 2 * counts[k] > buf_len: return None
    return o
counts = [0] * 7 + [1]          # seven empty prefixes, then entry 7 with one code unit (ASTRA's shape: prefix at 14)
m = (sel_model(18, counts, 7), sel_model(16, counts, 7), sel_model(16, counts, 7, fullspan=True), sel_model(18, [0] * 8, 7))
check("P", all(sel.get(a) == t for a, t in P_BYTES.items()) and len(cmps) == 2 and covered(0x19A605, 0x19A63A)
      and m == (14, 14, None, None),
      "selector anchors %s; end comparisons in the walk %s (both on the current pointer); model 18-byte / 16-byte resource, "
      "entry 7 count 1 -> %s / %s; rejected full-span model -> %s; count 0 -> %s"
      % (all(sel.get(a) == t for a, t in P_BYTES.items()), ["%08X" % a for a in cmps], m[0], m[1], m[2], m[3]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
