"""The menu's published selection +0x2FE0 (SWE2-DATA 2026-09-30), static: every instruction in .text that addresses
[reg + 0x2FE0], grouped by owning function (the pe.py function list), write vs read, and the base register's origin
in each of the three functions the page names.
  S1 the site census: functions, sites, writes (the page says fourteen sites across three functions, nine in the menu
     dispatcher of which one is a write, and 00279E20 writes once then reads three times);
  S2 in each function, the instruction that loads the base register used at the +0x2FE0 sites;
  S3 every direct call to the widget constructor 00245000 in .text whose r8 (the handler) is 00276D30 or 002778C0,
     with the size in edx - which widget each procedure runs on;
  S4 the dispatcher's base [widget + 0xD0] is its parent: 00276D30 builds the 0x2DC0-byte dispatcher widget in place
     at its own +0x220 with an init block whose +8 is its own widget pointer (00276DBD movsxd rax, edi; 00276DC7;
     r9 = that block at 00276DCB); the constructor calls the handler once with message id 1 (0024660A) whose +8 is
     the block's +8 (0024661A, 00246726..0024672A, 00246740); the dispatcher's id-1 arm (byte map + table at
     002778FF..00277923) stores message +8 at +0xD0 (00277925..00277931), and the handler loads r15 from there.
  C1 control: the census finds the page's two quoted sites 00278135 (write) and 00276FC5 (read).
  C2 control: S3 finds the construction the widget-constructor page quotes (00279E20 builds 0x3010-byte children
     at 0027A42D).
"""
import collections, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
import pe  # noqa
from pe import dis  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


FUNCS = [0x002778C0, 0x00276D30, 0x00279E20]
sites = collections.defaultdict(list)
for f in FUNCS:
    for x in dis(f):
        m = re.search(r"\[(r\w+) \+ 0x2fe0\]", x.op_str)
        if m:
            w = x.mnemonic.startswith("mov") and x.op_str.index("[") < x.op_str.index(",")
            sites[f].append((x.address, "W" if w else "R", m.group(1), x.mnemonic + " " + x.op_str))
tot = sum(len(v) for v in sites.values())
for f in FUNCS:
    v = sites[f]
    print("   %08X: %d sites, %d writes: %s" % (f, len(v), sum(1 for s in v if s[1] == "W"),
          " ".join("%08X%s" % (a, k) for a, k, _, _ in v)))
check("C1 control: the page's two quoted sites are found",
      any(a == 0x00278135 and k == "W" for a, k, _, _ in sites[0x002778C0])
      and any(a == 0x00276FC5 and k == "R" for a, k, _, _ in sites[0x00276D30]))
check("S1 fourteen sites over the three functions; the dispatcher has nine with one write; 00279E20 one write and "
      "three reads", tot == 14 and len(sites[0x002778C0]) == 9
      and sum(1 for s in sites[0x002778C0] if s[1] == "W") == 1
      and [s[1] for s in sites[0x00279E20]].count("W") == 1 and [s[1] for s in sites[0x00279E20]].count("R") == 3,
      "total %d" % tot)
# S2: base-register origin - the last write to that register before the first site
for f in FUNCS:
    v = sites[f]
    if not v:
        continue
    reg = v[0][2]
    body = dis(f)
    first = v[0][0]
    src = [x for x in body if x.address < first and re.match(r"(mov|lea) %s," % reg, x.mnemonic + " " + x.op_str)]
    print("   %08X base %s <- %s" % (f, reg, ("%08X %s %s" % (src[-1].address, src[-1].mnemonic, src[-1].op_str))
          if src else "argument (not written before the first site)"))
# S3: callers of 00245000 and the handler they install
import struct
from pe import d, off, secs  # noqa
hits = []
for sc in secs:
    name = sc[0] if isinstance(sc[0], str) else sc[0].decode(errors="ignore")
    if not name.startswith(".text"):
        continue
    va = sc[1] + (pe.BASE if sc[1] < pe.BASE else 0)
    o, size = sc[3], min(sc[2], sc[4])
    blob = d[o:o + size]
    i = blob.find(b"\xe8")
    while i != -1:
        if i + 5 <= len(blob):
            tgt = va + i + 5 + struct.unpack_from("<i", blob, i + 1)[0]
            if tgt == 0x00245000:
                hits.append(va + i)
        i = blob.find(b"\xe8", i + 1)
inst = []
for site in hits:
    f = pe.owner(site)
    if f is None:
        continue
    body = [x for x in dis(f) if site - 0x60 <= x.address <= site]
    if not body or body[-1].address != site:
        continue
    h = sz = None
    for x in body:
        if x.mnemonic == "lea" and x.op_str.startswith("r8, [rip"):
            m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
            h = x.address + x.size + (int(m.group(2), 16) * (1 if m.group(1) == "+" else -1))
        if x.mnemonic == "mov" and x.op_str.startswith("edx, 0x"):
            sz = int(x.op_str.split(", ")[1], 16)
    if h in (0x00276D30, 0x002778C0):
        inst.append((site, f, h, sz))
for site, f, h, sz in inst:
    print("   00245000 call %08X in %08X installs handler %08X, size %s" % (site, f, h, hex(sz) if sz else "?"))
print("   (%d direct calls to 00245000 scanned)" % len(hits))
check("C2 control: 00279E20 builds 0x3010-byte children with handler 00276D30 at 0027A42D",
      any(s_ == 0x0027A42D and h == 0x00276D30 and sz == 0x3010 for s_, f, h, sz in inst))
import struct as _st
a = {x.address: x for x in dis(0x00276D30)}
c = {x.address: x for x in dis(0x002465F0)}
m = {x.address: x for x in dis(0x002778C0)}
base = 0x0027790F - 0x15790F
t1 = base + _st.unpack_from("<I", d, off(base + 0x159D60 + 4 * d[off(base + 0x159D98)]))[0]
check("S4 the dispatcher's +0xD0 is the 0x3010 parent widget (init message +8)",
      a[0x00276DBD].op_str == "rax, edi" and a[0x00276DC7].op_str == "qword ptr [rbp - 0x29], rax"
      and a[0x00276DCB].op_str == "r9, [rbp - 0x31]" and a[0x00276DC0].op_str == "rcx, [rdi + 0x220]"
      and c[0x0024660A].op_str == "dword ptr [rsp + 0x20], 1" and c[0x0024661A].op_str == "rsi, r9"
      and c[0x00246726].op_str == "rax, qword ptr [rsi + 8]" and c[0x0024672A].op_str == "qword ptr [rsp + 0x28], rax"
      and c[0x00246740].op_str == "rdx, [rsp + 0x20]" and t1 == 0x00277925
      and m[0x00277925].op_str == "rax, qword ptr [r12 + 8]" and m[0x00277931].op_str == "qword ptr [rsi + 0xd0], rax"
      and m[0x002778EC].op_str == "r12, rdx" and m[0x002778EF].op_str == "r15, qword ptr [rcx + 0xd0]",
      "id-1 arm %08X" % t1)
print("RESULT one object type: the 0x3010-byte command-menu widget whose handler is 00276D30 - read by it directly, "
      "written by 00279E20 on each child it builds, and reached by the 0x2DC0-byte dispatcher 002778C0 through its "
      "parent pointer +0xD0")
print("FAILS %d" % FAILS)
