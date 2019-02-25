package training;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * An object of this class is used to accumulate training results over the training process.
 * It can finally get exported to be used by the plugin.
 */
public class TrainingResults {

    private List<TrainingSample> samples = new ArrayList<>();

    public void trainOnRepo(String repoName, int repoIndex, int totalRepos) {
        GitRepo repo = new GitRepo(repoName);
        repo.Update();
        samples.addAll(repo.allComments(repoIndex, totalRepos));
    }

    /**
     * @return all the accumulated knowledge
     */
    public String exportString() {
        return samples.stream().map(TrainingSample::toString).collect(Collectors.joining("\n"));
    }
}
