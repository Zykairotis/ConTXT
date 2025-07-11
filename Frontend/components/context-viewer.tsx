"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Database, Copy, Download } from "lucide-react"

interface ContextViewerProps {
  context: string
}

export function ContextViewer({ context }: ContextViewerProps) {
  const copyToClipboard = () => {
    navigator.clipboard.writeText(context)
  }

  const downloadContext = () => {
    const blob = new Blob([context], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "llm-context.txt"
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <Card className="dark:bg-gray-800 dark:border-gray-700">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 dark:text-white">
          <Database className="h-5 w-5" />
          Generated Context
        </CardTitle>
        <CardDescription className="dark:text-gray-400">
          Comprehensive context built from all data sources for your LLM
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-2">
          <Button
            onClick={copyToClipboard}
            variant="outline"
            size="sm"
            className="dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700 bg-transparent"
          >
            <Copy className="h-4 w-4 mr-2" />
            Copy
          </Button>
          <Button
            onClick={downloadContext}
            variant="outline"
            size="sm"
            className="dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700 bg-transparent"
          >
            <Download className="h-4 w-4 mr-2" />
            Download
          </Button>
        </div>
        <Textarea
          value={context}
          readOnly
          rows={20}
          className="font-mono text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300"
          placeholder="Built context will appear here..."
        />
      </CardContent>
    </Card>
  )
}
