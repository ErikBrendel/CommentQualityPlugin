package training;

import java.io.File;
import java.text.DecimalFormat;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class TrainingTaskList {

    public static class Task {
        public final File rootDirectory;
        public final String filename;

        private Task(File rootDirectory, String filename) {
            this.rootDirectory = rootDirectory;
            this.filename = filename;
        }
    }

    private final Queue<Task> tasks = new ConcurrentLinkedQueue<>();
    private final AtomicInteger totalCount = new AtomicInteger(0);
    private final AtomicInteger doneCount = new AtomicInteger(0);
    private final AtomicBoolean listComplete = new AtomicBoolean(false);

    public void enqueue(File rootDirectory, String filename) {
        tasks.add(new Task(rootDirectory, filename));
        totalCount.incrementAndGet();
    }

    public void setListComplete() {
        listComplete.set(true);
    }

    private static final DecimalFormat PERCENT_FORMAT = new DecimalFormat("00.0");

    public Task next() {
        Task task = tasks.poll();
        if (task != null) {
            System.out.println(PERCENT_FORMAT.format(doneCount.get() * 100f / totalCount.get()) + "%  " + task.filename);
        }
        return task;
    }

    public boolean isFinished() {
        return listComplete.get() && tasks.isEmpty();
    }

    public void done() {
        doneCount.incrementAndGet();
    }
}
