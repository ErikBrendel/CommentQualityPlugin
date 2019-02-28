package training;

import java.io.*;
import java.util.List;

public class CsvWriter {

    private final BufferedWriter writer;
    private final Closeable thingToClose;
    private boolean cellWritten = false;

    public CsvWriter(File file) {
        try {
            FileUtil.mkdirs(file.getParentFile());
            FileWriter writer = new FileWriter(file);
            thingToClose = writer;
            this.writer = new BufferedWriter(writer);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public CsvWriter writeCell(List<String> wordList) {
        return writeCell(stringifyList(wordList));
    }

    public static String stringifyList(List<String> wordList) {
        StringBuilder s = new StringBuilder();

        boolean firstDone = false;
        for (String word: wordList) {
            if (firstDone) {
                s.append(",");
            }
            firstDone = true;
            s.append(word.replaceAll(",", "_"));
        }

        return s.toString();
    }

    public CsvWriter writeCell(int data) {
        return writeCell(data + "");
    }

    public CsvWriter writeCell(String data) {
        try {
            if (cellWritten) {
                writer.write(";");
            }
            writer.write(data.replaceAll(";", "_").replaceAll("\n", "_"));
            cellWritten = true;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return this;
    }

    public void endLine() {
        try {
            cellWritten = false;
            writer.write("\n");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void close() {
        try {
            writer.close();
            thingToClose.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
