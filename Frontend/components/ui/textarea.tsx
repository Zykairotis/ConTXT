"use client"

import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Wand2, Loader2 } from "lucide-react"
import { useState } from "react"

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

export interface EnhancedTextareaProps extends TextareaProps {
  showImproveButton?: boolean
  onImprove?: (improvedText: string) => void
}

const Textarea = React.forwardRef<HTMLTextAreaElement, EnhancedTextareaProps>(
  ({ className, showImproveButton = false, onImprove, value, onChange, ...props }, ref) => {
    const [isImproving, setIsImproving] = useState(false)

    const handleImprove = async () => {
      if (!value || typeof value !== "string") return

      setIsImproving(true)
      try {
        const response = await fetch("/api/improve-text", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: value }),
        })

        if (response.ok) {
          const result = await response.json()
          if (onImprove) {
            onImprove(result.improvedText)
          } else if (onChange) {
            onChange({ target: { value: result.improvedText } } as any)
          }
        }
      } catch (error) {
        console.error("Error improving text:", error)
      } finally {
        setIsImproving(false)
      }
    }

    return (
      <div className="relative">
        <textarea
          className={cn(
            "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-colors",
            showImproveButton && "pr-12",
            className,
          )}
          ref={ref}
          value={value}
          onChange={onChange}
          {...props}
        />
        {showImproveButton && (
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="absolute top-2 right-2 h-8 w-8 p-0 hover:bg-accent"
            onClick={handleImprove}
            disabled={isImproving || !value}
            title="Improve text with AI"
          >
            {isImproving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Wand2 className="h-4 w-4" />}
          </Button>
        )}
      </div>
    )
  },
)
Textarea.displayName = "Textarea"

export { Textarea }
