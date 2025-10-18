import { useState, useCallback } from "react";
import { ProcessingView } from "@/components/pages/ProcessingView";
import { LandingView } from "@/components/pages/LandingView";
import { FILE_UPLOAD, UI } from "@/constants";
import { uploadImage, imageToText } from "@/services/api";
import type { UploadStatus, UploadResponse, ImageDescription } from "@/types";

interface UploadedFile {
  file: File;
  status: UploadStatus;
  response?: UploadResponse;
  error?: string;
}

function App() {
  const [files, setFiles] = useState<File[]>([]);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [isLoadingDescriptions, setIsLoadingDescriptions] =
    useState<boolean>(false);
  const [imageDescriptions, setImageDescriptions] = useState<
    ImageDescription[]
  >([]);

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

  const handleBeginProcess = useCallback(async (): Promise<void> => {
    setIsUploading(true);

    const uploadResults: UploadedFile[] = [];

    const uploadPromises = files.map(async (file) => {
      const uploadedFile: UploadedFile = {
        file,
        status: "uploading",
      };

      try {
        const response = await uploadImage(file);
        const successfulUpload = {
          ...uploadedFile,
          status: "success" as UploadStatus,
          response,
        };
        uploadResults.push(successfulUpload);
        setUploadedFiles((prev) => [...prev, successfulUpload]);
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : UI.TEXT.UPLOAD_ERROR;
        const failedUpload = {
          ...uploadedFile,
          status: "error" as UploadStatus,
          error: errorMessage,
        };
        uploadResults.push(failedUpload);
        setUploadedFiles((prev) => [...prev, failedUpload]);
      }
    });

    await Promise.all(uploadPromises);
    setIsUploading(false);

    const successfulUploads = uploadResults.filter(
      (uf) => uf.status === "success" && uf.response
    );

    setIsLoadingDescriptions(true);
    const descriptions: ImageDescription[] = [];
    for (const upload of successfulUploads) {
      try {
        const fileInfo = upload.response?.data?.file;
        if (!fileInfo) continue;

        const blobName = fileInfo.blob_name || fileInfo.filename;

        if (blobName) {
          const result = await imageToText({
            blob_name: blobName,
            detail_level: "low",
          });

          if (result.success && result.description) {
            descriptions.push({
              filename: upload.file.name,
              description: result.description,
              blob_name: blobName,
            });
          }
        }
      } catch (error) {
        console.error(
          `Failed to convert image ${upload.file.name} to text:`,
          error
        );
      }
    }
    setIsLoadingDescriptions(false);

    setImageDescriptions(descriptions);
    setIsProcessing(true);
  }, [files]);

  if (isProcessing) {
    const firstUploadedUrl =
      uploadedFiles[0]?.response?.data?.file?.public_url ||
      uploadedFiles[0]?.response?.data?.file?.path;

    return (
      <ProcessingView
        imageDescriptions={imageDescriptions}
        uploadedImageUrl={firstUploadedUrl}
      />
    );
  }

  return (
    <LandingView
      files={files}
      onFilesChange={setFiles}
      onFileValidate={onFileValidate}
      uploadedFiles={uploadedFiles}
      onBeginProcess={handleBeginProcess}
      isUploading={isUploading}
      isLoadingDescriptions={isLoadingDescriptions}
    />
  );
}

export default App;
