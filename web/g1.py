from bs4 import BeautifulSoup
import requests, logging, feedparser, dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=".log", filemode="w",
    format="%(asctime)s - %(message)s"
)

COMUNICA_URL = "http://localhost:8000/api"
RSS_URL = "https://g1.globo.com/rss/g1/"

class G1Scraper:
    dotenv.load_dotenv()

    def scrape(self):
        feed = feedparser.parse(RSS_URL)
        if feed.status != 200:
            raise requests.exceptions.HTTPError()
        
        token = requests.post(f"{COMUNICA_URL}/login/", json={
            "username": "20241174010007",
            "password": "D3lt4Run3kk"
        }).json().get("Token")


        for news in feed.entries:
            noticia = {
                "titulo": news.title,
                "sumario": news.get("subtitle", ''),
                "link": news.link,
                "disponivel": True,
                "imagem": self._get_imagem(news),
                "automatizado": True
            }

            result = requests.post(
                f"{COMUNICA_URL}/noticia/",
                json=noticia, headers={
                    "Authorization": f"Token {token}"
                }
            )

            if result.status_code != 201:
                logging.error(f"STATUS CODE {result.status_code} PARA {news.link}.")
    

    def _get_imagem(self, noticia):
        imagem = noticia.get("media_content", "")
        if imagem:
            return imagem[0].get("url")


if __name__ == '__main__':
    G1Scraper().scrape()
