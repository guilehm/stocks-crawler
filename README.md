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
* Docker


# Instalação

Clone este repositório

    $ git clone git@github.com:Guilehm/stocks-crawler.git

Entre no diretório

    $ cd stocks-crawler
    
Copie o arquivo `env.sample` para `.env`

    $ cp env.sample .env
    
Utilize algum editor para alterar suas credenciais*

    $ vim .env
    
### Instalação com Docker
*(se quiser rodar sem Docker, vá para a próxima etapa)*

É necessário ter o Docker e o Docker-compose instalados em sua máquina.
Recomendo este tutorial de instalação para o Linux [https://www.digitalocean.com/community/tutorials/como-instalar-e-usar-o-docker-no-ubuntu-18-04-pt](https://www.digitalocean.com/community/tutorials/como-instalar-e-usar-o-docker-no-ubuntu-18-04-pt)

Após ter concluído as etapas anteriores e estar com o serviço do Docker rodando, execute:

    $ docker-compose up
    
Neste ponto o app deverá estar rodando em [http://localhost:5000](http://localhost:5000) e o Mongodb na porta `27017`

### Execução via Flask local 

Crie o ambiente virtual *(necessário Pipenv)*

    $ pipenv install

Ative o ambiente virtual

    $ pipenv shell

Execute o app

    $ env $(cat .env) python app.py
    
### Execução via terminal

Execute o comando abaixo para obter ajuda

    $ python main.py --help

Inicie o crawler:

    $ python main.py
    

OBS.: para obter as credenciais se cadastre aqui [link](https://eduardocavalcanti.com/cadastro/)
