#define _GNU_SOURCE
/* SECTION-03. Original x64 instructions over synthetic state; no game session,
 * no scripted application callees. Never writes the supplied executable.
 * Linux x86-64, GCC-compatible compiler; expected-fault cases run in children. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <signal.h>
#include <unistd.h>
#define ABI __attribute__((ms_abi))
#define HEAP ((uintptr_t)0x40000000)
#define HEAP_SIZE 0x400000
#define FRAME (HEAP+0x20000)
#define UNITS (HEAP+0x100000)
#define U16T (HEAP+0x300000)
#define OBJD (HEAP+0x310000)
#define ROW70 (HEAP+0x320000)
#define ROW78 (HEAP+0x321000)
#define GFRAME ((uintptr_t)0x2ebf190)
#define GUNITS ((uintptr_t)0x208e688)
#define GCNT ((uintptr_t)0x208e6a0)
#define GFLAG ((uintptr_t)0x2add100)
#define GBOUND ((uintptr_t)0x2ebf130)
#define GINDEX ((uintptr_t)0x21654c4)
#define GLP ((uintptr_t)0x209a2a9)
static unsigned checks,failed;static const char *mutant;
static uint8_t r8(uintptr_t p){uint8_t x;memcpy(&x,(void*)p,1);return x;}
static uint16_t r16(uintptr_t p){uint16_t x;memcpy(&x,(void*)p,2);return x;}
static uint32_t r32(uintptr_t p){uint32_t x;memcpy(&x,(void*)p,4);return x;}
static uint64_t r64(uintptr_t p){uint64_t x;memcpy(&x,(void*)p,8);return x;}
static void w8(uintptr_t p,uint8_t x){memcpy((void*)p,&x,1);}
static void w16(uintptr_t p,uint16_t x){memcpy((void*)p,&x,2);}
static void w32(uintptr_t p,uint32_t x){memcpy((void*)p,&x,4);}
static void w64(uintptr_t p,uint64_t x){memcpy((void*)p,&x,8);}
static uintptr_t rec(unsigned i){return FRAME+8+(uintptr_t)i*0x1c8;}
static uintptr_t unit(unsigned i){return UNITS+(uintptr_t)i*0xf50;}
typedef int32_t (ABI *Reward)(uintptr_t,uintptr_t);
static int32_t xp(uintptr_t r){return ((Reward)0x2f8bb0)(r,unit(4));}
static int32_t lp(uintptr_t r){return ((Reward)0x2f90c0)(r,unit(4));}
static void report(const char *name,int ok,int64_t actual,int64_t expected){
 printf("%s{\"name\":\"%s\",\"pass\":%s,\"observed\":%lld,\"expected\":%lld}",checks?",\n":"",name,ok?"true":"false",(long long)actual,(long long)expected);
 checks++;failed+=!ok;
 if(!ok&&mutant){printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failed);exit(1);}
}
static void eq(const char *name,int64_t actual,int64_t expected){report(name,actual==expected,actual,expected);}
static void reset(unsigned n){
 memset((void*)HEAP,0,HEAP_SIZE);
 w64(GFRAME,FRAME);w64(GUNITS,UNITS);w32(GCNT,5);w64(GFLAG,U16T);w64(GBOUND,OBJD);w32(GINDEX,0);w8(GLP,0);
 w32(U16T+4,0);w32(OBJD+4,40);
 for(unsigned t=0;t<5;t++)for(unsigned i=0;i<9;i++)w16(FRAME+0x5a48+t*18+i*2,0xffff);
 for(unsigned i=0;i<4;i++){w64(unit(i)+0x698,rec(i));w16(rec(i)+4,(uint16_t)i);if(i<n)w16(FRAME+0x5a5a+i*2,(uint16_t)i);}
 w16(FRAME+0x5a48,0);w8(FRAME+0x5ad5,0);w32(FRAME+0x5b04,0);
 w64(unit(4)+0x698,rec(4));w16(rec(4)+4,0x100);w8(rec(4)+0x1c2,9);w8(rec(4)+0x88,1);
 w64(unit(4)+0xe70,ROW70);w64(unit(4)+0xe78,ROW78);w32(ROW70+0x34,3);w32(ROW78+0x34,2);w8(ROW70+0x2f,3);w8(ROW78+0x2f,2);
}
static void load_pe(const char *name){
 FILE *f=fopen(name,"rb");if(!f){perror("EXE");exit(2);}if(fseek(f,0,SEEK_END))exit(2);long n=ftell(f);rewind(f);if(n<512)exit(2);
 unsigned char *raw=malloc((size_t)n);if(!raw||fread(raw,1,(size_t)n,f)!=(size_t)n)exit(2);fclose(f);
 uintptr_t p=(uintptr_t)raw;uint32_t pe=r32(p+0x3c);if((uint64_t)pe+256>(uint64_t)n||r32(p+pe)!=0x4550)exit(2);
 uintptr_t opt=p+pe+24;uint64_t base=r64(opt+24);uint32_t size=r32(opt+56);if(r16(opt)!=0x20b||base!=0x120000||size>0x10000000)exit(2);
 void *m=mmap((void*)(uintptr_t)base,size,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0);if(m==MAP_FAILED){perror("image map");exit(2);}
 for(unsigned i=0;i<r16(p+pe+6);i++){uintptr_t s=opt+r16(p+pe+20)+40*i;if(s+40>p+(uintptr_t)n)exit(2);uint32_t va=r32(s+12),sz=r32(s+16),off=r32(s+20);if((uint64_t)off+sz>(uint64_t)n||(uint64_t)va+sz>size)exit(2);memcpy((void*)(uintptr_t)(base+va),raw+off,sz);}
 free(raw);
 if(mmap((void*)HEAP,HEAP_SIZE,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0)==MAP_FAILED){perror("fixture map");exit(2);}
}
static volatile uint64_t *fault_address;
static void on_segv(int sig,siginfo_t *info,void *context){(void)sig;(void)context;*fault_address=(uintptr_t)info->si_addr;_exit(101);}
static int faulted(int use_lp,uintptr_t recipient,uint64_t expected){
 fault_address=mmap(NULL,4096,PROT_READ|PROT_WRITE,MAP_SHARED|MAP_ANONYMOUS,-1,0);if(fault_address==MAP_FAILED)return 0;*fault_address=UINT64_MAX;
 pid_t child=fork();if(child==0){struct sigaction s={0};s.sa_sigaction=on_segv;s.sa_flags=SA_SIGINFO;sigemptyset(&s.sa_mask);sigaction(SIGSEGV,&s,NULL);if(use_lp)lp(recipient);else xp(recipient);_exit(102);}
 int status=0;int ok=child>0&&waitpid(child,&status,0)==child&&WIFEXITED(status)&&WEXITSTATUS(status)==101&&*fault_address==expected;
 munmap((void*)fault_address,4096);return ok;
}
static void patch(void){
 if(!mutant)return;
 if(!strcmp(mutant,"skip_xp_division")){if(r16(0x2f8d1d)!=0xfdf7)exit(3);w16(0x2f8d1d,0x9090);}
 else if(!strcmp(mutant,"lp_signed_row_byte")){if(r8(0x2f9133)!=0xb6)exit(3);w8(0x2f9133,0xbe);}
 else if(!strcmp(mutant,"xp_widen_double_mask")){if(r8(0x2f8d2b)!=8)exit(3);w8(0x2f8d2b,9);}
 else if(!strcmp(mutant,"only_three_roster_slots")){if(r8(0x2f8ce4)!=4)exit(3);w8(0x2f8ce4,3);}
 else if(!strcmp(mutant,"xp_ignore_missing_owner")){if(r16(0x2f8be6)!=0x840f)exit(3);memset((void*)0x2f8be6,0x90,6);}
 else if(!strcmp(mutant,"lp_ignore_global_gate")){if(r16(0x2f90d7)!=0x850f)exit(3);memset((void*)0x2f90d7,0x90,6);}
 else exit(3);
}
int main(int argc,char **argv){
 if(argc!=2){fprintf(stderr,"usage: native_controls FFXII_TZA.exe\n");return 2;}alarm(25);load_pe(argv[1]);mutant=getenv("FF12_REWARD_MUTANT");if(mutant&&!*mutant)mutant=NULL;patch();
 printf("{\"method\":\"Original reward bodies and original gate callees; synthetic data; zero scripted application callees; not a live FF12 session\",\"cases\":[\n");
 for(unsigned n=0;n<=4;n++){reset(n);char a[80];snprintf(a,sizeof a,"null_xp_roster_count_%u",n);eq(a,xp(0),n?19/(int)n:0);snprintf(a,sizeof a,"null_lp_roster_count_%u",n);eq(a,lp(0),19);}
 reset(2);eq("recipient_xp_two_way_share",xp(rec(0)),9);eq("recipient_lp_is_not_divided",lp(rec(0)),19);
 w8(rec(0)+0x6b,8);eq("xp_double_after_rounding",xp(rec(0)),18);eq("null_xp_ignores_recipient_modifier",xp(0),9);
 w8(rec(0)+0x6b,0x28);eq("xp_zero_wins_over_double",xp(rec(0)),0);eq("null_xp_ignores_zero_modifier",xp(0),9);
 w8(rec(0)+0x6b,0);w8(rec(0)+0x7b,8);eq("xp_second_bank_double",xp(rec(0)),18);w8(rec(0)+0x7b,0x20);eq("xp_second_bank_zero",xp(rec(0)),0);
 reset(2);w8(rec(0)+0x6b,1);eq("xp_unrelated_modifier_bit0",xp(rec(0)),9);
 reset(2);w8(rec(0)+0x6b,0x10);eq("lp_recipient_double",lp(rec(0)),38);eq("null_lp_ignores_recipient_double",lp(0),19);
 w8(rec(0)+0x6b,0);w8(rec(0)+0x7b,0x10);eq("lp_second_bank_double",lp(rec(0)),38);w8(rec(0)+0x7b,0x20);eq("lp_has_no_xp_zero_modifier",lp(rec(0)),19);
 reset(2);w32(FRAME+0x5b04,1);eq("single_mode_null_is_full_formula",xp(0),19);eq("single_mode_matching_recipient",xp(rec(0)),19);eq("single_mode_mismatching_recipient",xp(rec(1)),0);
 w8(FRAME+0x5ad5,0xff);eq("single_mode_null_ignores_invalid_designation",xp(0),19);eq("single_mode_recipient_invalid_designation",xp(rec(0)),0);
 reset(2);w16(rec(6)+4,0);eq("xp_orphan_has_no_owner",xp(rec(6)),0);eq("lp_orphan_does_not_require_owner",lp(rec(6)),19);
 reset(2);w8(rec(0)+4,0x1a);w16(FRAME+0x5a5a,0x1a);eq("id1a_recipient_xp_admitted_not_in_divisor",xp(rec(0)),19);eq("id1a_recipient_lp_admitted",lp(rec(0)),19);eq("null_xp_also_excludes_id1a_from_divisor",xp(0),19);
 reset(2);w8(rec(0)+4,0x19);w16(FRAME+0x5a5a,0x19);eq("id19_recipient_xp_admitted_counted",xp(rec(0)),9);eq("id19_recipient_lp_rejected",lp(rec(0)),0);
 unsigned ids[]={6,7,0x1b,0x27,0x28};for(unsigned i=0;i<5;i++){reset(2);w8(rec(0)+4,(uint8_t)ids[i]);char s[80];snprintf(s,sizeof s,"lp_id_boundary_%02x",ids[i]);eq(s,lp(rec(0)),(ids[i]<=6||ids[i]>=0x28)?19:0);}
 reset(1);w8(rec(0)+5,1);eq("kind1_cannot_match_roster_byte",xp(0),0);
 reset(0);w32(OBJD+4,256);w16(rec(0)+4,0xffff);eq("synthetic_ff_selector_can_count_kindff_four_times",xp(0),4);
 reset(2);w32(rec(0)+0x3c,1);eq("xp_status_rejects_recipient",xp(rec(0)),0);eq("lp_status_rejects_recipient",lp(rec(0)),0);eq("null_xp_still_applies_member_status_filter",xp(0),19);
 reset(2);w32(rec(1)+0x64,0x80000000);eq("second_status_bank_excludes_member",xp(0),19);
 reset(2);eq("xp_kind1_recipient_rejected",xp(rec(4)),0);eq("lp_kind1_recipient_rejected",lp(rec(4)),0);
 reset(2);w8(rec(4)+5,0);eq("xp_non_enemy_subject_rejected",xp(0),0);eq("lp_non_enemy_subject_rejected",lp(0),0);
 reset(2);eq("xp_null_subject_returns_zero",((Reward)0x2f8bb0)(0,0),0);eq("lp_null_subject_returns_zero",((Reward)0x2f90c0)(0,0),0);
 reset(2);w64(unit(4)+0x698,0);eq("xp_null_subject_stats_returns_zero",xp(0),0);eq("lp_null_subject_stats_returns_zero",lp(0),0);
 reset(2);w8(GLP,1);eq("lp_global_gate_precedes_award",lp(0),0);w8(GLP,0xff);eq("lp_negative_global_gate_blocks",lp(rec(0)),0);eq("xp_independent_of_licence_gate",xp(0),9);
 reset(2);w8(rec(4)+0x1c2,0);w32(ROW70+0x34,1);w32(ROW78+0x34,10);eq("xp_negative_division_truncates_toward_zero",xp(0),-4);w8(ROW70+0x2f,1);w8(ROW78+0x2f,10);eq("lp_negative_formula_not_clamped",lp(0),-9);
 reset(2);w32(ROW78+0x34,0);w32(ROW70+0x34,UINT32_MAX);eq("xp_negative_unit_share_rounds_to_zero",xp(0),0);
 reset(2);w8(rec(4)+0x1c2,3);w8(ROW78+0x2f,0xfe);w8(ROW70+0x2f,0xfb);eq("lp_unsigned_byte_multiplier",lp(0),759);
 reset(2);w8(rec(4)+0x1c2,2);w32(ROW78+0x34,0x7fffffff);w32(ROW70+0x34,1);eq("xp_wrap_then_signed_division",xp(0),-1073741824);
 reset(2);w8(rec(4)+0x88,4);eq("xp_reads_actual_growth_baseline",xp(0),6);eq("lp_reads_actual_growth_baseline",lp(0),13);
 reset(0);w64(unit(4)+0xe70,0);w64(unit(4)+0xe78,0);eq("empty_roster_xp_skips_null_reward_rows",xp(0),0);
 reset(2);w64(unit(4)+0xe78,0);eq("xp_dereferences_null_multiplier_at_34",faulted(0,0,0x34),1);eq("lp_dereferences_null_multiplier_at_2f",faulted(1,0,0x2f),1);
 reset(2);w64(unit(4)+0xe70,0);eq("xp_dereferences_null_base_at_34",faulted(0,0,0x34),1);eq("lp_dereferences_null_base_at_2f",faulted(1,0,0x2f),1);
 reset(2);w8(GLP,1);eq("lp_gate_before_invalid_argument_access",((Reward)0x2f90c0)(1,1),0);
 reset(2);unsigned char *snapshot=malloc(HEAP_SIZE);if(!snapshot)return 2;memcpy(snapshot,(void*)HEAP,HEAP_SIZE);int32_t xv=xp(rec(0)),lv=lp(rec(0));report("no_writes_to_fixture_records_or_tables",!memcmp(snapshot,(void*)HEAP,HEAP_SIZE)&&xv==9&&lv==19,memcmp(snapshot,(void*)HEAP,HEAP_SIZE)==0,1);free(snapshot);
 printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failed);return failed?1:0;
}
