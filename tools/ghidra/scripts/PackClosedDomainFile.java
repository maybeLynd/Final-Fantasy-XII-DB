import ghidra.app.script.GhidraScript;
import ghidra.framework.model.*;
import java.io.File;

public class PackClosedDomainFile extends GhidraScript {
  @Override
  protected void run() throws Exception {
    String[] args = getScriptArgs();
    if (args.length != 2) throw new IllegalArgumentException("usage: <domainPath> <outputFile>");
    String domainPath = args[0];
    File out = new File(args[1]);
    Project p = state.getProject();
    if (p == null) throw new IllegalStateException("no project");
    ProjectData pd = p.getProjectData();
    DomainFile df = pd.getFile(domainPath);
    if (df == null) {
      println("PROJECT_FILES_BEGIN");
      for (DomainFile f: pd) println(f.getPathname()+" open="+f.isOpen()+" busy="+f.isBusy()+" changed="+f.isChanged());
      println("PROJECT_FILES_END");
      throw new IllegalStateException("target DomainFile not found: "+domainPath);
    }
    println("PACK_TARGET path="+df.getPathname()+" open="+df.isOpen()+" busy="+df.isBusy()+" changed="+df.isChanged()+" canSave="+df.canSave());
    if (df.isOpen()) throw new IllegalStateException("target must be closed");
    if (df.isBusy()) throw new IllegalStateException("target must not be busy");
    if (df.isChanged()) throw new IllegalStateException("target DomainFile reports changed");
    if (out.exists() && !out.delete()) throw new IllegalStateException("cannot remove old output");
    df.packFile(out, monitor);
    if (!out.isFile() || out.length() < 1024*1024) throw new IllegalStateException("pack output missing/truncated: "+out);
    println("PACK_PASS output="+out.getAbsolutePath()+" size="+out.length());
  }
}
