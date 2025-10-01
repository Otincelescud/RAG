from webscraper import WebScraper
from urllib.parse import urlparse
from pathlib import Path
import requests
import json

def main():
    # Load paramaters from params.json
    parms_path = Path("./params.json")
    if not parms_path.exists():
        print("params.json file doesn't exist")
        return
    
    params = {}
    with open(parms_path, "r") as params_file:
        params = json.load(params_file)
    
    print("Parameter file loaded. Make sure all information is correct")

    # Check if url loads
    init_root_url_string = params.get("root_url", "")
    init_root_url = None
    try:
        init_root_url = urlparse(init_root_url_string)
    except ValueError:
        print("Invalid root url")
        return

    # Check if url has scheme and netloc
    if not all([init_root_url.scheme, init_root_url.netloc]):
        print("URL is invalid")
        return
    
    # Verify https
    if not init_root_url.scheme.lower() == "https":
        print("Url is not https")
        return
    
    # Try to ping root url
    try:
        r = requests.head(init_root_url.geturl(), allow_redirects=True, timeout=5)
        r.raise_for_status()
    except requests.RequestException:
        print("Pinging root url didn't work")
        return
    


    out_path = Path("./output") / Path(params.get("out_path", "default_output.txt")).name

    # This is just the url of the test web server
    webScraper = WebScraper()
    webScraper.scrape_urls(init_root_url.geturl(), str(out_path), 5, 10, init_root_url.netloc)

if (__name__ == "__main__"):
    main()