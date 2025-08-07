from article_scraper import ArticleScraper
from config import ALL_URLS, BS4_URLS, NATIONAL_URLS

def main():
    
    urls = NATIONAL_URLS
    scraper = ArticleScraper(urls)
    article_links = scraper.get_article_links_req()
    #print(article_links)
    
    results = scraper.get_content(article_links)
    scraper.print_results(results)
    print("FINISHED")
    

if __name__ == "__main__":
    main()