package training;

import java.io.File;

public class FileUtil {

    /**
     * Try multiple times to create a path of directories.
     * When this method correctly exits, the path exists.
     *
     * @param file the path to create
     * @throws RuntimeException if creating the path is not possible
     */
    public static void mkdirs(File file) {
        for (int i = 0; i < 5; i++) { // try several times because of multithreading
            if (file.exists() || file.mkdirs()) {
                return;
            }
        }
        throw new RuntimeException("Failed to create directory " + file.getAbsolutePath());
    }
}
