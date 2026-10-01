"""Raw-first imul-by-0x290 census: every dword 0x290 in .text decoded as an imul immediate from any start,
then kept only if the site is an instruction boundary of its listed function's linear decode (drops misaligned decodes)."""
import pefile,struct,bisect,re
from capstone import *
E="Database/Tools/work/exe/FFXII_TZA.exe"
pe=pefile.PE(E,fast_load=True);IB=pe.OPTIONAL_HEADER.ImageBase
tx=next(s for s in pe.sections if s.Name.startswith(b".text")); t=tx.get_data(); tva=IB+tx.VirtualAddress
L=[l.split("\t") for l in open("Database/Tools/work/graph/functions.tsv",encoding="utf-8").read().splitlines()[1:]]
e=sorted((int(x[0],16),int(x[2])) for x in L if x[0]); ks=[x[0] for x in e]
md=Cs(CS_ARCH_X86,CS_MODE_64)
pat=struct.pack("<I",0x290); i=t.find(pat); raw=set()
while i!=-1:
    for back in range(2,9):
        s=i-back; ins=next(md.disasm(t[s:s+15],tva+s),None)
        if ins and ins.mnemonic=="imul" and s+ins.size==i+4: raw.add(ins.address)
    i=t.find(pat,i+1)
bounds={}; fns=set(); mis=[]; unl=[]
for a in sorted(raw):
    j=bisect.bisect_right(ks,a)-1
    if j<0 or a>=e[j][0]+e[j][1]: unl.append(a); continue
    f,sz=e[j]
    if f not in bounds:
        bounds[f]={x.address for x in md.disasm(t[f-tva:f-tva+sz],f)}
    (fns.add(f) if a in bounds[f] else mis.append(a))
listed71=set(int(x,16) for x in re.findall(r"\b(00[0-9A-Fa-f]{6})\b",open("Database/FFXII TZA/_index/candidates/uq218-cm-entry-residues/imul290.txt",encoding="utf-8").read()))
print("raw imul-0x290 decodes",len(raw),"| aligned in listed bodies: functions",len(fns),"| misaligned",["%08X"%x for x in mis],"| outside listed bodies",["%08X"%x for x in unl])
print("functions inside imul290.txt:",len(fns&listed71),"of",len(listed71),"| outside it:",["%08X"%x for x in sorted(fns-listed71)])
