// @category GFZ
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.mem.Memory;
import java.io.*;import java.nio.charset.StandardCharsets;import java.security.*;import java.util.*;
public class DumpUnresolvedMechanismFeatures extends GhidraScript{
 static boolean pref(Function f,String p){for(FunctionTag t:f.getTags())if(t.getName().startsWith(p))return true;return false;}
 static boolean tag(Function f,String n){for(FunctionTag t:f.getTags())if(t.getName().equals(n))return true;return false;}
 static String dom(Function f){ArrayList<String>a=new ArrayList<>();for(FunctionTag t:f.getTags())if(t.getName().startsWith("GFZ.V121.CodeDomain."))a.add(t.getName().substring("GFZ.V121.CodeDomain.".length()));Collections.sort(a);return String.join(",",a);}
 static String hex(byte[]b){StringBuilder s=new StringBuilder();for(byte x:b)s.append(String.format("%02x",x));return s.toString();}
 static String esc(String s){return s==null?"":s.replace("\\","\\\\").replace("\t","\\t").replace("\n","\\n");}
 public void run()throws Exception{
  String[]a=getScriptArgs();if(a.length!=2)throw new IllegalArgumentException("out maxInsns");int mx=Integer.parseInt(a[1]);
  FunctionManager fm=currentProgram.getFunctionManager();Listing li=currentProgram.getListing();Memory mem=currentProgram.getMemory();MessageDigest md=MessageDigest.getInstance("SHA-256");int n=0;
  try(PrintWriter w=new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]),StandardCharsets.UTF_8))){
   w.println("entry\tname\tbody_bytes\tinsns\tsha256\tcall_insns\tcomputed_calls\tjump_insns\tcomputed_jumps\tconditional_flows\tback_edges\tdirect_callees\tall_callees_codedomain\tcallee_domains\tlast_flow\tcomment");
   for(Function f:fm.getFunctions(true)){
    if(f.isExternal()||pref(f,"GFZ.V120.PrimaryOwner.")||tag(f,"GFZ.V120.FinalNoPrimaryOwner")||pref(f,"GFZ.V121.CodeDomain."))continue;
    ArrayList<Instruction> is=new ArrayList<>();for(InstructionIterator ii=li.getInstructions(f.getBody(),true);ii.hasNext();)is.add(ii.next());if(is.size()>mx)continue;
    int calls=0,cc=0,jumps=0,cj=0,cond=0,back=0;String last="";
    for(Instruction in:is){FlowType ft=in.getFlowType();last=ft.toString();if(ft.isCall()){calls++;if(ft.isComputed())cc++;}if(ft.isJump()){jumps++;if(ft.isComputed())cj++;}if(ft.isConditional())cond++;for(Address t:in.getFlows()){if(f.getBody().contains(t)&&t.compareTo(in.getAddress())<0)back++;}}
    ArrayList<String> cs=new ArrayList<>(), ds=new ArrayList<>();boolean all=true;for(Function c:f.getCalledFunctions(monitor)){String d=dom(c);cs.add(String.format("%08X[%s]",c.getEntryPoint().getOffset(),c.getName()));ds.add(d);if(d.isEmpty()&&!pref(c,"GFZ.V120.PrimaryOwner.")&&!tag(c,"GFZ.V120.FinalNoPrimaryOwner"))all=false;}Collections.sort(cs);Collections.sort(ds);
    byte[] bb=new byte[(int)f.getBody().getNumAddresses()];int off=0;for(AddressRange r:f.getBody()){int len=(int)r.getLength();mem.getBytes(r.getMinAddress(),bb,off,len);off+=len;}md.reset();String sh=hex(md.digest(bb));
    w.printf("%08X\t%s\t%d\t%d\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%s\t%s\t%s\t%s\t%s%n",f.getEntryPoint().getOffset(),esc(f.getName()),bb.length,is.size(),sh,calls,cc,jumps,cj,cond,back,esc(String.join(";",cs)),all?"1":"0",esc(String.join(";",ds)),esc(last),esc(f.getComment()));n++;
   }
  }
  println("UNRESOLVED_MECHANISM_FEATURES_PASS total="+n+" max="+mx);
 }
}
