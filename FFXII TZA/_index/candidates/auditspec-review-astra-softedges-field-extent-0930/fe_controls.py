"""SWE2-AUDIT-SPEC controls for phyretext-softedges-field-extent. Nothing is written into the packet.
(1) cross-check the reducer's decoded name fixups against this review's own string starts / record bytes;
(2) in-memory mutations of the shipped bytes, including the exact AE0 threshold on both sides;
(3) actual CLI refusals on disposable copies under C:\\t\\auditspec (not retained here, only exits/stderr tails)."""
import importlib.util, json, pathlib, shutil, struct, subprocess, sys, tempfile, os
P = pathlib.Path(r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_experiments\evidence\phyretext-softedges-field-extent")
HERE = pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("reducer", P / "reduce-softedges-field-extent.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
ship = open(r"D:\FFXII_TZA_extract\gamedata\d3d11\artdata\shaders\phyretext.fx.phyre", "rb").read()
res = json.load(open(HERE / "rerun-result.json"))
# (1) bijection: decoded array offsets == string starts in the 164-byte region; record bytes == raw bytes
a0 = 29380; reg = ship[a0:a0 + 164]; starts = []; i = 0
while i < 164:
    z = reg.find(b"\0", i)
    if z < 0: break
    if z > i: starts.append(i)
    i = z + 1
offs = sorted(r["name_array_offset"] for r in res["records"])
print("string starts", starts); print("decoded offsets == string starts:", offs == starts)
print("keys", sorted({tuple(r["array_fixup"])[0] for r in res["records"]}), "indices", sorted(r["index"] for r in res["records"]) == list(range(12)))
print("record bytes match raw:", all(ship[r["record_file_start"]:r["record_file_start"] + 13].hex() == r["record_bytes"] for r in res["records"]))
for r in res["records"]: print("  idx %2d %-18s off %3d size %2d fixup %s" % (r["index"], r["name"], r["capture_offset"], r["masked_size"], r["array_fixup"]))
print("max masked size over all 12:", max(r["masked_size"] for r in res["records"]))
# (2) mutations
sel = res["selected"]; rec = sel["record_file_start"]
def run(name, data):
    try: out = R.analyze(data)
    except Exception as e: print("MUT %-34s REFUSED %s: %s" % (name, type(e).__name__, str(e)[:70])); return None
    c = out["conditional_copy"]; print("MUT %-34s len=%d any_AE0=%s whole_AE0=%s" % (name, c["length"], c["reads_any_AE0"], c["reads_whole_AE0"])); return out
run("shipped", ship)
for v in (0x9C0, 0x9C1, 0x9C3, 0x9C4, 0x29C1):
    b = bytearray(ship); struct.pack_into("<H", b, rec + 7, v); run("size word 0x%X" % v, bytes(b))
b = bytearray(ship); struct.pack_into("<H", b, rec + 5, 0x9C0); run("offset word 0x9C0 (size 8)", bytes(b))
b = bytearray(ship); b[sel["name_file_start"]] = ord("X"); run("name softEdges->XoftEdges", bytes(b))
h = struct.unpack_from("<21I", ship); ns = h[1]; nt = struct.unpack_from("<I", ship, ns + 8)[0]
b = bytearray(ship); struct.pack_into("<I", b, ns + 32 + 4 * nt + 36 * 43, 0); run("class44 parent word -> 0", bytes(b))
ms = 32 + 4 * nt + 36 * 78  # member table; class 44's single member m_size is found by name offset 0x822
hits = [k for k in range(239) if struct.unpack_from("<I", ship, ns + ms + 24 * k)[0] == 0x822]
cnt = [struct.unpack_from("<I", ship, ns + 32 + 4 * nt + 36 * c + 12)[0] for c in range(78)]
j = sum(cnt[:43])  # class 44 (index 43): its only member, by cumulative member counts
print("members named m_size (name offset 0x822):", hits, " class44's member index:", j)
b = bytearray(ship); struct.pack_into("<I", b, ns + ms + 24 * hits[0] + 8, 0); run("first m_size (other class) off -> 0", bytes(b))
b = bytearray(ship); struct.pack_into("<I", b, ns + ms + 24 * j + 8, 0); run("class44 m_size member offset 2 -> 0", bytes(b))
# swap the two alphabetically adjacent names' records would need fixup re-encoding; instead swap record 8 and record 1 bytes
b = bytearray(ship); r1 = 29237; b[rec:rec + 13], b[r1:r1 + 13] = ship[r1:r1 + 13], ship[rec:rec + 13]; run("swap record bytes 8<->1", bytes(b))
# (3) CLI on disposable copies
T = pathlib.Path(r"C:\t\auditspec"); T.mkdir(parents=True, exist_ok=True)
tmp = pathlib.Path(tempfile.mkdtemp(prefix="fe-cli-", dir=str(T)))
def cli(name, alter):
    dd = tmp / name; dd.mkdir()
    for p in (P / "softedges-resource-source-01").iterdir():
        if p.is_file(): shutil.copyfile(p, dd / p.name)
    alter(dd); out = dd / "MUST-NOT-EXIST.json"
    r = subprocess.run([sys.executable, "-B", str(P / "reduce-softedges-field-extent.py"), str(dd), str(out)], capture_output=True, text=True, timeout=60)
    print("CLI %-28s exit=%d result_exists=%s stderr_tail=%s" % (name, r.returncode, out.exists(), (r.stderr.strip().splitlines() or [""])[-1][:90]))
def nochange(dd): pass
def incomplete(dd):
    p = dd / "original-code-raw-01.json"; j = json.loads(p.read_text()); j["wrapper_complete"] = False; p.write_text(json.dumps(j))
def missing(dd): (dd / "constructor-source-retained-01.json").unlink()
def asset(dd):
    b = bytearray(ship); struct.pack_into("<H", b, rec + 7, 0x9C4); (dd / "phyretext.fx.phyre").write_bytes(bytes(b))
def instr(dd):  # change one expected instruction record (the copy source displacement) without touching the span hash
    p = dd / "original-code-raw-01.json"; s = p.read_text(); p.write_text(s.replace("r10, [rsi + 0x118]", "r10, [rsi + 0x9c8]", 1))
cli("unchanged-copy (positive)", nochange); cli("incomplete-source", incomplete); cli("missing-caller", missing)
cli("changed-shipping-asset", asset); cli("changed-copy-displacement", instr)
print("disposable dir", tmp)
