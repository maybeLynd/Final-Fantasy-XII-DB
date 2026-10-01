"""Validate the explicit composite; never relabel the failed full collector."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;T=P.parent if(P.parent/'validate-title-source-annotations.py').exists() else P/'dependencies';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main(src,out):
 if out.exists():raise RuntimeError('immutable result exists')
 old=json.loads((src/'raw-01.json').read_text());new=json.loads((src/'raw-02.json').read_text())
 for tag,driver,expected_exit in [('collect-01','collect.py',1),('resume-01','resume.py',0)]:
  st=json.loads((src/(tag+'.status.json')).read_text())
  if st.get('terminal') is not True or st.get('exception') is not None or st.get('exit')!=expected_exit or st['driver_sha256']!=sha(src/driver) or not(src/(tag+'.stdout')).read_bytes():raise RuntimeError('required collector status failed/stale '+tag)
 if (src/'collect-01.stderr').read_text().splitlines()[-1]!='RuntimeError: bounded collection incomplete; raw coverage retained' or(src/'resume-01.stderr').read_bytes():raise RuntimeError('wrong collection failure/result path')
 if old['collection_complete'] is not False or old['budget_stop'] is None or old['raw_candidates'] or old['sites'] or new.get('collection_complete') is not True or new.get('literal_question_settled') is not True or new['literal_candidates']:raise RuntimeError('incomplete/unresolved composite')
 if new['parent_raw_sha256']!=sha(src/'raw-01.json') or new['parent_status_sha256']!=sha(src/'collect-01.status.json') or old['tools']['collector_sha256']!=sha(src/'collect.py') or new['collector_sha256']!=sha(src/'resume.py') or new['archive']!=old['archive']:raise RuntimeError('mixed composite inputs')
 coverage=old['coverage'][:-1];gaps={r['path']:r for r in coverage if r['status']!='COVERED_LITERAL_CODE_SPANS'};recognized=[r for r in coverage if r['status']=='COVERED_LITERAL_CODE_SPANS']
 if len(coverage)!=9429 or len(gaps)!=26 or len(recognized)!=9403:raise RuntimeError('partial coverage population changed')
 rows=new['coverage'];newpaths={r['path'] for r in rows};oldpaths={r['path'] for r in coverage};suffix=newpaths-set(gaps)
 if len(rows)!=642 or len(newpaths)!=642 or len(suffix)!=616 or suffix&oldpaths or len(oldpaths|newpaths)!=10045 or old['archive']['ebp_index_entries']!=10045:raise RuntimeError('missing/duplicate composite entry')
 if new['small_layout_gaps_checked_as_whole_bytes']!=26 or new['new_suffix_entries']!=616 or new['old_prefix_entries']!=9429 or new['new_read_bytes']!=sum(r['bytes'] for r in rows) or new['planned_read_bytes']!=new['new_read_bytes']:raise RuntimeError('suffix/gap completeness changed')
 for r in rows:
  if r['source_method']!='WHOLE_DECOMPRESSED_ENTRY_LITERAL_SCAN' or r['candidate_hits']:raise RuntimeError('unclosed literal candidate')
  if r['path'] in gaps:
   oldrow=gaps[r['path']]
   if (oldrow['sha256'],oldrow['bytes'],oldrow['archive_entry'])!=(r['sha256'],r['bytes'],r['archive_entry']):raise RuntimeError('gap preimage changed')
   p=src/'raw-02'/r['retained_raw']
   if sha(p)!=r['sha256'] or p.stat().st_size!=r['bytes'] or any(bytes([op,0x44,0x30]) in p.read_bytes() for op in [0x58,0x59,0x5d,0x5e]):raise RuntimeError('gap whole-byte control changed')
 for r in recognized:
  if r.get('matches')!=0 or r.get('anomalies') or r.get('decoded_candidate_functions')!=0 or r.get('candidate_alignments'):raise RuntimeError('unclosed prefix code candidate')
 if old['positive_controls']['actual_control_CALLs']!=962 or sha(src/'raw/positive-btlctrl.ebp')!=old['positive_controls']['retained_btlctrl_sha256'] or old['native_result_slot']!={'address':'0x1f28a50','bytes':'b0ff500000000000','result':'0x50ffb0'}:raise RuntimeError('positive/native identity changed')
 native=json.loads((src/'retained-native-source.json').read_text());lineage=json.loads((src/'native-source-lineage.json').read_text())
 if lineage['copy_sha256']!=sha(src/'retained-native-source.json') or lineage['member']['sha256']!=lineage['copy_sha256']:raise RuntimeError('retained native input changed')
 sp=importlib.util.spec_from_file_location('authored_native_rolecheck',T/'validate-title-source-annotations.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V);annotation=V.validate(native)
 result={'producer_complete':True,'method':'A scoped composite original-resource literal absence, zero native/game runs','driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'retained-native-source.json','sha256':sha(src/'retained-native-source.json')}],'annotation_prerequisites':[annotation],'input_archive_header_sha256':old['archive']['header_sha256'],'entry_count':10045,'recognized_prefix_code_entries':9403,'whole_entry_suffix':616,'whole_entry_small_gaps':26,'literal_target_calls':0,'partial_full_run_status':'INVALID_INCOMPLETE preserved exit1; never upgraded to PASS','composite_scope':'9429 retained prefix entries, with26 small layout gaps discriminated by exact wholebytes;616 unread suffix wholebytes. No already-covered prefix recapture.','established':['No literal CALL/CALLACT/CALLPOPA/CALLACTPOPA id3044 in these recognized function spans and the whole suffix/gap EBP bytes','The chosen resource-method discriminator does not need a live game or absence sampling','Native3044 result binding is50FFB0 and its unchecked selector API remains part of the binary even without a located literal caller'],
 'limits':['All recognized prefix code spans use the existing section0 directory model; other sections of those entries were not globally scanned','Whole31GB archive hash not recomputed; archive header/stat plus each decompressed entry content hash bound, noninterference/declaredreference assumptions explicit','Not natural function unreachability: other IDs/callback aliases, external/generated/compressed programs, other native writers and source dataflows remain open','Does not prove original actor type initialization or safety of row275; no fullOV42/21 closure or independent acceptance','256 byte calculations/13constants fromb4772fab not repeated; decoder positive962CALLs is a control, not gameplay/execution or962 new tests']}
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'producer_complete':True,'entry_count':10045,'literal_target_calls':0,'scoped_source_discriminator_closed':True,'natural_unreachability':False}))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--src',type=Path,default=P);a=ap.parse_args();main(a.src,a.output if a.output.is_absolute() else P/a.output)
