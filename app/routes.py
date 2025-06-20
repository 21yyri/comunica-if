from app import app, db
from flask import jsonify, request
from datetime import datetime 
from app.models import *


@app.route('/usuarios')
def usuarios():
    query = db.select(Usuario)
    all_users = db.session.scalars(query).all()
    return jsonify([
        user.to_dict() for user in all_users
    ]), 200


@app.route('/usuarios/registrar', methods=["POST"])
def registrar_user():
    dados = request.get_json()
    if not dados:
        return jsonify({
            "Erro": "dados ausentes"
        }), 400
    
    query = db.select(Usuario)
    if not db.session.scalars(query.where(Usuario.username == dados["username"])).one_or_none():
        db.session.add(
            Usuario(
                username = dados["username"],
                senha = dados["senha"]
            )
        )
        db.session.commit()
        return jsonify({
            "Sucesso": "usuario adicionado."
        }), 201

    return jsonify({
        "Erro": "usuario ja existente."
    }), 403


@app.route('/usuarios/deletar', methods=["DELETE"])
def deletar_usuarios():
    query = db.select(Usuario)
    all_users = db.session.scalars(query).all()
    
    for user in all_users:
        all_user_posts = db.session.scalars(query.where(Postagem.autor == user))
        for post in all_user_posts:
            db.session.delete(post)
        db.session.delete(user)

    db.session.commit()

    return jsonify({
        "Sucesso": "usuarios deletados"
    }), 200


@app.route('/postagens')
def postagens():
    query = db.select(Postagem)
    postagens = db.session.scalars(query).all()
    return jsonify(
        [post.to_dict() for post in postagens]
    ), 201


@app.route('/postagens/postar', methods=['POST'])
def postar():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "dados ausentes"}), 400

    query = db.select(Usuario).where(Usuario.username == dados["autor"]["username"])

    if not db.session.scalars(query).all(): # Procura o usuario na tabela
        db.session.add(
            Usuario(
                username = dados["autor"]["username"],
                senha = dados["autor"]["senha"]
            )
        )

    autor = db.session.scalars(db.select(Usuario).where(Usuario.username == dados["autor"]["username"])).one()
 
    post = Postagem(
        autor = autor, postagem = dados["postagem"], data = datetime.now()
    )

    db.session.add(post)

    db.session.commit()

    return jsonify({
        "Sucesso": "O envio foi concluido."
    }), 201


@app.route('/postagens/deletar', methods=["DELETE"])
def apagar_post():
    query = db.select(Postagem)
    all_posts = db.session.scalars(query).all()

    for post in all_posts:
        db.session.delete(post)

    db.session.commit()

    return jsonify({
        "Sucesso": "posts deletados"
    }), 200


