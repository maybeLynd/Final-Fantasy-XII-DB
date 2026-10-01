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
static int lifecycle(uintptr_t a,uintptr_t q,uint32_t verb){return ((int(ABI*)(uintptr_t,uintptr_t,uintptr_t,uint32_t,uintptr_t))0x2621d0)(M,a,STACK,verb,q);}
static void smoke(void){
 strcpy(current,"literal");reset();uint8_t p[]={0x4f,0x34,0x12,0x36,0x19};script(p,sizeof p);eq("literal_return",interp(A,Q),1);eq("literal_to_i0",r32(A+0x64),0x1234);eq("literal_pc",r64(Q),CODE+5);eq("literal_stack_empty",r32(STACK),0);
 strcpy(current,"wait");reset();uint8_t w[]={0x4f,2,0,0x58,0,0,0x36,0x4f,99,0,0x37,0x19};script(w,sizeof w);
 for(unsigned i=0;i<3;i++){char n[80];int ret=interp(A,Q);snprintf(n,sizeof n,"wait%u_return",i);eq(n,ret,i<2?0:1);snprintf(n,sizeof n,"wait%u_pc",i);eq(n,r64(Q),i<2?CODE+3:CODE+sizeof w);snprintf(n,sizeof n,"wait%u_phase",i);eq(n,r8(Q+0x15),i<2?1:0);snprintf(n,sizeof n,"wait%u_counter",i);eq(n,(int32_t)r32(Q+0x18),1-(int)i);}
 eq("wait_then_continues_i1",r32(A+0x68),99);eq("wait_implicit_zero",r32(A+0x64),0);
 strcpy(current,"empty");reset();uint8_t e[]={0x58,0xb0,3,0x36,0x19};script(e,sizeof e);eq("empty_return",interp(A,Q),1);eq("empty_zero",r32(A+0x64),0);
 strcpy(current,"real_result");reset();w32(0x2164480+0x1044,73);uint8_t a[]={0x58,0x90,0,0x36,0x19};script(a,sizeof a);eq("real_map_rc",interp(A,Q),1);eq("real_map_value",r32(A+0x64),73);
 // Standalone phase2 path with original callback and real result writer.
 strcpy(current,"standalone");reset();w8(Q+0x15,2);w32(0x2164480+0x1044,42);eq("direct_result_rc",lifecycle(A,Q,0x90),0);eq("direct_result_count",r32(STACK),1);eq("direct_result_value",r32(STACK+0x184),42);
}
static void gates_and_arithmetic(void){
 reset();strcpy(current,"entry_gate");uint8_t p[]={0x4f,7,0,0x36,0x19};script(p,sizeof p);w32(STACK,5);w8(A+0x14,0x70);w32(A+0x64,0x5555);eq("halt_gate_return",interp(A,Q),1);eq("halt_gate_preserves_pc",r64(Q),CODE);eq("entry_clears_shared_depth_even_blocked",r32(STACK),0);eq("blocked_preserves_actor_i0",r32(A+0x64),0x5555);eq("entry_does_not_erase_value_storage",r32(STACK+0x184),0xa5a5a5a5U);
 reset();strcpy(current,"arithmetic");uint8_t ar[]={0x4f,7,0,0x4f,5,0,0x12,0x36,0x19};script(ar,sizeof ar);eq("integer_add_rc",interp(A,Q),1);eq("integer_add_value",r32(A+0x64),12);
 reset();uint8_t neg[]={0x4f,0xfd,0xff,0x36,0x19};script(neg,sizeof neg);interp(A,Q);eq("signed_immediate16",(int32_t)r32(A+0x64),-3);
 reset();w32(FPOOL+4,0x40700000);uint8_t fp[]={0x50,0,0,0x3a,0x42,0x36,0x19};script(fp,sizeof fp);interp(A,Q);eq("float_register_preserves_bits",r32(A+0x74),0x40700000);eq("float_to_int_truncates",r32(A+0x64),3);
 reset();w32(FPOOL+4,0x40700000);uint8_t mix[]={0x4f,2,0,0x50,0,0,0x12,0x3a,0x19};script(mix,sizeof mix);interp(A,Q);eq("mixed_add_is_float",r32(A+0x74),0x40b80000);
 reset();w32(IPOOL+4,0x7fffffff);uint8_t ov[]={0x4e,0,0,0x4f,1,0,0x12,0x36,0x19};script(ov,sizeof ov);interp(A,Q);eq("integer_add_wraps32",r32(A+0x64),0x80000000U);
 reset();strcpy(current,"zero_length_nop");uint8_t zero[]={0x00,0x4f,7,0,0x36,0x19};script(zero,sizeof zero);eq("zero_length_nop_budget_returns",interp(A,Q),1);eq("zero_length_nop_does_not_advance",r64(Q),CODE);eq("zero_length_nop_no_following_execution",r32(A+0x64),0);
 reset();strcpy(current,"zero_length_tag");w8(CODE,1);eq("zero_length_marker_returns",interp(A,Q),1);eq("zero_length_marker_stays_put",r64(Q),CODE);
 reset();strcpy(current,"syshalt");w8(CODE,3);eq("syshalt_returns",interp(A,Q),1);eq("syshalt_rewinds_current_pc",r64(Q),CODE);eq("syshalt_sets_actor40",r8(A+0x14)&0x40,0x40);
}
static void branches_and_stacks(void){
 reset();strcpy(current,"label_jump");w32(LABELS+4,8);uint8_t j[]={0x51,0,0,0x4f,99,0,0x36,0x19,0x4f,42,0,0x36,0x19};script(j,sizeof j);interp(A,Q);eq("jump_uses_label_offset",r32(A+0x64),42);eq("jump_lands_exactly_not_plus3",r64(Q),CODE+sizeof j);
 reset();strcpy(current,"self_jump_budget");uint8_t self[]={0x51,0,0};script(self,sizeof self);eq("self_jump_budget_returns",interp(A,Q),1);eq("self_jump_preserves_pc",r64(Q),CODE);
 reset();strcpy(current,"branch_compare");w32(Q+0xc,7);w32(LABELS+4,11);uint8_t b[]={0x4f,7,0,0x52,0,0,0x4f,99,0,0x36,0x19,0x4f,42,0,0x36,0x19};script(b,sizeof b);interp(A,Q);eq("conditional_equal_taken",r32(A+0x64),42);
 reset();w32(Q+0xc,8);w32(LABELS+4,11);script(b,sizeof b);interp(A,Q);eq("conditional_unequal_falls_through",r32(A+0x64),99);
 reset();strcpy(current,"same_wrapper_pointer");uint8_t own[]={0x4f,0x34,0x12,0x1c,0x19};script(own,sizeof own);interp(A,Q);eq("request_accumulator_persists",r32(Q+0x10),0x1234);uint8_t read[]={0x1b,0x36,0x19};script(read,sizeof read);interp(A,Q);eq("request_accumulator_survives_next_entry",r32(A+0x64),0x1234);
 reset();strcpy(current,"underflow_and_state");uint8_t pop[]={0x36,0x19};script(pop,sizeof pop);w32(STACK,1);w8(STACK+4,1);w32(STACK+0x184,123);interp(A,Q);eq("prior_invocation_stack_not_restored",r32(A+0x64),0);eq("underflow_depth_stays0",r32(STACK),0);
 reset();strcpy(current,"marker_stack_flush");uint8_t drain[]={0x4f,7,0,0x19,0x36,0x19};script(drain,sizeof drain);interp(A,Q);eq("yield_discards_nonempty_stack",r32(A+0x64),0);eq("yield_stack_drain_continues_one_opcode",r64(Q),CODE+5);
}
static void real_verbs(void){
 reset();strcpy(current,"float_result");w8(A+3,0x20);w64(A+0xb8,H+0x90000);w32(H+0x90000,0x40d00000);uint8_t x[]={0x58,0x6d,0,0x3a,0x19};script(x,sizeof x);interp(A,Q);eq("real_getx_float_result",r32(A+0x74),0x40d00000);eq("float_completion_phase_resets",r8(Q+0x15),0);
 reset();strcpy(current,"target_rebind");uint8_t act[]={0x4f,1,0,0x59,0x72,0,0x36,0x19};script(act,sizeof act);interp(A,Q);eq("callact_uses_other_actor",r32(A+0x64),1);eq("callact_saves_target_ordinal",r32(Q+8),1);eq("callact_result_written_to_issuer_not_target",r32(QB+0xc),0);
 reset();strcpy(current,"callactpopa");uint8_t actp[]={0x4f,1,0,0x5e,0x72,0,0x19};script(actp,sizeof actp);interp(A,Q);eq("callactpopa_preserves_popped_target",r32(Q+8),1);eq("callactpopa_result_uses_target",r32(Q+0x10),1);eq("callactpopa_clears_stack_by_accumulator",r32(STACK),0);
 reset();strcpy(current,"callpopa");w32(0x2164480+0x1044,91);uint8_t ca[]={0x5d,0x90,0,0x19};script(ca,sizeof ca);interp(A,Q);eq("callpopa_accumulator",r32(Q+0x10),91);eq("callpopa_no_stack_result_left",r32(STACK),0);
 reset();strcpy(current,"phase_resume_target");uint8_t aw[]={0x4f,5,0,0x4f,1,0,0x59,0,0,0x36,0x19};script(aw,sizeof aw);eq("actor_wait_first_busy",interp(A,Q),0);eq("actor_wait_first_counter",r32(Q+0x18),4);eq("actor_wait_pc_stays_at_call",r64(Q),CODE+6);eq("actor_wait_remembers_target",r32(Q+8),1);
 // Replace ordinal1 mapping without retaining old target pointer.
 uintptr_t c=H+0xa000;w16(c,77);w8(c+0x15,1);w64(LIST+16,c);w8(0x2099011+0x288,1);
 eq("actor_wait_resume_busy",interp(A,Q),0);eq("actor_wait_resolves_target_again",r32(Q+0x18),0);eq("actor_wait_no_begin_reexecution",r8(Q+0x15),1);eq("actor_wait_third_completion",interp(A,Q),1);eq("actor_wait_original_argument_not_repopulated",(int32_t)r32(Q+0x18),-1);w8(0x2099011+0x288,0);
 reset();strcpy(current,"two_actor_resume");uint8_t wait[]={0x4f,2,0,0x58,0,0,0x36,0x19};script(wait,sizeof wait);interp(A,Q);w32(A+0x64,71);uint8_t other[]={0x4f,22,0,0x36,0x19};memcpy((void*)CODEB,other,sizeof other);interp(B,QB);eq("other_actor_register_is_independent",r32(B+0x64),22);eq("first_actor_register_survives_peer",r32(A+0x64),71);eq("first_actor_phase_survives_peer",r8(Q+0x15),1);eq("first_actor_scratch_survives_peer",r32(Q+0x18),1);eq("first_actor_resume_busy",interp(A,Q),0);eq("first_actor_resume_completes",interp(A,Q),1);
 reset();strcpy(current,"zero_wait");uint8_t wz[]={0x4f,0,0,0x58,0,0,0x36,0x19};script(wz,sizeof wz);eq("zero_wait_completes_same_invocation",interp(A,Q),1);eq("zero_wait_counter_minus1",(int32_t)r32(Q+0x18),-1);eq("zero_wait_pc_advances",r64(Q),CODE+sizeof wz);
 reset();strcpy(current,"empty_catalog_verbs");unsigned ids[]={0x330,0x356,0x3b0,0xfff};for(unsigned k=0;k<4;k++){uint8_t e[]={0x58,(uint8_t)ids[k],(uint8_t)(ids[k]>>8),0x36,0x19};script(e,sizeof e);char n[80];snprintf(n,sizeof n,"empty_or_oob_%x_return",ids[k]);eq(n,interp(A,Q),1);snprintf(n,sizeof n,"empty_or_oob_%x_zero",ids[k]);eq(n,r32(A+0x64),0);}
 reset();strcpy(current,"full_result_stack");w32(STACK,63);w32(0x2164480+0x1044,83);eq("full_stack_command_still_finishes",lifecycle(A,Q,0x90),0);eq("full_stack_depth_unchanged",r32(STACK),63);eq("full_stack_return_slot_still_written",r32(Q+0xc),83);eq("full_stack_phase_resets",r8(Q+0x15),0);eq("full_stack_outside_guard_preserved",r32(STACK+0x184+63*4),0xa5a5a5a5U);
}
static void full_actor_driver(void){
 reset();strcpy(current,"full_actor_driver");w32(0x1dfe40c,5);w8(0x2098e20,0);memset((void*)0x215f200,0,8*0x68);w32(0x1dfe0c0,1);w32(0x1f82e38,0);w32(0x22ca400,0);w32(A+0x108,99);uint8_t w[]={0x4f,2,0,0x58,0,0,0x36,0x4f,66,0,0x37,0x19};script(w,sizeof w);
 for(unsigned i=0;i<3;i++){((void(ABI*)(uintptr_t,uintptr_t))0x25df00)(M,A);char n[80];snprintf(n,sizeof n,"outer%u_pc",i);eq(n,r64(Q),i<2?CODE+3:CODE+sizeof w);snprintf(n,sizeof n,"outer%u_phase",i);eq(n,r8(Q+0x15),i<2?1:0);}
 eq("outer_continues_after_wait",r32(A+0x68),66);eq("outer_active_actor_global_cleared",r64(0x2099d80),0);eq("outer_resets_actor108",r32(A+0x108),0);
}

