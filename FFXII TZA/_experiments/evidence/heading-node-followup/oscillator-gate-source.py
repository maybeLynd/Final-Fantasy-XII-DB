"""Read one shipping FF12 type-0x72 gated callee; no execution/live claim."""
import ast, hashlib, json, struct, sys, types
from pathlib import Path
import capstone

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
P = Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
N = Path('Database/FFXII TZA/_experiments/evidence/heading-source-consumers')
X = Path('Database/Tools/work/exe/FFXII_TZA.exe')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(X) == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pm = {m['path']:m for m in json.loads((P/'manifest.json').read_bytes())['members']}
nm = {m['path']:m for m in json.loads((N/'manifest.json').read_bytes())['members']}
for path in ('retained/functions.tsv','retained/reg_tracking.py','retained/producer-source.py','python-deps/pefile.py'):
    assert sha(P/path) == pm[path]['sha256']
assert sha(N/'node-reader-feasibility.json') == nm['node-reader-feasibility.json']['sha256']
prev = json.loads((N/'node-reader-feasibility.json').read_bytes())
row = next(r for r in prev['rows'] if r['step']=='0x52b5e0')
assert row['step_direct_offset_hits'][0]['pc']=='0x52bb35'
assert any(c['pc']=='0x52bb45' and c['target']=='0x52bbd0' for c in row['step_calls'])
sys.path.insert(0,str((P/'python-deps').resolve()))
import pefile
roles = types.ModuleType('roles')
policy = P/'retained/reg_tracking.py'
exec(compile(policy.read_bytes(),str(policy),'exec'),roles.__dict__)
catalogue = None
for line in (P/'retained/functions.tsv').read_text('utf-8').splitlines()[1:]:
    if line.startswith('0052BBD0\t'):
        catalogue = line; break
assert catalogue is not None and int(catalogue.split('\t')[2])==925
pe = pefile.PE(str(X),fast_load=True)
assert pe.OPTIONAL_HEADER.ImageBase == 0x120000
image = X.read_bytes(); off=pe.get_offset_from_rva(0x52bbd0-0x120000)
code = image[off:off+925]
assert len(code)==925
# Reuse the reviewed original metadata parser for a rooted extent check.
source=(P/'retained/producer-source.py').read_bytes()
nodes=[x for x in ast.parse(source).body if isinstance(x,ast.FunctionDef) and x.name in ('OFF','chain_root')]
assert len(nodes)==2
base=pe.OPTIONAL_HEADER.ImageBase
secs=[(s.Name.rstrip(b'\0').decode(),base+s.VirtualAddress,max(s.Misc_VirtualSize,s.SizeOfRawData),
       s.PointerToRawData,s.SizeOfRawData) for s in pe.sections]
meta={'blob':image,'BASE':base,'SECS':secs,'struct':struct}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'reviewed original extent functions','exec'),meta)
pdata=next(s for s in secs if s[0]=='.pdata')
praw=image[pdata[3]:pdata[3]+pdata[4]]
entries={}
for n in range(0,len(praw)-11,12):
    begin,end,unwind=struct.unpack('<III',praw[n:n+12])
    if begin:entries[base+begin]=(base+end,base+unwind)
meta['pent']=entries
fragments=sorted((a,entries[a][0],entries[a][1]) for a in entries if meta['chain_root'](a)==0x52bbd0)
contiguous=bool(fragments) and all(fragments[n][1]==fragments[n+1][0] for n in range(len(fragments)-1))
extent_ok=contiguous and fragments[0][0]==0x52bbd0 and fragments[-1][1]-fragments[0][0]==925
assert extent_ok, ('Unproved original 0052BBD0 function extent; stop before loop inference',fragments)
cs = capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ins=list(cs.disasm(code,0x52bbd0))
assert ins and ins[0].address==0x52bbd0 and sum(i.size for i in ins)==925
rows=[]
for i in ins:
    rows.append({'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str,
                 'writes':sorted(roles.written(i)),
                 'memory':[{'operand':j,'kind':roles.op_kind(i,o,j),'base':cs.reg_name(o.mem.base),
                            'displacement':o.mem.disp,'bytes':o.size}
                           for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]})
calls=[{'pc':hex(i.address),'target':i.op_str,'direct':i.operands[0].type==capstone.CS_OP_IMM}
       for i in ins if i.mnemonic=='call']
transfers=[{'pc':hex(i.address),'mnemonic':i.mnemonic,'target':i.op_str,
            'direct':i.operands[0].type==capstone.CS_OP_IMM}
           for i in ins if i.group(capstone.CS_GRP_JUMP)]
assert any(c['target']=='0x54b1f0' and c['direct'] for c in calls), calls
assert sha(X)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
result={'status':'SOURCE_ONLY_NESTED_GATE_OPEN','method':'A; original static byte read, no FF12/native execution',
        'exe_sha256':sha(X),'driver_sha256':sha(Path(__file__)),'capstone_version':capstone.__version__,
        'pefile_sha256':sha(Path(pefile.__file__)),'policy_sha256':sha(policy),
        'published_parent_sha256':sha(N/'node-reader-feasibility.json'),
        'entry':'0x52bbd0','catalogue':catalogue,'bytes':len(code),'code_sha256':hashlib.sha256(code).hexdigest(),
        'extent_status':'UNWIND_UNION_MATCH','fragments':[{'begin':hex(a),'end':hex(e),'unwind':hex(u)} for a,e,u in fragments],
        'instructions':rows,'calls':calls,'transfers':transfers,
        'limits':'Original rooted 925B metadata/complete decode, not all callee effects; parent receiver/step timing conditional, no initialized/live/presentation inference.'}
if '--write-result' in sys.argv:
    (W/'oscillator-gate-result.json').write_text(json.dumps(result,indent=2)+'\n')
    (W/'oscillator-gate-0052BBD0.bin').write_bytes(code)
print(json.dumps({'status':result['status'],'calls':calls,'transfers':len(transfers),
                  'instruction_count':len(rows),'code_sha256':result['code_sha256']},indent=2))
