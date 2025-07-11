"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { MessageSquare, Plus, Trash2 } from "lucide-react"

interface ChatLogProcessorProps {
  chatLogs: any[]
  onChatLogsChange: (logs: any[]) => void
}

export function ChatLogProcessor({ chatLogs, onChatLogsChange }: ChatLogProcessorProps) {
  const [newChatLog, setNewChatLog] = useState("")

  const addChatLog = () => {
    if (!newChatLog.trim()) return

    try {
      const parsed = JSON.parse(newChatLog)
      onChatLogsChange([...chatLogs, parsed])
      setNewChatLog("")
    } catch (error) {
      // If not JSON, treat as plain text
      onChatLogsChange([...chatLogs, { content: newChatLog, type: "text" }])
      setNewChatLog("")
    }
  }

  const removeChatLog = (index: number) => {
    onChatLogsChange(chatLogs.filter((_, i) => i !== index))
  }

  return (
    <Card className="dark:bg-gray-800 dark:border-gray-700">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 dark:text-white">
          <MessageSquare className="h-5 w-5" />
          AI Agent Chats
        </CardTitle>
        <CardDescription className="dark:text-gray-400">
          Process chat logs from other AI agents to extract insights and patterns
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Textarea
          placeholder="Paste chat log JSON or plain text conversation..."
          value={newChatLog}
          onChange={(e) => setNewChatLog(e.target.value)}
          rows={4}
          showImproveButton={true}
          onImprove={(improvedText) => setNewChatLog(improvedText)}
          className="dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        />
        <Button onClick={addChatLog} className="w-full">
          <Plus className="h-4 w-4 mr-2" />
          Add Chat Log
        </Button>
        <div className="space-y-2">
          {chatLogs.map((log, index) => (
            <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded dark:bg-gray-700">
              <div className="flex-1">
                <Badge variant="outline" className="mb-1">
                  {log.type || "conversation"}
                </Badge>
                <div className="text-sm text-gray-600 truncate dark:text-gray-300">
                  {typeof log === "string" ? log : log.content || JSON.stringify(log).slice(0, 100)}
                </div>
              </div>
              <Trash2 className="h-4 w-4 cursor-pointer text-red-500 ml-2" onClick={() => removeChatLog(index)} />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
