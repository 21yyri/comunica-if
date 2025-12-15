import requests
from cnn import CNNScraper
from metropoles import MetropolesScraper

# CRONJOB
# SCHEDULE : 30 14 * * * $HOME/Projects/comunica-if/.venv/bin/python3 $HOME/Projects/comunica-if/web/scraper.py

def scrape():
    MetropolesScraper().scrape()
    CNNScraper().scrape()


if __name__ == "__main__":
    healthcheck = requests.get(
        "http://localhost:8000/api/healthcheck/"
    )

    if healthcheck.status_code == 200:
        scrape()
