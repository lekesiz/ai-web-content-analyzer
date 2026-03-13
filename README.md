# AI Web Content Analyzer

A web-based system that analyzes website content and provides insights on SEO quality, readability, and content structure with AI-powered recommendations.

Developed as part of **UE 6.5 -- Projet Tutore (Licence Professionnelle LPDWCA)** at **Universite de Strasbourg**.

---

## Features

- **SEO Analysis**: Title tags, meta descriptions, heading hierarchy, image alt texts, link analysis, keyword density, Open Graph tags, canonical URLs
- **Content Analysis**: Readability scores (Flesch, Gunning Fog, Coleman-Liau), language detection, vocabulary richness, content structure quality
- **AI Recommendations**: GPT-4 powered suggestions for SEO optimization and content improvement (optional, requires OpenAI API key)
- **Scoring System**: Overall score (0-100) with weighted sub-scores for SEO (40%), Content (30%), Technical (20%), AI (10%)
- **Export**: Download results as JSON or PDF reports
- **History**: Browse, search, and compare past analyses

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | **React 19** (Vite build tool) |
| Backend | Python / Flask |
| Database | SQLite / SQLAlchemy |
| Scraping | BeautifulSoup4 / Requests |
| AI | OpenAI GPT-4 (optional) |
| Styling | Tailwind CSS (CDN) |
| Charts | Chart.js / react-chartjs-2 |
| Routing | React Router v7 |
| PDF Export | fpdf2 |

---

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### Setup

```bash
# Clone the repository
git clone https://github.com/lekesiz/ai-web-content-analyzer.git
cd ai-web-content-analyzer

# --- Backend Setup ---
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# (Optional) Add your OpenAI API key to .env
# OPENAI_API_KEY=sk-your-key-here

# --- Frontend Setup ---
cd frontend
npm install
npm run build
cd ..

# --- Run ---
python run.py
```

The application will be available at `http://127.0.0.1:5000`

### Development Mode

For frontend development with hot reload:

```bash
# Terminal 1: Start Flask backend
python run.py

# Terminal 2: Start Vite dev server
cd frontend
npm run dev
```

The Vite dev server runs on `http://localhost:3000` and proxies API requests to Flask.

---

## React Frontend Architecture

The frontend is built as a **Single Page Application (SPA)** using React with Vite.

### ES6 Features Used
- `const` / `let` with block scoping
- Template literals
- Arrow functions
- Destructuring (objects and arrays)
- Spread operator (`...`)
- ES6 modules (`import` / `export`)
- Async/await
- Classes (Chart.js integration)

### React Concepts Demonstrated
- **Functional Components** with JSX
- **useState** hook for state management
- **useEffect** hook for side effects and API calls
- **Props** for component communication
- **React Router** for client-side navigation
- **Conditional rendering** and list rendering with `map()`
- **Event handling** (forms, clicks)
- **Component composition** (Navbar, Footer, ScoreCard, etc.)

### Component Structure

```
frontend/src/
├── main.jsx              # Entry point (createRoot)
├── App.jsx               # Router setup
├── components/
│   ├── Navbar.jsx        # Navigation with active link highlighting
│   ├── Footer.jsx        # Footer with project info
│   ├── ScoreCard.jsx     # Score display with progress bar
│   ├── ScoreChart.jsx    # Doughnut chart (Chart.js)
│   ├── FeatureCard.jsx   # Feature card with icon/title/description
│   ├── LoadingSpinner.jsx # Reusable loading indicator
│   └── Notification.jsx  # Toast notification with auto-dismiss
├── pages/
│   ├── Home.jsx          # URL input form, recent analyses
│   ├── Results.jsx       # Full analysis results dashboard
│   ├── History.jsx       # Searchable/sortable analysis history
│   └── About.jsx         # Project information
└── services/
    └── api.js            # API service module (fetch wrapper)
```

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | React SPA (all frontend routes) |
| POST | `/api/analyze` | Run analysis (`{"url": "..."}`) |
| GET | `/api/analysis/<id>` | Get analysis results |
| DELETE | `/api/analysis/<id>` | Delete an analysis |
| GET | `/api/analysis/<id>/export/json` | Export as JSON |
| GET | `/api/analysis/<id>/export/pdf` | Export as PDF |
| GET | `/api/history` | Paginated history API |

---

## Project Structure

```
ai-web-content-analyzer/
├── frontend/                   # React SPA (Vite)
│   ├── src/
│   │   ├── main.jsx           # React entry point
│   │   ├── App.jsx            # Router & layout
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Page components
│   │   └── services/          # API service layer
│   ├── package.json
│   └── vite.config.js
├── app/                        # Flask backend
│   ├── __init__.py            # App factory + React serving
│   ├── config.py              # Configuration
│   ├── models.py              # Database models
│   ├── routes/
│   │   ├── analysis.py        # Analysis API
│   │   └── history.py         # History API
│   ├── services/
│   │   ├── scraper.py         # Web scraping engine
│   │   ├── seo_analyzer.py    # SEO analysis (10+ checks)
│   │   ├── content_analyzer.py # Readability analysis
│   │   ├── ai_analyzer.py     # OpenAI GPT integration
│   │   └── report_generator.py # PDF/JSON export
│   └── static/react/          # Built React app (generated)
├── tests/                      # Test suite
├── requirements.txt
├── run.py                      # Entry point
└── .env.example
```

---

## Methodology

1. **Web Scraping**: Fetch and parse HTML using BeautifulSoup4
2. **SEO Analysis**: Check title, meta, headings, images, links, keywords (10+ checks with weighted scoring)
3. **Content Analysis**: Calculate readability scores, detect language, evaluate structure
4. **AI Analysis**: Generate recommendations using OpenAI GPT-4 (optional)
5. **Scoring**: Compute weighted overall score and save to SQLite database
6. **Presentation**: React SPA displays results with Chart.js visualizations and export options

---

## Configuration

Environment variables (`.env` file):

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `OPENAI_API_KEY` | OpenAI API key (optional) | None |
| `FLASK_DEBUG` | Enable debug mode | `1` |

---

## Testing

```bash
# Run tests
pytest tests/ -v

# Lint check (backend)
flake8 app/ tests/

# Lint check (frontend)
cd frontend && npm run lint
```

---

## Author

**Mikail Lekesiz**
Licence Professionnelle -- LPDWCA
Universite de Strasbourg

---

## License

MIT
