"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Settings, Wand2 } from "lucide-react"

interface SystemPromptGeneratorProps {
  prompt: string
  onPromptChange: (prompt: string) => void
}

export function SystemPromptGenerator({ prompt, onPromptChange }: SystemPromptGeneratorProps) {
  const generatePrompt = async () => {
    try {
      const response = await fetch("/api/generate-system-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      })

      if (response.ok) {
        const result = await response.json()
        onPromptChange(result.prompt)
      }
    } catch (error) {
      console.error("Error generating system prompt:", error)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Settings className="h-5 w-5" />
          System Prompt Generation
        </CardTitle>
        <CardDescription>
          Generate tailored system prompts to guide the LLM's behavior and output format
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Button
          onClick={generatePrompt}
          variant="outline"
          className="w-full bg-transparent"
        >
          <Wand2 className="h-4 w-4 mr-2" />
          Generate System Prompt
        </Button>
        <Textarea
          placeholder="Enter or generate a system prompt..."
          value={prompt}
          onChange={(e) => onPromptChange(e.target.value)}
          rows={8}
          showImproveButton={true}
          onImprove={(improvedText) => onPromptChange(improvedText)}
          
        />
      </CardContent>
    </Card>
  )
}
