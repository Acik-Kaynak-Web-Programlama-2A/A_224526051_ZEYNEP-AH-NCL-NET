# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 09:38:58 2023

@author: C-117
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 08:38:07 2023

@author: C-117
"""

from socket import *
from threading import *

clients =[]
names = []

def clientThread(client):
    bayrak = True 
    while True:
        try:
            message = client.recv(1024).decode("utf8")
            if bayrak:
                names.append("message")
                print(message, "bağlandı")
                bayrak = False 
                for c in clients:
                    if c != client:
                        index = clients.index(client)
                        name=names[index]
                        c.send((name +":"+ message).encode("utf8"))
        except:
                index=clients.index(client)
                clients.remove(client)
                name=names[index]
                name.remove(name)
                print(name + "çıktı")
                break
            
server = socket(AF_INET, SOCK_STREAM)

ip ='10.100.5.103'
port  = 6666
server.bind((ip, port))
server.listen()
print("Server dinlenme...")


while True:
    client, address = server.accept()
    clients.append(client)
    print("Bağlantı yapıldı...", address[0] + ":" + str(address[1]))
    thread = Thread(target=clientThread, args=(client,))
    thread.start()