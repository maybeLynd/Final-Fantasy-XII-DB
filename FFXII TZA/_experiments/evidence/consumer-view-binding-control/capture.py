"""A actual consumer input-pair control; private changed binary is data only, never executed."""
import datetime,hashlib,importlib.util,json,os,struct,subprocess,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,detail=team.board_status(team.BOARD);assert ok,detail
t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-CONSUMER-VIEW-BINDING-CONTROL')
assert t['status']=='ACTIVE' and t['agent']=='ASTRA' and not (W/'result.json').exists()
producer=Path('Database/FFXII TZA/_index/candidates/fable-returns-0928e/three_check.py');source=producer.read_bytes()
assert b'Y1P_CACHE' in source and b'FFXII_EXE' in source
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('reader',rp);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image()
assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
R=W/'retained';R.mkdir(exist_ok=False);D=W/'disposable';D.mkdir(exist_ok=False)
(R/'producer.py').write_bytes(source);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes());(R/'shipping-reader.py').write_bytes(rp.read_bytes())
(R/'consumer-readme.md').write_bytes((producer.parent/'README.md').read_bytes())
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
refs=[(0x229E70,'rate-normalizer-domain/retained/source.bin',37),(0x20E600,'image-reference-roundtrip-domain/retained/decode.bin',10),(0x20E620,'image-reference-roundtrip-domain/retained/encode.bin',9),(0x339630,'approach-angle-divisor-domain/retained/source.bin',1061)]
bodies=[];original_lines=[];changed_lines=[]
for entry,name,n in refs:
    p=Path('Database/FFXII TZA/_experiments/evidence')/name;raw=p.read_bytes()
    assert len(raw)==n and raw==rd.img_rd(image,ss,entry,n)
    ii=list(cs.disasm(raw,entry));assert sum(i.size for i in ii)==n
    (R/(f'{entry:08X}.bin')).write_bytes(raw)
    bodies.append(dict(entry=f'{entry:08X}',bytes=n,path=p.as_posix(),sha256=sha(raw),scope='Dependency-verified retained source matched certified original image, not neworiginalcode execution'))
    for i in ii:
        op=(i.mnemonic+' '+i.op_str).rstrip()
        original_lines.append(f'{i.address:08X} {entry:08X} {op}')
        if i.address==0x229E7E:
            assert i.bytes.hex()=='7211' and op=='jb 0x229e91'
            changed_lines.append(f'{i.address:08X} {entry:08X} jbe 0x229e91')
        else:changed_lines.append(original_lines[-1])
view=('\n'.join(original_lines)+'\n').encode();mutview=('\n'.join(changed_lines)+'\n').encode()
assert sum(a!=b for a,b in zip(original_lines,changed_lines))==1
(R/'original-view.txt').write_bytes(view);(R/'changed-view.txt').write_bytes(mutview)
pc=0x229E7E;rv=pc-0x120000;sva,vs,ra,rs=next(s for s in ss if s[0]<=rv and rv+1<=s[0]+s[3]);off=ra+rv-sva
mut=bytearray(image);assert mut[off]==0x72;mut[off]=0x76
mutpath=(D/'changed-image-data.bin').resolve();assert mutpath.parent==D.resolve() and mutpath.is_relative_to(W.resolve());mutpath.write_bytes(mut)
assert sha(mutpath.read_bytes())==sha(mut) and len(mut)==len(image)
mutation=dict(pc=hex(pc),file_offset=hex(off),original_hex='72',changed_hex='76',instruction='JB->JBE samebranchdestination',original_body_sha256=bodies[0]['sha256'],changed_body_sha256=sha(rd.img_rd(mut,ss,0x229E70,37)),changed_image_sha256=sha(mut),changed_image_bytes=len(mut),changed_private_path=str(mutpath),limits='One-byte private data copy only; no machine instruction execution/deployment or original reference changes')
(W/'mutation.json').write_text(json.dumps(mutation,indent=2)+'\n')
receipts=[]
def tags(out):
    pairs=[(p[1],p[0]) for l in out.splitlines() if len(p:=l.split())>=3 and p[0] in ('PASS','FAIL')]
    assert len(pairs)==4 and {a for a,b in pairs}=={'R1','I1','A1','C'}, 'Incomplete/duplicate/zero-case output'
    return dict(pairs)
