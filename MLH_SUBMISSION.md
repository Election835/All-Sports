# MLH Fellowship Code Sample Submission Guide

This document guides you through preparing and submitting the All Sports project as your MLH Fellowship code sample.

---

## Why All Sports is an Excellent Code Sample

### ✅ Requirement Checklist

| Requirement | Status | Evidence |
|------------|--------|----------|
| **Representative** | ✅ | 1,140+ lines across all layers (backend, frontend, database) |
| **Original Code** | ✅ | Not from tutorial; solves real sports news filtering problem |
| **Public on GitHub** | ✅ | Full repository on GitHub (ready to push) |
| **Multiple Files** | ✅ | 6 core files: app.py, news_api.py, database.py, 3 templates |
| **Substance** | ✅ | Full-stack: API integration, database, responsive frontend |
| **Not Too Large** | ✅ | Lightweight Flask app—code is immediately understandable |
| **Solves Real Problem** | ✅ | Sports news mixing is a real issue (college content in NFL results) |
| **Deployable** | ✅ | Configured for Gunicorn + Render deployment |
| **Not Jupyter** | ✅ | Production web application with end-user interface |
| **Python/Track-Aligned** | ✅ | Perfect for MLH Backend/SRE tracks (Flask, database, API design) |

---

## Preparation Checklist

### Before Pushing to GitHub

- [ ] Remove any personal test data from `favorites.db`
- [ ] Ensure `.env` file is in `.gitignore` (NOT in repository)
- [ ] Verify all code has no temporary comments or debugging output
- [ ] Run a final test of all sport categories (NFL, NBA, etc.)
- [ ] Test team search functionality (Lakers, Falcons, Yankees)
- [ ] Verify save/remove favorites works
- [ ] Check mobile responsive layout

### Git Setup

```bash
cd /Users/sajisaravanan/all-sports

# Remove API key from any history
grep -r "GNEWS_API_KEY" --exclude-dir=.git

# Check git status
git status

# Verify only source code files are staged
git log --oneline | head -5
```

### Push to GitHub

```bash
# Stage all changes
git add .
git commit -m "Final: All Sports news aggregator for MLH Fellowship"

# Push to GitHub
git remote set-url origin https://github.com/YOUR_USERNAME/all-sports.git
git push -u origin main

# Verify it's public
# Visit: https://github.com/YOUR_USERNAME/all-sports
# Should show repository without "Private" label
```

---

## MLH Application Form - Code Sample Section

### Required Fields

**Repository URL:**
```
https://github.com/YOUR_USERNAME/all-sports
```

**Language:**
```
Python
```

**Description (2-3 sentences):**
```
All Sports is a full-stack sports news aggregator built with Flask that solves the real problem of mixed sports content in API results. It uses explicit professional-only queries, intelligent team-name expansion, and relevance filtering to ensure clean, specific results. The project demonstrates backend API integration, SQLite database design, responsive frontend development, and production deployment configuration.
```

**What problem does this solve?**
```
Users browsing sports news encounter mixed content—college football appears in NFL results, popular teams (like Lakers) dominate NBA results, and generic queries return irrelevant articles. All Sports solves this with sport-specific queries, team name expansion (Falcons → Atlanta Falcons NFL), and relevance scoring that prioritizes articles actually mentioning the searched content.
```

**What are you most proud of?**
```
The filter_relevant_articles() function and SPORT_QUERIES system. Instead of relying solely on the API for filtering, I implemented intelligent scoring that ranks articles by search term occurrence in title/description. Combined with explicit professional-only queries (NFL professional football vs just NFL), this nearly eliminates irrelevant results. It demonstrates understanding that API quality can be improved through thoughtful backend filtering.
```

---

## Interview Preparation

### Core Concepts to Prepare

**1. Architecture & Separation of Concerns**
- Explain the three-layer design: routing (app.py), API (news_api.py), database (database.py)
- Why this separation matters for testing and maintenance

**2. The Core Problem & Solution**
- Problem: Generic API queries return mixed sports content
- Solution: Explicit professional-only queries + relevance filtering
- Be ready to explain with specific examples (Lakers example)

