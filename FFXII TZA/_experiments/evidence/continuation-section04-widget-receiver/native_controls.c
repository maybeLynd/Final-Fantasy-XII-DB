#define _GNU_SOURCE
/* SECTION-04: full original widget entries over synthetic state. Selected resource,
 * allocation, manager, free and layout-service boundaries are explicitly replaced.
 * No FF12 process, actual asset IO, GPU work, or original scanner execution. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <setjmp.h>
#define ABI __attribute__((ms_abi))
#define H ((uintptr_t)0x40000000)
#define HS 0x40000
#define A (H+0x1000)
#define C (H+0x3000)
#define MSG (H+0x5000)
#define POOL (H+0x10000)
#define R1 ((uintptr_t)0x208f580)
#define R2 (H+0x8000)
#define G ((uintptr_t)0x2aee4c0)
#define CG ((uintptr_t)0x2aee4c8)
#define T ((uintptr_t)0x2090790)
#define BITSET ((uintptr_t)0x215f1c0)
static unsigned checks,failures;static const char *mutant;
static uint8_t r8(uintptr_t p){uint8_t v;memcpy(&v,(void*)p,1);return v;}
static uint16_t r16(uintptr_t p){uint16_t v;memcpy(&v,(void*)p,2);return v;}
static uint32_t r32(uintptr_t p){uint32_t v;memcpy(&v,(void*)p,4);return v;}
static uint64_t r64(uintptr_t p){uint64_t v;memcpy(&v,(void*)p,8);return v;}
static void w8(uintptr_t p,uint8_t v){memcpy((void*)p,&v,1);}
static void w16(uintptr_t p,uint16_t v){memcpy((void*)p,&v,2);}
static void w32(uintptr_t p,uint32_t v){memcpy((void*)p,&v,4);}
static void w64(uintptr_t p,uint64_t v){memcpy((void*)p,&v,8);}
static void result(const char *n,int ok,int64_t actual,int64_t expected){
 printf("%s{\"name\":\"%s\",\"pass\":%s,\"observed\":%lld,\"expected\":%lld}",checks?",\n":"",n,ok?"true":"false",(long long)actual,(long long)expected);
 ++checks;failures+=!ok;
 if(!ok&&mutant){printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);exit(1);}
}
static void eq(const char *n,int64_t v,int64_t e){result(n,v==e,v,e);}
static int filled(uintptr_t p,size_t n,uint8_t value){for(size_t i=0;i<n;i++)if(r8(p+i)!=value)return 0;return 1;}
static void load_pe(const char *name){
 FILE *f=fopen(name,"rb");if(!f){perror("EXE");exit(2);}if(fseek(f,0,SEEK_END))exit(2);long n=ftell(f);rewind(f);if(n<512)exit(2);
 unsigned char *raw=malloc((size_t)n);if(!raw||fread(raw,1,(size_t)n,f)!=(size_t)n)exit(2);fclose(f);
 uintptr_t p=(uintptr_t)raw;uint32_t pe=r32(p+0x3c);if((uint64_t)pe+256>(uint64_t)n||r32(p+pe)!=0x4550)exit(2);
 uintptr_t opt=p+pe+24;uint64_t base=r64(opt+24);uint32_t size=r32(opt+56);if(r16(opt)!=0x20b||base!=0x120000||size>0x10000000)exit(2);
 if(mmap((void*)(uintptr_t)base,size,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0)==MAP_FAILED){perror("map image");exit(2);}
 for(unsigned i=0;i<r16(p+pe+6);i++){uintptr_t s=opt+r16(p+pe+20)+40*i;if(s+40>p+(uintptr_t)n)exit(2);uint32_t va=r32(s+12),sz=r32(s+16),off=r32(s+20);if((uint64_t)off+sz>(uint64_t)n||(uint64_t)va+sz>size)exit(2);memcpy((void*)(uintptr_t)(base+va),raw+off,sz);}
 free(raw);
 if(mmap((void*)H,HS,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0)==MAP_FAILED){perror("map state");exit(2);}
}
/* Explicit service replacements. Entry-specific argument checks and return buffers
 * bound what the original callers are tested against. They are not resource models. */
