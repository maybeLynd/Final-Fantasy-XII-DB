"""SWE2-AUDIT-SEM independent checker for the SECTION-03 review (OPUS-REQ-AUDITSEM-SECTION03-REVIEW-1001).

Static evidence only. It re-derives ten of the 24 pinned bodies of
_experiments/evidence/continuation-section03-reward-bindings/ from the shipping EXE with its own
PE/.pdata parse and its own Capstone decode (the producer's file offsets and disassembly are not
used as inputs; the offsets are compared afterwards). Every instruction-pattern assertion has a
negative control on a mutated or foreign body so a pass cannot be a property of the filter.
It then compares the auditor's WSL rerun of run_review.py with the shipped results, and records
the one input-pin drift found (retained-reward-bindings/check.py).

Run from anywhere:  python -B sec03_sem.py > sec03_sem.out
"""
import hashlib, json, os, struct, subprocess, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
PKG = os.path.join(DB, '_experiments', 'evidence', 'continuation-section03-reward-bindings')
EXE = os.path.normpath(os.path.join(DB, '..', 'Tools', 'work', 'exe', 'FFXII_TZA.exe'))
WORK = os.path.normpath(os.path.join(DB, '..', 'Tools', 'work', 'SWE2-AUDIT-SEM', 'sec03'))
PIN = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
SAMPLE = ['002F8BB0', '002F90C0', '00264150', '002367A0', '0031B810',
          '0023A570', '0020E600', '00312280', '00254EE0', '00469E80']

FAILS = []
PASSES = 0
def check(name, ok, detail=''):
    global PASSES
    if ok:
        PASSES += 1
        print('PASS', name, detail)
    else:
        FAILS.append(name)
        print('FAIL', name, detail)

def sha(b):
    return hashlib.sha256(b).hexdigest()

raw = open(EXE, 'rb').read()
check('exe-pin', sha(raw) == PIN, sha(raw)[:16])

# --- own PE parse --------------------------------------------------------------------------
pe = struct.unpack_from('<I', raw, 0x3C)[0]
nsec = struct.unpack_from('<H', raw, pe + 6)[0]
optsz = struct.unpack_from('<H', raw, pe + 20)[0]
opt = pe + 24
base = struct.unpack_from('<Q', raw, opt + 24)[0]
secs = []
for i in range(nsec):
    o = opt + optsz + 40 * i
    vsz, va, rsz, rptr = struct.unpack_from('<IIII', raw, o + 8)
    secs.append((raw[o:o + 8].rstrip(b'\0').decode(), va, vsz, rptr, rsz))
def off(v):
    rva = v - base
    for _, va, vsz, rp, rs in secs:
        if va <= rva < va + max(vsz, rs):
            return rp + rva - va
    raise KeyError(hex(v))
