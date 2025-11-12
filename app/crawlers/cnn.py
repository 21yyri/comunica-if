import feedparser, requests
from bs4 import BeautifulSoup

COMUNICA_URL = "http://127.0.0.1:8000/api"
RSS_URL = "https://admin.cnnbrasil.com.br/feed/"

# def format_categoria(categoria: str) -> str:
#     """Retorna a categoria com capitalização e acentuação."""
    
#     match categoria:
#         case 'politica':
#             return 'Política'
#         case 'educacao':
#             return 'Educação'
#         case 'saude':
#             return 'Saúde'
#         case _:
#             return categoria.capitalize()


class CNNScraper:
    def scrape(self):
        feed = feedparser.parse(RSS_URL)
        if feed.status != 200:
            raise requests.exceptions.HTTPError()

        # CATEGORIAS = [
        #     'economia', 'politica', 
        #     'esportes', 'educacao', 
        #     'nacional', 'saude',
        #     'tecnologia', 'nacional'
        # ]

        token = requests.post(f"{COMUNICA_URL}/login/", json = {
            "username": "20241174010007",
            "password": "Und3rT4l3kk",
        }).json().get("Token")

        for news in feed.entries:
            # categoria = news.link.split('/')[3]
            # if categoria not in CATEGORIAS:
            #     continue
            
            noticia = {
                "titulo": news.title,
                "sumario": news.summary + '.',
                "link": news.link,
                "disponivel": True
            }

            requests.post(
                f"{COMUNICA_URL}/noticia/",
                json = noticia, headers = {
                    "Authorization": f"Token {token}"
                }
            )


    def _get_imagem(self, url: str) -> str:
        """Recebe uma notícia e retorna a URL para a imagem de capa da notícia."""
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        imagem = soup.select('img.flex.size-full.object-cover')[2]

        return imagem.get("src")
