"""Brief guarded delivery of *existing* prepared evidence tasks.

This is only a curated copy/preimage/path-list helper, not a new board/publisher.
It refuses without the exact current supported claim. Existing publish_paths.sh
still owns staging/commit. All scientific inputs/results remain frozen.
Usage: python prepare-residue-packet-publication.py EXACT_TASK_ID
       python prepare-residue-packet-publication.py --publish EXACT_TASK_ID
       python prepare-residue-packet-publication.py --claim EXACT_TASK_ID FRESH_RECEIPT_TAG
--claim is one bounded55-second foreground wait for this curated task's slot.
It writes at most one fresh supported claim; a refused claim is never retried.
--publish requires an already prepared plan and the actual publication claim.
It uses the existing publisher, checks its terminal status and exact commit
receipt (never moving HEAD), verifies blobs, then uses supported team.py finish.
It never acquires/reaps claims, retries an old operation or starts a server.
"""
import hashlib,json,pathlib,shutil,sys,subprocess,os,re,time
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
sys.path.insert(0,str(ROOT/'Database/Tools/analysis-kit/gfz-scripts'));import team
JOBS={
 'ASTRA-PUBLISH-SOFTEDGES-POINTER-KEYS-0930':dict(slug='softedges-pointer-key',pairs=[
  ('softedges-pointer-key-frozen-ready','phyretext-pointer-key-binding',49,'6a8251bc8e63e3c71c37743b040a0b5c1ae42ba0c6b854b4273c299c9dd34d77')],
  message='ASTRA: bind conditional PhyreText pointer keys and correct array recursion guard polarity',
  result='Under matching unchanged native mappings, packed22/27 recurse through outer kind3 arrays and stop at inner kind2 m_els: first11 definitions and World singleton. Both getters are verified original16D680 return-self;632A10 stores arg7 into+5C. Native address retains symbolic arrayF4/effectVariantF4. Query result1 permits kind2 recursion, contradicting current fail wording. Exact getter-slot and count-register failed hypotheses/no-result receipts preserved, repaired producers and actual affected refusal controls pass. Prior field/member reviews and canonical consumption stay separate. Actual successful load, native pointer identity/lifetime, aliases, pre-assignment59CD14/opaque cleanup and whole constructor/OV42 remain OPEN. Final03 pins the prior field manifest/table, not a moving report. Method A only, no new native/live samples or whole runtime-row closure. Next source question: identify59CD14 destination and value and their initialized-state prerequisites before any complete effects claim; use current board and retained source, no menu retry. All known own helpers terminal except this useful guarded publication.'),
 'ASTRA-PUBLISH-SOFTEDGES-MEMBER-BOUNDARIES-0930':dict(slug='softedges-member-boundaries',pairs=[
  ('softedges-member-boundaries-frozen-ready','phyretext-member-boundaries',41,'476a82ca36107bde2f8cf07b42b9e336524a836fbd7ba23c49928e5f13a81f5d')],
  message='ASTRA: delimit original packed-member address and shader-array callback ABI',
  result='Original named m_els slot40 ->60F3D0 directly passes object/source/count to registered60F280. The callback calls60EFE0 then overwrites inner status with0; signed negative count can yield inner5/no array write but callback0. Original59EC40 address adjustment is modulo32/zero-extended before adding the64-bit object, not unrestricted signed arithmetic. Exact sources, full normal unwind continuation and concrete refusal controls retained. File/native mapped-child construction, key22/27 terminal member, actual resource binding, lifetime, aliases and opaque cleanup remain OPEN. Method A only; no new native/live samples or whole OV closure. Prior field extent5bbbe5528 delivered; existing reviews/consumers remain separate. Next: source-trace construction of mapped-member+28 child link before a concrete key22/27 membership claim; do not assume it null or reuse the different outer60F590 setter. Seven normal unwind-chain entries now cover59EC40..59ED61; old19B checkpoint is historical and no longer the next step. METHODS preserves the failed hypotheses and exact source controls. Player version: loader success return alone cannot prove an array count was accepted; no game session needed.'),
 'ASTRA-PUBLISH-SOFTEDGES-FIELD-EXTENT-0930':dict(slug='softedges-field-extent',pairs=[
  ('softedges-field-extent-frozen-ready','phyretext-softedges-field-extent',81,'edc46fa5f7f4488bf7f65a91f527af97feed376104c822cef1bf5190a6938f76')],
  message='ASTRA: bind shipped PhyreText softEdges field and narrow original initializer source extent',
  result='Exact retained PhyreText file/class/name fixup binds record8 softEdges to offset160/size8. Original1EA609 copy, conditional on this unchanged definition and reaching the call, reads outer+120..127, excluding AE0/labels. Native reflected24B and packed13B layouts remain distinct. Actual inheritance/name/extent and CLI prerequisite controls pass; first inherited-member failure is preserved and producer repaired. Loaded-list membership, resource success, metadata changes, destination aliases, whole constructor return and natural lifetime/selection remain OPEN. One conditional copy-extent question answered offline, no new whole-row/runtime-request closure. Labels a568f9b5e also delivered; existing review/consumer routes remain pending.'),
 'ASTRA-PUBLISH-SPECIAL-OVERRIDE-LABELS-0930':dict(slug='override-labels',pairs=[
  ('special-override-label-binding-frozen-ready','special-action-override-label-binding',40,'3ab2573fa84a02a85586b5477207783d54f251b5631ca6785c08f50de2330d99')],
  message='ASTRA: deliver original override label representation and conditional native word mapping',
  result='Original reached initializer writes nine inline32-byte label slots AE4..C03. Formatter item182 selects via signed AE0*32, no local clamp. OFF then Black Hole241/Luminescence231/Ark Blast234/Whiteout237/Windburst229/Torrent228/Cataclysm227/Inferno226 correlate under unchanged state/table. Padding unknown; no independent combat meaning, whole-constructor return, alias/writer/lifetime or natural selection proof. Actual final02 prerequisite controls refuse missing/incomplete/corrupt evidence. R15 reused elsewhere, so no whole-function receiver assumption. Existing SPEC/FABLE labels routes41913/41914 remain separate.'),
 'ASTRA-PUBLISH-SPATTACK-REMAP-AND-RENDER-0930':dict(slug='remap-render',pairs=[
  ('spattack-remap-frozen-ready','spattack-native-word-remap',37,'294ec7aea17d2e2df94950c6db0949383cfb5f6fe62fdb65ebd7c06a237ae230'),
  ('render-executor-frozen-ready','render-executor-static-consumption',7,'5991ef6620fe339983ed61c6de629fbab70783dcb87b305b45c377c9f60cc83a')],
  message='ASTRA: deliver original special-action word remap and render executor source consumption',
  result='Native pending word-minus/plusD0 preserves511..534 conditionally;CF collides with the-1 sentinel. Exhaustive word arithmetic is not65536 native executions. Original member/caller initialization and natural selection remain open. Render callback gets stack context0=02CC0410,context10=block+10,not the opcode block; staticreturn60A8D9. One obsolete runtime request was already source-superseded41260, not newly counted here. Existing SPEC/FABLE routes41356/41357 remain separate.'),
 'ASTRA-PUBLISH-ACTION-SELECTOR-EXCLUSIONS-0930':dict(slug='selector-exclusions',pairs=[
  ('action-selector-exclusions-frozen-ready','action-selector-local-exclusions',74,'8221834782de76d5d53743a53d436240d9e3fd89adb8460e11f1017bdd82c81a')],
  message='ASTRA: deliver original category and byte-fallback selector exclusions',
  result='Category7 excludes the ordinary candidate action path only with nonnull raw+5==0; nonzero raw+5 bypasses. Negative-override fallback returns unsignedBYTE0..255 or rejectedFFFF, so that path cannot supply511..534. Two scoped Method A answers, not wholeOV42 closure. Dispatch01 invalid10-entry overread preserved; actual producer derives6 from source CMP/JA and checker requires completion/extent. Mode022C215C is not row category. Existing SPEC/FABLE routes41390/41391 await independent derivation/canonical adoption.'),
 'ASTRA-PUBLISH-SPECIAL-OVERRIDE-DOMAIN-0930':dict(slug='override-domain',pairs=[
  ('special-override-domain-frozen-ready','special-action-override-domain',9,'e5c23356a35f014a8232d203547ee608c7d9e5af86be7da16aa78fd5ed007115')],
  message='ASTRA: deliver conditional original override initialization and domain invariant',
  result='Original constructor QWORD2710 at+ADC clears high DWORD+AE0 at that store. Given same-object/no-overwrite initial0..8, native control preserves0..8/index-1..7 and eight initialized words exclude511..534. Corrupt9 remains9/index8, so no arbitrary-state sanitizer. File default and external EXP190 stubs are not live state or our runs. Full writer/alias/lifetime and other-producer closure remain open. Existing SPEC/FABLE routes41500/41502 govern acceptance/consumption.'),
 'ASTRA-PUBLISH-TITLE-MEMBER-NOTIFICATION-0930':dict(slug='title-member-routing',pairs=[
  ('title-member-notification-frozen-ready','title-member-notification-routing',46,'2649c608f3ae6af968954de2b0ab148d0063d1b3a194eafda357509008ee128c')],
  message='ASTRA: deliver title resource-member callback routing and incomplete-observer correction',
  result='Both title factories prepare2495C0 via249210. Its ordinary sealed/equal/custom-zero path runs member callback, increments done1A(expected18), sends16 to ticket+8 at249632. Old24947D/24955D sender list is incomplete for this route. Final result03 uses immutable sibling inputs; actual prerequisite controls02 refuse missing/incomplete/corrupt source. Full-pdata inline-data and guessed-address failures retained, no semantic evidence from them. Normal pending teardown/lifetime/IO remain OPEN; existing SPEC/FABLE routes41564/41565 correct preparation before any live collector.')
}
def checked_run(args, *, cwd=ROOT, data=None, env=None, timeout=60, receipt_prefix=None):
    r=subprocess.run(args,cwd=cwd,input=data,env=env,capture_output=True,timeout=timeout)
    if receipt_prefix is not None:
        for suffix,z in [('.stdout',r.stdout),('.stderr',r.stderr),('.status.json',json.dumps(dict(argv=args,exit=r.returncode),indent=2).encode())]:
            with pathlib.Path(str(receipt_prefix)+suffix).open('xb') as f:f.write(z)
    if r.returncode:
        raise RuntimeError('upstream exit '+str(r.returncode)+': '+r.stderr.decode('utf8','replace')[-2500:])
    return r

