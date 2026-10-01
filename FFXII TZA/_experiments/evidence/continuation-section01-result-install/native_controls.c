#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <errno.h>
#define MS __attribute__((ms_abi,noinline))
#define HEAP ((uintptr_t)0x40000000)
#define RS (HEAP+0x1000)
#define TS (HEAP+0x3000)
#define SS (HEAP+0x5000)
#define TU (HEAP+0x8000)
#define SU (HEAP+0xa000)
#define INST (HEAP+0x10000)
static uint16_t u16(uintptr_t p){uint16_t x;memcpy(&x,(void*)p,2);return x;}
static uint32_t u32(uintptr_t p){uint32_t x;memcpy(&x,(void*)p,4);return x;}
static uint64_t u64(uintptr_t p){uint64_t x;memcpy(&x,(void*)p,8);return x;}
static void w16(uintptr_t p,uint16_t x){memcpy((void*)p,&x,2);}
static void w32(uintptr_t p,uint32_t x){memcpy((void*)p,&x,4);}
static void w64(uintptr_t p,uint64_t x){memcpy((void*)p,&x,8);}
static unsigned cases=0,failures=0;
static void ck(const char *name,int ok);
struct Hit{uintptr_t a,b,c,d,e,f,g;};
static struct Hit status[80], hp[10], layer[10];
static unsigned ns,nh,nl,nmp,nrecomp,nmeta,nrekey; static int eligibility, select_ret;
static void ck(const char *name,int ok){
 printf("%s{\"name\":\"%s\",\"pass\":%s,\"observed\":{\"status_calls\":%u,\"tail_calls\":%u,\"hp_calls\":%u,\"mp_calls\":%u,\"duration7\":%u,\"word7\":%u,\"installer_flags\":%llu,\"tracked_row0\":%u}}",cases?",\n":"",name,ok?"true":"false",ns,nrecomp,nh,nmp,u32(TS+0xbc+28),u16(TS+0x13c+14),(unsigned long long)u64(INST),u32(0x2ec1380));
 cases++;failures+=!ok;
}

