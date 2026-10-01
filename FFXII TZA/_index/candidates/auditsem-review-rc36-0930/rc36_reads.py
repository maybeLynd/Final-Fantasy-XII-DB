"""SWE2-AUDIT-SEM RC-36 reads (own code): the bodies this review read, printed whole.
003C2320 (emitter), 003BF430 (point + kind out-slot), 003BE3A0..003BE560 (the emitter's one caller and the triple
array), 003C1AE0..003C1BD1 (triple fill: kind from 003BF430, null point skipped), 003BDDE0 head (out-slot writes),
003BE810 (the uncertain 003BE8DA path), 003BEA70..003BEB10 (003BE950's two arms), 004045C0..004046B5 (label pass),
002D8670 (the draw call's text operand [r9+0x28])."""
import img

def d(lo, hi, title):
    print("==", title)
    for back in range(0, 16):
        xs = list(img.md.disasm(img.rd(lo - back, hi - lo + back), lo - back))
        if any(x.address == lo for x in xs):
            break
    for x in xs:
        if x.address >= lo:
            print("%08X %s %s" % (x.address, x.mnemonic, x.op_str))

d(0x003C2320, 0x003C26C0, "003C2320 draw-row emitter")
d(0x003BF430, 0x003BF520, "003BF430 point + kind (0 = A, 1 = B, 3 = none with null)")
d(0x003BE3A0, 0x003BE560, "003BE3A0 caller of the emitter (003BE554)")
d(0x003C1AE0, 0x003C1BD8, "003C1A20 triple fill")
d(0x003BDDE0, 0x003BDF60, "003BDDE0 head: r8 out-slot written only at 003BDE7F")
d(0x003BE810, 0x003BE950, "003BE810 (003BE8DA)")
d(0x003BEA70, 0x003BEB10, "003BE950 arms: kind 0 -> 003BEAAC, kind != 0 -> 003BEB06")
d(0x004045C0, 0x004046B5, "004044D0 label pass: text [rdi+0x10] -> [rsp+0x58] -> 002D8670 r9 block +0x28")
d(0x002D8670, 0x002D8724, "002D8670 reads [r9+0x28] at 002D8718")