static void boundary_controls(void){
 reset();strcpy(current,"phase_is_not_actor_control");w8(Q+0x15,1);w32(Q+0x18,3);eq("phase1_alone_does_not_force_wait_end",lifecycle(A,Q,0),1);eq("phase1_and_zero_actor_control_counts_down",r32(Q+0x18),2);w8(0x2099011,1);eq("actor_control_can_shorten_wait_without_phase_change",lifecycle(A,Q,0),1);eq("actor_control_forces_scratch_zero",r32(Q+0x18),0);eq("request_phase_still_running_after_control",r8(Q+0x15),1);
 reset();strcpy(current,"marker_operand_read");w8(CODE+0xfff,0x47);w64(Q,CODE+0xfff);pid_t child=fork();if(child<0)exit(2);if(child==0){expected_fault_pc=0x25e5af;expected_fault_address=CODE+0x1001;if(mprotect((void*)(CODE+0x1000),0x1000,PROT_NONE))_exit(2);interp(A,Q);_exit(75);}int st=0;if(waitpid(child,&st,0)!=child)exit(2);eq("length1_marker_still_reads_second_operand_byte",WIFEXITED(st)?WEXITSTATUS(st):-1,73);
 reset();w8(CODE+0xfff,0x19);w64(Q,CODE+0xfff);if(mprotect((void*)(CODE+0x1000),0x1000,PROT_NONE))exit(2);eq("non_predecode_marker_at_page_end_returns",interp(A,Q),1);eq("non_predecode_marker_advances_to_boundary",r64(Q),CODE+0x1000);if(mprotect((void*)(CODE+0x1000),0x1000,PROT_READ|PROT_WRITE))exit(2);

 reset();strcpy(current,"budget_advance");memset((void*)CODE,4,66000);w8(CODE+66000,0x19);eq("instruction_budget_returns",interp(A,Q),1);eq("instruction_budget_65536_advance",r64(Q),CODE+65536);eq("instruction_budget_next_invocation_continues",interp(A,Q),1);eq("instruction_budget_final_marker",r64(Q),CODE+66001);
 reset();strcpy(current,"busy_extra_operand");uint8_t extra[]={0x4f,99,0,0x4f,2,0,0x58,0,0,0x36,0x19};script(extra,sizeof extra);eq("extra_operand_wait_returns_busy",interp(A,Q),0);eq("extra_operand_causes_second_poll_same_invocation",r32(Q+0x18),0);eq("extra_operand_pc_still_call",r64(Q),CODE+6);eq("extra_operand_stack_discarded",r32(STACK),0);eq("extra_operand_next_call_finishes",interp(A,Q),1);
 reset();strcpy(current,"empty_direct");w32(Q+0xc,0x12345678);eq("absent_callbacks_complete",lifecycle(A,Q,0x3b0),0);eq("absent_callbacks_append_one_zero",r32(STACK),1);eq("absent_callbacks_value_zero",r32(STACK+0x184),0);eq("absent_callbacks_clear_scratch_result",r32(Q+0xc),0);eq("absent_callbacks_tag_int",r8(STACK+4),1);
 reset();strcpy(current,"float_direct");w8(A+3,0x20);w64(A+0xb8,H+0x90000);w32(H+0x90000,0xc0700000);eq("float_direct_complete",lifecycle(A,Q,0x6d),0);eq("float_direct_stack_tag",r8(STACK+4),2);eq("float_direct_bits",r32(STACK+0x184),0xc0700000);eq("float_direct_phase_zero",r8(Q+0x15),0);
 reset();strcpy(current,"result_at62");w32(STACK,62);w32(0x2164480+0x1044,17);lifecycle(A,Q,0x90);eq("last_admitted_result_depth63",r32(STACK),63);eq("last_admitted_result_at62",r32(STACK+0x184+62*4),17);
 reset();strcpy(current,"wait_return_to_accumulator");uint8_t pw[]={0x4f,1,0,0x5d,0,0,0x4f,23,0,0x36,0x19};script(pw,sizeof pw);eq("callpopa_wait_busy_rc",interp(A,Q),0);eq("callpopa_wait_busy_pc",r64(Q),CODE+3);eq("callpopa_wait_complete_rc",interp(A,Q),1);eq("callpopa_wait_zero_accumulator",r32(Q+0x10),0);eq("callpopa_wait_following_exec",r32(A+0x64),23);
 reset();strcpy(current,"scaled_wait");w32(0x22c7f84,0);w32(0x1dfe40c,5);w8(0x2098e20,0);memset((void*)0x215f200,0,8*0x68);w32(0x1dfe0c0,0);w32(0x1f82e38,1);w32(0x1dfe0b4,2);uint8_t sc[]={0x4f,3,0,0x58,0,0,0x36,0x19};script(sc,sizeof sc);eq("wait_scaling_original_predicates_busy",interp(A,Q),0);eq("wait_scaling_3_times2_minus_first_poll",r32(Q+0x18),5);
 reset();strcpy(current,"selected_request1");w32(0x1dfe40c,5);w8(0x2098e20,0);memset((void*)0x215f200,0,8*0x68);w32(0x1dfe0c0,1);w32(0x1f82e38,0);w8(A+0x11,1);w64(Q+0x28,CODE);w8(Q+0x28+0x14,1);w32(Q+0xc,0x87654321);w32(0x2164480+0x1044,38);uint8_t mr[]={0x58,0x90,0,0x36,0x19};memcpy((void*)CODE,mr,sizeof mr);((void(ABI*)(uintptr_t,uintptr_t))0x25df00)(M,A);eq("driver_selects_40byte_request_stride",r64(Q+0x28),CODE+sizeof mr);eq("result_writer_uses_selected_request",r32(Q+0x28+0xc),38);eq("other_request_result_preserved",r32(Q+0xc),0x87654321);eq("selected_request_continues_into_actor_register",r32(A+0x64),38);
}

