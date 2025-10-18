import { motion } from "framer-motion";
import { Upload, X, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { IMAGES, ALT_TEXT, UI, FILE_UPLOAD } from "@/constants";
import type { UploadStatus } from "@/types";
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

interface LandingViewProps {
  files: File[];
  onFilesChange: (files: File[]) => void;
  onFileValidate: (file: File) => string | null;
  uploadedFiles: Array<{
    file: File;
    status: UploadStatus;
    error?: string;
  }>;
  onBeginProcess: () => void;
  isUploading: boolean;
  isLoadingDescriptions: boolean;
}

export function LandingView({
  files,
  onFilesChange,
  onFileValidate,
  uploadedFiles,
  onBeginProcess,
  isUploading,
  isLoadingDescriptions,
}: LandingViewProps) {
  const allUploadsSuccessful =
    uploadedFiles.length > 0 &&
    uploadedFiles.every((uf) => uf.status === "success");

  return (
    <div className="min-h-screen bg-white relative overflow-hidden">
      {/* Background gradient */}
      <div
        className="absolute inset-0 opacity-40"
        style={{
          backgroundImage: "url('/gradient.svg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
        }}
      />

      {/* Navigation */}
      <nav className="relative z-10 px-6 py-5 border-b border-gray-100">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <img src={IMAGES.LOGO} alt={ALT_TEXT.LOGO} className="h-8 w-auto" />
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 pt-20 pb-16 px-6">
        <div className="max-w-6xl mx-auto">
          {/* Top section - centered text */}
          <div className="text-center mb-16 max-w-3xl mx-auto">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mb-6"
            ></motion.div>

            {/* Headline */}
            <motion.h1
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="text-4xl md:text-5xl lg:text-5xl font-normal leading-tight mb-6 text-gray-900"
            >
              See furniture in your room before you buy
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="text-base text-gray-600 mb-8"
            >
              Upload a photo. We find options and show them in your space.
            </motion.p>

            {/* Quick features */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="flex flex-wrap items-center justify-center gap-6 text-sm text-gray-600"
            ></motion.div>
          </div>

          {/* Main Upload Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="max-w-3xl mx-auto"
          >
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-8">
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  Upload a photo of your room
                </h2>
                <p className="text-sm text-gray-600">
                  We'll find furniture that fits your space and budget.
                </p>
              </div>

              <FileUpload
                value={files}
                onValueChange={onFilesChange}
                onFileValidate={onFileValidate}
                accept="image/*"
                maxFiles={FILE_UPLOAD.MAX_FILES}
                className="w-full"
                multiple
              >
                <FileUploadDropzone className="border-2 border-dashed border-gray-300 bg-gray-50/50 hover:border-gray-900 hover:bg-white transition-all duration-200 rounded-xl">
                  <div className="flex flex-col items-center gap-3 py-10">
                    <div className="flex items-center justify-center rounded-full bg-gray-900 p-3">
                      <Upload className="size-5 text-white" />
                    </div>
                    <div className="text-center">
                      <p className="font-medium text-base text-gray-900 mb-1">
                        Drop your photo here
                      </p>
                      <p className="text-sm text-gray-500">
                        or click to browse (max {FILE_UPLOAD.MAX_FILES} images)
                      </p>
                    </div>
                    <FileUploadTrigger asChild>
                      <Button
                        size="sm"
                        className="mt-2 bg-gray-900 hover:bg-gray-800 focus:ring-gray-900 text-white"
                      >
                        Choose Photo
                      </Button>
                    </FileUploadTrigger>
                  </div>
                </FileUploadDropzone>

                <FileUploadList className="mt-4">
                  {files.map((file) => {
                    const uploadedFile = uploadedFiles.find(
                      (uf) => uf.file === file
                    );

                    return (
                      <FileUploadItem
                        key={file.name}
                        value={file}
                        className="bg-gray-50 rounded-lg border border-gray-200"
                      >
                        <FileUploadItemPreview />
                        <FileUploadItemMetadata />
                        {uploadedFile && (
                          <div className="flex items-center gap-2 text-xs font-medium">
                            {uploadedFile.status === "uploading" && (
                              <span className="text-blue-600">
                                {UI.TEXT.UPLOADING}
                              </span>
                            )}
                            {uploadedFile.status === "success" && (
                              <span className="text-green-600">
                                {UI.TEXT.UPLOAD_SUCCESS}
                              </span>
                            )}
                            {uploadedFile.status === "error" && (
                              <span className="text-red-600">
                                {uploadedFile.error || UI.TEXT.UPLOAD_ERROR}
                              </span>
                            )}
                          </div>
                        )}
                        <FileUploadItemDelete asChild>
                          <Button
                            variant="ghost"
                            size="icon"
                            className="size-8"
                            disabled={isUploading}
                          >
                            <X className="size-4" />
                          </Button>
                        </FileUploadItemDelete>
                      </FileUploadItem>
                    );
                  })}
                </FileUploadList>

                {files.length > 0 && (
                  <div className="mt-4">
                    <Button
                      size="lg"
                      className="w-full bg-gray-900 hover:bg-gray-800 focus:ring-gray-900 text-white font-medium"
                      onClick={onBeginProcess}
                      disabled={
                        isUploading ||
                        isLoadingDescriptions ||
                        allUploadsSuccessful
                      }
                    >
                      {(isUploading || isLoadingDescriptions) && (
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      )}
                      {isUploading
                        ? "Uploading..."
                        : isLoadingDescriptions
                        ? "Analysing your space..."
                        : "Find Furniture →"}
                    </Button>
                  </div>
                )}
              </FileUpload>

              {files.length === 0 && (
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <p className="text-xs font-medium text-gray-500 mb-4 uppercase tracking-wide">
                    How it works
                  </p>
                  <div className="space-y-3">
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gray-900 flex items-center justify-center text-white text-xs font-semibold">
                        1
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          Analyse your room
                        </p>
                        <p className="text-xs text-gray-600 mt-0.5">
                          We identify style, colours, and dimensions
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gray-900 flex items-center justify-center text-white text-xs font-semibold">
                        2
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          Find matching furniture
                        </p>
                        <p className="text-xs text-gray-600 mt-0.5">
                          Search across retailers within your budget
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gray-900 flex items-center justify-center text-white text-xs font-semibold">
                        3
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          See it in your space
                        </p>
                        <p className="text-xs text-gray-600 mt-0.5">
                          View products in your actual room before buying
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
