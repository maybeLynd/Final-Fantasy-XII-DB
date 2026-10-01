"""Reduce the recorded host/artifact observation; do not call Steam or FF12."""
import copy,hashlib,json,sys
from pathlib import Path,PureWindowsPath
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=json.loads((HERE/'raw.json').read_text(encoding='utf-8-sig'))
controls=json.loads((HERE/'profile-controls.json').read_text(encoding='utf-8-sig'))
prior_path=ROOT/'Database/FFXII TZA/_experiments/evidence/old-save-start-p/save-before.json'
prior=json.loads(prior_path.read_text())
def validate(j):
    assert j['status']=='HOST_ARTIFACT_OBSERVED_NO_FF12_PROCESS'
    assert j['ff12_process_count']==0 and not j['changes']
    assert j['steam_before']==j['steam_after']
    assert j['files_before']==j['files_after'] and len(j['files_before'])==2
    s=j['steam_before'];p=j['profile_file'];selected=p['selected'];uid=selected['steam_id64']
    assert p['record_count']>0 and p['sha256']==p['after_sha256']
    assert uid.isdecimal() and len(uid)==17 and int(uid)&0xffffffff==s['active_user_low32']!=0
    assert len(selected['account_name_casefold_sha256'])==64
    assert selected['account_name_casefold_sha256']==s['auto_login_name_casefold_sha256']
    entries={d['name']:d for d in j['directory_entries']}
    assert uid in entries and 'ReparsePoint' not in entries[uid]['attributes']
    root=PureWindowsPath(j['documents_root']);expected=[root/'keymap.ini',root/uid/'keymap.ini']
    assert [PureWindowsPath(f['path']) for f in j['files_before']]==expected
    for f in j['files_before']:
        assert f['bytes']>0 and f['keyboard1_header'] and f['circle_assignment']
        assert 'ReparsePoint' not in f['attributes']
        key=str(PureWindowsPath(f['path']).relative_to(root))
        assert prior['files'][key]==dict(bytes=f['bytes'],sha256=f['sha256'])
    assert j['files_before'][0]['sha256']==j['files_before'][1]['sha256']
    return uid
assert raw['capture_sha256']==sha(HERE/'capture.ps1')==controls['capture_sha256']
assert controls['control_sha256']==sha(HERE/'profile-controls.ps1')
assert controls['status']=='CONTROLS_PASS' and len(controls['cases'])==5 and all(controls['cases'].values())
uid=validate(raw)
mutations={}
for name in ('wrong_directory','changed_account_during_observation','empty_file_population'):
    m=copy.deepcopy(raw)
    if name=='wrong_directory':
        m['files_before'][1]['path']=str(PureWindowsPath(m['documents_root'])/'wrong-account'/'keymap.ini')
        m['files_after']=copy.deepcopy(m['files_before'])
    elif name=='changed_account_during_observation':m['steam_after']['active_user_low32']+=1
    else:m['files_before']=[];m['files_after']=[]
    try:validate(m)
    except AssertionError:mutations[name]=True
    else:raise AssertionError('Invalid observation accepted: '+name)
out=dict(method=raw['method'],status='EXISTING_DIRECTORY_MATCHES_HOST_PROFILE_ONLY',
         account_directory=uid,files=2,bytes_each=[f['bytes'] for f in raw['files_before']],
         same_content=True,unchanged_during_observation=True,observed_ff12_processes=0,
         prior=dict(path=str(prior_path.relative_to(ROOT)).replace('\\','/'),sha256=sha(prior_path),both_keymap_hashes_match=True),
         raw_sha256=sha(HERE/'raw.json'),source_sha256=sha(HERE/'capture.ps1'),
         python_version=sys.version,negative_controls=mutations,
         limits=['Host registry/profile metadata comparison, not ISteamUser::GetSteamID called by FF12.',
                 'Existing paths/files; neither creator nor current startup formatter execution observed.',
                 'Matching directory cannot prove returned-stack-pointer safety; no universal CRT claim.',
                 'Empty root path alone cannot diagnose corruption because uninitialized Steam is another documented path.'])
dest=HERE/'observation.json'
if '--write' in sys.argv:
    assert not dest.exists();dest.write_text(json.dumps(out,indent=2)+'\n')
else:assert json.loads(dest.read_text())==out
print('PASS: existing account directory matches bracketed Steam host identity; two699-byte keymaps agree with prior receipt.')
print('PASS: profile controls and three malformed-observation controls; no FF12 execution or formatter/lifetime conclusion.')
