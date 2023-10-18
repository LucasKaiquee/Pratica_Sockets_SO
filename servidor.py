import socket
from pathlib import Path

HOST = '127.0.0.1'
PORT = 5000

print('=== Servidor ===')

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)

path = Path('/tmp')

if not path.exists():
    path.mkdir()

udp.bind(orig)

def trata_opcoes(msg):
    # 1 /tmp
    valores = msg.split(sep=':')
    operacao = valores[0]
    caminho = valores[1]

    msg = ''

    if operacao == "LERDIR":
        # Mostra o conteúdo do diretório atual
        print('LERDIR:' + caminho)
        lerCaminho = path / caminho
        try:
            for arquivo in lerCaminho.iterdir():
                msg = f'Conteúdo: {arquivo}'
        except FileNotFoundError:
            msg = f'O diretório {caminho} não foi encontrado.'

    elif operacao == "CRIARDIR":
        # Cria um novo diretório
        novoCaminho = path / caminho
        try:
            novoCaminho.mkdir()
            msg = f'Diretório {novoCaminho} foi criado com sucesso.'
        except FileExistsError:
            msg = f'O diretório {novoCaminho} já existe.'

    elif operacao == "EXCLUIRDIR":
        # Exclui um diretório
        excluirCaminho = path / caminho
        try:
            excluirCaminho.rmdir()
            msg = f'Diretório {excluirCaminho} foi excluído com sucesso.'
        except FileNotFoundError:
            msg = f'O diretório {excluirCaminho} não foi encontrado.'
       
    elif operacao == "MOSTRAR":
        # Mostra o conteúdo de um arquivo
        mostrarArquivo = path / caminho

        if mostrarArquivo.exists() and mostrarArquivo.is_file():
            with open(mostrarArquivo, 'r') as arquivo:
                conteudo = arquivo.read()
                msg = f'Conteúdo do arquivo {mostrarArquivo}: \n {conteudo}'
        else:
            msg = f'O arquivo {mostrarArquivo} não existe ou não é um arquivo.'

    return msg

while True:
    msg, cliente = udp.recvfrom(1024)
    print('Recebi de', cliente, 'a mensagem', msg.decode(encoding="utf-8"))

    returnMsg = trata_opcoes(msg.decode())
    udp.sendto(returnMsg.encode(encoding=('utf-8')), cliente)
    
    # mini protocolo
    # LERDIR:/tmp/
    # CRIARDIR:/tmp/eu
    # EXCLUIRDIR:/tmp/eu
    # MOSTRAR:/tmp/eu/proxima_prova.txt

    # resposta = 'mensagem recebida com sucesso!'
    # udp.sendto(resposta.encode(), cliente)
    print('Resposta enviada!')
