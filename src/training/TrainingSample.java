package training;

import core.CommentQualityAnalysisResult;

import java.util.List;

public class TrainingSample {
    private final List<String> comment;
    private final List<String> code;
    private final CommentQualityAnalysisResult.Result classification;

    public TrainingSample(List<String> comment, List<String> code, CommentQualityAnalysisResult.Result classification) {
        this.comment = comment;
        this.code = code;
        this.classification = classification;
    }

    @Override
    public String toString() {
        return list(comment) + ";" + list(code) + ";" + classification;
    }

    private static String list(List<String> data) {
        return data.stream()
                .map(s -> s.replaceAll(";", "_").replaceAll(",", "_"))
                .reduce((accu, next) -> accu + "," + next).orElse("");
    }
}
