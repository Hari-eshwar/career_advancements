/// <reference types="vite/client" />

declare module 'firebase/firestore' {
  export * from '@firebase/firestore';
}

// jsPDF v4 does not ship its own TypeScript declarations
// Using `any` type to avoid circular declaration reference
// @types/jspdf can be installed for full type safety if needed
declare module 'jspdf' {
  const jsPDF: any;
  export default jsPDF;
}
