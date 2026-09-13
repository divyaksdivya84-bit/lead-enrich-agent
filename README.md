# Lead Enrichment Agent - SoftwareBrio Assignment

Python agent that takes company domains and enriches them using scraping + Groq LLM.

### Architecture (matches assignment requirements)
- **Step 1 Scraping**: Fetches homepage + /about, /team, /company, /contact, /pricing. Uses requests with Playwright fallback for JS sites. Handles 404, 403 bot blocker, timeouts gracefully.
- **Step 2 Token Opt**: Strips script, style, nav, footer, svg to save tokens. Extracts clean text only.
- **Step 3 LLM**: Uses Groq `openai/gpt-oss-20b` with Pydantic structured output (EnrichedLead model) to extract company_overview, ICP, contact_points, leadership, confidence score.
- **Step 4 Resilience**: Try/except for each domain, never crashes mid-run.
- **Bonus Cost Tracking**: Logs tokens and estimated cost per domain.

### Setup
1. pip install -r requirements.txt
2. playwright install
3. Create.env file: GROQ_API_KEY=your_key_here
4. python main.py
5. Check sample_output.json

Tested on: postman.com, supabase.com, vapi.ai
Author: Divya K S - Final year ECE student
