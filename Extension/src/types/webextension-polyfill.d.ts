declare module 'webextension-polyfill' {
  const browser: {
    runtime: {
      sendMessage: (message: any) => Promise<any>;
      onMessage: {
        addListener: (callback: (message: any, sender: any) => void | Promise<any>) => void;
        removeListener: (callback: (message: any, sender: any) => void | Promise<any>) => void;
      };
      getURL: (path: string) => string;
      onInstalled: {
        addListener: (callback: () => void) => void;
      };
    };
    storage: {
      local: {
        get: (keys?: string | string[] | null) => Promise<Record<string, any>>;
        set: (items: Record<string, any>) => Promise<void>;
        remove: (keys: string | string[]) => Promise<void>;
        clear: () => Promise<void>;
      };
      sync: {
        get: (keys?: string | string[] | null) => Promise<Record<string, any>>;
        set: (items: Record<string, any>) => Promise<void>;
        remove: (keys: string | string[]) => Promise<void>;
        clear: () => Promise<void>;
      };
    };
    tabs: {
      query: (queryInfo: any) => Promise<any[]>;
      sendMessage: (tabId: number, message: any) => Promise<any>;
      create: (createProperties: any) => Promise<any>;
      captureVisibleTab: (windowId?: number, options?: { format?: string, quality?: number }) => Promise<string>;
    };
    contextMenus: {
      create: (properties: any) => number | string;
      update: (id: number | string, properties: any) => Promise<void>;
      remove: (id: number | string) => Promise<void>;
      removeAll: () => Promise<void>;
      onClicked: {
        addListener: (callback: (info: any, tab: any) => void) => void;
      };
    };
    notifications: {
      create: (id: string | undefined, options: {
        type: 'basic' | 'image' | 'list' | 'progress';
        iconUrl?: string;
        title: string;
        message: string;
        priority?: number;
      }) => Promise<string>;
      clear: (id: string) => Promise<boolean>;
      onClicked: {
        addListener: (callback: (notificationId: string) => void) => void;
      };
    };
  };
  
  export default browser;
} 