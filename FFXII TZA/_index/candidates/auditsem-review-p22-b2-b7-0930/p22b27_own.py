"""SWE2-AUDIT-SEM P22-B2..B7 check (own code): the helper bodies and call-site windows FRONTIER's crossing paragraphs
describe, printed for reading. Short helpers are decoded whole to their first ret / tail jump; long bodies only at
the cited windows. Also the direct-caller counts the paragraphs give for a few helpers."""
import struct
import img

t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
def rel_sites(t):
    return [va0 + i for i in range(len(text) - 5)
            if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == t]
def whole(a, title, maxn=60):
    print("== %s %08X" % (title, a))
    n = 0
    for x in img.md.disasm(img.rd(a, 0x400), a):
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
        n += 1
        if x.mnemonic == "ret" or (x.mnemonic == "jmp" and n > 1 and not x.op_str.startswith("0x" + "%x" % a)) \
                or n >= maxn or x.mnemonic == "int3":
            break
def win(lo, hi, title, entry=None):
    print("== %s %08X-%08X" % (title, lo, hi))
    st = entry if entry else lo
    xs = None
    if entry is None:
        for back in range(0, 16):
            xs = list(img.md.disasm(img.rd(lo - back, hi - lo + back + 16), lo - back))
            if any(x.address == lo for x in xs):
                break
    else:
        xs = list(img.md.disasm(img.rd(st, hi - st + 16), st))
    for x in xs:
        if lo <= x.address <= hi:
            print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))

for a, t in ((0x00247870, "widget flag bit 1 + refresh"), (0x00254A10, "game-mode test"), (0x00282DF0, "char record"),
             (0x002DD7E0, "bounded id table"), (0x00249580, "slot claim"), (0x00244960, "attach child"),
             (0x003148F0, "field-id getter"), (0x003946B0, "layout copy"), (0x00263FF0, "manager slot"),
             (0x00263C30, "slot dword +0x20"), (0x003589B0, "handle encode"), (0x003ABCA0, "list remove"),
             (0x0024ED80, "subtype publisher"), (0x00229EA0, "mode getter"), (0x003A12D0, "bank loader 1"),
             (0x0035E810, "8-byte getter"), (0x002D66A0, "word setter"), (0x002D6620, "byte/qword setter"),
             (0x005C3A30, "dword getter"), (0x00313F60, "bit-15 tail"), (0x004304F0, "pair relocate"),
             (0x00500470, "four pairs"), (0x003697C0, "movement latch"), (0x0050DF30, "script release")):
    whole(a, t)
for a, t in ((0x003A1330, "bank loader 2"), (0x003A1390, "bank loader 3")):
    print("== %s %08X size to next int3 run:" % (t, a), end=" ")
    xs = list(img.md.disasm(img.rd(a, 0x80), a))
    end = next(x.address for x in xs if x.mnemonic == "int3")
    print(end - a)
win(0x00378437, 0x0037843D, "00378230 -> 003ABCA0")
win(0x0024BB5D, 0x0024BB6D, "0024B9B0 publisher call")
win(0x0024D6AA, 0x0024D6B2, "0024D540 mode test")
win(0x00262AF8, 0x00262B12, "002628B0 compaction calls")
win(0x0050E300, 0x0050E32B, "0050E300", entry=0x0050E300)
win(0x0050DEB0, 0x0050DF00, "0050DEB0", entry=0x0050DEB0)
win(0x002EF300, 0x002EF340, "002EF300", entry=0x002EF300)
win(0x002D78B0, 0x002D7910, "002D78B0", entry=0x002D78B0)
win(0x00582F09, 0x00582F0E, "00582860 -> 002814E0(-2)")
win(0x005829C0, 0x005829D0, "00582860 -> 003946B0(6)")
win(0x0058315C, 0x00583168, "00583040 -> 00244DD0")
win(0x0032E0F0, 0x0032E0F8, "pump -> 0035E810")
win(0x00583990, 0x00583A20, "00583990 head", entry=0x00583990)
for f, claim in ((0x00247510, 6), (0x00247870, 5), (0x00244960, 4), (0x005004C0, 3), (0x003B3C00, None)):
    s = rel_sites(f)
    print("callers of %08X: %d (paragraph: %s)" % (f, len(s), claim))
# 005004C0's dispatch: count distinct targets in its jump table (read its body for the table)
whole(0x005004C0, "005004C0 dispatch", maxn=40)
win(0x002478B1, 0x002478C8, "00247870 else path", entry=0x002478B1)
win(0x00262AFC, 0x00262B12, "002628B0 first compaction call", entry=0x00262AFC)
whole(0x0024FCF0, "0024ED80's tail target", maxn=40)
