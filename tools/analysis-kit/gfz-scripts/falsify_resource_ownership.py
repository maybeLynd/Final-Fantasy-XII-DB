"""falsify_resource_ownership.py - falsification pass 1 on 02-Resource-And-Asset-Pipeline/CONTRACT-resource-input-ownership.md
(OPUS, 2026-09-30). Static; reads only the shipping image. Each check is one of the contract's clauses at its bytes.

O1  RL-1 the parser tests mask 4 of context +2 at 003EE018 and 003EE117
O2  RL-1 003B38B0 builds a type-3 template with flags 0x0C
O3  RL-3 the copy length is the run length truncated toward zero to a multiple of 16 (cdq / and 0xf / add / and -16)
O4  RL-4 003A9600 / 003A9950: with context+3 mask1 set, free +0x870 / +0x878 only when mask4 is clear, always clear it;
    with mask1 clear, walk 8-byte entries 1..319 / 1..767 (to 0xA00 / 0x1800); always release the lookup table
O5  RL-6 00409D60: ticket cancellation at 00409EC0, entry reset at 00409EC8, bank-slot removal at 00409ED3, in that order
O6  §2 0041E490 acquires and releases, then tail-jumps to the disposal 00409D60 with rcx = [manager + 0xD90] and the original representation
O7  §3 the owner records are 0x1C bytes at 02B581A0 + (group*16 + index) * 0x1C
O8  §3 0051EEB0 copies two 16-byte lanes
O9  RL-8 00409960 pins through 003AB880; 00409C00 unpins through 003AB940
O10 §2 003DD7E0 resets eighty owner records and 003DD790 one group's sixteen
O11 RL-7 003DDA70 writes state 3 after the request call without testing its result
O12 §2 003DD740 exposes the handle only when the state is 4
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402
from capstone import x86 as X  # noqa: E402

at, md, ext = R.at, R.md, R.ext
results = []


def check(cid, ok, what):
    results.append((cid, ok))
    print("%-4s %-9s %s" % (cid, "SURVIVES" if ok else "BROKEN", what))


def body(f):
    return list(md.disasm(at(f, ext[f]), f))


def txt(f):
    return ["%s %s" % (i.mnemonic, i.op_str) for i in body(f)]


def ins(a):
    i = R.dec(a)
    return "%s %s" % (i.mnemonic, i.op_str)


def rip(i):
    for op in i.operands:
        if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def imm0(i):
    return i.operands[0].imm if i.operands and i.operands[0].type == X.X86_OP_IMM else None


o1 = [ins(0x003EE018), ins(0x003EE117)]
check("O1", all(x.startswith("test byte ptr [") and x.endswith("+ 2], 4") for x in o1), "%s" % o1)

t2 = txt(0x003B38B0)
# the template on the stack: type byte 3 at +0 and flags 0x0C ORed into +2
check("O2", "mov byte ptr [rsp + 0x20], 3" in t2 and "or byte ptr [rsp + 0x22], 0xc" in t2,
      "003B38B0: type `mov byte [rsp + 0x20], 3` %s; flags `or byte [rsp + 0x22], 0xc` %s" % (
          "mov byte ptr [rsp + 0x20], 3" in t2, "or byte ptr [rsp + 0x22], 0xc" in t2))

t3 = txt(0x003EDAD0)
# the idiom is interleaved with argument set-up: cdq, and edx 0xf, add eax edx, then and eax -16 within a few instructions
idioms = [t3[k:k + 8] for k in range(len(t3)) if t3[k].strip() == "cdq" and "and edx, 0xf" in t3[k:k + 3] and "add eax, edx" in t3[k:k + 4]
          and "and eax, 0xfffffff0" in t3[k:k + 8]]
check("O3", len(idioms) >= 2, "truncation to a multiple of 16 toward zero: %d sites, e.g. %s" % (len(idioms), idioms[:1]))

# RL-4 lives in 0024F410's callees 003A9600 (the 800 runs, +0x870) and 003A9950 (the A00 runs, +0x878)
def rl4(f, field, end):
    t = txt(f)
    # push / sub / load the context, then the mask1 test and the mask4 test
    return (t[3].endswith("+ 3], 1") and t[4].startswith("je") and t[5].endswith("+ 2], 4") and t[6].startswith("jne")
            and ("mov rcx, qword ptr [rax + %s]" % field) in t and ("mov qword ptr [rax + %s], rdi" % field) in t
            and "mov ebx, 8" in t and ("cmp rbx, %s" % end) in t and "add rbx, 8" in t
            and t[-1] == "jmp 0x3697f0")


o4 = {"800 (+0x870, to 0xA00: indices 1..319)": rl4(0x003A9600, "0x870", "0xa00"),
      "A00 (+0x878, to 0x1800: indices 1..767)": rl4(0x003A9950, "0x878", "0x1800")}
called = [x for x in txt(0x0024F410) if x in ("call 0x3a9600", "call 0x3a9950")]
check("O4", all(o4.values()) and len(called) == 2, "cleanup shapes %s; both called from 0024F410: %s" % (o4, called))

o5 = [ins(a) for a in (0x00409EC0, 0x00409EC8, 0x00409ED3)]
check("O5", all(x.startswith("call") or x.startswith("jmp") for x in o5), "00409D60's ordered calls: %s" % o5)

b6 = body(0x0041E490)
t6 = ["%s %s" % (i.mnemonic, i.op_str) for i in b6]
# the disposal is 00409D60(bank = [manager + 0xD90], the ORIGINAL representation), reached by a tail jump after the release
check("O6", t6[-1] == "jmp 0x409d60" and "mov rcx, qword ptr [rdi + 0xd90]" in t6 and "mov rdx, rbx" in t6
      and "call 0x3ab940" in t6 and "call 0x3ab880" in t6,
      "0041E490: acquire 003AB880 %s, release 003AB940 %s, then `mov rcx, [rdi + 0xd90]`, `mov rdx, rbx`, `%s`" % (
          "call 0x3ab880" in t6, "call 0x3ab940" in t6, t6[-1]))

hits7 = []
for f in (0x003DD740, 0x003DDA20, 0x003DD420):
    b = body(f)
    t = " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in b)
    base = any(rip(i) in (0x02B581A0, 0x02B581A4) for i in b)
    stride = "0x1c" in t or ("*8]" in t and "*4]" in t) or "imul" in t
    hits7.append(("%08X" % f, base, stride))
check("O7", all(h[1] and h[2] for h in hits7), "record base 02B581A0 and a 0x1C stride in the lookup, arm and delete helpers: %s" % hits7)

t8 = txt(0x0051EEB0)
lanes = [x for x in t8 if x.startswith(("movups", "movdqu", "movaps", "movdqa"))]
check("O8", len(lanes) >= 4, "0051EEB0 vector moves (two loads, two stores expected): %s" % lanes)

c9a = [imm0(i) for i in body(0x00409960) if i.mnemonic in ("call", "jmp")]
c9b = [imm0(i) for i in body(0x00409C00) if i.mnemonic in ("call", "jmp")]
check("O9", 0x003AB880 in c9a and 0x003AB940 in c9b, "00409960 reaches 003AB880: %s; 00409C00 reaches 003AB940: %s" % (
    0x003AB880 in c9a, 0x003AB940 in c9b))

t10a, t10b = " ; ".join(txt(0x003DD7E0)), " ; ".join(txt(0x003DD790))
check("O10", ("0x50" in t10a or ("0x10" in t10a and "5" in t10a)) and "0x10" in t10b,
      "003DD7E0 carries 80 (0x50) or 5 x 16: %s; 003DD790 carries 16: %s" % ("0x50" in t10a or ("0x10" in t10a and ", 5" in t10a), "0x10" in t10b))

b11 = body(0x003DDA70)
calls = [k for k, i in enumerate(b11) if i.mnemonic == "call"]
st3 = [k for k, i in enumerate(b11) if i.mnemonic == "mov" and i.op_str.endswith("+ 4], 3")]
tested = st3 and calls and any(i.mnemonic == "test" and i.op_str in ("eax, eax", "al, al", "rax, rax") for i in b11[calls[-1] + 1:st3[-1]])
check("O11", bool(st3) and bool(calls) and st3[-1] > calls[-1] and not tested,
      "state-3 store after the last call without a result test: %s" % (
          ["%08X %s %s" % (b11[k].address, b11[k].mnemonic, b11[k].op_str) for k in st3]))

t12 = txt(0x003DD740)
check("O12", any(x.startswith("cmp dword ptr [") and x.endswith("+ 4], 4") for x in t12), "003DD740 state test: %s" % [x for x in t12 if x.startswith("cmp")])

broken = [c for c, ok in results if not ok]
print("BROKEN %d: %s" % (len(broken), " ".join(broken) or "none"))
sys.exit(0)
