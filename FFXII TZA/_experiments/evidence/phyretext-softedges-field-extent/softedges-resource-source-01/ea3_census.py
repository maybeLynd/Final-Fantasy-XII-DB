"""EA-3: what the shipped shader clusters store in bits 13-15 of PShaderParameterDefinition.m_bufferLoc.m_size.

Question: the engine reads the definition's u16 at +0x12 (m_bufferLoc.m_size) and masks it with 0x1FFF in all 110
reads; the word is registered whole and comes from the asset. What do the assets put in bits 13-15?
Discriminator: every shipped definition record, located through the file's OWN packed namespace, read at its u16.

Route (OPUS, independent of FABLE's unpublished 2026-09-26 scratch draft, which reached the same census by name
lookup): the header and namespace are parsed per CONTRACT-phyre-packed-namespace.md and CONTRACT-phyre-cluster-header.md
with the two mandatory per-file controls (BOM 0x01020304; namespace size word == header m_packedNamespaceSize) and the
size closure 0x20 + 4A + 36B + 24C + D; m_bufferLoc's class is resolved through the member's TYPE REFERENCE
(nTypes + 1-based class id, CX-3), not by name; the record width is the class word w1's low 28 bits and must satisfy
m_objectsSize == m_count * width exactly; the list's data offset is the running sum of the lists' m_size (CU-3).

Controls:
  C1 population   files carrying the class == header-class clusters (2,184 per CU-2)
  C2 sensitivity  the same loop reading the high half of m_constantBufferLocation flags records (the 0xFFFFFFFF
                  sentinel), so the instrument reports set top bits when they exist
  C3 mutation     one record's size word in a copy of a real file has bit 13 set; the reader must count exactly 1
  C4 layout       every file's schema gives the same record layout; any other layout is reported, not assumed
  C5 extent       each list's m_objectsSize == count x width rounded up to even, else the file fails the run
Usage: python ea3_census.py [extract_root]  -> result.json beside this script.
"""
import os, sys, struct, hashlib, collections, json, pathlib

ROOT = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract"
HERE = pathlib.Path(__file__).resolve().parent
TARGETS = ("PShaderParameterDefinition", "PShaderStreamDefinition")


def parse(data):
    """-> (classes, lists, data_start) or raise ValueError naming the failed control."""
    if data[:4] != b"RYHP":
        raise ValueError("marker")
    hsz, nssz, _plat, nlists = struct.unpack_from("<IIII", data, 4)
    ns = data[hsz:hsz + nssz]
    bom, nsz, nT, nC, nM, D = struct.unpack_from("<6I", ns, 0)
    if bom != 0x01020304 or nsz != nssz:
        raise ValueError("namespace control")
    if 0x20 + 4 * nT + 36 * nC + 24 * nM + D != nssz:
        raise ValueError("size closure")
    coff = 0x20 + 4 * nT; moff = coff + 36 * nC; poff = moff + 24 * nM
    name = lambda o: ns[poff + o:ns.index(b"\0", poff + o)].decode("latin1")
    classes, mi = [], 0
    for c in range(nC):
        w = struct.unpack_from("<9I", ns, coff + 36 * c)
        mem = {}
        for k in range(w[3]):
            m = struct.unpack_from("<6I", ns, moff + 24 * (mi + k))
            mem[name(m[0])] = {"type": m[1], "off": m[2], "width": m[3], "attr": m[4], "bound": m[5]}
        mi += w[3]
        classes.append({"name": name(w[2]), "w1": w[1], "members": mem})
    if mi != nM:
        raise ValueError("member sum")
    off = hsz + nssz
    lists = [struct.unpack_from("<9I", data, off + 36 * i) for i in range(nlists)]
    return classes, lists, nT, off + 36 * nlists


