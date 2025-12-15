import feedparser, requests
from bs4 import BeautifulSoup
import logging, dotenv, os

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=".log", filemode="w",
    format="%(asctime)s - %(message)s"
)

COMUNICA_URL = "http://localhost:8000/api"
METROPOLES_URL = "https://metropoleonline.com.br/rss/latest-posts"

class MetropolesScraper:
    dotenv.load_dotenv()

    def scrape(self):
        feed = feedparser.parse(METROPOLES_URL)
        if feed.status != 200:
            raise requests.exceptions.ConnectionError()

        token = requests.post(f"{COMUNICA_URL}/login/", json = {
            "username": os.getenv("MATRICULA"),
            "password": os.getenv("SENHA"),
        }).json().get("Token")

        for news in feed.entries:
            noticia = {
                "titulo": news.title,
                "sumario": news.summary + '.',
                "link": news.link,
                "imagem": self._get_imagem(news.link),
                "disponivel": True,
                "automatizada": True
            }

            result = requests.post(
                f"{COMUNICA_URL}/noticia/", 
                json = noticia, headers = {
                    "Authorization": f"Token {token}"
                }
            )

            if result != 201:
                logger.error(f"STATUS CODE {result.status_code} PARA {news.link}.")
            

    def _get_imagem(self, url: str) -> str:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        return soup.select('img.img-fluid.center-image')[0].get("src")
