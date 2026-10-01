#define _GNU_SOURCE
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <signal.h>
#include <ucontext.h>
#include <sys/wait.h>
#include <sys/resource.h>
#define ABI __attribute__((ms_abi))
#define H ((uintptr_t)0x40000000)
#define HS 0x400000
#define M (H+0x1000)
#define A (H+0x3000)
#define B (H+0x5000)
#define Q (H+0x7000)
#define QB (H+0x8000)
#define CODE (H+0x10000)
#define CODEB (H+0x20000)
#define LIST (H+0x40000)
#define LABELS (H+0x42000)
#define IPOOL (H+0x44000)
#define FPOOL (H+0x46000)
#define STACK ((uintptr_t)0x2099ac0)
static uintptr_t expected_fault_pc,expected_fault_address;
static unsigned checks,failures;static const char *mutant;static char current[128];
static uint8_t r8(uintptr_t p){uint8_t x;memcpy(&x,(void*)p,1);return x;}
static uint16_t r16(uintptr_t p){uint16_t x;memcpy(&x,(void*)p,2);return x;}
static uint32_t r32(uintptr_t p){uint32_t x;memcpy(&x,(void*)p,4);return x;}
static uint64_t r64(uintptr_t p){uint64_t x;memcpy(&x,(void*)p,8);return x;}
static void w8(uintptr_t p,uint8_t v){memcpy((void*)p,&v,1);}
static void w16(uintptr_t p,uint16_t v){memcpy((void*)p,&v,2);}
static void w32(uintptr_t p,uint32_t v){memcpy((void*)p,&v,4);}
static void w64(uintptr_t p,uint64_t v){memcpy((void*)p,&v,8);}
static void result(const char*n,int ok,int64_t a,int64_t e){printf("%s{\"name\":\"%s\",\"pass\":%s,\"actual\":%lld,\"expected\":%lld}",checks?",\n":"",n,ok?"true":"false",(long long)a,(long long)e);checks++;failures+=!ok;if(!ok&&mutant){printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);exit(1);}}
static void eq(const char*n,int64_t a,int64_t e){result(n,a==e,a,e);}
static void on_fault(int s,siginfo_t*si,void*ctx){ucontext_t*u=ctx;if(expected_fault_pc){int ok=s==SIGSEGV&&(uintptr_t)si->si_addr==expected_fault_address&&(uintptr_t)u->uc_mcontext.gregs[REG_RIP]==expected_fault_pc;_exit(ok?73:74);}dprintf(2,"FAULT case=%s sig=%d addr=%p pc=%llx\n",current,s,si->si_addr,(unsigned long long)u->uc_mcontext.gregs[REG_RIP]);_exit(128+s);}
static void map_at(uintptr_t p,size_t n,int flags){if(mmap((void*)p,n,flags,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0)==MAP_FAILED){perror("map");exit(2);}}
static void load(const char*fn){FILE*f=fopen(fn,"rb");if(!f){perror(fn);exit(2);}fseek(f,0,SEEK_END);long n=ftell(f);rewind(f);unsigned char*b=malloc((size_t)n);if(!b||n<512||fread(b,1,(size_t)n,f)!=(size_t)n)exit(2);fclose(f);uintptr_t p=(uintptr_t)b;uint32_t pe=r32(p+0x3c);if(pe+256>(uint64_t)n||r32(p+pe)!=0x4550)exit(2);uintptr_t opt=p+pe+24;uint64_t base=r64(opt+24);uint32_t sz=r32(opt+56);if(r16(opt)!=0x20b||base!=0x120000||sz>0x10000000)exit(2);map_at(base,sz,PROT_READ|PROT_WRITE|PROT_EXEC);for(unsigned i=0;i<r16(p+pe+6);i++){uintptr_t s=opt+r16(p+pe+20)+40*i;uint32_t va=r32(s+12),rs=r32(s+16),off=r32(s+20);if(s+40>p+(uintptr_t)n||(uint64_t)off+rs>(uint64_t)n||(uint64_t)va+rs>sz)exit(2);memcpy((void*)(base+va),b+off,rs);}free(b);map_at(H,HS,PROT_READ|PROT_WRITE);struct sigaction sa={0};sa.sa_sigaction=on_fault;sa.sa_flags=SA_SIGINFO;sigemptyset(&sa.sa_mask);sigaction(SIGSEGV,&sa,NULL);sigaction(SIGILL,&sa,NULL);sigaction(SIGBUS,&sa,NULL);}
static void reset(void){memset((void*)H,0,HS);memset((void*)STACK,0xA5,0x284);w32(STACK,0);w64(M+8,LIST);w32(LIST,2);w64(LIST+8,A);w64(LIST+16,B);w32(M+0x28,0);w64(M+0x68,IPOOL);w64(M+0x70,FPOOL);w32(IPOOL,16);w32(FPOOL,16);
 for(int i=0;i<2;i++){uintptr_t a=i?B:A,q=i?QB:Q,c=i?CODEB:CODE;w16(a,(uint16_t)i);w8(a+0x14,0x30);w8(a+0x18,1);w64(a+0xa8,q);w64(a+0x50,LABELS);w64(a+0x58,c);w64(q,c);w8(q+0x14,1);}w32(LABELS,8);w32(0x22c7f84,1);w8(0x2099011,0);((void(ABI*)(void))0x3dc2d0)();}
