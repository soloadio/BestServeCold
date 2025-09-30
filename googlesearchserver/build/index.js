import express from "express";
import dotenv from "dotenv";
import { z } from "zod";
import { customsearch } from "@googleapis/customsearch";

// Load environment variables
dotenv.config();

// Collect all keys dynamically without assuming any are valid
const allKeys = [];
for (let i = 0; i < 10; i++) { // adjust 10 if you expect more
  const key = process.env[`GOOGLE_API_KEY${i}`];
  const cx = process.env[`GOOGLE_SEARCH_ENGINE_ID${i}`];
  if (key && cx) {
    allKeys.push({ key, cx, index: i });
  }
}

if (allKeys.length === 0) {
  console.error("❌ No Google API keys found in environment variables!");
  process.exit(1);
}

// Initialize Google Custom Search API client
const searchClient = customsearch("v1");

// Function to test a key
async function testKey({ key, cx, index }) {
  try {
    const response = await searchClient.cse.list({
      auth: key,
      cx,
      q: "test", // a very basic query to validate
      num: 1,
    });

    if (response.data.items && response.data.items.length > 0) {
      console.log(`✅ API key ${index} is valid and working.`);
      return true;
    } else {
      console.warn(`⚠️ API key ${index} responded but no results returned.`);
      return false;
    }
  } catch (error) {
    if (error?.response?.status === 429) {
      console.warn(`⚠️ API key ${index} hit quota limit at startup.`);
      return false;
    } else if (error?.response?.status === 403) {
      console.warn(`❌ API key ${index} is invalid or unauthorized.`);
      return false;
    } else {
      console.error(`❌ API key ${index} test failed:`, error.message);
      return false;
    }
  }
}

// Filter keys down to only valid ones
async function filterWorkingKeys() {
  const workingKeys = [];
  for (const keyObj of allKeys) {
    const works = await testKey(keyObj);
    if (works) workingKeys.push(keyObj);
  }
  return workingKeys;
}

let keys = [];

(async () => {
  keys = await filterWorkingKeys();
  if (keys.length === 0) {
    console.error("❌ No valid API keys available after testing!");
    process.exit(1);
  } else {
    console.log(`✅ ${keys.length} valid API keys loaded and ready.`);
  }
})();

// Express setup
const app = express();
app.use(express.json());

// Root route
app.get("/", (_req, res) => {
  res.send("MCP Google Custom Search server is running!");
});

// Search endpoint
const SearchArgumentsSchema = z.object({
  query: z.string().min(1),
  numResults: z.number().min(1).max(10).optional().default(5),
});

app.post("/search", async (req, res) => {
  try {
    const { query, numResults } = SearchArgumentsSchema.parse(req.body);
    console.log(`🔍 Search request: "${query}", numResults=${numResults}`);

    let lastError;

    for (let i = 0; i < keys.length; i++) {
      const { key, cx, index } = keys[i];
      try {
        const response = await searchClient.cse.list({
          auth: key,
          cx,
          q: query,
          num: numResults,
        });

        const results = response.data.items?.map((item, idx) => ({
          resultNumber: idx + 1,
          title: item.title || "No title",
          url: item.link || "No URL",
          description: item.snippet || "No description",
        })) || [];

        console.log(`✅ Search successful with key ${index}. Found ${results.length} results.`);
        return res.json({ results });
      } catch (error) {
        lastError = error;
        if (error?.response?.status === 429) {
          console.warn(`⚠️ Quota exceeded for key ${index}. Switching to next key...`);
          continue;
        } else {
          console.error(`❌ Search failed with key ${index}:`, error.message);
          return res.status(500).json({ error: "Search failed" });
        }
      }
    }

    console.error("❌ All API keys have been exhausted.", lastError?.message);
    res.status(429).json({ error: "All API keys have exceeded their quota" });
  } catch (error) {
    console.error("❌ Request error:", error.message);
    res.status(400).json({ error: "Invalid request" });
  }
});

// Start server if not on Vercel
if (!process.env.VERCEL) {
  const port = process.env.PORT || 81;
  app.listen(port, () => console.log(`🚀 Server running at http://localhost:${port}`));
}

export default app;