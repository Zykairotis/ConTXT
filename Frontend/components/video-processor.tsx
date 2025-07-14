"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Video, Plus, X, Loader2, Youtube, FileVideo } from "lucide-react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

interface VideoSource {
  id: string
  type: "file" | "youtube"
  url: string
  title?: string
  duration?: string
  status: "pending" | "processing" | "completed" | "error"
  transcription?: string
  progress?: number
}

interface VideoProcessorProps {
  videos: VideoSource[]
  onVideosChange: (videos: VideoSource[]) => void
}

export function VideoProcessor({ videos, onVideosChange }: VideoProcessorProps) {
  const [youtubeUrl, setYoutubeUrl] = useState("")
  const [videoFileUrl, setVideoFileUrl] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)

  const addYouTubeVideo = async () => {
    if (!youtubeUrl.trim()) return

    const newVideo: VideoSource = {
      id: Date.now().toString(),
      type: "youtube",
      url: youtubeUrl,
      status: "pending",
      progress: 0,
    }

    const updatedVideos = [...videos, newVideo]
    onVideosChange(updatedVideos)
    setYoutubeUrl("")

    await processVideo(newVideo.id, youtubeUrl, "youtube")
  }

  const addVideoFile = async () => {
    if (!videoFileUrl.trim()) return

    const newVideo: VideoSource = {
      id: Date.now().toString(),
      type: "file",
      url: videoFileUrl,
      status: "pending",
      progress: 0,
    }

    const updatedVideos = [...videos, newVideo]
    onVideosChange(updatedVideos)
    setVideoFileUrl("")

    await processVideo(newVideo.id, videoFileUrl, "file")
  }

  const processVideo = async (videoId: string, url: string, type: "youtube" | "file") => {
    setIsProcessing(true)

    try {
      // Update status to processing
      updateVideoStatus(videoId, "processing", 10)

      const response = await fetch("/api/process-video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, type, videoId }),
      })

      if (response.ok) {
        const reader = response.body?.getReader()
        const decoder = new TextDecoder()

        if (reader) {
          while (true) {
            const { done, value } = await reader.read()
            if (done) break

            const chunk = decoder.decode(value)
            const lines = chunk.split("\n").filter((line) => line.trim())

            for (const line of lines) {
              if (line.startsWith("data: ")) {
                try {
                  const data = JSON.parse(line.slice(6))

                  if (data.type === "progress") {
                    updateVideoStatus(videoId, "processing", data.progress)
                  } else if (data.type === "metadata") {
                    updateVideoMetadata(videoId, data.title, data.duration)
                  } else if (data.type === "transcription") {
                    updateVideoTranscription(videoId, data.transcription)
                  } else if (data.type === "complete") {
                    updateVideoStatus(videoId, "completed", 100)
                  }
                } catch (e) {
                  console.error("Error parsing SSE data:", e)
                }
              }
            }
          }
        }
      } else {
        updateVideoStatus(videoId, "error", 0)
      }
    } catch (error) {
      console.error("Error processing video:", error)
      updateVideoStatus(videoId, "error", 0)
    } finally {
      setIsProcessing(false)
    }
  }

  const updateVideoStatus = (videoId: string, status: VideoSource["status"], progress: number) => {
    onVideosChange(videos.map((video) => (video.id === videoId ? { ...video, status, progress } : video)))
  }

  const updateVideoMetadata = (videoId: string, title: string, duration: string) => {
    onVideosChange(videos.map((video) => (video.id === videoId ? { ...video, title, duration } : video)))
  }

  const updateVideoTranscription = (videoId: string, transcription: string) => {
    onVideosChange(videos.map((video) => (video.id === videoId ? { ...video, transcription } : video)))
  }

  const removeVideo = (videoId: string) => {
    onVideosChange(videos.filter((video) => video.id !== videoId))
  }

  

  const getStatusIcon = (status: VideoSource["status"]) => {
    switch (status) {
      case "processing":
        return <Loader2 className="h-3 w-3 animate-spin" />
      case "completed":
        return "✓"
      case "error":
        return "✗"
      default:
        return "⏳"
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Video className="h-5 w-5" />
          Video & YouTube Sources
        </CardTitle>
        <CardDescription>
          Add video files or YouTube URLs to extract audio and transcribe content using Whisper AI
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Tabs defaultValue="youtube" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger
              value="youtube"
              className="flex items-center gap-2"
            >
              <Youtube className="h-4 w-4" />
              YouTube
            </TabsTrigger>
            <TabsTrigger
              value="file"
              className="flex items-center gap-2"
            >
              <FileVideo className="h-4 w-4" />
              Video File
            </TabsTrigger>
          </TabsList>

          <TabsContent value="youtube" className="space-y-4">
            <div className="flex gap-2">
              <Input
                placeholder="https://youtube.com/watch?v=..."
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && addYouTubeVideo()}
                
              />
              <Button onClick={addYouTubeVideo} disabled={isProcessing}>
                {isProcessing ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
              </Button>
            </div>
            <p className="text-xs text-muted-foreground">Supports YouTube videos, shorts, and playlists</p>
          </TabsContent>

          <TabsContent value="file" className="space-y-4">
            <div className="flex gap-2">
              <Input
                placeholder="https://example.com/video.mp4"
                value={videoFileUrl}
                onChange={(e) => setVideoFileUrl(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && addVideoFile()}
                
              />
              <Button onClick={addVideoFile} disabled={isProcessing}>
                {isProcessing ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
              </Button>
            </div>
            <p className="text-xs text-muted-foreground">Supports MP4, MKV, AVI, MOV, and other common video formats</p>
          </TabsContent>
        </Tabs>

        <div className="space-y-3 max-h-48 overflow-y-auto pr-2">
          {videos.map((video) => (
            <div key={video.id} className="border rounded-lg p-3 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {video.type === "youtube" ? (
                    <Youtube className="h-4 w-4 text-red-500" />
                  ) : (
                    <FileVideo className="h-4 w-4 text-blue-500" />
                  )}
                  <span className="text-sm font-medium truncate max-w-xs">
                    {video.title || video.url}
                  </span>
                  {video.duration && (
                    <Badge variant="outline" className="text-xs">
                      {video.duration}
                    </Badge>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={video.status === 'error' ? 'destructive' : 'secondary'} className="text-xs flex items-center gap-1">
                    {getStatusIcon(video.status)}
                    {video.status}
                  </Badge>
                  <X className="h-4 w-4 cursor-pointer text-red-500" onClick={() => removeVideo(video.id)} />
                </div>
              </div>

              {video.status === "processing" && video.progress !== undefined && (
                <div className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span>Transcribing...</span>
                    <span>{video.progress}%</span>
                  </div>
                  <Progress value={video.progress} className="h-2" />
                </div>
              )}

              {video.transcription && (
                <div className="bg-gray-50 p-2 rounded text-xs">
                  <p className="text-muted-foreground mb-1">Transcription Preview:</p>
                  <p className="line-clamp-2">{video.transcription.slice(0, 200)}...</p>
                </div>
              )}
            </div>
          ))}
        </div>

        {videos.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            <Video className="h-12 w-12 mx-auto mb-2 opacity-50" />
            <p>No videos added yet</p>
            <p className="text-xs text-muted-foreground">Add YouTube URLs or video file links to get started</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