/* Mutations affect this process's private mapped image only. Each byte preimage is checked. */
static void apply_variant(void){if(!mutant)return;
if(!strcmp(mutant,"omit_entry_depth_reset")){const uint8_t before[]={ 0x44,0x89,0x1d,0xe1,0xb5,0xe3,0x01 },after[]={ 0x90,0x90,0x90,0x90,0x90,0x90,0x90 };if(memcmp((void*)0x25e4d8,before,sizeof before)){fprintf(stderr,"variant preimage mismatch\n");exit(2);}memcpy((void*)0x25e4d8,after,sizeof after);return;}
if(!strcmp(mutant,"repeat_begin_on_phase1")){const uint8_t before[]={ 0x8a,0x00,0x00,0x00 },after[]={ 0x5a,0x00,0x00,0x00 };if(memcmp((void*)0x262251,before,sizeof before)){fprintf(stderr,"variant preimage mismatch\n");exit(2);}memcpy((void*)0x262251,after,sizeof after);return;}
if(!strcmp(mutant,"omit_busy_pc_rewind")){const uint8_t before[]={ 0x4c,0x2b,0xf1 },after[]={ 0x90,0x90,0x90 };if(memcmp((void*)0x2619e4,before,sizeof before)){fprintf(stderr,"variant preimage mismatch\n");exit(2);}memcpy((void*)0x2619e4,after,sizeof after);return;}
if(!strcmp(mutant,"keep_phase_one_after_completion")){const uint8_t before[]={ 0x00 },after[]={ 0x01 };if(memcmp((void*)0x262385,before,sizeof before)){fprintf(stderr,"variant preimage mismatch\n");exit(2);}memcpy((void*)0x262385,after,sizeof after);return;}
if(!strcmp(mutant,"mislabel_float_result_as_integer")){const uint8_t before[]={ 0x03 },after[]={ 0x02 };if(memcmp((void*)0x26b4da,before,sizeof before)){fprintf(stderr,"variant preimage mismatch\n");exit(2);}memcpy((void*)0x26b4da,after,sizeof after);return;}
if(!strcmp(mutant,"force_issuer_instead_of_target")){const uint8_t before[]={ 0x74 },after[]={ 0xeb };if(memcmp((void*)0x262236,before,sizeof before)){fprintf(stderr,"variant preimage mismatch\n");exit(2);}memcpy((void*)0x262236,after,sizeof after);return;}
if(!strcmp(mutant,"omit_stop_depth_discard")){const uint8_t before[]={ 0x44,0x89,0x1d,0x23,0xb5,0xe3,0x01 },after[]={ 0x90,0x90,0x90,0x90,0x90,0x90,0x90 };if(memcmp((void*)0x25e596,before,sizeof before)){fprintf(stderr,"variant preimage mismatch\n");exit(2);}memcpy((void*)0x25e596,after,sizeof after);return;}
if(!strcmp(mutant,"shorten_instruction_budget")){const uint8_t before[]={ 0x00,0x00,0x01,0x00 },after[]={ 0x10,0x00,0x00,0x00 };if(memcmp((void*)0x25e4fb,before,sizeof before)){fprintf(stderr,"variant preimage mismatch\n");exit(2);}memcpy((void*)0x25e4fb,after,sizeof after);return;}
if(!strcmp(mutant,"callactpopa_uses_issuer")){const uint8_t before[]={ 0xaa },after[]={ 0xa6 };if(memcmp((void*)0x261b14,before,sizeof before)){fprintf(stderr,"variant preimage mismatch\n");exit(2);}memcpy((void*)0x261b14,after,sizeof after);return;}
if(!strcmp(mutant,"omit_default_zero_result")){const uint8_t before[]={ 0x48,0x63,0x0b,0x83,0xf9 },after[]={ 0xe9,0x1d,0x00,0x00,0x00 };if(memcmp((void*)0x262360,before,sizeof before)){fprintf(stderr,"variant preimage mismatch\n");exit(2);}memcpy((void*)0x262360,after,sizeof after);return;}
fprintf(stderr,"unknown variant\n");exit(2);}

int main(int argc,char**argv){if(argc<2)return 2;setvbuf(stdout,NULL,_IONBF,0);struct rlimit lim={0,0};setrlimit(RLIMIT_CORE,&lim);if(argc>2)mutant=argv[2];load(argv[1]);apply_variant();printf("{\"cases\":[\n");smoke();gates_and_arithmetic();branches_and_stacks();real_verbs();full_actor_driver();boundary_controls();printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);return failures?1:0;}