static int interp(uintptr_t a,uintptr_t q){return ((int(ABI*)(uintptr_t,uintptr_t,uintptr_t))0x25e4c0)(M,a,q);}
static void script(const uint8_t*p,size_t n){memcpy((void*)CODE,p,n);w64(Q,CODE);}

#define EA (H+0x60000)
#define EB (H+0x62000)
#define FA (H+0x64000)
#define FB (H+0x66000)
#define D (H+0x68000)
#define WL (H+0x69000)
static void setup(void){
 reset();
 w64(M,H+0xa0000);w64(0x2098e10,H+0xa0000);w64(0x2098e18,LIST);w32(0x2098e38,0);w32(0x1dfe40c,5);w8(0x2098e20,0);memset((void*)0x215f200,0,8*0x68);w32(0x1dfe0c0,1);w32(0x1f82e38,0);w32(0x22ca400,0);
 for(int k=0;k<2;k++){
  uintptr_t a=k?B:A,e=k?EB:EA,f=k?FB:FA,q=k?QB:Q,c=k?CODEB:CODE;
  w64(a+0xa0,e);w64(a+0x48,f);w8(a+2,2);w32(f,8);
  for(int j=0;j<8;j++){w32(f+8+8*j,0x100*j);w8(c+0x100*j,0x19);((void(ABI*)(uintptr_t))0x25d460)(q+0x28*j);}
  ((void(ABI*)(uintptr_t,int,int))0x3db580)(a,3,8);w8(a+0x62,0xff);w8(a+0x11,0);w64(q,c);w8(q+0x14,1);
 }
}
static void descriptor(int kind,int mode,int channel,int id,int origin,int origin_slot,int offset){
 memset((void*)D,0,0x14);w8(D,kind);w8(D+1,mode);w8(D+2,channel);w8(D+3,origin_slot);w16(D+4,id);w16(D+6,origin);w8(D+8,1);w32(D+0xc,0);w32(D+0x10,offset);
}
static int alloc_entry(uintptr_t a,int state){return ((int(ABI*)(uintptr_t,uintptr_t,int))0x3dbcf0)(a,D,state);}
static void select_entry(uintptr_t a){((void(ABI*)(uintptr_t))0x3db6e0)(a);}
static void drive(uintptr_t a){((void(ABI*)(uintptr_t,uintptr_t))0x25df00)(M,a);}
static int remove_entry(uintptr_t a,int idx){return ((int(ABI*)(uintptr_t,int))0x3db2a0)(a,idx);}
static int submit(int target,int channel,int id,int kind,int mode){
 w32(STACK,3);w8(STACK+4,1);w8(STACK+5,1);w8(STACK+6,1);w32(STACK+0x184,channel);w32(STACK+0x188,target);w32(STACK+0x18c,id);
 return ((int(ABI*)(uintptr_t,uintptr_t,uintptr_t,uintptr_t,uintptr_t,int,int))0x268850)(M,A,STACK,Q,CODE+9,kind,mode);
}
static void basic_arming(void){
 setup();strcpy(current,"initialize");eq("init_free_head_zero",r8(A+0x60),0);eq("init_detached_head_ff",r8(A+0x61),255);eq("init_channel_bits_zero",r16(A+6),0);eq("init_channels_empty",r8(A+0x94),255);eq("init_last_free_terminates",r8(EA+7*0x14),255);
 descriptor(2,1,2,1,0x8000,0,9);eq("queue_state1_admitted",alloc_entry(B,1),1);eq("queued_state1_retained",r8(EB+0x11),1);eq("allocated_consumes_free_head",r8(B+0x60),1);eq("entry_sets_channel2",r16(B+6),4);select_entry(B);eq("state1_is_not_selected",r8(B+0x62),255);eq("state1_only_sets_idle",r8(B+0x14)&0x40,0x40);eq("remove_queued_entry",remove_entry(B,0),1);eq("remove_last_clears_channel",r16(B+6),0);
 setup();strcpy(current,"start_entry");memset((void*)QB,0xa5,3*0x28);descriptor(2,1,2,1,0x8000,0,9);eq("queue_state2_admitted",alloc_entry(B,2),1);select_entry(B);eq("channel2_selected",r8(B+0x11),2);eq("entry_state_promoted3",r8(EB+0x11),3);eq("start_uses_function_offset",r64(QB+2*0x28),CODEB+0x100);eq("start_resets_phase",r8(QB+2*0x28+0x15),0);eq("start_preserves_scratch",r32(QB+2*0x28+0x18),0xa5a5a5a5U);eq("start_preserves_other_slot",r32(QB),0xa5a5a5a5U);
 setup();strcpy(current,"submit_issuer_gate");w8(A+2,1);w8(A+0x10,0);w8(B+2,2);eq("issuer_embodied_defers",submit(1,1,1,2,1),1);eq("deferral_depends_on_issuer",r8(EB+0x11),1);eq("target_not_started",r8(B+0x62),255);
 setup();w8(A+2,2);w8(B+2,1);strcpy(current,"submit_other_class");eq("issuer_control_starts",submit(1,1,1,2,1),1);eq("target_class_does_not_defer",r8(EB+0x11),3);eq("target_selected_one",r8(B+0x11),1);eq("submit_records_origin",r16(EB+6),0);eq("submit_records_resume_offset",r32(EB+0xc),10);eq("submit_pc_next_opcode",r64(Q),CODE+10);
}
static void request_program(unsigned opcode){
 uint8_t p[]={0x4f,1,0,0x4f,1,0,0x4f,1,0,(uint8_t)opcode,0x4f,99,0,0x36,0x19};script(p,sizeof p);
 const uint8_t target[]={0x4f,44,0,0x36,0x2d};memcpy((void*)(CODEB+0x100),target,sizeof target);
}
static void integrated_req(void){
 setup();strcpy(current,"REQSW");request_program(0x24);eq("reqsw_interpreter_return",interp(A,Q),1);eq("reqsw_kind4",r8(Q+0x14),4);eq("reqsw_continuation_pc",r64(Q),CODE+10);eq("reqsw_receipt_before_body",r8(A+0x61),0);eq("reqsw_target_not_yet_executed",r32(B+0x64),0);drive(A);eq("reqsw_consumes_receipt",r8(A+0x61),255);eq("reqsw_resumes_kind1",r8(Q+0x14),1);eq("reqsw_continues_script",r32(A+0x64),99);eq("reqsw_target_still_not_run",r32(B+0x64),0);
 setup();strcpy(current,"REQEW");request_program(0x27);eq("reqew_submit_return",interp(A,Q),1);eq("reqew_waits_kind4",r8(Q+0x14),4);eq("reqew_no_receipt_at_start",r8(A+0x61),255);drive(A);eq("reqew_stays_waiting",r8(Q+0x14),4);eq("reqew_no_early_following_code",r32(A+0x64),0);drive(B);eq("target_body_executes",r32(B+0x64),44);eq("target_RET_releases_channel",r16(B+6),0);eq("target_RET_posts_receipt",r8(A+0x61),0);drive(A);eq("reqew_continues_after_return",r32(A+0x64),99);eq("reqew_receipt_retired",r8(A+0x61),255);
}

