"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Lightbulb, Plus, X } from "lucide-react"
import { useState } from "react"

interface ProjectContextBuilderProps {
  context: string
  onContextChange: (context: string) => void
  rules: string[]
  onRulesChange: (rules: string[]) => void
  mcpTools: string[]
  onMcpToolsChange: (tools: string[]) => void
}

export function ProjectContextBuilder({
  context,
  onContextChange,
  rules,
  onRulesChange,
  mcpTools,
  onMcpToolsChange,
}: ProjectContextBuilderProps) {
  const [newRule, setNewRule] = useState("")
  const [newTool, setNewTool] = useState("")

  const addRule = () => {
    if (newRule.trim()) {
      onRulesChange([...rules, newRule])
      setNewRule("")
    }
  }

  const addTool = () => {
    if (newTool.trim()) {
      onMcpToolsChange([...mcpTools, newTool])
      setNewTool("")
    }
  }

  return (
    <Card className="dark:bg-gray-800 dark:border-gray-700">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 dark:text-white">
          <Lightbulb className="h-5 w-5" />
          Project Context & Configuration
        </CardTitle>
        <CardDescription className="dark:text-gray-400">
          Define project context, rules, and MCP tool requirements
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <label className="text-sm font-medium mb-2 block dark:text-gray-300">Project Context</label>
          <Textarea
            placeholder="Describe your project goals, scope, and intended functionality..."
            value={context}
            onChange={(e) => onContextChange(e.target.value)}
            rows={4}
            showImproveButton={true}
            onImprove={(improvedText) => onContextChange(improvedText)}
            className="dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
        </div>

        <div>
          <label className="text-sm font-medium mb-2 block dark:text-gray-300">Rules & Constraints</label>
          <div className="flex gap-2 mb-2">
            <Input
              placeholder="Add a rule or constraint..."
              value={newRule}
              onChange={(e) => setNewRule(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && addRule()}
              className="dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
            <Button onClick={addRule} size="sm">
              <Plus className="h-4 w-4" />
            </Button>
          </div>
          <div className="flex flex-wrap gap-2">
            {rules.map((rule, index) => (
              <Badge
                key={index}
                variant="outline"
                className="flex items-center gap-1 dark:border-gray-600 dark:text-gray-300"
              >
                {rule}
                <X
                  className="h-3 w-3 cursor-pointer"
                  onClick={() => onRulesChange(rules.filter((_, i) => i !== index))}
                />
              </Badge>
            ))}
          </div>
        </div>

        <div>
          <label className="text-sm font-medium mb-2 block dark:text-gray-300">MCP Tools Requirements</label>
          <div className="flex gap-2 mb-2">
            <Input
              placeholder="cursor, gemini-cli, windsurf..."
              value={newTool}
              onChange={(e) => setNewTool(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && addTool()}
              className="dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
            <Button onClick={addTool} size="sm">
              <Plus className="h-4 w-4" />
            </Button>
          </div>
          <div className="flex flex-wrap gap-2">
            {mcpTools.map((tool, index) => (
              <Badge
                key={index}
                variant="secondary"
                className="flex items-center gap-1 dark:bg-gray-700 dark:text-gray-300"
              >
                {tool}
                <X
                  className="h-3 w-3 cursor-pointer"
                  onClick={() => onMcpToolsChange(mcpTools.filter((_, i) => i !== index))}
                />
              </Badge>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
