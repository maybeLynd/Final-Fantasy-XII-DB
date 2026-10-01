"""frp_bounds.py - OV-26, the authored-format half: do shipped @FRP containers keep their offsets in bounds, and how are
entries aligned? (FABLE, Claude Opus 5.5, 2026-09-29). DATA: every .ca, .cm and every @FRP block in every .mot PKFL pack.

Layout (the FRP container page §2-3, and resource-section-addressing's child selector): header 0x30 bytes {'@FRP', variant,
contentLength, entryCount, name[16], 4 zero dwords}; variant 0: u32 offset[entryCount] at +0x30, relative to +0x30;
variant 1: the table at +0x40 relative to +0x40, and a zero offset means an empty slot.
  V  every container: magic '@FRP', variant 0 or 1, contentLength <= its block, the offset table ends inside the content
  O  every non-empty entry: base + offset + 4 <= contentLength (the 4-byte id fits), and the id is '@F' + two letters
  A  alignment of every entry start relative to the container, reported as a distribution (the guarantee is whatever it is)
  M  sensitivity: the same offsets read FILE-relative (the page's named trap) must break the id check for most entries,
     so O discriminates the base it assumes
Not claimed: the loader's allocation-failure behaviour (static, other half of OV-26); bytes inside each entry.
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
stats = collections.Counter(); bad = collections.defaultdict(list); align = collections.Counter(); ids = collections.Counter()
near = 0; wrong = 0
def container(blob, where):
    global near, wrong
    stats["containers"] += 1
    if len(blob) < 0x30 or blob[:4] != b"@FRP":
        bad["V magic"].append(where); return
    var, clen, cnt = U32(blob, 4), U32(blob, 8), U32(blob, 0xC)
    stats["v%d" % var] += 1
    if var not in (0, 1): bad["V variant"].append(where); return
    if clen > len(blob): bad["V contentLength"].append((where, clen, len(blob))); return
    base = 0x30 if var == 0 else 0x40
    if base + 4 * cnt > clen: bad["V table"].append((where, cnt, clen)); return
    for k in range(cnt):
        o = U32(blob, base + 4 * k)
        if var == 1 and o == 0:
            stats["empty slots"] += 1; continue
        stats["entries"] += 1
        s = base + o
        if s + 4 > clen:
            bad["O offset"].append((where, k, o, clen)); continue
        tag = blob[s:s + 4]
        ids[tag] += 1
        if not (tag[:2] == b"@F" and all(65 <= c <= 90 for c in tag[2:])): bad["O id"].append((where, k, tag))
        for a in (0x800, 0x100, 0x40, 0x10, 4):
            if s % a == 0: align[a] += 1; break
        else: align[1] += 1
        t2 = blob[o:o + 4]
        if not (t2[:2] == b"@F" and all(65 <= c <= 90 for c in t2[2:])): wrong += 1
for path in sorted(names):
    low = path.lower()
    if not (low.endswith(".ca") or low.endswith(".cm") or low.endswith(".mot")): continue
    try: b = V.read_entry(f, names, blocks, path)
    except Exception: stats["unreadable"] += 1; continue
    if low.endswith(".mot"):
        if b[:4] != b"PKFL": stats["mot not PKFL"] += 1; continue
        stats["mot packs"] += 1
        n = U32(b, 4)
        for i in range(n):
            o, sz = U32(b, 8 + 8 * i), U32(b, 12 + 8 * i)
            if o == 0 and sz == 0: continue
            blk = b[o:o + sz]
            if blk[:4] == b"@FRP": container(blk, "%s#%d" % (path, i))
            else: stats["mot slots not @FRP"] += 1
    else:
        container(b, path)
check("V", stats["containers"] > 10000 and not any(k.startswith("V") for k in bad),
      "%d containers (%d .mot packs; variant0 %d, variant1 %d); header/table violations: %s"
      % (stats["containers"], stats["mot packs"], stats["v0"], stats["v1"], {k: len(v) for k, v in bad.items() if k.startswith("V")}))
check("O", stats["entries"] > 10000 and not bad["O offset"] and not bad["O id"],
      "%d entries (%d empty variant-1 slots); offsets past the content: %d; ids not '@F'+2 letters: %d; tags %s"
      % (stats["entries"], stats["empty slots"], len(bad["O offset"]), len(bad["O id"]), dict(ids.most_common(12))))
print("      entry-start alignment (largest power of two dividing it, of 0x800/0x100/0x40/0x10/4/1): %s" % dict(align))
print("      .mot slots that are not @FRP: %d; unreadable files: %d" % (stats["mot slots not @FRP"], stats["unreadable"]))
check("M", wrong > stats["entries"] // 2, "sensitivity: read file-relative, %d of %d entry ids fail the check" % (wrong, stats["entries"]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
