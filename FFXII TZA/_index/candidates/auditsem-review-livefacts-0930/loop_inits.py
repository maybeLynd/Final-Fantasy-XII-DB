"""SWE2-AUDIT-SEM: for each candidate loop (bound_loops.out), decode from its .pdata fragment start (aligned) to the
loop head and print the last writes of the counter / end registers named in the loop's exit, so the trip count or
end address can be read."""
import re, struct
import img
PD = []
for n, rva, vsz, rp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rp + k)
            if b:
                PD.append((b + img.BASE, e + img.BASE))
def frag(a):
    for b, e in PD:
        if b <= a < e:
            return b, e
    return None
def norm(r):
    m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
    if r in m:
        return m[r]
    mm = re.fullmatch(r"(r\d+)[dwb]?", r)
    return mm.group(1) if mm else r
for line in open("bound_loops.out"):
    head = int(line.split()[0], 16)
    regs = set()
    for c in re.findall(r"(?:sub|cmp|inc|dec) (\w+)(?:, (\w+))?", line.split("exits:")[1]):
        for r in c:
            if r and not r.startswith("0x") and r not in ("dword", "byte", "qword"):
                regs.add(norm(r))
    f = frag(head)
    if not f:
        print("%08X no .pdata fragment" % head)
        continue
    xs = [x for x in img.md.disasm(img.rd(f[0], head - f[0]), f[0]) if x.address < head]
    last = {}
    for x in xs:
        o = [s.strip() for s in x.op_str.split(",")]
        if o and norm(o[0]) in regs and x.mnemonic not in ("cmp", "test", "push"):
            last[norm(o[0])] = "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
    print("%08X fragment %08X: %s" % (head, f[0], " | ".join("%s <- %s" % kv for kv in sorted(last.items())) or "-"))
