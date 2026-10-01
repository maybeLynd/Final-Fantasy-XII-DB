"""fst_r8_mode.py - which of the two (kind, id) read-item constructors runs its item at once, and which queues it.
SWE2-FRONTIER, 2026-09-30, for FABLE-REQ-FRONTIER-OV-PROBE-CORRECTIONS-0930 item (c). Static; reads the shipping image.

001A0BB0(queue, item, r8b): a nonzero r8b calls the item runner inline and returns; zero takes the list-insert path.
The old reading on file-size-tables-fst.md called 001D6FB0 "the asynchronous half". This control rejects it when
001D6FB0 passes r8b = 1, and its positive control is 001D6D90, which must pass r8d = 0, so the check can tell the
two apart.

C1  001A0BB0 tests r8b and, when set, calls a function and jumps to its exit; when clear it falls to the queue path
C2  001D6FB0 sets r8b = 1 right before its call to 001A0BB0            (rejects "001D6FB0 is the asynchronous half")
C3  001D6D90 zeroes r8d right before its call to 001A0BB0              (positive control: the queued constructor)
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402  (image access, extents and the decoder)

at, md, ext = R.at, R.md, R.ext
QUEUE = 0x001A0BB0
fails = 0


def body(f):
    return list(md.disasm(at(f, ext[f]), f))


def report(cid, ok, what):
    global fails
    fails += 0 if ok else 1
    print("%-3s %-4s %s" % (cid, "PASS" if ok else "FAIL", what))


def r8_before_call(f):
    """the last instruction writing r8/r8d/r8b before the call to 001A0BB0 in f, and the call site"""
    b = body(f)
    for k, i in enumerate(b):
        if i.mnemonic == "call" and i.op_str == hex(QUEUE):
            for j in range(k - 1, max(-1, k - 6), -1):
                ops = b[j].op_str.split(",")[0].strip()
                if ops in ("r8", "r8d", "r8b"):
                    return b[j], i
            return None, i
    return None, None


q = body(QUEUE)
txt = ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in q]
k = next((n for n, i in enumerate(q) if i.mnemonic == "test" and i.op_str == "r8b, r8b"), None)
ok1 = (k is not None and q[k + 1].mnemonic == "je" and q[k + 2].mnemonic == "call" and q[k + 3].mnemonic == "jmp")
if ok1:
    queued_at = int(q[k + 1].op_str, 16)
    inline_callee = int(q[k + 2].op_str, 16)
    report("C1", True, "%08X test r8b / %08X je %08X (queue path) / %08X call %08X (inline) / %08X jmp" % (
        q[k].address, q[k + 1].address, queued_at, q[k + 2].address, inline_callee, q[k + 3].address))
else:
    report("C1", False, "no test r8b / je / call / jmp shape in 001A0BB0: " + " | ".join(txt[:20]))

for cid, f, want in (("C2", 0x001D6FB0, "mov r8b, 1"), ("C3", 0x001D6D90, "xor r8d, r8d")):
    w, c = r8_before_call(f)
    got = None if w is None else "%s %s" % (w.mnemonic, w.op_str)
    report(cid, got == want, "%08X: r8 set by %s at %s before call 001A0BB0 at %s -> %s" % (
        f, got, "%08X" % w.address if w else "-", "%08X" % c.address if c else "-",
        "runs inline" if got == "mov r8b, 1" else "queued" if got == "xor r8d, r8d" else "?"))

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
