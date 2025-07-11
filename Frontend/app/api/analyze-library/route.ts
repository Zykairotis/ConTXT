import { type NextRequest, NextResponse } from "next/server"
import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"

export async function POST(request: NextRequest) {
  try {
    const { library } = await request.json()

    // Use AI to analyze the library
    const { text: analysis } = await generateText({
      model: openai("gpt-4o"),
      prompt: `
        Analyze the ${library} library and provide:
        1. Main purpose and functionality
        2. Key features and capabilities
        3. Common use cases
        4. Integration patterns
        5. Best practices
        
        Keep it concise but comprehensive for LLM context building.
      `,
    })

    return NextResponse.json({
      success: true,
      analysis,
    })
  } catch (error) {
    console.error("Error analyzing library:", error)
    return NextResponse.json({ error: "Failed to analyze library" }, { status: 500 })
  }
}
