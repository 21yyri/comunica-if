# TV Box
Nesse diretório encontra-se a documentação das ferramentas e direcionamentos acerca da configuração dos TV Box usados para display da interface web do projeto.

## On-boot script
Os dispositivos precisam inicializar junto do navegador para a visualização do carrossel, portanto, é neccessária a configuração de um cronjob que execute o `on_boot.py`.

Para a instalação dos pacotes necessários, digite no terminal:
```
pkg install python3
pkg install cronie
```
- No caso dos TV Box, pkg é o gerenciador de pacotes padrão, e cronie não vem instalado.

Para definir o cronjob, abra o editor cron através do comando:
```
crontab -e 
```

Com o editor aberto, digite a expressão:
```
@reboot /usr/bin/python3 ~/aplicacao/tv/on_boot.py
```
Essa asserção significa que a cada inicialização do aparelho, o navegador iniciará com a aplicação aberta, evitando configuração manual.