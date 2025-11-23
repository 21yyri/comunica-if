from google import genai
import dotenv, os

dotenv.load_dotenv()
CLIENT = genai.Client(
      api_key=os.getenv("GEMINI_API_KEY")
)

def validar_postagem(usuario, postagem):
        if usuario.is_authorized:
            return True
        
        validacao = CLIENT.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
                Verifique: ofensas (pessoais, intolerância, 
                escola, calão) ou burla (criptografia, substituições, 
                espaços). Resposta: S ou N\n\n{postagem}
            """
        ).text

        return validacao == "N"
