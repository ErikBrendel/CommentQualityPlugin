package training;

import java.io.File;
import java.util.List;

/**
 * Representation of a locally cloned git repository.
 */
public class GitRepo {

    public static String REPO_URL_START = "https://github.com/";
    public static String REPO_URL_END = ".git";

    private final String name;

    public GitRepo(String name) {
        this.name = name;
    }

    public void Update() {
        if (!isCloned()) {
            System.out.println("cloning " + name + ", this may take a while...");
            cloneRepo();
        } else {
            System.out.println("updating " + name + "...");
            System.out.println(new ExternalProgram(rootDirectory()).runJoined("git pull"));
        }
    }

    /**
     * find all the java files in that repository and add them as task into the given list
     *
     * @param tasks the list to add the tasks to
     */
    public void enqueueTasks(TrainingTaskList tasks) {
        List<String> foundFiles = new ExternalProgram(rootDirectory()).runArgs("find", ".", "-name", "*.java");
        for (String filename : foundFiles) {
            if ("".equals(filename)) continue;

            if (filename.startsWith("./")) {
                filename = filename.substring(2);
            }

            tasks.enqueue(rootDirectory(), filename);
        }
    }

    private void cloneRepo() {
        File root = rootDirectory();
        FileUtil.mkdirs(root);
        String gitUrl = REPO_URL_START + name + REPO_URL_END;
        System.out.println(ExternalProgram.Anywhere.runArgsJoined("git", "clone", gitUrl, root.getAbsolutePath()));
    }

    private File _rootDirectory = null;

    private File rootDirectory() {
        if (_rootDirectory == null) {
            _rootDirectory = new File(TrainingMain.REPO_CLONE_PATH + name.replaceAll("/", "-") + "/");
        }
        return _rootDirectory;
    }

    private boolean isCloned() {
        File root = rootDirectory();
        return root.exists() && root.isDirectory() && root.list().length > 0;
    }
}
