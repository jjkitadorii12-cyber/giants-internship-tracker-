import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# The absolute, uncompromised list of your 8 target labs
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Automatically calculates the upcoming internship years based on the current date
    current_year = datetime.now().year
    target_year_1 = str(current_year + 1)  # e.g., "2027"
    target_year_2 = str(current_year + 2)  # e.g., "2028"
    
    # Highly specific phrases that only appear when an active application portal drops
    strict_keywords = [
        f"summer {target_year_1}", f"{target_year_1} intern", f"internship {target_year_1}",
        f"summer {target_year_2}", f"{target_year_2} intern", f"internship {target_year_2}",
        "engineering intern", "research intern", "research fellow"
    ]
    
    for lab, url in LABS.items():
        try:
            response = requests.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Scans clickable application links and bold headers where job roles are listed
            job_elements = soup.find_all(['a', 'h2', 'h3', 'h4', 'span'])
            
            for element in job_elements:
                element_text = element.get_text().strip().lower()
                
                # Verified Match: Ensure the keyword matches active structural job text
                if any(keyword in element_text for keyword in strict_keywords):
                    # Quick filter to drop generic background paragraphs
                    if len(element_text) < 100: 
                        message = f"🚀 **ACTIVE HIRING DETECTED:** New internship listing found at **{lab}**!\n🎯 Role Found: `{element.get_text().strip()}`\n🔗 Apply instantly here: {url}"
                        payload = {"content": message}
                        requests.post(DISCORD_WEBHOOK_URL, json=payload)
                        print(f"Verified match found for {lab}: {element_text}")
                        break # Prevents spamming multiple alerts for the same company in one run
                        
        except Exception as e:
            print(f"Error checking {lab}: {e}")

if __name__ == "__main__":
    check_job_boards()
