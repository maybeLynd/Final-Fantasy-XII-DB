"""rc37_refused_read.py - RC-37: what the resource request queue does with a .btm request whose read 002DF780 refused
(the KR / CN file-size tables hold -1 for all six ids). OPUS, 2026-09-30. Static, the certified image. Reads only.

Each fact is an exact instruction (address, mnemonic, operands) read from the image; the script fails if any differs.

  F1  the kind-7 issue wrapper 0046E030 calls 002DF780 and returns 1 whatever it returned (0046E03E, 0046E043);
  F2  002DF780 refuses a (kind, id) whose file-size entry is -1 by jumping to its epilogue (002DF7B0/002DF7B9 ->
      002DF85D), which returns 0 and writes nothing; only its accepted paths hand the reader the status slot 0215EFF4
      (002DF808, 002DF838);
  F3  the pump 0032E070, state 1, kind != 0xFF: it calls 0046E030 (0032E0F1) and sets state 2 without testing the result
      (0032E0F6..0032E0FF); state 2 sets state 3 (0032E15A);
  F4  state 3: busy iff [0215EFF4] == -1 (0046DFE0); otherwise state 5 + (status < 0) (0032E19C..0032E1A8);
  F5  the status slot is written only by the readers' submit (-1: 001D6DD4, 001D6FF4, both through the pointer
      002DF780 / 002DF6C0 pass) and by their completion job 001D6D70 (the worker's result, once: 001D6D7C, then the
      stored pointer is cleared at 001D6D7E); census: every rip-relative reference to 0215EFF4 and to the pointer
      global 01F82CC0 lies in 002DF6C0, 002DF780, 0046DFE0, 0046E0E0, 001D6D70, 001D6D90, 001D6FB0;
  F6  the completion paths call the request's callback +0x40: the done helper 0032E330 always (r8d 1); the error helper
      0032E370 when the byte count +0x28 is -1 (0032E382, r8d 0);
  F7  the .btm request (00365810) passes the size query's result as the byte count (0032E400 returns -1 unrounded:
      0032E43D jle; 003658A4 mov r9d, ebx) and 00364380 as the callback (00365837);
  F8  the callback 00364380 sets bit `slot` of [[022CBE00] + 0x240] with no test of its success argument.
Control C1 (the same reading on the checked path): the kind-0xFF branch DOES test its submit result - 0032E111 call
002DF6C0, 0032E116 test eax, 0032E118 jne 0032E090 (re-visit the head) - so F3's "no test" is a property of the
kind != 0xFF branch, not of the reader. Control C2: F1's wrapper would propagate a refusal if its return were eax;
the script checks the literal `mov eax, 1` after the call, so a wrapper returning 002DF780's eax fails F1.
"""
import os, sys
import capstone
from capstone import x86 as X

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
fails = 0


def ins(a):
    return next(md.disasm(R.at(a, 16), a, 1))


def expect(tag, a, text):
    global fails
    i = ins(a)
    got = ("%s %s" % (i.mnemonic, i.op_str)).strip()
    ok = got == text
    fails += not ok
    print("%s  %s %08X %s%s" % ("PASS" if ok else "FAIL", tag, a, got, "" if ok else "   (expected: %s)" % text))


def target(a):
    i = next(md.disasm(R.at(a, 16), a, 1))
    return i.address + i.size + int(i.op_str.split("0x")[-1].rstrip("]"), 16) if "rip" in i.op_str else None


# F1
expect("F1", 0x0046E03E, "call 0x2df780")
expect("F1", 0x0046E043, "mov eax, 1")
expect("F1", 0x0046E048, "add rsp, 0x38")
# F2
expect("F2", 0x002DF7B0, "cmp dword ptr [r15 + rax*4 + 0x2da3ee0], -1")
expect("F2", 0x002DF7B9, "je 0x2df85d")
expect("F2", 0x002DF862, "xor eax, eax")
for a in (0x002DF808, 0x002DF838):
    t = a + ins(a).size + ins(a).operands[1].mem.disp
    ok = t == 0x0215EFF4
    fails += not ok
    print("%s  F2 %08X hands the reader the status slot %08X" % ("PASS" if ok else "FAIL", a, t))
