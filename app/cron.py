from crawlers import CNNScraper, MetropolesScraper

def get_cnn_news():
    CNNScraper().scrape()


def get_metropoles_news():
    MetropolesScraper().scrape()
