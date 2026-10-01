#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <signal.h>
#include <unistd.h>
#include <errno.h>
#define MS __attribute__((ms_abi,noinline))
#define ABI __attribute__((ms_abi))
#define SLOT ((uintptr_t)0x22c31c0)
#define PH ((uintptr_t)0x22c51c0)
#define PT ((uintptr_t)0x22c51c8)
#define FH ((uintptr_t)0x22c51d0)
#define CTR ((uintptr_t)0x1eed498)
#define READ_STATUS ((uintptr_t)0x215eff4)
#define CLOCK ((uintptr_t)0x22ca5e0)
#define HEAP ((uintptr_t)0x40000000)
#define AUX (HEAP+0x1000)
#define DST (HEAP+0x2000)
static uint16_t r16(uintptr_t p){uint16_t x;memcpy(&x,(void*)p,2);return x;}
static uint32_t r32(uintptr_t p){uint32_t x;memcpy(&x,(void*)p,4);return x;}
static uint64_t r64(uintptr_t p){uint64_t x;memcpy(&x,(void*)p,8);return x;}
static uint8_t r8(uintptr_t p){return *(uint8_t*)p;}
static void w32(uintptr_t p,uint32_t v){memcpy((void*)p,&v,4);}
static void w64(uintptr_t p,uint64_t v){memcpy((void*)p,&v,8);}
static void w8(uintptr_t p,uint8_t v){*(uint8_t*)p=v;}
static uintptr_t sl(unsigned i){return SLOT+0x80u*i;}
typedef void (ABI *V0)(void);
typedef uintptr_t (ABI *V1)(uintptr_t);
typedef uint32_t (ABI *B5)(uint32_t,uint32_t,uintptr_t,uint32_t,uintptr_t);
typedef uint32_t (ABI *R6)(uint32_t,uint32_t,uintptr_t,uint32_t,uintptr_t,uint32_t);
static void ctor(void){((V0)0x32e450)();}
static uintptr_t take(unsigned tail){return ((V1)0x32e990)(tail);}
static void retire(uintptr_t s){((V1)0x32ec40)(s);}
static void pump(void){((V0)0x32e070)();}
static uint32_t req(unsigned k,uint32_t i,uintptr_t d,uint32_t n,uintptr_t a,unsigned tail){return ((R6)0x32e870)(k,i,d,n,a,tail);}
static uint32_t build(unsigned k,uint32_t i,uintptr_t d,uint32_t n,uintptr_t a){return ((B5)0x32e620)(k,i,d,n,a);}
static void cancel(uint32_t id){((V1)0x32e590)(id);}
static unsigned ns,nb,nd,nc,np,nfree,ntail,ngate,npacer,nloader1,nloader2,nnotify;
static uintptr_t sa[5],sb[4],da[3],ca,fa;
static int busy,io_after_submit,loader1,loader2,pacer_completes,part_result,tail_gate;
static unsigned submitb_retry;
static unsigned checks,failures;
static uintptr_t lastret;
static char order[8192];static size_t oi;
static void logc(char c){if(oi+1<sizeof order){order[oi++]=c;order[oi]=0;}}
static MS uintptr_t service_gate(void){ngate++;logc('G');return (uintptr_t)busy;}
static MS uintptr_t submit_a(uintptr_t a,uintptr_t b,uintptr_t c,uintptr_t d,uintptr_t e){ns++;logc('I');sa[0]=a;sa[1]=b;sa[2]=c;sa[3]=d;sa[4]=e;w32(READ_STATUS,(uint32_t)io_after_submit);return 0;}
static MS uintptr_t submit_b(uintptr_t a,uintptr_t b,uintptr_t c,uintptr_t d){nb++;logc('J');sb[0]=a;sb[1]=b;sb[2]=c;sb[3]=d;w32(READ_STATUS,(uint32_t)io_after_submit);return submitb_retry&&nb<=submitb_retry?1:0;}
static MS uintptr_t tail_a(void){ntail++;logc('T');return 0;}
static MS uintptr_t tail_b(void){logc('U');return 0;}
static MS uintptr_t tail_c(void){logc('V');return (uintptr_t)tail_gate;}
static MS uintptr_t tail_d(void){logc('W');return 0;}
static MS uintptr_t pace(uintptr_t x){(void)x;npacer++;logc('P');if(pacer_completes)w32(READ_STATUS,0);return 0;}
static MS uintptr_t pred1(void){nloader1++;return (uintptr_t)loader1;}
static MS uintptr_t pred2(void){nloader2++;return (uintptr_t)loader2;}
static MS uintptr_t free_bridge(uintptr_t a,uintptr_t b){nfree++;fa=a;logc('F');(void)b;return 0;}
static MS uintptr_t notify(uintptr_t a){(void)a;nnotify++;return 0;}
static MS uintptr_t done(uintptr_t a,uintptr_t b,uintptr_t c){nd++;da[0]=a;da[1]=b;da[2]=c;logc('D');return 0x12345678;}
static MS uintptr_t canceled(uintptr_t a){nc++;ca=a;logc('C');return 0x12345678;}
static MS uintptr_t part(uintptr_t a){np++;logc('R');(void)a;return (uintptr_t)part_result;}
static void bridge(uintptr_t p,uintptr_t f){unsigned char j[12]={0x48,0xb8,0,0,0,0,0,0,0,0,0xff,0xe0};memcpy(j+2,&f,8);memcpy((void*)p,j,12);}
static void reset(unsigned fill){memset((void*)SLOT,fill,64*0x80);memset((void*)HEAP,0,0x10000);ctor();w32(READ_STATUS,0);w64(CLOCK,0x1234);w8(0x2b5e111,0);w32(0x22c51d8,0);w32(0x22c51dc,0);ns=nb=nd=nc=np=nfree=ntail=ngate=npacer=nloader1=nloader2=nnotify=0;busy=0;io_after_submit=0;loader1=loader2=pacer_completes=tail_gate=0;part_result=1;submitb_retry=0;memset(sa,0,sizeof sa);memset(sb,0,sizeof sb);memset(da,0,sizeof da);ca=fa=0;oi=0;order[0]=0;lastret=0;}
static void aux(int32_t off){w32(AUX,(uint32_t)off);w32(AUX+4,0x98765432);w32(AUX+8,0x89abcdef);w64(AUX+0x10,(uintptr_t)done);w64(AUX+0x18,(uintptr_t)canceled);w64(AUX+0x20,(uintptr_t)part);}
static int bytes_are(uintptr_t p,unsigned n,unsigned v){for(unsigned i=0;i<n;i++)if(r8(p+i)!=(uint8_t)v)return 0;return 1;}
static int graph(void){unsigned seen[64]={0},count=0;uintptr_t p=r64(PH),prev=0;while(p){if(p<SLOT||p>=SLOT+64*128||((p-SLOT)%128)||count++>=64)return 0;unsigned k=(unsigned)((p-SLOT)/128);if(seen[k]++||r64(p+0x18)!=prev)return 0;prev=p;p=r64(p+0x10);}if(prev!=r64(PT))return 0;p=r64(FH);prev=0;count=0;while(p){if(p<SLOT||p>=SLOT+64*128||((p-SLOT)%128)||count++>=64)return 0;unsigned k=(unsigned)((p-SLOT)/128);if(seen[k]++||r64(p+0x18)!=prev)return 0;prev=p;p=r64(p+0x10);}for(unsigned i=0;i<64;i++)if(seen[i]!=1)return 0;return 1;}
static void ck(const char *name,int ok){printf("%s{\"name\":\"%s\",\"pass\":%s,\"observed\":{\"free_head_offset\":%lld,\"pending_head_offset\":%lld,\"counter\":%u,\"slot0_state\":%u,\"slot0_kind\":%u,\"slot0_index\":%u,\"slot0_bytes\":%u,\"slot0_id\":%u,\"submits\":%u,\"path_submits\":%u,\"done_calls\":%u,\"cancel_calls\":%u,\"part_calls\":%u,\"free_calls\":%u,\"footer_calls\":%u,\"pacer_calls\":%u,\"last_return_normalized\":%llu,\"order\":\"%s\"}}",checks?",\n":"",name,ok?"true":"false",r64(FH)?(long long)(r64(FH)-SLOT):-1LL,r64(PH)?(long long)(r64(PH)-SLOT):-1LL,r32(CTR),r8(SLOT+0x20),r8(SLOT+0x21),r32(SLOT+0x24),r32(SLOT+0x28),r32(SLOT+0x64),ns,nb,nd,nc,np,nfree,ntail,npacer,(unsigned long long)(lastret==(uintptr_t)done?0:lastret),order);checks++;failures+=!ok;if(!ok&&getenv("FF12_QUEUE_MUTANT")){printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);exit(1);}}
static volatile uint64_t *fault_cell;
static void segv(int sig,siginfo_t *si,void *ctx){(void)sig;(void)ctx;*fault_cell=(uintptr_t)si->si_addr;_exit(101);}
static int empty_fault(unsigned flag){fault_cell=mmap(NULL,4096,PROT_READ|PROT_WRITE,MAP_SHARED|MAP_ANONYMOUS,-1,0);if(fault_cell==MAP_FAILED)return 0;*fault_cell=0xdead;pid_t p=fork();if(!p){struct sigaction a={0};a.sa_sigaction=segv;a.sa_flags=SA_SIGINFO;sigemptyset(&a.sa_mask);sigaction(SIGSEGV,&a,NULL);w64(FH,0);take(flag);_exit(102);}int st=0;if(p<0||waitpid(p,&st,0)!=p)return 0;int ok=WIFEXITED(st)&&WEXITSTATUS(st)==101&&*fault_cell==0x10;munmap((void*)fault_cell,4096);return ok;}
static void load_pe(const char *path){FILE*f=fopen(path,"rb");if(!f){perror("exe");exit(2);}fseek(f,0,SEEK_END);long n=ftell(f);rewind(f);if(n<512)exit(2);unsigned char*raw=malloc((size_t)n);if(!raw||fread(raw,1,(size_t)n,f)!=(size_t)n)exit(2);fclose(f);uint32_t pe=r32((uintptr_t)raw+0x3c);if(pe+256u>(unsigned long)n||r32((uintptr_t)raw+pe)!=0x4550)exit(2);uintptr_t opt=(uintptr_t)raw+pe+24,base=r64(opt+24);uint32_t size=r32(opt+56);if(base!=0x120000||size>0x10000000)exit(2);void*im=mmap((void*)base,size,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0);if(im==MAP_FAILED){perror("image map");exit(2);}for(unsigned i=0;i<r16((uintptr_t)raw+pe+6);i++){uintptr_t s=opt+r16((uintptr_t)raw+pe+20)+40*i;uint32_t va=r32(s+12),sz=r32(s+16),off=r32(s+20);if((uint64_t)off+sz>(uint64_t)n||(uint64_t)va+sz>size)exit(2);memcpy((void*)(base+va),raw+off,sz);}free(raw);if(mmap((void*)HEAP,0x10000,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0)==MAP_FAILED){perror("fixture map");exit(2);}}
int main(int argc,char **argv){if(argc!=2){fprintf(stderr,"usage: native_controls FFXII_TZA.exe\n");return 2;}alarm(20);load_pe(argv[1]);
 bridge(0x3eadd0,(uintptr_t)service_gate);bridge(0x46e030,(uintptr_t)submit_a);bridge(0x2df6c0,(uintptr_t)submit_b);bridge(0x46dd50,(uintptr_t)tail_a);bridge(0x3e9780,(uintptr_t)tail_b);bridge(0x36fd50,(uintptr_t)tail_c);bridge(0x3bb790,(uintptr_t)tail_d);bridge(0x35ea30,(uintptr_t)pace);bridge(0x1ede80,(uintptr_t)pred1);bridge(0x17d930,(uintptr_t)pred2);bridge(0x369860,(uintptr_t)free_bridge);bridge(0x8620c0,(uintptr_t)notify);
 const char*mu=getenv("FF12_QUEUE_MUTANT");if(mu&&*mu){
  if(!strcmp(mu,"omit_free_head_advance")){if(r8(0x32e9b5)!=0x48)return 3;memset((void*)0x32e9b5,0x90,7);}
  else if(!strcmp(mu,"remove_generation_increment")){if(r16(0x32e922)!=0xc2ff)return 3;memset((void*)0x32e922,0x90,2);}

  else if(!strcmp(mu,"constructor_clobber_unobserved")){/* redirect a verified ctor zero-store from +0x28 to +0x30 */if(r8(0x32e496)!=0x10)return 3;w8(0x32e496,0x18);}
  else if(!strcmp(mu,"retire_clobber_payload")){/* substitute the id clear with an index clear, deliberately wrong */if(r8(0x32ecc7)!=0x64)return 3;w8(0x32ecc7,0x24);}
  else if(!strcmp(mu,"offset_round_up")){/* bias positive offsets too */if(r16(0x32e8fc)!=0xe281)return 3;unsigned char b[]={0xba,0xff,0x07,0,0,0x90};memcpy((void*)0x32e8fc,b,6);}
  else if(!strcmp(mu,"ignore_generation_on_cancel")){if(r8(0x32e5b7)!=0x75)return 3;memset((void*)0x32e5b7,0x90,2);}
  else return 3;
 }
 printf("{\"method\":\"original CPU instructions; synthetic queue and scripted external service boundaries; not live FF12\",\"cases\":[\n");
 reset(0xa5);int ok=graph();for(unsigned i=0;i<64;i++)ok&=r32(sl(i)+0x58)==i&&r32(sl(i)+0x64)==0xffffffff&&r16(sl(i)+0x20)==0&&r32(sl(i)+0x28)==0;ck("constructor_all_64_links_and_indices",ok);
 ok=1;for(unsigned i=0;i<64;i++){uintptr_t s=sl(i);ok&=bytes_are(s,16,0xa5)&&bytes_are(s+0x22,6,0xa5)&&bytes_are(s+0x2c,0x2c,0xa5)&&bytes_are(s+0x5c,8,0xa5)&&bytes_are(s+0x68,0x18,0xa5);}ck("constructor_preserves_unwritten_bytes",ok);
 reset(0);lastret=take(1);ck("take_moves_free_head_not_array_base",lastret==SLOT&&r64(FH)==sl(1)&&r64(PH)==SLOT&&r64(PT)==SLOT&&graph());
 lastret=take(1);ck("tail_insert_preserves_head",lastret==sl(1)&&r64(PH)==SLOT&&r64(PT)==sl(1)&&r64(SLOT+0x10)==sl(1)&&graph());
 lastret=take(0);ck("head_insert_reorders_pending",lastret==sl(2)&&r64(PH)==sl(2)&&r64(PT)==sl(1)&&r64(sl(2)+0x10)==SLOT&&graph());
 retire(SLOT);ck("retire_middle_updates_both_neighbors",r64(sl(2)+0x10)==sl(1)&&r64(sl(1)+0x18)==sl(2)&&r64(FH)==SLOT&&graph());
 retire(sl(2));ck("retire_head_preserves_tail",r64(PH)==sl(1)&&r64(PT)==sl(1)&&graph());retire(sl(1));ck("retire_last_empties_pending",r64(PH)==0&&r64(PT)==0&&graph());
 reset(0xa5);take(1);unsigned char before[128];memcpy(before,(void*)SLOT,128);retire(SLOT);ok=1;for(unsigned i=0;i<128;i++)if(!(i>=0x10&&i<0x20)&&!(i>=0x64&&i<0x68))ok&=r8(SLOT+i)==before[i];ck("splice_does_not_zero_payload_or_state",ok&&r32(SLOT+0x64)==0xffffffff&&graph());
 reset(0);ck("empty_free_head_fault_flag0_at_0x10",empty_fault(0));ck("empty_free_head_fault_flag1_at_0x10",empty_fault(1));
 reset(0);for(unsigned i=0;i<64;i++)lastret=take(1);ck("sixty_fourth_take_exhausts_free_list",lastret==sl(63)&&r64(FH)==0&&graph());
 reset(0xa5);aux(0x8ff);lastret=req(9,0x1234,DST,0x500,AUX,1);ck("request_stamps_defined_fields",lastret==0x40&&r8(SLOT+0x20)==1&&r8(SLOT+0x21)==9&&r32(SLOT+0x24)==0x1234&&r64(SLOT+0x38)==DST&&r64(SLOT+0x70)==DST&&r32(SLOT+0x5c)==0&&r16(SLOT+0x22)==0);
 ck("request_ignores_descriptor_part_callback",r64(AUX+0x20)==(uintptr_t)part&&r64(SLOT+0x50)==0&&r64(SLOT+0x40)==(uintptr_t)done&&r64(SLOT+0x48)==(uintptr_t)canceled&&r32(SLOT+0x60)==0x89abcdef);
 ck("request_preserves_unused_stamp_caps_and_tail",bytes_are(SLOT+8,8,0xa5)&&bytes_are(SLOT+0x30,8,0xa5)&&bytes_are(SLOT+0x68,8,0xa5)&&bytes_are(SLOT+0x78,8,0xa5));
 int32_t offsets[]={0,0x7ff,0x800,0x801,-1,-0x7ff,-0x800,-0x801,INT32_MIN,INT32_MAX};for(unsigned i=0;i<sizeof offsets/sizeof*offsets;i++){reset(0);aux(offsets[i]);req(1,0,DST,1,AUX,1);char name[90];snprintf(name,sizeof name,"offset_truncation_%d",offsets[i]);int32_t expected=(offsets[i]/2048)*2048;ck(name,r32(SLOT+0x2c)==(uint32_t)expected);}
 reset(0);uint32_t id1=req(1,0,0,0,0,1),id2=req(1,0,0,0,0,1);ck("generation_and_slot_are_distinct",id1==0x40&&id2==0x81&&r32(CTR)==3&&graph());retire(SLOT);lastret=req(1,0,0,0,0,1);ck("slot_reuse_changes_request_generation",lastret==0xc0&&graph());
 reset(0);w32(CTR,0xffffff);lastret=req(1,0,0,0,0,1);ck("maximum_constructor_domain_counter_wraps_to_one",lastret==0x3fffffc0&&r32(CTR)==1);
 reset(0);w32(CTR,0);lastret=req(1,0,0,1,0,1);ck("planted_zero_counter_still_consumes_slot",lastret==0&&r64(PH)==SLOT&&r64(FH)==sl(1)&&r32(SLOT+0x64)==0);
 reset(0);w32(CTR,0x7fffffff);lastret=req(1,0,0,0,0,1);ck("out_of_domain_counter_uses_signed_wrap_compare",lastret==0xffffffc0&&r32(CTR)==0x80000000);
 reset(0);lastret=build(0x55,0xffffffff,DST,1,0);ck("negative_builder_index_changes_telemetry_not_queue",lastret==0xffffffff&&r32(0x22c51d8)==0x55&&r32(0x22c51dc)==0xffffffff&&r64(PH)==0&&r64(FH)==SLOT&&r32(CTR)==1);
 reset(0xa5);aux(0x8ff);unsigned char oldaux[40];memcpy(oldaux,(void*)AUX,40);lastret=build(2,3,DST,0x90000,AUX);ck("gate_clear_large_request_is_not_chunked",lastret==0x40&&r32(SLOT+0x28)==0x90000&&r16(SLOT+0x22)==0&&r32(SLOT+0x30)==0xa5a5a5a5&&r32(SLOT+0x34)==0xa5a5a5a5&&memcmp(oldaux,(void*)AUX,40)==0);
 reset(0xa5);aux(-0x801);memcpy(oldaux,(void*)AUX,40);w8(0x2b5e111,1);lastret=build(2,3,DST,0x90000,AUX);ck("gate_set_clamps_and_copies_without_mutating_descriptor",lastret==0x40&&r16(SLOT+0x22)==1&&r32(SLOT+0x30)==0x80000&&r32(SLOT+0x34)==0x90000&&r32(SLOT+0x28)==0x80000&&r32(SLOT+0x2c)==0xfffff800&&r64(SLOT+0x50)==0&&memcmp(oldaux,(void*)AUX,40)==0);
 reset(0);w8(0x2b5e111,1);lastret=build(2,3,DST,0xffffffff,0);ck("chunk_size_minimum_is_signed",r32(SLOT+0x28)==0xffffffff&&r32(SLOT+0x34)==0xffffffff&&r16(SLOT+0x22)==1);
 reset(0xa5);w8(0x2b5e111,1);w32(CTR,0);lastret=build(2,3,DST,0x90000,0);ck("planted_zero_id_skips_fixups_but_not_enqueue",lastret==0&&r64(PH)==SLOT&&r16(SLOT+0x22)==0&&r32(SLOT+0x28)==0x90000&&r32(SLOT+0x30)==0xa5a5a5a5);
 reset(0);req(1,0,0,1,0,1);lastret=((B5)0x32e780)(2,0,0,1,0);ck("head_request_wrapper_takes_priority",lastret==0x81&&r64(PH)==sl(1)&&r64(PT)==SLOT&&graph());
 reset(0);pump();ck("empty_pump_runs_common_footer_not_shutdown_claim",ngate==1&&ntail==1&&strcmp(order,"GTUV")==0);
 reset(0);aux(0);req(7,123,DST,0,AUX,1);pump();ck("zero_byte_request_completes_without_file_issue",nd==1&&ns==0&&nb==0&&da[0]==0x89abcdef&&da[1]==DST&&da[2]==1&&r64(PH)==0&&graph());
 ck("normal_retirement_leaves_kind_index_callbacks",r8(SLOT+0x21)==7&&r32(SLOT+0x24)==123&&r64(SLOT+0x40)==(uintptr_t)done&&r64(SLOT+0x70)==DST&&r8(SLOT+0x20)==0&&r32(SLOT+0x64)==0xffffffff);
 reset(0);aux(0);for(unsigned i=0;i<64;i++)req(1,i,DST,0,AUX,1);pump();ck("one_pump_can_drain_all_64_requests",nd==64&&ns==0&&ntail==1&&r64(PH)==0&&graph());
 reset(0);aux(0);for(unsigned i=0;i<64;i++)req(1,i,DST,0,AUX,1);lastret=req(2,55,DST,0,AUX,1);ck("sixty_fifth_request_self_pumps_then_returns",nd==64&&npacer==1&&ns==0&&lastret==0x107f&&r64(PH)==sl(63)&&graph());
 reset(0);aux(0x8ff);io_after_submit=-1;req(3,99,DST,0x100,AUX,1);pump();ck("single_pump_advances_queued_issued_waiting",ns==1&&r8(SLOT+0x20)==3&&nd==0&&r64(SLOT)==0x1234&&r64(SLOT+8)==0x1234&&sa[0]==3&&sa[1]==99&&sa[2]==0x800&&sa[3]==0x100&&sa[4]==DST);
 req(3,100,DST,0,AUX,1);unsigned oldtail=ntail;pump();ck("waiting_head_blocks_later_zero_byte_request",nd==0&&r8(sl(1)+0x20)==1&&ntail==oldtail+1&&r64(PH)==SLOT);
 w32(READ_STATUS,0);pump();ck("completed_head_then_next_request_same_pump",nd==2&&r64(PH)==0&&graph());
 reset(0);req(1,0,0,1,0,1);w8(SLOT+0x20,2);w64(SLOT,10);w64(SLOT+8,7);w64(CLOCK,100);w32(READ_STATUS,0xffffffff);pump();ck("state2_adds_absolute_counter_not_elapsed",r64(SLOT)==110&&r64(SLOT+8)==100&&r8(SLOT+0x20)==3);
 reset(0);aux(0);req(1,4,DST,17,AUX,1);w8(SLOT+0x20,6);pump();ck("error_callback_requires_minus_one_byte_count",nd==0&&r64(PH)==0);
 reset(0);aux(0);req(1,4,DST,0xffffffff,AUX,1);w8(SLOT+0x20,6);pump();ck("minus_one_byte_count_calls_error_callback",nd==1&&da[2]==0&&r64(PH)==0);
 reset(0);aux(0);req(1,4,DST,17,AUX,1);lastret=((V1)0x32e370)(SLOT);ck("gated_error_helper_returns_callback_pointer",lastret==(uintptr_t)done&&nd==0);
 reset(0);aux(0x801);req(255,0x80001234,DST,33,AUX,1);io_after_submit=-1;pump();ck("path_route_sign_extends_stored_32bit_value",nb==1&&sb[0]==0xffffffff80001234ULL&&sb[1]==DST&&sb[2]==33&&sb[3]==0x800);
 reset(0);req(255,0x1234000,DST,1,0,1);submitb_retry=1;io_after_submit=-1;pump();ck("path_submit_retry_can_revisit_same_head",nb==2&&r8(SLOT+0x20)==3);
 reset(0);aux(0);req(255,0x80001234,DST,0,AUX,1);pump();ck("path_done_free_uses_signed_extension",nd==1&&nfree==1&&fa==0xffffffff80001234ULL);
 reset(0);aux(0);uint32_t id=req(1,12,DST,123,AUX,1);cancel(id+64);ck("cancel_rejects_stale_generation",r64(PH)==SLOT&&nc==0&&r64(SLOT+0x40)==(uintptr_t)done);cancel(0);cancel(0xffffffff);ck("cancel_rejects_sentinel_ids",r64(PH)==SLOT&&nc==0);
 cancel(id);ck("cancel_queued_calls_cancel_then_retires",nc==1&&ca==0x89abcdef&&r64(PH)==0&&r32(SLOT+0x28)==0&&r64(SLOT+0x40)==0&&graph());
 reset(0);id=req(1,12,DST,123,0,1);cancel(id);ck("cancel_without_callback_preserves_byte_count",r64(PH)==0&&r32(SLOT+0x28)==123&&r8(SLOT+0x20)==0);
 reset(0);aux(0);id=req(1,12,DST,123,AUX,1);w8(SLOT+0x20,2);w32(READ_STATUS,0xffffffff);cancel(id);ck("cancel_inflight_marks_state4_without_retire",r8(SLOT+0x20)==4&&r64(PH)==SLOT&&nc==0&&r64(SLOT+0x40)==0);pump();ck("state4_waits_for_inflight_flag",nc==0&&r64(PH)==SLOT);w32(READ_STATUS,0);pump();ck("state4_completion_cancel_callback_and_reuse",nc==1&&nd==0&&r64(PH)==0&&graph());
 reset(0);aux(0);w8(0x2b5e111,1);build(1,2,DST,0x90000,AUX);pump();ck("chunked_builder_drains_two_parts_without_part_callback",ns==2&&np==0&&nd==1&&r64(PH)==0&&r32(SLOT+0x34)==0&&sa[3]==0x10000&&sa[4]==DST+0x80000&&graph());
 reset(0);aux(0);w8(0x2b5e111,1);build(1,2,DST,0x90000,AUX);w64(SLOT+0x50,(uintptr_t)part);part_result=2;pump();ck("part_result2_pauses_without_retirement",ns==1&&np==1&&r8(SLOT+0x20)==5&&r8(SLOT+0x23)==2&&r64(PH)==SLOT&&nd==0);part_result=1;pump();ck("part_result2_reprobes_then_continues",np==2&&ns==2&&nd==1&&r64(PH)==0&&graph());
 reset(0);aux(0);w8(0x2b5e111,1);build(1,2,DST,0x90000,AUX);w64(SLOT+0x50,(uintptr_t)part);part_result=3;pump();ck("part_result3_returns_with_pending_record",np==1&&r64(PH)==SLOT&&nd==0&&r8(SLOT+0x23)==3);pump();ck("part_result3_is_not_terminal_release_rule",np==1&&ns==1&&nd==1&&r64(PH)==0&&r32(SLOT+0x34)==0xfff90000);
 reset(0);req(1,2,DST,1,0,1);w8(SLOT+0x20,5);w8(SLOT+0x22,2);pump();ck("unrecognized_chunk_flag_exits_without_retire",r64(PH)==SLOT&&nd==0&&ns==0);
 reset(0);lastret=((V1)0x32e520)(1);ck("poll_idle_has_no_pump_side_effect",lastret==0&&ntail==0&&ngate==0);w32(READ_STATUS,0xffffffff);lastret=((V1)0x32e520)(1);ck("poll_sees_inflight_without_pending",lastret==1&&ntail==0);
 reset(0);req(1,2,DST,0,0,1);lastret=((V1)0x32e520)(1);ck("poll_does_not_drain_ready_work",lastret==1&&r64(PH)==SLOT&&ntail==0);lastret=((V1)0x32e520)(0);ck("drain_form_pumps_before_testing_idle",lastret==0&&r64(PH)==0&&ntail==1);
 reset(0);aux(0);req(1,2,DST,10,AUX,1);io_after_submit=-1;pacer_completes=1;lastret=((V1)0x32e520)(0);ck("drain_form_paces_and_pumps_until_completion",lastret==0&&npacer==1&&ns==1&&nd==1&&ntail==2&&graph());
 reset(0);((V0)0x32e040)();ck("frame_gate_idle_no_pump",nloader1==1&&nloader2==1&&ntail==0);loader1=1;((V0)0x32e040)();ck("frame_gate_first_predicate_short_circuits",nloader1==2&&nloader2==1&&ntail==1);loader1=0;loader2=1;((V0)0x32e040)();ck("frame_gate_second_predicate_runs_pump",nloader1==3&&nloader2==2&&ntail==2);
 printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);return failures?1:0;
}
