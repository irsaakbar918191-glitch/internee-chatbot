import os
import requests
from bs4 import BeautifulSoup

def scrape_internee_data():
    url = "https://www.internee.pk/"
    output_dir = "knowledge_base"
    output_file = os.path.join(output_dir, "internee_website_scraped.txt")

    os.makedirs(output_dir, exist_ok=True)

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_data = []

            for elem in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
                text = elem.get_text(strip=True)
                if len(text) > 20:
                    text_data.append(text)

            content = "\n".join(text_data)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            print("Successfully updated internee.pk knowledge base!")
            return True
    except Exception as e:
        print(f"Scraping error: {e}")
        return False