static MS uintptr_t noop(void){return 0;}
static MS uintptr_t resolve(uintptr_t p){return p==TS?TU:p==SS?SU:0;}
static MS uintptr_t eligible(uintptr_t a,uintptr_t b){(void)a;(void)b;return eligibility;}
static MS uintptr_t metadata(uintptr_t a,uintptr_t b,uintptr_t c,uintptr_t d){(void)a;(void)b;(void)c;(void)d;nmeta++;return 0;}
static MS uintptr_t status_stub(uintptr_t a,uintptr_t b,uintptr_t c,uintptr_t d,uintptr_t e,uintptr_t f,uintptr_t g){if(ns<80)status[ns]=(struct Hit){a,b,c,d,e,f,g};ns++;return 0;}
static MS uintptr_t layer_stub(uintptr_t a,uintptr_t b,uintptr_t c,uintptr_t d,uintptr_t e){if(nl<10)layer[nl]=(struct Hit){a,b,c,d,e,0,0};nl++;return 0;}
static MS uintptr_t hp_stub(uintptr_t a,uintptr_t b,uintptr_t c,uintptr_t d){if(nh<10)hp[nh]=(struct Hit){a,b,c,d,0,0,0};nh++;return 0;}
static MS uintptr_t mp_stub(uintptr_t a,uintptr_t b,uintptr_t c){(void)a;(void)b;(void)c;nmp++;return 0;}
static MS uintptr_t recompute(uintptr_t a,uintptr_t b){(void)a;(void)b;nrecomp++;return 0;}
static MS uintptr_t selected(void){return select_ret;}
static MS uintptr_t inner_rekey(uintptr_t a){(void)a;nrekey++;return 0x5678;}
static MS void *memset_bridge(void *p,int b,size_t n){return memset(p,b,n);}
struct Patch{uintptr_t a;unsigned char old[12];};static struct Patch patches[64];static size_t np;
static void patch(uintptr_t a,uintptr_t fn){if(np>=64)abort();patches[np].a=a;memcpy(patches[np++].old,(void*)a,12);unsigned char j[12]={0x48,0xb8,0,0,0,0,0,0,0,0,0xff,0xe0};memcpy(j+2,&fn,8);memcpy((void*)a,j,12);}
static void unpatch_all(void){while(np){np--;memcpy((void*)patches[np].a,patches[np].old,12);}}
static void reset_case(void){memset((void*)HEAP,0,0x20000);ns=nh=nl=nmp=nrecomp=nmeta=nrekey=0;eligibility=0;select_ret=0;memset(status,0,sizeof status);memset(hp,0,sizeof hp);memset(layer,0,sizeof layer);
 w64(TU+0x698,TS);w64(SU+0x698,SS);w32(RS+0x38,0xffffffff);
 memset((void*)(RS+0x3c),0xff,6);memset((void*)(RS+0x42),0xff,16);
 memset((void*)(RS+0x5c),0xff,0xc0);memset((void*)(RS+0x11c),0xff,10);
 w32(RS+0x138,0xffffffff);w32(RS+0x13c,0xffffffff);
}
typedef void (__attribute__((ms_abi)) *Apply)(void*,void*,void*,uint32_t,uint32_t);
static void apply(uint32_t flags,int src){((Apply)(uintptr_t)0x3112f0)((void*)RS,src?(void*)SS:NULL,(void*)TS,0,flags);}
int main(int argc,char **argv){
 if(argc!=2){fprintf(stderr,"usage: native_controls FFXII_TZA.exe\n");return 2;}
 FILE*f=fopen(argv[1],"rb");if(!f){perror("exe");return 2;}fseek(f,0,SEEK_END);long n=ftell(f);rewind(f);unsigned char*raw=malloc((size_t)n);if(!raw||fread(raw,1,(size_t)n,f)!=(size_t)n)return 2;fclose(f);
 if(n<0x100||raw[0]!='M'||raw[1]!='Z')return 2;
 uint32_t pe=u32((uintptr_t)raw+0x3c);if(pe+256u>(unsigned long)n)return 2;uintptr_t opt=(uintptr_t)raw+pe+24;uintptr_t base=u64(opt+24);uint32_t size=u32(opt+56);if(base!=0x120000||size>0x10000000)return 2;
 void *img=mmap((void*)base,size,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0);if(img==MAP_FAILED){perror("map image");return 2;}
 for(unsigned i=0;i<u16((uintptr_t)raw+pe+6);i++){uintptr_t s=opt+u16((uintptr_t)raw+pe+20)+40*i;uint32_t va=u32(s+12),rs=u32(s+16),rp=u32(s+20);if((uint64_t)rp+rs>(uint64_t)n||(uint64_t)va+rs>size)return 2;memcpy((void*)(base+va),raw+rp,rs);}
 if(mmap((void*)HEAP,0x20000,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0)==MAP_FAILED){perror("heap");return 2;}
 // Each sensitivity mutation affects a private image only, never the EXE.
 const char *mu=getenv("FF12_CONTROL_MUTANT");
 if(mu && *mu){
   if(!strcmp(mu,"skip_direct_dword_copy")){if(*(uint8_t*)0x3115d4!=0x78)return 3;*(uint8_t*)0x3115d4=0xeb;}
   else if(!strcmp(mu,"suppress_applier_dirty_flag")){if(u32(0x311541)!=1)return 3;w32(0x311541,0);}
   else if(!strcmp(mu,"wrong_tracked_base")){w32(0x328ffa,(uint32_t)(0x2e81380-(0x328ff7+7)));}
   else if(!strcmp(mu,"omit_mode_failure_bit_clear")){memset((void*)0x23a633,0x90,7);}
   else return 3;
 }
 // No original input file is modified. Bridges are only in this private image.
 unsigned char *th=(void*)0x861ec0;if(th[0]!=0xff||th[1]!=0x25)return 2;int32_t d;memcpy(&d,th+2,4);w64(0x861ec0+6+d,(uintptr_t)memset_bridge);
 printf("{\"method\":\"isolated original CPU instructions; synthetic state; disclosed private boundary bridges; not live FF12\",\"cases\":[\n");
 // Tests 1: unchanged original leaf bodies (no function patches).
 typedef void (__attribute__((ms_abi))*One)(void*);typedef void(__attribute__((ms_abi))*Tracked)(int,int,int);typedef uintptr_t(__attribute__((ms_abi))*Blob)(void*,int);
 reset_case();memset((void*)INST,0xa5,0x1000);((One)(uintptr_t)0x2feab0)((void*)INST);ck("pulse_reset_clears_EAC_EB0_only",u64(INST+0xeac)==0&&u32(INST+0xea8)==0xa5a5a5a5&&u32(INST+0xeb4)==0xa5a5a5a5&&u32(INST+0x2e0)==0xa5a5a5a5);
 Tracked track=(Tracked)(uintptr_t)0x328ff0;
 memset((void*)0x2ec1368,0xa5,96);memset((void*)0x2e81380,0x6c,48);track(0,0,7);ck("tracked_code_zero_positive_index_no_write",u64(0x2ec1380)==0xa5a5a5a5a5a5a5a5ULL);
 track(0,1,7);ck("tracked_real_base_EC1380_not_E81380",u32(0x2ec1380)==7&&u32(0x2ec1384)==1&&u32(0x2e81380)==0x6c6c6c6c);
 track(1,2,9);ck("tracked_row1_stride_24",u32(0x2ec1398)==9&&u32(0x2ec139c)==2);
 uint64_t before=u64(0x2ec13b0);track(2,2,9);ck("tracked_row2_rejected",u64(0x2ec13b0)==before);
 track(0,0,-1);ck("tracked_negative_index_allows_zero_code",u32(0x2ec1380)==0xffffffff&&u32(0x2ec1384)==0);
 Blob blob=(Blob)(uintptr_t)0x2b58b0;reset_case();ck("blob_null",blob(NULL,1)==0);memcpy((void*)INST,"X\0a\0",4);ck("blob_nonzero_header_returns_base",blob((void*)INST,2)==INST);memcpy((void*)INST,"\0\0abc\0de\0",9);ck("blob_zero_index_skips_prefix",blob((void*)INST,0)==INST+2);ck("blob_second_string",blob((void*)INST,1)==INST+6);ck("blob_negative_index_returns_first",blob((void*)INST,-1)==INST+2);
 // Real reset, with its optional external cleanup callback suppressed only.
 patch(0x3105d0,(uintptr_t)noop);reset_case();memset((void*)INST,0xff,0x1000);((One)(uintptr_t)0x236a60)((void*)INST);ck("reset_real_flag_conjunction",u64(INST)==0xffef7fb9ffe7b0e1ULL);ck("reset_real_identity_pointer_clears",u64(INST+0x698)==0&&u64(INST+0x6a0)==0&&u64(INST+0xe60)==0&&u64(INST+0xe68)==0);ck("reset_real_sentinels_and_arrays",u16(INST+0x714)==0xffff&&u16(INST+0x758)==0xffff&&*(uint8_t*)(INST+0x210)==0xff&&*(uint8_t*)(INST+0x28f)==0xff&&u32(INST+0xdd4)==0&&u32(INST+0xe50)==0);ck("reset_preserves_unrelated_storage_not_total_blank",u64(INST+0xeac)==0xffffffffffffffffULL);
 // Whole installer prefix through original reset/rekey; only selection and inner key resolver bridged.
 patch(0x303ec0,(uintptr_t)selected);patch(0x3220e0,(uintptr_t)inner_rekey);typedef int(__attribute__((ms_abi))*Install)(void*,uint32_t);Install inst=(Install)(uintptr_t)0x23a570;
 reset_case();w32(0x2089300,0);w64(INST+0x698,TS);int rv=inst((void*)INST,0x200);ck("install_disabled_resets_then_returns",rv==0&&u64(INST+0x698)==0&&nrekey==0);
 reset_case();w32(0x2089300,1);w64(INST,(1ULL<<26)|(1ULL<<42));rv=inst((void*)INST,0x200);ck("install_mode2_clears_bit26_not42",rv==0&&!(u64(INST)&(1ULL<<26))&&(u64(INST)&(1ULL<<42)));ck("install_mode2_rekeys_before_rejecting",nrekey==1&&u32(INST+8)==0x5678);
 unpatch_all();
 // Whole applier unchanged. All effect sinks here are explicitly no-effect argument-recording bridges.
 patch(0x31b860,(uintptr_t)resolve);patch(0x30b9b0,(uintptr_t)eligible);patch(0x385ba0,(uintptr_t)metadata);patch(0x30e360,(uintptr_t)status_stub);patch(0x30e130,(uintptr_t)layer_stub);patch(0x30fed0,(uintptr_t)recompute);
 patch(0x300530,(uintptr_t)hp_stub);patch(0x300520,(uintptr_t)hp_stub);patch(0x300ce0,(uintptr_t)mp_stub);patch(0x300c90,(uintptr_t)mp_stub);patch(0x300bc0,(uintptr_t)noop);patch(0x30c650,(uintptr_t)noop);patch(0x3008a0,(uintptr_t)noop);patch(0x3a1180,(uintptr_t)noop);patch(0x2df220,(uintptr_t)noop);patch(0x253690,(uintptr_t)noop);patch(0x254ee0,(uintptr_t)noop);
 reset_case();apply(0,0);ck("applier_neutral_fixture_no_effect_dispatch",ns==0&&nh==0&&nl==0&&nrecomp==0&&nmeta==1);
 reset_case();w32(RS+0x5c+7*4,73);w16(RS+0xdc+7*2,12);apply(0,0);ck("copy_without_any_status_mask",u32(TS+0xbc+7*4)==73&&u16(TS+0x13c+7*2)==12&&ns==0&&nrecomp==0);
 reset_case();w32(TS+0xbc,91);w16(TS+0x13c,17);w32(RS+0x5c,0xfffffffe);w16(RS+0xdc,0x8000);apply(0,0);ck("negative_copy_values_leave_destination",u32(TS+0xbc)==91&&u16(TS+0x13c)==17);
 reset_case();w32(TS+0xbc,91);w16(TS+0x13c,17);w32(RS+0x5c,0);w16(RS+0xdc,0);apply(0,0);ck("zero_copy_values_are_present",u32(TS+0xbc)==0&&u16(TS+0x13c)==0);
 reset_case();w32(RS+0x54,1u<<7);w32(RS+0x5c+7*4,73);w16(RS+0xdc+7*2,12);apply(0,1);ck("set_mask_mode3_stats_receiver_and_source",ns==1&&status[0].a==TS&&status[0].b==SS&&status[0].c==7&&(uint32_t)status[0].d==73&&(uint32_t)status[0].e==12&&(uint32_t)status[0].g==3);
 ck("no_effect_status_sink_still_sets_tail_refresh",nrecomp==1&&u32(TS+0x64)==0&&u32(TS+0xbc+7*4)==73);
 reset_case();w32(RS+0x54,1);apply(0x200,0);ck("caller_bit9_suppresses_outer_tail_only",ns==1&&nrecomp==0);
 reset_case();w32(RS+0x58,1u<<3);apply(0,0);ck("remove_mask_mode0_zero_parameters",ns==1&&(uint32_t)status[0].g==0&&(uint32_t)status[0].d==0&&(uint32_t)status[0].e==0&&nrecomp==1);
 reset_case();*(uint8_t*)(RS+0x3c)=5;apply(0,0);ck("layer_set_mode2_minus1_argument",nl==1&&(uint32_t)layer[0].e==2&&(uint32_t)layer[0].c==0xffffffff&&nrecomp==1);
 reset_case();w32(RS+0x2c,1u<<8);w32(RS+0x24,(uint32_t)-12);apply(0,1);ck("numeric_only_has_no_outer_tail_refresh",nh==1&&hp[0].a==TS&&hp[0].c==SS&&nrecomp==0);
 reset_case();w32(RS+0x2c,(1u<<7)|(1u<<13));apply(0,1);ck("source_presence_bits7_and13",nh==1&&hp[0].a==SS&&hp[0].c==0&&nmp==1&&nrecomp==0);
 reset_case();w32(RS+0x2c,1u<<8);apply(0,1);ck("target_hp_default_flags_0x50_not_0x400",nh==1&&(uint32_t)hp[0].d==0x50);
 reset_case();w32(RS+0x2c,(1u<<8)|(1u<<19));apply(0,1);ck("target_hp_input19_maps_output8",nh==1&&(uint32_t)hp[0].d==0x150);
 reset_case();w32(RS+0x2c,(1u<<8)|(1u<<10));apply(0,1);ck("target_hp_input10_maps_output5",nh==1&&(uint32_t)hp[0].d==0x70);
 reset_case();w32(RS+0x2c,(1u<<8)|(1u<<18)|(1u<<6));apply(0,1);ck("target_hp_inverted_inputs18_6",nh==1&&(uint32_t)hp[0].d==0);
 reset_case();w32(RS+0x2c,1u<<7);apply(0,1);ck("source_hp_default_flags_0x50",nh==1&&(uint32_t)hp[0].d==0x50);
 reset_case();w32(RS+0x2c,(1u<<7)|(1u<<17)|(1u<<5));apply(0,1);ck("source_hp_inverted_inputs17_5",nh==1&&(uint32_t)hp[0].d==0);
 reset_case();w32(RS+0x2c,(1u<<7)|(1u<<9));apply(0,1);ck("source_hp_input9_maps_output5",nh==1&&(uint32_t)hp[0].d==0x70);
 reset_case();w32(RS+0x2c,1u<<31);apply(0,1);ck("bit31_not_source_hp_presence",nh==0);
 reset_case();w32(RS+0x2c,1u<<7);apply(0,0);ck("null_source_skips_source_dispatch",nh==0);
 reset_case();eligibility=1;w32(RS+0x54,1);apply(0,0);ck("eligibility_gate_precedes_metadata",ns==0&&nmeta==0);
 reset_case();eligibility=1;w32(RS+0x54,1);apply(1,0);ck("caller_bit0_bypasses_eligibility",ns==1&&nmeta==1);
 reset_case();memset((void*)RS,0xff,0x148);apply(0,0);ck("all_FF_is_NOT_a_neutral_record",ns==64&&nh==1&&nmp==1&&nrecomp==1);
 reset_case();w32(RS+0x2c,1u<<19);apply(0,0);ck("transient_metadata_bit_alone_does_not_mark_tail",nrecomp==0&&(*(uint8_t*)(TU+0xe9a)&12)==0);
 unpatch_all();
 printf("\n],\"total\":%u,\"failures\":%u}\n",cases,failures);free(raw);return failures?1:0;
}
