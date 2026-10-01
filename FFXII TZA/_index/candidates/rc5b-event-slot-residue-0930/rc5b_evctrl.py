"""rc5b_evctrl.py - RC-5 residue item 1, the controller evctrl.ebp (ORACLE, 2026-09-30). Static; authored data.

It extracts image/ff12/in/bin/evctrl.ebp from the VBF, writes its section 000 to the system temp directory, and
decompiles it with ff12-script (-dc) into that same temp directory. It then prints the lines that pass a variable
to summoneventread / eventread_e8, the array initialisers they index, and the option count of each aask menu those
lines read. The option count is the first operand byte (minus 0x80) of the choice header 0E in the message text
section at container header +0x18.
Array reads are clamped into [0, dim - 1] by the variable resolver (script-variables page, section 2.2), so an indexed
read yields an initialiser element.
"""
import os, re, struct, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-as7-pages-0930"))
import arc  # noqa: E402
TOOL = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "Collaboration", "tools", "ffxii", "ff12-script-master",
                                    "x64", "Release", "ff12-script.exe"))
tmp = tempfile.mkdtemp(prefix="rc5b_")
b = arc.get("ps2data/image/ff12/in/bin/evctrl.ebp")
L = struct.unpack_from("<I", b, 0x84)[0]
s000 = os.path.join(tmp, "evctrl.s000")
open(s000, "wb").write(b[0x80:0x80 + L])
subprocess.run([TOOL, "-dc", s000, os.path.join(tmp, "evctrl.txt")], capture_output=True)
t = open(os.path.join(tmp, "evctrl.txt"), encoding="utf-8", errors="replace").read().splitlines()
print("decompiled lines:", len(t))
for n, line in enumerate(t, 1):
    if re.search(r"summoneventread\(|eventread_e8\(0, file_var|local_var_s1f1_6 = |file_var_s1_9 = aask|file_var_s1_4 = aask\(6, 0x0100000[78]", line):
        print("%5d  %s" % (n, line.strip()))
# the array initialisers
text = "\n".join(t)
for m in re.finditer(r"int\s+(file_var_s\d+_\d+)\[(\d+)\] = \{([^}]*)\}", text):
    vals = [int(v.strip(), 0) for v in m.group(3).split(",") if v.strip()]
    print("array %s[%s] = %s" % (m.group(1), m.group(2), vals))
# menu option counts from the text section
toff = struct.unpack_from("<I", b, 0x18)[0]
tend = struct.unpack_from("<I", b, 0x28)[0] if struct.unpack_from("<I", b, 0x28)[0] > toff else len(b)
sec = b[toff:tend]
first = struct.unpack_from("<I", sec, 0)[0] & 0xFFFF
count = first // 4
offs = [struct.unpack_from("<I", sec, 4 * i)[0] & 0xFFFF for i in range(count)]
for k in (7, 8, 0x12):
    if k < len(offs):
        o = offs[k]
        e = sec.find(b"\x00", o)
        msg = sec[o:e]
        i = msg.find(b"\x0e")
        print("message %#x: choice header %s -> %s options" % (k, msg[i:i + 6].hex(" ") if i >= 0 else "none",
                                                            (msg[i + 1] - 0x80) if i >= 0 else "n/a"))
    else:
        print("message %#x: not in this file's text section (%d messages)" % (k, len(offs)))
