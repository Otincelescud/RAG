from webscraper import WebScraper
from pathlib import Path

def main():
    # This is just the url of the test web server
    initial_root_url = "localhost:8000/local/"
    initial_output_url = "scraped_text.txt"
    webScraper = WebScraper(initial_root_url, initial_output_url)
    webScraper.scrape()

if (__name__ == "__main__"):
    main()