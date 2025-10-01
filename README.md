# AI Travel Vlogger

AI Travel Vlogger is a full‑stack application that generates day‑by‑day travel blog itineraries. A FastAPI backend orchestrates multiple AI agents to discover attractions, suggest local foods, build a balanced itinerary, and narrate each day in a vlogger tone. A React frontend renders the results as a clean, scrollable blog.

##Team Members:
23Z308 - Archana S
23Z336 - Krishnika K
23Z354 - Prahalya S
23Z380 - Yugandhara J
24Z432 - Desigaa R
24Z467 - Sarithra N
## Table of Contents

- What the project does
- Architecture and technology
- Data contracts (API)
- Local development setup
- Production deployment (Render + Netlify)
- Configuration (environment variables)
- Troubleshooting
- Project structure
- Customization notes
- License

## What the project does

- Accepts a user‑provided location and optional preferences (number of days, style).
- Runs a sequence of agents:
  - Explorer Agent: finds 5–10 attractions.
  - Foodie Agent: suggests local food items or venues.
  - Guide Agent: builds a multi‑day itinerary using attractions and foods.
  - Vlogger Agent: narrates each day in an engaging blog/vlog voice.
- Returns a JSON payload with attractions, foods, itinerary, narration, and an evaluation score.
- Renders a day‑by‑day blog UI in React.

## Architecture and technology

- Backend: FastAPI, LangChain/LangGraph, Google Gemini (via `langchain-google-genai`).
- Frontend: React (Create React App) + TypeScript.
- Optional tool: Tavily web search (disabled by default for Gemini; demo stubs provided).
- Auth: none by default; add a gateway/keys if deploying publicly.

## Data contracts (API)

Endpoint
- POST `/generate`

Request body
```json
{
  "location": "Tokyo",
  "user_prefs": {
    "duration": 3,
    "style": "fun"
  }
}
```

Response payload
```json
{
  "location": "Tokyo",
  "user_prefs": { "duration": 3, "style": "fun" },
  "attractions": [ { "name": "...", "description": "...", "category": "..." } ],
  "foods": [ { "name": "...", "description": "...", "type": "..." } ],
  "itinerary": [
    { "day": 1, "activities": [ { "time": "Morning", "item": "...", "details": "..." } ] }
  ],
  "narration": [ "Day 1 narration..." ],
  "evaluation_score": 8.7
}
```

## Local development setup

Prerequisites
- Python 3.10+
- Node.js 16+
- Google AI API key (GOOGLE_API_KEY)

Clone and open
```bash
git clone <your-repo-url>
cd ai-travel-vlogger
```

Backend
```bash
cd backend
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt

# Create .env (same directory as main.py)
# Example values:
```
GOOGLE_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-1.5-flash
DEMO_MODE=true
# Optional
TAVILY_API_KEY=your_tavily_key
```

# Run backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Frontend
```bash
cd ../frontend
npm install

# Create frontend/.env
```
REACT_APP_API_URL=http://localhost:8000
# Optional extras used if you add maps/images later
REACT_APP_GOOGLE_MAPS_API_KEY=
REACT_APP_UNSPLASH_API_KEY=
```

```bash
npm start
# Open http://localhost:3000
```

Notes
- DEMO_MODE=true returns mock data without calling Gemini (useful for development).
- When ready to use Gemini, set DEMO_MODE=false and ensure GOOGLE_API_KEY is valid.

## Production deployment (Render + Netlify)

Backend on Render
1. Create a new Web Service on Render and connect this repository.
2. Root directory: `ai-travel-vlogger/backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Environment variables (Render → Settings → Environment):
   - `GOOGLE_API_KEY=...`
   - `GEMINI_MODEL=gemini-1.5-flash`
   - `DEMO_MODE=false` (or `true` for mock data)
   - Optional: `TAVILY_API_KEY=...`
6. CORS: in `backend/main.py`, set `allow_origins` to include your Netlify site:
   - `https://<your-site>.netlify.app` and `http://localhost:3000`

Frontend on Netlify
1. New site from Git. Base directory: `ai-travel-vlogger/frontend`
2. Build command: `npm install && npm run build`
3. Publish directory: `build`
4. Environment variables (Site settings → Environment):
   - `REACT_APP_API_URL=https://<your-backend-on-render>.onrender.com`
   - Optional: `REACT_APP_GOOGLE_MAPS_API_KEY`, `REACT_APP_UNSPLASH_API_KEY`
5. Redeploy after changing environment variables (CRA inlines them at build time).

Alternative (no code change): Netlify redirect
- Add `frontend/public/_redirects` with:
```
/generate  https://<your-backend-on-render>.onrender.com/generate  200
```
- Then the frontend may POST `/generate` and Netlify forwards to Render.

## Configuration (environment variables)

Backend `.env`
- `GOOGLE_API_KEY` (required for Gemini)
- `GEMINI_MODEL` (default `gemini-1.5-flash`)
- `DEMO_MODE` (`true` or `false`)
- `TAVILY_API_KEY` (optional)

Frontend `.env`
- `REACT_APP_API_URL` (required in production)
- `REACT_APP_GOOGLE_MAPS_API_KEY` (optional)
- `REACT_APP_UNSPLASH_API_KEY` (optional)

Security note
- Frontend env vars are public after build. Put sensitive keys in backend `.env` and proxy via backend if needed.

## Troubleshooting

Build fails on Netlify (eslint/CI)
- Ensure imports are at the top of each file.
- If necessary, set `CI=false` in Netlify environment to avoid treating warnings as errors.

Frontend shows “Cannot POST /generate”
- In production, CRA proxy does not apply. Ensure `REACT_APP_API_URL` points to your Render backend and that the code uses `fetch(`${API_BASE}/generate`)`.
- Or add the Netlify redirect shown above.

CORS errors
- The origin must match exactly (protocol, host). Update `allow_origins` in `main.py` to include your Netlify URL.

500 errors or JSON parsing
- Set `DEMO_MODE=true` to validate the full UI.
- The backend includes tolerant JSON extraction; check server logs for the first failing agent.

429 / quota exceeded
- Temporary: set `DEMO_MODE=true`.
- Ensure keys and quotas are active for your account.

## Project structure

```
ai-travel-vlogger/
├─ backend/
│  ├─ agents/
│  │  ├─ explorer.py
│  │  ├─ foodie.py
│  │  ├─ guide.py
│  │  ├─ vlogger.py
│  │  └─ evaluator.py
│  ├─ api/
│  │  └─ endpoints.py
│  ├─ graph/
│  │  └─ workflow.py
│  ├─ models/
│  │  └─ state.py
│  ├─ tools/
│  │  └─ web_search.py
│  ├─ main.py
│  └─ requirements.txt
└─ frontend/
   ├─ public/
   │  ├─ index.html
   │  └─ _redirects (optional)
   ├─ src/
   │  ├─ App.tsx
   │  ├─ App.css
   │  └─ index.tsx
   └─ package.json
```

## Customization notes

- To change AI behavior, adjust system prompts in `backend/agents/*.py`.
- To change flow or add agents, edit `backend/graph/workflow.py`.
- To add images or maps, read keys from frontend `.env` and implement fetches in `App.tsx` (or proxy via backend to keep keys private).

## License

This project is open source; you may use, modify, and distribute per the repository license.
