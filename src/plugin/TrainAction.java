package plugin;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import core.CommentFinder;
import core.LanguageProcessor;
import core.QualityComment;
import org.jetbrains.annotations.NotNull;
import training.TrainingMain;

import java.util.List;

public class TrainAction extends AnAction {

    public TrainAction() {
        this("TrainAction");
    }

    public TrainAction(String name) {
        super(name);
    }

    @Override
    public void actionPerformed(@NotNull AnActionEvent anActionEvent) {
        TrainingMain.main(new String[0]);
    }
}
