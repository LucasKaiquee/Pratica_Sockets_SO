import socket
from pathlib import Path

HOST = '127.0.0.1'
PORT = 5000

servidor = (HOST, PORT)

print('=== Cliente ===')

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def menu():
    print("Menu:")
    print("1 - Mostrar conteúdo do diretório")
    print("2 - Criar diretório")
    print("3 - Excluir diretório")
    print("4 - Mostrar arquivo")

def trata_opcoes(opcao_digitada):
    # 1 /tmp
    valores = opcao_digitada.split()
    opcao = valores[0]
    caminho = valores[1]

    # LERDIR:/tmp/
    # CRIARDIR:/tmp/eu
    # EXCLUIRDIR:/tmp/eu
    # MOSTRAR:/tmp/eu/proxima_prova.txt

    msg = ''
    # Realiza a ação correspondente à opção do usuário
    if opcao == "1":
        # Mostra o conteúdo do diretório atual
        msg = 'LERDIR:' + caminho
    elif opcao == "2":
        # Cria um novo diretório
        msg = 'CRIARDIR:' + caminho
    elif opcao == "3":
        # Exclui um diretório
        msg = 'EXCLUIRDIR:' + caminho
    elif opcao == "4":
        # Mostra o conteúdo de um arquivo
        msg = 'MOSTRAR:' + caminho
    return msg

while True:
    menu()
    opcao = input('')
    msg = trata_opcoes(opcao)
    udp.sendto(msg.encode(encoding="utf-8"), servidor)
    resposta_servidor, s = udp.recvfrom(1024)
    print(resposta_servidor.decode(encoding='utf-8', errors='backslashreplace'))
