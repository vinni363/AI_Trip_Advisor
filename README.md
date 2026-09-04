# Wanderwise AI Trip Advisor

A Streamlit trip-planning app that creates a flexible itinerary from a destination, travel mood, trip length, date, and daily budget.

## Project structure

```text
AI_Trip_Advisor/
├── app.py             # Streamlit interface and session state
├── styles.py           # Streamlit theme and CSS
├── rag.py              # RAG and AI generation
├── travel_knowledge.py # Vector knowledge base and search
├── requirements.txt   # Python dependencies
├── README.md          # Setup and usage instructions
├── .gitignore         # Keeps .env and cache files out of Git
└── .env                # Local API key, never commit this file
```

## Run locally

```powershell
cd "C:\Users\knvin\OneDrive\Desktop\python\AI_Trip_Advisor"
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Then open the local URL shown in the terminal, usually `http://localhost:8501`.

## Use the RAG advisor

Create a `.env` file in the project folder:

```env
# Use OPENAI_API_KEY for OpenAI, or OPENROUTER_API_KEY for an OpenRouter key
OPENROUTER_API_KEY=sk-or-your-openrouter-key
```

Then launch the app:

```powershell
python -m streamlit run app.py
```

The app supports OpenAI and OpenRouter keys, and automatically detects OpenRouter keys beginning with `sk-or-`. The user enters only a city; supported South India destinations use the built-in TF-IDF knowledge base, while other cities use OpenRouter's explicit web-search plugin. Web-grounded recommendations must include sources and unsupported details are rejected by the prompt. The model key is loaded from `.env` and is not shown in the frontend. Add `.env` to `.gitignore` so it is never committed.
