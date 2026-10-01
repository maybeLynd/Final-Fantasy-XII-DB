"""B6 test_battle/<lang>/binaryfile/shop_data.bin and wepjob_matrix.bin vs the same folder's battle_pack.bin.
Claim: each standalone file == the first len(file) bytes of a battle_pack directory section (WepJob_Matrix = entry 0,
directory +0x04; shop_data = entry 39, directory +0xA0), the section's remaining bytes zero padding; the section is
bound by 00236C30 (WepJob +4 -> 02EBF180 at 00236C70-00236C74) / 00238660 (shop +0xA0 -> 02EBF158); the standalone
files are kind-2 path entries 0 and 39 with no requester among the kind-2 request sites."""
import struct
from common import *
header()
print("== static")
check("kind 2 idx 0 = WepJob_Matrix.bin", (kind_path(2, 0) or "").endswith("WepJob_Matrix.bin"), kind_path(2, 0))
check("kind 2 idx 39 = shop_data.bin", (kind_path(2, 39) or "").endswith("shop_data.bin"), kind_path(2, 39))
check("kind 2 idx 0x13 = battle_pack.bin", (kind_path(2, 0x13) or "").endswith("battle_pack.bin"), kind_path(2, 0x13))
expect_ins(0x2369C2, "mov ecx, 0x13"); expect_ins(0x2369CE, "call 0x3843f0")
expect_ins(0x236C5B, "mov ecx, 0x13"); expect_ins(0x236C6B, "jmp 0x3843f0")
expect_ins(0x384443, "mov ecx, 2"); expect_ins(0x38444E, "call 0x32e400")
expect_ins(0x236C70, "movsxd rax, dword ptr [rcx + 4]")
check("00236C74 stores directory +4 into 02EBF180", rip_target(0x236C74) == 0x2EBF180)
# the other two callers of the kind-2 loader 00384420: board files 0x47+n, and the message table 01E09F68
expect_ins(0x23836A, "add ecx, 0x47")
tab = d[off(0x1E09F68):off(0x1E09F68) + 0x1C]
check("message-loader id table 01E09F68 (28 entries) holds neither 0 nor 39", 0 not in tab and 39 not in tab, tab.hex())
check("board loader ids 0x47.. cannot be 0 or 39 for a non-negative board index", 0x47 > 39)
cp = open("callpairs_kind2.txt").read()
api = [l for l in cp.splitlines() if any(t in l for t in ("call 0x32e4", "call 0x32e6", "call 0x3843", "call 0x3844", "call 0x24ab90"))]
check("no (2,0)/(2,0x27) constant pair at any call to 0032E400/0032E620/003843F0/00384420/0024AB90", not api, str(api))
check("00238678/00238686: the shop binder rebases 02EBF158", rip_target(0x238678) == 0x2EBF158 and rip_target(0x238686) == 0x2EBF158)
sw = open("b6_refsweep_02EBF158.txt").read()
check("02EBF158 readers outside the binder: 002FA920 (listing) and 002FAE40 (name) only", all(f in sw for f in ("002FA920", "002FAE40")) and "(a) rip-relative confirmed: 13" in sw)
check("0032042D reads WepJob 02EBF180; 00320434 u16 stride; 0032043C byte row [ptr + stride*cat + 4]",
      rip_target(0x32042D) == 0x2EBF180 and "word ptr [rcx]" in ins_at(0x320434) and "[rax + rcx + 4]" in ins_at(0x32043C))
print("== corpus")
for name, sec in (("wepjob_matrix", 0), ("shop_data", 39)):
    files = copies(f"ps2data/image/ff12/test_battle/*/binaryfile/{name}.bin")
    check(f"{name}: 4 standalone copies (ch, cn, in, kr)", sorted(f.replace('\\', '/').split('/')[-3] for f in files) == ["ch", "cn", "in", "kr"])
    for f in files:
        s = open(f, "rb").read()
        pk = open(f.replace(f"{name}.bin", "battle_pack.bin"), "rb").read()
        n = struct.unpack_from("<I", pk, 0)[0]
        offs = struct.unpack_from("<%dI" % n, pk, 4)
        a, e = offs[sec], offs[sec + 1]
        body = pk[a:e]
        check(f"{f.replace(chr(92), '/').split('/')[-3]}/{name}: == battle_pack entry {sec} (dir +{4 + 4 * sec:#x}) bytes [0,{len(s)}), "
              f"tail {len(body) - len(s)} B zero", body[:len(s)] == s and set(body[len(s):]) <= {0} and len(body) - len(s) < 8)
    # the section in the five pack-only languages is identical too
    secs_all = set()
    for pkf in copies("ps2data/image/ff12/test_battle/*/binaryfile/battle_pack.bin"):
        pk = open(pkf, "rb").read(); n = struct.unpack_from("<I", pk, 0)[0]; offs = struct.unpack_from("<%dI" % n, pk, 4)
        secs_all.add(pk[offs[sec]:offs[sec + 1]])
    check(f"{name}: section byte-identical in all 9 battle_pack copies", len(secs_all) == 1, str(len(secs_all)))
w = open(copies("ps2data/image/ff12/test_battle/in/binaryfile/wepjob_matrix.bin")[0], "rb").read()
stride, count = struct.unpack_from("<HH", w, 0)
check(f"wepjob_matrix: u16 stride {stride}, u16 count {count}, 4 + stride*count == {len(w)}", 4 + stride * count == len(w))
print("  wepjob rows:", list(w[4:]))
sh = open(copies("ps2data/image/ff12/test_battle/in/binaryfile/shop_data.bin")[0], "rb").read()
tag, st, cnt, data = struct.unpack_from("<IHHI", sh, 0)
check(f"shop_data header tag {tag:#x} stride {st} count {cnt} data {data:#x} (the shop page's ShopTableHeader)", (tag, st, cnt, data) == (0x64, 8, 57, 0xC))
# walk the three levels; every nested offset is relative to the SECTION start (the shop page's file-side convention)
def hdr(o): return struct.unpack_from("<IHHI", sh, o)
nsec = nlist = nid = 0; ok = True; gk = {}
for i in range(cnt):
    so = struct.unpack_from("<I", sh, data + st * i + 4)[0]
    t2, st2, c2, d2 = hdr(so); ok &= t2 == 0x164 and st2 == 8; nsec += 1
    for j in range(c2):
        g, opi, thr, lo = struct.unpack_from("<BBHI", sh, d2 + st2 * j); gk[g] = gk.get(g, 0) + 1
        t3, st3, c3, d3 = hdr(lo); ok &= t3 == 0x264 and st3 == 2 and d3 + 2 * c3 <= len(sh); nlist += 1; nid += c3
print("  gate kinds:", dict(sorted(gk.items())))
print(f"  walked {nsec} rows, {nlist} lists, {nid} ids")
check("three-level walk: every section tag 0x164 stride 8, every list tag 0x264 stride 2 in bounds; 267 entries / 2,512 ids as the shop page counts", ok and nlist == 267 and nid == 2512)
finish()
