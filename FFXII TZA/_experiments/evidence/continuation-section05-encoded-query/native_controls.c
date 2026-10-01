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
#define HS 0x1000000
#define Q (H+0x1000)
#define STATE (H+0x20000)
#define HIGHSTATE ((uintptr_t)0x140020000)
#define REG ((uintptr_t)0x1eebcc0)
#define ROWQR ((uintptr_t)0x22ca520)
#define IDQR ((uintptr_t)0x22ca480)
#define TEXT (H+0x30000)
#define TEXTINDEX (H+0x31000)
#define STR0 (H+0x34000)
#define STR1 (H+0x34080)
#define EMPTY ((uintptr_t)0x1ceb638)
static int expected_fault_fd=-1;
static unsigned checks,failures; static const char *mutant; static char current[128];
static unsigned char shipped[15*0x58];
static uint8_t r8(uintptr_t p){uint8_t x;memcpy(&x,(void*)p,1);return x;}
static uint16_t r16(uintptr_t p){uint16_t x;memcpy(&x,(void*)p,2);return x;}
static uint32_t r32(uintptr_t p){uint32_t x;memcpy(&x,(void*)p,4);return x;}
static uint64_t r64(uintptr_t p){uint64_t x;memcpy(&x,(void*)p,8);return x;}
static void w8(uintptr_t p,uint8_t v){memcpy((void*)p,&v,1);}
static void w16(uintptr_t p,uint16_t v){memcpy((void*)p,&v,2);}
static void w32(uintptr_t p,uint32_t v){memcpy((void*)p,&v,4);}
static void w64(uintptr_t p,uint64_t v){memcpy((void*)p,&v,8);}
static void result(const char*n,int ok,int64_t a,int64_t e){
 printf("%s{\"name\":\"%s\",\"pass\":%s,\"actual\":%lld,\"expected\":%lld}",checks?",\n":"",n,ok?"true":"false",(long long)a,(long long)e);checks++;failures+=!ok;
 if(!ok&&mutant){printf("\n],\"checks\":%u,\"failures\":%u}\n",checks,failures);exit(1);}}
