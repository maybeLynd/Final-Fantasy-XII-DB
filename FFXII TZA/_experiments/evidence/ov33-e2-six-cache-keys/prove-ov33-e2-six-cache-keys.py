"""Six retained OV33 E2 paths against the entire shipping name-key domain.

Fresh result [disposable source directory]. Static finite-data proof. Reuse
external normalization source/controls without executing the external campaign.
"""
import ast,hashlib,importlib.util,json,pathlib,struct,sys,zlib
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
 s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('e2_cfg','prove-title-queue-consumption.py');S=module('e2_annotations','validate-title-source-annotations.py')
INPUT_SHA='07896eecfbc18ca086eeeed3df7a7a2e9e32622f4fe66455929b7aaf41086c7b'
FUNCTIONS={'norm':'7e16216edd050f155e9356c1c01b982bd485de783bd50e333d9f88a49264fd90','djb2':'bf5fd2a35938b22829ad17616a7ceb5039128d5ab95a8290656b8c4cad5f24ee'}
def main():
 if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source directory]')
 out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
 if out.exists():raise ValueError('immutable result exists')
 pins=[];raw,ix=P.load(src,'filecache-hash-loop-source-01.json',pins);annotations=S.validate(raw)
 if len(raw['ranges'])!=1 or (raw['ranges'][0]['start'],raw['ranges'][0]['end_exclusive'],raw['ranges'][0]['sha256'])!=('0x674a00','0x674a28','1b604e013c04950e3c0b1c29b3d08e6776b4cf316eabec0bccfc1cd036672397'):raise ValueError('original complete hash-loop identity changed')
 cfg=P.closed(ix,0x674a00,0x674a28)
 if cfg['calls'] or cfg['returns']!=['0x674a27']:raise ValueError('hash-loop call/return boundary changed')
 for pc,m,a in [(0x674a00,'movzx','edx, byte ptr [rcx]'),(0x674a03,'mov','eax, 0x1505'),(0x674a08,'test','dl, dl'),(0x674a0a,'je','0x674a23'),(0x674a10,'imul','eax, eax, 0x21'),(0x674a13,'lea','rcx, [rcx + 1]'),(0x674a17,'movsx','edx, dl'),(0x674a1a,'add','eax, edx'),(0x674a1c,'movzx','edx, byte ptr [rcx]'),(0x674a1f,'test','dl, dl'),(0x674a21,'jne','0x674a10'),(0x674a23,'btr','eax, 0x1f')]:P.need(ix,pc,m,a)
 d=src/'ov33-e2-key-inputs-01';ip=d/'inputs.json';receipt=json.loads(ip.read_text())
 if receipt.get('status')!='RETAINED_NONEMPTY_INDEX_AND_SELECTED_PEER_INPUTS' or receipt.get('archive',{}).get('file_count')!=89414:raise ValueError('required index input missing/zero/incomplete')
 if P.sha(ip)!=INPUT_SHA:raise ValueError('retained index/selected-input receipt identity changed')
 for p in receipt['peer_inputs']:
  if P.sha(d/p['path'])!=p['sha256']:raise ValueError('required external input changed')
 compressed=d/receipt['archive']['compressed_path']
 if P.sha(compressed)!=receipt['archive']['compressed_sha256']:raise ValueError('retained index-prefix identity changed')
 blob=zlib.decompress(compressed.read_bytes())
 if len(blob)!=receipt['archive']['index_prefix_end'] or hashlib.sha256(blob).hexdigest()!=receipt['archive']['index_prefix_sha256']:raise ValueError('retained raw index-prefix identity changed')
 magic,headerlen,count=struct.unpack_from('<4sIQ',blob)
 entries=16+16*count;strings_at=16+48*count
 if magic!=b'SRYK' or count!=89414 or strings_at+4>len(blob):raise ValueError('invalid nonempty raw archive header')
 slen=struct.unpack_from('<I',blob,strings_at)[0]
 if slen<4 or strings_at+slen!=len(blob) or len(blob)>headerlen:raise ValueError('invalid original raw name bounds')
 strings=blob[strings_at+4:];names=[]
 for k in range(count):
  noff=struct.unpack_from('<Q',blob,entries+k*32+24)[0]
  if noff>=len(strings):raise ValueError('raw name outside original table')
  stop=strings.find(b'\0',noff)
  if stop<0:raise ValueError('raw name unterminated')
  name=strings[noff:stop].decode('ascii')
  if not name:raise ValueError('empty raw archive name')
  names.append(name)
 if len(set(names))!=count:raise ValueError('duplicate raw archive name hidden')
 # Only the two pinned pure functions are reused; none of the peer campaign,
 # native/emulator code, outputs or assertion counters is run as ASTRA work.
 source=(d/'contract-b14-checks.py').read_text();tree=ast.parse(source);nodes=[]
 for n in tree.body:
  if isinstance(n,ast.FunctionDef) and n.name in FUNCTIONS:
   text=ast.get_source_segment(source,n)
   if hashlib.sha256(text.encode()).hexdigest()!=FUNCTIONS[n.name]:raise ValueError('normalization/hash function preimage changed')
   nodes.append(n)
 if {n.name for n in nodes}!=set(FUNCTIONS):raise ValueError('missing normalization/hash function')
 env={'__builtins__':{'len':len}};exec(compile(ast.Module(body=nodes,type_ignores=[]),'retained-pure-key-functions','exec'),env)
 norm,key=env['norm'],env['djb2'];domain={}
 for name in names:
  normalized=norm(name)
  if not normalized.isascii():raise ValueError('normalization left declared ASCII domain')
  domain.setdefault(key(normalized),[]).append(name)
 rows=receipt['selected_rows'];expected={('US',129),('US',130),('US',131),('UK',131),('UK',132),('CN',127)}
 if len(rows)!=12 or {(r['language'],r['edx_mode'],r['kind'],r['index']) for r in rows}!={(l,e,1,i) for l,i in expected for e in (0,1)}:raise ValueError('incomplete selected source rows')
 output=[]
 for lang,num in sorted(expected):
  selected=[r for r in rows if r['language']==lang and r['index']==num]
  if len({r['path'] for r in selected})!=1:raise ValueError('selected mode source disagreement')
  path=selected[0]['path'];normalized=norm(path);k=key(normalized)
  output.append(dict(language=lang,kind=1,index=num,edx_modes=[0,1],path=path,normalized_cache_path=normalized,key_hex=hex(k),colliding_archive_names=domain.get(k,[])))
 # Detection control uses the same complete domain and collision lookup.
 # Its query is explicitly not one of the six original missing-file paths.
 known='ps2data/cdi/in/system.cnf';known_key=key(norm(known));detected=domain.get(known_key,[])
 if not detected or known not in {n.lower() for n in detected}:raise ValueError('positive collision detection control failed')
 absent_control='ASTRA_E2_NONEXISTENT_CONTROL_0930'
 if norm(absent_control) in {norm(n) for n in names}:raise ValueError('known absence name control failed')
 collisions=[q for q in output if q['colliding_archive_names']]
 result=dict(status='PRODUCER_CHECKED_SIX_CACHE_KEY_INTERSECTION_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,
  question='Can archive-name key collisions supply cache membership for any of the six retained missing FST-sized kind1 paths?',
  verdict='COLLISIONS_FOUND' if collisions else 'NO_COLLISION_IN_COMPLETE_RETAINED_ARCHIVE_NAME_DOMAIN',
  source_pins=pins,annotation_prerequisite=annotations,normal_hash_cfg=cfg,
  required_input_pins=[dict(path='ov33-e2-key-inputs-01/inputs.json',sha256=P.sha(ip)),dict(path='ov33-e2-key-inputs-01/'+compressed.name,sha256=P.sha(compressed))]+[dict(path='ov33-e2-key-inputs-01/'+p['path'],sha256=p['sha256']) for p in receipt['peer_inputs']],
  archive=receipt['archive'],archive_name_count=count,distinct_cache_keys=len(domain),selected_paths=output,
  detection_positive=dict(query=known,key_hex=hex(known_key),matching_archive_names=detected,limits='Actual reducer detection control on retained data, not live cache contents'),
  normalization_source_functions=FUNCTIONS,hash_proof='Complete674A00 reads bytes untilNUL: low32 h starts1505, h=low32(33*h+sign8(byte)); BTR31 once after loop. Python recurrence matches these instructions, not an execution of them.',
  interpretation=('At least one selected missing-file key can come from a present archive name; preserve exact matches and require flag/entry/request lifetime proof.' if collisions else 'Under unchanged ASCII/C-locale normalization and cache populated only from archive-name keys, these six paths cannot pass the cache membership gate, regardless of map-jump timing. This removes that scoped E2 discriminator without live gameplay.'),
  assumptions=['ASCII/C-locale normalization as retained b14 norm/CRT boundary; original unmodified name-key algorithm','Cache population from these shipping archive-name keys only, no alternate inserts or injected/modded names; complete writer/indirect binding proof is separate','Retained FABLE six language/kind/id/path source census remains a pending/externally reviewed dependency, not a new ASTRA census'],
  limitations=['Not complete E2/OV33 closure: kindFF rewritten/uninitialized paths and all cache producer/binding paths remain separately open','No actual map-jump flag/cache initialization, scheduler, locale changes, lifetime/eviction or normal request observation','Archive identity is exact retained index/name prefix, not full VBF/payload integrity or successful file reads','External b14 three-string Unicorn controls and317 assertions are corroboration, not ASTRA executions or independent acceptance of this result'],
  affected_claims=['FABLE OV33 E2 six FST-sized absent-path cache-key possibility','OPUS resource issuance error/no-status contract scoped key-domain precondition'],
  next_discriminator='If no collision: establish accepted archive-only cache key provenance/all alternate insert closure and separately resolve rawkindFF/00377DC0 paths; no need to observe these six key absences in FF12.',
  checker_sha256=P.sha(pathlib.Path(__file__)),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
  cleanup='Read-only archive-name prefix/EXE/retained peer inputs; finite scripts, no PC/game/input/instrument/save/config/reference/peer-process writes or kills')
 out.open('x',encoding='utf-8').write(json.dumps(result,indent=2)+'\n');print(result['verdict'],len(output),'selected paths;',count,'archive names;',len(collisions),'candidate collisions; positive detector valid')
if __name__=='__main__':main()
