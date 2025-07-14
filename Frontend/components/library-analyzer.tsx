"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Code, Plus, X, Loader2 } from "lucide-react"

interface LibraryAnalyzerProps {
  libraries: string[]
  onLibrariesChange: (libraries: string[]) => void
}

export function LibraryAnalyzer({ libraries, onLibrariesChange }: LibraryAnalyzerProps) {
  const [newLibrary, setNewLibrary] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const addLibrary = async () => {
    if (!newLibrary.trim()) return

    setIsAnalyzing(true)
    try {
      const response = await fetch("/api/analyze-library", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ library: newLibrary }),
      })

      if (response.ok) {
        onLibrariesChange([...libraries, newLibrary])
        setNewLibrary("")
      }
    } catch (error) {
      console.error("Error analyzing library:", error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const removeLibrary = (index: number) => {
    onLibrariesChange(libraries.filter((_, i) => i !== index))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Code className="h-5 w-5" />
          Library Understanding
        </CardTitle>
        <CardDescription>
          Analyze libraries and their functionalities for better LLM integration
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-2">
          <Input
            placeholder="react, lodash, axios..."
            value={newLibrary}
            onChange={(e) => setNewLibrary(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && addLibrary()}
            
          />
          <Button onClick={addLibrary} disabled={isAnalyzing}>
            {isAnalyzing ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
          </Button>
        </div>
        <div className="flex flex-wrap gap-2 max-h-48 overflow-y-auto pr-2">
          {libraries.map((library, index) => (
            <Badge
              key={index}
              variant="secondary"
              className="flex items-center gap-1"
            >
              {library}
              <X className="h-3 w-3 cursor-pointer" onClick={() => removeLibrary(index)} />
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
