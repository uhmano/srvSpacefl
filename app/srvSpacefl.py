#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
srvSpacefl
servidor principal e rotas


# histórico
2022-06-01 	v.1
2022-05-30 	primeira versão

'''
from fastapi import FastAPI, Body, Response  #, HTTPException, status

#// modelo de dados
from modelo import Artigo

#// dados
from conexaoDB import fb_col
db, col = fb_col()

#// regras de negócio
from regras import lista_articles, inclui_article, atualiza_article, remove_article


#// servidor
app = FastAPI(
	
	#// configs para doc Openapi
	title       = 'srvSpacefl',
	description = 'artigos apartir de api.spaceflightnewsapi.net (e inclua o seu !)',
	version     = '1.0.0',
	contact     = {
		'name' : 'Márcio Augusto',
		'url'  : 'https://github.com/uhmano',
		'email': 'marcio.mais@indieo.com.br',
    },
)


#// rotas
@app.get('/')
async def ep_status():
	'''
	informação que o servidor está no ar

	Returns
	-------
	str:
		mensagem
	'''

	return 'Back-end Challenge 2022 - Space Flight News'


@app.get('/articles')
@app.get('/articles/{id}')
async def ep_lista_articles(response: Response, id: str= '', publishedAt: str= '', limite: int= 30):
	'''
	retorna um ou vários artigos
	
	Params
	-------
	- id (str, opcional):

		trazer artigo com o id; ou todos se vazio

	- publishedAt (str, opcional):

		trazer artigos apartir de

	- limite (int, opcional, default: 30):

		quantos itens retornar no máximo

	Returns
	-------
	- msg (str):

		mensagem de sucesso ou erro

	- qtde (int):

		quantidade de artigos sendo retornada

	- articles (array):

		relação de artigos

	'''
	
	(sucesso, retorno) = await lista_articles(id, publishedAt, limite)
	
	if not sucesso:
		response.status_code = 422
	
	return retorno


@app.post('/articles')
async def ep_inclui_article(response: Response, artigo: Artigo = Body(...)):
	'''
	inclui um novo artigo no db
	
	Params
	-------
	- featured (bool)
	- title (str)	
	- url (str)		
	- imageUrl (str)		
	- newsSite (str)		
	- summary (str)		
	- publishedAt (str)
	- launches (array)
	
		id: str 
		provider: str
		
	- events (array):

		id: str 
		provider: str

	Returns
	-------
	- msg (str):

		mensagem de sucesso ou erro

	- id (str):

		id inserido

	'''

	(sucesso, retorno) = await inclui_article(artigo)
	
	if not sucesso:
		response.status_code = 422
	
	return retorno


@app.put('/articles/{id}')
async def ep_atualiza_article(response: Response, id: str, artigo: Artigo = Body(...)):
	'''
	salva alterações de um artigo no db
	
	Params (url)
	-------
	- id (str):

		id do artigo a ser atualizado


	Params (body)
	-------
	- featured (bool)
	- title (str)	
	- url (str)		
	- imageUrl (str)		
	- newsSite (str)		
	- summary (str)		
	- publishedAt (str)
	- launches (array)
	
		id: str 
		provider: str
		
	- events (array):

		id: str 
		provider: str

	Returns
	-------
	- msg (str):

		mensagem de sucesso ou erro

	- id (str):

		id atualizado (mesmo)
	'''

	(sucesso, retorno) = await atualiza_article(id, artigo)
	
	if not sucesso:
		response.status_code = 422
	
	return retorno


@app.delete('/articles/{id}' )#, status_code= 200)
async def ep_remove_article(response: Response, id: str):
	'''
	remove artigo do db
	
	Params (url)
	-------
	- id (str):

		id do artigo a ser removido


	Returns
	-------
	- msg (str):

		mensagem de sucesso ou erro

	- id (str):

		id removido (mesmo)
	'''
	(sucesso, retorno) = await remove_article(id)
	
	if not sucesso:
		response.status_code = 422
	
	return retorno

