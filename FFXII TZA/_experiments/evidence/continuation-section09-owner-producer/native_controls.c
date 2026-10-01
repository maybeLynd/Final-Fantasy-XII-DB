/* SECTION-09: original source-owner initialization/arming/allocation/submission and bounded recovery.
 * Linux x86-64 host, Microsoft x64 ABI, private original PE image and synthetic state.
 * One diagnostic formatter substitution and three CRT import bridges; no IO or live game.
 * Real queue producer and terminal-state pump run. Service status is fixture-supplied; read issuance and OS IO do not run.
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
static uintptr_t ownrec(unsigned group,unsigned index){return 0x2b581a0+(group*16+index)*0x1c;}
static void request_delete(unsigned group,unsigned index){((void(ABI*)(int,int))0x3dd420)(group,index);}

static void all_init(void){((void(ABI*)(void))0x3dd7e0)();}
static void group_init(unsigned g){((void(ABI*)(unsigned))0x3dd790)(g);}
static int arm(unsigned g,unsigned i,uint32_t tag){return ((int(ABI*)(unsigned,unsigned,uint32_t))0x3dda20)(g,i,tag);}
static void produce(void){((void(ABI*)(void))0x3dd4c0)();}
static uintptr_t resolve(uint32_t h){return ((uintptr_t(ABI*)(uint32_t))0x36b130)(h);}
static void destroy(uint32_t h){((void(ABI*)(uint32_t))0x369800)(h);}
static void queue_init(void){((void(ABI*)(void))0x32e450)();}
static uintptr_t slot(unsigned g){return 0x2098e10+g*0x288;}
static uintptr_t data(unsigned g){return H+0x400000+g*0x2000;}
static uint32_t pending(unsigned g){return r32(0x2b58a60+g*4);}
static void prepare(unsigned g,unsigned i,int selector,int size,int off,int hold){
 reset();bank_setup(32,0);queue_init();all_init();
 memset((void*)0x22c6d18,0,0x30);memset((void*)0x2098e10,0,0xca8);
 w8(0x2add930,0);w8(0x2add931,0);w8(0x2b5e111,0);
 for(unsigned k=0;k<4;k++){w64(0x22c6e70+k*8,data(k));w8(data(k),1);}
 w8(0x22c6d18+g,1);w32(0x22c6d28+g*4,(uint32_t)selector);
 if(g<4){w32(data(g)+8+i*8,(uint32_t)off);w32(data(g)+12+i*8,(uint32_t)size);}
 w8(slot(g)+0x201,(uint8_t)hold);
 if(!arm(g,i,0x1234ABCD)){fputs("fixture arm failed\n",stderr);exit(2);}
}
static unsigned arena_of(uintptr_t p){return p>=P11&&p<P11+PS?11:p>=P6&&p<P6+PS?6:99;}
static uintptr_t exhaust(unsigned a){uintptr_t d=0x22d7fd0+a*0xa8,h=r64(d+0x90);if(!h){fputs("no free block to exhaust\n",stderr);exit(2);}return alloc(r32(h+0x18),a);}
static void abandon_queue_and_free(uintptr_t r){uint32_t h=r32(r);queue_init();if(h)destroy(h);}
static void init_and_arm(void){
 reset();phase="original_init";memset((void*)0x2b581a0,0xA7,0x8c0);memset((void*)0x2b58a60,0xD9,20);all_init();
 int good=1,keep=1;for(unsigned g=0;g<5;g++)for(unsigned i=0;i<16;i++){
  uintptr_t r=ownrec(g,i);good &=r64(r)==0 &&r8(r+0xc)==g&&r8(r+0xd)==0&&r16(r+0xe)==i;
  keep &=r32(r+8)==0xA7A7A7A7 && r64(r+0x10)==0xA7A7A7A7A7A7A7A7ULL&&r32(r+0x18)==0xA7A7A7A7;
 }
 eq("initializes_all_80_identity_state_route_records",good,1);eq("initializer_preserves_annotation_and_old_request_bytes",keep,1);
 good=1;for(unsigned g=0;g<5;g++)good&=pending(g)==0;eq("initializer_clears_exactly_five_pending_masks",good,1);
 uintptr_t r=ownrec(1,3);eq("arm_inactive_returns_one",arm(1,3,0x11223344),1);eq("arm_sets_only_own_pending_bit",pending(1),8);
 eq("arm_enters_state2",r32(r+4),2);eq("arm_retains_annotation_at_08",r32(r+8),0x11223344);
 eq("rearm_nonzero_state_refuses",arm(1,3,0x87654321),0);eq("refusal_preserves_annotation",r32(r+8),0x11223344);
 for(unsigned st=1;st<=5;st++){w32(r+4,st);char n[100];snprintf(n,sizeof n,"arming_state_%u_refused",st);eq(n,arm(1,3,7),0);}
 w32(ownrec(2,15)+4,4);w32(ownrec(2,15),0x1234);w32(0x2b58a68,0xFFFF);group_init(2);
 eq("one_group_init_clears_its_pending",pending(2),0);eq("one_group_init_clears_last_record",r64(ownrec(2,15)),0);
 eq("one_group_init_preserves_other_group_mask",pending(1),8);eq("one_group_init_preserves_other_group_state",r32(r+4),5);
}
static void normal_production(void){
 for(unsigned g=0;g<4;g++){
  unsigned i=g?15:0;prepare(g,i,2,0x420,0x1234,0);phase="normal_producer";
  uintptr_t r=ownrec(g,i);unsigned depth=r32(0x22d89c0),sel=r32(0x22d89bc);
  produce();uint32_t h=r32(r);uintptr_t p=resolve(h),q=r64(0x22c51c0);char n[120];
  #define C(label,a,e) do{snprintf(n,sizeof n,"group%u_%s",g,label);eq(n,(a),(e));}while(0)
  C("submitted_state3",r32(r+4),3);C("tagged_real_source_allocated",p!=0&&allocated(p),1);
  C("uses_arena6",arena_of(p),6);C("pending_bit_consumed",pending(g),0);C("route_byte_zero",r8(r+0xd),0);
  C("restores_arena_stack_depth",r32(0x22d89c0),depth);C("restores_selected_arena",r32(0x22d89bc),sel);
  C("source_is_pinned",r8(p-0x2b)&2,0);C("source_alloc_class_one",r8(p-0x29),1);
  C("request_kind",r16(r+0x10),g?8:5);C("mapped_index_plus_one",r16(r+0x12),g?9:7);
  C("size_from_index_metadata",r32(r+0x14),0x420);C("offset_from_index_metadata",r32(r+0x18),0x1234);
  C("queue_has_destination",q?r64(q+0x70):0,p);C("queue_offset_is_aligned",q?r32(q+0x2c):0,0x1000);
  C("callback_argument_is_owner_address",q?r32(q+0x60):0,r);C("queue_has_original_completion",q?r64(q+0x40):0,0x3dd850);
  C("annotation_does_not_choose_file_id",r32(r+8),0x1234ABCD);
  abandon_queue_and_free(r);C("allocation_reclaimed_by_fixture_cleanup",usage(6),0);
  #undef C
 }
}
static void deferral_and_routes(void){
 prepare(1,2,4,0x400,0,1);phase="hold_state1";uintptr_t r=ownrec(1,2);produce();uintptr_t p=resolve(r32(r));
 eq("hold_has_allocated_pinned_source",p!=0&&allocated(p)&&!(r8(p-0x2b)&2),1);
 eq("hold_enters_state1_without_queue",r32(r+4)==1&&r64(0x22c51c0)==0,1);eq("hold_clears_pending_bit",pending(1),0);
 w8(slot(1)+0x201,0);produce();eq("changing_hold_flag_does_not_automatically_submit",r32(r+4)==1&&r64(0x22c51c0)==0,1);
 request_delete(1,2);eq("prepared_owner_deletion_reclaims_source",allocated(p),0);
 for(unsigned variant=0;variant<3;variant++){
  prepare(1,2,4,0x400,0,1);phase="optional_arena";r=ownrec(1,2);w8(slot(1)+0x17,0x40);w8(0x2add930,2);w8(0x2add931,variant==2);
  uintptr_t filler=variant==1?exhaust(11):0;unsigned depth=r32(0x22d89c0);produce();p=resolve(r32(r));char n[100];
  snprintf(n,sizeof n,"arena_variant%u_actual_arena",variant);eq(n,arena_of(p),variant==0?11:6);
  snprintf(n,sizeof n,"arena_variant%u_route_receipt",variant);eq(n,r8(r+0xd),variant==0?1:0);
  snprintf(n,sizeof n,"arena_variant%u_balanced_stack",variant);eq(n,r32(0x22d89c0),depth);
  request_delete(1,2);if(filler)release(filler);
 }
}
static void failure_and_rearm(void){
 prepare(1,7,2,0x400,0,1);phase="producer_failure_latched_bit";uintptr_t r=ownrec(1,7);w8(0x22c6d18+1,0);produce();
 eq("missing_group_source_sets_state0",r32(r+4),0);eq("failed_selection_keeps_pending_bit",pending(1),0x80);
 w8(0x22c6d18+1,1);produce();eq("pending_bit_alone_does_not_retry",r32(r+4)==0&&r32(r)==0,1);
 eq("explicit_rearm_after_selection_failure_allowed",arm(1,7,0x44),1);produce();
 eq("explicit_rearm_reaches_prepared_state",r32(r+4),1);eq("explicit_rearm_clears_latched_bit",pending(1),0);request_delete(1,7);
 for(int len=0;len>=-1;len--){prepare(2,4,3,len,0,1);phase="nonpositive_length";produce();char n[100];
  snprintf(n,sizeof n,"length%d_inactive_with_pending",len);eq(n,r32(ownrec(2,4)+4)==0&&pending(2)==16&&r32(ownrec(2,4))==0,1);}
 prepare(4,15,2,0x400,0,1);phase="fifth_group_has_no_size_provider";produce();
 eq("fifth_group_size_accessor_rejects_before_allocation",r32(ownrec(4,15)+4)==0&&pending(4)==0x8000&&usage(6)==0&&usage(11)==0,1);
 prepare(1,7,2,0x400,0,1);phase="actual_allocator_exhaustion";r=ownrec(1,7);w8(slot(1)+0x17,0x40);w8(0x2add930,2);
 uintptr_t f11=exhaust(11),f6=exhaust(6);unsigned depth=r32(0x22d89c0);produce();
 eq("both_arenas_exhausted_owner_returns_inactive",r32(r+4),0);eq("allocation_failure_keeps_pending",pending(1),0x80);
 eq("allocation_failure_restores_arena_stack",r32(0x22d89c0),depth);eq("failed_allocation_does_not_create_handle",r32(r),0);
 release(f11);release(f6);produce();eq("freeing_capacity_does_not_rearm_state0",r32(r+4)==0&&r32(r)==0,1);
 eq("rearm_after_allocation_failure_allowed",arm(1,7,99),1);produce();eq("rearmed_request_can_use_recovered_capacity",r32(r+4)==1&&arena_of(resolve(r32(r)))==11,1);request_delete(1,7);
}
static void selectors_and_reuse(void){
 prepare(1,3,0x2000,0x400,0,0);phase="narrowed_negative_file_index";uintptr_t r=ownrec(1,3);produce();
 eq("file_index_is_low_word_plus_one",r16(r+0x12),0x8001);
 eq("signed_index_rejection_still_owner_state3",r32(r+4),3);
 eq("rejected_submission_has_no_queue",r64(0x22c51c0),0);eq("producer_consumes_pending_despite_queue_rejection",pending(1),0);
 eq("rejected_submission_retains_allocation_pin",allocated(resolve(r32(r)))&&!(r8(resolve(r32(r))-0x2b)&2),1);
 request_delete(1,3);eq("delete_after_rejected_submit_defers",r32(r+4),5);abandon_queue_and_free(r);
 prepare(1,3,2,0x400,0,1);phase="state2_deletion_is_not_cancel";r=ownrec(1,3);request_delete(1,3);
 eq("delete_does_not_cancel_armed_state2",r32(r+4)==2&&pending(1)==8,1);produce();eq("producer_still_processes_after_state2_delete",r32(r+4),1);request_delete(1,3);
 prepare(1,3,2,0x400,0,0);phase="reuse_after_real_completion";r=ownrec(1,3);produce();uintptr_t oldp=resolve(r32(r));uint32_t oldh=r32(r);uintptr_t q=r64(0x22c51c0);
 request_delete(1,3);eq("cannot_rearm_while_deferred_delete_pending",arm(1,3,0x77),0);
 ((void(ABI*)(uintptr_t))0x32e330)(q);eq("completion_frees_old_source_before_rearm",allocated(oldp),0);
 eq("completion_clears_state_but_keeps_old_number",r32(r+4)==0&&r32(r)==oldh,1);
 queue_init();eq("arm_after_completion_allowed",arm(1,3,0x77),1);produce();
 eq("fresh_allocation_can_reuse_the_same_numeric_handle",r32(r),oldh);eq("reused_handle_resolves_to_live_allocation",allocated(resolve(r32(r))),1);eq("new_request_reuses_same_owner_callback_address",r32(r64(0x22c51c0)+0x60),r);
 abandon_queue_and_free(r);
}

static void service_fixture(void){
 /* Supply a completed/pending service state, do not launch or emulate disk I/O. */
 w32(0x2ca6068,0);w64(0x215e6e0,0);w8(0x2ad9e00,0);
 memset((void*)0x2b5d0b0,0,0x1010);w8(0x2b5e111,0);
}
static void pump(void){((void(ABI*)(void))0x32e070)();}
static void pump_outcomes(void){
 for(unsigned outcome=0;outcome<3;outcome++){
  prepare(1,5,2,0x400,0,0);phase="original_pump_terminal_owner";produce();
  uintptr_t r=ownrec(1,5),q=r64(0x22c51c0),p=resolve(r32(r));uint32_t id=r32(q+0x64);
  memset((void*)p,0,0x400);memcpy((void*)p,"TEST",4);w32(p+8,0x400);memcpy((void*)(p+0x10),"pump-owner",11);
  service_fixture();w8(q+0x20,3);w32(0x215eff4,0xffffffff);pump();
  char n[120];
  #define P(label,a,e) do{snprintf(n,sizeof n,"outcome%u_%s",outcome,label);eq(n,(a),(e));}while(0)
  P("pending_service_preserves_request",r64(0x22c51c0),q);P("pending_service_does_not_publish",r32(r+4),3);
  if(outcome==2){((void(ABI*)(uint32_t))0x32e590)(id);P("queue_cancel_enters_state4",r8(q+0x20),4);P("queue_cancel_erases_completion",r64(q+0x40),0);}
  w32(0x215eff4,outcome==1?(uint32_t)-2:0);pump();
  P("terminal_pump_recycles_request",r64(0x22c51c0),0);P("terminal_slot_id_invalidated",r32(q+0x64),0xffffffff);
  if(outcome==0){
   P("success_owner_state4",r32(r+4),4);P("success_unpins_source",r8(p-0x2b)&2,2);P("success_registers_bank_entry",r32(H+0x2000+0x58),1);
   request_delete(1,5);P("published_owner_cleanup_frees_backing",allocated(p),0);
  }else{
   P("error_or_cancel_leaves_owner_state3",r32(r+4),3);P("error_or_cancel_retains_source_pin",r8(p-0x2b)&2,0);
   P("error_or_cancel_source_still_allocated",allocated(p),1);P("error_or_cancel_no_bank_entry",r32(H+0x2000+0x58),0);
   P("producer_bit_already_consumed",pending(1),0);produce();P("producer_does_not_resubmit_state3",r64(0x22c51c0),0);
   request_delete(1,5);P("owner_delete_after_queue_retirement_waits_in_state5",r32(r+4),5);
   P("state5_not_rearmed_by_public_arm",arm(1,5,0),0);
   destroy(r32(r)); /* Explicit fixture recovery, not a claimed engine error policy. */
  }
  P("fixture_cleanup_returns_arena_usage_to_zero",usage(6)|usage(8)|usage(11),0);
  #undef P
 }
}


