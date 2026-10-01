"""Readonly input-pair/host-control evidence, no checker invocation or binary writes."""
import hashlib,importlib.util,json
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text());ref=r['reference']
assert sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())==r['driver_sha256']
assert sha((R/'producer.py').read_bytes())==ref['producer_sha256']
assert sha((R/'shipping-reader.py').read_bytes())==ref['reader_sha256']=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('retained_reader',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image()
assert sha(image)==ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
original=[];changed=[]
assert len(ref['body_sources'])==4 and [x['entry'] for x in ref['body_sources']]==['00229E70','0020E600','0020E620','00339630']
for b in ref['body_sources']:
    entry=int(b['entry'],16);raw=(R/(b['entry']+'.bin')).read_bytes()
    assert len(raw)==b['bytes'] and sha(raw)==b['sha256'] and rd.img_rd(image,ss,entry,len(raw))==raw
    ii=list(cs.disasm(raw,entry));assert sum(i.size for i in ii)==len(raw)
    for i in ii:
        op=(i.mnemonic+' '+i.op_str).rstrip();line=f'{i.address:08X} {entry:08X} {op}'
        original.append(line);changed.append(f'{i.address:08X} {entry:08X} jbe 0x229e91' if i.address==0x229E7E else line)
view=(R/'original-view.txt').read_bytes();mv=(R/'changed-view.txt').read_bytes()
assert view==('\n'.join(original)+'\n').encode() and mv==('\n'.join(changed)+'\n').encode()
assert sha(view)==ref['original_view_sha256'] and sha(mv)==ref['changed_view_sha256'] and sum(a!=b for a,b in zip(original,changed))==1
m=r['mutation'];assert m==json.loads((W/'mutation.json').read_text()) and m['pc']=='0x229e7e' and m['original_hex']=='72' and m['changed_hex']=='76'
off=int(m['file_offset'],16);mut=bytearray(image);assert mut[off]==0x72;mut[off]=0x76
assert len(mut)==m['changed_image_bytes'] and sha(mut)==m['changed_image_sha256']
assert sha(rd.img_rd(image,ss,0x229E70,37))==m['original_body_sha256'] and sha(rd.img_rd(mut,ss,0x229E70,37))==m['changed_body_sha256']
rec=r['receipts'];assert len(rec)==3 and rec==json.loads((W/'partial-receipts.json').read_text()) and [x['returncode'] for x in rec]==[0,0,1]
assert [x['name'] for x in rec]==['original-pair','stale-view-changed-image','changed-view-changed-image']
for x in rec:
    out=(R/(x['name']+'.stdout')).read_bytes();err=(R/(x['name']+'.stderr')).read_bytes();assert sha(out)==x['stdout_sha256'] and sha(err)==x['stderr_sha256'] and not err
    pairs=[(p[1],p[0]) for l in out.decode().splitlines() if len(p:=l.split())>=3 and p[0] in ('PASS','FAIL')]
    assert len(pairs)==4 and {a for a,b in pairs}=={'R1','I1','A1','C'} and dict(pairs)==x['tags']
assert rec[0]['tags']==rec[1]['tags']==dict(R1='PASS',I1='PASS',A1='PASS',C='PASS') and rec[2]['tags']==dict(R1='FAIL',I1='PASS',A1='PASS',C='PASS')
assert [x['view_sha256'] for x in rec]==[sha(view),sha(view),sha(mv)] and [x['exe_sha256'] for x in rec]==[sha(image),sha(mut),sha(mut)]
c=json.loads((W/'cleanup.json').read_text());assert c==r['cleanup'] and c['changed_private_copy_removed'] and c['original_readback_sha256']==ref['exe_sha256']
if (W/'manifest.json').exists():
    members=json.loads((W/'manifest.json').read_text())['members'];assert members
    for x in members:
        d=(W/x['path']).read_bytes();assert len(d)==x['bytes'] and sha(d)==x['sha256']
print('PASS_HOST_VIEW_BINDING originalpair/stalepair-green/matchingchangedview-R1-fails/inputbyteidentities/cleanup; no original/native/live semantics or historicaldefaultpair defect proved')
