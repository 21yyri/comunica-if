from app import app, db, jwt
from flask import jsonify, request
from datetime import datetime
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import requests, os, dotenv, google.generativeai as genai
from app.models import *

dotenv.load_dotenv()

api_url = "https://suap.ifrn.edu.br/api"
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')   

@app.route('/api/usuarios')
@jwt_required
def usuarios():
    matricula = get_jwt_identity()
    query = db.select(Usuario).where(Usuario.matricula == matricula)

    if not db.session.scalars(query).one_or_none():
        return jsonify({"Erro": "usuário nâo encontrado."}), 404

    query = db.select(Usuario)
    all_users = db.session.scalars(query).all()
    return jsonify([user.to_dict() for user in all_users]), 200


@app.route('/api/usuarios/login', methods=["POST"])
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
        return jsonify({"Erro": "pipipipopopo"}), 400

    dados_usuario = dados_usuario.json()
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

    token = create_access_token(identity=credenciais["username"])
    print(token)

    return jsonify({"access": token}), 200


@app.route('/api/usuarios/deletar', methods=["DELETE"])
def deletar_todos_usuarios():
    usuarios: list[Usuario] = db.session.scalars(db.select(Usuario)).all()
    query = db.select(Postagem)

    for usuario in usuarios:
        postagens_usuario: list[Postagem] = db.session.scalars(
            query.where(Postagem.autor == usuario)
        ).all()
        for post in postagens_usuario:
            db.session.delete(post)
        db.session.delete(usuario)
    db.session.commit()

    return jsonify({"Sucesso": "usuarios deletados."}), 200


@app.route('/api/postagens')
@jwt_required
def postagens():
    matricula = get_jwt_identity()
    query = db.select(Usuario).where(Usuario.matricula == matricula)

    if not db.session.scalars(query).one_or_none():
        return jsonify({"Erro": "usuário nâo encontrado."}), 404
    
    postagens: list[Postagem] = db.session.scalars(db.select(Postagem)).all()
    if not postagens:
        return jsonify({"Erro": "nenhum post foi encontrado."}), 404
    return jsonify([post.to_dict() for post in postagens]), 201


@app.route('/api/postagens/postar', methods=['POST'])
@jwt_required
def postar():
    matricula = get_jwt_identity()
    query = db.select(Usuario).where(Usuario.matricula == matricula)

    if not db.session.scalars(query).one_or_none():
        return jsonify({"Erro": "usuário nâo encontrado."}), 404
    
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "dados ausentes"}), 400

    query = db.select(Usuario).where(
        Usuario.matricula == get_jwt_identity()
    )
    usuario = db.session.scalars(query).one_or_none()

    if not usuario:
        return jsonify({"Erro": "usuario nao existe"}), 400
    
    autorizacao = model.generate_content(f"""
        verifique msg p/ rede social escolar EM: filtre
        ofensas (pessoais, intolerância, escola, calão)
        Responda SIM ou NÃO \n\n {dados["postagem"]}
    """)

    if autorizacao.text == "SIM":
        post = Postagem(
            autor = usuario,
            postagem = dados["postagem"],
            data = datetime.now()
        )

        db.session.add(post)
        db.session.commit()

        return jsonify({"Sucesso": f"A postagem foi aceita no ambiente escolar: GEMINI -> {autorizacao.text}"}), 201
    
    return jsonify({"Erro": f"A postagem foi tida como imprópria ao ambiente escolar: GEMINI -> {autorizacao.text}"}), 400
    

@app.route('/api/postagens/deletar', methods=["DELETE"])
def apagar_todos__os_posts():
    query = db.select(Postagem)
    all_posts: list[Postagem] = db.session.scalars(query).all()

    for post in all_posts:
        db.session.delete(post)

    db.session.commit()

    return jsonify({"Sucesso": "posts deletados"}), 200