static void eq(const char*n,int64_t a,int64_t e){result(n,a==e,a,e);}
static int filled(uintptr_t p,size_t n,uint8_t v){for(size_t i=0;i<n;i++)if(r8(p+i)!=v)return 0;return 1;}
static void bytes(const char*n,uintptr_t p,const void*e,size_t len){result(n,memcmp((void*)p,e,len)==0,memcmp((void*)p,e,len)==0,1);}
static void ABI *host_memset(void*p,int v,size_t n){return memset(p,v,n);}
static void on_fault(int s,siginfo_t *si,void *ctx){ucontext_t*u=ctx; if(expected_fault_fd>=0){uint64_t rec[3]={(uint64_t)s,(uintptr_t)si->si_addr,(uint64_t)u->uc_mcontext.gregs[REG_RIP]}; if(write(expected_fault_fd,rec,sizeof rec)!=(ssize_t)sizeof rec)_exit(120);_exit(0);}dprintf(2,"FAULT case=%s sig=%d addr=%p pc=%llx\n",current,s,si->si_addr,(unsigned long long)u->uc_mcontext.gregs[REG_RIP]);_exit(128+s);}
static void map_at(uintptr_t p,size_t n,int flags){if(mmap((void*)p,n,flags,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0)==MAP_FAILED){perror("map");exit(2);}}
static void load(const char *fn){FILE*f=fopen(fn,"rb");if(!f){perror(fn);exit(2);}fseek(f,0,SEEK_END);long n=ftell(f);rewind(f);unsigned char*b=malloc((size_t)n);if(!b||n<512||fread(b,1,(size_t)n,f)!=(size_t)n)exit(2);fclose(f);uintptr_t p=(uintptr_t)b;uint32_t pe=r32(p+0x3c);if(pe+256>(uint64_t)n||r32(p+pe)!=0x4550)exit(2);uintptr_t opt=p+pe+24;uint64_t base=r64(opt+24);uint32_t sz=r32(opt+56);if(r16(opt)!=0x20b||base!=0x120000||sz>0x10000000)exit(2);map_at(base,sz,PROT_READ|PROT_WRITE|PROT_EXEC);for(unsigned i=0;i<r16(p+pe+6);i++){uintptr_t s=opt+r16(p+pe+20)+40*i;uint32_t va=r32(s+12),rs=r32(s+16),off=r32(s+20);if(s+40>p+(uintptr_t)n||(uint64_t)off+rs>(uint64_t)n||(uint64_t)va+rs>sz)exit(2);memcpy((void*)(base+va),b+off,rs);}free(b);map_at(H,HS,PROT_READ|PROT_WRITE);map_at(HIGHSTATE,0x10000,PROT_READ|PROT_WRITE);memcpy(shipped,(void*)REG,sizeof shipped);w64(0x8c2a60,(uintptr_t)&host_memset);struct sigaction sa={0};sa.sa_sigaction=on_fault;sa.sa_flags=SA_SIGINFO;sigemptyset(&sa.sa_mask);sigaction(SIGSEGV,&sa,NULL);sigaction(SIGILL,&sa,NULL);sigaction(SIGBUS,&sa,NULL);}
static const uintptr_t slots[]={0x2ebf038,0x2ebf040,0x2ebf050,0x2ebf058,0x2ebf060,0x2ebf068,0x2ebf070,0x2ebf078,0x2ebf080,0x2ebf088,0x2ebf090,0x2ebf098,0x2ebf0b0,0x2ebf0c8,0x2ebf0d0,0x2ebf0d8,0x2ebf0e0,0x2ebf0e8,0x2ebf0f0,0x2ebf0f8,0x2ebf100,0x2ebf110,0x2ebf118,0x2ebf120,0x2ebf128,0x2ebf130,0x2ebf138,0x2ebf150};
static uintptr_t desc(uintptr_t slot){for(size_t i=0;i<sizeof slots/sizeof slots[0];i++)if(slots[i]==slot)return H+0x50000+i*0x100;fprintf(stderr,"unknown slot\n");exit(2);}
static uintptr_t row(uintptr_t slot,unsigned j){return r32(desc(slot)+0xc)+(uintptr_t)j*r16(desc(slot)+8);}
static void rebase(uintptr_t p){((void(ABI*)(uintptr_t))0x30b6a0)(p);}
static int valid(unsigned c,uint32_t v){return ((int(ABI*)(unsigned,uint32_t,unsigned))0x322c50)(c,v,0);}
static int fill(uintptr_t p){return ((int(ABI*)(uintptr_t))0x31c5d0)(p);}
static uintptr_t rowwrap(unsigned c,uint32_t v){return ((uintptr_t(ABI*)(unsigned,uint32_t))0x35d330)(c,v);}
static uintptr_t idwrap(unsigned c,uint16_t v){return ((uintptr_t(ABI*)(unsigned,uint16_t))0x35d380)(c,v);}
static int query0(uint16_t v){return ((int(ABI*)(uint16_t,unsigned))0x309ec0)(v,0);}
static int query1(uint16_t v){return ((int(ABI*)(uint16_t,unsigned))0x30ae30)(v,0);}
static void reset(void){memset((void*)H,0,HS);memset((void*)HIGHSTATE,0,0x10000);memcpy((void*)REG,shipped,sizeof shipped);w64(0x1f83530,0);memset((void*)0x2ebf000,0,0x200);memset((void*)0x2ec3d80,0,0xe0);memset((void*)0x2f973c0,0,0xe0);for(size_t i=0;i<sizeof slots/sizeof slots[0];i++){uintptr_t d=desc(slots[i]);w64(slots[i],d);w32(d+4,1024);w16(d+8,0x80);w32(d+0xc,(uint32_t)(H+0x100000+i*0x40000));}rebase(STATE);w64(0x2ebf190,STATE+0x59c8);w32(row(0x2ebf0f8,0)+0x28,(uint32_t)(H+0x38000));memcpy((void*)STR0,"native-name-zero",17);memcpy((void*)STR1,"native-name-one",16);memset((void*)ROWQR,0xa5,0x98);memset((void*)IDQR,0x5a,0x98);}
static uint32_t request(unsigned c){if(c>=5&&c<=18)return (c-5)*0x1000;if(c==19)return 0xe000;if(c==30||c==31)return 0xa000;return 0;}
static void req(unsigned c,uint32_t v,int word){memset((void*)Q,0xa5,0x98);w32(Q,c);if(word)w16(Q+6,(uint16_t)v);else w32(Q+4,v);}
static int wordclass(unsigned c){return(c>=5&&c<=18)||c==30||c==31||c==1;}

