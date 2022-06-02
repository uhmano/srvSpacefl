# -*- coding: utf-8 -*-
'''
conexaoDB.py
lê config, cria objetos de conexão com o banco de dados MongoDB


# histórico
2022-06-01 	v.1
2022-05-29 	primeira versão

'''

# configs
from cfg import DB_MONGO_URL, DB_MONGO_DB, DB_MONGO_COL

import pymongo


def fb_col(qualCol = DB_MONGO_COL):
	'''
	retorna objetos banco e collection; fábrica

	
	Params
	-------
	- qualCol: qual collection usar; default 'articles'
	
	Returns
	-------
	- db: pymongo.database.Database
	- col: pymongo.collection.Collection
	
	'''
	client = pymongo.MongoClient(DB_MONGO_URL)
	db = client[DB_MONGO_DB]
	col = db[qualCol]
	
	return db, col
