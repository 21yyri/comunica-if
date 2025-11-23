# Comunica IFCM
Uma API que registra postagens e comunicados de alunos e servidores para display em carrossel de conteúdo via TVs disponibilizadas pelo campus.

Pensado para melhorar a ala de comunicação da escola em meio a proibição de celulares.
## Requisitos
- Python 3.10+
- pip (package manager)

## Instalando dependências
`pip install -r requirements.txt`

Algumas das dependências utilizadas: Django e DRF, Pillow, google-genai, mysqlclient, requests.

## Configuração
O arquivo `.env` deve conter uma chave da API do gemini, para a moderação das postagens.
```
GEMINI_API_KEY=value
```
## Autenticação
No endpoint `/api/login/`, o usuário deve fazer uma requisição POST contendo os parâmetros `username`, que deve ser uma matrícula válida no campus IFRN Ceará-Mirim, e `password`, referente à senha do usuário vinculado a matrícula. Caso os requisitos sejam propriamente cumpridos, o servidor retornará um token que deve cobrir uma boa parcela dos cabeçalhos de requisições, visando o acesso a diferentes features.

```
{
	"access": "Token {token_string}"
}
```

## Exemplos de endpoints

- `/api/posts/` -> POST: recebe um `body` com texto de até 80 caracteres e um argumento opcional `imagem`. Pode retornar **400** caso o conteúdo da postagem não seja validado pela IA, **201** caso a postagem seja válida e criada, ou **503** se o servidor da IA esteja sobrecarregado.
- ``/api/noticias/`` -> POST:  recebe um corpo com chaves que designam setor, titulo, corpo, imagem interna ou externa, data e link. Deve retornar **409** caso uma notícia externa já esteja registrada ou **201** caso tenha sido registrada com sucesso.

Muitas das views para usuário, postagem e notícia seguem os padrões REST e não precisam ser detalhadas aqui.

## Colaboradores
Leo Silva, orientador do projeto.
