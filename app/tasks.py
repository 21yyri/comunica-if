from celery import shared_task
from .crawlers import CNNScraper, MetropolesScraper

@shared_task
def scrape_news():
    CNNScraper().scrape()
    MetropolesScraper().scrape()
