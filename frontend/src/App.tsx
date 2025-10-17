import { Upload, X } from "lucide-react";
import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { ProcessingView } from "@/components/pages/ProcessingView";
import {
  FileUpload,
  FileUploadDropzone,
  FileUploadItem,
  FileUploadItemDelete,
  FileUploadItemMetadata,
  FileUploadItemPreview,
  FileUploadList,
  FileUploadTrigger,
} from "@/components/ui/file-upload";
import { FILE_UPLOAD, IMAGES, ALT_TEXT, UI } from "@/constants";

function App() {
  const [files, setFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  const onFileValidate = useCallback(
    (file: File): string | null => {
      if (files.length >= FILE_UPLOAD.MAX_FILES) {
        return FILE_UPLOAD.MESSAGES.MAX_FILES_EXCEEDED;
      }

      const isAllowedType = FILE_UPLOAD.ALLOWED_TYPES.some((type) =>
        file.type.startsWith(type)
      );

      if (!isAllowedType) {
        return FILE_UPLOAD.MESSAGES.INVALID_FILE_TYPE;
      }

      if (file.size > FILE_UPLOAD.MAX_SIZE_BYTES) {
        return FILE_UPLOAD.MESSAGES.FILE_TOO_LARGE(FILE_UPLOAD.MAX_SIZE_MB);
      }

      return null;
    },
    [files.length]
  );

  const handleBeginProcess = useCallback((): void => {
    setIsProcessing(true);
  }, []);

  if (isProcessing) {
    return <ProcessingView />;
  }

  return (
    <div className="min-h-screen bg-white flex items-center justify-center p-8">
      <div className="w-full max-w-md">
        <div className="flex justify-center mb-8">
          <img src={IMAGES.LOGO} alt={ALT_TEXT.LOGO} className="h-12 w-auto" />
        </div>

        <FileUpload
          value={files}
          onValueChange={setFiles}
          onFileValidate={onFileValidate}
          accept="image/*,application/pdf,text/*"
          maxFiles={FILE_UPLOAD.MAX_FILES}
          className="w-full"
          multiple
        >
          <FileUploadDropzone>
            <div className="flex flex-col items-center gap-1">
              <div className="flex items-center justify-center rounded-full border border-gray-200 p-2.5">
                <Upload className="size-6 text-muted-foreground" />
              </div>
              <p className="font-medium text-sm">{UI.TEXT.DRAG_DROP}</p>
              <p className="text-muted-foreground text-xs">
                {UI.TEXT.CLICK_BROWSE}
              </p>
            </div>
            <FileUploadTrigger asChild>
              <Button variant="outline" size="sm" className="mt-2 w-fit">
                {UI.LABELS.BROWSE_FILES}
              </Button>
            </FileUploadTrigger>
          </FileUploadDropzone>

          <FileUploadList>
            {files.map((file) => (
              <FileUploadItem key={file.name} value={file}>
                <FileUploadItemPreview />
                <FileUploadItemMetadata />
                <FileUploadItemDelete asChild>
                  <Button variant="ghost" size="icon" className="size-7">
                    <X />
                  </Button>
                </FileUploadItemDelete>
              </FileUploadItem>
            ))}
          </FileUploadList>

          {files.length > 0 && (
            <div className="flex justify-center mt-4">
              <Button
                variant="outline"
                size="sm"
                className="w-fit"
                onClick={handleBeginProcess}
              >
                {UI.LABELS.BEGIN_PROCESS}
              </Button>
            </div>
          )}
        </FileUpload>
      </div>
    </div>
  );
}

export default App;
