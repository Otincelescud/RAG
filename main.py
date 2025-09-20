from webscraper import WebScraper
from urllib.parse import urljoin, urlparse

def main():
    # This is just the url of the test web server
    initial_root_url = "http://localhost:8000/local/"
    initial_output_addr = "output/scraped_text.txt"
    webScraper = WebScraper()
    webScraper.scrape_urls(initial_root_url, initial_output_addr, 5, 10, urlparse(initial_root_url).netloc)

if (__name__ == "__main__"):
    main()