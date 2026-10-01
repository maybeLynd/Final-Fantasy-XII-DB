/* SECTION-10: nonempty PRF registration and specialized payload relocation/lifetime.
 * Linux x86-64 host, Microsoft x64 ABI, private original PE image and synthetic state.
 * One diagnostic formatter substitution and three CRT import bridges; no IO or live game.
 * Original registration/section selection, nonempty A00 subtype-0 fixup, original movement/refresh and teardown.
 * File contents/metadata/config and bank capacity are controlled; no live IO or rendering.
 * Mutants alter private mapped instructions only. See REVIEW.md and run_review.py.
 */
#define _GNU_SOURCE
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <asm/prctl.h>
#include <signal.h>
#include <ucontext.h>
#define ABI __attribute__((ms_abi))
#define H ((uintptr_t)0x40000000)
#define P6 ((uintptr_t)0x30000000)
#define P8 ((uintptr_t)0x31000000)
#define P11 ((uintptr_t)0x32000000)
#define PS 0x200000
#define TEB ((uintptr_t)0x43000000)
static unsigned checks,failures,formats;


static const char*phase="init";
static const char*mutant;


static uint8_t r8(uintptr_t p){
    uint8_t v;
    memcpy(&v,(void*)p,1);
    return v;
}
static uint16_t r16(uintptr_t p){
    uint16_t v;
    memcpy(&v,(void*)p,2);
    return v;
}
static uint32_t r32(uintptr_t p){
    uint32_t v;
    memcpy(&v,(void*)p,4);
    return v;
}
static uint64_t r64(uintptr_t p){
    uint64_t v;
    memcpy(&v,(void*)p,8);
    return v;
}
static void w8(uintptr_t p,uint8_t v){
    memcpy((void*)p,&v,1);
}
static void w16(uintptr_t p,uint16_t v){
    memcpy((void*)p,&v,2);
}
static void w32(uintptr_t p,uint32_t v){
    memcpy((void*)p,&v,4);
}
static void w64(uintptr_t p,uint64_t v){
    memcpy((void*)p,&v,8);
}
static void eq(const char*n,int64_t a,int64_t e){
    int ok=a==e;
    printf("%s{\"name\":\"%s\",\"pass\":%s,\"actual\":%lld,\"expected\":%lld}",checks?",\n":"",n,ok?"true":"false",(long long)a,(long long)e);
    checks++;
    failures+=!ok;
    if(!ok&&mutant){
        printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);
        exit(1);
    }
}
static void*ABI msset(void*p,int c,size_t n){
    return memset(p,c,n);
}
static void*ABI mscopy(void*p,const void*s,size_t n){
    uintptr_t d=(uintptr_t)p,a=(uintptr_t)s;
    if(n && d<a+n && a<d+n && d!=a){
        /* Overlap behavior is a separate import boundary: never silently emulate
         * the original Windows memcpy for an overlapping case. */
        fprintf(stderr,"overlapping memcpy requires separate CRT evidence\n");exit(3);
    }
    return memcpy(p,s,n);
}
static char* ABI mscopyname(char*d,const char*s,size_t n){
    size_t i=0;
    for(;i<n&&s[i];i++)d[i]=s[i];
    for(;i<n;i++)d[i]=0;
    return d;
}
static int ABI fmt(uintptr_t dst,uintptr_t format,uintptr_t a,uintptr_t b){
    (void)format;
    (void)a;
    (void)b;
    formats++;
    w8(dst,0);
    return 0;
}
static void patch(uintptr_t p,uintptr_t fn){
    unsigned char a[12]={
        0x48,0xb8
    }
    ;
    memcpy(a+2,&fn,8);
    a[10]=0xff;
    a[11]=0xe0;
    memcpy((void*)p,a,12);
}
static void fault(int n,siginfo_t*i,void*ctx){
    ucontext_t*u=ctx;
    dprintf(2,"fault phase=%s sig=%d addr=%p rip=%llx\n",phase,n,i->si_addr,(unsigned long long)u->uc_mcontext.gregs[REG_RIP]);
    _exit(128+n);
}
static void map(uintptr_t p,size_t n,int prot){
    if(mmap((void*)p,n,prot,MAP_ANONYMOUS|MAP_PRIVATE|MAP_FIXED_NOREPLACE,-1,0)==MAP_FAILED){
        perror("mmap");
        exit(2);
    }
}
static void load(const char*path){
    FILE*f=fopen(path,"rb");
    if(!f){
        perror(path);
        exit(2);
    }
    fseek(f,0,SEEK_END);
    long len=ftell(f);
    rewind(f);
    unsigned char*b=malloc((size_t)len);
    if(!b||len<512||fread(b,1,(size_t)len,f)!=(size_t)len)exit(2);
    fclose(f);
    uintptr_t q=(uintptr_t)b;
    uint32_t pe=r32(q+0x3c);
    if(pe+256>(uint64_t)len||r32(q+pe)!=0x4550)exit(2);
    uintptr_t op=q+pe+24;
    uintptr_t base=r64(op+24);
    uint32_t size=r32(op+56);
    if(r16(op)!=0x20b||base!=0x120000||size>0x10000000)exit(2);
    map(base,size,PROT_READ|PROT_WRITE|PROT_EXEC);
    for(unsigned j=0;j<r16(q+pe+6);j++){
        uintptr_t s=op+r16(q+pe+20)+j*40;
        uint32_t va=r32(s+12),rs=r32(s+16),ra=r32(s+20);
        if(s+40>q+(uintptr_t)len||(uint64_t)ra+rs>(uint64_t)len||(uint64_t)va+rs>size)exit(2);
        memcpy((void*)(base+va),b+ra,rs);
    }
    free(b);
    map(H,0x1000000,PROT_READ|PROT_WRITE);
    map(P6,PS,PROT_READ|PROT_WRITE);
    map(P8,PS,PROT_READ|PROT_WRITE);
    map(P11,PS,PROT_READ|PROT_WRITE);
    map(TEB,0x1000,PROT_READ|PROT_WRITE);
    if(syscall(SYS_arch_prctl,ARCH_SET_GS,TEB))exit(2);
    w64(TEB+0x10,0);
    w64(0x8c2a60,(uintptr_t)msset);
    w64(0x8c2a68,(uintptr_t)mscopy);
    w64(0x8c2f70,(uintptr_t)mscopyname);
    patch(0x17d2e0,(uintptr_t)fmt);
    struct sigaction sa={
        0
    }
    ;
    sa.sa_sigaction=fault;
    sa.sa_flags=SA_SIGINFO;
    sigemptyset(&sa.sa_mask);
    sigaction(SIGSEGV,&sa,NULL);
    sigaction(SIGBUS,&sa,NULL);
    sigaction(SIGILL,&sa,NULL);
    sigaction(SIGTRAP,&sa,NULL);
    sigaction(SIGFPE,&sa,NULL);
}
static void init_arena(unsigned k,uintptr_t p){
    ((void(ABI*)(unsigned,uintptr_t,unsigned,unsigned))0x369d30)(k,p,PS,32);
}
static void select_arena(unsigned k){
    ((void(ABI*)(unsigned,unsigned))0x36c1d0)(k,10);
}
static void pop(void){
    ((void(ABI*)(void))0x36c140)();
}
static uintptr_t alloc(size_t n,unsigned k){
    select_arena(k);
    uintptr_t p=((uintptr_t(ABI*)(unsigned))0x36a100)((unsigned)n);
    pop();
    if(!p){
        fprintf(stderr,"allocation null\n");
        exit(2);
    }
    return p;
}
static void release(uintptr_t p){
    ((void(ABI*)(uintptr_t))0x3697f0)(p);
}
static int allocated(uintptr_t p){
    return (r16(p-0x40)==0xff12)&&(r8(p-0x2c)&1);
}
static uint32_t usage(unsigned k){
    uint32_t a=0;
    for(unsigned j=0;j<9;j++)a+=r32(0x22d7fd0+k*0xa8+0x68+j*4);
    return a;
}
static void reset(void){
    phase="reset";
    memset((void*)H,0,0x1000000);
    memset((void*)P6,0xA5,PS);
    memset((void*)P8,0xA5,PS);
    memset((void*)P11,0xA5,PS);
    memset((void*)0x22d7fd0,0,0x1000);
    memset((void*)0x20910a0,0,0x1200);
    memset((void*)0x2ebcd80,0,0xe40);
    memset((void*)0x2ebef70,0,0x50);
    memset((void*)0x2f97340,0,0x10);
    memset((void*)0x2ec32c4,0,0x10);
    w64(0x1f83530,0);
    w64(0x22c6f28,H+0x100000);
    w32(H+0x100000+0x48800,0xffffffff);
    init_arena(6,P6);
    init_arena(8,P8);
    init_arena(11,P11);
    select_arena(8);
    formats=0;
    memset((void*)0x2b581a0,0,0x8e0);
    memset((void*)0x22c31c0,0,0x2040);
    w8(0x2b62e10,1); w64(H+0x100000+0x48830,H+0x180000);

}
static uintptr_t bank_setup(unsigned capacity,unsigned occupied){
 uintptr_t b=H+0x2000,slot=H+0x3000,page=H+0x4000,entry=H+0x5000;
 w64(b+0x38,slot);w64(b+0x10,page);w32(b+0x40,occupied?0:0xffffffff);w32(b+0x44,occupied?0:0xffffffff);
 w32(b+0x48,0x50);w32(b+0x4c,5);w32(b+0x50,31);w32(b+0x54,capacity);w32(b+0x58,occupied);
 w8(b,1);w16(b+0x22,1);w32(b+0x18,0xffffffff);
 for(unsigned i=0;i<32;i++){w32(slot+i*16,0xffffffff);w32(slot+i*16+4,0xffffffff);w32(slot+i*16+8,0xffffffff);}
 if(occupied)w32(slot,0);
 w32(page+0x10,(uint32_t)entry);w32(page+0x14,occupied);
 ((void(ABI*)(uintptr_t))0x409710)(entry);
 w64(H+0x180000+0xd90,b);return b;
}