def claim_ready(id,tag):
    job=JOBS[id]
    if not re.fullmatch('[a-z0-9-]{1,64}',tag):raise ValueError('invalid fresh receipt tag')
    receipt=W/(job['slug']+'-claim-watch-'+tag+'.json')
    op=W/(job['slug']+'-claim-operation-'+tag+'.json')
    if receipt.exists() or op.exists():raise ValueError('existing claim receipt/operation: reconcile, never replay')
    end=time.monotonic()+55;last=None;r=dict(task=id,status='WAITING',bounded_seconds=55)
    try:
        while time.monotonic()<end:
            ok,detail=team.board_status(team.BOARD)
            if not ok:raise ValueError('board incident: '+detail)
            b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']==id)
            if t['status']!='READY' or t.get('agent') is not None:
                raise ValueError('task changed/owned/not READY: reconcile without claiming')
            holders=[x['id'] for x in b['tasks'] if x['status']=='ACTIVE' and any(
                y['key'] in {'@publication','file:database/ffxii tza/_index/_inbox/astra.md'}
                for y in team.hold_set(x))]
            if not holders:
                with op.open('x') as f:json.dump(dict(action='claim',task=id,note=
                    'Fresh free-slot check for existing curated packet; one supported claim. No reaping/bypass/old-op replay.'),f,indent=2)
                result=checked_run([sys.executable,str(ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'),
                    'apply','--agent','ASTRA','--file',str(op)],timeout=45,
                    receipt_prefix=W/(job['slug']+'-claim-apply-'+tag))
                r.update(status='CLAIMED',operation=op.name,exit=result.returncode)
                break
            if holders!=last:print('Publication busy: '+','.join(holders),flush=True);last=holders
            time.sleep(3)
        else:r.update(status='BUSY_NO_OPERATION',holders=last)
        print(r['status'],flush=True)
    except Exception as e:
        r.update(status='REFUSED_REQUIRES_RECONCILIATION',error=str(e));raise
    finally:
        with receipt.open('x') as f:json.dump(r,f,indent=2)

def committed_identity(output):
    ids=re.findall(rb'^publish_paths\.sh: committed sha: ([0-9a-f]{40})\r?$',output,re.M)
    if len(ids)!=1:raise ValueError('missing/ambiguous exact publisher commit receipt; HEAD is not a substitute')
    return ids[0].decode('ascii')

def verify_git_blobs(commit, expected, *, handoff_bytes=None):
    if not re.fullmatch('[0-9a-f]{40}',commit) or not expected:raise ValueError('invalid/empty blob verification request')
    paths=list(expected)
    if any('\n' in p or '\r' in p for p in paths):raise ValueError('unsupported path newline')
    raw=checked_run(['git','cat-file','--batch'],data=('\n'.join(commit+':'+p for p in paths)+'\n').encode()).stdout
    pos=0;members=[]
    for p in paths:
        end=raw.find(b'\n',pos)
        if end<0:raise ValueError('missing Git blob header')
        header=raw[pos:end].split();pos=end+1
        if len(header)!=3 or header[1]!=b'blob' or not re.fullmatch(rb'[0-9a-f]{40}',header[0]):
            raise ValueError('missing/nonblob Git member: '+p)
        n=int(header[2]);z=raw[pos:pos+n];pos+=n
        # Empty stdout/stderr is an explicitly hashed valid artifact in negative
        # controls. A missing blob has a different header and remains refused;
        # the expected map itself must still be nonempty. Never infer empty data.
        if n<0 or len(z)!=n or raw[pos:pos+1]!=b'\n':raise ValueError('incomplete Git member: '+p)
        pos+=1;actual=hashlib.sha256(z).hexdigest();kind='strict SHA256'
        if p=='Database/FFXII TZA/_index/_inbox/ASTRA.md' and handoff_bytes is not None:
            if z.replace(b'\r\n',b'\n')!=handoff_bytes.replace(b'\r\n',b'\n'):
                raise ValueError('handoff differs beyond allowed LF normalization')
            kind='LF-only handoff normalization'
        elif actual!=expected[p]:raise ValueError('committed member hash mismatch: '+p)
        members.append(dict(path=p,bytes=n,git_sha256=actual,verification=kind))
    if pos!=len(raw):raise ValueError('unexpected extra Git batch output')
    return members

def publish_prepared(id):
    job=JOBS[id];pub=W/('publication-'+job['slug']+'-01')
    attempt=pub/'automated-publication-attempt-01.json'
    if not pub.is_dir() or attempt.exists() or (pub/'commit-verification.json').exists():
        raise ValueError('missing prepared plan or prior attempt/commit: reconcile; never auto-retry')
    ok,detail=team.board_status(team.BOARD)
    if not ok:raise ValueError(detail)
    board=json.loads(team.BOARD.read_text());t=next(t for t in board['tasks'] if t['id']==id)
    required={'@publication','file:database/ffxii tza/_index/_inbox/astra.md'}|{
        'file:database/ffxii tza/_experiments/evidence/'+name for src,name,n,pin in job['pairs']}
    if t['status']!='ACTIVE' or t['agent']!='ASTRA' or not required<={r['key'] for r in team.hold_set(t)}:
        raise ValueError('exact current publication/file claims absent')
    paths=json.loads((pub/'paths.json').read_text());expected=json.loads((pub/'reviewed-sha256.json').read_text())
    inbox='Database/FFXII TZA/_index/_inbox/ASTRA.md';artifacts=[p for p in paths if p!=inbox]
    if len(set(paths))!=len(paths) or set(paths)!=set(expected) or inbox not in paths:
        raise ValueError('empty/duplicate/mismatched reviewed path set')
    wanted=set()
    for src,name,n,pin in job['pairs']:
        frozen=W/src;m=json.loads((frozen/'manifest.json').read_text())
        if hashlib.sha256((frozen/'manifest.json').read_bytes()).hexdigest()!=pin or len(m['members'])!=n:
            raise ValueError('frozen manifest changed')
        rel='Database/FFXII TZA/_experiments/evidence/'+name+'/'
        wanted|={rel+x['path'] for x in m['members']}|{rel+'manifest.json'}
        for x in m['members']:
            p=ROOT/(rel+x['path'])
            if p.stat().st_size!=x['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:
                raise ValueError('canonical member differs from frozen manifest')
        if hashlib.sha256((ROOT/(rel+'manifest.json')).read_bytes()).hexdigest()!=pin:
            raise ValueError('canonical manifest changed')
    if set(artifacts)!=wanted:raise ValueError('publication contains missing/extra artifact paths')
    for p in artifacts:
        q=(ROOT/p).resolve()
        if not q.is_relative_to(ROOT.resolve()) or not q.is_file() or hashlib.sha256(q.read_bytes()).hexdigest()!=expected[p]:
            raise ValueError('reviewed artifact preimage moved')
    data=('\n'.join(artifacts)+'\n').encode()
    normal=checked_run(['git','hash-object','--stdin-paths'],data=data).stdout.splitlines()
    unfiltered=checked_run(['git','hash-object','--no-filters','--stdin-paths'],data=data).stdout.splitlines()
    if len(normal)!=len(artifacts) or any(not re.fullmatch(rb'[0-9a-f]{40}',x) for x in normal) or normal!=unfiltered:
        raise ValueError('Git filters would alter immutable payloads')
    publisher=ROOT/'Database/Tools/analysis-kit/gfz-scripts/publish_paths.sh'
    receipt=dict(status='STARTED',task=id,board_revision=board['revision'],own_pid=os.getpid(),
                 driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
                 publisher_sha256=hashlib.sha256(publisher.read_bytes()).hexdigest(),explicit_paths=len(paths))
    with attempt.open('x') as f:json.dump(receipt,f,indent=2)
    # No interpolated shell path/body. The original publisher receives an argv array.
    env=dict(os.environ,TEAM_AGENT='ASTRA')
    env.pop('XII_PUBLISH_NO_BOARD_CHECK',None)
    args=[r'C:\Program Files\Git\bin\bash.exe','-c','PATH=/usr/bin:/bin:$PATH; export PATH; exec "$@"','_',
          publisher.relative_to(ROOT).as_posix(),(pub/'message.txt').relative_to(ROOT).as_posix(),*paths]
    try:
        r=subprocess.run(args,cwd=ROOT,env=env,capture_output=True)
        (pub/'automated-publisher-stdout-01.txt').write_bytes(r.stdout)
        (pub/'automated-publisher-stderr-01.txt').write_bytes(r.stderr)
        receipt['publisher_exit']=r.returncode
        if r.returncode:raise RuntimeError('publisher failed; inspect retained terminal output, no finish')
        commit=committed_identity(r.stdout);receipt['commit']=commit
        changed=checked_run(['git','diff-tree','--no-commit-id','--name-only','-r',commit]).stdout.decode().splitlines()
        if len(changed)!=len(paths) or set(changed)!=set(paths):raise ValueError('committed path set differs from reviewed plan')
        members=verify_git_blobs(commit,expected,handoff_bytes=(ROOT/inbox).read_bytes())
        verification=pub/'commit-verification.json'
        with verification.open('x') as f:json.dump(dict(status='VERIFIED',commit=commit,exact_paths=len(paths),members=members),f,indent=2)
        # The supported transaction is a distinct checked prerequisite. An exception
        # or nonzero result never becomes a DONE receipt or downstream success.
        op=pub/'op-finish-automated-01.json'
        refs=['commit:'+commit,'record:'+inbox]+['record:Database/FFXII TZA/_experiments/evidence/'+n+'/README.md' for _,n,_,_ in job['pairs']]
        with op.open('x') as f:json.dump(dict(action='finish',task=id,note='Exact publisher commit '+commit+'; terminal0, '+str(len(paths))+' reviewed paths/blob checks valid. Existing independent review/consumption routes now unblocked; producer validity is not acceptance. No PC/game/instrument; all synchronous delivery children terminal. Full L1+L2/M0M5 goal ACTIVE/NOT_MET.',result_refs=refs),f,indent=2)
        finish=checked_run([sys.executable,str(ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'),'apply','--agent','ASTRA','--file',str(op)],receipt_prefix=pub/'automated-finish-01')
        final=json.loads(team.BOARD.read_text());ft=next(t for t in final['tasks'] if t['id']==id)
        if ft['status']!='DONE':raise ValueError('supported finish did not land')
        receipt.update(status='VERIFIED_AND_RELEASED',final_revision=final['revision'])
        print(receipt['status'],commit,len(paths),'paths; publisher and transaction terminal')
    except Exception as e:
        receipt.update(status='FAILED_REQUIRES_RECONCILIATION',error=str(e))
        raise
    finally:
        # Same run's final status, not an overwritten historical capture. A future
        # invocation refuses this attempt file even when a failure occurred.
        attempt.write_text(json.dumps(receipt,indent=2)+'\n')

def prepare(id):
 job=JOBS[id]
 ok,d=team.board_status(team.BOARD)
 if not ok:raise ValueError(d)
 b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']==id)
 required={'@publication','file:database/ffxii tza/_index/_inbox/astra.md'}|{
  'file:database/ffxii tza/_experiments/evidence/'+name for src,name,n,pin in job['pairs']}
 if t['status']!='ACTIVE' or t['agent']!='ASTRA' or not required<={r['key'] for r in team.hold_set(t)}:
  raise ValueError('required current publication/file ownership absent')
 pub=W/('publication-'+job['slug']+'-01')
 if pub.exists():raise ValueError('existing delivery: reconcile, never overwrite/replay')
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 for src,name,n,pin in job['pairs']:
  f=W/src;m=json.loads((f/'manifest.json').read_text())
  if sha(f/'manifest.json')!=pin or len(m['members'])!=n:raise ValueError('frozen manifest identity changed')
  if {p.relative_to(f).as_posix() for p in f.rglob('*') if p.is_file()}!={x['path'] for x in m['members']}|{'manifest.json'}:raise ValueError('missing/extra frozen input')
  for x in m['members']:
   p=f/x['path']
   if p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:raise ValueError('frozen input bytes changed')
  if (ROOT/'Database/FFXII TZA/_experiments/evidence'/name).exists():raise ValueError('canonical destination already exists: reconcile')
 pub.mkdir();inbox=ROOT/'Database/FFXII TZA/_index/_inbox/ASTRA.md';before=inbox.read_bytes()
 (pub/'astra-preimage.txt').write_bytes(before);paths=[]
 for src,name,n,pin in job['pairs']:
  p=ROOT/'Database/FFXII TZA/_experiments/evidence'/name;shutil.copytree(W/src,p)
  paths += [q.relative_to(ROOT).as_posix() for q in sorted(p.rglob('*')) if q.is_file()]
 prefix=('## SOL in ASTRA — '+job['slug']+' publication package, 2026-09-30\n\n'
 'Full L1+L2 plus accepted deployed M0-M5 goal ACTIVE/NOT_MET. Current supported\n'
 'board healthy epoch3; exact current task '+id+'.\n'
 'Prepared immutable evidence under guarded publication; exact commit verification\n'
 'and release remain part of the task. Producer validity is not independent acceptance.\n\n'
 +job['result']+'\n\n'
 'Class20/SP1 delivery1cf5316d0, remap/render1f6569546, selector exclusions7f625ac43\n'
 'and title routing0fcf9349e are committed/exact payload verified and their\n'
 'publication holds released. Existing independent routes are unblocked.\n'
 'Conditional override-domain30754ad4b is also committed/verified/released;\n'
 'its review and consumption remain pending, separately from the current packet.\n'
 'No self-acceptance. Heading supplement8969fe745 was SPEC acceptedcd86f404d and\n'
 'OPUS consumedc4eb91ad3. SP1 repair1c1dfec separately ACCEPTED.\n'
 'WholeOV42/21/29 remain OPEN. One obsolete runtime request eliminated offline so\n'
 'far; no extra live/native experiment count from delivery or external reviews.\n'
 'No FF12/PC/input/instrument/save/config/reference writes. EXP127 INVALID; parked\n'
 'menu allowance remains spent/unapproved. Next original-source work and remaining\n'
 'prepared deliveries follow current board, not an unchecked export.\n'
 'User resource preference: close only our shells/terminals/helpers when done.\n'
 'Known prior exec sessions are terminal; no PC/runtime session retained. This\n'
 'publisher remains useful until terminal cleanup and exact commit verification.\n'
 'Failed CIM inventory and unavailable optional psutil do not establish absence\n'
 'of other processes; do not terminate peers by process name.\n\n').encode()
 if inbox.read_bytes()!=before:raise ValueError('fresh handoff preimage moved')
 inbox.write_bytes(prefix+before);paths.append(inbox.relative_to(ROOT).as_posix())
 (pub/'paths.json').write_text(json.dumps(paths,indent=2)+'\n')
 (pub/'reviewed-sha256.json').write_text(json.dumps({p:sha(ROOT/p) for p in paths},indent=2)+'\n')
 (pub/'message.txt').write_text(job['message']+'\n\nScoped immutable original-source evidence; explicit limits and independent acceptance pending. No live gameplay.\n')
 print('Prepared',job['slug'],'explicit reviewed paths; existing guarded publisher required.')

if __name__=='__main__':
 if sys.argv[1]=='--claim':claim_ready(sys.argv[2],sys.argv[3])
 elif sys.argv[1]=='--publish':publish_prepared(sys.argv[2])
 else:prepare(sys.argv[1])
