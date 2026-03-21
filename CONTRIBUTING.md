# Contributing to AI Web Content Analyzer

## Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend)
- pip

### Backend Setup
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

# Run the application
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev    # Development server
npm run build  # Build for production
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_seo_analyzer.py -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Lint check
flake8 app/ tests/ --max-line-length=120
```

## Project Structure

```
ai-web-content-analyzer/
├── app/                    # Flask application
│   ├── __init__.py         # App factory
│   ├── config.py           # Configuration
│   ├── models.py           # SQLAlchemy models
│   ├── routes/             # API endpoints
│   │   ├── analysis.py     # Analysis pipeline
│   │   └── history.py      # History & search
│   ├── services/           # Business logic
│   │   ├── scraper.py      # Web scraping
│   │   ├── seo_analyzer.py # SEO checks
│   │   ├── content_analyzer.py  # Readability
│   │   ├── ai_analyzer.py  # GPT-4 integration
│   │   └── report_generator.py  # PDF/JSON export
│   ├── static/react/       # Built React app
│   └── templates/          # HTML templates
├── frontend/               # React + Vite SPA
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   └── services/       # API client
│   └── package.json
├── tests/                  # Test suite
│   ├── conftest.py         # Fixtures
│   ├── test_models.py      # Model tests
│   ├── test_routes.py      # API route tests
│   ├── test_scraper.py     # Scraper tests
│   ├── test_seo_analyzer.py    # SEO tests
│   └── test_content_analyzer.py # Content tests
├── .github/workflows/      # CI/CD
│   └── ci.yml              # GitHub Actions
├── requirements.txt
└── run.py                  # Entry point
```

## Code Style

- Follow PEP 8 for Python code
- Max line length: 120 characters
- Use docstrings for all public methods
- Write tests for all new features
