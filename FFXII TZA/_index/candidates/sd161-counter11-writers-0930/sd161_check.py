"""sd161_check.py - SD-161: who else writes achievement counter 11's field (OPUS, 2026-09-30). Static, the certified
image, via Database/Tools/analysis-kit/gfz-scripts/retool.py, plus the value-flow census sd161_objflow.out / .tsv
written by Database/Tools/analysis-kit/gfz-scripts/objflow.py:

  python -B objflow.py --ptr 020927C0 --static 02164280 021BA910 --base 0216C480 --region 0x385C 0x3860
         --getter 002EF640:-0x8200 --getter 002536A0:0 --out sd161_objflow.tsv > sd161_objflow.out

The field is record + 0x385C (block +0x384C + 0x10, counter 11), the record being [020927C0] = image + 0x8200
(0216C480), so the field is 0216FCDC inside the static save image 02164280 .. 021BA910 (0x56690 bytes).
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return i.address + i.size + int(re.search(r"rip \+ 0x([0-9a-f]+)", i.op_str).group(1), 16)


FIELD = 0x0216FCDC
out = open(os.path.join(HERE, "sd161_objflow.out"), encoding="utf-8").read()
region = [l for l in out.splitlines() if l.startswith("  REGION")]
# Z1 - the census: exactly four stores land on the field at a known offset, and all four are calls of 00861EC0
check("Z1", len(region) == 4 and all("call 0x861ec0" in l for l in region)
      and sorted(l.split()[1] for l in region) == ["00253A80", "00253A80", "002EF5F0", "002EF650"],
      "the census's four known-offset stores on +0x385C are 00861EC0 calls in 00253A80 (x2), 002EF5F0, 002EF650")
# Z2 - three of them are zero-fills that cover the field (the fourth, 00253A93, clears 0x58 bytes at [02092758]; the
#      census sizes it through an escape global, and it does not reach the field): 00861EC0 with edx = 0 over the whole image (002EF5F0, 002EF650:
#      02164280, 0x56690 bytes) and over the record (00253A80: [020927C0], 0x4818 bytes > 0x385C + 4)
check("Z2", txt(0x002EF5F4) == "xor edx, edx" and rip(0x002EF5F6) == 0x02164280 and txt(0x002EF5FD) == "mov r8d, 0x56690"
      and txt(0x002EF654) == "xor edx, edx" and rip(0x002EF656) == 0x02164280 and txt(0x002EF65D) == "mov r8d, 0x56690"
      and rip(0x00253A98) == 0x020927C0 and txt(0x00253A9F) == "xor edx, edx" and txt(0x00253AA1) == "mov r8d, 0x4818"
      and 0x02164280 <= FIELD < 0x02164280 + 0x56690 and 0x385C + 4 <= 0x4818
      and rip(0x00253A86) == 0x02092758 and txt(0x00253A8F) == "lea r8d, [rdx + 0x58]",
      "three are memset(.., 0, ..) over ranges that contain 0216FCDC; 00253A93 clears 0x58 bytes elsewhere")
# Z3 - so a new game starts the counter at 0: 002EF650 clears the image and then calls 00253A80, which clears the record
check("Z3", txt(0x002EF663) == "call 0x861ec0" and txt(0x002EF66F) == "call 0x253a80",
      "002EF650: image clear, then 00253A80's record clear")
# Z4 - the updater never stores a negative: its kind-4 arm keeps the sum only when it is not negative, else 0
check("Z4", txt(0x00316B9D) == "add ebx, edi" and txt(0x00316B9F) == "jns 0x316bbd" and txt(0x00316BA1) == "xor ebx, ebx",
      "00316A50 kind-4 arm: sum >= 0, else 0")
# Z5 - the save side reads the image, it does not write it: 00229B40 copies the image into the snapshot 021BA940 (from
#      the image getter 002EF640, 0x1C4 blocks); 0057E310 and 002EF690 copy the snapshot into 02211000 (0xACD blocks)
#      for the file
check("Z5", txt(0x00229B62) == "call 0x2ef640" and txt(0x00229C46) == "mov ecx, 0x1c4"
      and txt(0x0057E337) == "call 0x2ef630" and txt(0x0057E33F) == "call 0x2ef620" and txt(0x0057E347) == "mov r8d, 0xacd"
      and rip(0x002EF69D) == 0x02211000 and rip(0x002EF6A4) == 0x021BA940 and txt(0x002EF72C) == "jmp 0x20e540",
      "image -> snapshot 021BA940 -> save buffer 02211000 -> file")
# Z6 - the census's two unbounded bulk copies do not reach the field: 002EF4A0 writes 021B290C.. (0xC0 x 0x80 bytes)
#      and 00229B40's first loop writes image + 0x2200 .. + 0x8200
check("Z6", rip(0x002EF4A0) == 0x021B290C and txt(0x002EF4A7) == "mov edx, 0xc0" and 0x021B290C > FIELD
      and txt(0x00229B88) == "add rax, 0x2200" and txt(0x00229B7B) == "mov r8d, 0xc0" and 0x02164280 + 0x2200 + 0xC0 * 0x80 <= FIELD,
      "002EF4A0 and 00229B40's first loop end away from 0216FCDC")
print("FAILS %d" % fails)
