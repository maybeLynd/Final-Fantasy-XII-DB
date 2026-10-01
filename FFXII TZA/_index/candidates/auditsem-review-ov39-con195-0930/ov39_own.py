"""SWE2-AUDIT-SEM OV-39 / CON-195 re-read: 00409F80's body; 0040A230's lea/mov pairs (count, store range, strings);
direct callers of 00409F80 and of 0041E3A0's site 0041E40B."""
import struct, re, collections
import img
for x in img.dis(0x00409F80, 6):
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
def rt(x):
    m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    return x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1) if m else None
xs = [x for x in img.md.disasm(img.rd(0x0040A230, 0x7E1), 0x0040A230)]
pairs, strs, dsts, other = 0, [], [], collections.Counter()
for a, b in zip(xs, xs[1:]):
    if a.mnemonic == "lea" and "rip" in a.op_str and b.mnemonic == "mov" and "rip" in b.op_str.split(",")[0]:
        pairs += 1
        s = img.rd(rt(a), 80).split(b"\0")[0].decode("latin-1")
        strs.append(s)
        dsts.append(rt(b))
for x in xs:
    if x.mnemonic not in ("lea", "mov"):
        other[x.mnemonic] += 1
print("0040A230: instructions %d, lea/mov-to-rip pairs %d, other mnemonics %s, last %08X %s" % (len(xs), pairs, dict(other), xs[-1].address, xs[-1].mnemonic))
print("store range %08X..%08X, distinct stores %d" % (min(dsts), max(dsts), len(set(dsts))))
pre = collections.Counter(re.sub(r"[^\/]+$", "", s) for s in strs)
print("string directory prefixes:", dict(pre))
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
for T in (0x00409F80, 0x0041E3A0):
    s = [("%08X" % (va0 + i), "call" if text[i] == 0xE8 else "jmp") for i in range(len(text) - 5)
         if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == T]
    print("direct sites into %08X: %s" % (T, s))
print("strings containing 'obj_finish' and ending .cm: %d of %d" % (sum(1 for s in strs if "obj_finish" in s and s.lower().endswith(".cm")), len(strs)))
print("caller chain: 0041E3A0 RenderResourceRoot_InitializeSubcontainers is called from 0033263C in CharacterRenderSystem_AllocateAndInitialize (003325D0)")