**3. Key Functions to Deep-Dive**
- `find_best_query()` – How it converts shorthand to full team names
- `filter_relevant_articles()` – How it scores articles by relevance
- `save_favorite()` and `delete_favorite()` – Database operations

**4. Frontend Design**
- CSS variable system (show the palette)
- Responsive design approach (mobile-first or desktop-first)
- Accessibility considerations

**5. API Integration**
- NewsData.io endpoint and parameters
- Error handling (timeouts, missing keys, malformed responses)
- Why you chose this API over alternatives

### Expected Interview Questions

**"Walk me through the codebase."**
> "I've structured this with three clear layers. app.py handles Flask routes and business logic. It uses SPORT_QUERIES—a dictionary mapping sports to explicit professional-only queries—and the find_best_query() function to expand team names. news_api.py is isolated for API communication with error handling. database.py manages SQLite favorites with parameterized SQL. On the frontend, I have three Jinja templates with a modern dark theme CSS system. This keeps everything understandable without unnecessary abstraction."

**"What's the most interesting technical decision you made?"**
> "The relevance filtering function. I realized that even with good API queries, I'd still get false positives. So I implemented filter_relevant_articles() which scores each article by counting how many times the search term appears in the title or description. Articles are sorted by this score, ensuring the most relevant results appear first. This gives users the experience of sport-specific, team-specific content even when the API returns broader results."

**"Tell me about a bug or challenge you overcame."**
> "Initially, the Lakers were dominating NBA results because they're a popular team that appears in many articles. Simply searching 'NBA Lakers' didn't fix it because generic searches still returned too many irrelevant articles. I solved this by: 1) changing to explicit 'NBA professional basketball' queries to exclude college content, and 2) implementing the relevance scoring function to prioritize articles that actually mention 'Lakers' prominently."

**"How would you scale this?"**
> "For 1000+ daily users, I'd migrate from SQLite to PostgreSQL since SQLite doesn't handle concurrent writes well. I'd add user accounts to store personalized team preferences. I'd implement Redis caching for frequently-requested teams to reduce API calls. I'd add pagination to handle large result sets. For the UI, I might add filters or sorting options. The current Flask architecture scales fine with these additions."

**"What would you do differently if you rebuilt it?"**
> "I'd start by adding more comprehensive error handling—the app currently handles API failures gracefully, but I'd add retry logic with exponential backoff. I'd add unit tests from the beginning rather than only manual testing. I'd implement more analytics to understand which sports/teams users search for most. I'd also consider breaking out more logic into helper modules to make testing easier."

**"Tell me about the CSS design system."**
> "I used CSS variables for consistency and maintainability. I have 40+ variables covering colors, spacing, and effects. For example, --bg-primary is the darkest background (#070B14), --accent-primary is cyan (#38BDF8). Sport-specific variables like --sport-nfl, --sport-nba allow for visual coding. The responsive breakpoints are mobile-first: 1 column on mobile, 2 on tablet, 3 on desktop. I also respect prefers-reduced-motion for accessibility."

**"Why Flask instead of Django?"**
> "Flask is lightweight and lets the code be the star. With Django, there's so much framework boilerplate that it obscures what the developer actually wrote. Flask lets me show the full stack—routing, business logic, database, frontend—in a way that's immediately understandable. It's also more commonly used in production for focused applications like this."

**"What's the deployment process?"**
> "The app is configured for Gunicorn as the WSGI server. I've provided a DEPLOYMENT.md guide for Render.com. You set environment variables (GNEWS_API_KEY), point to this GitHub repo, set build command to 'pip install -r requirements.txt', and start command to 'gunicorn -w 4 -b 0.0.0.0:5000 app:app'. Render handles the rest—auto-deploys on every push to main."

---

## Technical Elevator Pitch (30 seconds)

