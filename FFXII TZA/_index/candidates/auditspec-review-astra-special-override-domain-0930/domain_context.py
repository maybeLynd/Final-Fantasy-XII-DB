"""SWE2-AUDIT-SPEC: context for two follow-ups of domain_indep.out.
 C1 the index/word consumer 002F8D60 around its reads of 01EEBAF0 / 022BE930 (how index -1 is handled)
 C2 the other image-wide +0xAE0 writers 00184FBA / 001881BF / 006DD2D0 / 007049B8: surrounding instructions,
    and whether their functions also touch +0xADC/+0xAE4 (the override object's neighbouring fields)
"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
def show(x): return "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
print("C1 consumer 002F8D60")
for x in tk.fdis(0x002F8D60):
    if x.address < 0x002F8DC0: print("  ", show(x))
print("C2 other +0xAE0 writers")
for site in (0x00184FBA, 0x001881BF, 0x006DD2D0, 0x007049B8):
    o, how = tk.owner(site)
    if o is None:
        o, how = site - 0x40, "unowned (no listed function or .pdata range); linear decode from site-0x40"
        body = [x for x in tk.dis(o, site + 16)]
    else:
        body = list(tk.fdis(o)) if how == "listed" else list(tk.dis(o, site + 16))
    i = next((j for j, x in enumerate(body) if x.address == site), None)
    print("  site %08X owner %08X (%s) %s" % (site, o, how, tk.fname(site)))
    if i is not None:
        for x in body[max(0, i - 5):i + 2]: print("     ", show(x))
    near = sorted(set("+0x%X" % op.mem.disp for x in body for op in x.operands if op.type == 3 and 0xAD0 <= op.mem.disp <= 0xC10 and x.reg_name(op.mem.base) != "rsp"))
    print("     displacements 0xAD0..0xC10 used in owner:", near)