original_exe=Path('Database/Tools/work/exe/FFXII_TZA.exe').resolve()
try:
    for name,cache,exe in [('original-pair',R/'original-view.txt',original_exe),('stale-view-changed-image',R/'original-view.txt',mutpath),('changed-view-changed-image',R/'changed-view.txt',mutpath)]:
        env=os.environ.copy();env['Y1P_CACHE']=str(cache.resolve());env['FFXII_EXE']=str(exe)
        c=subprocess.run([sys.executable,str(R/'producer.py')],env=env,capture_output=True,text=True,timeout=30)
        out=c.stdout.encode();err=c.stderr.encode();(R/(name+'.stdout')).write_bytes(out);(R/(name+'.stderr')).write_bytes(err)
        receipts.append(dict(name=name,returncode=c.returncode,stdout_sha256=sha(out),stderr_sha256=sha(err),view_sha256=sha(cache.read_bytes()),exe_sha256=sha(exe.read_bytes()),method='Actual cloned hostproducer, only its documented inputenvironment configured. NoFF12code/native/FP/live execution'))
        (W/'partial-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
        receipts[-1]['tags']=tags(c.stdout)
        (W/'partial-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
    assert [x['returncode'] for x in receipts]==[0,0,1]
    assert receipts[0]['tags']==receipts[1]['tags']==dict(R1='PASS',I1='PASS',A1='PASS',C='PASS')
    assert receipts[2]['tags']==dict(R1='FAIL',I1='PASS',A1='PASS',C='PASS')
    assert producer.read_bytes()==source and sha(original_exe.read_bytes())==sha(image)
finally:
    assert mutpath.parent==D.resolve() and mutpath.is_relative_to(W.resolve())
    if mutpath.exists():
        assert sha(mutpath.read_bytes())==mutation['changed_image_sha256']
        mutpath.unlink() # ownsinglefile, protectedoriginal andpeer pathsnever targeted
    (W/'cleanup.json').write_text(json.dumps(dict(changed_private_copy_removed=not mutpath.exists(),original_reference_path=str(original_exe),original_readback_sha256=sha(original_exe.read_bytes()),limits='Onlyownprivatechangeddatafile removed afterverifiedpath/hash; source/views/rawretained, no peer/process/control/saves'),indent=2)+'\n')
dll=Path(capstone._cs._name)
result=dict(question='Actual consumer rejects source/view mismatch or accepts stale pair?',method='A verifiedfourbodyview and threeexistinghostproducerinvocations plus onebyteprivatebinarydata control; zero original/native/emulator/live executions',
    reference=dict(exe_sha256=sha(image),producer_path=producer.as_posix(),producer_sha256=sha(source),reader_sha256=sha(rp.read_bytes()),original_view_sha256=sha(view),changed_view_sha256=sha(mutview),body_sources=bodies),
    tools=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_dll=dict(path=str(dll),sha256=sha(dll.read_bytes()))),driver_sha256=sha(Path(__file__).read_bytes()),mutation=mutation,receipts=receipts,
    interpretation='ActualexistingFABLEproducer passes changedJB->JBEimage when itsview remainsoriginal, but failsR1 with changedview. Viewside branch detector works; executable-to-view dependency/reference identity notchecked bythisconfigurableinvocation. A greenrundoesnotattest actualEXE branch. Historical/defaultcachepairwrongnessnotproven; originalASTRA41-43source andSPECacceptance unaffected.',
    required_change='FABLE bindactualEXE/cachedview identity/sourcecoverage or consumeverifiedimmutableoriginalsource; guardmustrejectstale/wrongpair, actualinvocationregressionnothelperhashonly. Preserve existingvalidfinite/sourcefields and COMISScompletion/DAZ/nativeFP/hostmodel limits in R1producer/consumer prose; no unqualifiedbitexact. Need namedaffectedconsumerclaims only, no broadclassification/export/reporter.',
    limits='Onlythreeexplicitconfigurableinvocations/fourbodyprojection, nothistoricaldefaultcacheprovenance or allrepositoryconsumers. Privatebinaryreadasdata neverexecuted; JB/JBE source distinction fromISA notnativeeffect. NooriginalFPcases/newsemantictestcount/nativecaller/init/lifetime/presentation claims. Producer/integritychecksnotindependentacceptance.',
    cleanup=json.loads((W/'cleanup.json').read_text()))
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('Confirmed originalpairPASS/stalepairchangedimagePASS/matchingchangedviewR1FAIL; missingactualsource-view binding, privatechangeddata removed/no game execution',flush=True)
