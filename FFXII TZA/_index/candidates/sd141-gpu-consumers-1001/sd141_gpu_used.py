"""sd141_gpu_used.py - SD-141 continued (OPUS, 2026-10-01): does any shipped shader READ the flying-fade pair?

Static chain (each step cited in the README):
  001C7940 stores the pair into 02CB8410 / 02CB8414 (the tunables block); 006084B0 hands the block to the copy 005DEC50
  (SWE2-AUDIT-SPEC's REJECT review); 00604750 writes the snapshot field by field through r14 = the pointer that
  006097B0 -> 00626060 returns, a mapped D3D11 buffer (00626060 logs "mapping buffer that was not created with
  D3D11_CPU_ACCESS_WRITE ..."); UQ-22's map (uq22-scenewide-cbuffer/map.tsv) places the two stores at
  SceneWideParameterConstantBuffer +0x5D4 mShadowFlyingFadeSpeed and +0x5DC mShadowFlyingFadeRange.

This checker reads every DXBC blob in the shipped .phyre shader packs that declares SceneWideParameterConstantBuffer
and counts, per variable, the blobs whose RDEF variable flags carry D3D_SVF_USED (0x2): the compiler sets that bit only
when the shader's code reads the variable. Controls: EyePosition and the non-flying pair mShadowFadeSpeed /
mShadowFadeRange must be USED somewhere (positive), and the layout must match UQ-22's (1 layout, 0x5F0 bytes, 154
variables). Input: the extracted archive (default D:/FFXII_TZA_extract). Prints PASS/FAIL and FAILS n."""
import collections, os, struct, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract"
WANT = ["mShadowFlyingFadeSpeed", "mShadowFlyingFadeRange", "mShadowFadeSpeed", "mShadowFadeRange", "EyePosition"]


def cstr(b, o):
    return b[o:b.index(b"\0", o)].decode("latin1")


def scenewide(blob):
    n = struct.unpack_from("<I", blob, 28)[0]
    for k in range(n):
        co = struct.unpack_from("<I", blob, 32 + 4 * k)[0]
        if blob[co:co + 4] != b"RDEF":
            continue
        r = blob[co + 8:co + 8 + struct.unpack_from("<I", blob, co + 4)[0]]
        cbn, cbo, _bn, _bo, ver, _pt, _fl, _cr = struct.unpack_from("<IIIIHHII", r, 0)
        vsz = 40 if (ver >> 8) & 0xFF >= 5 else 24
        for c in range(cbn):
            nm, vc, vo, sz, _cf, _ct = struct.unpack_from("<6I", r, cbo + 24 * c)
            if cstr(r, nm) != "SceneWideParameterConstantBuffer":
                continue
            out = {}
            for v in range(vc):
                base = vo + vsz * v
                vname = cstr(r, struct.unpack_from("<I", r, base)[0])
                off, size, flags = struct.unpack_from("<III", r, base + 4)
                out[vname] = (off, size, flags)
            return sz, vc, out
    return None


used = collections.Counter(); seen = collections.Counter(); offs = {}; layouts = set(); blobs = 0
files_used = collections.defaultdict(set)
for dp, _dn, fn in os.walk(ROOT):
    for f in fn:
        if not f.endswith(".phyre"):
            continue
        b = open(os.path.join(dp, f), "rb").read()
        if b"SceneWideParameterConstantBuffer" not in b:
            continue
        i = 0
        while True:
            i = b.find(b"DXBC", i)
            if i < 0:
                break
            try:
                tot = struct.unpack_from("<I", b, i + 24)[0]
                res = scenewide(b[i:i + tot])
            except (struct.error, ValueError, IndexError):
                res = None
            if res:
                sz, vc, vs = res
                blobs += 1; layouts.add((sz, vc))
                for w in WANT:
                    if w in vs:
                        seen[w] += 1; offs[w] = vs[w][0]
                        if vs[w][2] & 2:
                            used[w] += 1; files_used[w].add(f.split("#")[0])
            i += 4

fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


check("L1", blobs == 4799 and layouts == {(0x5F0, 154)}, "UQ-22's layout: %d blobs, layouts %s" % (blobs, sorted(layouts)))
check("L2", offs.get("mShadowFlyingFadeSpeed") == 0x5D4 and offs.get("mShadowFlyingFadeRange") == 0x5DC,
      "the pair sits at +0x5D4 / +0x5DC: %s / %s" % (hex(offs.get("mShadowFlyingFadeSpeed", -1)), hex(offs.get("mShadowFlyingFadeRange", -1))))
check("K1", used["EyePosition"] > 0, "control: EyePosition is USED in %d of %d blobs" % (used["EyePosition"], seen["EyePosition"]))
check("K2", used["mShadowFadeSpeed"] > 0 or used["mShadowFadeRange"] > 0,
      "control: the non-flying pair is USED (speed %d, range %d of %d blobs)" % (used["mShadowFadeSpeed"], used["mShadowFadeRange"], seen["mShadowFadeSpeed"]))
for w in ("mShadowFlyingFadeSpeed", "mShadowFlyingFadeRange"):
    print("      %-24s declared in %d blobs, USED in %d (files: %s)" % (w, seen[w], used[w], sorted(files_used[w])))
print("      RESULT: flying pair used by %d blob(s)" % (used["mShadowFlyingFadeSpeed"] + used["mShadowFlyingFadeRange"]))
print("FAILS %d" % fails)
