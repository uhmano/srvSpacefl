'''
app.cfg
configs para uso do sistema


# histórico
2022-06-01 	v.1

'''

#// debug| mensagens de erro detalhadas  (False = em produção)
emDebug = False

#// atualização| filtra docs apartir desta data; não encher sem necessidade o db destino (None = todos)
UPD_MIN_PUBLISHEDAT = '2022-01-01'

#// atualização| quantos docs por vez são buscados: evitar sobrecarga, e um possível bloqueio na origem  (None = sem limite)
UPD_LOTE_LIMITE = 2

#// atualização| tempo para pedir um novo lote de registros na origem  (0 = imediato)
UPD_LOTE_SEGS = 3


#// mongoDB| dados de acesso ao db
DB_MONGO_USUARIO = '<CONFIGURAR>'
DB_MONGO_PASS 	 = '<CONFIGURAR>'
DB_MONGO_DB 	 = '<CONFIGURAR>'
DB_MONGO_COL 	 = '<CONFIGURAR>'

#// mongoDB| string de conexão
#//		direto com nome e senha, ou no formato: 
#//		'mongodb+srv://{USUARIO}:{PASS}@clusterunico.m7hqtic.mongodb.net/?retryWrites=true&w=majority'
DB_MONGO_URL 	 = '<CONFIGURAR>'


#// -- (OPÇÃO): variáveis de ambiente  --
#from os import environ as environ
#
# # mongoDB| dados de acesso ao db
# DB_MONGO_USUARIO = environ.get('DB_MONGO_USUARIO', '')
# DB_MONGO_PASS    = environ.get('DB_MONGO_PASS', '')
# DB_MONGO_DB 	   = environ.get('DB_MONGO_DB', 'spacefl')
# DB_MONGO_COL 	   = 'articles'

# # mongoDB| string de conexão
# #		direto com nome e senha, ou no formato: 
# #		'mongodb+srv://{USUARIO}:{PASS}@clusterunico.m7hqtic.mongodb.net/?retryWrites=true&w=majority'
# DB_MONGO_URL 	 = environ.get('DB_MONGO_URL', '') .format(USUARIO= DB_MONGO_USUARIO, PASS= DB_MONGO_PASS)


#// SMTP| envio de email de alerta
SMTP_TO     = '<CONFIGURAR>'
SMTP_FROM   = '<CONFIGURAR>'
SMTP_USER   = '<CONFIGURAR>'
SMTP_PASS   = '<CONFIGURAR>'
SMTP_SERVER = '<CONFIGURAR>'
SMTP_DOOR   = 587
