#coding:utf-8
from socket import *
import sys
import os

#função

def extensao(arquivo):
	ext = ''
	if (arquivo == '.txt'):
		ext = 'Content-Type: text/plain\r\n'
	elif (arquivo == '.png'):
		ext = 'Content-Type: image/png\r\n'
	elif (arquivo == '.html'):
		ext = 'Content-Type: text/html\r\n'

	return ext

porta = 8000
socket = socket(AF_INET, SOCK_STREAM)
socket.bind(('', porta))
socket.listen(1)

print ('http://localhost:{}/'.format(porta) + 'está recebendo...')


while True:
	conexao, endereco = socket.accept()
	linha =conexao.recv(1024).decode('utf-8').split(' ')
	metodo = linha[0]
	caminho = linha[1]
	versao = linha[2].split('\r\n')[0]
	cabecalho = ''

	try:
		if (caminho == '/'):
			caminho = '/index.html'


		arquivo = open('.' + caminho, 'rb')
		leitura = arquivo.read()
		arquivo.close()
		cabecalho = '{} 200 OK\r\n'.format(versao)
		nome, arquivo = os.path.splitext(caminho)
		ext = extensao(arquivo)
		cabecalho += ext

		envio = cabecalho.encode('utf-8') + '\r\n'.encode('utf-8') + leitura + "\r\n".encode('utf-8')
		print('{} {} - {} 200 OK'.format(metodo, caminho, nome))
		conexao.send(envio)


	except:


		cabecalho = '{} 404 NOT FOUND\r\n'.format(versao)
		print('{} {} - 404 NOT FOUND'.format(metodo, caminho))
		error = 'Arquivo ' + caminho + ' nao encontrado.'
		conexao.send(error.encode('utf-8'))


	conexao.close()



