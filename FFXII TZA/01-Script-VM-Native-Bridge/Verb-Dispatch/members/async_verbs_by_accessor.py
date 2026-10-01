"""Which script verbs are asynchronous - read the way the engine's own accessors read the dispatch table.

The three accessors (003DC270 begin, 003DC240 poll, 003DC2A0 result) index family 0's table at 01EED700 as
    begin(n)  = [tbl + 0x20*n + 0x08]
    poll(n)   = [tbl + 0x20*n + 0x10]
    result(n) = [tbl + 0x20*n + 0x20]
A verb is asynchronous when it has a begin or a poll callback.

This script lists every such call id with its authored name (from the bundled ff12-script catalogue, an external
community source: a name is a lead, not proof) and compares the begin/poll columns of scriptvm-dispatch.tsv against
the accessor frame for call id n and for n + 1.

Controls: the table's count dword must be 1496, and every `handler` value of the TSV must equal result(n).
"""
import re, struct, sys

ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
EXE = ROOT + r"\Database\Tools\work\exe\FFXII_TZA.exe"
TSV = ROOT + r"\Database\FFXII TZA\01-Script-VM-Native-Bridge\Verb-Dispatch\scriptvm-dispatch.tsv"
CAT = ROOT + r"\Collaboration\tools\ffxii\ff12-script-master\ff12-script\CScriptContainerInitializers.cpp"
TBL = 0x01EED700

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, rs, ro))


def q(va):
    r = va - 0x120000
    for v, rs, ro in secs:
        if v <= r < v + rs:
            return struct.unpack_from("<Q", d, ro + r - v)[0]
    raise ValueError(hex(va))


count = q(TBL) & 0xFFFFFFFF
B = lambda n: q(TBL + 0x20 * n + 0x08)
P = lambda n: q(TBL + 0x20 * n + 0x10)
R = lambda n: q(TBL + 0x20 * n + 0x20)

cat = {}
for m in re.finditer(r'\{\s*0x([0-9A-Fa-f]{4})\s*,\s*\{\s*L"([^"]+)"', open(CAT, encoding="utf-8", errors="replace").read()):
    cat.setdefault(int(m.group(1), 16), m.group(2))

HEX8 = re.compile(r"^[0-9A-Fa-f]{8}$")
hx = lambda s: int(s, 16) if HEX8.match(s.strip()) else 0
rows = []
for line in open(TSV, encoding="utf-8", errors="replace"):
    r = line.rstrip("\n").split("\t")
    if re.match(r"^[0-9A-Fa-f]{4}$", r[0]):
        rows.append((int(r[0], 16), r[1], hx(r[3]) if len(r) > 3 else 0, hx(r[6]) if len(r) > 6 else 0, hx(r[7]) if len(r) > 7 else 0))

res_ok = sum(1 for n, _, res, _, _ in rows if res == R(n))
bp = [(n, nm, b, p) for n, nm, _, b, p in rows if b or p]
same = sum(1 for n, _, b, p in bp if (b, p) == (B(n), P(n)))
nxt = sum(1 for n, _, b, p in bp if n + 1 < count and (b, p) == (B(n + 1), P(n + 1)))
asyncs = [n for n in range(count) if B(n) or P(n)]
in_tsv = {n for n, *_ in rows}

print("# control: table count dword = %d (expected 1496)" % count)
print("# control: TSV rows %d, handler == accessor result(n) in %d" % (len(rows), res_ok))
print("# TSV rows carrying begin/poll: %d ; equal to accessor (begin, poll)(n): %d ; equal to (begin, poll)(n+1): %d" % (len(bp), same, nxt))
print("# asynchronous call ids by the accessor frame: %d ; of them with a row in the TSV: %d ; with an authored name: %d"
      % (len(asyncs), sum(1 for n in asyncs if n in in_tsv), sum(1 for n in asyncs if n in cat)))
print("call_id\tauthored_name\tbegin\tpoll\tresult\thas_tsv_row")
for n in asyncs:
    f = lambda v: ("%08X" % v) if v else "-"
    print("%04X\t%s\t%s\t%s\t%s\t%s" % (n, cat.get(n, "-"), f(B(n)), f(P(n)), f(R(n)), "yes" if n in in_tsv else "no"))
if count != 1496 or res_ok != len(rows):
    sys.exit("CONTROL FAILED")
