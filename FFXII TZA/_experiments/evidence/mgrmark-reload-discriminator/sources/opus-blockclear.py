"""Enumerate every static block-clear whose destination is a rip-relative global, and
report which ones span a probe address.

Two shapes are decoded, not guessed at by displacement:
  A. `lea rdi,[rip+d]` ... `mov ecx,imm` ... `rep stos{b,d,q}`   -> [dst, dst + imm*width)
  B. `lea rcx,[rip+d]` ... `mov r8d,imm` ... `call f`            -> [dst, dst + imm) if f is
     a 3-arg fill (reported with the callee so a non-memset can be dismissed by name)

Positive control: the run must find 0032EB10's own `rep stosb` of 0x100 at 022C59F0, or the
decoder is not seeing block clears at all and every zero below is a property of the filter.
"""
import io, sys, capstone
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP
from pe import DATA, va2off

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); md.detail = True
FN = []
with io.open('functions.tsv', encoding='utf-8') as f:
    f.readline()
    for line in f:
        p = line.rstrip('\n').split('\t'); FN.append((int(p[0],16), p[1], int(p[2])))

RDI, RCX, R8, ECX, R8D = 'rdi','rcx','r8','ecx','r8d'
W = {'stosb':1,'stosd':4,'stosw':2,'stosq':8}
spans = []   # (lo, hi, kind, fnva, site, detail)
for fva, name, size in FN:
    off = va2off(fva)
    if off is None or size <= 0: continue
    regva = {}   # reg name -> rip target
    regimm = {}  # reg name -> immediate
    for ins in md.disasm(DATA[off:off+size], fva):
        m = ins.mnemonic
        if m == 'lea' and len(ins.operands) == 2 and ins.operands[1].type == X86_OP_MEM \
           and ins.operands[1].mem.base == X86_REG_RIP:
            regva[ins.reg_name(ins.operands[0].reg)] = ins.address + ins.size + ins.operands[1].mem.disp
            continue
        if m == 'mov' and len(ins.operands) == 2 and ins.operands[0].type == X86_OP_REG \
           and ins.operands[1].type == X86_OP_IMM:
            r = ins.reg_name(ins.operands[0].reg)
            regimm[r] = ins.operands[1].imm
            regva.pop(r, None)
            if r == 'ecx': regimm['rcx'] = ins.operands[1].imm; regva.pop('rcx', None)
            if r == 'r8d': regimm['r8'] = ins.operands[1].imm; regva.pop('r8', None)
            continue
        if 'stos' in m:
            mm = [t for t in m.split() if t.startswith('stos')][0]
            w = W.get(mm, 1); d = regva.get('rdi'); n = regimm.get('rcx')
            if d is not None and n and 0 < n <= 0x400000:
                spans.append((d, d + n*w, mm, fva, ins.address, '0x%X bytes'%(n*w)))
            regva.pop('rdi', None); regimm.pop('rcx', None); continue
        if m == 'call':
            d = regva.get('rcx'); n = regimm.get('r8')
            if d is not None and n and 8 <= n <= 0x400000:
                spans.append((d, d + n, 'call', fva, ins.address, 'callee %s len 0x%X'%(ins.op_str, n)))
            regva.clear(); regimm.clear(); continue
        # anything that writes a tracked register conservatively kills it
        try:
            _, wr = ins.regs_access()
        except capstone.CsError:
            wr = ()
        for rid in wr:
            r = ins.reg_name(rid)
            regva.pop(r, None); regimm.pop(r, None)
            if r == 'ecx': regva.pop('rcx', None); regimm.pop('rcx', None)
            if r == 'r8d': regva.pop('r8', None); regimm.pop('r8', None)

print('block-clear spans decoded: %d' % len(spans))
ctrl = [s for s in spans if s[3] == 0x0032EB10]
print('POSITIVE CONTROL 0032EB10: %s' % (ctrl if ctrl else 'NOT FOUND -- decoder blind, stop'))
for probe in [int(x,16) for x in sys.argv[1:]] or [0x022C6D20]:
    hit = [s for s in spans if s[0] <= probe < s[1]]
    print('probe %08X covered by %d span(s)' % (probe, len(hit)))
    for s in hit: print('   %08X..%08X  %s in %08X at %08X  (%s)' % s)
    near = sorted([s for s in spans if s[0] <= probe and probe - s[1] < 0x4000 and probe >= s[1]], key=lambda s: probe - s[1])[:5]
    print('   nearest spans ending below the probe:')
    for s in near: print('     %08X..%08X  (%d B short)  %s in %08X at %08X (%s)' % (s[0],s[1],probe-s[1],s[2],s[3],s[4],s[5]))