static void full_sweep(void){
 for(unsigned capacity=32;capacity<=128;capacity*=4){
  prepare(0,0,2,0x80,0,0);phase="five_group_sweep";
  /* Reinitialize an EMPTY fixture arena with declared handle-slot capacity. */
  ((void(ABI*)(unsigned,uintptr_t,unsigned,unsigned))0x369d30)(6,P6,PS,capacity);
  for(unsigned g=0;g<5;g++){
   w8(0x22c6d18+g,1);w32(0x22c6d28+g*4,2);
   for(unsigned i=0;i<16;i++){
    if(g<4){w32(data(g)+8+i*8,i*0x800);w32(data(g)+12+i*8,0x80);}
    if(g||i)arm(g,i,g*100+i);
   }
  }
  produce();unsigned n=0;uintptr_t q=r64(0x22c51c0);int order=1;unsigned expected=capacity==32?32:64;
  while(q&&n<=64){order &=r32(q+0x60)==ownrec(n/16,n%16);q=r64(q+0x10);n++;}
  char name[100];
  #define F(label,a,e) do{snprintf(name,sizeof name,"slots%u_%s",capacity,label);eq(name,(a),(e));}while(0)
  F("enqueues_as_many_as_handle_capacity_allows",n,expected);F("submission_order_group_then_index",order&&q==0,1);
  int groups=1,last=1;for(unsigned g=0;g<4;g++){
   groups &=pending(g)==(g<expected/16?0u:0xffffu);
   for(unsigned i=0;i<16;i++)groups &=r32(ownrec(g,i)+4)==(g<expected/16?3u:0u);
  }
  for(unsigned i=0;i<16;i++)last &=r32(ownrec(4,i)+4)==0&&r32(ownrec(4,i))==0;
  F("first_four_group_masks_and_states",groups,1);F("fifth_group_rejected_records_inactive",last,1);F("fifth_group_pending_remain",pending(4),0xffff);
  F("only_successful_handles_consume_payload_usage",usage(6),expected*0x80);
  queue_init();for(unsigned g=0;g<4;g++)for(unsigned i=0;i<16;i++)destroy(r32(ownrec(g,i)));
  F("all_fixture_backing_reclaimed",usage(6)|usage(8)|usage(11),0);
  #undef F
 }
}

