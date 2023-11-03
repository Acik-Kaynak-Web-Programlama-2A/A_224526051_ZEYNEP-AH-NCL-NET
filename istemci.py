import os
import tkinter as tk
from tkinter import Tk, Text, Entry, Button, filedialog


from socket import *
from threading import *

client = socket(AF_INET, SOCK_STREAM)

ip = '10.100.5.103'
port = 6666

client.connect((ip,port))

pencere = Tk()
pencere.title("Bağlandı : "   +ip      +" "      + str(port))

message = Text(pencere, width=50)
message.grid(row=0,column=0, 
             padx=10, pady=10)

mesaj_giris= Entry(pencere, width=50)
mesaj_giris.insert(0, "Adınız")

mesaj_giris.grid(row=1, column=0, 
                 padx=10, pady=10)
mesaj_giris.focus()
mesaj_giris.selection_range(0, tk.END)

def mesaj_gonder():
    istemci_mesaji = mesaj_giris.get()
    message.insert(tk.END, '\n' + 'Sen :' + istemci_mesaji)
    client.send(istemci_mesaji.encode('utf8'))
    mesaj_giris.delete(0, tk.END)
    
btn_msg_gonder = Button(pencere, text='Gönder',
                        width=30, 
                        command=mesaj_gonder)
btn_msg_gonder.grid(row=2, column=0, 
                    padx=10, pady=10)
mesaj_giris.bind("<Return>", lambda event=None: btn_msg_gonder.invoke())
def dosya_gonder():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        client.send(f"SEND_FILE:{file_name}".encode('utf8'))
        with open(file_path, 'rb') as file:
            file_data = file.read(1024)
            while file_data:
                client.send(file_data)
                file_data = file.read(1024)

btn_gozat = Button(pencere, text='Gözat', width=30, command=dosya_gonder)
btn_gozat.grid(row=2, column=1, padx=10, pady=10)



def gelen_mesaj_kontrol():
    while True:
        server_msg=client.recv(1024).decode('utf8') 
        message.insert(tk.END, '\n'+ server_msg)
        
recv_kontrol = Thread(target=gelen_mesaj_kontrol)
recv_kontrol.daemon = True
recv_kontrol.start()
pencere.mainloop()