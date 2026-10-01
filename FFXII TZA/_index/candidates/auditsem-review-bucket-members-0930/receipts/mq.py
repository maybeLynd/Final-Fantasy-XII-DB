import glob,struct,os
for f in sorted(glob.glob("ent/*menuquest0*")):
    d=open(f,"rb").read()
    off=struct.unpack_from("<6H",d,0); ff,N=struct.unpack_from("<2H",d,12)
    print(os.path.basename(f)[-34:],len(d),[hex(x) for x in off],hex(ff),N,"recs_end",hex(16+20*N),"QHD0@",hex(d.find(b"QHD0")),"QHT0@",hex(d.find(b"QHT0")),"tail rows end",hex(off[5]+28*N) if off[5]!=0xffff else None)
