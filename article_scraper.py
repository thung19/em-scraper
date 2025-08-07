from datetime import datetime, timezone, timedelta
import requests
from bs4 import BeautifulSoup
import time
from typing import List
from requests_html import HTMLSession
import re
from urllib.parse import urljoin, urlparse
import spacy
from config import HEADERS, REGEX_PATTERNS, HOME_KEYWORDS, EM_KEYWORDS, POSSIBLE_CLASSES, DATE_ATTRS

class ArticleScraper:
    

    def __init__(self, home_urls, headers=None):
        self.home_urls = home_urls

        self.session = HTMLSession()

        #Sets header to appear as regular 
        self.headers  = HEADERS

        self.nlp = spacy.load("en_core_web_lg")

    def get_article_links_req(self):
        article_links = set()
        

        for url in self.home_urls:
            try:
                print("Trying", url)

                #Makes a request to the URL. Waits 10 seconds max.
                response = self.session.get(url, headers=self.headers, timeout=10)

                #Checks response proceeds if it is valid
                response.raise_for_status()

                #Create BeautifulSoup object with the html and allows parsing
                soup = BeautifulSoup(response.text, "lxml")
                print("Got homepage. Parsing links...")

                #Finds all urls in the html of the webpage. Looks for <a> tags and finds html that contain href attribute
                for a in soup.find_all("a", href=True):
                    href = a["href"]

                    #Combines url with base url if needed
                    full_url = urljoin(url, href)

                    #gets relative link
                    path = urlparse(full_url).path
                    
                    #print(full_url) #For testing
                    #print(path) #For testing

                    #Filters through all URLS and only adds ones that match with common article regex patterns and have a keyword related to emergency management
                    if (any(re.match(pattern, path) for pattern in REGEX_PATTERNS)) and \
                       any(keyword.lower() in path.lower() for keyword in EM_KEYWORDS):
                        article_links.add(full_url)

                    elif any(keyword in path.lower() for keyword in HOME_KEYWORDS) and \
                         any(keyword.lower() in path.lower() for keyword in EM_KEYWORDS):
                        article_links.add(full_url)
                    
                    '''
                    if (any(re.match(pattern, path) for pattern in REGEX_PATTERNS)):
                        article_links.add(full_url)

                    elif any(keyword in path.lower() for keyword in HOME_KEYWORDS):
                        article_links.add(full_url)
                    '''
                print(article_links)
                print("Links retrieved")
            except Exception as e:
                print(f"Error during homepage scraping from {url}: {e}")
        return article_links
    

    def get_content(self, urls):
        results = []
        ha24 = datetime.now(timezone.utc) - timedelta(days=1)

        for url in urls:
            soup = self.fetch_html(url)
            if not soup:
                continue

            date = self.extract_date(soup)
            if not isinstance(date, datetime) or date < ha24:
                print("Skipping... invalid or too old date.")
                continue

            title = self.extract_title(soup)
            content = self.extract_content(soup)

            if not content.strip():
                print("Skipping... content is empty.")
                continue

            new_article = {"url": url, "title": title, "date": date, "content": content}
            self.deduplicate(results, new_article)

        return results

    def fetch_html(self, url):
        try:
            response = self.session.get(url, headers=HEADERS, timeout=20)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            print(f"Failed to fetch HTML from {url}: {e}")
            return None

    def extract_date(self, soup):
        try:
            for attrs in DATE_ATTRS:
                meta_date = soup.find("meta", attrs=attrs)
                if meta_date and meta_date.get("content"):
                    return self.parse_date(meta_date["content"])
        except Exception as e:
            print(f"Date parsing error: {e}")

        try:
            time_tag = soup.find("time", attrs={"datetime": True})
            if time_tag:
                return self.parse_date(time_tag["datetime"])
        except Exception as e:
            print(f"time fallback failed: {e}")

        return None

    def parse_date(self, date_str):
        try:
            if date_str.endswith("Z"):
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            else:
                dt = datetime.fromisoformat(date_str)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except Exception as e:
            print(f"Date parsing failed for {date_str}: {e}")
            return None

    def extract_title(self, soup):
        try:
            title_tag = soup.find("h1")
            return title_tag.text.strip() if title_tag else ""
        except Exception as e:
            print(f"Title parsing failed: {e}")
            return ""

    def extract_content(self, soup):
        try:
            body = None
            for cls in POSSIBLE_CLASSES:
                body = soup.find("div", class_=re.compile(cls, re.IGNORECASE))
                if body:
                    break

            if not body:
                for div in soup.find_all("div"):
                    ps = div.find_all("p")
                    if len([p for p in ps if p.get_text(strip=True)]) >= 1:
                        body = div
                        break

            if body:
                paragraphs = body.find_all("p")
            else:
                article = soup.find("article")
                paragraphs = article.find_all("p") if article else soup.find_all("p")

            content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            if not content.strip():
                og_desc = soup.find("meta", property="og:description")
                if og_desc and og_desc.get("content"):
                    print("Used og:description as fallback content.")
                    return og_desc["content"].strip()

            return content
        except Exception as e:
            print(f"Content extraction failed: {e}")
            return ""

    def deduplicate(self, results, new_article):
        for i, existing_article in enumerate(results):
            if self.calc_sim_titles(new_article["title"], existing_article["title"]):
                if len(new_article["content"]) > len(existing_article["content"]):
                    results[i] = new_article
                return
        results.append(new_article)



    
    def calc_sim_titles (self, title1, title2, threshold=0.75):
        w1 = self.nlp(title1)
        w2 = self.nlp(title2)
        similarity = w1.similarity(w2)
        return similarity >= threshold
    
    def print_results(self, results):
        for article in results:
            print(article["title"])
            print(article["date"])
            print(article["url"])
            print(article["content"])
            print("\n" + "="*80 + "\n")  
        
    


           