"""SWE2-AUDIT-SEM: run the SEAD/audio selector WITHOUT --write (runpy; nothing in the tree is written) and diff each of
its six lists against the tracked members files."""
import runpy, sys, os
M = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\18-Audio\members"
INV = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\23-Third-Party-Libraries\members"
sys.path.insert(0, M)
sys.argv = [os.path.join(M, "select_audio_libraries.py")]
g = runpy.run_path(sys.argv[0], run_name="__main__")
def tracked(p):
    return [int(l.split()[0], 16) for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")]
for name, var, path in (("SEAD", "members", os.path.join(M, "sead-library-span.tsv")),
                        ("libogg framing", "ogg", os.path.join(INV, "libogg-framing.tsv")),
                        ("tremor", "tremor", os.path.join(INV, "tremor-vorbisfile.tsv")),
                        ("cri", "cri", os.path.join(INV, "cri-hca-decoder.tsv")),
                        ("libvorbis", "vorbis", os.path.join(INV, "libvorbis.tsv")),
                        ("bitwise", "bitw", os.path.join(INV, "libogg-bitwise.tsv"))):
    sel, tr = list(g[var]), tracked(path)
    add = sorted(set(sel) - set(tr)); drop = sorted(set(tr) - set(sel))
    print("%-15s selector %5d tracked %5d  equal=%s  +%s  -%s" % (name, len(sel), len(tr), sel == tr,
          " ".join("%08X" % x for x in add[:10]), " ".join("%08X" % x for x in drop[:10])))
S = g["SPAN"]; sead = tracked(os.path.join(M, "sead-library-span.tsv"))
out = [x for x in sead if not S[0] <= x < S[1]]
print("SEAD span %08X-%08X; tracked members outside it: %d %s" % (S[0], S[1], len(out), " ".join("%08X" % x for x in out)))
