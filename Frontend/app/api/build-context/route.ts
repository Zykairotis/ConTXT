import { type NextRequest, NextResponse } from "next/server"
import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"

export async function POST(request: NextRequest) {
  try {
    const contextData = await request.json()

    // Build comprehensive context using AI
    const { text: builtContext } = await generateText({
      model: openai("gpt-4o"),
      prompt: `
    You are an AI agent specialized in building comprehensive context for Large Language Models.
    
    Based on the following data sources, create a comprehensive context document:
    
    Web URLs: ${JSON.stringify(contextData.webUrls)}
    Files: ${contextData.files.map((f: any) => f.name).join(", ")}
    Chat Logs: ${contextData.chatLogs.length} conversations
    Libraries: ${contextData.libraries.join(", ")}
    Videos: ${contextData.videos.length} video sources with transcriptions
    Video Transcriptions: ${contextData.videos
      .map((v: any) => v.transcription)
      .filter(Boolean)
      .join("\n\n")}
    System Prompt: ${contextData.systemPrompt}
    Project Context: ${contextData.projectContext}
    Rules: ${contextData.rules.join(", ")}
    MCP Tools: ${contextData.mcpTools.join(", ")}
    
    Create a structured context document that includes:
    1. Executive Summary
    2. Project Overview
    3. Technical Requirements
    4. Library Dependencies
    5. System Configuration
    6. Rules and Constraints
    7. Available Tools and Resources
    8. Context from External Sources (including video transcriptions)
    9. Video Content Analysis (if applicable)
    
    Make it comprehensive and well-organized for LLM consumption.
  `,
    })

    return NextResponse.json({ context: builtContext })
  } catch (error) {
    console.error("Error building context:", error)
    return NextResponse.json({ error: "Failed to build context" }, { status: 500 })
  }
}
