"""producers.py - OV-39: what shipped data guarantees for the nonempty registration's names, file-size metadata, offset
tables and optional configuration (FABLE, Claude Opus 5.5, 2026-09-29). DATA: every .ca, .cm and .mot @FRP container.

The registration 00409FE0 looks up an @FEF section by tag; with one present it folds the root name's last five characters
into an index of the configuration table 02B64380, reads the parser offset as the dword at roundup64(size) - 4 of the
loaded source, and builds the effect from there (the fef page; the nonempty-registration page).

  F  WHO CARRIES @FEF: every @FEF entry in the shipped @FRP corpus is in a .cm under ps2data/obj_finish/in/; no .mot or .ca
     container has one (count and paths)
  M  THE METADATA DWORD: for each carrier, the dword at roundup64(size) - 4 is read under both sizes the loader could
     see - the archive entry's size and the container's own contentLength - and compared with the file offset of the
     carrier's EFX data (and with that offset relative to the @FEF entry). It never locates it
  N  NAMES: every container's 16-byte name field (+0x10) and every @FEF entry's name field (+0x0C) is NUL-terminated
     within its field
  Offset tables: ../ov26-frp-bounds-fable/frp_bounds.py V O M (all 320,736 entries in bounds) - not repeated here.
  Configuration: the fef page shows 02B64380 is never populated in the shipped build (its only populator 0040A230 is
     dead-stripped), so the arm faults at 0040A135 before the metadata step - not repeated here.
     CORRECTED 2026-09-29 (CON-195): 02B64380 IS seeded at start-up (0041E3A0 -> 00409F80 -> 0040A230, 144 obj_finish
     paths); the two lines above are history. This script does not test the configuration input either way.
  K  sensitivity: the EFX data of each carrier is found (so M compares against a real offset), and M's comparison accepts
     the true offset when it is planted as the last dword
"""
import collections, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "agent_flow", "tools"))
import vbfextract as V
VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
f = io.open(VBF, "rb"); names, blocks = V.load_index(f)
st = collections.Counter(); carriers = []; badname = []
def container(blob, where, is_file):
    st["containers"] += 1
    if blob[:4] != b"@FRP": return
    if b"\0" not in blob[0x10:0x20]: badname.append(where)
    var, clen, cnt = U32(blob, 4), U32(blob, 8), U32(blob, 12); base = 0x30 if var == 0 else 0x40
    for k in range(cnt):
        o = U32(blob, base + 4 * k)
        if var == 1 and o == 0: continue
        s = base + o
        if blob[s:s + 4] == b"@FEF":
            st["fef"] += 1
            if b"\0" not in blob[s + 0x0C:s + 0x1C]: badname.append(where + "#@FEF")
            carriers.append((where, blob, clen, s, is_file))
for path in sorted(names):
    low = path.lower()
    if not low.endswith((".ca", ".cm", ".mot")): continue
    b = V.read_entry(f, names, blocks, path)
    if low.endswith(".mot"):
        if b[:4] != b"PKFL": continue
        for i in range(U32(b, 4)):
            o, sz = U32(b, 8 + 8 * i), U32(b, 12 + 8 * i)
            if o or sz: container(b[o:o + sz], "%s#%d" % (path, i), False)
    else:
        container(b, path, True)
paths = [w for w, *_ in carriers]
check("F", len(carriers) == 144 and all(p.lower().endswith(".cm") and p.lower().startswith("ps2data/obj_finish/in/") for p in paths),
      "%d @FEF entries in %d containers; all in .cm under ps2data/obj_finish/in/: %s" % (len(carriers), st["containers"],
      all(p.lower().endswith(".cm") and p.lower().startswith("ps2data/obj_finish/in/") for p in paths)))
def dword_at_end(b, n):
    r = (n + 0x3F) & ~0x3F
    return U32(b + b"\0" * max(0, r - len(b)), r - 4)
hits = collections.Counter(); found = 0; planted = 0
for where, b, clen, s, is_file in carriers:
    efx = b.find(b"EFX00", s)
    found += 0 <= efx - s <= 0x40
    targets = (efx, efx - s)
    for label, n in (("archive size", len(b)), ("contentLength", clen)):
        dw = dword_at_end(b, n)
        hits[(label, "locates the EFX data" if dw in targets else ("0" if dw == 0 else "another value"))] += 1
    r = (len(b) + 0x3F) & ~0x3F
    pb = bytearray(b + b"\0" * (r - len(b))); struct.pack_into("<I", pb, r - 4, efx)
    planted += dword_at_end(bytes(pb), len(b)) in targets
check("M", not any(k[1] == "locates the EFX data" for k in hits),
      "the dword at roundup64(size) - 4 never locates the carrier's EFX data: %s" % dict(sorted(hits.items())))
check("N", not badname, "container and @FEF entry names NUL-terminated within their 16 bytes (%d exceptions)" % len(badname))
check("K", found == len(carriers) and planted == len(carriers),
      "sensitivity: EFX data found in all %d carriers (within 0x40 of the @FEF entry); a planted true offset is accepted %d/%d"
      % (found, planted, len(carriers)))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
