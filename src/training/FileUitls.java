package training;

import java.io.File;

public class FileUitls {
    public static void mkdirs(File file) {
        if (!file.mkdirs()) {
            throw new RuntimeException("Failed to create directory " + file.getAbsolutePath());
        }
    }
}
