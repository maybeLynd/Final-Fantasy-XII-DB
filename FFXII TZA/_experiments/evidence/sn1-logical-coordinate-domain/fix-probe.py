from pathlib import Path
W=Path(__file__).resolve().parent;p=W/'probe.py';old=p.read_bytes();q=W/'retained/probe-before-decoded-default.py';assert not q.exists();q.write_bytes(old);s=old.decode()
s=s.replace('import collections,hashlib,json,struct,sys','import collections,hashlib,json,struct,subprocess,sys')
a="assert not (W/'preparation.json').exists()";z="if (W/'preparation.json').exists():\n subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)"
assert s.count(a)==1;s=s.replace(a,z)
a="L,bases,starts,p=g['sbn_group_read'](s,o);texts=[s[a:s.index(b'\\0',a,end)] for a in starts];continuations=[j for j,x in enumerate(texts) if x.endswith(b'\\\\')];logical=L-len(continuations)\n  ambiguous=[j for j in continuations if not texts[j].decode('cp932').endswith('\\\\')]"
z="L,bases,starts,p=g['sbn_group_read'](s,o);texts=[s[a:s.index(b'\\0',a,end)] for a in starts];raw_terminal=[j for j,x in enumerate(texts) if x.endswith(b'\\\\')];continuations=[j for j,x in enumerate(texts) if x.decode('cp932').endswith('\\\\')];logical=L-len(continuations)\n  ambiguous=[j for j in raw_terminal if not texts[j].decode('cp932').endswith('\\\\')]"
assert s.count(a)==1;s=s.replace(a,z).replace('raw_terminal_backslash_count=len(continuations)','raw_terminal_backslash_count=len(raw_terminal),decoded_ascii_continuations=len(continuations)').replace("open_terminal_continuation=bool(texts[-1].endswith(b'\\\\'))","open_terminal_continuation=bool(texts[-1].decode('cp932').endswith('\\\\'))")
a="out=dict(status='PREPARATION_ONLY_NOT_VALIDATED_NO_ACCEPTED_NEGATIVE'";z="out=dict(counter_mode='DECODED_ASCII_CONTINUATION',status='PREPARATION_ONLY_NOT_VALIDATED_NO_ACCEPTED_NEGATIVE'";assert s.count(a)==1;s=s.replace(a,z).replace('conditional63 raw terminal-backslash fold','conditional63 decoded ASCII-backslash fold')
assert p.read_bytes()==old;p.write_bytes(s.encode())
