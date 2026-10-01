"""Read-only checker for two bounded original-source follow-up claims."""
import hashlib, json, subprocess, sys
from pathlib import Path

sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
N=Path('Database/FFXII TZA/_experiments/evidence/heading-source-consumers')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(name):return json.loads((W/name).read_bytes())

identity=load('tool-identity.json')
for rec in identity['files'].values():assert sha(rec['path'])==rec['sha256']
assert identity['files']['exe']['sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
base=json.loads((N/'node-reader-feasibility.json').read_bytes())
base_manifest={m['path']:m for m in json.loads((N/'manifest.json').read_bytes())['members']}
assert sha(N/'node-reader-feasibility.json')==base_manifest['node-reader-feasibility.json']['sha256']
step67=next(r for r in base['rows'] if r['step']=='0x45fd10')
step72=next(r for r in base['rows'] if r['step']=='0x52b5e0')
assert any(i['pc']=='0x45fd33' and i['instruction']=='mov rcx, rbx' for i in step67['step_entry_instructions'])
assert any(i['pc']=='0x45fd36' and i['instruction']=='call 0x4607c0' for i in step67['step_entry_instructions'])
assert [(h['pc'],h['kind']) for h in step72['step_direct_offset_hits']]==[('0x52bb35','r')]
assert any(c['pc']=='0x52bb45' and c['target']=='0x52bbd0' for c in step72['step_calls'])

a=load('node-67-reader-result.json');b=load('oscillator-gate-result.json')
receipt=load('node-followup-terminal.json')
assert [r['case'] for r in receipt]==['type-67-reader','type-72-gated-callee']
for item,name in zip(receipt,('node-67-reader-source.py','oscillator-gate-source.py')):
    assert item['terminal'] is True and item['returncode']==0 and not item['stderr']
    assert item['driver_sha256']==sha(W/name)
    q=subprocess.run([sys.executable,'-B',str(W/name)],capture_output=True,text=True)
    assert q.returncode==0 and not q.stderr and json.loads(q.stdout)==json.loads(item['stdout'])
assert a['status']=='ONE_LEVEL_67_READER_FEASIBILITY' and b['status']=='SOURCE_ONLY_NESTED_GATE_OPEN'
assert a['exe_sha256']==b['exe_sha256']==identity['files']['exe']['sha256']
assert a['published_parent_sha256']==b['published_parent_sha256']==sha(N/'node-reader-feasibility.json')
assert a['driver_sha256']==sha(W/'node-67-reader-source.py')
assert b['driver_sha256']==sha(W/'oscillator-gate-source.py')
assert a['policy_sha256']==b['policy_sha256']==identity['files']['policy']['sha256']
assert [(r['entry'],len(r['direct_offset_hits'])) for r in a['rows']]==[('0x2f2530',0),('0x4607c0',2)]
for r in a['rows']:
    assert sha(W/f"node-67-{int(r['entry'],16):08X}.bin")==r['code_sha256']
read=a['rows'][1]
assert [(h['pc'],h['role'],h['base']) for h in read['direct_offset_hits']]==[
    ('0x460aca','r','rbx'),('0x460ad3','w','rbx')]
assert read['rbx_writes_before_first_hit']==[{'pc':'0x4607e2','instruction':'mov rbx, rcx'}]
assert {'pc':'0x460a5b','instruction':'xor r12d, r12d'} in read['r12_writes']
post={x['pc']:x['instruction'] for x in read['post_store_window']}
assert all(post[pc]==op for pc,op in {
    '0x460ada':'mov esi, 0x20','0x460aea':'call 0x533b20',
    '0x460aef':'sub rsi, 1','0x460af3':'jne 0x460ae0'}.items())

assert b['entry']=='0x52bbd0' and b['bytes']==925 and b['extent_status']=='UNWIND_UNION_MATCH'
assert b['fragments']==[{'begin':'0x52bbd0','end':'0x52bf6d','unwind':'0x1d91384'}]
assert sha(W/'oscillator-gate-0052BBD0.bin')==b['code_sha256']
ins={x['pc']:x['mnemonic']+' '+x['operands'] for x in b['instructions']}
assert all(ins[pc]==op for pc,op in {
    '0x52bbf5':'xor ebx, ebx','0x52bbf7':'mov dword ptr [rcx + 0x3f8], ebx',
    '0x52bf21':'mov ebx, 0x20','0x52bf30':'xor r9d, r9d',
    '0x52bf33':'lea rdx, [rsp + 0x30]','0x52bf38':'lea rcx, [rdi + 0x280]',
    '0x52bf3f':'lea r8d, [r9 + 1]','0x52bf43':'call 0x54b1f0',
    '0x52bf48':'sub rbx, 1','0x52bf4c':'jne 0x52bf30'}.items())
assert len([x for x in b['instructions'] if x['mnemonic']=='ret'])==1
assert len(b['transfers'])==7 and all(x['direct'] and 0x52bbd0<=int(x['target'],16)<0x52bf6d for x in b['transfers'])
assert ins['0x52bbf7'] and int(b['calls'][0]['pc'],16)>0x52bbf7
assert '0054B1F0' in (W/'retained/the-per-model-oscillator-subsystem.md').read_text()
claim=load('result.json')
assert claim['status']=='STATIC_ONLY_CONDITIONAL_SOURCE' and claim['live_observation'] is False
assert claim['class_stability']=='OPEN' and claim['full_52bbd0_extent']=='UNWIND_UNION_MATCH'
print(json.dumps({'status':claim['status'],'type_67_reader':'0x460aca',
                  'type_72_clears':'0x52bbf7','type_72_installer_loop':'0x52bf21..0x52bf4c',
                  'live_observation':False,'class_stability':'OPEN'}))
