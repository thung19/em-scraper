from article_scraper import ArticleScraper
from config import ALL_URLS, BS4_URLS, NATIONAL_URLS
from article_summarizer import summarize
from emailer import build_body, send_email

def main():
    
    urls = ["https://www.cnn.com/us"]
    scraper = ArticleScraper(urls)
    article_links = scraper.get_article_links_req()
    #print(article_links)
    
    results = scraper.get_content(article_links)

    
    send_email(build_body(results))

    print("FINISHED")
    

if __name__ == "__main__":
    main()