package training;

/**
 * An object of this class is used to accumulate training results over the training process.
 * It can finally get exported to be used by the plugin.
 */
public class TrainingResults {

    public void trainOnRepo(String repoName) {
        GitRepo repo = new GitRepo(repoName);
        repo.Update();
        //todo save these results
        repo.allComments();
    }

    /**
     * @return all the accumulated knowledge
     */
    public String exportString() {
        return "";
    }
}