static unsigned svc_errors,attach_calls,resource_calls,file_calls,free_calls,cancel_calls,heap_calls;
static uintptr_t free_args[8],attach_self,attach_manager;static uint32_t heap_size;
static int pending;
static void ABI *host_zero(void *p,int b,size_t n){return memset(p,b,n);}
static uintptr_t ABI resource(uintptr_t ticket,uint32_t cls,uint32_t id,uint32_t mode,uintptr_t descriptor,uint32_t x){
 resource_calls++;
 svc_errors+=ticket!=T||cls!=7||id!=0x3d||mode!=3||descriptor!=r64(0xd11390)||x!=2;
 svc_errors+=r64(ticket+8)!=r64(G)||r32(r64(G)+0xc0)!=0;
 if(pending)w16(ticket+0x18,(uint16_t)(r16(ticket+0x18)+1));
 return R1;
}
static uintptr_t ABI file(uintptr_t ticket,uint32_t cls,uint32_t id){
 file_calls++;svc_errors+=ticket!=T||cls!=7||id!=0x3a;
 if(pending)w16(ticket+0x18,(uint16_t)(r16(ticket+0x18)+1));
 return R2;
}
static void ABI attach(uintptr_t manager,uintptr_t self){attach_calls++;attach_self=self;attach_manager=manager;}
static void ABI release(uintptr_t p,uint32_t mode){if(free_calls<8)free_args[free_calls]=p;free_calls++;svc_errors+=mode!=0;}
static void ABI cancel(uintptr_t p){cancel_calls++;svc_errors+=p!=R1;}
static uintptr_t ABI allocate(uint32_t bytes){heap_calls++;heap_size=bytes;return C;}
static jmp_buf barrier;static uintptr_t seen_consumer,seen_resource;static uint32_t seen_tag;
static void ABI layout_boundary(uintptr_t consumer,uintptr_t resource_pointer,uint32_t tag){seen_consumer=consumer;seen_resource=resource_pointer;seen_tag=tag;longjmp(barrier,1);}
static void replacement(uintptr_t at,uintptr_t to){/* absolute jmp RAX: all callers may clobber RAX */
 w8(at,0x48);w8(at+1,0xb8);w64(at+2,to);w8(at+10,0xff);w8(at+11,0xe0);
}
static void services(void){
 w64(0x8c2a60,(uintptr_t)&host_zero); /* imported memset target through original 00861EC0 */
 replacement(0x2493d0,(uintptr_t)&resource);replacement(0x249320,(uintptr_t)&file);
 replacement(0x248220,(uintptr_t)&attach);replacement(0x369860,(uintptr_t)&release);
 replacement(0x181610,(uintptr_t)&cancel);replacement(0x2497b0,(uintptr_t)&allocate);
 replacement(0x3946b0,(uintptr_t)&layout_boundary);
}
static void reset(void){
 memset((void*)H,0,HS);memset((void*)A,0xa5,0x120);memset((void*)C,0xa5,0x240);
 memset((void*)T,0,12*0x20);memset((void*)R1,0,64*0x48);
 w64(G,0);w64(CG,0);w64(0x208ea58,POOL);w32(0x208ed5c,0);w32(0x208f560,0);
 w32(0x1dfe0c0,0);w32(0x1f82e38,0);w32(0x22c2548,0);w64(0x208ea28,H+0x9000);w64(0x1fd4948,0);
 w32(BITSET,0);w32(BITSET+4,0);w32(0x2090780,1);
 w32(R1+0x38,0x20);w32(R1+0x40,0x12345678);w64(R1+0x18,H+0xa000);
 svc_errors=attach_calls=resource_calls=file_calls=free_calls=cancel_calls=heap_calls=0;
 memset(free_args,0,sizeof free_args);attach_self=attach_manager=0;heap_size=0;pending=0;
 seen_consumer=seen_resource=0;seen_tag=0;
}
typedef uintptr_t (ABI *Init)(uintptr_t,uint32_t,uintptr_t,uintptr_t,uint32_t);
typedef int32_t (ABI *Handler)(uintptr_t,uintptr_t);
typedef uintptr_t (ABI *New)(uint32_t,uintptr_t,uintptr_t);
static void init(uintptr_t object,uint32_t size,uintptr_t handler,uintptr_t args,uint32_t pooled){((Init)0x2465f0)(object,size,handler,args,pooled);}
static int32_t dispatch(uintptr_t code,uintptr_t object,uint32_t id){w32(MSG,id);return ((Handler)code)(object,MSG);}
static int consumer_gate(void){if(setjmp(barrier)==0){dispatch(0x3939b0,C,2);return 0;}return 1;}
static void mutations(void){
 if(!mutant)return;
 if(!strcmp(mutant,"message_read_from_receiver")){if(r8(0x3939f9)!=0x43)exit(3);w8(0x3939f9,0x46);}
 else if(!strcmp(mutant,"erase_rbx_kill")){if(r16(0x3939fb)!=0xdb33)exit(3);w16(0x3939fb,0x9090);}
 else if(!strcmp(mutant,"ready_wrong_bit")){if(r8(0x3940e9)!=1)exit(3);w8(0x3940e9,2);}
 else if(!strcmp(mutant,"skip_d0_clear")){if(r8(0x3940b9)!=0x48)exit(3);memset((void*)0x3940b9,0x90,11);}
 else if(!strcmp(mutant,"clear_other_singleton")){if(r32(0x3940d5)!=0x275a3e3)exit(3);w32(0x3940d5,0x275a3eb);}
 else if(!strcmp(mutant,"consumer_tests_own_ready")){if(r8(0x393a99)!=0x82)exit(3);w8(0x393a99,0x86);}
 else exit(3);
}
int main(int argc,char **argv){
 if(argc!=2){fprintf(stderr,"usage: native_widget FFXII_TZA.exe\n");return 2;}alarm(20);load_pe(argv[1]);services();
 mutant=getenv("FF12_WIDGET_MUTANT");if(mutant&&!*mutant)mutant=NULL;mutations();
 printf("{\"method\":\"Original widget bodies, explicit service replacements, synthetic states; no live FF12\",\"cases\":[\n");
 reset();pending=1;uintptr_t raw_return=((Init)0x2465f0)(A,0xd8,0x394070,0,0);
 eq("raw_initializer_does_not_return_object",raw_return,1);
 eq("constructor_publishes_asset_receiver",r64(G),A);eq("constructor_handler_identity",r64(A),0x394070);
 eq("constructor_declared_extent_zeroed",filled(A+0xbc,4,0),1);eq("constructor_does_not_zero_pool_tail",filled(A+0xd8,0x48,0xa5),1);
 eq("pending_resource_ready_remains_zero",r32(A+0xc0),0);eq("resource_slot_written_at_c8",r64(A+0xc8),R1);eq("file_result_written_at_d0",r64(A+0xd0),R2);
 eq("resource_pointee_offset40_is_reset",r32(R1+0x40),0);eq("resource_call_argument_contract",svc_errors,0);
 eq("request_owner_is_asset_not_message",r64(T+8),A);eq("request_counts_two_pending_boundaries",r16(T+0x18),2);
 eq("manager_receives_asset",attach_self,A);eq("manager_is_selected_global",attach_manager,H+0x9000);
 eq("asset_sets_channel0_bit21",r32(BITSET),1u<<21);eq("asset_does_not_set_channel1",r32(BITSET+4),0);
 eq("ready_message_zero_return",dispatch(0x394070,A,16),0);eq("ready_message_sets_bit0",r32(A+0xc0),1);
 w32(A+0xc0,0x80000004);dispatch(0x394070,A,16);eq("ready_message_preserves_other_bits",r32(A+0xc0),0x80000005);
 w64(A+0x8,0x1122334455667788ull);w64(A+0x15,0x2233445566778899ull);
 eq("default_message_returns_zero",dispatch(0x394070,A,99),0);eq("default_preserves_unrelated_header",r64(A+8),0x1122334455667788ull);
 w64(CG,C);dispatch(0x394070,A,18);
 eq("teardown_clears_file_pointer",r64(A+0xd0),0);eq("teardown_preserves_released_c8_value",r64(A+0xc8),R1);
 eq("teardown_clears_asset_global",r64(G),0);eq("teardown_preserves_consumer_global",r64(CG),C);
 eq("teardown_releases_resource_payload_first",free_args[0],H+0xa000);eq("teardown_releases_file_pointer_second",free_args[1],R2);
 eq("teardown_resource_slot_count",r32(0x2090780),0);eq("teardown_no_resource_active_bit",r32(R1+0x38)&0x20,0);
 eq("teardown_clears_channel0_bit21",r32(BITSET),0);eq("teardown_service_contract",svc_errors,0);
 reset();pending=1;w32(0x1f82e38,1);
 eq("raw_initializer_half_rate_outside_tick_returns_zero",((Init)0x2465f0)(A,0xd8,0x394070,0,0),0);
 reset();pending=1;
 eq("in_place_wrapper_returns_object",((uintptr_t (ABI*)(uintptr_t,uint32_t,uintptr_t,uintptr_t))0x245000)(A,0xd8,0x394070,0),A);
 reset();init(A,0xd8,0x394070,0,0);eq("already_complete_request_notifies_during_initialization",r32(A+0xc0),1);eq("completed_request_slot_released",r32(T)&1,0);
 reset();w64(A+0xc8,0);w64(A+0xd0,0);w64(G,C);w64(CG,H+0xb000);w32(BITSET,0xffffffff);dispatch(0x394070,A,18);
 eq("null_handles_do_not_call_free",free_calls,0);eq("teardown_unconditionally_clears_even_other_publication",r64(G),0);eq("teardown_only_clears_selected_channel_bit",r32(BITSET),0xffdfffff);
 /* Consumer's INIT branch: original scratch reset / channel setter / mode predicate;
  * only manager-link service is substituted along this branch. */
 reset();w64(G,A);w64(MSG+8,0xa5a5a5a5a5a5a55aull);w8(C+8,0xcc);dispatch(0x3939b0,C,1);
 eq("consumer_initial_mode_comes_from_message",r8(C+0xc0),0x5a);
 eq("consumer_xor_clears_state_not_message_address",r32(C+0xc4),0);eq("consumer_initial_child_pointer_is_zero",r64(C+0xc8),0);
 eq("consumer_publishes_distinct_slot",r64(CG),C);eq("consumer_does_not_replace_asset_publication",r64(G),A);
 eq("consumer_lea_selects_channel1_bit21",r32(BITSET+4),1u<<21);eq("consumer_lea_does_not_read_header15",r8(C+0x15),0xa5);
 eq("consumer_message_payload_unchanged",r64(MSG+8),0xa5a5a5a5a5a5a55aull);
 /* Stop exactly at original layout-service call. This verifies original gate/arguments,
  * not the expensive child-tree/UI behavior following it. */
 reset();w32(C+0xc4,0);w64(G,0);eq("consumer_null_asset_does_not_rebuild",consumer_gate(),0);
 w64(G,A);w32(A+0xc0,0);w32(C+0xc0,1);eq("consumer_gate_uses_asset_not_own_status",consumer_gate(),0);
 w32(A+0xc0,0x100);eq("consumer_requires_low_bit_not_any_nonzero_status",consumer_gate(),0);
 w32(A+0xc0,1);w64(A+0xd0,R2);w32(C+0xc0,0);eq("consumer_ready_asset_reaches_layout_boundary",consumer_gate(),1);
 eq("layout_receives_consumer_not_asset",seen_consumer,C);eq("layout_receives_asset_d0_value",seen_resource,R2);eq("layout_selector_is_five",seen_tag,5);
 w32(C+0xc4,1);seen_resource=0;eq("already_built_consumer_skips_rebuild",consumer_gate(),0);
 /* Actual pooled allocation preserves backing slot tail beyond declared object extent. */
 reset();pending=1;memset((void*)POOL,0xa5,0x120);w32(POOL+0x40,0);w8(POOL+0xa2,0);
 uintptr_t allocated=((New)0x244f50)(0xd8,0x394070,0);eq("small_asset_uses_native_pool_slot",allocated,POOL);
 eq("native_pool_does_not_call_heap",heap_calls,0);eq("pool_backing_tail_preserved",filled(POOL+0xd8,0x48,0xa5),1);eq("native_pool_sets_header_pool_bit",r32(POOL+0x40)&0x4000,0x4000);
 reset();w64(G,A);w64(CG,0);((void (ABI*)(uint32_t))0x394530)(0x7a);
 eq("separate_consumer_allocation_extent",heap_size,0x1d0);eq("separate_consumer_handler",r64(C),0x3939b0);eq("wrapper_passes_low_byte_message_argument",r8(C+0xc0),0x7a);
 eq("consumer_creation_retains_asset_slot",r64(G),A);eq("consumer_creation_publishes_consumer_slot",r64(CG),C);eq("consumer_size_does_not_clear_beyond_extent",filled(C+0x1d0,0x70,0xa5),1);
 reset();((void (ABI*)(uint32_t))0x394530)(7);eq("consumer_factory_requires_existing_asset",heap_calls,0);
 printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);return failures?1:0;
}