exc_rva, exc_size = struct.unpack_from('<II', raw, opt + 112 + 3 * 8)
pdata = {}
po = off(base + exc_rva)
for k in range(exc_size // 12):
    b, e, _u = struct.unpack_from('<III', raw, po + 12 * k)
    pdata[base + b] = base + e
check('image-base', base == 0x120000, hex(base))

md = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(start, end, blob=None):
    data = blob if blob is not None else raw[off(start):off(end)]
    return [(i.address, i.mnemonic, i.op_str) for i in md.disasm(data, start)]
def text(ins):
    return ['%s %s' % (m, o) for _, m, o in ins]
def has(ins, s):
    return any(t == s for t in text(ins))
def at(ins, addr):
    for a, m, o in ins:
        if a == addr:
            return '%s %s' % (m, o)
    return None

man = json.load(open(os.path.join(PKG, 'original_body_manifest.json')))
check('manifest-24-bodies', len(man['bodies']) == 24, str(len(man['bodies'])))
bodies = {b['entry']: b for b in man['bodies']}
idx = [list(bodies).index(e) for e in SAMPLE]
check('sample-spread', len(SAMPLE) >= 6 and min(idx) == 0 and max(idx) == 23, 'manifest indices %s' % idx)

# --- A. byte identity, independent offsets, extents ----------------------------------------
for e in SAMPLE:
    b = bodies[e]
    s, t = int(e, 16), int(b['end_exclusive'], 16)
    fo = off(s)
    blob = raw[fo:fo + (t - s)]
    check('A-hash ' + e, fo == b['file_offset'] and len(blob) == b['bytes'] and sha(blob) == b['sha256'],
          'own offset 0x%X' % fo)
    pend = pdata.get(s)
    ins = dis(s, t)
    last = ins[-1][1] if ins else None
    decoded_to_end = bool(ins) and (ins[-1][0] + len(md.disasm(raw[off(ins[-1][0]):off(t)], ins[-1][0]).__next__().bytes) == t)
    check('A-extent ' + e, decoded_to_end and last in ('ret', 'jmp'),
          '.pdata end %s; last %s' % ('%08X' % pend if pend else 'none (not a .pdata root)', last))
# negative controls for A
s0 = int(SAMPLE[0], 16)
check('A-neg shifted range hash differs', sha(raw[off(s0) + 1:off(s0) + 1 + 430]) != bodies[SAMPLE[0]]['sha256'])
check('A-neg no .pdata root mid-body', (s0 + 4) not in pdata)

# --- B. semantic assertions (each with a negative control) ---------------------------------
exp = dis(0x2F8BB0, 0x2F8D5E)
lp = dis(0x2F90C0, 0x2F9173)
def exp_divides(ins):
    t = text(ins)
    return any(t[i] == 'cdq ' and t[i + 1] == 'idiv ebp' for i in range(len(t) - 1))
check('B1 EXP signed divide by roster count (cdq; idiv ebp)', exp_divides(exp))
check('B1-neg LP has no divide', not exp_divides(lp) and not any(m.startswith('idiv') or m == 'div' for _, m, _ in lp))
check('B1 EXP DWORD coefficient row+0x34 (both rows, both paths)',
      sum(1 for x in text(exp) if x.endswith('dword ptr [rax + 0x34]') or x.endswith('dword ptr [rcx + 0x34]')) == 4)
check('B1 EXP walks four roster slots via 0031B810',
      has(exp, 'cmp ebx, 4') and has(exp, 'call 0x31b810') and has(exp, 'inc ebp'))
check('B1 EXP id 0x1A admitted as recipient but not counted',
      has(exp, 'cmp byte ptr [rcx + 4], 0x1a') and at(exp, 0x2F8CDC) == 'je 0x2f8ce0')
check('B1 EXP zero count skips row reads (test ebp; je to modifiers)',
      at(exp, 0x2F8CEC) == 'test ebp, ebp' and at(exp, 0x2F8CEE) == 'je 0x2f8d21')
check('B1 EXP NULL recipient skips recipient checks to subject validation',
      at(exp, 0x2F8BCF) == 'test rcx, rcx' and at(exp, 0x2F8BD2) == 'je 0x2f8c11')
check('B1 EXP NULL skips designation equality and modifiers',
      at(exp, 0x2F8C45) == 'je 0x2f8c5c' and at(exp, 0x2F8D24) == 'je 0x2f8d42')
d8 = [a for a, m, o in exp if m == 'add' and o == 'esi, esi']
z20 = [a for a, m, o in exp if m == 'xor' and o == 'esi, esi' and a > 0x2F8D00]
check('B1 EXP doubling (bit 8) precedes zeroing (bit 0x20)', d8 and z20 and d8[0] < z20[0], str((d8, z20)))
# LP
check('B2 LP global gate is the first act (call 00264150; nonzero rejects)',
      at(lp, 0x2F90D0) == 'call 0x264150' and at(lp, 0x2F90D5) == 'test eax, eax' and at(lp, 0x2F90D7) == 'jne 0x2f9166')
first_deref = min(a for a, m, o in lp if '[rbx' in o or '[rdi' in o)
check('B2 LP gate precedes every recipient/subject dereference', first_deref > 0x2F90D7, '%08X' % first_deref)
gate = dis(0x264150, 0x264158)
check('B2 gate loads a signed global byte', text(gate)[0].startswith('movsx eax, byte ptr [rip'))
check('B2 LP unsigned byte coefficients row+0x2F (movzx x2)',
      sum(1 for x in text(lp) if x == 'movzx ecx, byte ptr [rax + 0x2f]') == 2)
lpb = bytearray(raw[off(0x2F90C0):off(0x2F9173)])
lpb[0x2F9132 - 0x2F90C0 + 1] = 0xBE  # 0f b6 -> 0f be (movsx)
lp_mut = dis(0x2F90C0, 0x2F9173, bytes(lpb))
check('B2-neg sign-extending mutant is caught', sum(1 for x in text(lp_mut) if x == 'movzx ecx, byte ptr [rax + 0x2f]') == 1)
check('B2 LP no owner lookup: its only call is the gate',
      [o for _, m, o in lp if m == 'call'] == ['0x264150'])
check('B2-neg EXP does call the owner/selector helpers', len([1 for _, m, _ in exp if m == 'call']) >= 5)
check('B2 LP ids 0..6, 0x1A, >=0x28',
      at(lp, 0x2F90EB) == 'cmp al, 0x1a' and at(lp, 0x2F90EF) == 'cmp al, 6' and at(lp, 0x2F90F1) == 'jbe 0x2f90f7'
      and at(lp, 0x2F90F3) == 'cmp al, 0x28' and at(lp, 0x2F90F5) == 'jb 0x2f9166')
# FF sentinel
sel = dis(0x2367A0, 0x23681E)
check('B3 selector 0xFF compares against 0xFFFF',
      at(sel, 0x2367E3) == 'cmp edi, 0xff' and at(sel, 0x2367E9) == 'mov ecx, 0xffff' and at(sel, 0x2367EE) == 'cmovne ecx, edi')
w = dis(0x31B810, 0x31B856)
check('B3 0031B810 feeds 0xFF when its descriptor gate fails', at(w, 0x31B82B) == 'mov al, 0xff' and at(w, 0x31B835) == 'jmp 0x2367a0')
check('B3-neg the EXP body has no 0xFFFF literal', not any('0xffff' in o for _, _, o in exp))
# installer
inst = dis(0x23A570, 0x23AC80)
check('B4 base row store 0023A9A5 is a QWORD of a 32-bit sum',
      at(inst, 0x23A9A5) == 'mov qword ptr [rdi + 0xe70], rcx' and at(inst, 0x23A99C) == 'imul ecx, edx'
      and at(inst, 0x23A99F) == 'add ecx, eax' and at(inst, 0x23A998) == 'movzx ecx, word ptr [rsi + 0x22]'
      and at(inst, 0x23A994) == 'movzx edx, word ptr [rcx + 8]')
check('B4 per-level row store 0023A9F4 is a QWORD of a 32-bit sum',
      at(inst, 0x23A9F4) == 'mov qword ptr [rdi + 0xe78], rcx' and at(inst, 0x23A9E3) == 'imul ecx, edx'
      and at(inst, 0x23A9E6) == 'add ecx, eax' and at(inst, 0x23A9DF) == 'movzx ecx, word ptr [rsi + 0x24]')
check('B4 descriptor absence and decoded zero both give 0',
      at(inst, 0x23A96F) == 'je 0x23a9a3' and at(inst, 0x23A97C) == 'je 0x23a9a3' and at(inst, 0x23A9A3) == 'xor ecx, ecx'
      and at(inst, 0x23A971) == 'mov ecx, dword ptr [rax + 0xc]')
check('B4-neg stores at a non-site are not row stores', at(inst, 0x23A95E) == 'mov qword ptr [rdi + 0x6e0], rax')
dec = text(dis(0x20E600, 0x20E60A))
check('B4 decoder zero-extends and adds the relocation base',
      dec[0] == 'mov eax, ecx' and dec[1].startswith('add rax, qword ptr [rip') and dec[2] == 'ret ')
# caller
cal = dis(0x312280, 0x3125D9)
check('B5 caller zeroes ECX for both computers',
      at(cal, 0x3124BC) == 'xor ecx, ecx' and at(cal, 0x3124BE) == 'call 0x2f8bb0'
      and at(cal, 0x3124C6) == 'xor ecx, ecx' and at(cal, 0x3124CA) == 'call 0x2f90c0')
check('B5 ebp is zero for the gil floor', at(cal, 0x3122A9) == 'xor ebp, ebp'
      and not any(m in ('mov', 'xor', 'lea', 'pop') and o.startswith('ebp,') for a, m, o in cal if 0x3122A9 < a < 0x312558))
seq = [at(cal, a) for a in (0x312553, 0x312556, 0x312558, 0x31255B, 0x31255D, 0x312562, 0x312564, 0x312566)]
check('B5 floor old+award at 0, set, then notify requested-old',
      seq == ['lea edx, [rax + rdi]', 'test edx, edx', 'cmovns ebp, edx', 'mov ecx, ebp', 'call 0x254ee0',
              'sub ebp, ebx', 'mov ecx, ebp', 'call 0x469e80'], str(seq))
st = dis(0x254EE0, 0x254F28)
check('B5 setter meters requested-current, then clamps 0..99,999,999 and stores',
      at(st, 0x254EF1) == 'sub edx, dword ptr [rax + 8]' and at(st, 0x254F09) == 'mov eax, 0x5f5e0ff'
      and at(st, 0x254F10) == 'cmovns ecx, ebx' and at(st, 0x254F15) == 'cmovg ecx, eax' and at(st, 0x254F1F) == 'mov dword ptr [rax + 8], ecx')
# Model of the stated arithmetic (INFERRED: assumes no intervening balance change, as the package says)
def gil(old, award, cap=99999999):
    req = max(old + award, 0)
    meter = req - old
    note = req - old
    stored = min(max(req, 0), cap)
    return meter, note, stored - old
check('B5 worked example 99,999,995 + 10', gil(99999995, 10) == (10, 10, 4), str(gil(99999995, 10)))
check('B5 worked example 5 - 10', gil(5, -10) == (-5, -5, -5), str(gil(5, -10)))
# notifier
nt = dis(0x469E80, 0x469EBC)
def clears(ins):
    return [o for _, m, o in ins if m == 'mov' and o.startswith('qword ptr [r11 - ') and o.endswith('], rax')]
c = clears(nt)
frame = 0x58
offs = sorted(frame - int(o.split('- ')[1].split(']')[0], 16) for o in c)
check('B6 notifier clears six QWORDs at rsp+0x20..+0x48', at(nt, 0x469E83) == 'sub rsp, 0x58' and offs == [0x20, 0x28, 0x30, 0x38, 0x40, 0x48], str([hex(x) for x in offs]))
check('B6 delta at rsp+0x30 = payload+0x10 (payload r8 = rsp+0x20)',
      at(nt, 0x469EA1) == 'mov dword ptr [rsp + 0x30], ecx' and at(nt, 0x469EA9) == 'lea r8, [r11 - 0x38]' and 0x30 - (frame - 0x38) == 0x10)
check('B6 positive deltas only, event 0x26',
      at(nt, 0x469EA5) == 'test ecx, ecx' and at(nt, 0x469EA7) == 'jle 0x469eb7' and at(nt, 0x469EAF) == 'lea edx, [rax + 0x26]')
ntb = bytearray(raw[off(0x469E80):off(0x469EBC)])
ntb[0x469E9D - 0x469E80:0x469EA1 - 0x469E80] = b'\x90' * 4
check('B6-neg a mutant with one store removed counts five', len(clears(dis(0x469E80, 0x469EBC, bytes(ntb)))) == 5)

# --- C. rerun of run_review.py (WSL Ubuntu-22.04, Python 3.10.12, GCC 11.4.0) -----------------
res = os.path.join(PKG, 'results')
rr = os.path.join(WORK, 'rerun')
same, diff = [], []
for f in sorted(os.listdir(rr)):
    a = json.load(open(os.path.join(rr, f), encoding='utf-8'))
    b = json.load(open(os.path.join(res, f), encoding='utf-8'))
    (same if a == b else diff).append(f)
check('C rerun outputs identical to shipped (14 files)', len(same) == 14 and diff == ['execution_environment.json'], 'diff=%s' % diff)
summ = json.load(open(os.path.join(rr, 'summary.json'), encoding='utf-8'))
check('C rerun summary: 24 bodies, 71/71 native, 6 mutants, 88 spans, 10 corruptions',
      (summ['original_bodies_verified'], summ['native_controls'], summ['native_failures'], summ['code_mutants_rejected'],
       summ['retained_spans_verified'], summ['new_corrupted_record_controls']) == (24, 71, 0, 6, 88, 10))
env = json.load(open(os.path.join(rr, 'execution_environment.json'), encoding='utf-8'))
shipped_env = json.load(open(os.path.join(res, 'execution_environment.json'), encoding='utf-8'))
check('C rerun used the shipped fixture and driver', env['fixture_sha256'] == shipped_env['fixture_sha256']
      and env['driver_sha256'] == shipped_env['driver_sha256'])
# input-pin drift (finding N1)
im = json.load(open(os.path.join(PKG, 'input_manifest.json'), encoding='utf-8'))
drift = []
for r in im['inputs']:
    blob = open(os.path.join(DB, r['path']), 'rb').read()
    if sha(blob) != r['sha256']:
        drift.append(r['path'])
check('C live-tree input drift is exactly one file', drift == ['_experiments/evidence/retained-reward-bindings/check.py'], str(drift))
pre = subprocess.run(['git', 'show', '13a61b94b~1:./_experiments/evidence/retained-reward-bindings/check.py'],
                     cwd=DB, capture_output=True).stdout
pin = [r['sha256'] for r in im['inputs'] if r['path'].endswith('retained-reward-bindings/check.py')][0]
check('C pinned check.py = the pre-image of 13a61b94b', sha(pre) == pin)
check('C rerun tree used that pre-image', sha(open(os.path.join(WORK, 'pindb', '_experiments', 'evidence', 'retained-reward-bindings', 'check.py'), 'rb').read()) == pin)
cur = json.load(open(os.path.join(WORK, 'current_check.json'), encoding='utf-8'))
obs = json.load(open(os.path.join(DB, '_experiments', 'evidence', 'retained-reward-bindings', 'observation.json'), encoding='utf-8'))
check('C current (sealed) check.py --mutations still equals observation.json', cur == obs)

print('PASSES %d' % PASSES)
print('FAILS %d' % len(FAILS) + ('' if not FAILS else ' ' + ', '.join(FAILS)))
