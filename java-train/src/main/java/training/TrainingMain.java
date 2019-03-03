package training;

import java.util.ArrayList;
import java.util.List;

public class TrainingMain {

    public static String REPO_CLONE_PATH = "/home/erik/Documents/repos/qualityCommentRepos/";
    public static String REPO_URL_START = "https://github.com/";
    public static String REPO_URL_END = ".git";
    private static String[] REPOS = { // their clone url is REPO_URL_START + this string + REPO_URL_END
            //"apache/flink",
            //"apache/camel",
            //"elastic/elasticsearch",
            //"spring-projects/spring-boot",
            //"spring-projects/spring-framework",
            "square/okhttp", // that's a small one
    };
    // find more at:
    // https://github.com/search?l=Java&o=desc&q=pushed%3A%3E2019-02-25&s=stars&type=Repositories

    public static void main(String[] args) {
        execute();
    }

    public static void execute() {
        TrainingTaskList taskList = new TrainingTaskList();

        List<TrainingWorker> workers = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            TrainingWorker worker = new TrainingWorker(taskList);
            worker.start();
            workers.add(worker);
        }

        for (String repoName : REPOS) {
            GitRepo repo = new GitRepo(repoName);
            repo.Update();
            repo.enqueueTasks(taskList);
        }
        taskList.setListComplete();

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
