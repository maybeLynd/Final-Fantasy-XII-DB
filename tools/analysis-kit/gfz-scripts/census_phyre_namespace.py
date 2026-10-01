"""Census the packed namespace of every extracted .phyre file.

The namespace is bytes [m_size, m_size + m_packedNamespaceSize) -- 0059A6F0 reads exactly that many
bytes straight after the header, byte-swapping via 0059C180 only when the marker said big-endian.
It opens with the byte-order mark 04 03 02 01 and its own size, and ends in a NUL-separated string
pool holding type names, class names and field names in plain ASCII.
"""
import os, re, struct, collections, json

ROOT = r'D:/FFXII MP Mod/extracted'
files = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if f.lower().endswith('.phyre'):
            files.append(os.path.join(dp, f))
files.sort()

TOK = re.compile(rb'[A-Za-z_][A-Za-z0-9_]{2,80}')
classes = collections.Counter()
fields = collections.Counter()
other = collections.Counter()
bom_ok = 0
size_ok = 0
per_file = []
for p in files:
    with open(p, 'rb') as fh:
        d = fh.read()
    hs = struct.unpack_from('<I', d, 4)[0]
    ns = struct.unpack_from('<I', d, 8)[0]
    blob = d[hs:hs + ns]
    if blob[:4] == b'\x04\x03\x02\x01':
        bom_ok += 1
    if len(blob) >= 8 and struct.unpack_from('<I', blob, 4)[0] == ns:
        size_ok += 1
    names = {m.group().decode() for m in TOK.finditer(blob)}
    for s in names:                      # once per FILE, not per occurrence
        if s.startswith('m_'):
            fields[s] += 1
        elif s.startswith('P') and len(s) > 2 and s[1].isupper():
            classes[s] += 1
        else:
            other[s] += 1
    per_file.append((os.path.relpath(p, ROOT), ns, len(names)))

print("files                                : %d" % len(files))
print("namespace begins 04 03 02 01         : %d" % bom_ok)
print("namespace word[1] == m_packedNamespaceSize : %d" % size_ok)
print("distinct P* class/type names         : %d" % len(classes))
print("distinct m_* field names             : %d" % len(fields))
print("distinct other tokens                : %d" % len(other))
print()
print("=== the 25 most widespread class/type names ===")
for k, v in classes.most_common(25):
    print("%4d files  %s" % (v, k))
print()
print("=== 20 sample 'other' tokens ===")
for k, v in other.most_common(20):
    print("%4d  %s" % (v, k))

with open(r'C:\Users\Kristian\AppData\Local\Temp\claude\C--Users-Kristian-source-repos-XIIOnline\862388d6-126d-4d2f-ae78-c9bed3a0394d\scratchpad\ns_classes.txt', 'w') as fh:
    for k in sorted(classes):
        fh.write("%s\t%d\n" % (k, classes[k]))
with open(r'C:\Users\Kristian\AppData\Local\Temp\claude\C--Users-Kristian-source-repos-XIIOnline\862388d6-126d-4d2f-ae78-c9bed3a0394d\scratchpad\ns_fields.txt', 'w') as fh:
    for k in sorted(fields):
        fh.write("%s\t%d\n" % (k, fields[k]))
print("\nwrote ns_classes.txt / ns_fields.txt")