static void mutate(uintptr_t a,const unsigned char*old,const unsigned char*replacement,size_t n){
 if(memcmp((void*)a,old,n)){fputs("variant preimage mismatch\n",stderr);exit(2);}
 memcpy((void*)a,replacement,n);
}
static void apply_variant(void){
 if(!mutant)return;
 if(!strcmp(mutant,"init_only_four_groups")){mutate(0x003DD83B,(const unsigned char[]){0x83,0xfa,0x05},(const unsigned char[]){0x83,0xfa,0x04},3);return;}
 if(!strcmp(mutant,"arm_prepared_instead_of_pending")){mutate(0x003DDA4E,(const unsigned char[]){0xc7,0x44,0x08,0x04,0x02,0x00,0x00,0x00},(const unsigned char[]){0xc7,0x44,0x08,0x04,0x01,0x00,0x00,0x00},8);return;}
 if(!strcmp(mutant,"skip_pending_consumption")){mutate(0x003DD672,(const unsigned char[]){0x41,0x21,0x07},(const unsigned char[]){0x90,0x90,0x90},3);return;}
 if(!strcmp(mutant,"skip_file_index_increment")){mutate(0x003DD618,(const unsigned char[]){0x66,0xff,0xc0},(const unsigned char[]){0x90,0x90,0x90},3);return;}
 if(!strcmp(mutant,"offset_uses_length_accessor")){mutate(0x003DD621,(const unsigned char[]){0xe8,0x3a,0x1c,0xf5,0xff},(const unsigned char[]){0xe8,0x6a,0x1c,0xf5,0xff},5);return;}
 if(!strcmp(mutant,"resolve_without_pinning")){mutate(0x003DD5EC,(const unsigned char[]){0xe8,0x0f,0xca,0xf8,0xff},(const unsigned char[]){0xe8,0x3f,0xdb,0xf8,0xff},5);return;}
 if(!strcmp(mutant,"preferred_arena_is_default")){mutate(0x003DD59E,(const unsigned char[]){0x8d,0x48,0x09},(const unsigned char[]){0x8d,0x48,0x04},3);return;}
 if(!strcmp(mutant,"ignore_deferral_gate")){mutate(0x003DD636,(const unsigned char[]){0x74,0x09},(const unsigned char[]){0xeb,0x09},2);return;}
 if(!strcmp(mutant,"positive_errors_deliver_success_callback")){mutate(0x0032E386,(const unsigned char[]){0x75,0x0c},(const unsigned char[]){0x90,0x90},2);return;}
 if(!strcmp(mutant,"skip_sixteenth_pending_slot")){mutate(0x003DD68A,(const unsigned char[]){0x41,0x83,0xfe,0x10},(const unsigned char[]){0x41,0x83,0xfe,0x0f},4);return;}
 fputs("unknown variant\n",stderr);exit(2);
}
int main(int argc,char**argv){
 if(argc<2||argc>3)return 2;
 mutant=argc==3?argv[2]:NULL;load(argv[1]);apply_variant();printf("{\"cases\":[\n");
 init_and_arm();normal_production();deferral_and_routes();failure_and_rearm();selectors_and_reuse();pump_outcomes();full_sweep();
 printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);return failures?1:0;
}
