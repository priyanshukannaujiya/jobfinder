import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class InternshalaSpider:
    def __init__(self, keywords=None):
        self.base_url = "https://internshala.com/internships/"
        # We can append keywords for filtering: e.g., https://internshala.com/internships/data-engineer-internship/
        self.keywords = keywords or ['data-engineer', 'data-analyst', 'data-science']
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def scrape(self):
        jobs = []
        for keyword in self.keywords:
            url = f"{self.base_url}{keyword}-internship/"
            logger.info(f"Scraping Internshala URL: {url}")
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code != 200:
                    logger.warning(f"Failed to fetch {url}. Status: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='internship_meta')
                
                for card in job_cards:
                    title_elem = card.find('h3', class_='job-title-href')
                    company_elem = card.find('p', class_='company-name')
                    location_elem = card.find('a', class_='location_link')
                    link_elem = title_elem.find('a') if title_elem else None
                    
                    job_title = title_elem.text.strip() if title_elem else 'Unknown'
                    company = company_elem.text.strip() if company_elem else 'Unknown'
                    location = location_elem.text.strip() if location_elem else 'Remote'
                    link = f"https://internshala.com{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else ''
                    
                    if not link:
                        continue
                        
                    jobs.append({
                        'job_title': job_title,
                        'company': company,
                        'location': location,
                        'skills': keyword.replace('-', ' '), # Guessing skills based on keyword
                        'experience_level': 'Internship',
                        'description': 'Description can be viewed on Internshala',
                        'link': link,
                        'posting_date': datetime.utcnow(),
                        'source': 'Internshala'
                    })
            except Exception as e:
                logger.error(f"Error scraping {keyword}: {e}")
                
        return jobs
