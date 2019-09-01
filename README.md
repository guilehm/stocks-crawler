# Web Scraper de Análise Fundamentalista de Ações


# Api em Produção
https://gui-stocks.herokuapp.com/


---
# Visão Geral

* Mongodb
* Pymongo
* Scrapy
* Xpath
* Flask
* Rest API
* Click


# Instalação

Clone este repositório

    $ git clone git@github.com:Guilehm/stocks-crawler.git

Entre no diretório

    $ cd stocks-crawler

Crie o ambiente virtual *(necessário Pipenv)*

    $ pipenv install

Ative o ambiente virtual

    $ pipenv shell
    
    

### Execução via terminal

Execute o comando abaixo para obter ajuda

    $ python main.py --help

Inicie o crawler:

    $ python main.py


### Execução via Flask

Copie o arquivo env.sample para .env

    $ cp env.sample .env
    
   
Utilize algum editor para alterar suas credenciais*

    $ vim .env
    
Execute o app

    $ env $(cat .env) python app.py

OBS.: para obter as credenciais se cadastre aqui [link](https://eduardocavalcanti.com/cadastro/)
