"""counter_raw.py - SWE2-AUDIT-SPEC independent census of the event-slot counters [01F832B0, 01F832C4) over ALL
.text bytes (tk.py raw disp32 sweeps, not the functions.tsv extents counter_access.py walks): rip-relative and
image-base-relative (disp = rva) forms, plus DIR64 stored pointers. Prints each access with its owner (listed /
pdata / none) so an access outside listed bodies would show. Then compares with counter_access.out's 21 sites."""
import sys, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
LO, HI = 0x01F832B0, 0x01F832C4
rh, rraw = tk.rip_refs(LO, HI)
dh, draw = tk.disp_refs(LO - tk.BASE, HI - tk.BASE)
rp = tk.reloc_ptrs(LO, HI)
sites = {}
for x, k, t in rh: sites[x.address] = ("rip", x, t)
for x, k, v in dh: sites[x.address] = ("ibr", x, v + tk.BASE)
print("rip=%d (raw-only %d) image-base=%d (raw-only %d) dir64=%d" % (len(rh), len(rraw), len(dh), len(draw), len(rp)))
for a in sorted(sites):
    f, x, t = sites[a]
    o, how = tk.owner(a)
    print("%08X %-3s %-5s %-44s -> %08X owner %s (%s)" % (a, f, x.mnemonic, x.op_str, t, "%08X" % o if o else "-", how))
ref = open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\swe2contract-ddres-b4-0930\counter_access.out").read()
theirs = {int(m.group(1), 16) for m in re.finditer(r"^[0-9A-F]{8}  ([0-9A-F]{8})  ", ref, re.M)}
print("counter_access sites=%d, raw census sites=%d, only-raw=%s, only-theirs=%s" % (
    len(theirs), len(sites), ["%08X" % a for a in sorted(set(sites) - theirs)], ["%08X" % a for a in sorted(theirs - set(sites))]))