static unsigned char class_after[32][0x98];
static void allclass(void){for(unsigned c=1;c<=32;c++){reset();snprintf(current,sizeof current,"fill_class_%02u",c);req(c,request(c),wordclass(c));w64(Q+0x98,0xfeedface98765432ULL);int n=fill(Q),want=c==12?-2:c==19?-1:0;eq(current,n,want);memcpy(class_after[c-1],(void*)Q,0x98);snprintf(current,sizeof current,"fill_class_%02u_extent",c);eq(current,(int64_t)r64(Q+0x98),(int64_t)0xfeedface98765432ULL);}}
static void rebasing(void){
 reset();memcpy((void*)REG,shipped,sizeof shipped);memset((void*)STATE,0xa5,0x6000);uint32_t run=0;rebase(STATE);int pointers=1,prefix=1,source=1;
 for(unsigned i=0;i<15;i++){uintptr_t p=REG+i*0x58;for(unsigned j=0;j<3;j++){unsigned off=(unsigned[]){0,0x18,0x28}[j];uint64_t src;memcpy(&src,shipped+i*0x58+off,8);pointers &= r64(p+off+8)==(src?(uint32_t)(src+STATE):0);source &= r64(p+off)==src;}prefix &= r32(p+0x40)==run;run+=r32(p+0x3c);}
 eq("rebase_all_45_pointer_lanes",pointers,1);eq("rebase_all_15_prefix_sums",prefix,1);eq("rebase_total_shipped_ids",run,6892);eq("rebase_keeps_source_offsets",source,1);
 eq("rebase_zeroes_exact_512_bytes",filled(STATE+0x57c8,0x200,0),1);eq("rebase_preceding_byte_preserved",r8(STATE+0x57c7),0xa5);eq("rebase_masks_128_bytes",filled(STATE+0x59c8,0x80,0xa0),1);eq("rebase_following_byte_preserved",r8(STATE+0x5a48),0xa5);
 memset((void*)HIGHSTATE,0xa5,0x6000);memset((void*)(STATE+0x57c8),0x77,0x280);rebase(HIGHSTATE);eq("rebase_pointer_uses_low32_base",r64(REG+8),(uint32_t)(HIGHSTATE+0x4748));eq("rebase_cleanup_uses_full64_base",filled(HIGHSTATE+0x57c8,0x200,0),1);eq("rebase_high_does_not_clear_low_alias",filled(STATE+0x57c8,0x280,0x77),1);
 reset();w64(REG,0);w64(REG+8,0x123456789);w64(REG+0x18,0x100000000ULL);w64(REG+0x20,0x7777);w64(REG+0x28,0xfffffff0ULL);rebase(STATE);eq("rebase_zero_offset_preserves_old_pointer",r64(REG+8),0x123456789);eq("rebase_highhalf_only_offset_still_writes",r64(REG+0x20),(uint32_t)STATE);eq("rebase_addition_wraps32",r64(REG+0x30),(uint32_t)(STATE-16));
 w32(REG+0x3c,0xffffffff);w32(REG+0x58+0x3c,2);rebase(STATE);eq("prefix_sum_uses_wrapping32",r32(REG+2*0x58+0x40),1);
 w8(STATE+0x57c8,0xee);rebase(STATE);eq("repeat_rebase_resets_derived_state",r8(STATE+0x57c8),0);eq("repeat_rebase_not_add_to_old_pointer",r64(REG+0x30),(uint32_t)(STATE-16));
}
static void outputs_and_reuse(void){unsigned char expected[0x98],peer[0x98];
 reset();req(12,0x7000,1);memcpy(expected,(void*)Q,0x98);memset(expected+0x18,0,8);eq("class12_rejects_without_validator",fill(Q),-2);bytes("direct_rejection_only_clears_name",Q,expected,0x98);
 reset();req(19,0xeffe,0);eq("class19_valid_unimplemented_returns_minus1",fill(Q),-1);req(19,0xefff,0);eq("class19_effF_rejected",fill(Q),-2);eq("class19_validator_last_valid",valid(19,0xeffe),1);eq("class19_validator_first_invalid",valid(19,0xefff),0);
 reset();req(1,0x1000,1);eq("class1_resolves_equipment",fill(Q),0);eq("class1_rewrites_class_tag",r32(Q),6);eq("class1_preserves_overlay_low_word",r16(Q+4),0xa5a5);
 req(1,0xe000,1);eq("class1_to19_does_not_convert_word_to_dword",fill(Q),-2);eq("class1_to19_mutates_tag_before_failure",r32(Q),19);
 req(1,0xf000,1);eq("class1_bad_nibble_returns_minus2",fill(Q),-2);eq("bad_nibble_retains_original_class",r32(Q),1);
 for(unsigned c=4;c<=23;c+=(c==4?18:1)){reset();req(c,0,0);memcpy(expected,(void*)Q,0x98);memset(expected+0x18,0,8);eq(c==4?"class4_name_only_rc":c==22?"class22_name_only_rc":"class23_name_only_rc",fill(Q),0);bytes(c==4?"class4_other_bytes_preserved":c==22?"class22_other_bytes_preserved":"class23_other_bytes_preserved",Q,expected,0x98);}
 reset();req(10,0x5000,1);memcpy(expected,(void*)Q,0x98);memset(expected+0x18,0,8);uint64_t empty=EMPTY;memcpy(expected+8,&empty,8);memcpy(expected+0x10,&empty,8);memset(expected+0x20,0,16);for(unsigned k=0;k<12;k++)memset(expected+0x38+8*k,0xff,4);eq("class10_rc",fill(Q),0);bytes("class10_strided_full98_layout",Q,expected,0x98);eq("class10_tail_written_through_93",r32(Q+0x90),0xffffffff);eq("class10_gap_54_preserved",r8(Q+0x54),0xa5);eq("class10_end94_preserved",r32(Q+0x94),0xa5a5a5a5U);
 reset();memcpy(peer,(void*)IDQR,0x98);eq("row_wrapper_returns_fixed_record",rowwrap(4,0),ROWQR);bytes("row_wrapper_keeps_peer_record",IDQR,peer,0x98);eq("successful_row_wrapper_keeps_tail",r32(ROWQR+0x90),0xa5a5a5a5U);
 memcpy(peer,(void*)ROWQR,0x98);eq("id_wrapper_returns_distinct_record",idwrap(6,0x1000),IDQR);bytes("id_wrapper_keeps_row_record",ROWQR,peer,0x98);eq("id_wrapper_writes_only_high_request_word",r16(IDQR+4),0x5a5a);
 w64(IDQR+0x88,0x8877665544332211ULL);eq("id_failure_still_returns_pointer",idwrap(12,0x7000),IDQR);eq("id_failure_zeroes_full_record",filled(IDQR,0x98,0),1);
 eq("row_failure_still_returns_pointer",rowwrap(0,0),ROWQR);eq("row_failure_zeroes_full_record",filled(ROWQR,0x98,0),1);
 reset();eq("wrong_wrapper_word_for_rowclass_fails",idwrap(2,1),IDQR);eq("wrong_wrapper_failure_is_zero_record",filled(IDQR,0x98,0),1); /* stale +4 low word is intentionally nonzero */
 reset();rowwrap(4,0);w64(ROWQR+0x58,0x8877665544332211ULL);uintptr_t saved=rowwrap(22,0);eq("success_reuses_same_row_address",saved,ROWQR);eq("later_success_keeps_unassigned_bytes",r64(saved+0x58),0x8877665544332211ULL);eq("later_success_changes_prior_view",r32(saved),22);
}
static void equipment_and_inventory(void){
 reset();uintptr_t r=row(0x2ebf0f8,0);w8(r+7,2);w16(r+0x12,123);w8(r+9,0xff);w8(H+0x38000+0x13,11);w32(H+0x38000+0xc,0x12345678);w16(STATE+0x47c8,(uint16_t)(19+(3<<10)));req(6,0x1000,1);w8(Q+0x54,0xa4);eq("equipment_fill_rc",fill(Q),0);eq("equipment_bit54_sets_low_bit",r8(Q+0x54),0xa5);eq("equipment_price_from_row12",r32(Q+0x28),123);eq("equipment_queries_available",r32(Q+0x20),16);eq("equipment_queries_total",r32(Q+0x24),19);eq("equipment_subrecord_byte",r8(Q+0x3c),11);eq("equipment_subrecord_dword",r32(Q+0x44),0x12345678);eq("equipment_subtype0_keeps_tail",r32(Q+0x58),0xa5a5a5a5U);
 w8(r+7,0);eq("equipment_refill_rc",fill(Q),0);eq("equipment_bit54_clears_only_low_bit",r8(Q+0x54),0xa4);
 /* Exhaust the 27 defined category inputs plus one default while checking only bit54 behavior. */
 int flags=1;for(unsigned k=0;k<28;k++){w8(r+9,(uint8_t)(k==27?255:k));w8(r+7,2);req(6,0x1000,1);w8(Q+0x54,0x7e);flags&=fill(Q)==0&&r8(Q+0x54)==0x7f;}eq("equipment_all_category_arms_write_flag_bit",flags,1);
 reset();r=row(0x2ebf0f8,0);w8(r+7,2);idwrap(6,0x1000);eq("equipment_id_record_low_flag_set",r8(IDQR+0x54)&1,1);idwrap(12,0x7000);eq("equipment_prior_flag_erased_on_failure",r8(IDQR+0x54),0);
 reset();w16(STATE+0x4748,(uint16_t)(19+(3<<10)));eq("packed_query_mode0",query0(0),16);eq("packed_query_mode1",query1(0),19);w16(STATE+0x4748,(uint16_t)(3+(7<<10)));eq("packed_available_can_be_negative",query0(0),-4);eq("packed_total_independent",query1(0),3);w16(STATE+0x4f10,1);eq("bitset_mode0",query0(0x3000),1);eq("bitset_mode1",query1(0x3000),1);eq("query_absent_handler_returns_zero",query0(0x9000),0);eq("query_count_refusal_returns_zero",query0(0x1040+420),0);eq("query_FFFF_returns_minus1",query0(0xffff),-1);eq("query_bad_nibble_returns_minus1",query1(0xf000),-1);
}
static void strings_and_partial_fields(void){
 reset();w64(0x2ebf170,TEXT);w32(TEXT+4,TEXTINDEX);w32(TEXTINDEX+4,STR0);w32(TEXTINDEX+8,STR1);uintptr_t r=row(0x2ebf130,0);w16(r+0x30,1);req(2,0,0);eq("row_name_decode_rc",fill(Q),0);eq("row_name_decode_second_string",r64(Q+0x18),STR1);w16(r+0x30,0);eq("row_name_repeat_rc",fill(Q),0);eq("row_name_changes_to_first_string",r64(Q+0x18),STR0);eq("old_name_bytes_not_owned_by_query",memcmp((void*)STR1,"native-name-one",15),0);
 w64(0x2ebf170,0);eq("missing_text_bank_not_validation_failure",fill(Q),0);eq("missing_text_bank_null_name",r64(Q+0x18),0);
 /* Real description helper, real relative-address helper; synthetic descriptor chain. */
 w64(0x2ec3d80,1);w64(0x2f973c0,H+0x36000);w32(H+0x36004,2);w32(H+0x36014,TEXT);w32(TEXT+4,TEXTINDEX);w32(TEXTINDEX+4,STR0);w32(TEXTINDEX+8,STR1);
 r=row(0x2ebf138,0);w16(r,0);w16(r+0x2e,1);w32(r+0xc,0x300);w8(r+0x13,9);req(20,0,0);eq("action_fill_rc",fill(Q),0);eq("action_secondary_string_at08",r64(Q+8),STR0);eq("action_description_at10",r64(Q+0x10),STR1);eq("action_two_bit_field_from_row0C",r32(Q+0x20),3);eq("action_zero_parameter_preserves24",r32(Q+0x24),0xa5a5a5a5U);eq("action_zero_parameter_preserves28",r32(Q+0x28),0xa5a5a5a5U);eq("action_byte30_not_dword",r32(Q+0x30),0xa5a5a509U);
 w8(r+0xa,7);w8(r+0x1e,5);fill(Q);eq("action_kind5_writes28",r32(Q+0x28),7);eq("action_kind5_keeps24",r32(Q+0x24),0xa5a5a5a5U);w8(r+0x1e,4);fill(Q);eq("action_other_kind_writes24",r32(Q+0x24),7);
 reset();r=row(0x2ebf128,0);req(21,0,0);fill(Q);eq("command_description_is_at08",r64(Q+8),EMPTY);eq("command_does_not_fill10",r64(Q+0x10),0xa5a5a5a5a5a5a5a5ULL);
 reset();r=row(0x2ebf110,0);req(24,0,0);fill(Q);eq("school_has_secondary_string08",r64(Q+8),EMPTY);
 reset();r=row(0x2ebf118,0);w16(r+6,0x2000);w8(r+0x24,0xd);req(26,0,0);w8(Q+0x25,0xe0);fill(Q);eq("status_mask_preserves_upper_three_bits",r8(Q+0x25),0xfb);w16(r+6,0);w8(r+0x24,0);fill(Q);eq("status_mask_clears_only_low_five",r8(Q+0x25),0xe0);
 reset();r=row(0x2ebf038,0);w16(r+0xa,0x1234);w16(r+0xc,0x5678);w8(r+7,9);req(25,0,0);fill(Q);eq("licence_query_28_from_row0A",r16(Q+0x28),0x1234);eq("licence_query_2A_from_row0C",r16(Q+0x2a),0x5678);eq("licence_25_does_not_write36",r8(Q+0x36),0xa5);req(32,0,0);fill(Q);eq("licence_32_writes36",r8(Q+0x36),9);eq("licence_32_keeps_description",r64(Q+0x10),0xa5a5a5a5a5a5a5a5ULL);
 reset();r=row(0x2ebf068,0);w16(r,11);w16(r+2,12);w16(r+4,13);w16(r+6,21);w16(r+8,22);w16(r+0xa,23);req(15,0xa000,1);fill(Q);eq("bundle15_uses_first_triple",r16(Q+0x38),11);req(30,0xa000,1);fill(Q);eq("bundle30_alias_uses_first_triple",r16(Q+0x38),11);req(31,0xa000,1);fill(Q);eq("bundle31_uses_second_triple",r16(Q+0x38),21);eq("bundle31_second_triple_end",r16(Q+0x3c),23);
}


