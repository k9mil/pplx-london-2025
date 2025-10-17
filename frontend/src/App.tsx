import { Upload, X } from "lucide-react";
import * as React from "react";
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

function App() {
  const [files, setFiles] = React.useState<File[]>([]);
  const [isProcessing, setIsProcessing] = React.useState(false);

  const onFileValidate = React.useCallback(
    (file: File): string | null => {
      // Validate max files
      if (files.length >= 5) {
        return "You can only upload up to 5 files";
      }

      // Validate file type (images and documents)
      const allowedTypes = ["image/", "application/pdf", "text/"];
      if (!allowedTypes.some((type) => file.type.startsWith(type))) {
        return "Only images, PDFs, and text files are allowed";
      }

      // Validate file size (max 10MB)
      const MAX_SIZE = 10 * 1024 * 1024; // 10MB
      if (file.size > MAX_SIZE) {
        return `File size must be less than ${MAX_SIZE / (1024 * 1024)}MB`;
      }

      return null;
    },
    [files]
  );

  const handleBeginProcess = () => {
    setIsProcessing(true);
  };

  if (isProcessing) {
    return <ProcessingView />;
  }

  return (
    <div className="min-h-screen bg-white flex items-center justify-center p-8">
      <div className="w-full max-w-md">
        <div className="flex justify-center mb-8">
          <img src="/logo.png" alt="Space Logo" className="h-12 w-auto" />
        </div>
        <FileUpload
          value={files}
          onValueChange={setFiles}
          onFileValidate={onFileValidate}
          accept="image/*,application/pdf,text/*"
          maxFiles={5}
          className="w-full"
          multiple
        >
          <FileUploadDropzone>
            <div className="flex flex-col items-center gap-1">
              <div className="flex items-center justify-center rounded-full border border-gray-200 p-2.5">
                <Upload className="size-6 text-muted-foreground" />
              </div>
              <p className="font-medium text-sm">Drag & drop files here</p>
              <p className="text-muted-foreground text-xs">
                Or click to browse (max 5 files)
              </p>
            </div>
            <FileUploadTrigger asChild>
              <Button variant="outline" size="sm" className="mt-2 w-fit">
                Browse files
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
                Begin process
              </Button>
            </div>
          )}
        </FileUpload>
      </div>
    </div>
  );
}

export default App;