static uint32_t halloc(unsigned n){select_arena(6);uint32_t h=((uint32_t(ABI*)(unsigned))0x36b160)(n);pop();if(!h)exit(2);return h;}
static uintptr_t resolve(uint32_t h){return ((uintptr_t(ABI*)(uint32_t))0x36b130)(h);}
static void destroy(uint32_t h){((void(ABI*)(uint32_t))0x369800)(h);}
static void tickets(void){for(unsigned i=0;i<64;i++){uintptr_t p=0x2ebcd80+i*0x38;w32(p,0x20000000|i);w64(p+0x20,i==63?0:p+0x38);w64(p+0x28,i?p-0x38:0);}w64(0x2ebdb88,0x2ebcd80);}
static void header(uintptr_t p,uint32_t tag,const char*name){w32(p,tag);memset((void*)(p+0x10),0,32);strncpy((char*)(p+0x10),name,31);}
static void effect(uintptr_t p,unsigned subtype){
 memset((void*)p,0,0xc0);memcpy((void*)p,(void*)0xd11c70,8);w32(p+12,0xa0);
 w32(p+0x10,0x90);w16(p+0x14,0x100);w16(p+0x16,0xa00);w32(p+0x18,0);w16(p+0x1c,1);w8(p+0x1e,subtype);
 for(unsigned i=0;i<4;i++){w32(p+0x20+i*16,0x30+i*8);w32(p+0x24+i*16,0x34+i*8);}
}
static void prf(uintptr_t p,unsigned ver){memset((void*)p,0,0x1000);header(p,0x50524640,"r00000");w32(p+4,ver);w32(p+8,0x1000);w32(p+12,2);
 unsigned b=ver?0x40:0x30;w32(p+b,0x100-b);w32(p+b+4,0x180-b);
 header(p+0x100,0x46454640,"r00000");w32(p+0x108,0x80);header(p+0x180,0x41544144,"second");w32(p+0x188,0x80);
 w32(p+0xfc,0x300);effect(p+0x300,0);
 w32(0x21641fc,0);w32(0x2ec3ee0+(5000+51)*4,0xf1);
 strcpy((char*)(H+0x90000),"no-config");w64(0x2b64380+(48*1280)*8,H+0x90000);
}

