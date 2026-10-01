"""SWE2-AUDIT-SEM: independent slot->evaluator map of the rig frame 003E00C0..003E0720: for each direct call that is not
the resolver 0020E600, the controller index = (displacement of the last `mov ecx, dword ptr [rdi + X]`)/4 since the
previous stage call; '-' when none. Then the calls after the display-deny test at 003E0680."""
import re
rows = []
last = None
seen_deny = False
after = []
for l in open("rig_frame.dis.txt"):
    a, rest = l[:8], l[9:].strip()
    m = re.match(r"mov ecx, dword ptr \[rdi(?: \+ (0x[0-9a-f]+|\d+))?\]", rest)
    if m:
        last = int(m.group(1) or "0", 0) // 4
    if a == "003E0680":
        seen_deny = True
    m = re.match(r"call 0x([0-9a-f]+)", rest)
    if m and m.group(1) != "20e600":
        rows.append((a, m.group(1).upper().zfill(8), "-" if last is None else last))
        if seen_deny:
            after.append(("-" if last is None else last))
        last = None
for r in rows:
    print("%s\t%s\t%s" % r)
print("calls:", len(rows), " with a slot:", sum(1 for r in rows if r[2] != "-"))
print("after 003E0680:", after)
