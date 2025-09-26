import express from "express";
import dotenv from "dotenv";
import { z } from "zod";
import { customsearch_v1, customsearch } from "@googleapis/customsearch";

// Load environment variables
dotenv.config();

// Validate environment variables
const EnvSchema = z.object({
  GOOGLE_API_KEY: z.string().min(1),
  GOOGLE_SEARCH_ENGINE_ID: z.string().min(1),
});
const env = EnvSchema.safeParse(process.env);
if (!env.success) {
  console.error("❌ Invalid environment variables:", env.error.flatten().fieldErrors);
  process.exit(1);
}
const { GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID } = env.data;

// Initialize Custom Search API client
const searchClient = customsearch("v1");

// Express server setup
const app = express();
app.use(express.json());

// Root route for testing
app.get("/", (_req, res) => {
  res.send("MCP Google Custom Search server is running!");
});

// /search POST endpoint
const SearchArgumentsSchema = z.object({
  query: z.string().min(1),
  numResults: z.number().min(1).max(10).optional().default(5),
});

app.post("/search", async (req, res) => {
  try {
    const { query, numResults } = SearchArgumentsSchema.parse(req.body);

    const response = await searchClient.cse.list({
      auth: GOOGLE_API_KEY,
      cx: GOOGLE_SEARCH_ENGINE_ID,
      q: query,
      num: numResults,
    });

    const results = response.data.items?.map((item, index) => ({
      resultNumber: index + 1,
      title: item.title || "No title",
      url: item.link || "No URL",
      description: item.snippet || "No description",
    })) || [];

    res.json({ results });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: error.errors });
    }
    console.error("Search error:", error);
    res.status(500).json({ error: "Search failed" });
  }
});

// Start server if running locally
if (process.env.VERCEL === undefined) {
  const port = process.env.PORT || 3000;
  app.listen(port, () => console.log(`Server running at http://localhost:${port}`));
}

export default app;
