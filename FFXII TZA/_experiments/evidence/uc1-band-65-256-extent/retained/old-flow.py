"""ASTRA's bounded independent UC1 boundary falsification. Static shipping bytes only.

Reads peer tables without modifying them. Reachable instructions, not linear-decode
success alone, determine whether each proposed extent contains its whole control flow.
Unresolved indirect branches stay a limitation. No .pdata is used.
"""
import bisect, collections, csv, hashlib, json, struct
from pathlib import Path
import capstone

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
DB = ROOT / 'Database/FFXII TZA'
EXE = ROOT / 'Database/Tools/work/exe/FFXII_TZA.exe'
ADM = DB / '99-Unresolved-Residual/Unlisted-Code/unlisted-body-admissions.tsv'
BAND = DB / '_index/candidates/uc1-band-1-64-fable-2026-09-25.tsv'
FUNCS = ROOT / 'Database/Tools/work/graph/functions.tsv'
ERRATA = DB / '_index/FUNCTION-EXTENT-ERRATA.tsv'

def table(p):
    return list(csv.DictReader((l for l in p.read_text(encoding='utf-8-sig').splitlines()
                               if l and not l.startswith('#')), delimiter='\t'))

raw = EXE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I', raw, 0x3c)[0]
nsec, opt = struct.unpack_from('<H', raw, pe+6)[0], struct.unpack_from('<H', raw, pe+20)[0]
secs = []
for k in range(nsec):
    p = pe+24+opt+k*40
    vs, va, rs, ro = struct.unpack_from('<IIII', raw, p+8)
    secs.append((raw[p:p+8].rstrip(b'\0').decode(), 0x120000+va, min(vs,rs), ro))

def bytes_at(v, n):
    for _, s, size, off in secs:
        if s <= v and v+n <= s+size:
            return raw[off+v-s:off+v-s+n]
    raise ValueError(('unbacked', hex(v), n))

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True

def flow(v, n, data=None):
    data = bytes_at(v,n) if data is None else data
    ins = list(md.disasm(data,v))
    im = {i.address:i for i in ins}
    pending, seen, problems, exits = [v], set(), [], []
    while pending:
        a = pending.pop()
        if a in seen: continue
        seen.add(a)
        if a not in im:
            problems.append({'address':hex(a),'reason':'reachable missing/mid-instruction boundary'})
            continue
        i = im[a]; nxt = a+i.size
        isbranch = i.group(capstone.CS_GRP_JUMP)
        direct = isbranch and i.operands and i.operands[0].type == capstone.x86.X86_OP_IMM
        target = i.operands[0].imm if direct else None
        if i.group(capstone.CS_GRP_RET) or i.mnemonic in ('int3','ud2','hlt'):
            exits.append([hex(a),i.mnemonic]); continue
        if isbranch:
            if direct and v <= target < v+n: pending.append(target)
            else: exits.append([hex(a),'external/direct' if direct else 'indirect'])
            if i.mnemonic == 'jmp': continue
        pending.append(nxt)
    return {'full_linear': bool(ins) and ins[-1].address+ins[-1].size == v+n,
            'problems':problems,'exits':exits,
            'instructions': [[hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str,
                              i.address in seen] for i in ins]}

adm = table(ADM); rows = table(BAND)
orig = {r['start_va']:r for r in adm if r['verdict']=='body' and 1 <= int(r['bytes']) <= 64}
assert len(rows)>0 and len(orig)==len(rows) and {r['start_va'] for r in rows}==set(orig)
for r in rows:
    assert r['bytes']==orig[r['start_va']]['bytes'] and r['prev_entry']==orig[r['start_va']]['prev_entry']
listed = table(FUNCS)
sizes = {int(r['entry'],16):int(r['body_bytes']) for r in listed
         if r['body_bytes'].isdigit() and not r['name'].startswith(('Unwind@','Catch_All@'))}
for r in table(ERRATA):
    if r['verdict']=='merge' and r['corrected_end'].strip():
        v,end = int(r['entry'],16),int(r['corrected_end'],16)
        if v in sizes and v < end < v+sizes[v]: sizes[v] = end-v

observations=[]
for r in rows:
    v,n = int(r['start_va'],16),int(r['bytes'])
    f=flow(v,n)
    observations.append({'candidate':r,'raw_hex':bytes_at(v,n).hex(),'flow':f})

# Controls exercise detection rather than assuming negative results are sufficient.
controls={
 'split_first':flow(0x125743,16), 'split_second':flow(0x125753,17),
 'small_import':flow(0x862028,6),
 'truncated_candidate':flow(0x7ee7c0,48),
 'complete_candidate':flow(0x7ee7c0,57),
 'cut_one_byte':flow(0x125743,15),
 'internal_target_mid_instruction':flow(0x1000,5,bytes.fromhex('750189c8c3')),
}
# Synthetic detector control: jnz lands in the second byte of mov eax,ecx.
assert not controls['split_first']['problems'] and not controls['split_second']['problems']
assert not controls['small_import']['problems']
assert controls['truncated_candidate']['problems'] and not controls['complete_candidate']['problems']
assert controls['cut_one_byte']['problems'] and controls['internal_target_mid_instruction']['problems']