static void queue_policies(void){
 setup();strcpy(current,"priority_fifo");descriptor(2,1,0,1,0x8000,0,0);alloc_entry(B,2);descriptor(2,1,2,2,0x8000,0,0);alloc_entry(B,2);descriptor(2,1,2,3,0x8000,0,0);alloc_entry(B,2);
 select_entry(B);eq("highest_channel_wins",r8(B+0x11),2);eq("fifo_first_on_high_channel",r8(B+0x62),1);eq("first_high_starts_func2",r64(QB+0x50),CODEB+0x200);remove_entry(B,1);select_entry(B);eq("fifo_successor_after_remove",r8(B+0x62),2);eq("second_high_starts_func3",r64(QB+0x50),CODEB+0x300);remove_entry(B,2);select_entry(B);eq("lower_channel_after_high_empty",r8(B+0x62),0);
 setup();strcpy(current,"skip_unstarted");descriptor(2,1,2,1,0x8000,0,0);alloc_entry(B,1);descriptor(2,1,0,2,0x8000,0,0);alloc_entry(B,2);select_entry(B);eq("unselectable_high_does_not_block_low",r8(B+0x62),1);eq("blocked_high_channel_still_active",r16(B+6),5);
 setup();strcpy(current,"admission_kinds");descriptor(0,1,1,1,0x8000,0,0);eq("kind0_empty_admits",alloc_entry(B,2),1);descriptor(0,1,1,2,0x8000,0,0);eq("kind0_occupied_refuses",alloc_entry(B,2),3);eq("rejected_candidate_back_on_free_list",r8(B+0x60),1);descriptor(2,1,1,1,0x8000,0,0);eq("kind2_same_id_admits",alloc_entry(B,2),1);descriptor(4,1,1,1,0x8000,0,0);eq("kind4_same_id_refuses",alloc_entry(B,2),3);descriptor(4,1,1,2,0x8000,0,0);eq("kind4_distinct_id_admits",alloc_entry(B,2),1);
 setup();strcpy(current,"bad_function_and_capacity");descriptor(2,1,1,8,0x8000,0,0);eq("bad_function_refuses_before_allocation",alloc_entry(B,2),3);eq("bad_function_preserves_free_head",r8(B+0x60),0);w8(B+0x60,0xff);descriptor(2,1,1,1,0x8000,0,0);eq("entry_capacity_refusal2",alloc_entry(B,2),2);
 setup();strcpy(current,"clamp_vs_bookkeeping");eq("high_channel_submit_admitted",submit(1,7,1,2,1),1);eq("high_channel_entry_clamps_to2",r8(EB+2),2);eq("clamped_active_bit_is2",r16(B+6),4);eq("submitted_mask_uses_unclamped7",r16(B+0x26),128);
 setup();strcpy(current,"promotion_and_same_actor");descriptor(2,1,0,1,0x8000,0,0);alloc_entry(B,1);descriptor(2,1,2,2,0x8000,0,0);alloc_entry(B,1);eq("different_actor_submission_admitted",submit(1,1,3,2,1),1);eq("promotion_existing_low_entry_to2",r8(EB+0x11),2);eq("promotion_selects_high_entry_to3",r8(EB+0x14+0x11),3);eq("new_lower_priority_entry_stays2",r8(EB+2*0x14+0x11),2);
 setup();strcpy(current,"same_actor");eq("same_actor_request_admitted",submit(0,1,1,2,1),1);eq("same_actor_not_immediately_started",r8(EA+0x11),2);eq("same_actor_selection_not_forced",r8(A+0x62),255);
 setup();strcpy(current,"issuer_counter_override");w8(A+2,1);w8(A+0x10,1);eq("issuer_nonzero_counter_uses_start_path",submit(1,1,1,2,1),1);eq("nonzero_counter_target_started",r8(EB+0x11),3);
}
static void receipt_boundaries(void){
 setup();strcpy(current,"receipt_capacity_start");w8(A+0x60,255);request_program(0x24);eq("startwait_success_without_receipt_capacity",interp(A,Q),1);eq("startwait_target_started_without_receipt",r8(EB+0x11),3);eq("startwait_no_receipt_allocated",r8(A+0x61),255);drive(A);eq("startwait_missing_receipt_still_waits",r8(Q+0x14),4);eq("startwait_missing_receipt_no_continuation",r32(A+0x64),0);
 setup();strcpy(current,"receipt_capacity_end");request_program(0x27);interp(A,Q);w8(A+0x60,255);drive(B);eq("endwait_target_finishes_without_receipt_capacity",r16(B+6),0);eq("endwait_receipt_failure_ignored",r8(A+0x61),255);drive(A);eq("endwait_missing_receipt_still_waits",r8(Q+0x14),4);
 setup();strcpy(current,"receipt_correlation");uint8_t c[]={0x4f,71,0,0x36,0x19};script(c,sizeof c);w8(Q+0x14,4);descriptor(2,4,1,0,0x8000,0,0);eq("mismatched_channel_notice_inserted",alloc_entry(A,1),1);drive(A);eq("wrong_channel_does_not_resume",r8(Q+0x14),4);w8(EA+2,0);w32(EA+0xc,1);drive(A);eq("wrong_resume_offset_does_not_resume",r8(Q+0x14),4);w32(EA+0xc,0);drive(A);eq("matching_pair_resumes",r32(A+0x64),71);eq("matching_notice_recycled",r8(A+0x61),255);
 setup();strcpy(current,"wait_submission_refusal");request_program(0x27);w8(B+0x60,255);eq("no_target_entry_capacity_returns",interp(A,Q),1);eq("refused_submit_does_not_arm_wait4",r8(Q+0x14),1);eq("refused_submit_continues_bytecode",r32(A+0x64),99);
}
static void wait_direct_controls(void){
 setup();strcpy(current,"kind3_entry");uint8_t p[]={0x4f,81,0,0x36,0x19};script(p,sizeof p);descriptor(2,1,1,1,0x8000,0,0);alloc_entry(B,1);w8(Q+0x14,3);w32(Q+0x18,B);w16(Q+0x20,1);drive(A);eq("kind3_sees_queued_state1_entry",r8(Q+0x14),3);eq("kind3_no_script_while_entry_exists",r32(A+0x64),0);remove_entry(B,0);drive(A);eq("kind3_absence_resumes_same_drive",r32(A+0x64),81);eq("kind3_sets_completion_marker",r8(Q+0x27),1);eq("kind3_becomes_runnable",r8(Q+0x14),1);
 setup();strcpy(current,"kind6_channel");script(p,sizeof p);w8(Q+0x14,6);w32(Q+0x18,B);w8(Q+0x26,2);w16(B+6,4);drive(A);eq("kind6_waits_on_channel_bit",r8(Q+0x14),6);w16(B+6,2);drive(A);eq("kind6_ignores_other_channel",r32(A+0x64),81);eq("kind6_sets_marker",r8(Q+0x27),1);
 setup();strcpy(current,"kind2_runnable_alias");script(p,sizeof p);w8(Q+0x14,2);drive(A);eq("kind2_dispatches_interpreter",r32(A+0x64),81);eq("kind2_not_automatically_retyped",r8(Q+0x14),2);
 setup();strcpy(current,"kind0_no_run");script(p,sizeof p);w8(Q+0x14,0);drive(A);eq("kind0_no_execution",r32(A+0x64),0);eq("kind0_marks_serviced",r8(Q+0x16),1);
 setup();strcpy(current,"kind8_no_run");script(p,sizeof p);w8(Q+0x14,8);drive(A);eq("kind8_no_execution",r32(A+0x64),0);eq("kind8_marks_serviced",r8(Q+0x16),1);
}
static void list_wait_controls(void){
 setup();strcpy(current,"kind7_monotonic_cursor");uint8_t p[]={0x4f,82,0,0x36,0x19};script(p,sizeof p);w8(Q+0x14,7);w32(Q+0x1c,WL);w8(Q+0x26,1);w32(WL,2);w16(WL+4,0);w16(WL+8,1);w16(A+6,0);w16(B+6,2);drive(A);eq("kind7_cursor_stops_at_active_second_actor",r16(Q+0x22),1);eq("kind7_stays_waiting",r8(Q+0x14),7);w16(A+6,2);w16(B+6,0);drive(A);eq("kind7_does_not_recheck_passed_actor",r32(A+0x64),82);eq("kind7_cursor_reaches_end",r16(Q+0x22),2);eq("kind7_sets_marker",r8(Q+0x27),1);
 setup();strcpy(current,"kind5_resource_cursor");script(p,sizeof p);descriptor(2,1,1,2,0x8000,0,0);alloc_entry(B,1);w8(Q+0x14,5);w8(Q+0x27,0x7e);w32(Q+0x1c,WL);w32(WL,2);w16(WL+4,0);w16(WL+6,2);w16(WL+8,1);w16(WL+10,2);drive(A);eq("kind5_cursor_advances_past_absent",r16(Q+0x22),1);eq("kind5_sees_queued_matching_entry",r8(Q+0x14),5);remove_entry(B,0);drive(A);eq("kind5_continues_same_invocation",r32(A+0x64),82);eq("kind5_does_not_write_marker",r8(Q+0x27),0x7e);eq("kind5_cursor_exhausted",r16(Q+0x22),2);
 setup();strcpy(current,"empty_wait_list");script(p,sizeof p);w8(Q+0x14,7);w32(Q+0x1c,0);drive(A);eq("null_list_is_complete",r32(A+0x64),82);
 setup();strcpy(current,"serviced_bit_defer");script(p,sizeof p);w32(0x1dfe0c0,0);w32(0x1f82e38,1);w8(Q+0x16,1);drive(A);eq("serviced_gate_skips_once",r32(A+0x64),0);eq("serviced_gate_clears_marker",r8(Q+0x16),0);drive(A);eq("serviced_gate_later_invocation_executes",r32(A+0x64),82);
}


