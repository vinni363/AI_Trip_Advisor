import re
from datetime import date
from typing import Any

from openai import OpenAI
from pypdf import PdfReader


def read_uploaded_files(uploaded_files: list[Any]) -> list[dict[str, str]]:
    documents = []
    for uploaded_file in uploaded_files:
        if uploaded_file.name.lower().endswith(".pdf"):
            text = "\n".join(page.extract_text() or "" for page in PdfReader(uploaded_file).pages)
        else:
            text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
        if text.strip():
            documents.append({"name": uploaded_file.name, "text": text})
    return documents


def retrieve_context(query: str, documents: list[dict[str, str]], limit: int = 5) -> str:
    chunks = []
    for document in documents:
        paragraphs = re.split(r"\n\s*\n", document["text"])
        for paragraph in paragraphs:
            words = paragraph.split()
            for start in range(0, len(words), 140):
                chunk = " ".join(words[start : start + 180]).strip()
                if chunk:
                    chunks.append((document["name"], chunk))

    query_terms = set(re.findall(r"[a-z0-9]+", query.lower()))
    ranked = sorted(
        chunks,
        key=lambda item: sum(term in set(re.findall(r"[a-z0-9]+", item[1].lower())) for term in query_terms),
        reverse=True,
    )
    return "\n\n".join(f"Source: {name}\n{chunk}" for name, chunk in ranked[:limit])


def generate_plan(
    client: OpenAI,
    model: str,
    destination: str,
    days: int,
    travel_style: str,
    budget: int,
    start_day: date,
    context: str,
    web_search: bool = False,
) -> str:
    prompt = f"""Create a practical {days}-day itinerary for {destination}.
Travel style: {travel_style}
Daily budget: about ₹{budget} INR
Start date: {start_day.isoformat()}

Use only the retrieved travel knowledge below as grounding. For live web research requests, you MUST use the web-search tool before writing the answer and use the returned sources for this exact city. Do not claim that web access is unavailable when the tool is enabled. Do not invent attractions, hotels, restaurants, prices, opening hours, availability, or safety claims. If the sources do not support a detail, write "Not found in the retrieved sources" instead of guessing. Include a short section with hotel or stay examples and a short section with famous restaurant examples supported by the sources. Add the source URL in parentheses after each recommendation when a URL is available. These are suggestions, not bookings; tell the user to verify current prices, availability, reviews, opening hours, and dietary suitability. Keep the plan flexible. Format each day with a heading and Morning, Afternoon, and Evening bullets.

Retrieved travel knowledge:
{context}"""
    request_kwargs = {
        "model": model,
        "temperature": 0.0,
        "messages": [
            {"role": "system", "content": "You are a source-grounded travel advisor. Use only facts explicitly supported by the retrieved sources or web-search results. Never fill missing evidence with memory or plausible guesses. If evidence is insufficient, say so clearly."},
            {"role": "user", "content": prompt},
        ],
    }
    if web_search:
        request_kwargs["extra_body"] = {
            "plugins": [
                {
                    "id": "web",
                    "engine": "exa",
                    "max_results": 8,
                    "search_prompt": "Find current, reputable sources for attractions, hotels, restaurants, transport, and safety information.",
                }
            ]
        }
    response = client.chat.completions.create(**request_kwargs)
    return response.choices[0].message.content or "The advisor returned an empty plan. Please try again."
