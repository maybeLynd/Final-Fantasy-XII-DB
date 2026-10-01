"""Acceptance counterexamples from original instructions/data and retained B result."""
import copy,hashlib,json,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def original_defaults(record):
 assert record['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
 parsed={}
 for body in record['code']:
  raw=bytes.fromhex(body['hex']);assert len(raw)==body['bytes'] and sha(raw)==body['sha256']
  entry=int(body['entry'],16);ins=list(md.disasm(raw,entry));assert sum(i.size for i in ins)==len(raw)
  actual=[{'address':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins];assert actual==body['instructions']
  if body['runtime_function'] is not None:assert body['runtime_function'][0]+0x120000==entry
  parsed[entry]={i.address:(i.mnemonic,i.op_str) for i in ins}
 ctor=parsed[0x18CD90]
 assert ctor[0x18CDD2]==('mov','dword ptr [rbx + 0xf4], 0x3f4ccccd')
 assert ctor[0x18CDDC]==('mov','dword ptr [rbx + 0xf8], 0x3dcccccd')
 assert ctor[0x18CDE6]==('mov','byte ptr [rbx + 0x110], 1')
 setter=parsed[0x194310]
 assert setter[0x194310]==('movss','dword ptr [rcx + 0xf4], xmm1')
 assert setter[0x194318]==('movss','dword ptr [rcx + 0xf8], xmm2')
 return {'glare_luminance_bits':'3f4ccccd','glare_threshold_bits':'3dcccccd','dof_enable':1}
def distinguish(default,authored,fields):
 assert fields
 assert any(default[k]!=authored[k] for k in fields),'selected values also fit constructor-only state'
 return True
def require_initialized_evidence(observed):
 assert observed['object_nonnull'] and observed['flags']==0x20001
 assert observed.get('successful_initialization') is True and observed.get('healthy_session') is True,'nonnull/flags alone are insufficient'
def main():
 source=json.loads((HERE/'source.json').read_text());defaults=original_defaults(source)
 data=(HERE/'scene.json').read_bytes();res=source['resources'][0];assert len(data)==res['bytes'] and sha(data)==res['sha256']
 common=json.loads(data.decode('utf-8-sig'))['Common']
 assert common['mGlareLuminance']==0.8 and common['mGlareThreshold']==0.1 and common['EnableDof']==0
 result_bytes=(HERE/'retained-init-result.json').read_bytes();readme=(HERE/'retained-init-README.md').read_bytes()
 assert sha(result_bytes)==source['retained_fixture']['result.json']['sha256'] and sha(readme)==source['retained_fixture']['README.md']['sha256']
 driver=(HERE/'retained-init-driver.txt').read_bytes();assert sha(driver)==source['retained_fixture']['check.py']['sha256']
 assert 'd4(lib + 0x20C)' in driver.decode() and 'uc.mem_read(a, 4)' in driver.decode()
 result=json.loads(result_bytes);assert result['ok'] is True and result['live_game'] is False and len(result['cases'])==8 and all(result['cases'].values())
 p=result['results']['P2'];assert p['flags_20C']=='20001' and p['lib']!='0' and p['ok'] is False and p['rets']['ctx_init']=='80070057' and p['plus_108']=='0'
 assert p['halt'][0]=='00000068'
 constructor_reading={'glare_luminance':0.8,'glare_threshold':0.1,'dof_enable':1}
 authored_expectation={'glare_luminance':common['mGlareLuminance'],'glare_threshold':common['mGlareThreshold'],'dof_enable':common['EnableDof']}
 # Expected displayed values, not an execution/certification of the native JSON conversion.
 cases=[]
 def reject(name,fn):
  try:fn()
  except AssertionError:cases.append({'name':name,'rejected':True})
  else:raise AssertionError('unrejected counterexample '+name)
 reject('equal glare observations establish scene binding',lambda:distinguish(constructor_reading,authored_expectation,['glare_luminance','glare_threshold']))
 refused={'object_nonnull':True,'flags':int(p['flags_20C'],16),'successful_initialization':False,'healthy_session':False,'evidence_class':'retained B deferred-context model'}
 reject('object and flags alone qualify successful healthy initialization',lambda:require_initialized_evidence(refused))
 wrong=copy.deepcopy(source);wrong['exe_sha256']='0'*64
 reject('wrong executable identity',lambda:original_defaults(wrong))
 wrong=copy.deepcopy(source);wrong['code'][1]['instructions'][0]['args']='dword ptr [rcx + 0xf4], xmm2'
 reject('setter transcript swapped without matching original bytes',lambda:original_defaults(wrong))
 assert distinguish(constructor_reading,authored_expectation,['dof_enable'])
 observation={'result':'A_DISCRIMINATOR_CORRECTION; NO_NEW_RUNTIME_RESULT; PENDING_REVIEW',
 'question':'Can requested source-glare/flags reads establish normal scene binding or successful library init?',
 'hypotheses':{'scene_H1':'constructor-only glare values','scene_H2':'authored Common equal glare values applied',
 'init_H1':'object/flags stored before refusal','init_H2':'successful immediate-context initialization'},
 'constructor':defaults,'selected_resource':res['path'],'selected_authored':res['selected_common'],
 'equal_glare_cannot_discriminate':True,'dof_enable_separates_constructor_only_from_this_Common_expectation':True,
 'retained_init_counterexample':{'class':'accepted retained B with disclosed deferred-device model','object_nonnull':True,'flags20C':'20001','Initialize_result':'80070057','plus108':'0','expected_fault':'read68'},
 'established':['original constructor glare/enable stores','one selected scene authored Common values','requested equal glare values fit constructor-only','retained original-code refusal stores matching flags/non-null object'],
 'unresolved':['actual initialized map/cutscene resource and active preset','normal live scene loader/producer occurrence','real immediate device/library success, scheduling and presentation','canonical consumer agreement'],
 'next_C':'Only after named consumer/state/trigger: read-only stable object/source/library snapshots with initialized-state/health controls; choose active non-default field against ctor or qualified producer transition. DOF0 refutes ctor-only but does not identify its writer on its own.',
 'limits':'No new original-code execution/live observation. Authored decimal comparison is not a test of native JSON conversion. One scene, no corpus universal. Device model refusal is not live game failure. No claims about absent writers/readers.',
 'cleanup':'No process/control/memory/input/instrument opened; no save/config/reference writes.'}
 (HERE/'observation.json').write_text(json.dumps(observation,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'result':'PASS_A_CONTROL_REVIEW','cases':len(cases),'controls':cases,
 'positive':'selected DOF enable differs from original ctor; actual scene activation remains unprepared',
 'native_fixture_rerun':False,'live_run':False,'fresh_semantic_live_closure':[]},indent=2)+'\n')
 print('PASS',len(cases),'controls; matching glare/flags not provenance or healthy-init proof; potential DOF discriminator, NO C')
if __name__=='__main__':main()
