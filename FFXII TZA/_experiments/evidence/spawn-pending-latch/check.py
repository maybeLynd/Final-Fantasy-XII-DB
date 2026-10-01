"""Primary-byte and local call/order checks; no execution or global absence proof."""
import hashlib,json
from pathlib import Path
W=Path('Database/Tools/work/ASTRA');ns={}
s=(W/'spawn_pending_primary.py').read_text()
exec(compile(s[:s.index('for a in (0x332130')],str(W/'spawn_pending_primary.py'),'exec'),ns)
cat={int(b['address'],16):b for n in ('primary','callers') for b in json.loads((W/('spawn-pending-'+n+'.json')).read_text())['bodies']}
assert len(cat)==10
for a,b in cat.items():
    raw=b'';pos=a
    for i in b['instructions']:
        assert int(i['address'],16)==pos
        d=bytes.fromhex(i['bytes']);raw+=d;pos+=len(d)
    o=ns['off'](a-ns['ib'])
    assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'] and raw==ns['raw'][o:o+len(raw)]
    last=b['instructions'][-1]
    assert last['mnemonic'] in ('ret','jmp') or (a==0x32ED80 and last['mnemonic']=='call' and last['operands']=='0x809728')
def at(a):return next(i for b in cat.values() for i in b['instructions'] if int(i['address'],16)==a)
assert at(0x332150)['operands']=='rbx, 0xfffffffffffffffe'
assert at(0x332154)['mnemonic']=='mov' and at(0x332178)['operands']=='0x32f1b0'
assert at(0x33216F)['operands']=='0x33217d' and at(0x332174)['operands']=='0x33217d'
assert at(0x37821F)['operands']=='ecx, ecx' and at(0x378225)['operands']=='0x332130'
assert at(0x3776DB)['operands']=='0x3776e9' and at(0x3776DD)['operands']=='0x378120'
assert at(0x3776E2)['operands'].endswith(', 0xfffffff7')
assert at(0x25D4E1)['operands'].endswith(', 0xfd')
assert all(i['operands']!='0x332130' for i in cat[0x32F6F0]['instructions'] if i['mnemonic'] in ('call','jmp'))
ref=Path('Database/Tools/work/graph/imagebase_refs.tsv')
rows=[l for l in ref.read_text().splitlines() if '\t022C6E48\t' in l]
assert rows and any(l.startswith('0032ED80\t0032F0FF\t') for l in rows)
assert not any(l.startswith('00332130\t') for l in rows)
out=dict(exe_sha256=ns['sha'],method='A only',catalog_extents=10,primary_bytes_verified=True,
    pending_mask_reference_export=dict(path=str(ref).replace('\\','/'),sha256=hashlib.sha256(ref.read_bytes()).hexdigest(),selected_rows=rows,
        control='Known indexed reset0032F0FF present; known RIP-base latch clearer00332130 absent. Export is not an exhaustive writer proof.'),
    rejected_lead='0032F6F0 is a path-string rewrite helper, not the pending latch; retained to avoid repeating the lead.',
    limits='Local original call/order and field semantics; no B/live execution or transitive native initialization/scheduling proof.',checks='pass')
(W/'spawn-pending-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(out,indent=2))
