"""Candidate search only: context references plus local400/3F8 operands."""
from pathlib import Path
import hashlib,json
W=Path('Database/Tools/work/ASTRA');ns={};s=(W/'spawn_load_close_primary.py').read_text()
exec(compile(s[:s.index('for a in (0x233C10')],'<existing PE reader>','exec'),ns)
p=Path('Database/Tools/work/h78/rip_data_refs.tsv')
entries=sorted({int(c[0],16) for l in p.read_text().splitlines()[1:] if (c:=l.split('\t'))[1]=='0209AC30'})
hits=[];incomplete=[]
for a in entries:
 name,n=ns['f'][a];o=ns['off'](a-ns['ib']);data=ns['raw'][o:o+n];ins=list(ns['md'].disasm(data,a))
 if sum(i.size for i in ins)!=n:incomplete.append(dict(address=hex(a),catalog_bytes=n,decoded_bytes=sum(i.size for i in ins)))
 selected=[dict(address=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins if any(t in i.op_str for t in ('0x400','0x3f8'))]
 if selected:hits.append(dict(address=hex(a),name=name,bytes=n,sha256=hashlib.sha256(data).hexdigest(),candidate_sites=selected))
assert any(h['address']=='0x285e60' for h in hits)
assert any(h['address']=='0x280140' for h in hits)
out=dict(exe_sha256=ns['sha'],source=dict(path=p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()),
 candidate_function_count=len(entries),hits=hits,incomplete=incomplete,
 limits='Leads only. Starts from existing RIP-reference index, not all possible indirect context users. Literal400/3F8 operands do not prove context field ownership. Body-count extents/partial decode and multi-step aliases can miss references. Known285E60/280140 positive controls required.')
(W/'spawn-load-close-leads.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Candidate entries',len(entries),'matching functions',len(hits),'incomplete',len(incomplete))
for h in hits:
 print(h['address'],h['name'],h['bytes'])
 for i in h['candidate_sites']:print(i['address'],i['mnemonic'],i['operands'])
