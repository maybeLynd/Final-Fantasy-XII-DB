"""SWE2-AUDIT-SEM own request-site census (independent of the producer's callpairs/nearcall_imm).
1) every rel32 call/jmp in .text whose target is one of the request entries (0032E620 request, 0032E400 size lookup)
   or a thunk/wrapper that is a bare jmp to one of them (found here, not assumed);
2) at each site, a backward constant-propagation over the preceding straight-line instructions (up to 24, stopping
   at a ret/jmp/call boundary) for ecx (kind) and edx (id): mov r,imm / xor r,r / lea r,[r2+imm] / lea r,[imm] /
   mov r,r2 chains resolved when r2 is known.
Prints every site as KIND ID (or '?'), then the kind-9 table and the unresolved sites."""
import struct, collections, sys
import img
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
ENTRIES = {0x0032E620: "request", 0x0032E400: "sizeof"}

def rel_targets():
    out = collections.defaultdict(list)
    for i in range(len(text) - 5):
        op = text[i]
        if op in (0xE8, 0xE9):
            tgt = va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0]
            out[tgt].append((va0 + i, "call" if op == 0xE8 else "jmp"))
    return out

refs = rel_targets()
# thunks: a jmp to an entry that is itself the first instruction of a function (preceded by int3/ret padding)
entries = dict(ENTRIES)
for e in list(ENTRIES):
    for site, kind in refs.get(e, []):
        if kind == "jmp":
            prev = text[site - va0 - 1]
            if prev in (0xCC, 0xC3):
                entries[site] = ENTRIES[e] + "-thunk@%08X" % site

REG32 = {"ecx": "rcx", "edx": "rdx", "r8d": "r8", "r9d": "r9", "eax": "rax", "ebx": "rbx", "esi": "rsi", "edi": "rdi",
         "ebp": "rbp", "r10d": "r10", "r11d": "r11", "r12d": "r12", "r13d": "r13", "r14d": "r14", "r15d": "r15"}
def norm(r):
    return REG32.get(r, r)

def decode_back(site, maxn=24):
    """straight-line instructions ending at site, found by trying start offsets and keeping the decode that
    reaches the call exactly (longest chain wins)."""
    best = []
    for back in range(8, 160):
        s = site - back
        seq = []
        ok = False
        for ins in img.md.disasm(text[s - va0: site - va0 + 5], s):
            seq.append(ins)
            if ins.address == site:
                ok = True
                break
            if ins.address > site:
                break
        if ok and len(seq) > len(best):
            best = seq
    return best[:-1][-maxn:]

def const_regs(seq):
    known = {}
    for ins in seq:
        m, ops = ins.mnemonic, [o.strip() for o in ins.op_str.split(",")]
        if m in ("call",):
            known = {}
            continue
        if m in ("ret", "jmp") :
            known = {}
            continue
        if len(ops) != 2:
            continue
        d, s = norm(ops[0]), ops[1]
        if m == "mov":
            if s.startswith("0x") or s.isdigit():
                known[d] = int(s, 0)
            elif norm(s) in known:
                known[d] = known[norm(s)]
            else:
                known.pop(d, None)
        elif m == "xor" and norm(ops[0]) == norm(ops[1]):
            known[d] = 0
        elif m == "lea" and s.startswith("[") and "rip" not in s and "*" not in s:
            inner = s.strip("[]").replace(" ", "")
            parts = inner.replace("-", "+-").split("+")
            val, okk = 0, True
            for p in parts:
                if not p:
                    continue
                if p.lstrip("-").startswith("0x") or p.lstrip("-").isdigit():
                    val += int(p, 0)
                elif norm(p) in known:
                    val += known[norm(p)]
                else:
                    okk = False
            if okk:
                known[d] = val
            else:
                known.pop(d, None)
        else:
            known.pop(d, None)
    return known

rows = []
for e, name in entries.items():
    for site, kind in refs.get(e, []):
        if site in entries:
            continue
        seq = decode_back(site)
        k = const_regs(seq)
        rows.append((site, name, kind, k.get("rcx"), k.get("rdx")))
rows.sort()
print("entries/thunks:", {"%08X" % a: n for a, n in entries.items()})
print("sites:", len(rows))
pairs = collections.Counter((r[3], r[4]) for r in rows)
for site, name, kind, K, I in rows:
    print("%08X %-26s %-4s kind=%s id=%s" % (site, name, kind, "?" if K is None else hex(K), "?" if I is None else hex(I)))
print("== kind 9 resolved ids:", sorted({hex(r[4]) for r in rows if r[3] == 9 and r[4] is not None}))
print("== sites with kind unresolved:", sum(1 for r in rows if r[3] is None),
      " kind known but id unresolved:", sum(1 for r in rows if r[3] is not None and r[4] is None))
print("== kind-known/id-unresolved sites by kind:", collections.Counter(r[3] for r in rows if r[3] is not None and r[4] is None))
