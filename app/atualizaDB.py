#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
atualizaDB
atualiza banco de dados apartir de artigos em api.spaceflightnewsapi.net

O schema Artigo não têm necessidade de uso: 
	simplemente json original > adaptação mínima > json enviado para o destino MongoDB

Se as bases ficarem no futuro com uma estrutura diferente, mudar aqui.


# histórico
2022-06-01 	v.1
2022-05-30 	primeira versão

'''
import requests
from time import sleep

from auxiliares import msgErro, envia_email, Agora

#// configs
from cfg import UPD_MIN_PUBLISHEDAT, UPD_LOTE_LIMITE, UPD_LOTE_SEGS

#// modelo
#from modelo import Artigo

#// dados
from conexaoDB import fb_col
db, col = fb_col()

#// origem dos artigos
urlORIGEM = 'https://api.spaceflightnewsapi.net/v3/articles/'

#// algum log
import logging
logging.basicConfig(filename= 'atualizaDB.log', filemode= 'a', format= '%(asctime)s  %(levelname)s:  %(message)s')


def log(msg):
	logging.warning(msg)
	print(msg)


def ult_publishedAt():
	'''
	retorna maior publishedAt nos artigos no db
	objetivo: executar atualização apartir deste
	'''
	try:
		filtro = { 'id_original' : { "$ne": None } }  # importante aqui: docs incluídos manualmente têm id_original None - filtrar
		doc = col.find( filtro, limit= 1 , sort= [('publishedAt', -1)] )[0]
	
		return doc['publishedAt']
	
	except:
		return ''


def atualiza_db():
	'''
	atualiza db mongoDB, lendo origem
	'''
	global urlORIGEM
	
	#// cria filtro e adiciona parâmetros (se tiverem valor)
	payload = {
		'_sort': 'publishedAt'
	}
	if UPD_LOTE_LIMITE: 
		payload['_limit']         = UPD_LOTE_LIMITE
	
	#// maior publishedAt no db: executar atualização apartir desta
	apartir = ult_publishedAt()
	
	#// precedências para buscar dados via publishedAt: 
	#// 	acima do último no banco > UPD_MIN_PUBLISHEDAT > todos os docs
	if (not apartir) and (UPD_MIN_PUBLISHEDAT):
		apartir = UPD_MIN_PUBLISHEDAT

	# útil para ver no container; outros print()'s idem
	log(f'apartir antes: {apartir}')  
	qtdeProc = 0

	while True:
		payload['publishedAt_gt'] = apartir
		
		try:		

			#// buscar lista
			r = requests.get(urlORIGEM, params= payload)

			if not (200 <= r.status_code <= 299): 
				raise Exception('Erro ao buscar dados @API origem.')
		
			lista = r.json()
			tamLista = len(lista)

			#// lote vazio: encerra
			if tamLista < 1:
				break

			#// processa
			listaInserir(lista)

		except Exception as e:
			#// erro na atualização
			msg = msgErro + 'Atualização do Banco de Dados Mongo'
			envia_email(None, msg, str(e))

			log(f'{msg} {str(e)}')
			break

		#// aguarda alguns segundos antes de pedir o próx.lote - evitar bloqueios na origem
		sleep(UPD_LOTE_SEGS)

		#// próximo: seguinte apartir do último do lote atual
		apartir = lista[tamLista -1]['publishedAt']
		
		qtdeProc += tamLista


	log(f'processados: {qtdeProc}')
	log(f'apartir depois: apartir')


def listaInserir(lista):
	'''salva lista no db, e atualiza doc controle
	returna qtde de registros inseridos
	'''
	global col
	ultimo = ''
	qtde = 0
	
	for item in lista:
		
		#// no artigo original, guarda 'id' original em 'id_original': novo _id é gerado no mongoDB
		if ('id' in item.keys()):
			item['id_original'] = item.pop('id', None)
		
		#// insere
		col.insert_one(item)
		
		ultimo = max(ultimo, item['publishedAt'])
		qtde += 1
	
	return qtde


if __name__ == '__main__':
	'''executar apartir da cli'''
	log(f'-- iniciando atualização: {Agora()} --')

	atualiza_db()

	log(f'-- fim da atualização: {Agora()} --')
