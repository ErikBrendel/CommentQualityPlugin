package training;

import com.intellij.openapi.vfs.LocalFileSystem;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.openapi.vfs.VirtualFileSystem;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.io.*;
import java.nio.charset.StandardCharsets;

public class OtherContentFileDecorator extends VirtualFile {

    private final VirtualFile wrappedFile;
    private final String content;

    public OtherContentFileDecorator(File file, String content) {
        this.wrappedFile = LocalFileSystem.getInstance().findFileByIoFile(file);
        this.content = content;
    }

    @NotNull
    @Override
    public String getName() {
        return wrappedFile.getName();
    }

    @NotNull
    @Override
    public VirtualFileSystem getFileSystem() {
        return wrappedFile.getFileSystem();
    }

    @NotNull
    @Override
    public String getPath() {
        return wrappedFile.getPath();
    }

    @Override
    public boolean isWritable() {
        return false;
    }

    @Override
    public boolean isDirectory() {
        return false;
    }

    @Override
    public boolean isValid() {
        return true;
    }

    @Override
    public VirtualFile getParent() {
        return wrappedFile.getParent();
    }

    @Override
    public VirtualFile[] getChildren() {
        return wrappedFile.getChildren();
    }

    @NotNull
    @Override
    public OutputStream getOutputStream(Object o, long l, long l1) throws IOException {
        throw new IOException("Cannot write to OtherContentFileDecorator");
    }

    @NotNull
    @Override
    public byte[] contentsToByteArray() {
        return content.getBytes(StandardCharsets.UTF_8);
    }

    @Override
    public long getTimeStamp() {
        return wrappedFile.getTimeStamp();
    }

    @Override
    public long getLength() {
        return contentsToByteArray().length;
    }

    @Override
    public void refresh(boolean b, boolean b1, @Nullable Runnable runnable) {
        wrappedFile.refresh(b, b1, runnable);
    }

    @Override
    public InputStream getInputStream() {
        return new ByteArrayInputStream(contentsToByteArray());
    }

    @Override
    public long getModificationStamp() {
        return wrappedFile.getModificationStamp();
    }
}
