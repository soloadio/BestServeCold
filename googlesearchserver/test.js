import { performSearch, formatSearchResults } from "./build/index.js";

async function main() {
  const query = "Ying Fu Li Lab";
  const results = await performSearch(query, 5);
  console.log(formatSearchResults(results));
}

main();
