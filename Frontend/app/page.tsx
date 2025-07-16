"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { WebUrlInput } from "@/components/web-url-input"
import { FileUpload } from "@/components/file-upload"
import { LibraryAnalyzer } from "@/components/library-analyzer"
import { SystemPromptGenerator } from "@/components/system-prompt-generator"
import { ProjectContextBuilder } from "@/components/project-context-builder"
import { ContextViewer } from "@/components/context-viewer"
import { Brain, Globe, FileText, MessageSquare, Code, Settings, Eye, Video } from "lucide-react"
import { Textarea } from "@/components/ui/textarea"
import { VideoProcessor } from "@/components/video-processor"
import { ThemeToggle } from "@/components/theme-toggle"
import { SourceDetailModal } from "@/components/source-detail-modal"
import { ClientOnly } from "@/components/client-only"

interface ContextData {
  webUrls: string[]
  files: File[]
  libraries: string[]
  videos: any[]
  systemPrompt: string
  projectContext: string
  rules: string[]
  mcpTools: string[]
}

export default function LLMContextBuilder() {
  const [contextData, setContextData] = useState<ContextData>({
    webUrls: [],
    files: [],
    libraries: [],
    videos: [],
    systemPrompt: "",
    projectContext: "",
    rules: [],
    mcpTools: [],
  })

  const [isBuilding, setIsBuilding] = useState(false)
  const [buildProgress, setBuildProgress] = useState(0)
  const [builtContext, setBuiltContext] = useState<string>("")
  const [originalText, setOriginalText] = useState("")
  const [improvedText, setImprovedText] = useState("")

  const [isModalOpen, setIsModalOpen] = useState(false)
  type SourceType = 'webUrls' | 'files' | 'videos' | 'libraries';

  const [modalContent, setModalContent] = useState<{ title: string; sources: any[]; sourceType: SourceType }>({
    title: "",
    sources: [],
    sourceType: 'webUrls',
  })

  const handleBuildContext = async () => {
    setIsBuilding(true)
    setBuildProgress(0)

    try {
      const response = await fetch("/api/build-context", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(contextData),
      })

      if (response.ok) {
        const result = await response.json()
        setBuiltContext(result.context)
        setBuildProgress(100)
      }
    } catch (error) {
      console.error("Error building context:", error)
    } finally {
      setIsBuilding(false)
    }
  }

  const updateContextData = (key: keyof ContextData, value: any) => {
    setContextData((prev) => ({ ...prev, [key]: value }))
  }

  const openModal = (title: string, sources: any[], sourceType: SourceType) => {
    setModalContent({ title, sources, sourceType })
    setIsModalOpen(true)
  }

  return (
    <ClientOnly>
      <div className="min-h-screen bg-background p-4 transition-all duration-300">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-start mb-8">
          <div className="text-center flex-1">
            <h1 className="text-4xl font-bold text-foreground mb-2 flex items-center justify-center gap-2">
              <Brain className="h-8 w-8 text-primary" />
              LLM Context Builder
            </h1>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Construct comprehensive context for Large Language Models by integrating multiple data sources
            </p>
          </div>
          <div className="flex items-center gap-2">
            <ThemeToggle />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="cursor-pointer hover:border-primary transition-colors" onClick={() => openModal("Web URLs", contextData.webUrls, 'webUrls')}>
            <CardContent className="p-4 text-center">
              <Globe className="h-8 w-8 text-blue-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-foreground">{contextData.webUrls.length}</div>
              <div className="text-sm text-muted-foreground">Web URLs</div>
            </CardContent>
          </Card>
          <Card className="cursor-pointer hover:border-primary transition-colors" onClick={() => openModal("Files", contextData.files, 'files')}>
            <CardContent className="p-4 text-center">
              <FileText className="h-8 w-8 text-green-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-foreground">{contextData.files.length}</div>
              <div className="text-sm text-muted-foreground">Files</div>
            </CardContent>
          </Card>
          <Card className="cursor-pointer hover:border-primary transition-colors" onClick={() => openModal("Videos", contextData.videos.map(v => v.source), 'videos')}>
            <CardContent className="p-4 text-center">
              <Video className="h-8 w-8 text-red-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-foreground">{contextData.videos.length}</div>
              <div className="text-sm text-muted-foreground">Videos</div>
            </CardContent>
          </Card>
          <Card className="cursor-pointer hover:border-primary transition-colors" onClick={() => openModal("Libraries", contextData.libraries, 'libraries')}>
            <CardContent className="p-4 text-center">
              <Code className="h-8 w-8 text-orange-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-foreground">{contextData.libraries.length}</div>
              <div className="text-sm text-muted-foreground">Libraries</div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="sources" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="sources">Data Sources</TabsTrigger>
            <TabsTrigger value="configuration">Configuration</TabsTrigger>
            <TabsTrigger value="preview">Preview & Compare</TabsTrigger>
            <TabsTrigger value="build">Build Context</TabsTrigger>
            <TabsTrigger value="output">Output</TabsTrigger>
          </TabsList>

          <TabsContent value="sources" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <WebUrlInput urls={contextData.webUrls} onUrlsChange={(urls) => updateContextData("webUrls", urls)} />
              <FileUpload files={contextData.files} onFilesChange={(files) => updateContextData("files", files)} />
              <LibraryAnalyzer
                libraries={contextData.libraries}
                onLibrariesChange={(libs) => updateContextData("libraries", libs)}
              />
              <VideoProcessor
                videos={contextData.videos}
                onVideosChange={(videos) => updateContextData("videos", videos)}
              />
            </div>
          </TabsContent>

          <TabsContent value="configuration" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <SystemPromptGenerator
                prompt={contextData.systemPrompt}
                onPromptChange={(prompt) => updateContextData("systemPrompt", prompt)}
              />
              <ProjectContextBuilder
                context={contextData.projectContext}
                onContextChange={(context) => updateContextData("projectContext", context)}
                rules={contextData.rules}
                onRulesChange={(rules) => updateContextData("rules", rules)}
                mcpTools={contextData.mcpTools}
                onMcpToolsChange={(tools) => updateContextData("mcpTools", tools)}
              />
            </div>
          </TabsContent>

          <TabsContent value="preview" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Eye className="h-5 w-5" />
                  Preview & Compare Improvements
                </CardTitle>
                <CardDescription>
                  Preview your text improvements and compare original vs enhanced versions
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium mb-2 block text-foreground">Original Text</label>
                    <Textarea
                      placeholder="Enter text to improve..."
                      value={originalText}
                      onChange={(e) => setOriginalText(e.target.value)}
                      rows={8}
                      showImproveButton={true}
                      onImprove={(improvedText) => setImprovedText(improvedText)}
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block text-foreground">Improved Text</label>
                    <Textarea
                      placeholder="Improved text will appear here..."
                      value={improvedText}
                      onChange={(e) => setImprovedText(e.target.value)}
                      rows={8}
                      readOnly
                      className="bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800 dark:text-green-100"
                    />
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button onClick={() => setOriginalText(improvedText)} disabled={!improvedText} variant="outline">
                    Accept Improvement
                  </Button>
                  <Button onClick={() => setImprovedText("")} disabled={!improvedText} variant="outline">
                    Clear Comparison
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="build" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Build Comprehensive Context
                </CardTitle>
                <CardDescription>
                  Process all data sources and generate a comprehensive context for your LLM
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {isBuilding && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm text-muted-foreground">
                      <span>Building context...</span>
                      <span>{buildProgress}%</span>
                    </div>
                    <Progress value={buildProgress} />
                  </div>
                )}
                <Button onClick={handleBuildContext} disabled={isBuilding} className="w-full" size="lg">
                  {isBuilding ? "Building Context..." : "Build Context"}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="output">
            <ContextViewer context={builtContext} />
          </TabsContent>
        </Tabs>
      </div>
      <SourceDetailModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={modalContent.title}
        sources={modalContent.sources}
        sourceType={modalContent.sourceType}
      />
    </div>
    </ClientOnly>
  )
}
