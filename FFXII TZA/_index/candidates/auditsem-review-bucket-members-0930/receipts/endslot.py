"""SWE2-AUDIT-SEM: the count-and-offsets frames carry count+1 offsets; the last equals the file size."""
import glob, struct, os
for f in sorted(glob.glob("ent/*_name.bin") + glob.glob("ent/*logicpack*")):
    d = open(f, "rb").read(); n = struct.unpack_from("<I", d, 0)[0]
    first = struct.unpack_from("<I", d, 4)[0]; end = struct.unpack_from("<I", d, 4 + 4 * n)[0]
    print("%-60s size %8d count %5d offsets[0] %6d (4+4n=%d, 8+4n=%d) offsets[count] %8d == size: %s"
          % (os.path.basename(f)[-60:], len(d), n, first, 4 + 4 * n, 8 + 4 * n, end, end == len(d)))
