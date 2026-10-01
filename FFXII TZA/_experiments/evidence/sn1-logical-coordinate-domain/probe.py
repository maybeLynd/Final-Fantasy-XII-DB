"""Preparation only: controls and reducer not yet accepted."""
import collections,hashlib,json,struct,subprocess,sys
from pathlib import Path
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-q0-source-coordinate-domain');sha=lambda b:hashlib.sha256(b).hexdigest()
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SN1-LOGICAL-COORDINATE-DOMAIN');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
if (W/'preparation.json').exists():
 subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
raw=json.loads((P/'raw.json').read_text());g={'struct':struct};pb=(P/'retained/selected-sbn-functions.py').read_bytes();assert sha(pb)==raw['reference']['selected_parser_sha256'];exec(compile(pb,'retained unchanged source parser','exec'),g)
rows=[];new_missing=[];known_missing=[];totals=collections.Counter()
for m in raw['modules']:
 s=(P/'retained'/(m['name']+'.sbn')).read_bytes();b=(P/'retained'/(m['name']+'.dbg')).read_bytes()
 for ext,data in [('sbn',s),('dbg',b)]:assert sha(data)==next(i['sha256'] for i in raw['reference']['files'] if (i['module'],i['extension'])==(m['name'],ext))
 counts=[]
 for bi,(o,end) in enumerate(g['sbn_blocks'](s)):
  L,bases,starts,p=g['sbn_group_read'](s,o);texts=[s[a:s.index(b'\0',a,end)] for a in starts];raw_terminal=[j for j,x in enumerate(texts) if x.endswith(b'\\')];continuations=[j for j,x in enumerate(texts) if x.decode('cp932').endswith('\\')];logical=L-len(continuations)
  ambiguous=[j for j in raw_terminal if not texts[j].decode('cp932').endswith('\\')]
  counts.append(logical);rows.append(dict(module=m['name'],block=bi,physical=L,logical=logical,raw_terminal_backslash_count=len(raw_terminal),decoded_ascii_continuations=len(continuations),non_ascii_terminal5c=ambiguous,open_terminal_continuation=bool(texts[-1].decode('cp932').endswith('\\'))))
 for sc in m['scopes']:
  for x in sc['records']:
   data=b[x['file_offset']:x['file_offset']+4];assert data.hex()==x['record_hex'];line,block,flag=struct.unpack('<HBB',data)
   if data==b'\0'*4:totals['pad_original_all_zero']+=1;continue
   if block>=len(counts) or line<1 or line>counts[block]:
    row=dict(module=m['name'],scope=sc['index'],index=x['index'],offset=x['file_offset'],record_hex=data.hex(),line=line,block=block,flag=flag,logical_count=counts[block] if block<len(counts) else None,old_physical_category=x['category'])
    (known_missing if x['category']=='outside-both-index-conventions' else new_missing).append(row)
   else:totals['conditional_logical_in_range']+=1
out=dict(counter_mode='DECODED_ASCII_CONTINUATION',status='PREPARATION_ONLY_NOT_VALIDATED_NO_ACCEPTED_NEGATIVE',method='A original immutable60 inputs/parser and conditional63 decoded ASCII-backslash fold, no compiler/VM/native/game',parent=P.as_posix(),parent_manifest_sha256=sha((P/'manifest.json').read_bytes()),parent_raw_sha256=sha((P/'raw.json').read_bytes()),source_blocks=rows,counts=dict(totals),new_logical_missing=new_missing,known_physical_missing=known_missing,next='Build exact positive/negative actual record controls at logicalL/logicalL+1 with physicalL larger; verify alias spans/terminal continuation/encoding limits and actual default before treating absence as evidence. No repeated four call tests, no peer source lookup edit.',limits='Conditional domain calculation only, not universal compiler rule or complete source attribution. Preparation has no detection control yet and cannot pass/close the claim. Actual original input hashes checked; PC OFF/S19 parked/full L1+L2 NOT_MET.')
(W/'preparation.json').write_text(json.dumps(out,indent=2)+'\n')
print('PREP64',[(x['module'],x['block'],x['physical'],x['logical']) for x in rows],'new-logical-missing',len(new_missing),'known',len(known_missing),'CONTROLS_PENDING',flush=True)
