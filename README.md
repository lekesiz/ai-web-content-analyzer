# AI Web Content Analyzer

A web-based system that analyzes website content and provides insights on SEO quality, readability, and content structure with AI-powered recommendations.

Developed as part of **UE 6.5 -- Projet Tutoure (Licence Professionnelle LPDWCA)** at **Universite de Strasbourg**.

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
| Backend | Python / Flask |
| Database | SQLite / SQLAlchemy |
| Scraping | BeautifulSoup4 / Requests |
| AI | OpenAI GPT-4 (optional) |
| Frontend | HTML / CSS / JavaScript |
| Styling | Tailwind CSS (CDN) |
| Charts | Chart.js |
| PDF Export | fpdf2 |

---

## Installation

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/lekesiz/ai-web-content-analyzer.git
cd ai-web-content-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# (Optional) Add your OpenAI API key to .env
# OPENAI_API_KEY=sk-your-key-here

# Initialize database and run
python run.py
```

The application will be available at `http://127.0.0.1:5000`

---

## Usage

1. **Enter a URL** on the home page
2. **Wait for analysis** (typically 2-5 seconds)
3. **View results** including scores, SEO details, and issues
4. **Export** results as JSON or PDF
5. **Browse history** of past analyses

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Home page |
| GET | `/about` | About the project |
| GET | `/history` | Analysis history page |
| GET | `/results/<id>` | Results dashboard |
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
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── models.py            # Database models
│   ├── routes/
│   │   ├── main.py          # Home, About pages
│   │   ├── analysis.py      # Analysis API
│   │   └── history.py       # History pages & API
│   ├── services/
│   │   ├── scraper.py       # Web scraping engine
│   │   ├── seo_analyzer.py  # SEO analysis (10+ checks)
│   │   ├── content_analyzer.py  # Readability analysis
│   │   ├── ai_analyzer.py   # OpenAI GPT integration
│   │   └── report_generator.py  # PDF/JSON export
│   ├── static/js/           # Frontend JavaScript
│   └── templates/           # HTML templates
├── tests/                   # Test suite
├── requirements.txt
├── run.py                   # Entry point
└── .env.example
```

---

## Methodology

1. **Web Scraping**: Fetch and parse HTML using BeautifulSoup4
2. **SEO Analysis**: Check title, meta, headings, images, links, keywords (10+ checks with weighted scoring)
3. **Content Analysis**: Calculate readability scores, detect language, evaluate structure
4. **AI Analysis**: Generate recommendations using OpenAI GPT-4 (optional)
5. **Scoring**: Compute weighted overall score and save to SQLite database
6. **Presentation**: Display results with charts and export options

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

# Lint check
flake8 app/ tests/
```

---

## Author

**Mikail Lekesiz**
Licence Professionnelle -- LPDWCA
Universite de Strasbourg

---

## License

MIT
