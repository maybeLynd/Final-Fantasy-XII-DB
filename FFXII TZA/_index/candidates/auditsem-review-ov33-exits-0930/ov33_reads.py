"""SWE2-AUDIT-SEM OV-33 reads (own code): bodies read whole for the four review questions.
Q1 0024AC10 / 0024AC30 (kind 0x23 request, size test), 0037B330 (mode), 002DF780 head to 002DF7C0 (the -1 exit),
   the router open-table arms 0027FFC0..0027FFE0 and the tick 0027FC00..0027FC40.
Q2 001A1220, 001A11B0, 001A11F0.
Q3 001D6FB0 (loose job), 001A0BB0 (inline run), 001A0E50..001A0EE0 (loose worker to the -2 store).
Q4 0032FE40..00330000 (event loader gates), 00330340..00330450 (primary payload gate)."""
import img

def d(lo, hi, title):
    print("==", title)
    for back in range(0, 16):
        xs = list(img.md.disasm(img.rd(lo - back, hi - lo + back + 16), lo - back))
        if any(x.address == lo for x in xs):
            break
    for x in xs:
        if lo <= x.address < hi:
            print("%08X %s %s" % (x.address, x.mnemonic, x.op_str))

d(0x0024AC10, 0x0024ACF0, "0024AC10 / 0024AC30")
d(0x0037B330, 0x0037B350, "0037B330")
d(0x002DF780, 0x002DF7D0, "002DF780 head")
d(0x0027FFC0, 0x0027FFE0, "router open arms")
d(0x0027FC00, 0x0027FC40, "router tick state 2")
d(0x001A1220, 0x001A1230, "001A1220")
d(0x001A11B0, 0x001A1220, "001A11B0 create / 001A11F0 destroy")
d(0x001D6FB0, 0x001D7010, "001D6FB0 loose job")
d(0x001A0BB0, 0x001A0BF0, "001A0BB0")
d(0x001A0E50, 0x001A0EE0, "001A0E50 loose worker")
d(0x0032FE40, 0x00330000, "0032FCA0 gates")
d(0x00330340, 0x00330450, "00330310 primary payload")
d(0x0032FCA0, 0x0032FE40, "0032FCA0 head: the size results the gates test")
d(0x0027FC0F, 0x0027FC40, "router tick: state 2 -> 0024AC10([+0xCC])")
d(0x0027FD30, 0x0027FD60, "router tick: state 0 -> 1")
d(0x00280090, 0x00280110, "router open table 00280090")
d(0x0027FE10, 0x0027FE50, "router open dispatch through the 00280090 table")
d(0x0027FF88, 0x00280012, "router open arms 8/9/13/14/4 (table index)")
d(0x0027FE88, 0x0027FEA2, "router open arm: parameter 0x40/0x41")
d(0x0037B390, 0x0037B3C0, "0037B390 boot reset of the mode bytes")
d(0x0024ACF0, 0x0024AD20, "0024ACF0 done callback (address-taken at 0024AC6D)")
d(0x001D7010, 0x001D7090, "001D6FB0 continued: job fields and the inline run")
d(0x0059FBA0, 0x0059FC40, "0059FBA0 seek")
d(0x0059D900, 0x0059D930, "0059D900 record-set test")
d(0x0017D540, 0x0017D5D4, "0017D4C0 platform init: create at 0017D56C before the boot call at 0017D5CC")
d(0x0017D670, 0x0017D690, "0017D670 teardown: destroy at 0017D679")
d(0x001FDF70, 0x001FE000, "001FDF70 (called on the record when the stored size is -1)")
