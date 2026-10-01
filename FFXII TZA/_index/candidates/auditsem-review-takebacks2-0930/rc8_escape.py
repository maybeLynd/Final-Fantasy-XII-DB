"""SWE2-AUDIT-SEM RC-8 attack (own code): does the shadow singleton's pointer escape anywhere a 3-hop direct-call
census cannot follow? For every rip-relative load of 01F82EA8 (longest decode) and every direct call of the creators
001F0850 / 001F0810 (rax after the call), follow the register linearly for 40 instructions and report
  - STORE-ESCAPE: the pointer itself stored to memory (other than a stack spill) -> another structure could reload it;
  - CALL-ARG: a call with the pointer in rcx/rdx/r8/r9 (the callee list, to compare with the producer's H1);
  - BULK: a call to a memset/memcpy-shaped callee with the pointer as destination.
Also: every rip-relative STORE to 01F82EA8 (who installs the pointer).
"""
import struct, re
import img
CELL = 0x01F82EA8
CREATORS = (0x001F0850, 0x001F0810)
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
R = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
def norm(r):
    m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
    if r in m:
        return m[r]
    mm = re.fullmatch(r"(r\d+)[dwb]?", r)
    return mm.group(1) if mm else r

seeds = []
for i in range(len(text) - 4):
    d = struct.unpack_from("<i", text, i)[0]
    if va0 + i + 4 + d == CELL:
        for back in range(11, 0, -1):
            s = i - back
            x = next(img.md.disasm(text[s:s + 16], va0 + s), None)
            if x and x.size == back + 4 and "rip" in x.op_str:
                ops = [o.strip() for o in x.op_str.split(",")]
                if x.mnemonic == "mov" and "rip" in ops[1] and norm(ops[0]) in R:
                    seeds.append((x.address, x.address + x.size, norm(ops[0]), "load"))
                elif "rip" in ops[0]:
                    print("CELL STORE/RMW: %08X %s %s" % (x.address, x.mnemonic, x.op_str))
                else:
                    print("CELL other use: %08X %s %s" % (x.address, x.mnemonic, x.op_str))
                break
    if text[i] in (0xE8, 0xE9) and i + 5 <= len(text):
        tgt = va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0]
        if tgt in CREATORS:
            seeds.append((va0 + i, va0 + i + 5, "rax", "creator-%s" % ("call" if text[i] == 0xE8 else "jmp")))
print("seeds:", len(seeds))
calls = {}
for a, nxt, reg, kind in seeds:
    taint = {reg}
    for x in list(img.md.disasm(img.rd(nxt, 300), nxt))[:40]:
        ops = [o.strip() for o in x.op_str.split(",")]
        if x.mnemonic in ("ret", "jmp", "int3"):
            break
        if x.mnemonic == "call":
            args = [r for r in ("rcx", "rdx", "r8", "r9") if r in taint]
            if args:
                calls.setdefault(x.op_str, []).append("%08X(%s)" % (x.address, ",".join(args)))
            taint -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
            continue
        if len(ops) == 2 and norm(ops[1]) in taint and "ptr [" in ops[0] and not re.search(r"\[(rsp|rbp)", ops[0]) \
                and x.mnemonic == "mov":
            print("STORE-ESCAPE seed %08X (%s): %08X %s %s" % (a, kind, x.address, x.mnemonic, x.op_str))
        if ops and norm(ops[0]) in R:
            dst = norm(ops[0])
            if x.mnemonic in ("mov", "lea") and len(ops) == 2 and (norm(ops[1]) in taint or re.search(r"\[(%s)( \+ 0x[0-9a-f]+)?\]" % "|".join(taint), ops[1])):
                if x.mnemonic == "mov" and "ptr" in ops[1]:
                    taint.discard(dst)  # a load through the pointer is a field, not the pointer
                else:
                    taint.add(dst)
            elif x.mnemonic not in ("cmp", "test", "push"):
                taint.discard(dst)
print("\ncallees receiving the pointer (first 40 instructions after each seed):")
for c in sorted(calls):
    print("  %-14s %s" % (c, " ".join(calls[c][:8])))
