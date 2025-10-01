import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time
import random
import re

# Scraper Algorithm
"""
The scraper will go down recursively through the links it finds starting from the root url, saving the new urls in a list
The user will have to specify, the number of levels it wants the scraper to go down and the
max number of urls it can scrape.
The user will also have to provide a list of domains from which
it can collect data. If instead of a list, the user provides the boolean value True, the webscraper will collect data from everywhere
After url collection, the get_data() function will collect all html and docx files and save their
text in a file at the output_address.
"""

class WebScraper:
    visited = set()
    min_delay_between_requests = 1.0
    max_delay_between_requests = 3.0
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    } # Change to whatever you need


    def delay_requests(self):
        time.sleep(random.uniform(self.min_delay_between_requests, self.max_delay_between_requests))

    
    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)

        # Lowercase scheme and netloc
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()

        # Normalize path (remove redundant slashes, etc.)
        path = parsed.path or "/"

        # Rebuild URL without fragment
        return urlunparse((scheme, netloc, path, "", parsed.query, ""))

    def clean_text(self, text: str):
        # remove extra space/tabs around newlines
        text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
        # collapse multiple newlines into one
        text = re.sub(r"\n{2,}", "\n", text)
        # Collapse multiple spaces into one
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text

        # Pretend i am microsoft edge browser on windows or some bs like that
        # send request to root url
        # get text from start page

        # add all relevant additional urls to list
        # send get requests to urls i haven't visited before
        # get html or docx data or whatever else needs to be collected
        # repeat until done or until it hits recursion limit

    def read_html(self, r, output_addr, max_urls_per_page):
        # Save Text contents
        soup = BeautifulSoup(r.text, features="html.parser")
        text = soup.get_text()
        with open(output_addr, "at", encoding="utf-8", errors="ignore") as out:
            out.write(self.clean_text(text))

        self.delay_requests()

        # Follow next urls
        link_list = []
        for link in soup.find_all("a", href=True, limit=max_urls_per_page):
            # Append normalized url
            link_list.append(self.normalize_url(str(link["href"])))

        return link_list

    def scrape_urls(self, root_url, output_addr, max_recursion, max_urls_per_page, domain, recursion_level=0):
        # recursively scrape links

        # Check if condition is met to stop scraping branch
        if recursion_level >= max_recursion:
            return None
        if root_url in self.visited:
            return
        if len(root_url) < 8 and root_url[:8] != "https://":
            return
        
        self.visited.add(root_url)
        
        print(f"Visiting {root_url}")

        # Get request

        try:
            r = requests.get(root_url, headers=self.headers, timeout=5)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed: {root_url}")
            return
        
        # Check if content is html
        
        if "text/html" not in r.headers.get("Content-Type", ""):
            print(f"Skipping non-HTML content: {root_url}")
            return

        # Follow next urls
        link_list = self.read_html(r, output_addr, max_urls_per_page)
        
        for url in link_list:
            abs_url = urljoin(root_url, url)
            if urlparse(abs_url).netloc == domain:
                self.scrape_urls(abs_url, output_addr, max_recursion, max_urls_per_page, domain, recursion_level+1)