"""Coast-down contract s8 regression (OPUS, 2026-09-27). The contract may not say, unstruck, that the subtype at +0x0CC
'comes from authored data': 00424D80 stores the record's current posted event there (00424FAB mov word ptr [rbx+0xcc], si),
and FABLE's bt4-event-motion-slots/ names the engine posters. FAILS on the contract before the correction.
Usage: python coastdown_source_check.py [exe] [contract]"""
import re, struct, sys, pathlib
EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
C = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else pathlib.Path(__file__).resolve().parents[3] / "17-Presentation-Rendering/CONTRACT-coast-down-latch.md")
d = open(EXE, "rb").read(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - BASE - va + ro for vs, va, rs, ro in secs if BASE + va <= v < BASE + va + rs)
store = d[off(0x424FAB):off(0x424FAB) + 7] == bytes.fromhex("6689b3cc000000")
live = re.sub(r"~~.*?~~", "", C.read_text(encoding="utf-8"), flags=re.S)
page = "comes from authored data" not in live
print("PASS" if store else "FAIL", "K1 00424FAB mov word ptr [rbx+0xcc], si")
print("PASS" if page else "FAIL", "K2 the contract no longer says the subtype comes from authored data")
print("FAILS", (not store) + (not page)); sys.exit(0 if store and page else 1)
