import os, re, json, requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from openai import OpenAI
# from playwright.sync_api import sync_playwright # for JS sites, installed

load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

# Step 3: Pydantic structured output
class Leader(BaseModel):
    name: str
    role: Optional[str] = None
    linkedin_url: Optional[str] = None

class Lead(BaseModel):
    domain: str
    company_overview: str
    target_audience_icp: str
    contact_points: List[str]
    key_leadership: List[Leader]
    data_confidence_score: float
    status: str = "enriched"

def clean(html):
    # Step 2: Remove scripts, nav, footer to save tokens
    soup = BeautifulSoup(html, 'html.parser')
    for t in soup(['script','style','nav','footer','svg']):
        t.decompose()
    return re.sub(r'\s+', ' ', soup.get_text())[:5000]

def scrape(domain):
    # Step 1: Fetch homepage + about, team, contact, pricing
    text = ""
    for path in ["", "/about", "/team", "/contact", "/pricing"]:
        try:
            url = f"https://{domain}{path}"
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code in [404, 403]:
                continue # Step 4: Handle 404, bot blocker
            text += clean(r.text) + " "
        except:
            continue # Step 4: Never crash if one fails
    return text

def enrich(domain):
    print(f"Enriching {domain}...")
    site_text = scrape(domain)
    emails = list(set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', site_text)))[:2]

    prompt = f"From
