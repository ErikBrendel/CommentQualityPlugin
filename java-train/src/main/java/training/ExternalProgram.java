package training;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Utility class for executing external programs (like python scripts).
 * One can specify a working directory, or just use the "Anywhere" - constant.
 * All "run" - methods take command line parameters and return the stdout of the program.
 */
public class ExternalProgram {

    public static final ExternalProgram Anywhere = new ExternalProgram(null);

    private File workingDirectory = null;

    public ExternalProgram(File workingDirectory) {
        this.workingDirectory = workingDirectory;
    }

    public List<String> run(String command) {
        return runArgs(command.split(" "));
    }

    public List<String> runArgs(String... args) {
        try {
            Process process = new ProcessBuilder(args).directory(workingDirectory).start();
            InputStream is = process.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);
            String line;

            List<String> outputLines = new ArrayList<>();
            while ((line = br.readLine()) != null) {
                outputLines.add(line);
            }
            return outputLines;
        } catch (IOException e) {
            e.printStackTrace();
            return Collections.emptyList();
        }
    }

    public String runArgsJoined(String... args) {
        return String.join("\n", runArgs(args));
    }

    public String runJoined(String command) {
        return String.join("\n", run(command));
    }
}
