import hashlib,importlib.util,json
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'selection-correction';sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((R/'result.json').read_text());assert r['producer_sha256']==sha((W/'selection_addendum.py').read_bytes())==sha((R/'producer-before-run.py').read_bytes())
sp=importlib.util.spec_from_file_location('labels',W/'selection_addendum.py');labels=importlib.util.module_from_spec(sp);sp.loader.exec_module(labels)
sp=importlib.util.spec_from_file_location('rd',W/'retained/shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)==r['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);expected={0x36C110:38,0x36C140:84,0x36C1A0:48,0x36C1D0:20};assert len(r['bodies'])==4
for b in r['bodies']:
    a=int(b['entry'],16);n=expected[a];code=(R/(format(a,'08x')+'.bin')).read_bytes();assert code==rd.img_rd(d,ss,a,n) and sha(code)==b['sha256'] and b['bytes']==n
    ii=list(cs.disasm(code,a));assert sum(i.size for i in ii)==n and [dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii]==b['instructions'];assert b['label']==labels.label(a)
    assert not any(i.mnemonic.startswith('lock ') or i.mnemonic in ('call','xchg','cmpxchg') for i in ii)
assert labels.verified_labels(labels.CALL_LABELS);wrong=dict(labels.CALL_LABELS);wrong[0x36C110]='mutex unlock';assert not labels.verified_labels(wrong)
assert r['procedure_controls']==dict(default_verified=True,wrong_mutex_label_rejected=True)
assert [x['target'] for x in r['wrapper_calls']]==['0x36c1d0','0x36c1a0','0x36c110','0x36c140']
assert sha((R/'known-selection-primary.md').read_bytes())==r['known_primary']['retained_sha256']
if (R/'manifest.json').exists():
    for x in json.loads((R/'manifest.json').read_text())['members']:
        b=(W/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
print('PASS_SELECTION_ADDENDUM exact4knownhelpers/defaultlabels/wrongmutexlabel rejection; wholeallocator synchronization remains unproved')
