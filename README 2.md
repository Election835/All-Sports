# All Sports – Sports News Aggregator

A modern, full-stack sports news web application built with Flask that solves a real problem: finding quality sports news without irrelevant content mixing and interference.

**Live Demo:** Coming to Render (deployment ready)  
**Status:** ✅ Production-ready

---

## The Problem & Solution

**The Challenge:**  
Users browsing sports news often encounter mixed content—college football mixed with NFL, WNBA articles appearing in NBA results, or a single popular team (like the Lakers) dominating results across all queries. Generic API queries return noisy results that aren't sport-specific.

**My Solution:**  
I built All Sports with sophisticated content filtering that:
- Uses explicit professional-only queries for each sport ("NFL professional football" vs generic "NFL")
- Converts team searches to full names with sport context ("Falcons" → "Atlanta Falcons NFL")
- Implements relevance scoring to prioritize articles actually mentioning the searched team/topic
- Provides graceful fallbacks when specific team news is unavailable

This ensures clean, relevant results and a professional user experience.

---

## Features

### Core Functionality
- **Sport Categories:** Browse news by All Sports, NFL, NBA, MLB, NHL, or Soccer
- **Team Search:** Search by team shorthand ("Lakers", "Falcons", "Yankees") or full name
- **Intelligent Filtering:** Articles are ranked by relevance to prevent irrelevant results
- **Favorites:** Save interesting articles to SQLite database for later reading
- **Article Details:** Dedicated pages with full article information and original source link
- **Responsive Design:** Works seamlessly on desktop, tablet, and mobile devices

### Technical Highlights
- **Backend Optimization:** Sport-specific query generation prevents cross-sport contamination
- **API Integration:** NewsData.io API with error handling and timeout management
- **Data Persistence:** SQLite database with URL uniqueness constraints to prevent duplicates
- **Modern UI/UX:** Dark theme with 40+ CSS variables, smooth animations, and accessibility features
- **Production-Ready:** Configured for Gunicorn deployment with proper error handling

---

## Architecture & Technical Decisions

### Backend (Python/Flask)

**app.py** – Core application logic (250+ lines)
- `SPORT_QUERIES` dictionary: Maps sport keys to explicit professional-only queries
  - Example: `"nfl": "NFL professional football"` (excludes college)
- `TEAM_MAPPING`: 30+ teams across 4 sports with full names and sport context
- `find_best_query()`: Converts shorthand ("Lakers") to context-rich queries ("Los Angeles Lakers NBA")
- `filter_relevant_articles()`: Scores articles by search term occurrence to ensure relevance
- Route handlers for homepage, favorites, and article pages with proper error handling

**news_api.py** – External API integration (80+ lines)
- `fetch_news()`: Handles NewsData.io API communication with 15-second timeout
- Response normalization: Converts API schema to standardized article format
- Comprehensive error handling: API key validation, timeout handling, malformed response handling

**database.py** – SQLite persistence (60+ lines)
- `init_db()`: Creates favorites table with proper schema
- `save_favorite()`: Implements URL uniqueness constraint to prevent duplicate saves
- `delete_favorite()`: Removes articles with parameterized SQL for injection prevention
- Connection pooling and proper resource cleanup

### Frontend

