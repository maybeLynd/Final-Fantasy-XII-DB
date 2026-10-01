"""A source-only actual producer control, no original-code/game execution."""
import ast,datetime,hashlib,json,sys
from pathlib import Path
import capstone
from adapter import make,window,observe
sha=lambda b:hashlib.sha256(b).hexdigest();W=Path(__file__).resolve().parent
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d
t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-PRESET-REFERENCE-BOUNDARY-BINDING');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'raw.json').exists()
p=Path('Database/FFXII TZA/_index/candidates/yebis-preset-selector/yebis_preset.py');source=p.read_bytes();s=source.decode()
assert 'MD.disasm(d[off(f):off(f) + (va - f) + 16], f)' in s and s.count('and boundary(va):')==4
R=W/'retained';R.mkdir(exist_ok=False)
for n,b in [('producer-original.py',source),('producer-readme.md',(p.parent/'README.md').read_bytes()),('producer-output.txt',(p.parent/'yebis_preset.out').read_bytes()),('driver-before-run.py',Path(__file__).read_bytes()),('adapter-before-run.py',(W/'adapter.py').read_bytes())]:(R/n).write_bytes(b)
old,old_selected=make(s,repaired=False);fixed,fixed_selected=make(s)
(R/'selected-original.py').write_text(old_selected);(R/'selected-corrected.py').write_text(fixed_selected)
image=old['d'];assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and fixed['d']==image
entry=0x712090;candidate=0x712095;target=0x6DAA30;n=48
original_pd=list(old['PD']);root=old['fstart'](entry);bounds=[(b+0x120000,e+0x120000) for b,e in original_pd if b+0x120000<=entry<e+0x120000];assert root==entry and len(bounds)==1 and bounds[0][1]>=entry+n
o=window(old,entry,n);assert window(fixed,entry,n)==o
orig=image[o:o+n];(R/'original-window.bin').write_bytes(orig)
ii=list(old['MD'].disasm(orig,entry));assert candidate in [i.address for i in ii] and bytes(ii[0].bytes).hex()=='48895c2408'
import struct
positive=bytearray(image);positive[o:o+5]=b'\xe8'+struct.pack('<i',target-(entry+5))
negative=bytearray(image);negative[o:o+10]=b'\x48\xb8'+b'\x90'*3+b'\xe8'+struct.pack('<i',target-(candidate+5))
assert len(positive)==len(negative)==len(image)
cases=[]
for name,img,pc in [('original',image,candidate),('real-call',bytes(positive),entry),('immediate-payload',bytes(negative),candidate)]:
    (R/(name+'.bin')).write_bytes(img[o:o+n])
    a=observe(old,img,entry,pc,target,n);b=observe(fixed,img,entry,pc,target,n)
    cases.append(dict(name=name,image_sha256=sha(img),window_sha256=sha(img[o:o+n]),original_path=a,corrected_default_path=b))
    (W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
raw=dict(method='A only source/image parsing; unchanged actual producer definitions selected by AST, bounded48B section/text scan projection; no original/native/emulator/game instruction execution',question='Does refs(img) bind its boundary gate to that image?',reference=dict(producer_path=p.as_posix(),producer_sha256=sha(source),exe_sha256=sha(image),entry=f'{entry:08X}',candidate=f'{candidate:08X}',target=f'{target:08X}',bytes=n,file_offset=o,root=f'{root:08X}',containing_pdata=[[f'{a:08X}',f'{b:08X}'] for a,b in bounds],selected_original_sha256=sha(old_selected.encode()),selected_corrected_sha256=sha(fixed_selected.encode())),tools=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,dll_path=str(capstone._cs._name),dll_sha256=sha(Path(capstone._cs._name).read_bytes())),cases=cases,cleanup=dict(original_reference_unchanged=sha(Path(old['EXE']).read_bytes())==sha(image),peer_producer_unchanged=p.read_bytes()==source,pc_off=True,private_images='Only in-memory data bytearrays, not executable copies, no deploy/launch/other process/save/config writes'))
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
assert raw['cleanup']['original_reference_unchanged'] and raw['cleanup']['peer_producer_unchanged']
assert cases[0]['original_path']['refs']==cases[0]['corrected_default_path']['refs']==[]
assert cases[1]['original_path']['refs']==cases[1]['corrected_default_path']['refs']==[['rel32','00712090']]
assert cases[1]['corrected_default_path']['decode'][0]['mnemonic']=='call' and cases[1]['corrected_default_path']['decode'][0]['operands']=='0x6daa30'
assert cases[2]['original_path']['refs']==[['rel32','00712095']] and cases[2]['corrected_default_path']['refs']==[]
assert cases[2]['original_path']['boundary_with_image'] and not cases[2]['corrected_default_path']['boundary_with_image']
assert cases[2]['corrected_default_path']['decode'][0]['size']==10 and cases[2]['corrected_default_path']['decode'][0]['mnemonic']=='movabs' and '00712095' not in cases[2]['corrected_default_path']['source_boundaries']
print('Confirmed actual old path accepts E8 inside MOV immediate; corrected default rejects and retains real-CALL positive control',flush=True)
