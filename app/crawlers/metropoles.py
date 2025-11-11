import feedparser, requests
from bs4 import BeautifulSoup

COMUNICA_URL = "http://localhost:8000/api"
METROPOLES_URL = "https://metropoleonline.com.br/rss/latest-posts"

class MetropolesScraper:
    def scrape(self):
        feed = feedparser.parse(METROPOLES_URL)
        if feed.status != 200:
            raise requests.exceptions.ConnectionError()

        token = requests.post(f"{COMUNICA_URL}/login/", json = {
            "username": "20241174010007",
            "password": "",
        }).json().get("Token")

        for news in feed.entries:
            noticia = {
                "titulo": news.title,
                "sumario": news.summary + '.',
                "link": news.link,
            }

            requests.post(
                f"{COMUNICA_URL}/news/post/", 
                json = noticia, headers = {
                    "Authorization": f"Bearer {token}"
                }
            )
            

    def _get_imagem(self, url: str) -> str:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        return soup.select('img.img-fluid.center-image')[0].get("src")
