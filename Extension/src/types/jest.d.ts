// This file provides TypeScript type definitions for Jest functions
declare const jest: {
  fn: () => jest.Mock;
  mock: (moduleName: string, factory?: () => unknown) => void;
};

declare namespace jest {
  interface Mock<T = any, Y extends any[] = any[]> {
    (...args: Y): T;
    mockImplementation: (fn: (...args: Y) => T) => Mock<T, Y>;
    mockReturnValue: (value: T) => Mock<T, Y>;
    mockResolvedValue: <U>(value: U) => Mock<Promise<U>, Y>;
    mockRejectedValue: <U>(value: U) => Mock<Promise<U>, Y>;
  }
}

declare const describe: (name: string, fn: () => void) => void;
declare const it: (name: string, fn: () => void | Promise<void>) => void;
declare const expect: <T>(value: T) => {
  toBe: (expected: T) => void;
  toEqual: (expected: any) => void;
  // Add other matchers as needed
}; 