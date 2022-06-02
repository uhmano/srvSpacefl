#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
test_srvSpacefl
testes 


# histórico
2022-06-01 	v.1
2022-05-31 	primeira versão


# executar
pytest --tb=short -v --maxfail=1 testes/test_srvSpacefl.py

'''
import requests

URLBASE = 'http://localhost:8000/'

# variáveis entre testes
testeId = ''

testeItem = {
	"title": "ARTIGO pyTEST",
	"featured": False,
	"url": "",
	"imageUrl": "",
	"newsSite": None,
	"summary": "teste automatizado, será excluído",
	"publishedAt": None
}

# header para request; alguns ambientes podem exigir
headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20191022 Firefox/70.0', # AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'utf-8,ISO-8859-1;q=0.7,*;q=0.3',
			'Accept-Language': 'pt-BR,en-US,en;q=0.8'
			#, 'Accept-Encoding': 'none',
			}


def test_status():
	'''ep status (raiz)'''
	headers["Content-Type"] = 'text/html'

	req = requests.get(URLBASE, headers=headers)

	print ('req.status_code:', req.status_code)
	assert req.status_code == 200

	print ('req.text:', req.text)
	assert 'Back-end Challenge 2022 - Space Flight News' in req.text


def test_post():
	'''teste de incluir um artigo (post)'''
	global testeId, testeItem
	headers["Content-Type"] = 'application/json'

	# busca id
	req = requests.post(f'{URLBASE}articles/', headers= headers, json= testeItem)
	 
	print ('req.status_code:', req.status_code)
	assert req.status_code == 200

	# se não vier um json correto, ocorrerá erro, que vale como teste também
	retJson = req.json()

	# útil para os próximos testes
	testeId = retJson['id']


def test_busca_artigos():
	'''teste de busca de vários artigos'''
	headers["Content-Type"] = 'application/json'

	# busca geral
	req = requests.get(f'{URLBASE}articles/', headers= headers, params= { 'limite' : 3 })
	 
	print ('req.status_code:', req.status_code)
	assert req.status_code == 200

	retJson = req.json()
	id = retJson.get('articles')[0].get('id', None)
	
	print ('retJson:', retJson)
	assert isinstance(id, str)


def test_busca_por_id():
	'''teste de busca por id'''
	global testeId
	headers["Content-Type"] = 'application/json'

	# busca id
	req = requests.get(f'{URLBASE}articles/{testeId}', headers= headers)
	 
	print ('req.status_code:', req.status_code)
	assert req.status_code == 200

	retJson = req.json()
	idnovo = retJson.get('articles')[0].get('id', None)
	
	assert idnovo == testeId


def test_put():
	'''teste de alterar um artigo (put)'''
	global testeId, testeItem
	headers["Content-Type"] = 'application/json'
	
	testeItem['title'] = 'ARTIGO pyTEST - modificado'

	# modifica
	req = requests.put(f'{URLBASE}articles/{testeId}', headers= headers, json= testeItem)
	 
	print ('req.status_code:', req.status_code, req.text)
	assert req.status_code == 200


def test_delete():
	'''teste de excluir um artigo (delete)'''
	global testeId
	headers["Content-Type"] = 'application/json'
	
	# exclui
	req = requests.delete(f'{URLBASE}articles/{testeId}', headers= headers)
	 
	print ('req.status_code:', req.status_code, req.text)
	assert req.status_code == 200
