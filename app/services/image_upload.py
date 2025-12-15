import cloudinary, os, dotenv
from cloudinary.uploader import upload_image

dotenv.load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    secure=True
)

def upload(imagem) -> str:
    return upload_image(imagem).url
