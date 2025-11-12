from google import genai

CLIENT = genai.Client()

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
