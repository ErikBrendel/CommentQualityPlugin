package actions;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import core.CommentFinder;
import core.LanguageProcessor;
import core.QualityComment;
import org.jetbrains.annotations.NotNull;

import java.util.List;

public class ScanCurrentFileAction extends AnAction {

    public ScanCurrentFileAction() {
        this("ScanCurrentFileAction");
    }

    public ScanCurrentFileAction(String name) {
        super(name);
    }

    @Override
    public void actionPerformed(@NotNull AnActionEvent anActionEvent) {
        List<QualityComment> comments = CommentFinder.CommentsInCurrentFile(anActionEvent);
        System.out.println("Comments: " + comments.size());
        for (QualityComment comment : comments) {
            System.out.println("----");
            System.out.println(LanguageProcessor.normalizedWordList(comment.contentString()));
        }
    }
}
