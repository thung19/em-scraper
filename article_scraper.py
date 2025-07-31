import requests
from bs4 import BeautifulSoup
import time
from typing import List
from requests_html import HTMLSession
import re
from urllib.parse import urljoin, urlparse

class ArticleScraper:

    def __init__(self, home_urls, headers=None):
        self.home_urls = home_urls

        #Creates HTML object
        self.session = HTMLSession()

        #Sets header to appear as regular 
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        #Used to match and search for standard URL formatting
        self.regex_patterns = [r"^/[\d]{4}/[\d]{2}/[\d]{2}/[a-z0-9-]+(/[a-z0-9-]+)*$",
                               r"^/[\d]{4}/[\d]{2}/[\d]{2}/[a-z0-9/-]+$",
                               r"^/[\d]{4}/[\d]{2}/[\d]{2}/[a-z]+(?:/[a-z]+)*/[a-z0-9-]+$",
                               r"/\d{4}/\d{2}/\d{2}/",
                               r"\b\d{8}\b"
                            ]
        
        self.home_keywords = ["news", "aritcle","articles", "stories", "story"]

        self.em_keywords = ["FEMA", "NJEMA", "earthquake", "storm", "flood", "shooting", "bomb", "hospital", "disaster", "Federal Emergency Management Agency"]
        
        #Container Names
        self.possible_classes = ["articleBody", "ArticleBody", "article-body", "article-content",
            "article__content", "story-body", "entry-content"]

    def get_article_links(self):
        article_links = set()

        for url in self.home_urls:
            try:

                print("Trying")
                homepage = self.session.get(url, headers=self.headers)
                print("Got homepage. Rendering")

                homepage.html.render(timeout=10)

                print("Rendered")

                soup = BeautifulSoup(homepage.html.html, "lxml")


                #Loops through <a> tags that have href attribute
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    
                    
                    #Joins together the parsed url with the main url
                    full_url = urljoin(url,href)
                    
                    print(full_url)


                    #Separates url into main part and then suburl
                    path = urlparse(full_url).path

                    if (any(re.match(pattern, path) for pattern in self.regex_patterns)) and any(keyword.lower() in path.lower() for keyword in self.em_keywords):
                        article_links.add(full_url)
                    elif (any (keyword in path.lower() for keyword in self.home_keywords))and  any(keyword.lower() in path.lower() for keyword in self.em_keywords):
                        article_links.add(full_url)


            except Exception as e: 
                print(f"Error during homepage scraping: {e}")
        return article_links



         
    def get_content(self, url):
        try:
            response = self.session.get(url, headers=self.headers)

            #Try to render javascript for at least 20secs
            response.html.render(timeout=20)  

            #print(response.html.html[:1000])  #prints first 1000 chars

            soup = BeautifulSoup(response.html.html, 'lxml')

            #print(soup)

            #Finds instance of "h1" in html
            title_tag = soup.find("h1")

            #Take contents within tag and strip it if a tag was found, if not set title to ""
            title = title_tag.text.strip() if title_tag else ""

            body = None
            #Check to see if there is a container with the names in possible_classes
            for cls in self.possible_classes:
            #Find mathing "div" element (disregard case)
            
                body = soup.find("div", class_=re.compile(cls, re.IGNORECASE))
                if body:
                    break
                #Find all paragraphs if right "div" element was found
            if body:
                paragraphs = body.find_all("p")
            else:
                # Fallback: get all <p> tags inside <article>, then fallback to all <p>
                article = soup.find('article')
                paragraphs = article.find_all("p") if article else soup.find_all("p")
                #Join paragraphs only if the "p" elements contain text and are not empty
                content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            return title, content
        except Exception:
            return None, None
           