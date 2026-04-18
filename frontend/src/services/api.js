const API_URL = "http://127.0.0.1:5000/api/agent/query";

export async function askAgent(query) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Agent request failed");
  }

  return data;
}