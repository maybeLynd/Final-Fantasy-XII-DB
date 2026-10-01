import sys,re,collections
sys.path.insert(0,'.')
import xdis
from capstone import *
from capstone.x86 import *
import kit_paths as KP  # noqa: E402
import os
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
FN=os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
LO,HI=0x022D8F00,0x022D9500
fns=[];own={}
for ln in open(FN,encoding='utf-8',errors='replace'):
    p=ln.rstrip('\n').split('\t')
    if len(p)<9 or not re.match(r'^[0-9A-F]{8}$',p[0]): continue
    if 'CompilerGeneratedEH' in p[8]: continue
    fns.append((int(p[0],16),int(p[2]))); own[int(p[0],16)]=p[3]
blk=collections.defaultdict(lambda: {'w':set(),'r':set(),'wid':collections.Counter(),'sub':set()})
for va,sz in fns:
    b=xdis.rd(va,sz)
    if not b: continue
    for i in md.disasm(b,va):
        for k,op in enumerate(i.operands):
            if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP and op.mem.index==0:
                t=i.address+i.size+op.mem.disp
                if not (LO<=t<HI): continue
                B=t & ~0xF
                d=blk[B]
                d['wid'][op.size]+=1; d['sub'].add(t-B)
                (d['w'] if (k==0 and i.mnemonic not in ('cmp','test','lea')) else d['r']).add(va)
print('block      W    R   widths                sub-offsets touched          owners')
prev=None
for B in sorted(blk):
    d=blk[B]
    if prev is not None and B-prev>16: print('  ======== %d-byte hole ========'%(B-prev-16))
    o=collections.Counter((own.get(f,'') or '-').split('.')[-1] for f in d['w'])
    subs=','.join('%X'%x for x in sorted(d['sub']))
    print('%08X %4d %4d   %-20s %-28s %s'%(B,len(d['w']),len(d['r']),
        ','.join('%d:%d'%(k,v) for k,v in sorted(d['wid'].items())),subs[:28],
        ', '.join('%s×%d'%(k,v) for k,v in o.most_common(2))))
    prev=B
