package training;

import java.io.File;

public class FileUtil {
    public static void mkdirs(File file) {
        if (file.exists()) return;
        if (!file.mkdirs()) {
            throw new RuntimeException("Failed to create directory " + file.getAbsolutePath());
        }
    }
}
