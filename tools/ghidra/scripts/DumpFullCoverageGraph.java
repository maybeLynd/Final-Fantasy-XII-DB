// @category GFZ
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.text.SimpleDateFormat;
import java.util.*;

public class DumpFullCoverageGraph extends GhidraScript {
    static String esc(String s){ if(s==null)return ""; return s.replace("\\","\\\\").replace("\t","\\t").replace("\n","\\n").replace("\r","\\r"); }
    static String owner(Function f){
        for(FunctionTag t:f.getTags()) if(t.getName().startsWith("GFZ.V120.PrimaryOwner.")) return t.getName().substring("GFZ.V120.PrimaryOwner.".length());
        return "";
    }
    static boolean finalNo(Function f){ for(FunctionTag t:f.getTags()) if(t.getName().equals("GFZ.V120.FinalNoPrimaryOwner")) return true; return false; }
    static String tags(Function f){ ArrayList<String> a=new ArrayList<>(); for(FunctionTag t:f.getTags()) a.add(t.getName()); Collections.sort(a); return String.join(";",a); }
    static String sha256(Path p) throws Exception {
        MessageDigest md=MessageDigest.getInstance("SHA-256");
        try(InputStream in=Files.newInputStream(p)){ byte[] buf=new byte[1<<20]; int n; while((n=in.read(buf))>0) md.update(buf,0,n); }
        StringBuilder sb=new StringBuilder(); for(byte b:md.digest()) sb.append(String.format("%02x",b));
        return sb.toString();
    }
    public void run() throws Exception {
        String[] a=getScriptArgs();
        if(a.length!=2 && a.length!=4) throw new IllegalArgumentException("functions.tsv edges.tsv [sidecar.json parent.gzf] required - a sidecar without the parent it names is the defect the stamp exists to catch");
        List<Function> fs=new ArrayList<>(); FunctionIterator it=currentProgram.getFunctionManager().getFunctions(true); while(it.hasNext()){Function f=it.next(); if(!f.isExternal())fs.add(f);} fs.sort(Comparator.comparingLong(f->f.getEntryPoint().getOffset()));
        long edges=0;
        try(PrintWriter fw=new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]),StandardCharsets.UTF_8)); PrintWriter ew=new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[1]),StandardCharsets.UTF_8))){
            fw.println("entry\tname\tbody_bytes\towner\tfinal_no_owner\tthunk\tnoreturn\tcomment_len\ttags");
            ew.println("caller\tcallee\tcallee_external\tcallee_name");
            for(Function f:fs){
                long bodyBytes=f.getBody().getNumAddresses(); String c=f.getComment();
                fw.printf("%08X\t%s\t%d\t%s\t%s\t%s\t%s\t%d\t%s%n",f.getEntryPoint().getOffset(),esc(f.getName()),bodyBytes,owner(f),finalNo(f),f.isThunk(),f.hasNoReturn(),c==null?0:c.length(),esc(tags(f)));
                Set<Function> called=f.getCalledFunctions(monitor); ArrayList<Function> cs=new ArrayList<>(called); cs.sort(Comparator.comparingLong(x->x.getEntryPoint().getOffset()));
                for(Function g:cs){ ew.printf("%08X\t%08X\t%s\t%s%n",f.getEntryPoint().getOffset(),g.getEntryPoint().getOffset(),g.isExternal(),esc(g.getName())); edges++; }
            }
        }
        if(a.length==4){
            // PROVENANCE STAMP. The census carries no manifest, so a wrong-generation export is
            // indistinguishable from a current one. Record what the PROGRAM says about itself
            // (name carries the generation tag; executable sha ties it to the binary) and what
            // the parent FILE measures as -- hashing the GZF here, not trusting a passed-in
            // string, because a caller-supplied sha can only ever agree with itself.
            Path gzf=Paths.get(a[3]);
            String sha=sha256(gzf); long size=Files.size(gzf);
            String utc=new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'"){{setTimeZone(TimeZone.getTimeZone("UTC"));}}.format(new Date());
            try(PrintWriter sw=new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[2]),StandardCharsets.UTF_8))){
                sw.printf("{%n  \"program_name\": \"%s\",%n  \"executable_sha256\": \"%s\",%n  \"function_count\": %d,%n  \"edge_count\": %d,%n  \"parent_gzf\": \"%s\",%n  \"parent_gzf_sha256\": \"%s\",%n  \"parent_gzf_size\": %d,%n  \"exported_utc\": \"%s\"%n}%n",
                    // The generation tag lives on the DomainFile name
                    // (..._GN161_..._2026-09-14), NOT on getName(), which returns
                    // the original executable name "FFXII_TZA.exe" forever.
                    esc(currentProgram.getDomainFile().getName()).replace("\"","\\\""),currentProgram.getExecutableSHA256(),fs.size(),edges,esc(gzf.getFileName().toString()).replace("\"","\\\""),sha,size,utc);
            }
            println("FULL_COVERAGE_GRAPH_SIDECAR parent_sha256="+sha);
        }
        println("FULL_COVERAGE_GRAPH_WRITTEN functions="+fs.size());
    }
}
