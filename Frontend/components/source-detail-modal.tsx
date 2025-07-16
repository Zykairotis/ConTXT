"use client"

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogClose } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

type SourceType = 'webUrls' | 'files' | 'videos' | 'libraries';

interface SourceDetailModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  sources: any[];
  sourceType: SourceType;
}

const formatBytes = (bytes: number, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

export function SourceDetailModal({ isOpen, onClose, title, sources, sourceType }: SourceDetailModalProps) {

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          {sources.length > 0 ? (
            <div className="space-y-3 max-h-60 overflow-y-auto pr-2">
              {sources.map((source, index) => (
                <div key={index} className="text-sm p-2 rounded-md border">
                  {sourceType === 'webUrls' && (
                    <a href={source} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline break-all">
                      {source}
                    </a>
                  )}
                  {sourceType === 'files' && source instanceof File && (
                    <div>
                      <p className="font-medium text-foreground break-all">{source.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {formatBytes(source.size)} - {source.type}
                      </p>
                    </div>
                  )}
                  {sourceType === 'videos' && (
                    <a href={source} target="_blank" rel="noopener noreferrer" className="text-red-500 hover:underline break-all">
                      {source}
                    </a>
                  )}
                  {sourceType === 'libraries' && (
                    <p className="text-foreground break-all">{source}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No sources have been added yet.</p>
          )}
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button type="button" variant="secondary">
              Close
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