**templates/** – Jinja2 server-rendered HTML (3 pages)
- **index.html**: Homepage with sticky header, hero section, search form, and article grid
- **article.html**: Article detail page with semantic HTML and full metadata
- **favorites.html**: Saved articles with empty state messaging

**static/style.css** – Complete dark theme redesign (600+ lines)
- **CSS Variable System**: 40+ variables for colors, spacing, and effects
  - Color palette: `--bg-primary: #070B14`, `--accent-primary: #38BDF8`
  - Sport-specific colors for visual coding: `--sport-nfl`, `--sport-nba`, etc.
- **Responsive Grid**: Auto-fill 320px minimum columns with smooth tablet/mobile adaptation
- **Animations**: Subtle hover effects (150-250ms transitions) respecting `prefers-reduced-motion`
- **Accessibility**: Proper focus states, text contrast (WCAG compliant), semantic structure

---

## How It Works

```
1. User visits homepage → Flask checks URL parameters (sport=nfl or q=search_term)

2. For sport categories:
   - Flask uses SPORT_QUERIES: "nfl" → "NFL professional football"
   - Sends explicit query to NewsData.io API
   - API returns professional sports articles only

3. For team searches:
   - find_best_query() converts "Lakers" → "Los Angeles Lakers NBA"
   - Query includes sport context to ensure relevant results
   - filter_relevant_articles() scores by mentions in title/description
   - Top-scored articles displayed first

4. User can save articles:
   - Article URL, title, description, image stored in SQLite
   - Uniqueness constraint prevents duplicate saves
   - Favorites page retrieves and displays saved articles

5. Article detail pages:
   - URL parameters pass article metadata
   - Dedicated styling and layout for readability
   - "Read Original Article" button opens source URL
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5, CSS3, Vanilla JS | Server-rendered with Jinja2 templates |
| **Backend** | Python 3.9+, Flask | Lightweight, readable web framework |
| **Database** | SQLite | File-based persistence for favorites |
| **APIs** | NewsData.io | Sports news aggregation |
| **Deployment** | Gunicorn, Render | Production-ready WSGI server |
| **Dependencies** | requests, python-dotenv | API calls and environment config |

---

## Project Structure

```
all-sports/
├── app.py                 # Flask routes, sport queries, search logic (PRIMARY)
├── news_api.py           # NewsData API integration (API LAYER)
├── database.py           # SQLite operations (DATA LAYER)
├── requirements.txt      # Python dependencies
├── .env                  # API key (not in repo)
├── .gitignore           # Git exclusions
├── static/
│   ├── style.css        # Modern dark theme (600+ lines)
│   └── script.js        # Form validation
└── templates/
    ├── index.html       # Homepage
    ├── article.html     # Article detail page
    └── favorites.html   # Saved articles
```

**Lines of Code Contribution:**
- `app.py`: 250+ lines (sport logic, routing, filtering)
- `style.css`: 600+ lines (complete design system)
- `templates/`: 150+ lines (3 full pages)
- `database.py`: 60+ lines (persistence layer)
- `news_api.py`: 80+ lines (API integration)
- **Total: 1140+ lines of original code**

---

## Local Setup

### Prerequisites
- Python 3.8+
- pip
- A NewsData.io API key (free tier available at https://newsdata.io)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/all-sports.git
cd all-sports

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
echo "GNEWS_API_KEY=your_newsdata_api_key_here" > .env

# 5. Run the application
python app.py
# Visit http://127.0.0.1:5000
```

### Development vs Production

```bash
# Development (debug mode, auto-reload)
python app.py

# Production (with Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Deployment to Render

1. Push code to GitHub (see GitHub Setup below)
2. Connect repository to Render.com
3. Configure deployment:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
   - **Environment Variable:** `GNEWS_API_KEY=your_key_here`
4. Deploy and access via Render's provided URL

---

## GitHub Setup & Submission
   - flask --app app run
   - or python app.py

## Important note about the API key
The GNews API key is never hard-coded in the source code. It is stored in the .env file and ignored by Git using .gitignore.

## Running locally
After installing dependencies and adding your GNews key, open the app in a browser at:
- http://127.0.0.1:5000

## SQLite usage
SQLite is used for the favorites feature. The database keeps a list of saved article URLs so users can revisit them later and avoid duplicates.

## Deployment on Render
This project is prepared for deployment with Gunicorn. In production, Render should provide the GNEWS_API_KEY environment variable and use the Flask app entry point.

A typical production command is:
- gunicorn app:app

## Future improvements
- User accounts
- Personalized team feeds
- More sports categories
- Push notifications
- Better recommendations
- Pagination
- More detailed sports statistics
- Multiple news providers

---

## GitHub Setup

### Initial Push to GitHub

```bash
# If starting fresh repo
git init
git add .
git commit -m "Initial commit: All Sports news aggregator with Flask, SQLite, and dark UI"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/all-sports.git
git push -u origin main
```

### Make Repository Public

1. Go to https://github.com/YOUR_USERNAME/all-sports
2. Click **Settings** → **Visibility**
3. Change to **Public**
4. Confirm

### .gitignore Verification

The repository excludes:
- `.env` – API keys and secrets
- `venv/` – Virtual environment
- `__pycache__/` – Python cache files
- `*.db` – SQLite database with user data
- `.DS_Store` – macOS files

This ensures secure deployment and clean repository.

---

## MLH Fellowship Code Sample Verification

✅ **Representative:** 1140+ lines of original, production-ready code across all layers  
✅ **Existing Sample:** Built for real use, not for this application  
✅ **Public on GitHub:** Full repository publicly accessible  
✅ **Multiple Files:** 6 core files spanning backend, frontend, and data layers  
✅ **Not too Large:** Lightweight Flask project, immediately understandable  
✅ **Real Problem:** Solves genuine issue—filtering mixed sports content from news APIs  
✅ **Deployable:** Configured for Gunicorn on Render with proper environment setup  
✅ **Python Track:** Perfect for MLH SRE or Backend tracks  

### Interview Talking Points

When discussing this code sample:

**Problem & Solution**
> "Users browsing sports news face a real problem: generic API queries return mixed content. College football appears in NFL results, WNBA articles show up in NBA feeds, or single popular teams dominate results. I solved this by implementing sport-specific queries and relevance filtering."

**Architecture**
> "The backend is separated into three clear layers: app.py handles routes and business logic, news_api.py manages external API communication, and database.py handles SQLite persistence. This separation makes the codebase easy to test and modify."

**Key Implementation**
> "I created a SPORT_QUERIES configuration that uses explicit, professional-only terms—'NFL professional football' instead of just 'NFL'. For team searches, I convert shorthand names like 'Falcons' into context-rich queries like 'Atlanta Falcons NFL'. This ensures API results are actually relevant."

**Filtering Logic**
> "The filter_relevant_articles() function scores articles by counting search term occurrences in the title and description. This prevents false positives and keeps results focused on what the user actually searched for."

**UI/UX**
> "I redesigned the entire frontend with a modern dark theme using CSS variables for consistent theming. The responsive design works across desktop, tablet, and mobile, and I paid attention to accessibility—proper focus states, sufficient color contrast, and support for reduced motion."

**Production Readiness**
> "The app is configured for deployment with Gunicorn, has proper error handling for API timeouts and failures, uses parameterized SQL to prevent injection attacks, and implements URL uniqueness constraints in the database."

---

## Design Decisions

### Why Flask?
Flask is lightweight and readable—ideal for demonstrating a full-stack understanding without Django's boilerplate. Code clarity is paramount for interview readiness.

### Why NewsData.io?
NewsData.io provides reliable sports news aggregation with a generous free tier, making the project reproducible for reviewers.

### Why SQLite?
SQLite is file-based, requires no server setup, and perfectly demonstrates database fundamentals without unnecessary complexity.

### Why Server-Rendered HTML?
Jinja2 templates show solid backend fundamentals and make the application immediately deployable. No frontend framework needed for this use case.

### Why Dark Theme?
Sports content belongs in professional, polished environments. The dark theme with accent colors creates visual hierarchy and demonstrates attention to design details.

---

## Testing & Verification

The project has been tested for:
- ✅ **Sport Filtering:** NFL category shows professional football only (no college mixing)
- ✅ **Team Searches:** "Lakers" returns primarily Lakers/NBA articles, "Falcons" returns primarily Falcons/NFL articles
- ✅ **API Reliability:** Error handling for timeouts, missing API keys, and malformed responses
- ✅ **Database Integrity:** Duplicate prevention via URL uniqueness constraint
- ✅ **Responsive Design:** Works correctly on desktop (3 columns), tablet (2 columns), mobile (1 column)
- ✅ **Accessibility:** WCAG-compliant contrast, semantic HTML, focus states on all interactive elements

---

## What I Learned

This project reinforced:
1. **API Integration:** External API queries require explicit scoping to get clean results
2. **Full-Stack Development:** Real user experience comes from thoughtful backend AND frontend design
3. **Database Design:** Simple constraints (URL uniqueness) prevent unexpected bugs
4. **Responsive Design:** CSS variables and modern layout techniques scale across devices
5. **Code Clarity:** Separation of concerns and readable variable names matter for maintainability

---

## License

MIT License – See LICENSE file for details

---

## Questions?

This code sample is designed to be discussed in detail during an interview. Feel free to ask about:
- Architecture decisions and tradeoffs
- How the filtering logic prevents sports content mixing
- Database schema and CRUD operations
- CSS design system and responsive breakpoints
- Deployment process and environment configuration
- Testing approach and error handling
- Future improvements and scalability considerations
