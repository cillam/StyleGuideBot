export const sessionManager = {
  // Generate a new session ID
  generateSessionId: () => {
    return crypto.randomUUID();
  },

  // Get current session ID from sessionStorage
  getSessionId: () => {
    let sessionId = sessionStorage.getItem('styleGuideBot_sessionId');
    
    if (!sessionId) {
      sessionId = sessionManager.generateSessionId();
      sessionStorage.setItem('styleGuideBot_sessionId', sessionId);
    }
    
    return sessionId;
  },

  // Clear current session (start fresh)
  clearSession: () => {
    sessionStorage.removeItem('styleGuideBot_sessionId');
  }
};