from app import app, db
from flask import jsonify, request
from flask_login import login_user, logout_user
from datetime import datetime
import requests
from app.models import *

api_url = "https://suap.ifrn.edu.br/api"


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

@app.route('/usuarios/registrar', methods=["POST"])
def registrar_user():
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "dados ausentes"}), 400

    query = db.select(Usuario).where(Usuario.username == dados["username"])
    usuario_existe = db.session.scalars(query).one_or_none()
    if usuario_existe:
        return jsonify({"Erro": "usuario ja existente."}), 403

    senha_hash = hash_senha(dados["senha"])

    db.session.add(Usuario(
        username=dados["username"], senha=senha_hash
    ))
    db.session.commit()
    return jsonify({"Sucesso": "usuario adicionado."}), 201

"""
    O HASH DA SENHA TA RETORNANDO UM OBJETO
"""



@app.route('/usuario/login', methods=["POST"])
def login():
    credenciais = request.get_json()
    dados = {
        "username": credenciais["matricula"],
        "password": credenciais["senha"]
    }

    response = requests.post(api_url + "/token/pair", json=dados)
    if response.status_code == 200:
        query = db.select(Usuario).where(Usuario.matricula == dados["username"])

        usuario = db.session.scalars(query).one_or_none()
        if not usuario:
            token = response.json()["access"]
            headers = {
                "Authorization": f"Bearer {token}"
            }

            dados_usuario = requests.get(api_url + "/v2/minhas-informacoes/meus-dados/", headers=headers)
            print(dados_usuario.json())
            print('oii')
            if dados_usuario.status_code != 200:
                return jsonify({"Erro": "matrícula ou senha incorretos."}), 400
            usuario = Usuario(
                username = dados_usuario.json()["vinculo"]["nome"],
                matricula = credenciais["matricula"],
                senha = hash_senha(dados["password"])
            )
            print(hash_senha(dados["password"]))
            db.session.add(usuario)
            db.session.commit()

        login_user(usuario, remember=credenciais["remember-me"])
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
def del_user_por_nome():
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "dados vazios."}), 400

    username = dados["username"]
    senha = hash_senha(dados["senha"])

    query = db.select(Usuario).where(Usuario.username == username and Usuario.senha == senha)
    usuario = db.session.scalars(query).one_or_none()

    if not usuario or usuario.senha != senha:
        return jsonify({"Erro": "usuario nao encontrado ou senha incorreta."}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"sucesso": "usuario deletado"}), 200


@app.route('/usuarios/deletar/todos', methods=["DELETE"])
# FUNCAO DE DEBUG
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


@app.route('/postagens/<username>')
def postagem_by_username(username: str):
    query_user = db.select(Usuario).where(Usuario.username == username)
    usuario = db.session.scalars(query_user).one_or_none()

    if not usuario:
        return jsonify({"Erro": "usuario nao encontrado."}), 404

    query_posts = db.select(Postagem).where(Postagem.autor == usuario)
    posts_do_usuario: list[Postagem] = db.session.scalars(query_posts).all()

    if not posts_do_usuario:
        return jsonify({"Erro": "usuario nao tem posts registrados."})
    return jsonify([post.to_dict() for post in posts_do_usuario]), 200


@app.route('/postagens/postar', methods=['POST'])
def postar():
    dados: dict[Postagem] = request.get_json()
    if not dados:
        return jsonify({"erro": "dados ausentes"}), 400

    query = db.select(Usuario).where(
        Usuario.username == dados["autor"]["username"])
    usuario: Usuario | None = db.session.scalars(query).one_or_none()

    if not usuario:
        return jsonify({"Erro": "usuario nao existe"}), 400

    post = Postagem(
        autor=usuario, postagem=dados["postagem"], data=datetime.now()
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({"Sucesso": "O envio foi concluido."}), 201


@app.route('/postagens/deletar', methods=["DELETE"])
def apagar_todos__os_posts():
    query = db.select(Postagem)
    all_posts: list[Postagem] = db.session.scalars(query).all()

    for post in all_posts:
        db.session.delete(post)

    db.session.commit()

    return jsonify({"Sucesso": "posts deletados"}), 200