static void bytecode_entry_wait(void){
 setup();strcpy(current,"entry_wait_producer");descriptor(2,1,1,2,0x8000,0,0);alloc_entry(B,1);const uint8_t p[]={0x4f,1,0,0x4f,2,0,0x32,0x4f,83,0,0x36,0x19};script(p,sizeof p);
 eq("opcode32_returns_after_arming",interp(A,Q),1);eq("opcode32_kind3",r8(Q+0x14),3);eq("opcode32_saves_encoded_target",r32(Q+0x18),B);eq("opcode32_saves_resource_id",r16(Q+0x20),2);eq("opcode32_saves_next_pc",r64(Q),CODE+7);eq("opcode32_no_early_continuation",r32(A+0x64),0);drive(A);eq("opcode32_still_waits_with_entry",r32(A+0x64),0);remove_entry(B,0);drive(A);eq("opcode32_resumes_after_removal",r32(A+0x64),83);
 setup();strcpy(current,"entry_wait_absent");script(p,sizeof p);eq("opcode32_absent_returns",interp(A,Q),1);eq("opcode32_absent_does_not_arm",r8(Q+0x14),1);eq("opcode32_absent_continues",r32(A+0x64),83);
 setup();strcpy(current,"request_guard");w8(A+0x10,2);w8(B+0x10,3);eq("reserved_id_bit_rejects_before_lookup",submit(1,1,0x8000,2,1),0);eq("early_reject_leaves_target_counter",r8(B+0x10),3);eq("early_reject_leaves_issuer_counter",r8(A+0x10),2);
 setup();strcpy(current,"rejected_target_counter");w8(B+0x60,255);w8(B+0x10,3);eq("failed_submission_returns_capacity2",submit(1,1,1,2,1),2);eq("failed_submission_decrements_target_counter",r8(B+0x10),2);eq("failed_submission_still_updates_saved_pc",r64(Q),CODE+10);
}

