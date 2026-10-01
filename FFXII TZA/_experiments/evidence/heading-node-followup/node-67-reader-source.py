"""One-level original source scan for a type-0x67 field consumer."""
import hashlib, json, sys, types
from pathlib import Path
import capstone

sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
P=Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
N=Path('Database/FFXII TZA/_experiments/evidence/heading-source-consumers')
X=Path('Database/Tools/work/exe/FFXII_TZA.exe')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(X)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pm={m['path']:m for m in json.loads((P/'manifest.json').read_bytes())['members']}
nm={m['path']:m for m in json.loads((N/'manifest.json').read_bytes())['members']}
for f in ('retained/functions.tsv','retained/reg_tracking.py','python-deps/pefile.py'):
    assert sha(P/f)==pm[f]['sha256']
assert sha(N/'node-reader-feasibility.json')==nm['node-reader-feasibility.json']['sha256']
parent=json.loads((N/'node-reader-feasibility.json').read_bytes())
row=next(r for r in parent['rows'] if r['step']=='0x45fd10')
assert row['step_direct_offset_hits']==[] and [(x['pc'],x['target']) for x in row['step_calls']]==[
    ('0x45fd1d','0x2f2530'),('0x45fd36','0x4607c0')]
sys.path.insert(0,str((P/'python-deps').resolve()))
import pefile
roles=types.ModuleType('roles');policy=P/'retained/reg_tracking.py'
exec(compile(policy.read_bytes(),str(policy),'exec'),roles.__dict__)
cat={}
for line in (P/'retained/functions.tsv').read_text('utf-8').splitlines()[1:]:
    if line.startswith(('002F2530\t','004607C0\t')):
        a=int(line.split('\t')[0],16);cat[a]=(int(line.split('\t')[2]),line)
assert set(cat)=={0x2f2530,0x4607c0}
pe=pefile.PE(str(X),fast_load=True);assert pe.OPTIONAL_HEADER.ImageBase==0x120000
image=X.read_bytes();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
out=[]
for a in sorted(cat):
    size,line=cat[a];off=pe.get_offset_from_rva(a-0x120000);code=image[off:off+size]
    ins=list(cs.disasm(code,a));assert ins and sum(i.size for i in ins)==size
    if '--write-result' in sys.argv:(W/f'node-67-{a:08X}.bin').write_bytes(code)
    hits=[]
    for i in ins:
        for j,o in enumerate(i.operands):
            if o.type==capstone.CS_OP_MEM and o.mem.disp==0x3d8:
                hits.append({'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,
                             'operands':i.op_str,'base':cs.reg_name(o.mem.base),'index':cs.reg_name(o.mem.index),
                             'role':roles.op_kind(i,o,j)})
    first=min((int(h['pc'],16) for h in hits),default=None)
    before=[{'pc':hex(i.address),'instruction':i.mnemonic+' '+i.op_str} for i in ins
            if first is not None and i.address<first and 'rbx' in roles.written(i)]
    windows=[]
    for n,i in enumerate(ins):
        if first is not None and i.address in {int(h['pc'],16) for h in hits}:
            windows.append([{'pc':hex(q.address),'instruction':q.mnemonic+' '+q.op_str}
                            for q in ins[max(0,n-6):min(len(ins),n+6)]])
    out.append({'entry':hex(a),'catalogue':line,'bytes':size,'code_sha256':hashlib.sha256(code).hexdigest(),
                'direct_offset_hits':hits,'call_sites':[{'pc':hex(i.address),'target':i.op_str}
                                                   for i in ins if i.mnemonic=='call'],
                'entry_instructions':[{'pc':hex(i.address),'instruction':i.mnemonic+' '+i.op_str}
                                      for i in ins[:18]],
                'rbx_writes_before_first_hit':before,
                'r12_writes':[{'pc':hex(i.address),'instruction':i.mnemonic+' '+i.op_str}
                               for i in ins if 'r12' in roles.written(i)],
                'hit_windows':windows,
                'post_store_window':[{'pc':hex(i.address),'bytes':i.bytes.hex(),
                                      'instruction':i.mnemonic+' '+i.op_str}
                                     for i in ins if a==0x4607c0 and 0x460ad3<=i.address<=0x460af5]})
assert sha(X)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
result={'status':'ONE_LEVEL_67_READER_FEASIBILITY','method':'A original source, no native/live execution',
        'exe_sha256':sha(X),'driver_sha256':sha(Path(__file__)),'policy_sha256':sha(policy),
        'published_parent_sha256':sha(N/'node-reader-feasibility.json'),'rows':out,
        'limits':'Only exact direct 0x3D8 operands in two catalogued immediate callees. No proven full extents, receiver identity, nested/indirect readers, scheduling, initialized state or presentation.'}
if '--write-result' in sys.argv:(W/'node-67-reader-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'hits':[(r['entry'],len(r['direct_offset_hits'])) for r in out],
                  'calls':[(r['entry'],len(r['call_sites'])) for r in out]},indent=2))
