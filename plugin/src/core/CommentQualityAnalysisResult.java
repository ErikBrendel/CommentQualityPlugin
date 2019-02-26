package core;

/**
 * the result of analyzing a comments quality
 */
public class CommentQualityAnalysisResult {
    public enum Result {
        GOOD, BAD
    }

    private final Result result;
    private final String additionalInfo;

    public CommentQualityAnalysisResult(Result result, String additionalInfo) {
        this.result = result;
        this.additionalInfo = additionalInfo;
    }

    public boolean isBad() {
        return result != Result.GOOD;
    }

    public String fullMessage() {
        String msg = basicMessage();
        if (additionalInfo != null && !additionalInfo.isEmpty()) {
            msg += ": " + additionalInfo;
        }
        return msg;
    }

    private String basicMessage() {
        switch (result) {
            case GOOD: return "Good comment";
            case BAD: return "Bad comment";
        }
        return "Error";
    }
}
