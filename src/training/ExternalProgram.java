package training;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class ExternalProgram {

    public static File WorkingDirectory = null;

    public static String run(String command) {
        return runArgs(command.split(" "));
    }

    public static String runArgs(String... args) {
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
            return String.join("\n", outputLines);
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }

}
