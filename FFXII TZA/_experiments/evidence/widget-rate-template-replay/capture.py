"""A host-producer replay, FI-only redirection; no original FF12 instructions executed."""
import datetime,hashlib,json,subprocess,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,detail=team.board_status(team.BOARD);assert ok,detail
t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-WIDGET-RATE-TEMPLATE-REPLAY')
assert t['status']=='ACTIVE' and t['agent']=='ASTRA' and not (W/'result.json').exists()
producer=Path('Database/FFXII TZA/_index/candidates/widget-rate-b8/widget_b8_rate.py').resolve()
source=producer.read_bytes();text=source.decode();needle='FI = os.path.join(DB, "_types", "fields.tsv")'
assert text.count(needle)==1 and 'COMPLETED comparison' in text and 'DAZ' in text
fields=Path('Database/FFXII TZA/_types/fields.tsv');fb=fields.read_bytes()
current=next(l for l in fb.decode().splitlines() if l.split('\t')[:2]==['Widget','0x0B8'])
assert 'COMPLETED comparison' in current and 'DAZ' in current
oldpath=Path('Database/FFXII TZA/_experiments/evidence/rate-normalizer-domain/retained/field-preimage.json')
oldbytes=oldpath.read_bytes();old=json.loads(oldbytes)['row'];assert old.split('\t')[5].startswith('1.0f on every widget in the game')
exe=Path('Database/Tools/work/exe/FFXII_TZA.exe');eh=sha(exe.read_bytes())
assert eh=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
R=W/'retained';R.mkdir(exist_ok=False);D=W/'disposable';D.mkdir(exist_ok=False)
(R/'producer.py').write_bytes(source)
(R/'legacy-before.tsv').write_text(old+'\n');(R/'current-control.tsv').write_text(current+'\n')
(R/'legacy-input-identity.json').write_text(json.dumps(dict(path=oldpath.as_posix(),sha256=sha(oldbytes),original_fields_sha256=json.loads(oldbytes)['source_sha256'],row=old),indent=2)+'\n')
(R/'producer-readme.md').write_bytes((producer.parent/'README.md').read_bytes())
(D/'legacy.tsv').write_text(old+'\n');(D/'current.tsv').write_text(current+'\n')
wrapper='''import sys
from pathlib import Path
w=Path(__file__).resolve().parent
spec=__import__('json').loads((w/'invocation.json').read_text())
source=(w/'retained/producer.py').read_text()
needle='FI = os.path.join(DB, "_types", "fields.tsv")'
assert source.count(needle)==1
fixture=Path(sys.argv[1]).resolve()
assert fixture.parent==w/'disposable' and fixture.name in ('legacy.tsv','current.tsv')
transformed=source.replace(needle,'FI = '+repr(str(fixture)))
sys.argv=[spec['original_file'],*sys.argv[2:]]
exec(compile(transformed,spec['original_file'],'exec'),{'__file__':spec['original_file'],'__name__':'__main__'})
'''
(W/'invoke_private.py').write_text(wrapper)
spec=dict(original_file=str(producer),producer_sha256=sha(source),transform='One exact FI assignment substitution to a private fixture absolute path; original __file__ and EXE hash guard/read/source logic unchanged',needle=needle,private_fixture_root=str(D.resolve()),wrapper_sha256=sha((W/'invoke_private.py').read_bytes()))
(W/'invocation.json').write_text(json.dumps(spec,indent=2)+'\n')
receipts=[]
for name,path,args in [('current-positive',D/'current.tsv',[]),('legacy-patch',D/'legacy.tsv',['--patch']),('generated-check',D/'legacy.tsv',[])]:
    before=path.read_bytes()
    c=subprocess.run([sys.executable,str(W/'invoke_private.py'),str(path),*args],capture_output=True,text=True,timeout=30)
    out=c.stdout.encode();err=c.stderr.encode();(R/(name+'.stdout')).write_bytes(out);(R/(name+'.stderr')).write_bytes(err)
    transformed=text.replace(needle,'FI = '+repr(str(path.resolve())))
    receipts.append(dict(name=name,args=args,fixture=path.name,returncode=c.returncode,stdout_sha256=sha(out),stderr_sha256=sha(err),before_sha256=sha(before),after_sha256=sha(path.read_bytes()),transformed_source_sha256=sha(transformed.encode()),limits='Actual hostproducer clonedsource invocation with FI-only redirection. No FF12 machine code/game/native FP execution.'))
