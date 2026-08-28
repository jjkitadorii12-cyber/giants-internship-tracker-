import os
import requests
from bs4 import BeautifulSoup

# The exact URLs for your curated list of labs
LABS = {
    "OpenAI Emerging Talent": "https://openai.com",
    "Anthropic Careers": "https://www.anthropic.com/careers",
    "Google DeepMind": "https://deepmind.google",
    "Meta University Recruiting": "https://metacareers.com",
    "xAI Careers": "https://x.ai",
    "Scale AI University": "https://scale.com",
    "Microsoft Research India": "https://microsoft.com",
    "Google India Careers": "https://google.com"
}

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def check_job_boards():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for lab, url in LABS.items():
        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text().lower()
            
            # Smart keywords targeting the Summer 2028 cycle
            if "intern" in page_text or "2028" in page_text or "fellow" in page_text:
                message = f"🚨 **ALERT:** Potential Summer 2028/Intern opening detected at **{lab}**!\n🔗 Check immediate listings here: {url}"
                payload = {"content": message}
                requests.post(DISCORD_WEBHOOK_URL, json=payload)
                print(f"Match found for {lab}!")
        except Exception as e:
            print(f"Error checking {lab}: {e}")

if __name__ == "__main__":
    check_job_boards()
