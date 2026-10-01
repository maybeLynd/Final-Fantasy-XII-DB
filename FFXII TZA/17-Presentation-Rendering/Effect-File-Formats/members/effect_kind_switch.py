"""effect_kind_switch.py: the definition-kind switch inside 00441970.

00441970(instance) gates its element-chain walk on a switch over the definition
kind byte [[instance+0x108]+0x44], range 0x40..0xD0 (add edx,-0x40 / cmp edx,0x90 /
ja tail). Byte map 00441A98, dword RVA table 00441A90, targets = image base + RVA,
jmp rcx. Decodes to exactly two targets: 004419D0 (set render byte 02AEE910 from
definition +0x4A/+0x4C, then walk the element chains) and 00441A89 (function tail:
add rsp,0x20 / pop rdi / ret - the chains are NOT walked).

Writes effect-kind-441970.tsv beside this script: kind, slot, target, action.
Run from the repository root (needs the image under Database/Tools/work/exe)."""
import os, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
ns = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 12)[0],
         struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 8)[0],
         struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 20)[0]) for i in range(ns)]
def off(va):
    r = va - BASE
    for a, vs, ro in secs:
        if a <= r < a + vs:
            return ro + r - a
BM, OT = 0x441A98, 0x441A90          # byte map, dword RVA table (from 004419B5/004419BC/004419C4)
rows = []
for t in range(0x91):                # selector 0x40..0xD0
    c = d[off(BM) + t]
    target = BASE + struct.unpack_from("<I", d, off(OT) + 4 * c)[0]
    rows.append((t + 0x40, c, target))
cnt = collections.Counter(t for _, _, t in rows)
assert len(cnt) == 2, cnt            # degenerate: render-byte arm and the function tail
with open(os.path.join(HERE, "effect-kind-441970.tsv"), "w", encoding="utf-8", newline="\n") as fo:
    fo.write("kind\tslot\ttarget\taction\n")
    for k, c, t in rows:
        act = "set 02AEE910 from def +0x4A/+0x4C, then walk element chains" if t == 0x4419D0 \
              else "return (element chains not walked)"
        fo.write("0x%02X\t%d\t%08X\t%s\n" % (k, c, t, act))
print("written: %d rows, %d walk kinds, %d return kinds"
      % (len(rows), sum(1 for _, _, t in rows if t == 0x4419D0),
         sum(1 for _, _, t in rows if t == 0x441A89)))
