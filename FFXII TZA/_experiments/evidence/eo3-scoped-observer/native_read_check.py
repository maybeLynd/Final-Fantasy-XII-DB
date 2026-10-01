"""Read-only check of native reader receipts. No API calls or process launch."""
import copy
import hashlib
import json
from pathlib import Path
import sys

E=Path(__file__).resolve().parent;R=E/'native-reader-1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def check(data):
    ready,calls,owned,ended,clean,result,plan=(data[n] for n in ['ready','calls','ownership','exit','parent-cleanup','result','plan'])
    assert owned['popen_pid']==owned['child_pid']==ready['pid']==ended['pid']
    assert owned['parent_pid']==owned['child_parent_pid']==ready['parent_pid']
    assert owned['access']==0x410 and owned['python_sha256']==ready['python']['sha256']
    assert owned['opened_image'].casefold()==ready['python']['path'].casefold()
    assert clean['child_exit']==0 and clean['read_handle_closed'] and not clean['forced_stop']
    assert ended['normal'] and ended['allocation_freed'] and not ended['debugger_present']
    assert result['status']=='NATIVE_READER_CONTROL_ONLY' and result['fresh_live_game'] is False and result['original_code_executed'] is False
    assert plan['runner_sha256']==ready['source_sha256']==sha(E/'native_read_control.py')
    assert plan['reader_sha256']==sha(R/'reader-source.py')
    address=ready['path_address'];path=bytes.fromhex(ready['path_hex']);boundary=ready['page_boundary']
    assert address>0xffffffff and path.endswith(b'\0') and b'\0' not in path[:-1]
    assert address+len(path)==boundary==ready['allocation']+4096
    assert ready['allocation_bytes']==8192 and ready['second_page_protection']==1
    expected=[(address,len(path),path),(boundary-1,1,b'\0'),(boundary-1,2,None),(boundary,1,None)]
    expected += [(address+i,1,bytes([v])) for i,v in enumerate(path)]
    expected += [(address,len(path),path)]
    assert len(calls)==len(expected) and calls,'missing/extra/empty read sequence'
    handle=calls[0]['handle'];assert handle
    for row,(at,n,value) in zip(calls,expected):
        assert row['handle']==handle and (row['address'],row['requested'])==(at,n)
        raw=bytes.fromhex(row['raw_hex']);assert len(raw)==row['transferred']<=n
        if value is None:
            assert not row['result'] or row['transferred']!=n,'failed/partial control became a complete read'
        else:
            assert row['result']==1 and row['transferred']==n and raw==value
    assert len(result['outcomes'])==6
    for i in (0,4,5):assert bytes.fromhex(result['outcomes'][i]['bytes_hex'])==path
    assert result['outcomes'][1]['bytes_hex']=='00'
    for i in (2,3):assert result['outcomes'][i]['returned'] is None
    return dict(path_address=address,path_bytes=len(path),cross_page_raw=calls[2],noaccess_raw=calls[3],
                owned_child_pid=ready['pid'],cleanup_verified=True,
                established='Full-width exact native read succeeds; failed/cross-page reads are rejected; byte-limited NUL read avoids the guard page; positive still succeeds after failures.',
                limits=['Supplied stable native memory, not FF12 initialization/ownership/lifetime.',
                        'Selected Python/kernel32 identities only; no complete forwarded-module census.',
                        'No stopped debug-event read adapter, pending-event abort or game health qualification.'])


def main():
    data={n:json.loads((R/(n+'.json')).read_text()) for n in ['ready','calls','ownership','exit','parent-cleanup','result','plan']}
    observation=check(data);rejected=[]
    def reject(label,bad):
        try:check(bad)
        except (AssertionError,KeyError):rejected.append(label)
        else:raise AssertionError('invalid native evidence accepted: '+label)
    bad=copy.deepcopy(data);bad['calls']=[];reject('empty reads',bad)
    bad=copy.deepcopy(data);bad['calls'][0]['address']&=0xffffffff;reject('truncated native source pointer',bad)
    bad=copy.deepcopy(data);bad['result']['outcomes'][2]['returned']='00';reject('partial failed read promoted to data',bad)
    bad=copy.deepcopy(data);bad['ownership']['child_parent_pid']+=1;reject('wrong native parent identity',bad)
    bad=copy.deepcopy(data);bad['parent-cleanup']['read_handle_closed']=False;reject('unclosed owned read handle',bad)
    bad=copy.deepcopy(data);bad['exit']['allocation_freed']=False;reject('unfreed native allocation',bad)
    bad=copy.deepcopy(data);bad['calls'][-1]['raw_hex']='00'*bad['calls'][-1]['transferred'];reject('post-failure positive lost',bad)
    out=dict(status='VALID_NATIVE_READER_CONTROL_ONLY',observation=observation,rejected=rejected,
             raw_source_sha256={p.name:sha(p) for p in R.iterdir() if p.is_file()},
             ff12_run=False,original_code_executed=False)
    if '--write' in sys.argv:
        with (E/'native-reader-observation.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    else:assert json.loads((E/'native-reader-observation.json').read_text())==out
    print('Native reader evidence/control/ownership/cleanup checks PASS;',len(rejected),'corruptions reject. No FF12 claim.')


if __name__=='__main__':main()
