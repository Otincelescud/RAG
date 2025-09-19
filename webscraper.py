import requests
from bs4 import BeautifulSoup

class WebScraper:
    root_url: str
    output_address: str

    def __init__(self, root_url: str, output_address: str):
        self.root_url = root_url
        self.output_address = output_address

    def __repr__(self) -> str:
        return f"WebScraper(root_url={self.root_url}, output_address={self.output_address})"

    def set_root_url(self, root_url: str):
        self.root_url = root_url

    def set_output_address(self, output_address: str):
        self.output_address = output_address        

    def scrape(self):
        pass