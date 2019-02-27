package training;

import java.util.ArrayList;
import java.util.List;

public class TrainingMain {

    public static String REPO_CLONE_PATH = "/home/erik/Documents/repos/qualityCommentRepos/";
    public static String REPO_URL_START = "https://github.com/";
    public static String REPO_URL_END = ".git";
    private static String[] REPOS = { // their clone url is REPO_URL_START + this string + REPO_URL_END
            "apache/flink",
            "apache/camel"
    };

    public static void execute() {
        System.out.println(ExternalProgram.Anywhere.run("pwd"));

        TrainingTaskList taskList = new TrainingTaskList();

        List<TrainingWorker> workers = new ArrayList<>();
        for (int i = 0; i < 8; i++) {
            TrainingWorker worker = new TrainingWorker(taskList);
            worker.start();
            workers.add(worker);
        }

        for (String repoName : REPOS) {
            GitRepo repo = new GitRepo(repoName);
            repo.Update();
            repo.findAllComments(taskList);
        }

        for (TrainingWorker worker : workers) {
            while (worker.running) {
                try {
                    worker.join();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }

        System.out.println("Done!");
    }

}
