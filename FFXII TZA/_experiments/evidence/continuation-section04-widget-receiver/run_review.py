#!/usr/bin/env python3
"""Reproduce SECTION-04 without changing the original executable or database.
Linux x86-64, Python 3.10+, GCC and Capstone 5.0.9. No game process or downloads.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,os,platform,shutil,struct,subprocess,sys,tempfile
from importlib.metadata import version
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
CODE_MUTANTS={'message_read_from_receiver':'consumer_initial_mode_comes_from_message',
 'erase_rbx_kill':'consumer_xor_clears_state_not_message_address','ready_wrong_bit':'ready_message_sets_bit0',
 'skip_d0_clear':'teardown_clears_file_pointer','clear_other_singleton':'teardown_clears_asset_global',
 'consumer_tests_own_ready':'consumer_gate_uses_asset_not_own_status'}
AUDITOR_MUTANTS={'ignore_partial_write':['partial_byte_write_kills_pointer'],
 'keep_volatile':['call_clobbers_volatile_pointer'],
 'lea_is_memory':['lea_is_not_a_memory_read','lea_preserves_known_subobject_offset'],
 'xor_keeps_pointer':['xor32_kills_pointer','constant_lea_folds_without_access'],
 'join_chooses_pointer':['join_discards_disagreeing_provenance']}
def need(ok:bool,msg:str)->None:
    if not ok:raise RuntimeError(msg)
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def save(p:Path,o:object)->None:p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def native(binary:Path,exe:Path,out:Path,name:str,mutant:str|None=None)->tuple[dict,int]:
    env=dict(os.environ);env.pop('FF12_WIDGET_MUTANT',None)
    if mutant:env['FF12_WIDGET_MUTANT']=mutant
    p=subprocess.run([str(binary),str(exe)],capture_output=True,text=True,env=env,timeout=30)
    need(bool(p.stdout.strip()) and not p.stderr.strip(),f'native failure {name}: {p.returncode} {p.stderr}')
    obj=json.loads(p.stdout);save(out/(name+'.json'),obj);return obj,p.returncode

def main()->None:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--exe',required=True,type=Path)
    ap.add_argument('--output',required=True,type=Path);ap.add_argument('--cc',default='gcc');args=ap.parse_args()
    need(platform.system()=='Linux' and platform.machine().lower() in ('x86_64','amd64'),'requires Linux x86-64')
    need(shutil.which(args.cc) is not None,'compiler unavailable')
    import capstone
    need(version('capstone')=='5.0.9','bounded diagnostic pinned to capstone distribution 5.0.9')
    from receiver_audit import analyze,regression
    out=args.output.resolve();exe=args.exe.resolve();need(not out.exists() or not any(out.iterdir()),'refusing nonempty output')
    out.mkdir(parents=True,exist_ok=True);raw=exe.read_bytes();manifest=json.loads((HERE/'original_body_manifest.json').read_text())
    need(sha(raw)==manifest['exe_sha256'],'wrong original executable')
    for r in manifest['bodies']+manifest['additional_data']:
        b=raw[r['file_offset']:r['file_offset']+r['bytes']];need(len(b)==r['bytes'] and sha(b)==r['sha256'],'range hash mismatch '+str(r))
    save(out/'body_verification.json',{'exe_sha256':sha(raw),'body_count':len(manifest['bodies']),'all_matched':True,'bodies':manifest['bodies'],'additional_data':manifest['additional_data']})
    scope=json.loads((HERE/'scope.json').read_text());bodies={r['entry']:r for r in manifest['bodies']};data={r['address']:r for r in manifest['additional_data']}
    audits={};flat=[]
    for s in scope['bodies']:
        row=bodies[s['entry']];code=raw[row['file_offset']:row['file_offset']+row['bytes']];switches={}
        if 'jump_table' in s:
            t=s['jump_table'];d=data[t['address']]
            need(d['bytes']==4*t['entries'],'table size mismatch')
            switches[int(t['site'],16)]=[n+int(t['base'],16) for n in struct.unpack('<'+str(t['entries'])+'I',raw[d['file_offset']:d['file_offset']+d['bytes']])]
        a=analyze(code,int(s['entry'],16),{k:tuple(v) for k,v in s['seeds'].items()},
                  {int(k,16):v for k,v in scope['global_root_slots'].items()},switches)
        audits[s['entry']]=a
        flat.extend(dict(entry=s['entry'],**r) for r in a['accesses'])
    save(out/'receiver_audit.json',audits)
    # Concrete positive/negative supports, not a claim of complete field enumeration.
    expected=[('003939F7','message',8,1,'R'),('003939FD','consumer',0xc4,4,'W'),
      ('00393A03','consumer',0xc8,8,'W'),('00393A18','consumer',0xc0,1,'W'),
      ('00393A98','asset',0xc0,1,'R'),('00393AA5','asset',0xd0,8,'R'),
      ('00394033','asset',0xc8,8,'W'),('00394050','asset',0xd0,8,'W'),
      ('00394097','asset',0xc8,8,'R'),('003940A8','asset',0xd0,8,'R'),
      ('003940B9','asset',0xd0,8,'W'),('003940E3','asset',0xc0,4,'RW'),
      ('003940FC','asset',0xc0,4,'W'),('003945BB','consumer',0xc4,4,'RW')]
    actual={(r['site'],r['root'],r['offset'],r['bytes'],r['mode']) for r in flat}
    concrete=[]
    for e in expected:
        ok=e in actual;need(ok,'missing expected original support '+repr(e));concrete.append({'expected':e,'pass':True})
    need(not any(r['root']=='asset' and r['site'] in ('003939F7','00393A23') for r in flat),'false asset field attribution')
    expr=[r for r in audits['003939B0']['expressions'] if r['site']=='00393A23'];need(len(expr)==1 and expr[0]['value']==['const',21],'LEA constant not established')
    save(out/'concrete_support_checks.json',{'positive_supports':concrete,'false_asset_supports_absent':True,'lea_value':expr[0]})
    with (out/'receiver_accesses.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(flat)
    tests=regression();need(len(tests)==16 and all(t['pass'] for t in tests),'auditor regression failed');save(out/'auditor_regression.json',tests)
    am=[]
    for m,failures in AUDITOR_MUTANTS.items():
        r=regression(m);bad=[t['name'] for t in r if not t['pass']];need(bad==failures,'auditor mutant failed wrong checks: '+m+repr(bad))
        am.append({'mutant':m,'detected':True,'failed_checks':bad})
    save(out/'auditor_mutations.json',am)
    with tempfile.TemporaryDirectory(prefix='ff12-widget-section04-') as temp:
        binary=Path(temp)/'native_controls';command=[args.cc,'-std=c11','-O2','-Wall','-Wextra','-Werror','-fPIE','-pie',str(HERE/'native_controls.c'),'-o',str(binary)]
        p=subprocess.run(command,capture_output=True,text=True,timeout=45);need(p.returncode==0 and not p.stderr.strip(),'compile failed/warned: '+p.stderr)
        baseline,rc=native(binary,exe,out,'native_baseline');need(rc==0 and baseline['checks']==65 and baseline['failures']==0,'baseline failure')
        repeat,rc=native(binary,exe,out,'native_repeat');need(rc==0 and repeat==baseline,'repeat differs')
        cm=[]
        for m,expect in CODE_MUTANTS.items():
            r,rc=native(binary,exe,out,'mutant_'+m,m);bad=[c['name'] for c in r['cases'] if not c['pass']]
            need(rc==1 and bad==[expect],'code mutant failed wrong assertion: '+m+repr(bad));cm.append({'mutant':m,'detected':True,'failed_assertion':expect})
    save(out/'code_mutations.json',cm);need(sha(exe.read_bytes())==manifest['exe_sha256'],'original executable modified')
    summary={'section':'SECTION-04','status':'LOCAL PRODUCTION VALIDATED; independent acceptance pending','original_bodies_verified':len(bodies),'bounded_original_instruction_assertions':65,'repeat_identical':True,'original_code_mutants_rejected':len(cm),'auditor_regression_checks':len(tests),'auditor_mutants_rejected':len(am),'concrete_positive_support_checks':len(concrete),'analyzed_bodies':len(audits),'original_exe_unchanged':True,'application_boundary_substitutions':7,'import_bridge':'memset only','scope_limits':['No live FF12 session or actual IO/GPU/manager-tree/lifetime validation.','Positive consumer build path stops at 003946B0; later child tree not executed.','Service returns/pending counts and allocation/free boundaries are synthetic.','No rerun or repair of unavailable original producer scanner.','No new Ghidra import, whole-game scan, TEAM/L2 or terminal acceptance.']}
    save(out/'summary.json',summary)
    save(out/'execution_environment.json',{'python':sys.version,'system':platform.platform(),'compiler':subprocess.check_output([args.cc,'--version'],text=True).splitlines()[0],'capstone_distribution':version('capstone'),'capstone_binding_reported_version':capstone.__version__,'capstone_api':capstone.cs_version(),'fixture_sha256':sha((HERE/'native_controls.c').read_bytes()),'auditor_sha256':sha((HERE/'receiver_audit.py').read_bytes()),'driver_sha256':sha(Path(__file__).read_bytes())})
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
