import os, requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Groq uses OpenAI format
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def scrape(domain):
    print(f"Scraping {domain}...")
    urls = [f"https://{domain}", f"https://{domain}/about", f"https://{domain}/about-us"]
    text = ""
    for url in urls:
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
            soup = BeautifulSoup(r.text, 'html.parser')
            for tag in soup(['script','style','nav','footer']):
                tag.decompose()
            text += soup.get_text(separator=' ')[:4000] + "\n"
        except:
            continue
    return text[:8000]

def enrich(domain):
    website_text = scrape(domain)
    if not website_text.strip():
        return "Could not scrape website."

    prompt = f"""You are a lead enrichment expert. From this website text, extract:
1. What the company does (1 sentence)
2. Industry
3. Ideal customer
4. 3 pain points they solve

Website text from {domain}:
{website_text}

Give answer in clean bullet points."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    domain = input("Enter domain (like postman.com): ").strip()
    result = enrich(domain)
    print("\n--- ENRICHED LEAD ---\n")
    print(result)
