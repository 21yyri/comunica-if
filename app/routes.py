from app import app, db
from flask import jsonify, request
from datetime import datetime, timedelta
import requests, os, jwt, dotenv, google.generativeai as genai
from app.models import *

dotenv.load_dotenv()

api_url = "https://suap.ifrn.edu.br/api"
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')   

@app.route('/usuarios')
def usuarios():
    query = db.select(Usuario)
    all_users = db.session.scalars(query).all()
    return jsonify([user.to_dict() for user in all_users]), 200


@app.route('/usuarios/login', methods=["POST"])
def login():
    credenciais = request.get_json()

    token = requests.post(api_url + "/token/pair", json=credenciais)
    if token.status_code != 200:
        return jsonify({"Erro": "matrícula ou senha incorretos."}), 400
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    dados_usuario = requests.get(api_url + "/v2/minhas-informacoes/meus-dados/", headers=headers).json()
    usuario = Usuario.query.filter_by(
        Usuario.matricula == credenciais["matricula"] and Usuario.senha == hash_senha(credenciais["senha"])
    ).one_or_none()

    if not usuario:
        db.session.add(Usuario(
            username = dados_usuario["vinculo"]["nome"],
            matricula = credenciais["username"],
            senha = hash_senha(credenciais["senha"]),
        ))
        db.session.commit()
    







    if token.status_code == 200:
        query = db.select(Usuario).where(Usuario.matricula == credenciais["username"])

        usuario = db.session.scalars(query).one_or_none()
        if not usuario:
            token.update({
                "iat": datetime.now().timestamp(),
                "exp": (datetime.now() + timedelta(days=7)).timestamp()
            })

            token_jwt = jwt.encode(token, os.getenv("SECRET_KEY"), algorithm='HS256')

            headers = {
                "Authorization": f"Bearer {token_jwt}"
            }

            dados_usuario = requests.get(api_url + "/v2/minhas-informacoes/meus-dados/", headers=headers)

            if dados_usuario.status_code != 200:
                return jsonify({"Erro": "matrícula ou senha incorretos."}), 400
            
            if dados_usuario["campus"] != 'CM':
                return jsonify({"Erro": "Campus não autorizado."})
            
            usuario = Usuario(
                username = dados_usuario.json()["vinculo"]["nome"],
                matricula = credenciais["username"],
                senha = hash_senha(credenciais["password"])
            )

            db.session.add(usuario)
            db.session.commit()

        return jsonify({"Sucesso": "logado com sucesso."}), 200


@app.route('/usuarios/deletar', methods=["DELETE"])
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


@app.route('/postagens')
def postagens():
    postagens: list[Postagem] = db.session.scalars(db.select(Postagem)).all()
    if not postagens:
        return jsonify({"Erro": "nenhum post foi encontrado."}), 404
    return jsonify([post.to_dict() for post in postagens]), 201


@app.route('/postagens/postar', methods=['POST'])
def postar():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "dados ausentes"}), 400

    query = db.select(Usuario).where(
        Usuario.matricula == dados["autor"]["username"]
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
    

@app.route('/postagens/deletar', methods=["DELETE"])
def apagar_todos__os_posts():
    query = db.select(Postagem)
    all_posts: list[Postagem] = db.session.scalars(query).all()

    for post in all_posts:
        db.session.delete(post)

    db.session.commit()

    return jsonify({"Sucesso": "posts deletados"}), 200
