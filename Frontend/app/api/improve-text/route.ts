import { type NextRequest, NextResponse } from "next/server"
import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"

export async function POST(request: NextRequest) {
  try {
    const { text } = await request.json()

    const { text: improvedText } = await generateText({
      model: openai("gpt-4o"),
      prompt: `
        Improve the following text by making it:
        - More clear and concise
        - Better structured
        - More professional
        - Grammatically correct
        - More engaging where appropriate
        
        Original text:
        ${text}
        
        Return only the improved text without any explanations or additional commentary.
      `,
    })

    return NextResponse.json({ improvedText })
  } catch (error) {
    console.error("Error improving text:", error)
    return NextResponse.json({ error: "Failed to improve text" }, { status: 500 })
  }
}
