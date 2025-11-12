import cloudinary, os, dotenv
from cloudinary.uploader import upload_image

dotenv.load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_secret=os.getenv("API_SECRET"),
    api_key=os.getenv("API_KEY"),
    secure=True
)

def upload(imagem) -> str:
    return upload_image(imagem).url