focused={}
for v,n in [(0x7ee730,208),(0x125740,48),(0x862022,30),(0x7c2a29,47),(0x7298dd,48)]:
    focused[hex(v)]={'bytes':n,'hex':bytes_at(v,n).hex(),'flow':flow(v,n)}

# Focused decoded-call/branch reference check for the extent collision, and cold-tail
# detector control. Every supplying listed/admitted range is named; no opcode-byte
# matches or unwind records are promoted to caller identity.
targets={0x7ee7c0,0x7ee7f0,0x76666f}
references=[]
for v,n in sorted(set(sizes.items()) | {(int(r['start_va'],16),int(r['bytes']))
                                        for r in adm if r['verdict']=='body'}):
    for i in md.disasm(bytes_at(v,n),v):
        if (i.group(capstone.CS_GRP_JUMP) or i.group(capstone.CS_GRP_CALL)) and i.operands and i.operands[0].type==capstone.x86.X86_OP_IMM:
            if i.operands[0].imm in targets:
                references.append({'range_start':hex(v),'range_bytes':n,'site':hex(i.address),
                                   'raw':i.bytes.hex(),'mnemonic':i.mnemonic,'target':hex(i.operands[0].imm)})
assert sum(r['target']=='0x76666f' and r['range_start']=='0x7651f0' for r in references)==4

# Validate the historical raw reference route specifically for the disputed start.
# Its byte-wise scanner can match E8/E9 or LEA inside other instructions.
tn,tv,ts,to = next(s for s in secs if s[0]=='.text')
route_hits=[]
starts=sorted(sizes)
for k in range(to,to+ts-8):
    length=None
    if raw[k] in (0xe8,0xe9): length=5; disp_at=k+1
    elif raw[k] in (0x48,0x4c) and raw[k+1]==0x8d and raw[k+2]&0xc7==5:
        length=7; disp_at=k+3
    if length and tv+k-to+length+struct.unpack_from('<i',raw,disp_at)[0]==0x7ee7c0:
        site=tv+k-to
        idx=bisect.bisect_right(starts,site)-1
        sources=[]
        if idx>=0 and site<starts[idx]+sizes[starts[idx]]:sources.append((starts[idx],sizes[starts[idx]]))
        sources.extend((int(r['start_va'],16),int(r['bytes'])) for r in adm
                       if int(r['start_va'],16)<=site<int(r['start_va'],16)+int(r['bytes']))
        proof=[]
        for v,n in sources:
            decoded=list(md.disasm(bytes_at(v,n),v))
            proof.extend([[hex(v),hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str]
                         for i in decoded if i.address<=site<i.address+i.size])
        route_hits.append({'site':hex(site),'matching_bytes':raw[k:k+length].hex(),
                           'containing_decode':proof})

tail_table=[struct.unpack('<I',bytes_at(0x7c2a30+4*k,4))[0]+0x120000 for k in range(10)]
assert all(0x7c23c0<=t<0x7c2a29 for t in tail_table)

clean = [r for r in observations if r['candidate']['ruling']=='admit']
result={'method':'A static verified shipping instructions; never original execution or live',
 'capstone':capstone.__version__,
 'inputs':{str(p.relative_to(ROOT)).replace('\\','/'):{'bytes':p.stat().st_size,
        'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (EXE,ADM,BAND,FUNCS,ERRATA)},
 'population':dict(collections.Counter(r['ruling'] for r in rows)),
 'proposed_admit_flow_failures':[r['candidate']['start_va'] for r in clean if r['flow']['problems']],
 'observations':observations,'focused':focused,'controls':controls,'focused_direct_references':references,
 'disputed_start_raw_reference_hits':route_hits,
 '007C2A29_tail_table':{'code_stop':'0x7c2a2f','padding_hex':bytes_at(0x7c2a2f,1).hex(),
                      'table_start':'0x7c2a30','targets':[hex(v) for v in tail_table]},
 'listed_007EE7F0': [r for r in listed if r['entry']=='007EE7F0'],
 'limits':['No indirect-target recovery, execution, reachability or universal body count proof.',
           'A reachable direct external branch is an exit, not proof it is a native tail call.',
           'Historical peer reference scan can match opcodes inside immediates; not treated as a validated caller.']}
(HERE/'observation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('method','capstone','population','proposed_admit_flow_failures')},indent=2))
print('PASS seven nonzero flow controls and four cold-tail edges; original byte identity; peer-input membership and extent agreement')
