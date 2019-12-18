from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

                #Client-Server Asenkron Soketli Mesajlaşma Uygulaması#

host = 'localhost'
port = 8080
bufsize = 1024
ADDR = (host, port)

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)

clients = {}
addresses = {}

def accept_incoming_connections():
                                            #Bağlantı kurulumunu ayarladık.
    while True:
        client, client_address = server.accept()
        print("%s %s Bağlantı kurdu." % client_address)
        client.send(bytes("Server'ımıza hoşgeldiniz " + "Kullanıcı adınızı girip enter'a basınız...","utf-8"))
        addresses[client] = client_address

        Thread(target=handle_client, args=(client,)).start()

def broadcast(message, prefix=""):
                                        #önek tanımlamak için prefix kullandık.
                                        #Birden fazla bağlantı kurulduğunda tüm clientlara mesajın iletilmesini sağlar.
    for sock in clients:
        sock.send(bytes(prefix, "utf-8")+ message)


def handle_client(client):
                                                        #İstemci soketini argüman olarak aldık.
                                                        #Tek bir client bağlantısını yöneten kısım.
    name = client.recv(bufsize).decode("utf-8")
    welcome = 'Hoşgeldiniz %s! Çıkış yapmak için lütfen {çıkış} yazın... ' %name
    client.send(bytes(welcome,"utf-8"))
    message = "%s chat'e katıldı..." %name
    broadcast(bytes(message,"utf-8"))
    clients[client] = name
    while True:
        message = client.recv(bufsize)
        if message != bytes("{çıkış}", "utf-8"):
            broadcast(message, name+": ")
        else:
            client.send(bytes("{çıkış}","utf-8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s konuşmadan ayrıldı..." %name, "utf-8"))
            break



if __name__ == "__main__":
    server.listen(5)
    print("Bağlantı bekleniyor...")
    accept_thread = Thread(target=accept_incoming_connections())
    accept_thread.start()
    accept_thread.join()
    server.close()