generated=(D/'legacy.tsv').read_bytes();(R/'legacy-generated.tsv').write_bytes(generated)
assert [x['returncode'] for x in receipts]==[0,0,1],receipts
def tags(output):
    rows=[l.split() for l in output.splitlines()]
    checks=[(l[1],l[0]) for l in rows if len(l)>=3 and l[0] in ('PASS','FAIL')]
    assert len(checks)==4 and {a for a,b in checks}=={'R1','R2','M','S'}, 'Incomplete/duplicate/zero-case producer output'
    return dict(checks)
# Regress against the exact initial double-spaced outputs before accepting this run.
F=W/'initial-parser-failure/retained'
assert tags((F/'current-positive.stdout').read_text())==dict(R1='PASS',R2='PASS',M='PASS',S='PASS')
assert tags((F/'generated-check.stdout').read_text())==dict(R1='PASS',R2='PASS',M='PASS',S='FAIL')
assert tags((R/'current-positive.stdout').read_text())==dict(R1='PASS',R2='PASS',M='PASS',S='PASS') and 'FAILS 0' in (R/'current-positive.stdout').read_text()
assert 'patched' in (R/'legacy-patch.stdout').read_text() and receipts[1]['before_sha256']!=receipts[1]['after_sha256']
assert tags((R/'generated-check.stdout').read_text())==dict(R1='PASS',R2='PASS',M='PASS',S='FAIL') and 'FAILS 1' in (R/'generated-check.stdout').read_text()
row=generated.decode().rstrip('\r\n').split('\t')
assert row[:2]==['Widget','0x0B8'] and 'BY DEFAULT' in row[5] and 'COMPLETED comparison' not in row[5] and 'DAZ' not in row[5]
assert producer.read_bytes()==source and sha(exe.read_bytes())==eh
postfb=fields.read_bytes()
dll=Path(capstone._cs._name)
result=dict(question='Fresh legacy-input generation retains FP qualifiers or current-row-only repair?',method='A actual boundedhostproducer threeinvocations withFI-onlywritepath redirection; no original/native/emulator/live FF12 executions',
    reference=dict(exe_sha256=eh,producer_path=producer.relative_to(Path.cwd()).as_posix(),producer_sha256=sha(source),fields_path=fields.as_posix(),fields_pre_sha256=sha(fb),fields_post_sha256=sha(postfb),fields_readback_unchanged=fb==postfb,old_input_path=oldpath.as_posix(),old_input_sha256=sha(oldbytes)),
    tools=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_dll=dict(path=str(dll),sha256=sha(dll.read_bytes()))),driver_sha256=sha(Path(__file__).read_bytes()),invocation=spec,receipts=receipts,
    normalized=dict(current_positive_S='PASS',legacy_patch_exit=0,generated_S='FAIL',generated_failure_count=1,source_R1_R2_M='PASS on both current and generated check',generated_default_refinement=True,generated_completed_qualifier=False,generated_DAZ_qualifier=False),
    initial_failure='Firstthreehostinvocations reachedexpectedexitcodes but captureparser incorrectly required single-spaced FAIL S; normalization abortedbeforefinalidentity/result. Exactinitialsource/raw/privatefixtures retained INVALID_NORMALIZATION. Correctedtokenparser regressedagainstbothactualrawcontrols, completedthreeinvocations/identities below; notsixsemantic/nativeexperiments.',
    interpretation='Actual e867536cf consumer/Scurrentrow repair valid, but existing --patch generator still emits oldunqualifiedrate text. Successful --patch is not satisfiedpostcondition. Default refinement/sourcefinitepredictions retained; no semanticrate/FP/native results changed.',
    required_change='OPUS fix actual --patch generatedtemplate or shared amendment procedure, retaining completedCOMISS/DAZ/DIVSS/nativeMXCSR/hostmodel limits already supplied41. Add same freshlegacy->patch->S regression withcurrentpositive, not just editscurrentrow/Stext. No new FF12/nativetest. SPEC verify producerpath and retainedfailure independently.',
    limits='Single WidgetB8 generator path with exact clonedproducer and two retained row inputs; other generator/type paths not surveyed. FI-only transformation and original__file__ explicit; source/hash guard unchanged, not raw unmodifiedhostprogram defaultpath invocation. R1/R2 staticdecoder and M hostfloat calculations, not original instructions/native game FP. Currentcanonical peerinput maychange later; historicalspecimen immutable. No canonical acceptance from owncontrols.',
    cleanup='No peerfield/reference/game/save/config/input/instrument/process writes. Only two privatefixture files writable; producer/reference readback unchanged; fieldsreadback status reported separately, no unrelatedpeerchange reset. Privatefixtures retained as boundedhostreplay data. PC OFF/S19spentunapproved/DBGOALNOT_MET.')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('Confirmed currentS PASS, freshlegacy --patch succeeds but generatedS FAIL(onlyS); actualgenerator misses requiredFP qualifiers, source/privateFIonly',flush=True)
