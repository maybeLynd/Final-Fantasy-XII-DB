import glob,struct,os
for f in sorted(glob.glob("ent/*_name.bin"))[:2]:
    d=open(f,"rb").read(); n=struct.unpack_from("<I",d,0)[0]
    w=struct.unpack_from("<%dI"%(n+2),d,0)
    print(os.path.basename(f)[-40:],len(d),"count",n,"w[1]",hex(w[1]),"w[n]",hex(w[n]),"w[n+1]",hex(w[n+1]),"8+4n",hex(8+4*n))
    o=w[1]; print("  at w[1]:",d[o:o+24].hex(" "), d[o:o+24].decode("utf-16-le","replace"))
    offs=w[1:n+1]; print("  ascending",all(offs[i]<=offs[i+1] for i in range(n-1)),"last",hex(offs[-1]),"size",hex(len(d)))
    # any offset outside file
    print("  max offset < size", max(offs)<len(d))