static void apply_variant(void){if(!mutant)return;
if(!strcmp(mutant,"read_target_instead_of_issuer")){const uint8_t before[]={0x41,0x80,0x7f,0x02,0x01},after[]={0x40,0x80,0x7b,0x02,0x01};if(memcmp((void*)0x2689f0,before,sizeof before)){fputs("variant preimage mismatch\n",stderr);exit(2);}memcpy((void*)0x2689f0,after,sizeof after);return;}
if(!strcmp(mutant,"drop_start_notification")){const uint8_t before[]={0xe8,0x8c,0xfe,0xff,0xff},after[]={0x90,0x90,0x90,0x90,0x90};if(memcmp((void*)0x3dbe5f,before,sizeof before)){fputs("variant preimage mismatch\n",stderr);exit(2);}memcpy((void*)0x3dbe5f,after,sizeof after);return;}
if(!strcmp(mutant,"drop_return_notification")){const uint8_t before[]={0xe8,0x4e,0x0d,0x00,0x00},after[]={0x90,0x90,0x90,0x90,0x90};if(memcmp((void*)0x3db37d,before,sizeof before)){fputs("variant preimage mismatch\n",stderr);exit(2);}memcpy((void*)0x3db37d,after,sizeof after);return;}
if(!strcmp(mutant,"reverse_entry_wait_polarity")){const uint8_t before[]={0x0f,0x85},after[]={0x0f,0x84};if(memcmp((void*)0x25e045,before,sizeof before)){fputs("variant preimage mismatch\n",stderr);exit(2);}memcpy((void*)0x25e045,after,sizeof after);return;}
if(!strcmp(mutant,"reverse_notification_wait_polarity")){const uint8_t before[]={0x74},after[]={0x75};if(memcmp((void*)0x25e0a9,before,sizeof before)){fputs("variant preimage mismatch\n",stderr);exit(2);}memcpy((void*)0x25e0a9,after,sizeof after);return;}
if(!strcmp(mutant,"decrement_list_cursor")){const uint8_t before[]={0x66,0xff,0x43,0x0a},after[]={0x66,0xff,0x4b,0x0a};if(memcmp((void*)0x267471,before,sizeof before)){fputs("variant preimage mismatch\n",stderr);exit(2);}memcpy((void*)0x267471,after,sizeof after);return;}
if(!strcmp(mutant,"erase_scratch_in_core_reset")){const uint8_t before[]={0x88,0x41,0x16},after[]={0x88,0x41,0x18};if(memcmp((void*)0x25d470,before,sizeof before)){fputs("variant preimage mismatch\n",stderr);exit(2);}memcpy((void*)0x25d470,after,sizeof after);return;}
if(!strcmp(mutant,"omit_channel_completion_marker")){const uint8_t before[]={0x01},after[]={0x00};if(memcmp((void*)0x25e07d,before,sizeof before)){fputs("variant preimage mismatch\n",stderr);exit(2);}memcpy((void*)0x25e07d,after,sizeof after);return;}
fputs("unknown variant\n",stderr);exit(2);}
int main(int argc,char**argv){if(argc<2||argc>3)return 2;if(argc==3)mutant=argv[2];setvbuf(stdout,NULL,_IONBF,0);struct rlimit l={0,0};setrlimit(RLIMIT_CORE,&l);load(argv[1]);apply_variant();printf("{\"cases\":[\n");basic_arming();integrated_req();queue_policies();receipt_boundaries();wait_direct_controls();list_wait_controls();bytecode_entry_wait();printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);return failures?1:0;}
