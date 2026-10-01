import sys, img
for a in sys.argv[1:]:
    va=int(a,16); r=img.owner(va) or va
    print("== %08X root %08X frags %s" % (va, r, ["%08X-%08X"%f for f in img.fragments(r)]))
    img.pr(img.fn_ins(r))
