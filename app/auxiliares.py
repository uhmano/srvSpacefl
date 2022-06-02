'''
auxiliares
funções comuns


# histórico
2022-06-01 	v.1
2022-05-31 	primeira versão

'''
from datetime import datetime

#// mensagens mais simpáticas
msgOk   = '[ok]'
msgErro = '[erro] '


def Agora():
	'''
	retorna data e hora atual, uso como sugestão se publishedAt vazio
	''' 
	return datetime.now().isoformat()


def envia_email(para, assunto, conteudo, emTexto = True):
	'''
	envia email via smtp
	uso simples, melhorar por segurança se necessário

	uso:
		envia_email('enderecoEmail', 'assunto', 'conteudo', emTexto = True)
	'''
	import smtplib, ssl
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.header import Header

	from cfg import SMTP_TO, SMTP_USER, SMTP_PASS, SMTP_SERVER, SMTP_DOOR, SMTP_FROM


	if not para:
		para = SMTP_TO

	msg = MIMEMultipart('alternative')
	msg['From'] = SMTP_FROM
	msg['To'] = para
	msg['Subject'] = Header(assunto, 'utf-8')

	tipo = 'plain' if emTexto else 'html'

	try:
		msg.attach(MIMEText(conteudo, tipo, 'utf-8'))
		
		context = ssl.create_default_context()

		smtpserver = smtplib.SMTP(SMTP_SERVER, port= SMTP_DOOR)
		smtpserver.starttls(context= context)
		smtpserver.login(SMTP_USER, SMTP_PASS)

		smtpserver.sendmail(msg['From'], msg['To'], msg.as_string())

		smtpserver.close()

		ret = msgOk

	except Exception as e:
		ret = msgErro + str(e)

	return ret

