from article_scraper import ArticleScraper
from config import ALL_URLS, BS4_URLS, NATIONAL_URLS
from article_summarizer import summarize

def main():
    
    urls = NATIONAL_URLS
    scraper = ArticleScraper(urls)
    article_links = scraper.get_article_links_req()
    #print(article_links)
    
    results = scraper.get_content(article_links)
    scraper.print_results(results)
    
    summarize(results)

    print("FINISHED")
    

if __name__ == "__main__":
    main()