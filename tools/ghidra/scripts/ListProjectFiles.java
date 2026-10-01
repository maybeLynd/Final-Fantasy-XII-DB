// @category GFZ
// Lists every DomainFile in the open project with its lock/dirty state.
// Used by the pipeline wrappers to discover the program name, which is derived from the
// packed GZF filename and therefore changes at every checkpoint. Never hardcode it.
//
// Usage: ListProjectFiles.java [outputFile]
//   Prints:  PROJECT_FILE <path> content=<type> open=<b> busy=<b> changed=<b> canSave=<b>
//   Then:    PROJECT_FILE_COUNT <n>
import ghidra.app.script.GhidraScript;
import ghidra.framework.model.*;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class ListProjectFiles extends GhidraScript {
  @Override
  protected void run() throws Exception {
    String[] args = getScriptArgs();
    Project p = state.getProject();
    if (p == null) throw new IllegalStateException("no project");
    ProjectData pd = p.getProjectData();

    StringBuilder sb = new StringBuilder();
    int n = 0;
    for (DomainFile f : pd) {
      String line = "PROJECT_FILE " + f.getPathname()
          + " content=" + f.getContentType()
          + " open=" + f.isOpen()
          + " busy=" + f.isBusy()
          + " changed=" + f.isChanged()
          + " canSave=" + f.canSave();
      println(line);
      sb.append(line).append('\n');
      n++;
    }
    println("PROJECT_FILE_COUNT " + n);
    sb.append("PROJECT_FILE_COUNT ").append(n).append('\n');

    if (args.length > 0) {
      try (Writer w = new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)) {
        w.write(sb.toString());
      }
    }
  }
}
