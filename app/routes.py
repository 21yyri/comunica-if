from app import app, db
from flask import jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import requests, os, dotenv, google.generativeai as genai
from base64 import b64decode
from app.models import *

dotenv.load_dotenv()

api_url = "https://suap.ifrn.edu.br/api"
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')   


@app.route('/api/login', methods=["POST"])
def login():
    credenciais = request.get_json()

    token = requests.post(api_url + "/token/pair", json=credenciais)
    if token.status_code != 200:
        return jsonify({"Erro": "matrícula ou senha incorretos."}), 400
    
    headers = {
        "Authorization": f"Bearer {token.json().get("access")}"
    }

    dados_usuario = requests.get(api_url + "/rh/eu/", headers=headers)
    if dados_usuario.status_code != 200:
        return jsonify(dados_usuario.json()), 400

    dados_usuario = dados_usuario.json()
    if dados_usuario.get("campus") != "CM":
        return jsonify({"Erro": "campus não autorizado."}), 400
    
    query = db.select(Usuario).where(
        Usuario.matricula == credenciais["username"] and Usuario.senha == hash_senha(credenciais["password"])
    )

    usuario = db.session.scalars(query).one_or_none()

    vinculo = requests.get(api_url + "/rh/meus-dados", headers=headers).json().get("tipo_vinculo")
    if not usuario:
        db.session.add(Usuario(
            username = dados_usuario["nome_social"] or dados_usuario["nome_registro"],
            matricula = credenciais["username"],
            senha = hash_senha(credenciais["password"]),
            servidor = True if vinculo == "Servidor" else False
        ))
        db.session.commit()

    token = create_access_token(identity=credenciais["username"], expires_delta=timedelta(days = 7))
    return jsonify({"access": token}), 200


@app.route('/api/usuarios')
@jwt_required()
def get_usuarios():
    query = db.select(Usuario)
    all_users = db.session.scalars(query).all()

    return jsonify([user.__dict__ for user in all_users]), 200


@app.route('/api/postagens')
@jwt_required()
def get_postagens():
    postagens: list[Postagem] = db.session.scalars(db.select(Postagem)).all()

    if not postagens:
        return jsonify({"Erro": "nenhum post foi encontrado."}), 404
    
    return jsonify([post.__dict__ for post in postagens]), 201


@app.route('/api/postagens/post', methods=['POST'])
@jwt_required()
def post():
    postagem = request.get_json()
    if not postagem:
        return jsonify({"erro": "dados ausentes"}), 400

    query = db.select(Usuario).where(
        Usuario.matricula == get_jwt_identity()
    )
    usuario = db.session.scalars(query).one_or_none()

    if not usuario:
        return jsonify({"Erro": "usuario nao existe"}), 400
    
    # Verifica se a postagem é imprópria, retornando N ou S
    autorizacao = model.generate_content(
        f"""Verifique: ofensas (pessoais, intolerância,
        escola, calão) ou burla (criptografia, substituições, 
        espaços). Resposta: S ou N\n\n{postagem}""")
    
    if autorizacao.text == "N":
        post = Postagem(
            autor = usuario,
            postagem = postagem["postagem"],
            data = datetime.now()
        )

        db.session.add(post)
        db.session.commit()

        return jsonify({"Sucesso": "A postagem foi aceita no ambiente escolar."}), 201
    
    return jsonify({"Erro": "A postagem foi tida como imprópria ao ambiente escolar."}), 400


@app.route('/api/noticia/post', methods=["POST"])
@jwt_required()
def post_noticias():
    query = db.select(Usuario).where(Usuario.matricula == get_jwt_identity())
    usuario = db.session.scalar(query)

    if not usuario.is_servidor:
        return jsonify({"Erro": "usuário não autorizado para postar notícias."})
    
    noticia = request.get_json()
    imagem = noticia.get("imagem")
    
    # Criando a imagem
    if imagem["conteudo"]:
        with open(f"imgs/{imagem["caminho"]}.png", "wb") as file:
            file.write(b64decode(imagem.get("conteudo")))

    db.session.add(Noticia(
        autor = usuario,
        titulo = noticia.get("titulo"),
        corpo = noticia.get("corpo"),
        imagem = imagem.get("caminho"),
        link = noticia.get("link")
    ))
    db.session.commit()
    
    return jsonify({"Sucesso": "notícia registrada."}), 200

    """
        {
            titulo: titulo,
            corpo: corpo,
            imagem: {
                caminho: caminho,
                conteudo: conteudo
            },
            link: link
        }
    
    """


@app.route('/api/noticias')
@jwt_required()
def noticias():
    noticias = db.session.scalars(db.select(Noticia)).all()
    if not noticias:
        return jsonify({"Erro": "nenhuma noticia registrada."}), 400
    
    return jsonify([noticia.__dict__ for noticia in noticias]), 200
