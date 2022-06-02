#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
modelo
modelo de dados para o pydantic/mongoDB


# histórico
2022-06-01 	v.1
2022-05-30 	primeira versão

'''
from pydantic import BaseModel, Field #, Dict
from bson import ObjectId
from typing import Optional, List, Dict


class PyObjectId(ObjectId):
	'''
	classe auxiliar para converter de id para _id @mongoDB
	'''
	@classmethod
	def __get_validators__(cl):
		yield cl.validate

	@classmethod
	def validate(cl, v):
		if not ObjectId.is_valid(v):
			raise ValueError("Objectid inválido !")
		return ObjectId(v)

	@classmethod
	def __modify_schema__(cl, field_schema):
		field_schema.update(type="string")


class Artigo(BaseModel):
	'''
	classe-schema para validar dados recebidos via API
	'''
	id: Optional[PyObjectId] = Field(alias = '_id')
	featured    : bool = Field(False)
	title       : str  = Field(...)
	url         : str  = Field(None)
	imageUrl    : str  = Field(None)
	newsSite    : str  = Field(None)
	summary     : str  = Field(None)
	publishedAt : str  = Field(None)
	updatedAt   : str  = Field(None)
	launches    : List[ Dict[ str, str] ] = None
	events      : List[ Dict[ str, str] ] = None

