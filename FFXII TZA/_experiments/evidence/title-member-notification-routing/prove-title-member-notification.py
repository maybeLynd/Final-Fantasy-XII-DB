"""Prove exact title-member notification routing; no natural lifetime assertion.

Use verified original bytes and retained SECTION-04 input, not its fixture
verdict. Every required capture must have completed its wrapper and role
controls. A missing prerequisite is failure, never valid empty output.
Usage: python prove-title-member-notification.py FRESH_RESULT
"""
import hashlib, json, pathlib, re, struct, sys
W=pathlib.Path(__file__).resolve().parent; ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1])
if out.exists(): raise ValueError('immutable result already exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
exe=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'; b=exe.read_bytes()
if hashlib.sha256(b).hexdigest()!=PIN: raise ValueError('original image prerequisite')
pe=struct.unpack_from('<I',b,0x3c)[0]; opt=struct.unpack_from('<H',b,pe+20)[0]
secs=[struct.unpack_from('<IIII',b,pe+24+opt+i*40+8) for i in range(struct.unpack_from('<H',b,pe+6)[0])]
def read(va,n):
    for vs,sva,rs,ro in secs:
        if 0x120000+sva<=va and va+n<=0x120000+sva+rs:
            return b[ro+va-0x120000-sva:ro+va-0x120000-sva+n]
    raise ValueError('unbacked original input')
records={}; inputs=[]
for name,driver in [('title-watcher-lifetime-raw-02.json','capture-title-watcher-lifetime.py'),
                    ('title-member-routing-raw-01.json','capture-title-member-routing.py'),
                    ('title-watcher-attachment-raw-01.json','capture-title-watcher-attachment.py')]:
    p=W/name; r=json.loads(p.read_text())
    if r.get('exe_sha256')!=PIN or not r.get('wrapper_complete'):
        raise ValueError('missing completed capture prerequisite')
    if r['driver_sha256']!=sha(W/'capture-index-path.py') or r.get('invocation_driver_sha256')!=sha(W/driver):
        raise ValueError('actual capture invocation prerequisite')
    if len(r['controls'])!=3 or any(c['expected']!=c['observed'] for c in r['controls']):
        raise ValueError('access-role prerequisite')
    for s in r['ranges']:
        start=int(s['start'],16); end=int(s['end_exclusive'],16)
        if hashlib.sha256(read(start,end-start)).hexdigest()!=s['sha256']:
            raise ValueError('original source hash prerequisite')
        cursor=start
        for i in s['instructions']:
            pc=int(i['pc'],16); z=bytes.fromhex(i['bytes'])
            if pc!=cursor or read(pc,len(z))!=z: raise ValueError('original instruction prerequisite')
            cursor+=len(z)
            if pc in records and records[pc]!=i: raise ValueError('overlapping source disagreement')
            records[pc]=i
        if cursor!=end: raise ValueError('incomplete original source coverage')
    if name=='title-watcher-attachment-raw-01.json':
        t=r['controller_message_table']; z=read(0x582f54,19*4)
        if t['entries']!=19 or t['bytes']!=z.hex() or t['sha256']!=hashlib.sha256(z).hexdigest():
            raise ValueError('guard-derived controller table prerequisite')
        if t['message18']!='0x582e81': raise ValueError('controller teardown identity')
    inputs.append(dict(path=name,sha256=sha(p),driver=driver,driver_sha256=sha(W/driver)))

# Reuse original descriptor/caller bytes; do not re-execute old native samples.
old=W/'section04-title-member-source'
for name,pin in [('original_body_manifest.json','2ae22b0b46bbb7a83cb545d5bc45bb62d350f03509a4e5d41b2725e26cbee5ef'),
                 ('original_disassembly.txt','ca93837847ed6efdc72a7ee26d8457324fc44ef06dddcfe60ffcf43c4aad1c57')]:
    if sha(old/name)!=pin: raise ValueError('immutable retained source prerequisite')
manifest=json.loads((old/'original_body_manifest.json').read_text())
if manifest['exe_sha256']!=PIN: raise ValueError('retained source identity')
selected={0x393ff0,0x394070,0x249580}
for body in manifest['bodies']:
    a=int(body['entry'],16)
    if a not in selected: continue
    n=body['bytes']
    if hashlib.sha256(read(a,n)).hexdigest()!=body['sha256']:
        raise ValueError('retained original body identity')
text=(old/'original_disassembly.txt').read_text()
covered={a:0 for a in selected}
for line in text.splitlines():
    m=re.match(r'^([0-9A-F]{8})\s+([0-9a-f]+)\s+(\w+)\s*(.*?)\s*$',line)
    if not m: continue
    pc=int(m[1],16)
    body=next((x for x in manifest['bodies'] if int(x['entry'],16) in selected and int(x['entry'],16)<=pc<int(x['end_exclusive'],16)),None)
    if not body: continue
    z=bytes.fromhex(m[2]); args=m[4].split(' ;')[0].rstrip()
    if read(pc,len(z))!=z: raise ValueError('retained disassembly byte disagreement')
    a=int(body['entry'],16)
    if pc!=a+covered[a]: raise ValueError('retained disassembly gap')
    covered[a]+=len(z)
    records[pc]=dict(pc=hex(pc),bytes=z.hex(),mnemonic=m[3],args=args)
for a in selected:
    expected=next(x['bytes'] for x in manifest['bodies'] if int(x['entry'],16)==a)
    if covered[a]!=expected: raise ValueError('missing retained source')

required={
    0x393ffd:('call','0x249580'), 0x394029:('call','0x2493d0'),
    0x394048:('call','0x249320'),0x394061:('jmp','0x249410'),
    0x2493de:('call','0x249210'),0x249332:('call','0x249210'),
    0x249274:('lea','rax, [rip + 0x345]'),
    0x24927e:('mov','qword ptr [rsp + 0x40], rax'),
    0x249286:('mov','dword ptr [rsp + 0x38], ebx'),
    0x24928d:('mov','qword ptr [rbx], rbp'),
    0x2492d9:('lea','rax, [rsp + 0x30]'),
    0x2492e5:('mov','qword ptr [rsp + 0x20], rax'),
    0x2492f3:('call','0x32e620'),
    0x2492f8:('inc','word ptr [rbp + 0x18]'),
    0x2495d9:('movsxd','rbx, ecx'),
    0x2495dc:('mov','rax, qword ptr [rbx + 0x10]'),
    0x2495e5:('mov','rcx, rbx'),0x2495e8:('call','rax'),
    0x2495ea:('mov','rdi, qword ptr [rbx]'),
    0x2495ed:('inc','word ptr [rdi + 0x1a]'),
    0x2495f1:('test','byte ptr [rdi], 2'),
    0x2495fa:('cmp','ax, word ptr [rdi + 0x18]'),
    0x249600:('cmp','dword ptr [rdi + 4], 0'),
    0x24960b:('mov','rcx, qword ptr [rdi + 8]'),
    0x249612:('mov','dword ptr [rsp + 0x20], 0x10'),
    0x249625:('mov','rax, qword ptr [rcx]'),
    0x249632:('call','rax'),
    0x249634:('and','dword ptr [rdi], 0xfffffffe'),
    0x249637:('and','dword ptr [rbx + 0x20], 0xfffffffe'),
    0x2491dc:('lea','rdx, [rip - 0xae3]'),
    0x2491f0:('call','0x244f50'),
    0x248746:('call','0x2494f0'),
}
def witnesses(rr):
    for pc,expected in required.items():
        if pc not in rr or (rr[pc]['mnemonic'],rr[pc]['args'])!=expected:
            raise ValueError('title member-routing witness changed at%x'%pc)
witnesses(records)
if records[0x249274]['memory'][0]['rip_target']!='0x2495c0':
    raise ValueError('request completion target changed')
if records[0x2491dc]['memory'][0]['rip_target']!='0x248700':
    raise ValueError('separate watcher factory identity')
controls={'member_callback_is_2495c0':True,'watcher_factory_is_distinct_2491b0':True,
          'requested_count_18_done_count_1a':True,'controller_message18_bound':True}
bad={pc:dict(i) for pc,i in records.items()};bad[0x249274]['args']='rax, [rip + 0x275]'
try:witnesses(bad)
except ValueError: controls['altered_completion_descriptor_refused']=True
else: raise ValueError('wrong completion descriptor accepted')
bad={pc:dict(i) for pc,i in records.items()};bad[0x249632]['mnemonic']='nop'
try:witnesses(bad)
except ValueError: controls['removed_owner_notification_refused']=True
else: raise ValueError('missing owner delivery accepted')

result=dict(
    question='Does the original title asset request path require the resource-member owner notification site249632, beyond the old synchronous/watcher probe sites?',
    hypotheses=['old synchronous24947D/watcher24955D sites are complete for the title requests',
                'the two title request factories use249210 and therefore prepare a2495C0 member-completion descriptor with a distinct owner-notify site249632'],
    method='A retained original caller/handler bytes plus selected original descriptor/factory/completion code. This distinguishes routing without live FF12 or isolated execution.',
    exe_sha256=PIN,driver_sha256=sha(pathlib.Path(__file__)),inputs=inputs,
    retained_inputs=[dict(path=str((old/x).relative_to(W)),sha256=sha(old/x)) for x in ['original_body_manifest.json','original_disassembly.txt']],
    controls=controls,
    normalized=dict(title_request_calls=['0x2493d0','0x249320'],common_factory='0x249210',
        completion_descriptor='0x2495c0',descriptor_user='low32 member pointer',
        member_owner='ticket+8',member_ticket='member+0',expected_count='ticket+18',completed_count='ticket+1a',
        ordinary_owner_notify='0x249632',message_id=16,member_callback_before_count=True,
        separate_watcher_factory='0x2491b0',separate_watcher_notify='0x24955d'),
    established=[
        '393FF0 prepares its two requests through2493D0 and249320, both calling249210.',
        '249210 prepares queue completion2495C0 and low32 member context before requesting32E620, then increments expected count18.',
        '2495C0 executes the member-specific callback first, increments ticket done count1A, and on sealed/equal/custom-zero branch sends16 to ticket+8 through handler call249632.',
        'The watcher route through248700/2494F0 exists separately; watching only24947D/24955D does not cover the member owner-notify site.',
        'A future negative callback observation needs249632 or an independently demonstrated equivalent complete detector, plus owner/ticket identity and live health controls.'
    ],
    refuted=['The old list of synchronous24947D and watcher24955D recipient sites is a complete detector for the prepared title member-completion path.'],
    unresolved=['Natural pending teardown/later delivery; callback cancellation/drain across full resource/parent lifetime; actual IO outcomes; pointer reuse/generation; any broader claim that no additional watcher is ever created through omitted services.'],
    affected=['OV29 preparation successor-request.md and notes.md, downstream future collector/negative-result criteria; title page lifetime claim remains OPEN'],
    limits='Source routing under valid ticket/member/service premises; no runtime hit, IO timing, original-machine execution or forced call. Member-specific callback may affect state; omitted helper effects are not silently assumed safe. No existing EXP is reclassified merely from this discovery.',
    cleanup='Offline reads only; reference image unchanged, no game/process/save/config session.'
)
if not all(controls.values()):raise ValueError('failed controls')
out.write_text(json.dumps(result,indent=2)+'\n')
print('ESTABLISHED title-member notification site249632; old two-site detector incomplete. Natural OV29 lifetime remains OPEN; no gameplay.')
