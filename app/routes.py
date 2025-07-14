from app import app, db
from flask import jsonify, request
from flask_login import login_user, logout_user
from datetime import datetime, timedelta
import requests, os, jwt, dotenv, google.generativeai as genai
from app.models import *

dotenv.load_dotenv()

api_url = "https://suap.ifrn.edu.br/api"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')   

@app.route('/usuarios')
def usuarios():
    query = db.select(Usuario)
    all_users = db.session.scalars(query).all()
    return jsonify([user.to_dict() for user in all_users]), 200


@app.route('/usuarios/<username>')
def usuario_por_username(username):
    query = db.select(Usuario).where(Usuario.username == username)
    resultado = db.session.scalars(query).one_or_none()

    if not resultado:
        return jsonify({"Erro": "usuario nao encontrado."}), 404
    return jsonify(resultado.to_dict()), 200


@app.route('/usuarios/login', methods=["POST"])
def login():
    credenciais = request.get_json()

    response = requests.post(api_url + "/token/pair", json=credenciais)
    if response.status_code == 200:
        query = db.select(Usuario).where(Usuario.matricula == credenciais["username"])

        usuario = db.session.scalars(query).one_or_none()
        if not usuario:
            credenciais.update({
                "exp": datetime.now() + timedelta(days=7)
            })

            token_jwt = jwt.encode(credenciais, os.getenv("SECRET_KEY"), algorithm='HS256')

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

        login_user(usuario, remember = True, duration = datetime.now() + timedelta(days=7))
        return jsonify({"Sucesso": "logado com sucesso."}), 200






    # query = db.select(Usuario).where(
    #     Usuario.username == credenciais["username"]
    # )
    # usuario: Usuario = db.session.scalar(query).one_or_none()

    # if not usuario or usuario.check_senha(hash_senha(credenciais["senha"])):
    #     return jsonify({"Erro": "usuario ou senha incorretos."}), 404
    
    # login_user(usuario, remember=credenciais["remember-me"])
    # return jsonify({"Sucesso": "user autenticado."}), 200


@app.route('/usuarios/deletar', methods=["DELETE"])
def deletar_todos_usuarios():
    usuarios: list[Usuario] = db.session.scalars(db.select(Usuario)).all()
    query = db.select(Postagem)

    for usuario in usuarios:
        postagens_usuario: list[Postagem] = db.session.scalars(
            query.where(Postagem.autor == usuario)).all()
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
        verifique msg p/ rede social escolar EM: filtre ofensas (pessoais, intolerância, escola, baixo calão) Responda SIM ou NÃO\n\n
        {dados["postagem"]}
    """)

    print(autorizacao.text)
    if autorizacao.text == "SIM":
        post = Postagem(
            autor=usuario, postagem=dados["postagem"], data=datetime.now()
        )
        db.session.add(post)
        db.session.commit()

        return jsonify({"Sucesso": f"O envio foi concluido: gemini disse {autorizacao.text}"}), 201
    
    return jsonify({"Erro": f"O envio não teve sucesso: {autorizacao.text}"}), 400
    


@app.route('/postagens/deletar', methods=["DELETE"])
def apagar_todos__os_posts():
    query = db.select(Postagem)
    all_posts: list[Postagem] = db.session.scalars(query).all()

    for post in all_posts:
        db.session.delete(post)

    db.session.commit()

    return jsonify({"Sucesso": "posts deletados"}), 200
