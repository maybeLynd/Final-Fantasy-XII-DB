"""Animation-channel binder: a path segment that does not resolve binds nothing and logs nothing (SWE2-DATA 2026-09-30),
static, the binder 005C0820 read whole.
  A1 the member lookup's null test (005C0980 test rax / 005C0983 je) branches to a block that only releases (calls
     00584730, nothing else) and jumps to 005C0B0C, past the only kind store `mov dword ptr [rax], 1` (005C0AF4);
  A2 the binder has exactly one store of a kind value, at 005C0AF4 (so a descriptor that skips it is left unbound);
  C1 control: the out-of-range array index path does call a routine with the log format (the page's "logged"
     refusal), so the check can tell a logged refusal from a silent one: the refusal block reaches 005CDAA0 and the
     silent block does not.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import dis  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


f = dis(0x005C0820)
a = {x.address: x for x in f}
blk = [x for x in f if 0x005C09CB <= x.address <= 0x005C09EA]
calls = sorted(set(x.op_str for x in blk if x.mnemonic == "call"))
check("A1 null member -> 005C09CB block: only 00584730 calls, then jmp past the kind store",
      a[0x005C0980].op_str == "rax, rax" and a[0x005C0983].op_str == "0x5c09cb" and calls == ["0x584730"]
      and a[0x005C09EA].mnemonic == "jmp" and a[0x005C09EA].op_str == "0x5c0b0c" and 0x005C0B0C > 0x005C0AF4, str(calls))
kind = [x.address for x in f if x.mnemonic == "mov" and x.op_str.startswith("dword ptr [rax], ")]
check("A2 one kind store in the binder", kind == [0x005C0AF4], " ".join("%08X" % k for k in kind))
check("C1 control: the refusal path calls 005CDAA0, the silent block does not",
      a[0x005C0A88].op_str == "0x5cdaa0" and "0x5cdaa0" not in calls)
print("RESULT a segment the member lookup cannot resolve leaves the descriptor unbound and logs nothing")
print("FAILS %d" % FAILS)