def read_file(data, st, hist, cbl_hist, low13, examples, path):
    classes, lists, nT, cur = parse(data)
    for tname in TARGETS:
        ids = [i for i, c in enumerate(classes) if c["name"] == tname]
        if not ids:
            continue
        c = classes[ids[0]]; st[tname + " files"] += 1
        bl = c["members"]["m_bufferLoc"]
        sub = classes[bl["type"] - nT - 1]               # CX-3: type ref >= nTypes -> nTypes + 1-based class id
        if bl["type"] < nT or sub["name"] != "PShaderParameterCaptureBufferLocationSize":
            raise ValueError("m_bufferLoc type ref does not resolve to the capture-location class")
        so = sub["members"]["m_size"]
        if so["width"] != 2:
            raise ValueError("m_size width %d" % so["width"])
        width = c["w1"] & 0x0FFFFFFF
        cb = c["members"].get("m_constantBufferLocation")
        lay = (width, bl["off"], bl["width"], so["off"], cb and cb["off"], cb and cb["width"])
        st[tname + " layout " + json.dumps(lay)] += 1
        pos = cur
        for L in lists:
            if L[0] - 1 == ids[0]:
                st[tname + " lists"] += 1
                # C5: the objects region is the packed records, rounded up to an even length (a 13-byte record count
                # that is odd carries one pad byte: first seen on materialsphere.dae, 121 records, 1,574 bytes)
                if L[3] != (L[1] * width + 1) & ~1:
                    raise ValueError("objectsSize %d != even(count %d x width %d)" % (L[3], L[1], width))
                st[tname + " objects pad %d" % (L[3] - L[1] * width)] += 1
                for k in range(L[1]):
                    r = pos + k * width
                    size = struct.unpack_from("<H", data, r + bl["off"] + so["off"])[0]
                    st[tname + " records"] += 1; hist[tname][size >> 13] += 1
                    low13[tname] = max(low13[tname], size & 0x1FFF)
                    if size >> 13 and len(examples) < 20:
                        examples.append([path, tname, k, hex(size)])
                    if cb and cb["width"] == 4:
                        hi = struct.unpack_from("<H", data, r + cb["off"] + 2)[0]
                        cbl_hist[tname][hi >> 13] += 1
                        if struct.unpack_from("<I", data, r + cb["off"])[0] == 0xFFFFFFFF:
                            st[tname + " cbl sentinel 0xFFFFFFFF"] += 1
            pos += L[2]
        if pos > len(data):
            raise ValueError("list walk overruns the file")


def main():
    st = collections.Counter(); hist = collections.defaultdict(collections.Counter)
    cbl = collections.defaultdict(collections.Counter); low13 = collections.Counter(); ex = []
    digest = hashlib.sha256(); distinct = set(); mutation_seed = None
    files = []
    for dp, _dn, fn in os.walk(ROOT):
        files += [os.path.join(dp, f) for f in fn if f.lower().endswith(".phyre")]
    files.sort()
    for p in files:
        st["phyre files"] += 1
        data = open(p, "rb").read()
        try:
            parse(data)
        except ValueError as e:
            st["rejected: " + str(e)] += 1; continue
        if b"PShaderParameterDefinition\0" not in data:
            continue
        h = hashlib.md5(data).hexdigest(); distinct.add(h)
        digest.update((os.path.relpath(p, ROOT).replace("\\", "/") + " " + h + "\n").encode())
        read_file(data, st, hist, cbl, low13, ex, os.path.relpath(p, ROOT).replace("\\", "/"))
        if mutation_seed is None:
            mutation_seed = p
    # C3 mutation: set bit 13 of the first definition record's size word in a copy of a real file
    data = bytearray(open(mutation_seed, "rb").read())
    classes, lists, nT, cur = parse(bytes(data))
    i = [k for k, c in enumerate(classes) if c["name"] == TARGETS[0]][0]
    pos = cur
    for L in lists:
        if L[0] - 1 == i:
            break
        pos += L[2]
    bl = classes[i]["members"]["m_bufferLoc"]; so = classes[bl["type"] - nT - 1]["members"]["m_size"]
    struct.pack_into("<H", data, pos + bl["off"] + so["off"],
                     struct.unpack_from("<H", data, pos + bl["off"] + so["off"])[0] | 0x2000)
    mst = collections.Counter(); mh = collections.defaultdict(collections.Counter)
    read_file(bytes(data), mst, mh, collections.defaultdict(collections.Counter), collections.Counter(), [], "mutant")
    mutant_flagged = sum(v for k, v in mh[TARGETS[0]].items() if k)
    out = {
        "root": ROOT, "stats": dict(sorted(st.items())),
        "distinct_contents_with_class": len(distinct),
        "input_digest_sha256": digest.hexdigest(),
        "size_bits13_15_hist": {t: {str(k): v for k, v in sorted(h.items())} for t, h in hist.items()},
        "max_low13": dict(low13),
        "C2_cbl_high_bits13_15_hist": {t: {str(k): v for k, v in sorted(h.items())} for t, h in cbl.items()},
        "C3_mutation": {"seed": os.path.relpath(mutation_seed, ROOT).replace("\\", "/"), "flagged": mutant_flagged},
        "examples_bits_set": ex,
    }
    ok = (st.get("PShaderParameterDefinition files") == 2184 and mutant_flagged == 1
          and sum(v for k, v in cbl[TARGETS[0]].items() if k) > 0
          and len([k for k in st if k.startswith("PShaderParameterDefinition layout")]) == 1
          and not [k for k in st if k.startswith("rejected")])
    out["controls_pass"] = ok
    (HERE / "result.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
