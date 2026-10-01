// @category GFZ
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.*;
import ghidra.program.model.symbol.*;
import java.util.*;
public class ReportFunctionBrief extends GhidraScript {
 public void run() throws Exception {
  AddressSpace sp=currentProgram.getAddressFactory().getDefaultAddressSpace();
  FunctionManager fm=currentProgram.getFunctionManager(); Listing l=currentProgram.getListing();
  for(String s:getScriptArgs()){
   long e=Long.parseUnsignedLong(s,16); Function f=fm.getFunctionContaining(sp.getAddress(e));
   String tgt="null"; if(f!=null&&f.getThunkedFunction(false)!=null)tgt=f.getThunkedFunction(false).getEntryPoint().toString();
   println("ADDR="+s+" FUNC="+(f==null?"null":f.getEntryPoint()+" "+f.getName()+" thunk="+f.isThunk()+" tgt="+tgt));
   if(f!=null){InstructionIterator it=l.getInstructions(f.getBody(),true);while(it.hasNext()){
    Instruction i=it.next();StringBuilder rr=new StringBuilder();for(Reference x:i.getReferencesFrom())rr.append(" ").append(x.getReferenceType()).append("->").append(x.getToAddress());
    println("  "+i.getAddress()+" "+i+" flows="+Arrays.toString(i.getFlows())+" refs="+rr);
   }}
  }
 }
}
