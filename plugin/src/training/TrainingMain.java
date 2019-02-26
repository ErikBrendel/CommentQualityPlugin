package training;

public class TrainingMain {

    public static String REPO_CLONE_PATH = "/home/erik/Documents/repos/qualityCommentRepos/";
    public static String REPO_URL_START = "https://github.com/";
    public static String REPO_URL_END = ".git";
    private static String[] REPOS = { // their clone url is REPO_URL_START + this string + REPO_URL_END
            "apache/flink",
            //"apache/camel"
    };

    public static void execute() {
        System.out.println(ExternalProgram.run("pwd"));

        int totalRepos = REPOS.length;
        int repoCount = 0;
        for (String repoName : REPOS) {
            GitRepo repo = new GitRepo(repoName);
            repo.Update();
            repo.findAllComments(repoCount, totalRepos);
            repoCount++;
        }
    }
}