# srvSpacefl

## descrição
Servidor de artigos da Spaceflight News (https://spaceflightnewsapi.net/).  <br />
Inclua ou modifique seus próprios artigos !


## objetivo
Importando da Spaceflight News API (https://api.spaceflightnewsapi.net), este servidor disponibiliza artigos sobre voos espaciais, que podem ser consultados, modificados, incluidos novos ou excluídos.

Projeto criado para atender um Code Challenge, mas totalmente funcional e pode ser usado para referência, estudo, base para seu próprio servidor, lançamento dos seus próprios foguetes (brincadeira !).


## tecnologias
* python 3.8+
* FastAPI
* MongoDB


## estudo
Se for seu objetivo, pode estudar neste projeto:
* uso das tecnologias acima
* uso do FastAPI, criação dos endpoints, recepção e envio de dados
* uso do banco de dados MongoDB
* o arquivo de configuração cfg.py funciona para os propósitos atuais, mas deve ser repensado em um uso mais sério
* validação dos dados sendo inseridos ou modificados
* separação em módulos (.py) com respectivas funções
* sincronia com a API de origem; minha opção por identificar os novos itens via campo publishedAt (e não criar um doc de controle - que falha ocasionalmente)
* padronização das mensagens de retorno (mantra: padronização = menos código desnecessário)
* Dockerfile utilizando Alpine Linux (super leve !)
* arquivo cron 'cronjob' executando dentro do container, para executar a sincronia periodicamente
* testes de funcionamento dos endpoints; minha opção por rodar estes de - fora - do container (isto é, como um client real)
* outros que sou modesto demais para relacionar


## como instalar
### // baixe 
ou copie este repo para sua máquina <br />
<i>(porque escrever o óbvio ?!)</i>

### // python 3.8+
Instale uma versão atualizada do Python (3.8+).

Aqui têm um tutorial beeem completo: [ Python 3 Installation & Setup Guide – Real Python ](https://realpython.com/installing-python/)  <br />
<i>(aliás, guarde este site nos seus bookmarks, RealPython faz um trabalho excelente de divulgação e educação da linguagem)</i>

### // instale as dependências
> pip3 install -r requirements.txt

### // MongoDB
1. crie uma conta na [ MongoDB Atlas Database ](https://www.mongodb.com/atlas/database)
2. na plataforma crie um database, e neste uma collection (a interface não é muito intuitiva, um pouco dura, mas aws é pior)
3. modifique o arquivo cfg.py com as informações de acesso

### // execute
> cd (pasta onde baixou o projeto)/app  <br />
> uvicorn --host=0.0.0.0 --reload srvSpacefl:app

### // uso com docker
faça somente o passo 'MongoDB' acima <br />
tenha o docker instalado na sua máquina <i>(outra !)</i>

execute:
> sudo docker build -t srvspace1 .   <br />
> docker run -p 8000:8000 srvspace1

## como acessar
no seu browser ou via Postman:
> http://<IP>:8000/

a documentação OpenApi em:
> http://<IP>:8000/docs/


## como rodar os testes
> cd (pasta onde baixou o projeto)/testes  <br />
> pytest --tb=short -v --maxfail=0 testes/test_srvSpacefl.py


## video
Não


## desafio
This is a challenge by Coodesh


## contato
_Márcio Augusto_
* marcio.mais@indieo.com.br
* https://github.com/uhmano
