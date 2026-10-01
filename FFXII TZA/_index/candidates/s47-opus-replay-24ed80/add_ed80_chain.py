"""OPUS block 289 scratch-copy patch: load 0024ED80's real chain so the block-265 case can run it.
0024ED80 (0x84 B, ends with jmp 0024FCF0 at 0024EDFF) -> 0024FCF0 (162 B) -> 003A2B20 (53 B leaf).
Data they touch: 02096800..02096843 (0024FCF0 stores), 022D8F30 / 022D92E0..022D92FF (003A2B20 stores),
02AEE7F4 (0024FD86 store), 01CEBBA8 (.rdata 1.0f read at 0024FD2E). Pages mapped and the .rdata page loaded from the EXE."""
p = "check.py"
s = open(p, encoding="utf-8", newline="").read()
CR = "\r\n" in s
s = s.replace("\r\n", "\n")
if "OPUS block 289" not in s:
    a = "          0x20E600: 10, 0x20E620: 9}\n"
    assert a in s
    s = s.replace(a, "          0x20E600: 10, 0x20E620: 9,\n"
                     "          0x24ED80: 0x84, 0x24FCF0: 0xA2, 0x3A2B20: 0x35}   # OPUS block 289: 0024ED80 real chain\n")
    b = "                   (0x60000000, 0x4000)]:\n"
    assert b in s
    s = s.replace(b, "                   (0x60000000, 0x4000),\n"
                     "                   (0x02096000, 0x1000), (0x022D8000, 0x2000), (0x02AEE000, 0x1000),\n"
                     "                   (0x01CEB000, 0x1000)]:   # OPUS block 289: pages the 0024ED80 chain touches\n")
    c = "    u.mem_write(DEC_BASE, struct.pack('<Q', base))\n"
    assert c in s
    s = s.replace(c, "    u.mem_write(0x01CEB000, extract(0x01CEB000, 0x1000))   # OPUS block 289: .rdata page (1.0f at 01CEBBA8)\n" + c)
    open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if CR else s)
print("ok")
