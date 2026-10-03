"""One additive publication using existing publisher transport/blob guards.

Existing packets are never replaced. Only eight absent referents and the new
alias's byte policy are added, alongside the immutable addendum.
"""
import hashlib,importlib.util,json,os,re,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
ROOT=next(p for p in W.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
T=ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'
ID='ASTRA-PUBLISH-RENDER-REVIEW-LINK-CLOSURE-1003'
F=W/'render-review-link-closure-frozen-ready'
DEST='Database/FFXII TZA/_experiments/evidence/render-review-link-closure'
OLD='Database/FFXII TZA/_experiments/evidence/render-review-phase-qualification'
ALIAS='Database/FFXII TZA/_experiments/evidence/fable-review-astra-render-clear-callee-footprints-1002'
PIN='9cb38594892152f23dbbc3644ad494b24cf6eaeafa2e83bece64138c88a4666e'
spec=importlib.util.spec_from_file_location('existing_guarded_publisher',W/'prepare-residue-packet-publication.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.JOBS[ID]=dict(slug='render-link-closure',pairs=[],message='ASTRA: restore exact referents for copied render reviews')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def apply(folder,name,op):
    p=folder/(name+'.json');p.write_text(json.dumps(op,indent=2)+'\n')
    return m.checked_run([sys.executable,'-B',str(T),'apply','--agent','ASTRA','--file',str(p)],timeout=90,receipt_prefix=folder/(name+'-receipt'))

if sys.argv[1]=='--add':
    folder=W/'render-link-publication-setup';folder.mkdir()
    task=dict(id=ID,kind='research',priority='P1',assigned_to='ASTRA',target='Ten broken copied-render-review links: immutable additive repair',
      scope='New29member addendum plus8 absent referents/one byte policy, original76 untouched',
      completion='Guarded explicit-path commit/blob verification/release; existing HEAD-aware check and independent route',
      checkpoint='Prepared default closure guard and actual invocation-path controls',dependencies=[],
      resources=[dict(key='@publication'),dict(key='file:database/ffxii tza/_index/_inbox/astra.md')]+[dict(key='file:'+x.lower()) for x in [DEST,OLD,ALIAS]])
    apply(folder,'add',dict(action='add',task=task))
elif sys.argv[1] in ['--deliver','--continue']:
    tag=sys.argv[2]
    if not re.fullmatch('[a-z0-9-]{1,64}',tag):raise ValueError('invalid fresh receipt tag')
    if sys.argv[1]=='--deliver':
        if m.claim_ready(ID,tag)!='CLAIMED':raise SystemExit(0)
    else:
        # A failed pre-write preparation can continue an existing own claim.
        # The supported current guard and exact ownership below still apply.
        guard=m.checked_run([sys.executable,'-B',str(T),'boardcheck'],timeout=90,
            receipt_prefix=W/('render-link-own-resume-'+tag))
        if not guard.stdout.strip().startswith(b'board ok: ') or guard.stderr.strip():raise ValueError('current owned-resume guard failed')
    folder=W/('publication-render-link-closure-'+tag);folder.mkdir()
    ok,why=m.team.board_status(m.team.BOARD)
    if not ok:raise ValueError(why)
    b=json.loads(m.team.read_board_text(m.team.BOARD));task=next(t for t in b['tasks'] if t['id']==ID)
    required={'@publication','file:database/ffxii tza/_index/_inbox/astra.md'}|{'file:'+x.lower() for x in [DEST,OLD,ALIAS]}
    if task['status']!='ACTIVE' or task['agent']!='ASTRA' or not required<={r['key'] for r in m.team.hold_set(task)}:raise ValueError('exact current ownership absent')
    manifest=json.loads((F/'manifest.json').read_bytes())
    if sha(F/'manifest.json')!=PIN or len(manifest['members'])!=29:raise ValueError('new frozen identity changed')
    if {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}!={r['path'] for r in manifest['members']}|{'manifest.json'}:raise ValueError('new frozen member set changed')
    for row in manifest['members']:
        if sha(F/row['path'])!=row['sha256'] or (F/row['path']).stat().st_size!=row['bytes']:raise ValueError('frozen bytes changed')
    oldmf=json.loads((ROOT/OLD/'manifest.json').read_bytes())
    if sha(ROOT/OLD/'manifest.json')!='5b647504198d614ff8f507eef6efbaf89875d9142853703f65854ec7980d8823':raise ValueError('original manifest moved')
    for row in oldmf['members']:
        if sha(ROOT/OLD/row['path'])!=row['sha256']:raise ValueError('original member moved')
    additions=json.loads((F/'additive-paths.json').read_bytes())
    if len(additions)!=8:raise ValueError('additive population changed')
    mapping={DEST+'/'+row['path']:F/row['path'] for row in manifest['members']}
    mapping[DEST+'/manifest.json']=F/'manifest.json'
    # Exact returned ORACLE remediation, additive within the existing file claim.
    extra=W/'render-review-link-driver-fix-frozen-ready'
    em=json.loads((extra/'manifest.json').read_bytes())
    if sha(extra/'manifest.json')!='f6ccb00e674e3100cb73a7628089148db1d4139c897c0b512b06a3d16ea59579' or len(em['members'])!=6:
        raise ValueError('driver-correction identity changed')
    if {p.relative_to(extra).as_posix() for p in extra.rglob('*') if p.is_file()}!={r['path'] for r in em['members']}|{'manifest.json'}:
        raise ValueError('driver-correction members changed')
    for row in em['members']:
        if sha(extra/row['path'])!=row['sha256'] or (extra/row['path']).stat().st_size!=row['bytes']:
            raise ValueError('driver-correction bytes changed')
        mapping[DEST+'/drivers-v2/'+row['path']]=extra/row['path']
    mapping[DEST+'/drivers-v2/manifest.json']=extra/'manifest.json'
    mapping[DEST+'/publication-delivery.py']=Path(__file__)
    apply(folder,'oracle-scope-checkpoint',dict(action='checkpoint',task=ID,
        note='Preparation04 claimed then failed BEFORE canonical writes: LF-only policy guard contradicted the old immutable manifest which pins CRLF8b9c3028. Git confirms text unset. Prior checkpoint47 was the planned pathset, not an actual commit. Corrected guard keeps the exact old76/manifest hash prerequisite and accepts equivalent LF/CRLF policy syntax without changing bytes. Supported owned-resume guard/current exact claims checked; fresh receipt, no claim replay. Returned ORACLE76bf92900 requires case IDs/committed drivers: six successor files+manifest plus the actual delivery source under the existing owned addendum; planned48 explicit paths. Commit/blob verification/release still pending until actual terminal receipts. Then run tracked drivers, seal/check and route independent review. No peer scope or semantic credit.'))
    for row in additions:
        if not row['path'].startswith((OLD+'/',ALIAS+'/')) or sha(F/row['frozen_source'])!=row['sha256']:raise ValueError('additive destination/source mismatch')
        mapping[row['path']]=F/row['frozen_source']
    if any((ROOT/path).exists() for path in mapping):raise ValueError('destination exists: reconcile, no overwrite')
    paths=list(mapping)+[ALIAS+'/.gitattributes','Database/FFXII TZA/_index/_inbox/ASTRA.md']
    m.qualify_native_path_budget(paths)
    inbox=ROOT/paths[-1];before=inbox.read_bytes();(folder/'astra-preimage.txt').write_bytes(before)
    # Byte policy precedes payload. The old packet's existing policy is verified.
    # Its exact bytes are already pinned by oldmf. LF/CRLF both express -text;
    # preserve the actual CRLF member rather than rewriting it to satisfy a guard.
    if (ROOT/OLD/'.gitattributes').read_bytes() not in (b'* -text\n',b'* -text\r\n'):raise ValueError('original byte policy syntax unsupported')
    (ROOT/DEST).mkdir();(ROOT/DEST/'.gitattributes').write_bytes(b'* -text\n')
    (ROOT/ALIAS).mkdir();(ROOT/ALIAS/'.gitattributes').write_bytes(b'* -text\n')
    for path,source in mapping.items():
        target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True)
        if path==DEST+'/.gitattributes':
            if target.read_bytes()!=source.read_bytes():raise ValueError('byte policy differs')
        else:
            with target.open('xb') as out:out.write(source.read_bytes())
    prefix='''## SOL in ASTRA — checkpoint79: delivery and returned evidence

Full L1+L2 plus accepted deployed M0-M5 ACTIVE/NOT_MET. Checked current epoch4
board governs; no old operations/restore/reaping or parked menu retry.
SD194 caller frames committed ace5507ec007c42c2336a5668221ad371db282e6,
82 exact paths/blob checks and publication release. Under normal private ABI,
two reaching paths use inputs S-440/S-392: 48B apart, admitted ranges overlap212B.
Actual bytes, natural field entry, queue acceptance and lifetime remain open.
Independent SPEC/DATA/OPUS routes issued once, incorporation is separate.

The24 returned SPEC reviews at abac4e3d9/5cf0bc196/74b96c7cd are DONE/ACCEPT;
do not re-run their samples or describe their review as pending. Owning consumer
changes still need exact receipts. DATA authored flow c77a50981 and independent
c5f35fc3c accepted: loop H1 under valid nonNULL/context/ABI/noninterference
premises; first read H2 because init29A result is untested. Initial queue order,
native writers, loaded allocation/nonalias/lifetime and action0 remain open.
AUTO incorporation ACTIVE; FABLE/OPUS owning pages once-routed, not overwritten.

FRONTIER3319c2a6f resolved the atomic-write cause: overlapping parse-while-open
readers exceeded old3.2s retry. Current writer uses30s fail-closed deadline and
readers close before parsing. Boardcheck passes. All118 prior operations were
already reconciled; do not replay failed62. Original failure receipts preserved.

Current additive link repair preserves original76 members/manifest5b647504.
Seven exact reviewer referents plus a navigation alias resolve ten links;
the actual shared prepare() now rejects omitted copied-review referents before
writes. Three CLI refusals and a private actual-path control are publication
controls, not FF12 or reviewer executions. ORACLE sealing request routed once.
Exact commit/release/HEAD check receipts govern closure, not preparation alone.

Dashboard READY counts all addressed READY, including publication waits and new
incorporation notices. Earlier resource-ready counts were a narrower measure.
Gauge/copy proof deliveries remain queued; original PC1/UQ146/UQ147 propositions
remain unresolved. Do not turn resource waits or this checkpoint into completion.
PC OFF; all own finite helpers terminal after completion, no game/native/attach/
input/save/config/reference changes. Menu allowance spent/extension unapproved,
EXP127 invalid/crash unknown, K14 independently accepted closed.

'''.encode()
    prefix="""## SOL in ASTRA — checkpoint82: actual returned evidence and receipt prerequisites

SD194 caller frames independently ACCEPTED at96820750d: inputs48B apart,
possible260B spans overlap212B, no surviving contents or natural reach implied.
DATA resumed its existing consumer; OPUS has an existing automatic unblock.
No duplicate request or peer edit; canonical commit receipts remain pending.
Reviewer reproduction is not another ASTRA test. One additional bounded
proposition accepted offline here; historical four remain separate.

FRONTIER read repair543493b is published: matching replace-window denial was
reproduced offline; core board_status/sixCLI reads use bounded10s retry without
stale fallback. Current supported guard is the resumption condition. No old
operation replay, board restore, reaping, or all-consumer-read protection claim.

ORACLE76bf92900 is DONE with an exact required correction, not a seal. Old
render preparation/control receipts remain unsealable and immutable: missing
case IDs/uncommitted drivers. Additive drivers-v2 declares IDs and commits the
exact successor producers beside their retained shared publisher source.
Next run these committed copies into fresh ignored outputs; route ORACLE once
with the driver commit and actual raw outputs, then finish HEAD link checks and
independent procedure review. Never promote the old receipt or call a trial seal
durable acceptance. Full goal ACTIVE/NOT_MET, no FF12/PC activity.

Event0 proof03 is validated and frozen separately: both prescribed callbacks
read view+48, return EAX0/no call/nonstack write; registration itself has stores.
Producer/path controls complete, independent review/consumption still pending.
Menu setup remains spent/extension unapproved; EXP127 remains invalid.

""".encode()+prefix
    if inbox.read_bytes()!=before:raise ValueError('fresh handoff preimage moved')
    inbox.write_bytes(prefix+before)
    m.checked_run([sys.executable,'-B',str(T),'current','--agent','ASTRA','--file',str(inbox),'--write'],timeout=90,receipt_prefix=folder/'current-refresh')
    expected={path:sha(ROOT/path) for path in paths}
    (folder/'paths.json').write_text(json.dumps(paths,indent=2));(folder/'reviewed-sha256.json').write_text(json.dumps(expected,indent=2))
    (folder/'message.txt').write_text('ASTRA: restore exact referents for copied render reviews\n\nOriginal76 members/manifest immutable; additive8 plus byte policy. Returned ORACLE requires stable case IDs and committed producers: seven additive drivers-v2 paths plus actual delivery source, original29 unchanged. Exact48 paths, then committed reruns/sealing/HEAD checks and independent acceptance pending. No FF12/reviewer execution credit.\n')
    argv,transport=m.publisher_argv(folder,ROOT/'Database/Tools/analysis-kit/gfz-scripts/publish_paths.sh',paths)
    artifacts=paths[:-1];data=('\n'.join(artifacts)+'\n').encode()
    if m.checked_run(['git','hash-object','--stdin-paths'],data=data).stdout!=m.checked_run(['git','hash-object','--no-filters','--stdin-paths'],data=data).stdout:raise ValueError('filters would change immutable payload')
    env=dict(os.environ,TEAM_AGENT='ASTRA');env.pop('XII_PUBLISH_NO_BOARD_CHECK',None)
    r=m.checked_run(argv,env=env,timeout=150,receipt_prefix=folder/'publisher')
    commit=m.committed_identity(r.stdout)
    changed=m.checked_run(['git','diff-tree','--no-commit-id','--name-only','-r',commit]).stdout.decode().splitlines()
    if len(changed)!=len(paths) or set(changed)!=set(paths):raise ValueError('commit path set differs')
    members=m.verify_git_blobs(commit,expected,handoff_bytes=inbox.read_bytes())
    (folder/'commit-verification.json').write_text(json.dumps(dict(status='VERIFIED',commit=commit,paths=len(paths),members=members),indent=2))
    apply(folder,'finish',dict(action='finish',task=ID,note='Exact additive commit '+commit+'; '+str(len(paths))+' reviewed paths/blob checks, original76 untouched. Publication released; affected HEAD check and independent incorporation remain separate.',result_refs=['commit:'+commit,'record:'+DEST+'/README.md']))
    print('VERIFIED_AND_RELEASED',commit,len(paths),'paths',flush=True)
else:raise ValueError('usage --add / --deliver FRESH_TAG')
