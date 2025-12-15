import requests
from cnn import CNNScraper
from metropoles import MetropolesScraper
from g1 import G1Scraper

# CRONJOB
# 0 */8 * * * $HOME/Projects/comunica-if/.venv/bin/python3 $HOME/Projects/comunica-if/web/scraper.py

def scrape():
    MetropolesScraper().scrape()
    CNNScraper().scrape()
    G1Scraper().scrape()


if __name__ == "__main__":
    healthcheck = requests.get(
        "http://localhost:8000/api/healthcheck/"
    )

    if healthcheck.status_code == 200:
        scrape()
