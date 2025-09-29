import * as dotenv from 'dotenv';
dotenv.config();

export const environment = {
  SECRET_KEY: process.env.SECRET_KEY,
  DEBUG: process.env.DEBUG === 'true',
  ALLOWED_HOSTS: process.env.ALLOWED_HOSTS,

  SERPAPI_KEY: process.env.SERPAPI_KEY,
  GEMINI_KEY: process.env.GEMINI_KEY,
  GOOGLE_API_KEY: process.env.GOOGLE_API_KEY,
  CSE_ID: process.env.CSE_ID,

  DATABASE_URL: process.env.DATABASE_URL,
  CLIENT_ID: process.env.CLIENT_ID,

  GOOGLE_SEARCH_SERVER: process.env.GOOGLE_SEARCH_SERVER,
  BACKEND_SERVER: process.env.BACKEND_SERVER
};