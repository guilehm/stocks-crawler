# Web Scraper de Análise Fundamentalista de Ações


# Api em Produção
https://gui-stocks.herokuapp.com/


---

# Descrição

Este [crawler](https://github.com/Guilehm/stocks-crawler/blob/master/stocks_spider.py) extrai as informações do site do [Eduardo](https://eduardocavalcanti.com/) que tem várias análises sobre as empresas da Bolsa de Valores.
Criei a API para poder utilizar estas as informações em [meu BOT](https://github.com/Guilehm/dark-souls).
![Screenshot from 2019-09-01 22-24-59](https://user-images.githubusercontent.com/33688752/64085159-5c637d80-cd07-11e9-9c3e-c85809798ed7.png)


###  Endpoints base
Estes endpoints aceitam `GET` e `POST`.

Com `GET` as informações serão recuperadas do Mongodb, com `POST` o crawler irá extrair em tempo real e salvar no Mongo.
* https://gui-stocks.herokuapp.com/stocks/
* [https://gui-stocks.herokuapp.com/stocks/mglu/analysis/](https://gui-stocks.herokuapp.com/stocks/mglu/analysis/)

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
    
*<small>*para obter as credenciais se cadastre [aqui](https://eduardocavalcanti.com/cadastro/).
    faça o cadastro com e-mail e senha, <strong>não</strong> utilize o login do Facebook.*</small>
    
### Instalação com Docker
*(se quiser rodar sem Docker, vá para a próxima etapa)*

É necessário ter o Docker e o Docker-compose instalados em sua máquina.
Recomendo este tutorial de instalação para o Linux [https://www.digitalocean.com/community/tutorials/como-instalar-e-usar-o-docker-no-ubuntu-18-04-pt](https://www.digitalocean.com/community/tutorials/como-instalar-e-usar-o-docker-no-ubuntu-18-04-pt)

Após ter concluído as etapas anteriores e estar com o serviço do Docker rodando, execute:

    $ docker-compose up
    
Finalizamos, neste ponto o app deverá estar rodando em [http://localhost:5000](http://localhost:5000) e o Mongodb na porta `27017`. Siga os próximos passos apenas se não desejar executar o app via Docker.


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
    
    
## Resolução de problemas
*Caso ocorra o seguinte erro:*
```
Error starting userland proxy: listen tcp 0.0.0.0:5000: bind: address already in use
```
*Pare a execução do seu mongo local com o seguinte comando:*

    $ sudo systemctl stop mongodb

Faça o build novamente

    $ docker-compose up --build
