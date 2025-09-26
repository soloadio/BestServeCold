import express from "express";
import bodyParser from "body-parser";
import { performSearch, formatSearchResults } from "./index.js";

const app = express();
app.use(bodyParser.json());

app.post("/search", async (req, res) => {
  const { query } = req.body;

  if (!query) {
    return res.status(400).json({ error: "Query is required" });
  }

  try {
    const results = await performSearch(query, 5); // top 5 results
    res.json(formatSearchResults(results));
  } catch (error) {
    console.error("Search error:", error);
    res.status(500).json({ error: "Search failed" });
  }
});

app.get("/", (req, res) => {
  res.send("MCP search server is running!");
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`MCP search server running on port ${PORT}`);
});

