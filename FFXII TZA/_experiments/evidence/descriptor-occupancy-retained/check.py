"""Bounded Method A reduction of EXP124's retained descriptor list-head bytes.
No live access, observer import, native execution, or default-buffer recapture.
"""
import collections, copy, hashlib, json, struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
SRC=ROOT/'Database/FFXII TZA/_experiments/evidence/phyre-startup-globals'
RAW_SHA='25931a0cb4f734c941b04ad50281a7c18a86119c9d02c13b64e5d4b4f3ef0b05'
EXE_SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'

def reduce(r):
 assert r['status']=='OBSERVED' and r['pid']==34568 and r['image_base']==0x120000
 assert r['exe_sha256']==EXE_SHA and r['null_read_rejected'] and not r['debugger_present'] and r['read_handle_closed']
 assert r['modules_before']==r['modules_after'] and len(r['modules_before'])==102
 for phase in ('text_before','text_after'):
  t=r[phase];assert t['bytes']==7996981 and t['matches'] and t['live_sha256']==t['disk_sha256']=='5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
 assert len(r['descriptors'])==r['requested_descriptors']==173
 positives=[x for x in r['reads'] if x['purpose']=='nonzero positive']
 assert positives and all(x['address']==0x1ccd300 and x['size']==6 and x['hex']=='19930d0a1a0a' for x in positives)
 before={};after={}
 for i,x in enumerate(r['reads']):
  if x['purpose'] in ('descriptor-before','descriptor-after'):
   out=before if x['purpose']=='descriptor-before' else after
   assert x['address'] not in out and x['size']==0x108 and len(bytes.fromhex(x['hex']))==0x108
   out[x['address']]=(i,x)
 assert len(before)==len(after)==173
 rows=[]
 for item in r['descriptors']:
  target=item['target'];a=target['address'];bi,b=before[a];ai,z=after[a]
  assert bi<ai and b['hex']==z['hex'] and item['header_bracket_matches']
  h=bytes.fromhex(b['hex']);q=lambda o:struct.unpack_from('<Q',h,o)[0]
  assert q(0)==item['fields']['vtable'] and q(0)!=0
  assert q(0x30)==item['fields']['name_pointer'] and struct.unpack_from('<I',h,0x38)[0]==target['size']==item['fields']['size']
  assert q(0xc0)==target['default_address']==item['fields']['default_pointer'] and item['pointer_matches']
  flags=struct.unpack_from('<I',h,0xfc)[0]
  assert flags==item['fields']['flags'] and bool(flags&0x80000000)==item['prepared_bit31']
  nm=[x for x in r['reads'][bi+1:ai] if x['purpose']=='class-name-byte']
  assert nm and all(x['address']==q(0x30)+k and x['size']==1 and len(bytes.fromhex(x['hex']))==1 for k,x in enumerate(nm))
  name=bytes.fromhex(''.join(x['hex'] for x in nm));assert name.endswith(b'\0')
  name=name[:-1].decode('ascii');assert name==item['name'] and name.split('::')[-1]==target['name']
  links={}
  for o in (0x60,0x90,0xb0):
   f,p=q(o),q(o+8);head=a+o
   tag='self-linked' if f==p==head else 'null/uninitialized-or-invalid' if not f or not p else 'non-self-linked'
   links[hex(o)]={'head':hex(head),'next':hex(f),'previous':hex(p),'state':tag}
  rows.append({'descriptor':hex(a),'name':name,'instance_size':target['size'],'vtable':hex(q(0)),
               'prepared_default_bit31':item['prepared_bit31'],'links':links,
               'raw_read_indexes':[bi,ai],'header_sha256':hashlib.sha256(h).hexdigest()})
 assert len({x['descriptor'] for x in rows})==173
 return {'rows':rows,'counts':{hex(o):dict(collections.Counter(x['links'][hex(o)]['state'] for x in rows)) for o in (0x60,0x90,0xb0)}}

raw=(SRC/'title-defaults.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==RAW_SHA
m=json.loads((SRC/'manifest.json').read_text());receipt=next(x for x in m['artifacts'] if x['path']=='title-defaults.json')
assert receipt['bytes']==len(raw) and receipt['sha256']==RAW_SHA
r=json.loads(raw);out=reduce(r)
# A known actually captured non-self method-list head is a detector positive,
# not proof that all its nodes form a valid/owned ring.
positive=next(x for x in out['rows'] if x['name']=='PAnimatableComponent')
assert positive['links']['0x90']['state']=='non-self-linked'
assert out['counts']['0x90']['non-self-linked']==24
mutations=[]
for label in ('changed-after','short-header','wrong-name','zero-case'):
 c=copy.deepcopy(r)
 if label=='changed-after':
  x=next(x for x in c['reads'] if x['purpose']=='descriptor-after');b=bytearray.fromhex(x['hex']);b[0x60]^=1;x['hex']=b.hex()
 elif label=='short-header':next(x for x in c['reads'] if x['purpose']=='descriptor-before')['size']=0x100
 elif label=='wrong-name':c['descriptors'][0]['target']['name']='wrong identity'
 else:c['descriptors']=[];c['requested_descriptors']=0
 try:reduce(c)
 except (AssertionError,ValueError,KeyError):mutations.append({'case':label,'rejected':True})
 else:raise AssertionError('missed corruption '+label)
# Synthetic reducer-only controls ensure zeros are not promoted to empty and a
# populated candidate is detectable, rather than hardcoding all heads as empty.
controls={}
for label,f,p in [('null',0,0),('nonself',0x2cb0c30,0x2cb1470)]:
 c=copy.deepcopy(r);a=c['descriptors'][0]['target']['address']
 for x in c['reads']:
  if x['address']==a and x['purpose'] in ('descriptor-before','descriptor-after'):
   b=bytearray.fromhex(x['hex']);struct.pack_into('<QQ',b,0x60,f,p);x['hex']=b.hex()
 state=reduce(c)['rows'][0]['links']['0x60']['state'];controls[label]=state
assert controls=={'null':'null/uninitialized-or-invalid','nonself':'non-self-linked'}
out.update(method='A retained C sample reduction; no new observation',source_raw_sha256=RAW_SHA,
           source_pid=34568,exe_sha256=EXE_SHA,positive_descriptor=positive['descriptor'],
           corruptions=mutations,synthetic_detector_controls=controls,
           limits=['Title state only; 173 named/bracketed descriptors, not all410 statics or all heap descriptors.',
                   'Seven extra ancestor headers excluded from bracketed count; four failed mappings remain outside it.',
                   'Equal sequential brackets do not prove atomicity, continuous lifetime, or never-populated semantics.',
                   'Default preparation is separate: seven unprepared buffers remain unknown; no buffer interpretation changed.',
                   'Non-self control describes head words, not node ownership, payload or complete ring validity.'])
(HERE/'observation.json').write_bytes((json.dumps(out,indent=2)+'\n').encode())
print(json.dumps(out['counts'],indent=2))
print('PASS 173 identity/extent/name/bracket controls;24 captured nonself method-head positives;4 corruption rejects;2 synthetic detector cases.')
