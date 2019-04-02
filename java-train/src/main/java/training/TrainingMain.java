package training;

import java.util.ArrayList;
import java.util.List;

/**
 * main entry point for finding base data:
 * Select the github repositories to use, and it will clone them and extract comments and uncommented comment-positions
 */
public class TrainingMain {

    public static String REPO_CLONE_PATH = "../../CommentRepos/";
    public static final int NUM_PARALLEL_WORKERS = 4;


    private static String[] bigRepoCollection = {
            "square/okhttp",
            "eclipse/che",
            "apache/flink",
            "apache/camel",
            "elastic/elasticsearch",
            "spring-projects/spring-boot",
            "spring-projects/spring-framework",
            "ReactiveX/RxJava",
            "kdn251/interviews",
            "square/retrofit",
            "google/guava",
            "PhilJay/MPAndroidChart",
            "owncloud/android",
            "nextcloud/android",
            "owntracks/android",
            "netty/netty",
            "skylot/jadx",
            "libgdx/libgdx", // really big
            "chrisbanes/PhotoView",
            "jenkinsci/jenkins",
            //"TheAlgorithms/Java",
    };
    private static String[] mediumRepoCollection = {
            "square/okhttp",
            "eclipse/che",
            "apache/flink",
            "apache/camel",
            "elastic/elasticsearch",
            "spring-projects/spring-boot",
            "spring-projects/spring-framework",
            "ReactiveX/RxJava",
    };
    private static String[] smallRepoCollection = {"square/okhttp"};
    private static String[] REPOS = bigRepoCollection;

    // find more at:
    // https://github.com/search?l=Java&o=desc&q=pushed%3A%3E2019-02-25&s=stars&type=Repositories


    public static void main(String[] args) {
        execute();
    }

    public static void execute() {
        TrainingTaskList taskList = new TrainingTaskList();

        List<TrainingWorker> workers = new ArrayList<>();
        for (int i = 0; i < NUM_PARALLEL_WORKERS; i++) {
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
