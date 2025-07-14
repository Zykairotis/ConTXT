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
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-5 w-5" />
          File Integration
        </CardTitle>
        <CardDescription>
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
          className="w-full"
        >
          <Upload className="h-4 w-4 mr-2" />
          Upload Files
        </Button>
        <div className="text-xs text-muted-foreground">Supported: {supportedFormats.join(", ")}</div>
        <div className="space-y-2 max-h-48 overflow-y-auto pr-2">
          {files.map((file, index) => (
            <div key={index} className="flex items-center justify-between p-2 bg-muted rounded">
              <span className="text-sm truncate">{file.name}</span>
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
