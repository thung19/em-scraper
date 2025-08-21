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
                    '''
                    if (any(re.match(pattern, path) for pattern in REGEX_PATTERNS)) and \
                       any(keyword.lower() in path.lower() for keyword in EM_KEYWORDS):
                        article_links.add(full_url)

                    elif any(keyword in path.lower() for keyword in HOME_KEYWORDS) and \
                         any(keyword.lower() in path.lower() for keyword in EM_KEYWORDS):
                        article_links.add(full_url)
                    '''
                    article_links.add(full_url)
                        

                    '''
                    if (any(re.match(pattern, path) for pattern in REGEX_PATTERNS)):
                        article_links.add(full_url)

                    elif any(keyword in path.lower() for keyword in HOME_KEYWORDS):
                        article_links.add(full_url)
                    '''
                #print(article_links) #for debugging

                print("Links retrieved")
            except Exception as e:
                print(f"Error during homepage scraping from {url}: {e}")
        return article_links
    

    def get_content(self, urls):
        results = []
        ha24 = datetime.now(timezone.utc) - timedelta(days=1)

        #Loops through collected page urls and gets html
        for url in urls:
            soup = self.fetch_html(url)
            #If unable to get html, move on to next article
            if not soup:
                print("Skipping... Unable to retrieve URL")
                continue
            
            #Gets date
            date = self.extract_date(soup)
            #Go to next url if collected date is not of datetime object or is older than 24 hrs
            if not isinstance(date, datetime):
                print("Skipping... unable to get valid date object")
                continue

            if date <ha24:
                print("Skipping... article older than 24 hours")
                continue
            
            #Collects Article Title from html
            title = self.extract_title(soup)
            #Skips article if it does not contain keywords related to emergency management
            
            if not any(keyword.lower() in title.lower() for keyword in EM_KEYWORDS):
                print("Skipping... Title not relevant")
                continue
            
            
            #Collects actual content of article from html
            content = self.extract_content(soup)

            #If no content is retrieved, go to next article
            if not content.strip():
                print("Skipping... content is empty.")
                continue
            
            #If  content is less than 100 chars, go to next article
            if len(content) < 100:
                print("Skipping... content is too little")
                continue
            
            #Create dictionary containing article attributes
            new_article = {"url": url, "title": title, "date": date, "content": content}

            #Filters out articles that are different but cover similar story
            self.deduplicate(results, new_article)

        return results

    #Gets article html
    def fetch_html(self, url):
        #Tries to get article html
        try:
            response = self.session.get(url, headers=HEADERS, timeout=20)
            response.raise_for_status()
            #Parses html
            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            print(f"Failed to fetch HTML from {url}: {e}")
            return None

    #Gets article publication date
    def extract_date(self, soup):
        #Loops through common date attributes and finds the meta tag that matches one of those attributes
        try:
            for attrs in DATE_ATTRS:
                meta_date = soup.find("meta", attrs=attrs)
                #Returns if tag has a content field
                if meta_date and meta_date.get("content"):
                    return self.parse_date(meta_date["content"])
        except Exception as e:
            print(f"Date parsing error: {e}")

        try:
            #Searches for a time tag and gets content
            time_tag = soup.find("time", attrs={"datetime": True})
            if time_tag and time_tag.get("datetime"):
                return self.parse_date(time_tag["datetime"])
        except Exception as e:
            print(f"time fallback failed: {e}")

        return None

      
    #Converts HTML date string into python datetime object
    def parse_date(self, date_str):
        try:
            #Finds strings that end with Z and converts to understandable format
            if date_str.endswith("Z"):
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            else:
                dt = datetime.fromisoformat(date_str)
            #Ensure datetime object has timezone
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except Exception as e:
            print(f"Date parsing failed for {date_str}: {e}")
            return None

    #Gets title of article
    def extract_title(self, soup):
        #Finds h1 tag and returns content within
        try:
            h1 = soup.find("h1")
            if h1 and h1.get_text(strip=True):
                return h1.get_text(strip=True)
            
            og_title = soup.find("meta", property="og:title")
            if og_title and og_title.get("content"):
                return og_title["content"].strip()
            
        except Exception as e:
            print(f"Title parsing failed: {e}")
            return ""

    def extract_content(self, soup):
        try:
            body = None
            #Loops through common class name patterns and searches for a div tag that has a class that matches
            for cls in POSSIBLE_CLASSES:
                body = soup.find("div", class_=re.compile(cls, re.IGNORECASE))
                if body:
                    break
            
            #If no div tag is found, looks for first non-empty p tag and assumes it to be article body
            if not body:
                for div in soup.find_all("div"):
                    ps = div.find_all("p")
                    if len([p for p in ps if p.get_text(strip=True)]) >= 1:
                        body = div
                        break

            #Extracts p tags if valid body elements were found              
            if body:
                paragraphs = body.find_all("p")
            else:
                article = soup.find("article")
                paragraphs = article.find_all("p") if article else soup.find_all("p")

            content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            #If nothing is found, try to use common og description as article body
            if not content.strip():
                og_desc = soup.find("meta", property="og:description")
                if og_desc and og_desc.get("content"):
                    print("Used og:description as fallback content.")
                    content = og_desc["content"].strip()

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



    #Uses Spacy natural language processing to determine similarity of two article titles
    def calc_sim_titles (self, title1, title2, threshold=0.75):
        w1 = self.nlp(title1)
        w2 = self.nlp(title2)
        similarity = w1.similarity(w2)
        return similarity >= threshold
    
    #Prints article results
    def print_results(self, results):
        print("")
        print("Article Results")
        for article in results:
            print(article["title"])
            print(article["date"])
            print(article["url"])
            print(article["content"])
            print("\n" + "="*80 + "\n")  
        
    


           