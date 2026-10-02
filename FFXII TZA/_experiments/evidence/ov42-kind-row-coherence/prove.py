"""Prove the conditional full32 classifier / low16 queue consistency invariant."""
import copy,hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def module(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def receipt(tag,driver):
 s=json.loads((P/(tag+'.status.json')).read_text());need(s.get('terminal') is True and s.get('exit')==0 and s.get('exception') is None and s.get('driver_sha256')==sha(P/driver) and bool((P/(tag+'.stdout')).read_bytes()) and not(P/(tag+'.stderr')).read_bytes(),'required successful current invocation '+tag)
def derive(ix,d,G):
 ops=[(0x306be0,'mov','rsi, rdx'),(0x306c0a,'mov','ebx, 3'),(0x306c40,'mov','dword ptr [rip + 0x1fbb516], 2'),(0x306c4d,'call','0x309230'),(0x306c52,'mov','edx, eax'),(0x306c54,'mov','ecx, ebx'),(0x306c56,'call','0x32fc30'),(0x306c5b,'mov','ecx, ebx'),(0x306c5d,'call','0x32ed70'),(0x306c62,'mov','rax, qword ptr [rip + 0x2bb84cf]'),(0x306c69,'mov','ecx, dword ptr [rax + 0xc]'),(0x306c6c,'call','0x20e600'),(0x306c71,'sub','esi, eax'),(0x306c73,'xor','edx, edx'),(0x306c75,'mov','rax, qword ptr [rip + 0x2bb84bc]'),(0x306c7c,'movzx','ecx, word ptr [rax + 8]'),(0x306c80,'mov','eax, esi'),(0x306c82,'div','ecx'),(0x306c84,'add','eax, 0xffffff6c'),(0x306c89,'cmp','eax, 0x7f'),(0x306c8c,'ja','0x306ccc'),(0x306c8e,'lea','rdx, [rip - 0x1e6c95]'),(0x306c95,'movzx','eax, byte ptr [rdx + rax + 0x1e6d08]'),(0x306c9d,'mov','ecx, dword ptr [rdx + rax*4 + 0x1e6cec]'),(0x306ca4,'add','rcx, rdx'),(0x306ca7,'jmp','rcx'),(0x306cb7,'mov','ebx, 4'),(0x306cd6,'mov','eax, 1'),(0x306cdb,'mov','dword ptr [rip + 0x1fbb47b], ebx')]
 for pc,m,a in ops:need(pc in ix and(ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'classifier operation changed '+hex(pc))
 need(d['jump_dwords']==[0x1e6cbe,0x1e6cc5,0x1e6cd1,0x1e6cb7,0x1e6ca9,0x1e6cb0,0x1e6ccc] and len(d['mapping'])==128 and set(d['mapping'])<=set(range(7)),'original classifier targets/domain changed')
 # No semantic-name/table corpus census: derive only which finite dispatch
 # entries can publish literal4, from their original instruction paths.
 arms=[]
 for k,t in enumerate(d['jump_dwords']):
  target=0x120000+t;g=G.graph(ix,target,0x306cec)
  defs=[i['args'] for a,i in sorted(ix.items()) if a in g['visited'] and i['mnemonic']=='mov' and i['args'].startswith('ebx, ')]
  need(len(defs)<=1 and 0x306cdb in g['visited'],'classifier arm publication changed')
  value=int(defs[0].split(',')[1],0) if defs else 3
  arms.append(dict(selector=k,target=hex(target),published_kind=value))
 need([a['selector'] for a in arms if a['published_kind']==4]==[3],'kind4 source arm changed')
 indices=[i for i,s in enumerate(d['mapping']) if s==3];need(indices==list(range(60,78)),'kind4 row band changed')
 v=copy.deepcopy(ix);v[0x306ca7]['args']='0x306cb7';g=G.graph(v,0x306c62,0x306cec,fixed={0x306c8c:False})
 need(G.dominates(g,0x306c82,0x306cdb),'kind publication bypasses quotient')
 # Original queue source is separately byte-verified by main, not an oracle
 # fixture: check its exact quotient and narrowing operations here too.
 for pc,m,a in [(0x3068a7,'sub','edi, eax'),(0x3068a9,'xor','edx, edx'),(0x3068b2,'movzx','ecx, word ptr [rax + 8]'),(0x3068b6,'mov','eax, edi'),(0x3068b8,'div','ecx'),(0x3068c2,'cmp','ax, dx'),(0x3068c7,'movzx','eax, ax'),(0x3068ca,'sub','eax, 0xd0')]:
  need((ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'queue comparison operation changed '+hex(pc))
 return dict(classifier='Unsigned full32 q=floor(((low32(row)-low32(lookup base)) mod2^32)/u16(second context+8)). Positive divisor/normal ABI/readable state required. ADD EAX,-94 and unsigned CMP7F admit full q148..275, not low16(q).',kind4='Published kind4 iff admitted full classifier quotient lies208..225, under this function\'s kind-publishing path and unchanged original embedded table.',arms=arms,conditional_invariant='If the queue dispatch still uses this published kind4 and its full quotient equals the classifier quotient, queued WORD is208..225 and queue DWORD0..17. Thus511..534 excluded under that explicit equality/stable-kind premise.',sufficient_binding='Same incoming row low32, same lookup-base low32 and same positive divisor suffice for equal quotients. Exact quotient equality is the weaker sufficient premise; pointer identity is not necessary and is not established.',unproved='Actual same-row/caller/owner relationship, descriptor consistency between the two loads and across calls, kind persistence and scheduling are not proved. This is a conditional invariant, not natural impossibility.',countermodels=[dict(classifier_q=208,published_kind=4,queue_q=511,queue_dword=303,meaning='Changing bindings can invalidate the conditional exclusion; mathematical supplied-state model only.'),dict(classifier_q=65744,published_kind=7,queue_q=65744,queue_dword=0,meaning='Classifier uses full32, queue low16 aliases208; do not narrow classifier before its guard.')],request_status='On the kind-publishing normal-return path,32FC30 result is not tested before32ED70; its RAX is dead at that call and subsequently overwritten by the context load. No native armer/slot effects or successful presentation are certified by this.',limits='STATIC_ONLY conditional original-code facts. No full interpreter/live initialization, natural candidate use, resource success, owner/kind reachability/lifetime/reuse or whole OV42 closure.')
def main():
 out=Path(sys.argv[1]);out=out if out.is_absolute() else P/out;need(not out.exists(),'immutable result exists')
 for tag,driver in [('extent-01','extent.py'),('capture-02','capture.py'),('data-01','capture-data.py')]:receipt(tag,driver)
 need(sha(P/'capture-index-path.py')=='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497' and sha(P/'validate-title-source-annotations.py')=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed dependency changed')
 V=module('roles','validate-title-source-annotations.py');G=module('cfg','prove_owner_reload_order.py')
 x=json.loads((P/'source-01.json').read_text());r=json.loads((P/'retained-prefix-01.json').read_text());d=json.loads((P/'data-01.json').read_text());lineage=json.loads((P/'retained-lineage-01.json').read_text());e=json.loads((P/'extent-01.json').read_text())
 need(x.get('wrapper_complete') is True and x['invocation_driver_sha256']==sha(P/'capture.py'),'capture incomplete/current driver changed')
 z=subprocess.run(['git','show',lineage['commit']+':'+lineage['member']],capture_output=True,timeout=15);need(z.returncode==0 and not z.stderr and bool(z.stdout) and z.stdout==(P/'retained-prefix-01.json').read_bytes() and sha(P/'retained-prefix-01.json')==lineage['sha256'],'retained prefix Git identity moved')
 # Queue proof is producer-valid and immutable, not independent acceptance.
 F=P/'retained';mf=F/'queue-manifest.json';need(sha(mf)=='59f6be899f03c3b65ba88f73fff8bb82e15e25565eacabb860ad72289a063c24','queue source parent moved')
 members={q['path']:q for q in json.loads(mf.read_text())['members']};need(sha(F/'queue-source-02.json')==members['source-02.json']['sha256'],'retained queue member moved');q=json.loads((F/'queue-source-02.json').read_text())
 PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference image moved');pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,sz,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original bytes')
 need(d.get('complete') is True and e.get('complete') is True and e['bytes']==440 and len(e['records'])==3 and bytes.fromhex(d['physical_body_hex'])==read(0x306bd0,440) and d['physical_body_sha256']==e['body_sha256']==hashlib.sha256(read(0x306bd0,440)).hexdigest(),'physical classifier identity differs')
 need(d['mapping']==list(read(0x306d08,128)) and d['jump_dwords']==list(struct.unpack('<7I',read(0x306cec,28))),'embedded table differs')
 ix={};annotations=[]
 for y in [x,r,q]:
  need(y['exe_sha256']==PIN,'source identity differs');annotations.append(V.validate(y))
  for span in y['ranges']:
   a,b=int(span['start'],16),int(span['end_exclusive'],16);need(bytes.fromhex(''.join(i['bytes'] for i in span['instructions']))==read(a,b-a),'not original instructions')
   if y is r and a!=0x306bd0:continue
   for i in span['instructions']:
    pc=int(i['pc'],16);need(pc not in ix or ix[pc]==i,'overlapping source disagreement');ix[pc]=i
 need(all(a in ix for a in [0x306bd0,0x306c5b,0x306ceb,0x3068d4]),'missing producer/comparison range')
 facts=derive(ix,d,G)
 with out.open('x') as f:json.dump(dict(producer_complete=True,method='A STATIC_ONLY conditional kind/full32-to-low16 coherence',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path=n,sha256=sha(P/n)) for n in ['source-01.json','retained-prefix-01.json','retained/queue-source-02.json']],retained_queue=dict(manifest_sha256=sha(mf),member_sha256=sha(F/'queue-source-02.json'),limits='Producer-valid source parent, independent acceptance pending; original bytes reverified, not rerun/credited.'),annotation_prerequisites=annotations,facts=facts,limits=facts['limits'],cleanup='Offline only, all finite children terminated; no game/native/emulator/PC/save/config/reference/peer intervention.'),f,indent=2)
 print('PROVED conditional kind4 q208..225 versus low16 queue; natural coherence OPEN')
if __name__=='__main__':main()
