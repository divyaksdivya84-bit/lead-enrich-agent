# Lead Enrichment Agent

AI agent that takes company domain and enriches it.

### What it does:
1. Scrapes company website (About page)
2. Uses Groq AI to extract: industry, size, value proposition, keywords
3. Returns clean JSON

### How to run:
pip install -r requirements.txt
python main.py

### Tech used:
- Python, BeautifulSoup, Groq (Llama 3)
