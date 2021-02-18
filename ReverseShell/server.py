# esse conectara ao servidor

import socket  # necessaria para a conversar com outro pc
import sys


# Criando um Socket para se conectar a outro Computador
def create_socket():
    try:
        global host
        global port
        global s

        host = ''
        port = 9999  # por aqui que o pc identifica que tipo de data esta vindo (evite usar portas conhecidas)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
    except socket.error as error_msg:
        print(f"Erro na criação do socket: {error_msg}")


# Mandando o socket para a porta e esperando a conexão com o cliente
def init_socket():
    try:
        global host
        global port
        global s
        print(f"Socket na porta: {str(port)}")
        s.bind((host, port))
        s.listen(5)  # numero de bad connections que o servidor pega apos recusar
    except socket.error as error_msg_2:
        print(f"Erro na ligação do socket: {error_msg_2}\n")
        print("Tentando de novo...")
        init_socket()


# Aceitando conexões com o client (socket deve estar ligado)
def socket_accepted():
        connection, address = s.accept()
        print(f"Conexão Estabelecida\nIP: {address[0]}\nPort: {str(address[1])}")
        send_commands(connection)
        connection.close()


# os caracteres q voce manda = string
# os caracteres que a cmd entende = bytes
# por isso é necessário encode e decode
def send_commands(connection):
    while True:
        cmd = input()
        if cmd == 'quit':
            connection.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0: # checando se a mensagem é maior que 0 caracteres, pois
            # se o user escrever e nao digitar nada e mandar, o servidor nao precisa enviar a mensagem.
            # Assim evitamops trafego desnecessário
            connection.send(str.encode(cmd))
            try:
                client_response = str(connection.recv(1024), 'utf-8') # conversao> 1024 tamanho dos dados
                print(client_response, end="") # end automaticamente nos da uma nova linha apos ter digitado um comando
            except UnicodeDecodeError as u:
                print(u)
                pass

def master():
    create_socket()
    init_socket()
    socket_accepted()

master()