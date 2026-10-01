"""Instruction-bound ASCII stage lemma; no samples substitute for the induction."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
ROOT=next(p for p in W.parents if (p/'Database/FFXII TZA/_experiments/evidence').is_dir())
E=ROOT/'Database/FFXII TZA/_experiments/evidence';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def parent(folder,pin,name):
 if sha(folder/'manifest.json')!=pin:raise ValueError('required external manifest changed/missing')
 m=json.loads((folder/'manifest.json').read_text());x=next(x for x in m['members'] if x['path']==name)
 if sha(folder/name)!=x['sha256']:raise ValueError('required external member changed/missing')
 return json.loads((folder/name).read_text()),dict(folder=str(folder.relative_to(ROOT)),manifest_sha256=pin,path=name,sha256=x['sha256'])
def main(src,out):
 if out.exists():raise ValueError('immutable result exists')
 st=json.loads((src/'filecache-format-boundary-capture-01.status.json').read_text())
 if st.get('exit')!=0 or st.get('terminal') is not True or st.get('driver_sha256')!=sha(src/'capture-filecache-format-boundary.py'):raise ValueError('format capture failed/incomplete/stale')
 if not(src/'filecache-format-boundary-capture-01.stdout').read_bytes().strip() or (src/'filecache-format-boundary-capture-01.stderr').read_bytes():raise ValueError('format capture missing/error output')
 f=json.loads((src/'filecache-format-boundary-source-01.json').read_text())
 if f['invocation_driver_sha256']!=sha(src/'capture-filecache-format-boundary.py'):raise ValueError('format actual invocation changed')
 vals=[f];deps=[]
 for folder,pin,name in [(E/'filecache-key-preprocessing','f7b5ffccc16ae832d1a7279e1f616c2687e97868b4d98d4378db48ba17e15db6','filecache-key-boundaries-source-02.json'),
                        (E/'filecache-fill-and-failure','3ec198b7e33d6bd3aaa18ef8574a33eead108f51a6611ccdfc42fe5e2edfbd02','filecache-fill-key-resolver-source-01.json')]:
  v,d=parent(folder,pin,name);vals.append(v);deps.append(d)
 V=load('composition_roles',src/'validate-title-source-annotations.py')
 for v in vals:
  if v['exe_sha256']!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong shipping image')
  V.validate(v)
 qs={int(q['start'],16):q for v in vals for q in v['ranges']}
 pins=[(0x17d2e0,0x17d33b,'8cee24942ffb9e71495d571868938e0540a0be6bc5fad7a4fea582889578a6e6'),
       (0x16d670,0x16d678,'3cfbe7e81225a3f1f1232206f4754a6127e1bcafc9c9f726d476192e97c09ca5'),
       (0x20c440,0x20c551,'f9bd563df026e5a30e8a55828668de4925acfcaef7b6617a8b5731c184b34aef'),
       (0x59ee90,0x59f1fc,'b6631ed174665398c271a8ad7cd9bb57310fc5ffe1b3da0a2d59234caaaea036')]
 for lo,hi,pin in pins:
  if (int(qs[lo]['end_exclusive'],16),qs[lo]['sha256'])!=(hi,pin):raise ValueError('required complete original body identity failed')
 ix={int(i['pc'],16):i for q in qs.values() for i in q['instructions']}
 gp=src/'prove_owner_reload_order.py'
 if sha(gp)!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise ValueError('reviewed CFG helper changed')
 G=load('composition_graph',gp);graphs={hex(lo):G.graph(ix,lo,hi) for lo,hi,pin in pins}
 def need(pc,m,a):
  if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise ValueError('original stage operation changed '+hex(pc))
 ops=[(0x59f118,'lea','eax, [rcx - 0x2e]'),(0x59f11b,'cmp','al, 1'),(0x59f11d,'jbe','0x59f124'),(0x59f11f,'cmp','cl, 0x5c'),
  (0x59f130,'lea','rdx, [rip + 0x355301]'),(0x59f137,'add','r8, rdi'),(0x59f13d,'call','0x17d2e0'),
  (0x59f150,'cmp','byte ptr [rax], 0x5c'),(0x59f155,'mov','byte ptr [rax], 0x2f'),
  (0x59f173,'lea','eax, [rdx - 0x41]'),(0x59f176,'cmp','al, 0x19'),(0x59f17a,'add','dl, 0x20'),
  (0x20c4d0,'cmp','byte ptr [rcx], 0x2f'),(0x20c4d5,'mov','byte ptr [rcx], 0x5c'),
  (0x20c4ef,'cmp','byte ptr [rdi + 1], al'),(0x20c4f2,'je','0x20c502'),
  (0x20c4f4,'movsx','ecx, al'),(0x20c4f7,'call','qword ptr [rip + 0x6b6af3]'),
  (0x20c523,'cmp','byte ptr [rbx], 0x20'),(0x20c528,'mov','byte ptr [rbx], 0'),
  (0x17d2f6,'mov','rbx, rdx'),(0x17d2f9,'lea','rsi, [rsp + 0x60]'),(0x17d2fe,'mov','rdi, rcx'),
  (0x17d306,'mov','r9, rbx'),(0x17d309,'mov','qword ptr [rsp + 0x28], rsi'),(0x17d30e,'or','rbx, 0xffffffffffffffff'),
  (0x17d312,'mov','qword ptr [rsp + 0x20], 0'),(0x17d31b,'mov','r8, rbx'),(0x17d31e,'mov','rdx, rdi'),
  (0x17d328,'call','qword ptr [rip + 0x745bda]')]
 for op in ops:need(*op)
 literal=f['exact_literal'];decl=f['static_format_import']
 if literal['va']!='0x8f4438' or literal['bytes']!='257300' or literal['sha256']!=hashlib.sha256(b'%s\0').hexdigest():raise ValueError('exact original short format literal failed')
 if decl['iat_va']!='0x8c2f08' or decl['name']!='__stdio_common_vsprintf' or decl['dll']!='api-ms-win-crt-stdio-l1-1-0.dll':raise ValueError('static formatter import attribution failed')
 if ix[0x17d328]['memory'][0]['rip_target']!='0x8c2f08':raise ValueError('original formatter IAT target failed')
 def alpha(c):return 48<=c<=57 or 65<=c<=90 or 97<=c<=122
 def cpoint(c):return 92 if c==47 else c-32 if 97<=c<=122 else c
 def gpoint(c):return 47 if c==92 else c+32 if 65<=c<=90 else c
 rows=[]
 for c in range(128):
  if alpha(gpoint(c))!=alpha(c) or cpoint(gpoint(c))!=cpoint(c):raise ValueError('finite ASCII point-map invariant failed')
  rows.append(dict(byte=c,g=gpoint(c),c=cpoint(c),c_after_g=cpoint(gpoint(c)),alphanumeric=alpha(c)))
 if any(alpha(c) for c in [46,47,92]):raise ValueError('archive removed prefix not ignored by cache scanner')
 r=dict(method='A STATIC_ONLY, compositional source lemma',producer_complete=True,driver_sha256=sha(Path(__file__)),
  source_pins=[dict(path='filecache-format-boundary-source-01.json',sha256=sha(src/'filecache-format-boundary-source-01.json'))],external_dependencies=deps,
  graphs={k:dict(visited=sorted(g['visited']),calls=g['calls'],returns=g['returns']) for k,g in graphs.items()},instruction_assertions=len(ops),ascii_stage_controls=rows,
  theorem='For valid bounded ASCII p containing an alphanumeric, normal nonaliasing %s copy, C-locale toupper and ordinary returns: C(G(p))=C(p). Thus IF G(p) literally equals archiveName, raw-path insertion key equals that archiveName cache key.',
  proof=['G discards only a leading run of dot/slash/backslash, none alphanumeric; C would ignore them before its first alphanumeric. Removing that run preserves C selected suffix.',
   'Pointwise G preserves ASCII alphanumeric classification, hence first retained alphanumeric in the remaining string is the same position.',
   'For every ASCII byte, Cpoint(Gpoint(byte))=Cpoint(byte). Byte mapping therefore produces identical sequences after the first alphanumeric by induction on suffix length.',
   'Both inputs to the identical cache backslash-collapse/trailing-space stages are equal. Their outputs and deterministic original hash are equal.',
   'G removes bytes or maps one-for-one and %s copies normally; it cannot lengthen p, preserving the declared <256 direct-cache buffer domain.'],
  limits=['A semantic source proof with finite point-map controls, not128 native executions or sampled whole-path proof.',
   'Normal narrow %s copy/CRT options/locale behavior is a named contract premise, not observed loaded CRT. No high-byte, overflow, empty output, malformed-pointer or interference guarantee.',
   'G(p)=archiveName literal equality is stronger than equal MD5 digests. MD5 collisions/different raw sources/all writer/address escapes/mounted namespace identity and natural issuance remain open.',
   '20BE50 gate-specific /hostapp prefix stripping is separate. This lemma concerns raw direct lookup/insertion20C1B0, not every API prefix.',
   'No archive collision census, native or live execution. Prior accepted namespace and previous failure-call lemma remain separate.'],
  affected_claims=['FABLE/OPUS archive-name-only cache-key population premise for literal raw aliases'],native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0)
 out.write_text(json.dumps(r,indent=2)+'\n');print('ORIGINAL STAGE COMPOSITION VERIFIED; ASCII128 point-map controls; inductive whole-path lemma under named premises; no native/live runs')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=W);p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.source,a.out)
