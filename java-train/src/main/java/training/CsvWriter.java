package training;

import java.io.*;
import java.util.List;

public class CsvWriter {

    private final BufferedWriter writer;
    private final Closeable thingToClose;
    private final File file;
    private boolean cellWritten = false;
    private int rowsWritten = 0;

    public CsvWriter(File file) {
        try {
            this.file = file;
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

    public CsvWriter writeCell(boolean data) {
        return writeCell(data ? "true" : "false");
    }

    public CsvWriter writeCell(int data) {
        return writeCell(data + "");
    }

    public CsvWriter writeCell(String data) {
        try {
            if (cellWritten) {
                writer.write(";");
            }
            data = data.replaceAll("\"", "\"\"");
            data = "\"" + data + "\"";
            writer.write(data);
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
            rowsWritten++;
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

    public int getRowsWritten() {
        return rowsWritten;
    }

    public void abort() {
        if (file.exists()) {
            if (!file.delete()) {
                throw new RuntimeException("Could not delete file. Have you called close?");
            }
        }
    }
}
