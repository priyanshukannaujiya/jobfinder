import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LinkedInSpider:
    def __init__(self, keywords=None):
        self.keywords = keywords or ['Data Engineer', 'Data Analyst']
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def scrape(self):
        jobs = []
        # LinkedIn public job search URL pattern
        for keyword in self.keywords:
            search_query = keyword.replace(' ', '%20')
            url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location=Worldwide&f_TPR=r86400&position=1&pageNum=0"
            logger.info(f"Scraping LinkedIn URL: {url}")
            
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code != 200:
                    logger.warning(f"Failed to fetch {url}. Status in LinkedIn is likely blocked (429/999). Status Code: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='base-card')
                
                for card in job_cards:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    location_elem = card.find('span', class_='job-search-card__location')
                    link_elem = card.find('a', class_='base-card__full-link')
                    time_elem = card.find('time')
                    
                    job_title = title_elem.text.strip() if title_elem else 'Unknown'
                    company = company_elem.text.strip() if company_elem else 'Unknown'
                    location = location_elem.text.strip() if location_elem else 'Worldwide'
                    link = link_elem['href'].split('?')[0] if link_elem and 'href' in link_elem.attrs else ''
                    
                    date_posted = None
                    if time_elem and 'datetime' in time_elem.attrs:
                        try:
                            date_posted = datetime.strptime(time_elem['datetime'], '%Y-%m-%d')
                        except:
                            pass
                            
                    if not link:
                        continue
                        
                    jobs.append({
                        'job_title': job_title,
                        'company': company,
                        'location': location,
                        'skills': keyword,
                        'experience_level': 'Entry Level', # Assume Entry level for generic searches unless parsed
                        'description': 'See LinkedIn posting for details.',
                        'link': link,
                        'posting_date': date_posted or datetime.utcnow(),
                        'source': 'LinkedIn'
                    })
            except Exception as e:
                logger.error(f"Error scraping LinkedIn for {keyword}: {e}")
                
        return jobs
