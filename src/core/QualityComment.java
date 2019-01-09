package core;

import com.intellij.psi.PsiComment;
import org.jetbrains.annotations.NotNull;

/**
 * our model class that represents one comment in the code base that can get quality-analysed
 */
public class QualityComment {

    private final PsiComment psiComment;

    public QualityComment(@NotNull PsiComment psiComment) {
        this.psiComment = psiComment;
    }

    /**
     * @return the whole content of this comment, including the comment-creating characters
     */
    public String fullText() {
        return psiComment.getText();
    }
}
