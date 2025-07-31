from article_scraper import ArticleScraper

def main():
    urls = ["https://www.cnn.com", "https://www.bbc.com"]
    scraper = ArticleScraper(urls)
    article_links = scraper.get_article_links()
    print(article_links)
    print("FINISHED")

if __name__ == "__main__":
    main()