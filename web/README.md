# Web crawlers
Uma das propostas da plataforma é trazer notícias cotidianas ao seu terminal mais próximo. Além das notícias propostas por servidores e administradores, há também as notícias automatizadas por scripts de web crawling.

Esses scripts carregam centenas de notícias online e as inserem na API da plataforma para que componham o carrossel.

## Scrape script
A automatização é dada pelo uso de cronjobs. O servidor usa de tarefas agendadas diariamente para fazer a raspagem.

Para a instalação dos pacotes necessários:
```
pkg/apt/dnf install python3
pkg/apt/dnf install cronie
```

- Note que: em muitos sistemas Linux, o cronie já vem instalado por padrão, e o gerenciador de pacotes fica a critério do instalador, considerando a amplitude dos pacotes mencionados.

Para definir o cronjob, abra o editor cron através do comando:
```
crontab -e 
```
Com o editor aberto, digite a expressão:
```
0 */8 * * * /aplicacao/.venv/bin/python3 aplicacao/web/scrape.py
```

A expressão significa que, em um ciclo diário, 3 (três) vezes ao dia, o script será executado.