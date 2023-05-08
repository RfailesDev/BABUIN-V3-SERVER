import socket

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print("IP: "+str(ip_address))
serv_sock.bind((ip_address, 8080))
serv_sock.listen(10)

while True:
    client_sock, client_addr = serv_sock.accept()
    print('Connected by', client_addr)
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        client_sock.sendall(data)

    client_sock.close()