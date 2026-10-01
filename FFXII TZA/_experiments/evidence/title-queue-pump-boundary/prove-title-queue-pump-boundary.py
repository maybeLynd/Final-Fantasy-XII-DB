"""Original pump-to-queue caller and local gate/catch-up boundary.

Reuse checked original source/CFG helpers; no native/emulated/game execution.
Fresh result [optional disposable source directory].
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
helper=W/'prove-title-queue-consumption.py'
EXPECTED_HELPER='041769e937b7f8fe03315ee522c77ca7774cd918cb428ef0a2de717b2d99e344'
if hashlib.sha256(helper.read_bytes()).hexdigest()!=EXPECTED_HELPER:raise ValueError('changed source/CFG prerequisite helper')
s=importlib.util.spec_from_file_location('source_checks',helper);P=importlib.util.module_from_spec(s);s.loader.exec_module(P)
def main():
 if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source directory]')
 out=pathlib.Path(sys.argv[1]);source=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
 if out.exists():raise ValueError('immutable output exists')
 pins=[];raw,x=P.load(source,'title-queue-pump-source-01.json',pins);getter,g=P.load(source,'title-cleanup-callback-queue-source-01.json',pins)
 if raw.get('pdata_entries')!=[[0x17d6e0,0x17d874,0x1d537c8]]:raise ValueError('wrong pump pdata')
 for q in raw['ranges']:
  wanted={'0x17d6e0':('0x17d874','32cd69cae29209ffb334e1a5a88307b8d7d05999f3e852740ba3cb5646bae78e'),'0x185c20':('0x185c25','94dfb411a8d6467828c1495d2998cdb39ef5388036fe707258faef658bd0264f')}
  if q['start'] not in wanted or (q['end_exclusive'],q['sha256'])!=wanted[q['start']]:raise ValueError('pump/tail identity changed')
 if len(raw['ranges'])!=2:raise ValueError('missing/extra original pump/tail source')
 cfg=P.closed(x,0x17d6e0,0x17d874)
 for pc,m,a in [(0x17d6ef,'xor','ebx, ebx'),(0x17d6f6,'cmp','dword ptr [rip + 0x1e5736c], ebx'),(0x17d706,'mov','dword ptr [rip + 0x1e01dac], ebx'),(0x17d70c,'jne','0x17d71b'),(0x17d70e,'call','0x189120'),(0x17d713,'mov','rcx, rax'),(0x17d716,'call','0x185c20'),(0x185c20,'jmp','0x186230'),(0x17d761,'call','0x189120'),(0x17d766,'mov','rcx, rax'),(0x17d769,'call','0x189ce0'),(0x17d76e,'call','0x189120'),(0x17d773,'mov','rcx, rax'),(0x17d776,'call','0x189570'),(0x17d853,'jmp','0x17d723')]:P.need(x,pc,m,a)
 if g[0x189120]['bytes']!='488b057164df01' or g[0x189127]['mnemonic']!='ret':raise ValueError('global getter instructions changed')
 def rip(ix,pc):
  z=[int(m['rip_target'],16) for m in ix[pc]['memory'] if m.get('rip_target')]
  if len(z)!=1:raise ValueError('missing/ambiguous original RIP identity')
  return z[0]
 if rip(g,0x189120)!=0x1f7f598 or rip(x,0x17d6f6)!=0x1fd4a68:raise ValueError('global context/gate identity changed')
 # Check the concrete normal caller path for FLAG preservation after the CMP.
 between=[i for p,i in sorted(x.items()) if 0x17d6f6<p<0x17d70c]
 if any(i['mnemonic'] not in {'mov','movaps'} for i in between):raise ValueError('gate flags changed before conditional jump')
 # Structural invariant: after this direct flush returns, no local CFG edge can
 # reach its own call site. Calls are treated as ABI-normal returning boundaries.
 todo=[0x17d71b];seen=set()
 while todo:
  p=todo.pop()
  if p==0x17d716:raise ValueError('repeat path re-enters direct flush')
  if p in seen:continue
  seen.add(p);i=x[p];m=i['mnemonic'];n=p+len(bytes.fromhex(i['bytes']))
  if m=='ret':continue
  if m=='jmp':todo.append(int(i['args'],16));continue
  if m.startswith('j'):todo.append(int(i['args'],16))
  todo.append(n)
 r=dict(status='PRODUCER_CHECKED_STATIC_CALLER_BOUNDARY_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,normal_cfg=cfg,helper_sha256=EXPECTED_HELPER,question='Does the shipping engine pump enter the four-bank consumer with the shared context, and does its internal repeat loop repeat this entry?',established=[
 'At17D6E0 entry, EBX is zero. Original DWORD01FD4A68 comparison survives only MOV/MOVAPS instructions to JNE17D70C. Zero gate takes189120->RCX=RAX->185C20; nonzero gate skips that direct entry.',
 '189120 returns the QWORD shared global01F7F598. The call passes that current returned value unchanged as RCX. Exact5B185C20 tail JMP186230 preserves it and reuses the caller return address; no object resolution or extra queue staging occurs at that tail.',
 'The first direct queue-consumer entry precedes the later renderer189CE0 and189570 calls in this pump. Those each fetch the shared global again; object stability between these reads is not silently guaranteed.',
 'Within this normal caller CFG, the direct queue entry can execute at most once per invocation. The internal repeat backedge17D853->17D723 skips the initial gate/getter/queue call while repeating later updates. The reachability check proves no normal path after17D71B returns to17D716.',
 'This is an original static caller relationship, extending the prior local consumer ABI. Conditional four-bank delays must count enabled consumer entries, not internal repeat iterations or necessarily wall-clock frames.'
 ],gate=dict(address='0x1fd4a68',width=4,enabled_value=0),context_global='0x1f7f598',assumptions=['ABI-normal caller state and returning named callees; external reentry is a separate boundary','Current shared global points to an initialized valid queue context for successful consumer behavior','Gate value observation, global pointer stability and concurrent writes are not established by code bytes'],limitations=['No observed process initialization, actual gate/pump execution, thread, frame duration, natural title callback overlap or cancellation/lifetime','No full caller census or indirect absence assertion; matched original caller plus5B tail is positive evidence only','Local at-most-once excludes nested reentry through opaque callees; no whole-transitive flush count guarantee','Pump and tail source/reducer checks are producer evidence, independent acceptance and canonical incorporation remain pending'],next_discriminators=['Bind5DE250/19C590 resource release effects and actual initialized-state/writer premises where title lifetime still depends on them','Use retained/static gate writers/constructor evidence before fresh process observation; do not reopen parked menu'],affected_claims=['FABLE renderer pump scheduling and title deferred-release boundary','OPUS queue entry ABI/gate and callback lifecycle contracts'],checker_sha256=P.sha(pathlib.Path(__file__)),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Original file reads only; own synchronous producer/reducer exits; no PC/game/process/instrument/save/config/reference write')
 with out.open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
 print('Shipping gated pump-to-consumer path and local once-per-entry invariant proved; initialized process/timing remain OPEN')
if __name__=='__main__':main()
