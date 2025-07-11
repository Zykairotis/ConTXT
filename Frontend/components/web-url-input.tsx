"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Globe, Plus, X, Loader2 } from "lucide-react"

interface WebUrlInputProps {
  urls: string[]
  onUrlsChange: (urls: string[]) => void
}

export function WebUrlInput({ urls, onUrlsChange }: WebUrlInputProps) {
  const [newUrl, setNewUrl] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)

  const addUrl = async () => {
    if (!newUrl.trim()) return

    setIsProcessing(true)
    try {
      const response = await fetch("/api/process-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: newUrl }),
      })

      if (response.ok) {
        onUrlsChange([...urls, newUrl])
        setNewUrl("")
      }
    } catch (error) {
      console.error("Error processing URL:", error)
    } finally {
      setIsProcessing(false)
    }
  }

  const removeUrl = (index: number) => {
    onUrlsChange(urls.filter((_, i) => i !== index))
  }

  return (
    <Card className="dark:bg-gray-800 dark:border-gray-700">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 dark:text-white">
          <Globe className="h-5 w-5" />
          Web URLs
        </CardTitle>
        <CardDescription className="dark:text-gray-400">
          Add web URLs to extract content and enrich the LLM's knowledge base
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-2">
          <Input
            placeholder="https://example.com"
            value={newUrl}
            onChange={(e) => setNewUrl(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && addUrl()}
            className="dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
          <Button onClick={addUrl} disabled={isProcessing}>
            {isProcessing ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
          </Button>
        </div>
        <div className="flex flex-wrap gap-2">
          {urls.map((url, index) => (
            <Badge
              key={index}
              variant="secondary"
              className="flex items-center gap-1 dark:bg-gray-700 dark:text-gray-300"
            >
              {url}
              <X className="h-3 w-3 cursor-pointer" onClick={() => removeUrl(index)} />
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
