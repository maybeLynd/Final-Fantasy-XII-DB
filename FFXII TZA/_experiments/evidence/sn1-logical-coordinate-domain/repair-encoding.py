import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;p=W/'check.py';old=p.read_bytes();assert not (W/'result.json').exists();q=W/'retained/check-before-terminal5c-fix.py';assert not q.exists();q.write_bytes(old)
s=old.decode();a="data=s[a:s.index(b'\\0',a,end)];cont=data.endswith(b'\\\\');assert not cont or data.decode('cp932').endswith('\\\\'),'Terminal5C encoding ambiguity'"
z="data=s[a:s.index(b'\\0',a,end)];decoded=data.decode('cp932');raw_end=data.endswith(b'\\\\');cont=raw_end if '--fault-raw-byte-fold' in sys.argv else decoded.endswith('\\\\')\n   assert not (raw_end and not decoded.endswith('\\\\')) or not cont, 'CP932 trailing5C character must not be classified as ASCII continuation'"
assert s.count(a)==1;s=s.replace(a,z)
a="assert [{k:v for k,v in x.items() if k!='continuations'} for x in source_blocks]==[{k:x[k] for k in ['module','block','physical','logical']} for x in prep['source_blocks']]"
z="assert [(x['module'],x['block'],x['physical'],x['logical']) for x in source_blocks]==[(x['module'],x['block'],x['physical'],x['logical']+len(x['non_ascii_terminal5c'])) for x in prep['source_blocks']], 'Decoded logical domain corrects raw terminal-byte candidate'"
assert s.count(a)==1;s=s.replace(a,z).replace("==3 and len([c for c in controls", "==2 and len([c for c in controls")
a="interpretation='All actual non-pad";assert s.count(a)==1;s=s.replace(a,"interpretation='Decoded CP932 ASCII-backslash folding, not raw terminal5C folding: mapctrl block0 has two non-ASCII trailing5C characters and zero actual terminal ASCII backslashes. All actual non-pad")
a="Three encoded logicalL+1 controls";assert s.count(a)==1;s=s.replace(a,"Two encoded logicalL+1 controls")
a="All raw terminal5C continuation candidates in these inputs decode to ASCII backslash; lexical interpretation/comments/quotes/general encoding behavior not proved."
z="Raw terminal5C is not sufficient: two mapctrl source lines end in CP932 multibyte characters; corrected decoded-ASCII candidate used. evctrl544 and ctrl19 terminal ASCII backslashes remain; general lexical/compiler/comments/quotes behavior not proved."
assert s.count(a)==1;s=s.replace(a,z).replace('four original positive and three encoded boundary controls','four original positive and two encoded boundary controls')
assert p.read_bytes()==old;p.write_bytes(s.encode())
f=json.loads((W/'failure.json').read_text());f['second_failure']=dict(status='INVALID_RAW_TERMINAL5C_CONTINUATION_DOMAIN_BEFORE_RESULT',cause='Global-phase fix then reaches actual original mapctrl source whose CP932 terminal character contains byte5C; assertion identifies non-ASCII alias. First preparation classified raw terminal5C as continuation, so its map logical2766 is not accepted.',repair='Decode CP932 and classify terminal ASCII backslash, retaining raw byte/decoded distinction. Actual source negative and --fault-raw-byte-fold regression; mapped-domain counts adjusted against raw preparation alias counts, not overwritten.',affected='64 raw-byte candidate preparation/source classification and FABLE unpublished logical_lines.py raw-byte cont() corpus count/procedure; original63 ev544 all ASCII/call controls unaffected',old_checker_sha256=hashlib.sha256(old).hexdigest(),corrected_checker_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
(W/'failure.json').write_text(json.dumps(f,indent=2)+'\n')
