package plugin;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import org.jetbrains.annotations.NotNull;
import training.TrainingMain;

public class TrainAction extends AnAction {

    public TrainAction() {
        this("TrainAction");
    }

    public TrainAction(String name) {
        super(name);
    }

    @Override
    public void actionPerformed(@NotNull AnActionEvent anActionEvent) {
        TrainingMain.execute();
    }
}
