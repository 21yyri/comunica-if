from app import app, db
from flask import jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import requests, os, dotenv, google.generativeai as genai
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
        "Authorization": f"Bearer {token.json()["access"]}"
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
    if not usuario:
        db.session.add(Usuario(
            username = dados_usuario["nome_social"] or dados_usuario["nome_registro"],
            matricula = credenciais["username"],
            senha = hash_senha(credenciais["password"]),
        ))
        db.session.commit()

    token = create_access_token(identity=credenciais["username"], expires_delta=timedelta(days = 7))
    print(token)

    return jsonify({"access": token}), 200


@app.route('/api/usuarios')
@jwt_required()
def get_usuarios():
    query = db.select(Usuario)
    all_users = db.session.scalars(query).all()

    return jsonify([user.to_dict() for user in all_users]), 200


@app.route('/api/postagens')
@jwt_required()
def get_postagens():
    postagens: list[Postagem] = db.session.scalars(db.select(Postagem)).all()

    if not postagens:
        return jsonify({"Erro": "nenhum post foi encontrado."}), 404
    
    return jsonify([post.to_dict() for post in postagens]), 201


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
    