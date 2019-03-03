package training;

import java.io.File;

public class FileUtil {
    public static void mkdirs(File file) {
        for (int i = 0; i < 5; i++) { // try several times because of multithreading
            if (file.exists() || file.mkdirs()) {
                return;
            }
        }
        throw new RuntimeException("Failed to create directory " + file.getAbsolutePath());
    }
}
