# Comunica IFCM
Uma API que registra postagens e comunicados de alunos e servidores para display em carrossel de conteúdo via TVs disponibilizadas pelo campus.

Pensado para melhorar a ala de comunicação da escola em meio a proibição de celulares.
## Requisitos
- Python 3.10+
- pip (package manager)
- MySQL/MariaDB
- Redis Cache

## Instalando dependências
`pip install -r requirements.txt`

Algumas das dependências utilizadas: Django e DRF, Pillow, google-genai, mysqlclient, requests, redis, feedparser.

## Configuração
As variáveis de ambiente necessárias para o funcionamento da aplicação estão presentes no arquivo `.env.example`:

```
# Chave da aplicação
SECRET_KEY=

# Serviço de moderação
GEMINI_API_KEY=

# Serviço de upload em nuvem
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# Placeholders enquanto não há um super usuário
MATRICULA=
SENHA=
```
## Autenticação
No endpoint `/api/login/`, o usuário deve fazer uma requisição POST contendo os parâmetros `username`, que deve ser uma matrícula válida no campus IFRN Ceará-Mirim, e `password`, referente à senha do usuário vinculado a matrícula. Caso os requisitos sejam propriamente cumpridos, o servidor retornará um token que deve cobrir parte dos cabeçalhos de requisições, visando o acesso a diferentes features.

```
{
	"access": "Token e46c32f98a9aa7669e3d11d95570e7890e66c768"
}
```

## Exemplos de endpoints
- `/api/carrossel/` ->  GET: não requer autenticação. Retorna uma lista que mistura postagens e notícias sob a razão de 1 para 5. Retorna sempre **200** quando requisitado.
- `/api/postagem/` -> POST: recebe um `corpo` com texto de até 80 caracteres e um argumento `imagem`. Pode retornar **400** caso o conteúdo da postagem não seja validado pela IA, **201** caso a postagem seja válida e criada, ou **503** se o servidor da IA esteja sobrecarregado.
- ``/api/noticia/`` -> POST:  recebe um corpo com chaves que designam titulo, sumário e como opcionais: url de imagem e link da notícia. Deve retornar **409** caso uma notícia externa já esteja registrada ou **201** caso tenha sido registrada com sucesso.

## Colaboradores
Leo Silva, orientador do projeto.