static void check(const char*prefix,const char*label,int64_t actual,int64_t expected){char n[180];snprintf(n,sizeof n,"%s_%s",prefix,label);eq(n,actual,expected);}
static int lookup(uintptr_t e,uint32_t tag,const char*name,int32_t *idx){int32_t off=42;*idx=42;((void(ABI*)(uintptr_t,uint32_t,const char*,int32_t*,int32_t*))0x409780)(e,tag,name,idx,&off);return off;}
static void setup(uintptr_t e,uintptr_t src,int mode){((void(ABI*)(uintptr_t,uintptr_t,int))0x409a60)(e,src,mode);}
static void drop(uintptr_t bank,uintptr_t src){((void(ABI*)(uintptr_t,uintptr_t))0x409d60)(bank,src);}
static void find_controls(void){
 for(unsigned v=0;v<2;v++){
  reset();phase="prf_lookup";uintptr_t p=H+0x20000,e=H+0x5000;prf(p,v);((void(ABI*)(uintptr_t))0x409710)(e);
  /* The input's short strings are terminated but their trailing bytes are dirty. */
  memset((void*)(p+0x10+8),0xA5,24);memset((void*)(p+0x100+0x10+8),0xA5,24);memset((void*)(p+0x180+0x10+8),0xA5,24);
  setup(e,p,1);w64(e+0x38,p);char tag[50];snprintf(tag,sizeof tag,"prf%u",v);int32_t ix;
  check(tag,"normalizes_root_padding",r64(p+0x28),0);check(tag,"normalizes_child_padding",r64(p+0x128),0);
  check(tag,"effect_section_offset",lookup(e,0x46454640,"r00000",&ix),0x100);check(tag,"effect_section_index",ix,0);
  check(tag,"second_section_offset",lookup(e,0x41544144,"second",&ix),0x180);check(tag,"second_section_index",ix,1);
  check(tag,"wrong_name_not_found",lookup(e,0x46454640,"other",&ix),-1);check(tag,"failed_index_reset",ix,-1);
  check(tag,"wildcard_selects_root",lookup(e,0,NULL,&ix),0);check(tag,"PRF_root_offset_valid_index_stays_minus1",ix,-1);
  check(tag,"ALL_literal_selects_named_child",lookup(e,0x4c4c4140,"second",&ix),0x180);
  ((void(ABI*)(uintptr_t))0x409730)(e);
 }
 reset();phase="sparse_prf1";uintptr_t p=H+0x20000,e=H+0x5000;prf(p,1);w32(p+0x40,0);w32(p+0x44,0x100-0x40);setup(e,p,1);w64(e+0x38,p);int32_t ix;
 eq("sparse_zero_offset_skipped",lookup(e,0x46454640,"r00000",&ix),0x100);eq("sparse_result_keeps_authored_index",ix,1);
 w32(p+4,2);eq("unsupported_PRF_version_no_match",lookup(e,0,NULL,&ix),-1);
 w32(p,0x54534554);eq("plain_header_match_offset",lookup(e,0x54534554,"r00000",&ix),0);eq("plain_header_match_index",ix,0);
 w32(e+4,2);eq("unsupported_mode_nonzero_offset_returns_offset",((intptr_t(ABI*)(uintptr_t,int))0x4096c0)(e,0x100),0x100);
 eq("unsupported_mode_zero_offset_returns_NULL",((intptr_t(ABI*)(uintptr_t,int))0x4096c0)(e,0),0);
 /* Modular addition can itself produce NULL; -1/null entry are not the only causes. */
 w32(e+4,1);w8(0x2b62e10,0);w64(e+0x38,0xFFFFFFF0ULL);eq("valid_mode_sum_wraps_to_NULL",((intptr_t(ABI*)(uintptr_t,int))0x4096c0)(e,0x10),0);
}
static void registration_cases(void){
 for(unsigned which=0;which<4;which++){
  reset();phase="nonempty_registration";tickets();uintptr_t b=bank_setup(32,0);unsigned mode=which==2?0:1;uint32_t h=mode?halloc(0x1000):0;uintptr_t p=mode?resolve(h):H+0x20000;prf(p,which==1);
  if(which==3){effect(p+0x700,0);w32(p+0xfc,0x700);}
  uintptr_t src=mode?h:p;uint16_t id=((uint16_t(ABI*)(uintptr_t,uintptr_t))0x409fe0)(b,src);uintptr_t en=H+0x5000;uint32_t t=r32(en+0x44);char tag[50];snprintf(tag,sizeof tag,"registration%u",which);
  check(tag,"bank_index",id,0);check(tag,"bank_count",r32(b+0x58),1);check(tag,"entry_mode",r32(en+4),mode);check(tag,"ticket_generation",t,0x20000040);
  uintptr_t sl=0x2ebcd80+(t&63)*0x38,c=r64(sl+0x18),back=mode?p:r64(en+0x18),off=which==3?0x700:0x300,record=back+off+0x20;
  check(tag,"ticket_uses_metadata_not_section_offset",r64(sl+8),back+off);check(tag,"context_nonnull",c!=0,1);check(tag,"context_source_base",r64(c+0x858),back+off);
  check(tag,"context_source_representation",r32(c+0x860),mode?h:back);check(tag,"lookup_names_nonempty_A00_record",r64(r64(c+0x850)+8),record);
  int all=1;for(unsigned j=0;j<4;j++){all&=r32(record+j*16)==(uint32_t)(record+0x30+j*8);all&=r32(record+4+j*16)==(uint32_t)(record+0x34+j*8);}
  check(tag,"specialized_nonzero_relocations",all,1);check(tag,"specialized_first_word",r32(record),record+0x30);check(tag,"specialized_second_word",r32(record+4),record+0x34);
  check(tag,"registration_writes_index",r16(record+0x42),1);check(tag,"registration_writes_subtype",r8(record+0x44),0);
  if(!mode)check(tag,"copy_mode_does_not_relocate_original_payload",r32(p+off+0x20),0x30);
  uint32_t before=r32(record);unsigned oldusage=usage(8);
  check(tag,"same_key_returns_existing_index",((uint16_t(ABI*)(uintptr_t,uintptr_t))0x409fe0)(b,src),0);
  check(tag,"same_key_does_not_relocate_twice",r32(record),before);check(tag,"same_key_keeps_ticket",r32(en+0x44),t);check(tag,"same_key_allocates_no_context",usage(8),oldusage);
  drop(b,mode?h:back);check(tag,"bank_removed",r32(b+0x58),0);check(tag,"context_reclaimed",allocated(c),0);check(tag,"arena8_empty",usage(8),0);
  if(mode){check(tag,"external_source_preserved",allocated(p),1);destroy(h);}else check(tag,"copied_backing_reclaimed",allocated(back),0);
  check(tag,"source_arena_empty",usage(6),0);check(tag,"no_diagnostics",formats,0);
 }
}
static void limited_successes(void){
 for(unsigned k=0;k<3;k++){
  reset();tickets();uintptr_t b=bank_setup(32,0);uint32_t h=halloc(0x1000);uintptr_t p=resolve(h);prf(p,1);char tag[50];snprintf(tag,sizeof tag,"limited%u",k);phase="limited_success";
  if(k==0)header(p+0x100,0x46454640,"different");
  if(k==1)w64(0x2ebdb88,0);
  if(k==2)memcpy((void*)(p+0x300),"INVALID!",8);
  check(tag,"entry_admitted",((uint16_t(ABI*)(uintptr_t,uintptr_t))0x409fe0)(b,h),0);
  check(tag,"bank_count",r32(b+0x58),1);
  if(k==0){check(tag,"missing_named_FEF_leaves_no_ticket",r32(H+0x5044),0xffffffff);check(tag,"no_context_allocated",usage(8),0);}
  if(k==1){check(tag,"ticket_exhaustion_stores_zero",r32(H+0x5044),0);check(tag,"no_context_allocated",usage(8),0);}
  if(k==2){uint32_t t=r32(H+0x5044);check(tag,"bad_signature_still_has_ticket",t,0x20000040);uintptr_t c=r64(0x2ebcd80+(t&63)*0x38+0x18);check(tag,"bad_signature_lookup_empty",r64(r64(c+0x850)+8),0);}
  drop(b,h);destroy(h);check(tag,"all_owned_allocations_reclaimed",usage(6)+usage(8),0);
 }
}
static void repeated_registration(void){
 reset();phase="repeat_same_mutated_source";tickets();uintptr_t b=bank_setup(32,0);uint32_t h=halloc(0x1000);uintptr_t p=resolve(h);prf(p,0);
 ((uint16_t(ABI*)(uintptr_t,uintptr_t))0x409fe0)(b,h);uintptr_t record=p+0x320;uint32_t first=r32(record);drop(b,h);
 eq("disposing_context_does_not_unrelocate_borrowed_bytes",r32(record),first);
 ((uint16_t(ABI*)(uintptr_t,uintptr_t))0x409fe0)(b,h);
 eq("re_registering_mutated_source_adds_base_again",r32(record),(uint32_t)(first+record));drop(b,h);destroy(h);eq("repeat_registration_cleanup",usage(6)+usage(8),0);
}
static void specialized_move(void){
 reset();phase="nonempty_specialized_move";tickets();uintptr_t b=bank_setup(32,0),hole=alloc(0x1000,6),sep=alloc(0x100,6);uint32_t h=halloc(0x1000);uintptr_t p=resolve(h);prf(p,1);
 ((uint16_t(ABI*)(uintptr_t,uintptr_t))0x409fe0)(b,h);uint32_t t=r32(H+0x5044);uintptr_t c=r64(0x2ebcd80+(t&63)*0x38+0x18);release(hole);
 eq("original_compactor_moves_nonempty_source",((int(ABI*)(unsigned,int))0x369c60)(6,0),1);uintptr_t q=resolve(h),record=q+0x320;
 eq("new_backing_is_prior_hole",q,hole);eq("source_context_stale_before_refresh",r64(c+0x858),p+0x300);eq("nested_word_stale_before_refresh",r32(record),p+0x350);
 ((void(ABI*)(uintptr_t,uintptr_t))0x3b3480)(c,0);
 eq("refresh_updates_nonempty_context",r64(c+0x858),q+0x300);eq("refresh_relocates_lookup",r64(r64(c+0x850)+8),record);
 eq("refresh_relocates_specialized_first_word",r32(record),record+0x30);eq("refresh_relocates_specialized_second_word",r32(record+4),record+0x34);
 eq("refresh_preserves_record_identity",r16(record+0x42),1);eq("old_run_origin_remains_stale",r64(c+0x878),p+0x310);
 ((void(ABI*)(uintptr_t,uintptr_t))0x3b3480)(c,0);eq("repeat_refresh_does_not_shift_nested_word_twice",r32(record),record+0x30);
 drop(b,h);eq("moved_context_reclaimed",allocated(c),0);eq("moved_external_backing_remains_owned",allocated(q),1);destroy(h);release(sep);eq("moved_cleanup_balanced",usage(6)+usage(8),0);
}
static void apply_variant(void){
 if(!mutant)return;
 if(!strcmp(mutant,"prf1_wrong_table_base")){unsigned char expected[]={0x83,0xc1,0x40},replacement[]={0x83,0xc1,0x30};if(memcmp((void*)0x409895,expected,sizeof expected))exit(2);memcpy((void*)0x409895,replacement,sizeof replacement);return;}
 if(!strcmp(mutant,"skip_v0_child_normalization")){unsigned char expected[]={0xe8,0x3b,0x83,0x45,0x00},replacement[]={0x90,0x90,0x90,0x90,0x90};if(memcmp((void*)0x409b80,expected,sizeof expected))exit(2);memcpy((void*)0x409b80,replacement,sizeof replacement);return;}
 if(!strcmp(mutant,"use_section_offset_instead_of_metadata")){unsigned char expected[]={0x42,0x8b,0x54,0x30,0xfc},replacement[]={0xba,0x00,0x01,0x00,0x00};if(memcmp((void*)0x40a16f,expected,sizeof expected))exit(2);memcpy((void*)0x40a16f,replacement,sizeof replacement);return;}
 if(!strcmp(mutant,"skip_specialized_first_pair")){unsigned char expected[]={0xe8,0x6c,0x00,0xf3,0xff},replacement[]={0x90,0x90,0x90,0x90,0x90};if(memcmp((void*)0x50047f,expected,sizeof expected))exit(2);memcpy((void*)0x50047f,replacement,sizeof replacement);return;}
 if(!strcmp(mutant,"skip_context_destruction")){unsigned char expected[]={0xe8,0xeb,0xbb,0xe9,0xff},replacement[]={0x90,0x90,0x90,0x90,0x90};if(memcmp((void*)0x3b3820,expected,sizeof expected))exit(2);memcpy((void*)0x3b3820,replacement,sizeof replacement);return;}
 if(!strcmp(mutant,"ignore_existing_bank_match")){unsigned char expected[]={0x0f,0x85,0xa7,0x01,0x00,0x00},replacement[]={0x90,0x90,0x90,0x90,0x90,0x90};if(memcmp((void*)0x40a024,expected,sizeof expected))exit(2);memcpy((void*)0x40a024,replacement,sizeof replacement);return;}
 if(!strcmp(mutant,"skip_nested_refresh")){unsigned char expected[]={0xe8,0xe2,0x68,0x15,0x00},replacement[]={0x90,0x90,0x90,0x90,0x90};if(memcmp((void*)0x3a9bd9,expected,sizeof expected))exit(2);memcpy((void*)0x3a9bd9,replacement,sizeof replacement);return;}
 if(!strcmp(mutant,"skip_registration_ticket_store")){unsigned char expected[]={0x89,0x47,0x44},replacement[]={0x90,0x90,0x90};if(memcmp((void*)0x40a17c,expected,sizeof expected))exit(2);memcpy((void*)0x40a17c,replacement,sizeof replacement);return;}
 fputs("unknown variant\n",stderr);exit(2);
}
int main(int argc,char**argv){if(argc<2||argc>3)return 2;load(argv[1]);if(argc==3)mutant=argv[2];apply_variant();printf("{\"cases\":[\n");find_controls();registration_cases();limited_successes();repeated_registration();specialized_move();printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);return failures?1:0;}
