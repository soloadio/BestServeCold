export {};

declare global {
  interface Window {
    handleCredentialResponse: (response: any) => void;
  }
}