from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    #soket üzerinden gelen mesajı yazdırmak için oluşturduk.
    while True:
        try:
            msg = client_socket.recv(bufsize).decode("utf-8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  #client sohbetten çıkarsa çalışır.
            break

def send(event = None):
    #olay bağlayıcılar tarafından iletilir
    msg = my_msg.get()
    my_msg.set("")          #mesaj girilecek kısım temizlenir.
    client_socket.send(bytes(msg, "utf-8"))
    if msg == "{çıkış}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    #Pencere kapatıldığında çağırılması gereken fonksiyon.
    my_msg.set("{çıkış}")
    send()

top = tkinter.Tk()
top.title("Chat Odası")

message_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()            #Gönderilecek mesaj için
my_msg.set("Mesajınızı buraya girin...")
scrollbar = tkinter.Scrollbar(message_frame)        #Geçmiş mesajları görebilmek için scrollbar aktif edildi.
#Aşağıdaki mesajları içerecektir.
msg_list = tkinter.Listbox(message_frame, height = 35, width = 70, yscrollcommand = scrollbar.set)
scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)
msg_list.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
msg_list.pack()
message_frame.pack()

entry_field = tkinter.Entry(top, textvariable = my_msg)
entry_field.bind("<Return>",send)
entry_field.pack()
send_button = tkinter.Button(top, text = "Gönder", command = send)
send_button.pack()


top.protocol("WM_DELETE_WINDOW", on_closing)

host = input('Host adresini girin : ')
port = input('Port numarası girin : ')

if not port :
    port = 8080
else:
    port = int(port)

bufsize = 1024
addr = (host, port)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(addr)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()