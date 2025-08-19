import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X } from 'lucide-react';

const VideoUploader = ({ onFileSelect, selectedFile }) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
    },
    multiple: false
  });

  const removeFile = () => {
    onFileSelect(null);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-4">
      {!selectedFile ? (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors duration-200 ${
            isDragActive
              ? 'border-secondary-500 bg-secondary-50'
              : 'border-primary-300 hover:border-secondary-400 hover:bg-primary-50'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="w-12 h-12 mx-auto mb-4 text-secondary-500" />
          {isDragActive ? (
            <p className="text-secondary-600">Drop the video file here...</p>
          ) : (
            <div>
              <p className="text-gray-600 mb-2">
                Drag & drop a video file here, or click to select
              </p>
              <p className="text-sm text-gray-500">
                Supports MP4, AVI, MOV, WMV, FLV, WebM
              </p>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <File className="w-8 h-8 text-secondary-500" />
              <div>
                <p className="font-medium text-gray-800">{selectedFile.name}</p>
                <p className="text-sm text-gray-500">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>
            <button
              onClick={removeFile}
              className="p-1 hover:bg-red-100 rounded-full transition-colors duration-200"
            >
              <X className="w-5 h-5 text-red-500" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoUploader;