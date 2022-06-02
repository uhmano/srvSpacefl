#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
regras.py
regras de negócio


# histórico
2022-06-01 	v.1

'''
from bson import ObjectId

#// modelo de dados
from modelo import Artigo

#// dados
from conexaoDB import fb_col
db, col = fb_col()

#// auxiliares
#// 	Agora: data e hora atual, uso como sugestão se publishedAt vazio
from auxiliares import Agora, msgOk, msgErro

#// emDebug: mensagens de erro detalhadas (True/False)
from cfg import emDebug


async def lista_articles(id, publishedAt, limite):
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
	- sucesso (bool)
		True/False se conseguiu

	- retorno (dict)
		- msg (str):
			mensagem de sucesso ou erro
	
		- qtde (int):
			quantidade de artigos sendo retornada; ou 0
	
		- articles (array):
			relação de artigos; ou vazio

	'''
	artigos = []
	msg = ''
	filtro = {}
	
	try:
		#// se recebido param publishedAt, inclui no filtro
		if publishedAt != '':
			filtro['publishedAt'] = {'$gt': publishedAt}
		
		#// se recebido param id, inclui no filtro
		if id != '':
			wid = ObjectId(id)
			filtro['_id'] = wid
			#filtro['id'] = id

		#// pesquisa		
		for item in col.find( filtro, #{'publishedAt' : {'$gt': publishedAt} , '_id': wid} , 
									limit= limite , 
							        sort= [('publishedAt', -1)] ): #).sort('publishedAt'):
			item['id'] = str( item['_id'])  # TODO: transformar ObjectID em str na classe (?fn helper)
			##delattr(item, '_id')
			del item['_id']
			#item['id'] = str( item.pop('_id'))

			artigos.append( item)  #Artigo(**user))
	 		#artigos.append( Artigo( **item))

		if len(artigos) < 1:
			raise ValueError(msgErro + 'Nada encontrado.')

		msg = msgOk
		sucesso = True

	except Exception as e:
		msg = msgErro + 'Ao pesquisar os dados.' if not emDebug else str(e)
		sucesso = False
		
	return sucesso, { 'qtde': len(artigos) , 'msg': msg , 'articles': artigos }


async def inclui_article(artigo):
	'''
	inclui um novo artigo no db
	
	Params
	-------
	- artigo (dict):
		- featured (bool)
		- title (str)	
		- url (str)		
		- imageUrl (str)		
		- newsSite (str)		
		- summary (str)		
		- publishedAt (str)
		- launches (list)
			- id: str 
			- provider: str
		- events (list)
			- id: str 
			- provider: str
		
	Returns
	-------
	- sucesso (bool)
		True/False se conseguiu

	- retorno (dict)
		- msg (str):
			mensagem de sucesso ou erro

		- id (str):
			id inserido

	'''
	try:
		#// doc a incluir não deve ter id ou _id (é criado no db); remove se existir
		if hasattr(artigo, 'id'):  delattr(artigo, 'id')
		if hasattr(artigo,'_id'):  delattr(artigo,'_id')

		#// (opcional) sugere data e hora atual, se publishedAt vazio
		if not artigo.publishedAt: 
			artigo.publishedAt = Agora()

		#// salvar e testes
		ret = col.insert_one( artigo.dict( by_alias= True))

		if not ret.acknowledged:
 			raise ValueError(msgErro + 'Nada inserido.')

		id = str(ret.inserted_id)
		msg = msgOk
		sucesso = True

	except Exception as e:
		id = ''
		msg = msgErro + 'Ao inserir os dados.' if not emDebug else str(e)
		sucesso = False

	return sucesso, { 'id': id , 'msg': msg }


async def atualiza_article(id, artigo):
	'''
	salva alterações de um artigo no db
	
	Params
	-------
	- id (str):
		id do artigo a ser atualizado

	- artigo (dict):
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
	- sucesso (bool)
		True/False se conseguiu

	- retorno (dict)
		- msg (str):
			mensagem de sucesso ou erro
	
		- id (str):
			id atualizado (mesmo)

	'''

	try:
		#artigo = artigo.dict()
		#// (opcional) atualiza publishedAt com data e hora atual
		artigo.publishedAt = Agora()

		#// usa o id que vêm na url
		oid = ObjectId(id)

		#// remove se existir para evitar conflito de atualização no db; usa o id que vêm na url
		if hasattr(artigo, 'id'):  delattr(artigo, 'id')
		if hasattr(artigo,'_id'):  delattr(artigo,'_id')

		#// salva
		ret = col.update_one({ '_id': oid } , { '$set': artigo.dict( by_alias= True) })

		#// testes
		if ret.matched_count < 1:
			raise ValueError(msgErro + 'Id não encontrado.')

		if ret.modified_count < 1:
			raise ValueError(msgErro + 'Nada modificado.')

		msg = msgOk
		sucesso = True

	except Exception as e:
		id = ''
		msg = msgErro + 'Ao atualizar os dados.' if not emDebug else str(e)
		sucesso = False

	return sucesso, { 'id': id , 'msg': msg } 


async def remove_article(id: str):
	'''
	remove artigo do db
	
	Params (url)
	-------
	- id (str):
		id do artigo a ser removido


	Returns
	-------
	- sucesso (bool)
		True/False se conseguiu

	- retorno (dict)
		- msg (str):
			mensagem de sucesso ou erro
	
		- id (str):
			id removido (mesmo)

	'''
	try:
		#// exclui
		ret = col.delete_one({ '_id': ObjectId(id) })

		#// teste
		if ret.deleted_count < 1:
			raise ValueError(msgErro + 'Nada removido.')

		msg = msgOk
		sucesso = True

	except Exception as e:
		id = ''
		msg = msgErro + 'Ao remover o artigo.' if not emDebug else str(e)
		
		sucesso = False

	return sucesso, { 'id': id , 'msg': msg }
