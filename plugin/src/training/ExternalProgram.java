package training;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ExternalProgram {

    public static File WorkingDirectory = null;

    public static List<String> run(String command) {
        return runArgs(command.split(" "));
    }

    public static List<String> runArgs(String... args) {
        try {
            Process process = new ProcessBuilder(args).directory(WorkingDirectory).start();
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

    public static String runArgsJoined(String... args) {
        return String.join("\n", runArgs(args));
    }

    public static String runJoined(String command) {
        return String.join("\n", run(command));
    }

}
