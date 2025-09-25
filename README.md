# AI Travel Vlogger Simulator

A multi-agent AI system that generates personalized travel itineraries with day-by-day blog-style narration. Users input a location, and AI agents collaborate to find attractions, suggest local foods, build itineraries, and create engaging vlog-style content.

## 🎯 What This Project Does

- **Explorer Agent**: Finds 5-10 attractions in your chosen location
- **Foodie Agent**: Suggests local foods and restaurants
- **Guide Agent**: Creates day-by-day itineraries based on your preferences
- **Vlogger Agent**: Narrates the trip in engaging blog/vlog style
- **React Frontend**: Beautiful day-by-day travel blog UI

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (download from [python.org](https://python.org))
- **Node.js 16+** (download from [nodejs.org](https://nodejs.org))
- **Google AI API Key** (free at [makersuite.google.com](https://makersuite.google.com))

### Step 1: Clone and Setup Backend

1. **Clone the repository** (or download as ZIP):
   ```bash
   git clone <your-repo-url>
   cd ai-travel-vlogger
   ```

2. **Navigate to backend**:
   ```bash
   cd backend
   ```

3. **Create virtual environment**:
   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # Windows Command Prompt
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file**:
   ```bash
   # Windows PowerShell
   notepad .env
   
   # macOS/Linux
   nano .env
   ```

6. **Add your API keys to `.env`**:
   ```env
   GOOGLE_API_KEY=your_google_ai_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   TAVILY_API_KEY=your_tavily_key_here
   DEMO_MODE=false
   ```

   **Getting API Keys**:
   - **Google AI**: Go to [makersuite.google.com](https://makersuite.google.com) → Get API Key (free)
   - **Tavily** (optional): Go to [tavily.com](https://tavily.com) → Sign up for free tier

7. **Start the backend server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

### Step 2: Setup Frontend

1. **Open a new terminal** and navigate to frontend:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the React development server**:
   ```bash
   npm start
   ```
   
   This will automatically open http://localhost:3000 in your browser.

### Step 3: Test the Application

1. **Open your browser** to http://localhost:3000
2. **Enter a location** (e.g., "Tokyo", "Paris", "New York")
3. **Choose duration** (1-10 days) and style (Fun, Luxury, Budget, Foodie)
4. **Click Generate** and watch the AI create your travel itinerary!

## 🛠️ Project Structure

```
ai-travel-vlogger/
├── backend/                 # FastAPI backend
│   ├── agents/             # AI agent implementations
│   │   ├── explorer.py     # Finds attractions
│   │   ├── foodie.py       # Suggests local foods
│   │   ├── guide.py        # Builds itineraries
│   │   ├── vlogger.py      # Creates narration
│   │   └── evaluator.py    # Scores output
│   ├── api/                # REST API endpoints
│   ├── graph/              # LangGraph workflow
│   ├── models/             # Data models
│   ├── tools/              # External tools (web search)
│   ├── main.py             # FastAPI app entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.tsx         # Main React component
│   │   └── App.css         # Styling
│   ├── public/
│   └── package.json        # Node.js dependencies
└── README.md               # This file
```

## 🔧 Configuration Options

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Required
GOOGLE_API_KEY=your_google_ai_api_key

# Optional (with defaults)
GEMINI_MODEL=gemini-1.5-flash
TAVILY_API_KEY=your_tavily_key
DEMO_MODE=false
```

### Demo Mode

Set `DEMO_MODE=true` in your `.env` file to test the UI without API calls:
- Returns mock data instantly
- No API costs
- Perfect for development and demos

## 🚨 Troubleshooting

### Common Issues

1. **"Could not import module main"**
   - Make sure you're in the `backend/` directory
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **"OPENAI_API_KEY not found"**
   - You switched to Gemini, so this shouldn't appear
   - If it does, check your `.env` file has `GOOGLE_API_KEY`

3. **Frontend won't start**
   - Make sure you're in the `frontend/` directory
   - Run `npm install` first
   - Check that Node.js is installed

4. **"Port 8000 already in use"**
   - Stop other services on port 8000
   - Or change the port: `uvicorn main:app --reload --port 8001`

5. **API calls fail**
   - Check your Google AI API key is valid
   - Ensure `DEMO_MODE=false` in `.env`
   - Try `DEMO_MODE=true` to test without API calls

### Getting Help

- **Check the logs**: Look at the terminal running `uvicorn` for error details
- **Browser console**: Press F12 in your browser to see frontend errors
- **API testing**: Visit http://localhost:8000/docs for interactive API documentation

## 🎨 Customization

### Adding New Agent Types

1. Create a new file in `backend/agents/`
2. Implement the agent with `ChatGoogleGenerativeAI`
3. Add it to the workflow in `backend/graph/workflow.py`

### Changing the UI

- Modify `frontend/src/App.tsx` for functionality
- Update `frontend/src/App.css` for styling
- The app uses modern CSS Grid and Flexbox

### Different AI Models

- Change `GEMINI_MODEL` in `.env` to:
  - `gemini-1.5-flash` (fast, cheap)
  - `gemini-1.5-pro` (more capable)
  - `gemini-2.0-flash-exp` (experimental)

## 📦 Deployment

### Backend Deployment

1. **Set up production environment**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with production server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Frontend Deployment

1. **Build for production**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Serve the `build/` folder** with any static file server

### Environment Variables for Production

- Set `GOOGLE_API_KEY` in your production environment
- Remove or set `DEMO_MODE=false`
- Consider adding rate limiting and authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- AI powered by [Google Gemini](https://ai.google.dev/)
- Frontend with [React](https://reactjs.org/)
- Workflow orchestration with [LangGraph](https://github.com/langchain-ai/langgraph)

---

**Need help?** Check the troubleshooting section above or create an issue in the repository.