# F3
expect("F3", 0x0032E0F1, "call 0x46e030")
expect("F3", 0x0032E0F6, "call 0x35e810")
expect("F3", 0x0032E0FB, "mov qword ptr [rbx + 8], rax")
expect("F3", 0x0032E0FF, "mov byte ptr [rbx + 0x20], 2")
expect("F3", 0x0032E15A, "mov byte ptr [rbx + 0x20], 3")
# F4
expect("F4", 0x0046DFE7, "cmp dword ptr [rip + 0x1cf1006], -1")
expect("F4", 0x0046E0E0, "mov eax, dword ptr [rip + 0x1cf0f0e]")
expect("F4", 0x0032E163, "call 0x46dfe0")
expect("F4", 0x0032E16A, "jne 0x32e2a0")
expect("F4", 0x0032E19C, "call 0x46e0e0")
expect("F4", 0x0032E1A3, "sets al")
expect("F4", 0x0032E1A6, "add al, 5")
# F5 census over the catalogue
refs = {}
for f, n in R.ext.items():
    d = R.at(f, n)
    if not d:
        continue
    for i in R.md.disasm(d, f):
        for op in i.operands:
            if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
                t = i.address + i.size + op.mem.disp
                if t in (0x0215EFF4, 0x01F82CC0):
                    refs.setdefault(t, set()).add(f)
allowed = {0x002DF6C0, 0x002DF780, 0x0046DFE0, 0x0046E0E0, 0x001D6D70, 0x001D6D90, 0x001D6FB0}
got = set().union(*refs.values()) if refs else set()
ok = got <= allowed and 0x0215EFF4 in refs and 0x01F82CC0 in refs
fails += not ok
print("%s  F5 references to 0215EFF4 / 01F82CC0 lie only in %s" % ("PASS" if ok else "FAIL", " ".join("%08X" % x for x in sorted(got))))
expect("F5", 0x001D6DD4, "mov dword ptr [rax], 0xffffffff")
expect("F5", 0x001D6FF4, "mov dword ptr [rax], 0xffffffff")
expect("F5", 0x001D6D7C, "mov dword ptr [rax], ecx")
expect("F5", 0x001D6D7E, "mov qword ptr [rip + 0x1dabf37], 0")
# F6
expect("F6", 0x0032E336, "mov rax, qword ptr [rcx + 0x40]")
expect("F6", 0x0032E346, "mov r8d, 1")
expect("F6", 0x0032E34F, "call rax")
expect("F6", 0x0032E382, "cmp dword ptr [rcx + 0x28], -1")
expect("F6", 0x0032E38C, "xor r8d, r8d")
expect("F6", 0x0032E392, "call rax")
# F7
expect("F7", 0x00365882, "call 0x32e400")
expect("F7", 0x0032E43D, "jle 0x32e44b")
expect("F7", 0x003658A4, "mov r9d, ebx")
expect("F7", 0x003658C7, "call 0x32e620")
t = 0x00365837 + ins(0x00365837).size + ins(0x00365837).operands[1].mem.disp
ok = t == 0x00364380
fails += not ok
print("%s  F7 00365837 passes the callback %08X" % ("PASS" if ok else "FAIL", t))
# F8
expect("F8", 0x00364391, "shl eax, cl")
expect("F8", 0x00364393, "or dword ptr [rdx + 0x240], eax")
body = [("%s %s" % (i.mnemonic, i.op_str)) for i in md.disasm(R.at(0x00364380, 0x1A), 0x00364380)]
ok = not any("r8" in b for b in body)
fails += not ok
print("%s  F8 00364380 never reads its success argument (r8): %s" % ("PASS" if ok else "FAIL", "; ".join(body[:7])))
# C1 the kind-0xFF branch tests its submit result
expect("C1", 0x0032E111, "call 0x2df6c0")
expect("C1", 0x0032E116, "test eax, eax")
expect("C1", 0x0032E118, "jne 0x32e090")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
