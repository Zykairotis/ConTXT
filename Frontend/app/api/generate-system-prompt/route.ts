import { type NextRequest, NextResponse } from "next/server"
import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"

export async function POST(request: NextRequest) {
  try {
    const { text: prompt } = await generateText({
      model: openai("gpt-4o"),
      prompt: `
        Generate a comprehensive system prompt for an LLM that will be used for software development and AI assistance.
        
        The prompt should include:
        1. Role definition
        2. Capabilities and limitations
        3. Output format guidelines
        4. Interaction patterns
        5. Error handling instructions
        6. Code quality standards
        7. Documentation requirements
        
        Make it professional, clear, and actionable.
      `,
    })

    return NextResponse.json({ prompt })
  } catch (error) {
    console.error("Error generating system prompt:", error)
    return NextResponse.json({ error: "Failed to generate system prompt" }, { status: 500 })
  }
}
