"""Read-only retained reducer and bounded actual-function regression controls."""
import ast,hashlib,json,struct,sys
from pathlib import Path
from adapter import make,window,observe
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
raw=json.loads((W/'raw.json').read_text());ref=raw['reference'];source=(R/'producer-original.py').read_bytes();s=source.decode()
assert sha(source)==ref['producer_sha256'] and sha((R/'driver-before-run.py').read_bytes())==sha((W/'capture.py').read_bytes())
assert (R/'adapter-before-run.py').read_bytes()==(W/'adapter.py').read_bytes()
assert 'MD.disasm(d[off(f):off(f) + (va - f) + 16], f)' in s and s.count('and boundary(va):')==4
assert make.__defaults__==(True,), 'Corrected source binding must be the default'
old,a=make(s,repaired=False);fixed,b=make(s) if '--fault-old-binding' not in sys.argv else make(s,repaired=False)
assert sha(a.encode())==ref['selected_original_sha256'] and (R/'selected-original.py').read_text()==a
if '--fault-old-binding' not in sys.argv:assert sha(b.encode())==ref['selected_corrected_sha256'] and (R/'selected-corrected.py').read_text()==b
entry=int(ref['entry'],16);candidate=int(ref['candidate'],16);target=int(ref['target'],16);n=ref['bytes'];assert (entry,candidate,target,n)==(0x712090,0x712095,0x6DAA30,48)
image=old['d'];assert sha(image)==ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and fixed['d']==image
o=window(old,entry,n);assert o==window(fixed,entry,n)==ref['file_offset'] and image[o:o+n]==(R/'original-window.bin').read_bytes()
assert ref['root']=='00712090' and len(ref['containing_pdata'])==1 and int(ref['containing_pdata'][0][1],16)>=entry+n
cases=raw['cases'];assert len(cases)==3 and [c['name'] for c in cases]==['original','real-call','immediate-payload']
for c in cases:
    data=(R/(c['name']+'.bin')).read_bytes();assert len(data)==n and sha(data)==c['window_sha256']
    img=bytearray(image);img[o:o+n]=data;img=bytes(img);assert sha(img)==c['image_sha256']
    pc=entry if c['name']=='real-call' else candidate
    assert observe(old,img,entry,pc,target,n)==c['original_path']
    actual=observe(fixed,img,entry,pc,target,n)
    assert actual==c['corrected_default_path'], 'Default source binding regression: actual refs(img) must reject the immediate-data payload'
assert cases[0]['original_path']['refs']==cases[0]['corrected_default_path']['refs']==[]
assert cases[1]['original_path']['refs']==cases[1]['corrected_default_path']['refs']==[['rel32','00712090']]
positive=(R/'real-call.bin').read_bytes();assert positive[:5]==b'\xe8'+struct.pack('<i',target-(entry+5))
negative=(R/'immediate-payload.bin').read_bytes();assert negative[:10]==b'\x48\xb8'+b'\x90'*3+b'\xe8'+struct.pack('<i',target-(candidate+5))
c=cases[2];assert c['original_path']['refs']==[['rel32','00712095']] and c['corrected_default_path']['refs']==[]
assert c['original_path']['boundary_with_image'] is True and c['corrected_default_path']['boundary_with_image'] is False
i=c['corrected_default_path']['decode'][0];assert i['pc']=='00712090' and i['size']==10 and i['mnemonic']=='movabs' and '00712095' not in c['corrected_default_path']['source_boundaries']
assert raw['cleanup']['original_reference_unchanged'] and raw['cleanup']['peer_producer_unchanged'] and raw['cleanup']['pc_off']
result=dict(question=raw['question'],method=raw['method'],reference=ref,raw_sha256=sha((W/'raw.json').read_bytes()),established='Actual unchanged refs(img) accepts E8/rel32 payload at00712095 inside a private MOV immediate, because boundary ignores img and reads original d. Corrected default forwards img in all3 boundary calls and decodes img: realCALL at00712090 remains detected, immediate payload rejected.',not_established='Historical default original-image census wrong; any actual computed caller; full image unreachable; all instruction boundaries/PE gaps/leaf roots; YEBIS family association false; any game behavior. Projection is48B, not a new whole-image scan.',affected_claims='FABLE planted-reference control cannot establish image-consistent boundaries for changed inputs. Qualify no-call language to actual searched patterns/boundary algorithm; computed/encoded/derived inside/outside-image paths remain unresolved. Preserve positive shared third-table/YEBIS association and source selector coupling.',required_change='FABLE producer boundary must use img and refs must forward img on actual invocation path; add realCALL/immediate-data control. Adjust producer/check/procedure and only dependent caller/unreachability consumers, preserving prior record/additive correction; OPUS/SPEC review separate.',cleanup=raw['cleanup'],limits='A source-only private in-memory patches, actual selected unchanged functions plus disclosed local two-site repair/default scoped projection. Original bytes never execute/deploy, no native/live/source tables modified; no semantic acceptance/admission shortcut. PC OFF/S19 extension unapproved/full L1+L2 NOT_MET.')
out=W/'result.json'
if out.exists():assert json.loads(out.read_text())==result
else:out.write_text(json.dumps(result,indent=2)+'\n')
manifest=W/'manifest.json'
if manifest.exists():
 for m in json.loads(manifest.read_text())['members']:
  data=(W/m['path']).read_bytes();assert len(data)==m['bytes'] and sha(data)==m['sha256'],m['path']
print('PASS retained original3 windows and actual old/corrected-default function calls; real-CALL positive, immediate-data negative; no original instructions executed',flush=True)
