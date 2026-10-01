"""Method A exact callee of the verified 62EB90 wrapper; no queue invocation.

Question: does 199DB0 insert/call the supplied async object, and what does its
fourth argument control? Full original unwind extent and source annotations
first. Transitive callbacks and actual thread/order are not inferred from entry.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'texture-queue-entry-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(d).hexdigest()!=SHA:raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,p+6)[0];opt=struct.unpack_from('<H',d,p+20)[0]
sections=[struct.unpack_from('<IIII',d,p+24+opt+40*k+8) for k in range(ns)]
def read(a,n):
    for vs,va,rs,ro in sections:
        if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError('whole range lacks original backing')
rva,size=struct.unpack_from('<II',d,p+24+112+3*8)
if size%12:raise ValueError('incomplete exception directory')
pd=[tuple(t+0x120000 for t in struct.unpack('<III',read(0x120000+rva+12*k,12))) for k in range(size//12)]
entries=[e for e in pd if e[0]==0x199DB0]
if len(entries)!=1:raise ValueError('ambiguous queue entry extent')
if read(0x62EBB3,5)!=bytes.fromhex('e8f8b1b6ff'):raise ValueError('original wrapper callee identity changed')
spec=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(a,b) for a,b,u in entries];sys.argv=[sys.argv[0],str(out)];C.main()
raw=json.loads(out.read_text())
spec=importlib.util.spec_from_file_location('actual_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
raw.update(wrapper_complete=True,pdata_entries=[list(e) for e in entries],annotation_prerequisite=S.validate(raw),wrapper_call=dict(pc='0x62ebb3',bytes=read(0x62EBB3,5).hex(),target='0x199db0'),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Retained original code only; reduction and independent acceptance pending; no executed queue, runtime scheduler/thread, natural reachability or transitive lifetime proof')
out.write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8')
print('Qualified queue entry source',raw['pdata_entries'])
for q in raw['ranges']:
    for i in q['instructions']:print(i['pc'],i['bytes'],i['mnemonic'],i['args'])
