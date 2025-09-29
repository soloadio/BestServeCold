declare namespace NodeJS {
  interface ProcessEnv {
    SECRET_KEY: string;
    DEBUG: string;
    ALLOWED_HOSTS: string;
    SERPAPI_KEY: string;
    GEMINI_KEY: string;
    GOOGLE_API_KEY: string;
    CSE_ID: string;
    DATABASE_URL: string;
    CLIENT_ID: string;
    GOOGLE_SEARCH_SERVER: string;
    BACKEND_SERVER: string;
  }
}
