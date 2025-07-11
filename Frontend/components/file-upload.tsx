"use client"

import type React from "react"

import { useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { FileText, Upload, X } from "lucide-react"

interface FileUploadProps {
  files: File[]
  onFilesChange: (files: File[]) => void
}

export function FileUpload({ files, onFilesChange }: FileUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(event.target.files || [])
    onFilesChange([...files, ...selectedFiles])
  }

  const removeFile = (index: number) => {
    onFilesChange(files.filter((_, i) => i !== index))
  }

  const supportedFormats = ["JSON", "PDF", "HTML", "TXT", "MD", "PNG", "JPG", "JPEG"]

  return (
    <Card className="dark:bg-gray-800 dark:border-gray-700">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 dark:text-white">
          <FileText className="h-5 w-5" />
          File Integration
        </CardTitle>
        <CardDescription className="dark:text-gray-400">
          Upload files in various formats (JSON, PDF, HTML, images) for content extraction
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".json,.pdf,.html,.txt,.md,.png,.jpg,.jpeg"
          onChange={handleFileSelect}
          className="hidden"
        />
        <Button
          onClick={() => fileInputRef.current?.click()}
          variant="outline"
          className="w-full dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
        >
          <Upload className="h-4 w-4 mr-2" />
          Upload Files
        </Button>
        <div className="text-xs text-gray-500 dark:text-gray-400">Supported: {supportedFormats.join(", ")}</div>
        <div className="space-y-2">
          {files.map((file, index) => (
            <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded dark:bg-gray-700">
              <span className="text-sm truncate dark:text-gray-300">{file.name}</span>
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="text-xs">
                  {file.type || "Unknown"}
                </Badge>
                <X className="h-4 w-4 cursor-pointer text-red-500" onClick={() => removeFile(index)} />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
