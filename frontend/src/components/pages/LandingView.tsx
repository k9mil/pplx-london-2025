import { motion } from "framer-motion";
import { Upload, X, Loader2, Sparkles, ShoppingBag, Eye } from "lucide-react";
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
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-pink-50 to-purple-50 relative overflow-hidden">
      {/* Subtle mesh gradient overlay */}
      <div 
        className="absolute inset-0 opacity-30"
        style={{
          background: "radial-gradient(at 20% 30%, rgba(255, 47, 47, 0.15) 0%, transparent 50%), radial-gradient(at 80% 70%, rgba(138, 67, 225, 0.15) 0%, transparent 50%), radial-gradient(at 50% 50%, rgba(239, 123, 22, 0.1) 0%, transparent 50%)"
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
            >
              <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-gray-100 rounded-full text-xs font-medium text-gray-700">
                <Sparkles className="w-3 h-3" />
                AI-Powered · Multi-Vendor · Real Visualization
              </div>
            </motion.div>

            {/* Headline */}
            <motion.h1
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-6 text-gray-900"
            >
              See furniture in{" "}
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                your room
              </span>
              {" "}before you buy
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="text-lg text-gray-600 mb-8 leading-relaxed"
            >
              We learn your style, curate from multiple vendors, then visualize products in your actual space. Not another single-store AR app.
            </motion.p>

            {/* Quick features */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="flex flex-wrap items-center justify-center gap-6 text-sm text-gray-600"
            >
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-purple-600" />
                <span>AI learns your taste</span>
              </div>
              <div className="flex items-center gap-2">
                <ShoppingBag className="w-4 h-4 text-purple-600" />
                <span>Multiple vendors</span>
              </div>
              <div className="flex items-center gap-2">
                <Eye className="w-4 h-4 text-purple-600" />
                <span>See it in your space</span>
              </div>
            </motion.div>
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
                  Our AI will analyze your space and find furniture that matches your style from across the web.
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
                <FileUploadDropzone className="border-2 border-dashed border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-gray-100 transition-all duration-200 rounded-xl">
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
                        className="mt-2 bg-gray-900 hover:bg-gray-800 text-white"
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
                      className="w-full bg-gray-900 hover:bg-gray-800 text-white font-medium"
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
                        ? "Analyzing your space..."
                        : "Find My Furniture →"}
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
                          AI analyzes your room
                        </p>
                        <p className="text-xs text-gray-600 mt-0.5">
                          We identify style, colors, and dimensions from your photo
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gray-900 flex items-center justify-center text-white text-xs font-semibold">
                        2
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          Curate from multiple vendors
                        </p>
                        <p className="text-xs text-gray-600 mt-0.5">
                          Swipe through furniture that matches from across the web
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gray-900 flex items-center justify-center text-white text-xs font-semibold">
                        3
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          Visualize in your space
                        </p>
                        <p className="text-xs text-gray-600 mt-0.5">
                          See products placed in YOUR room before buying
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Social proof */}
            <div className="mt-6 flex items-center justify-center gap-3 text-sm text-gray-600">
              <div className="flex">
                {[1, 2, 3, 4, 5].map((i) => (
                  <svg
                    key={i}
                    className="w-4 h-4 text-yellow-400 fill-current"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <span className="text-gray-900 font-medium">4.9</span>
              <span>·</span>
              <span>10,000+ rooms transformed</span>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