static void keyitem_partitions(void){
 reset();w32(desc(0x2ebf090)+4,64);w32(desc(0x2ebf088)+4,32);w32(desc(0x2ebf080)+4,416);w32(desc(0x2ebf078)+4,16);
 const uint16_t ids[]={0x8000,0x803f,0x8040,0x805f,0x8060,0x81ff};const uintptr_t cells[]={0x2ebf090,0x2ebf090,0x2ebf088,0x2ebf088,0x2ebf080,0x2ebf080};const unsigned js[]={0,63,0,31,0,415};
 for(unsigned k=0;k<6;k++){uintptr_t r=row(cells[k],js[k]);w16(r+2,(uint16_t)(100+k));w8(r+4,(uint8_t)(20+k));req(13,ids[k],1);char n[90];snprintf(n,sizeof n,"keyitem_%04X_rc",ids[k]);eq(n,fill(Q),0);snprintf(n,sizeof n,"keyitem_%04X_correct_subtable",ids[k]);eq(n,r32(Q+0x30),100+k);}
 req(13,0x8200,1);eq("fourth_key_descriptor_extends_validity",valid(13,0x8200),1);eq("fourth_key_range_fill_returns_success",fill(Q),0);eq("fourth_key_range_leaves_table_outputs",r32(Q+0x30),0xa5a5a5a5U);eq("fourth_key_range_still_writes_sentinel",r32(Q+0x28),0xffffffffU);
}
static void additional_boundaries(void){
 reset();uintptr_t r=row(0x2ebf100,0);w16(r+0xa,543);w64(0x1f83530,0x100000000ULL);req(5,0,1);eq("query_row_add_truncates_decoder_high_half",fill(Q),0);eq("query_row_is_low32_alias",r32(Q+0x28),543);
 reset();w32(desc(0x2ebf130)+0xc,0);req(2,0,0);eq("name_only_class2_allows_zero_row_base",fill(Q),0);eq("name_only_class2_zero_row_name",r64(Q+0x18),0);
 /* Caller-selected absence is controlled: each fault executes in a disposable child. */
 const unsigned classes[2]={5,6};const uintptr_t cells[2]={0x2ebf100,0x2ebf0f8};const uint64_t pcs[2]={0x31c81a,0x31c981};const uint64_t addresses[2]={0xa,0x12};
 for(unsigned k=0;k<2;k++){int fd[2];if(pipe(fd))exit(2);fflush(stdout);pid_t child=fork();if(child<0)exit(2);if(child==0){close(fd[0]);expected_fault_fd=fd[1];reset();w32(desc(cells[k])+0xc,0);req(classes[k],request(classes[k]),1);(void)fill(Q);_exit(99);}close(fd[1]);uint64_t rec[3]={0};ssize_t got=read(fd[0],rec,sizeof rec);close(fd[0]);int status=0;if(waitpid(child,&status,0)!=child)exit(2);char name[100];snprintf(name,sizeof name,"null_row_class%u_fault_receipt",classes[k]);eq(name,got==sizeof rec&&WIFEXITED(status)&&WEXITSTATUS(status)==0,1);snprintf(name,sizeof name,"null_row_class%u_fault_address",classes[k]);eq(name,rec[1],addresses[k]);snprintf(name,sizeof name,"null_row_class%u_original_site",classes[k]);eq(name,rec[2],pcs[k]);}
}
static void mutate(const char*n){mutant=n;if(!n)return;
 if(!strcmp(n,"equipment_flag")){if(r8(0x31ca47)!=0x30)exit(2);memset((void*)0x31ca47,0x90,3);}
 else if(!strcmp(n,"tail_six")){if(r32(0x31cf52)!=12)exit(2);w32(0x31cf52,6);}
 else if(!strcmp(n,"rebase_64bit")){if(r8(0x30b6c8)!=0x41)exit(2);w8(0x30b6c8,0x49);}
 else if(!strcmp(n,"failure_short_clear")){if(r32(0x35d3b4)!=0x98)exit(2);w32(0x35d3b4,0x64);}
 else if(!strcmp(n,"derived_mask")){if(r8(0x30b752)!=0xf8)exit(2);w8(0x30b752,0xff);}
 else if(!strcmp(n,"class19_upper")){if(r32(0x322f69)!=0xefff)exit(2);w32(0x322f69,0xf000);}
 else if(!strcmp(n,"clear_wrong_output")){if(r8(0x31c5f3)!=0x18)exit(2);w8(0x31c5f3,0x10);}
 else {fprintf(stderr,"unknown mutant\n");exit(2);}}
static void dumps(void){printf(",\"class_record_hex\":{");for(unsigned i=0;i<32;i++){printf("%s\"%u\":\"",i?",":"",i+1);for(unsigned j=0;j<0x98;j++)printf("%02x",class_after[i][j]);printf("\"");}printf("}");}
int main(int argc,char**argv){if(argc<2||argc>3)return 2;load(argv[1]);mutate(argc==3?argv[2]:NULL);printf("{\"cases\":[\n");allclass();rebasing();outputs_and_reuse();equipment_and_inventory();strings_and_partial_fields();keyitem_partitions();additional_boundaries();printf("\n],\"checks\":%u,\"failures\":%u",checks,failures);dumps();printf("}\n");return failures?1:0;}
