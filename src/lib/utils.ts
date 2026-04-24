import { clsx, type ClassValue } from 'clsx';
  import { twMerge } from 'tailwind-merge';

  export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
  }

  export interface FirestoreErrorInfo {
    error: string;
    operationType: 'create' | 'update' | 'delete' | 'list' | 'get' | 'write';
    path: string | null;
    authInfo: {
      userId: string;
      email: string;
      emailVerified: boolean;
      isAnonymous: boolean;
    } | null;
  }

  export function handleFirestoreError(error: any, operationType: FirestoreErrorInfo['operationType'], path: string | null = null, auth: any = null): never {
    const errorInfo: FirestoreErrorInfo = {
      error: error.message || 'Unknown Firestore error',
      operationType,
      path,
      authInfo: auth?.currentUser ? {
        userId: auth.currentUser.uid,
        email: auth.currentUser.email || '',
        emailVerified: auth.currentUser.emailVerified,
        isAnonymous: auth.currentUser.isAnonymous,
      } : null
    };

    console.error('Firestore Error Details:', errorInfo);
    throw new Error(JSON.stringify(errorInfo));
  }
