import requests
from cnn import CNNScraper
from metropoles import MetropolesScraper

def scrape():
    MetropolesScraper().scrape()
    CNNScraper().scrape()


if __name__ == "__main__":
    healthcheck = requests.get(
        "http://localhost:8000/api/healthcheck/"
    )

    if healthcheck.status_code == 200:
        scrape()