```
"All Sports is a Flask-based sports news aggregator I built to solve a real problem: 
generic news APIs return mixed content—college football in NFL results, popular teams 
dominating results. 

I solved this with three key features: explicit professional-only queries for each sport, 
a function that expands team names with sport context (Falcons → Atlanta Falcons NFL), 
and a relevance-scoring filter that ranks articles by search term occurrence.

The backend has clean separation of concerns—routing, API, and database in separate files. 
The frontend is a modern dark theme using CSS variables for consistency. The whole thing 
is configured for production deployment with Gunicorn and Render."
```

---

## File Structure for Interview Discussion

When they ask "show me the key files," refer them to:

1. **Backend Logic:** [app.py](app.py) (lines 1-50 for SPORT_QUERIES)
2. **Smart Search:** [app.py](app.py) (lines 60-80 for find_best_query)
3. **Filtering:** [app.py](app.py) (lines 85-110 for filter_relevant_articles)
4. **API Integration:** [news_api.py](news_api.py) (complete file, ~80 lines)
5. **Database:** [database.py](database.py) (complete file, ~60 lines)
6. **Frontend Design:** [static/style.css](static/style.css) (CSS variables at top)

---

## Common Pitfalls to Avoid

❌ **"I used X framework/library, so most of the work was boilerplate"**  
✅ Instead: Explain what YOU added on top of Flask/HTML/CSS

❌ **"I followed a tutorial"**  
✅ Instead: Explain how your implementation differs from standard patterns

❌ **"I don't remember why I made that decision"**  
✅ Instead: Think through and be ready to explain all major choices

❌ **"The code is too complex to explain in an interview"**  
✅ This is a sign your sample might not be interview-friendly; this project is simple enough to explain clearly

---

## MLH Tracks & Positioning

### Best Fit: Backend/SRE Track

This project demonstrates:
- ✅ Backend API design (SPORT_QUERIES, route handlers)
- ✅ Database design (schema, constraints, SQL)
- ✅ External API integration (error handling, timeouts)
- ✅ Production deployment (Gunicorn configuration)
- ✅ Code organization (separation of concerns)

### Bonus: Full-Stack Capabilities

While primarily backend-focused, you also show:
- ✅ Modern frontend with CSS variables and responsive design
- ✅ HTML/CSS/JS competency
- ✅ Server-rendered web application (Jinja2 templates)

---

## After Submission

### If Interviewed

**Before the interview:**
- Have the repository URL ready
- Deploy to Render so they can see it live (optional but impressive)
- Open the code in your editor—be ready to share screen
- Have talking points prepared for each major function

**During the interview:**
- Be comfortable explaining line-by-line code
- Be honest about tradeoffs and limitations
- Ask clarifying questions about what they want to know
- Show enthusiasm for the problem the code solves

### Success Indicators

During the interview, they'll be assessing:
- ✅ Can you explain your own code?
- ✅ Do you understand design decisions?
- ✅ Can you talk about tradeoffs?
- ✅ How would you improve it?
- ✅ Do you know the tools/libraries you used?

---

## Quick Reference

| Item | Location |
|------|----------|
| Code Sample | https://github.com/YOUR_USERNAME/all-sports |
| README | [README.md](README.md) (comprehensive project overview) |
| Architecture | [CONTRIBUTIONS.md](CONTRIBUTIONS.md) (detailed breakdown) |
| Deployment | [DEPLOYMENT.md](DEPLOYMENT.md) (Render guide) |
| Main Logic | [app.py](app.py) (250+ lines) |
| Tests | Manual testing (all features verified) |

---

## Final Checklist Before Submitting

- [ ] Repository is public on GitHub
- [ ] README clearly explains the project
- [ ] `.env` is NOT in repository (check .gitignore)
- [ ] `requirements.txt` lists all dependencies
- [ ] Code has no obvious errors (tested locally)
- [ ] Commit history is clean (ideally < 20 commits)
- [ ] You can explain every major function
- [ ] You're ready to discuss architectural decisions
- [ ] Deployment guide is included
- [ ] Sample data doesn't contain personal information

---

Good luck with your MLH Fellowship application! This code sample clearly demonstrates your abilities and will give interviewers plenty to discuss.

