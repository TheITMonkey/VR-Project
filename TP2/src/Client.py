import socket
import os

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        
        self.addr = ('127.0.0.1',5000)
    
    def browse(self):
        server = input("Indique qual o servidor a utilizar: ")
        
        self.socket.sendto(bytes("Browse","UTF-8"), self.addr)

        directory = input("Introduza a diretoria a visualizar: ")

        self.socket.sendto(bytes(directory,"UTF-8"), self.addr)

        list_files = self.socket.recv(1024).decode()
        files = list_files.split('!')
        print("Present files:")
        print(files)

    def download(self):
        
        self.socket.sendto(bytes("Download","UTF-8"),self.addr)

        filepath = input("Indique o ficheiro que pretende fazer download: ")

        self.socket.sendto(bytes(filepath,'UTF-8'),self.addr)

        #Esperar que nos digam que existe ou que nao existe
        status = self.socket.recv(1024).decode()
        if status != "OK":
            print(status)
            return
        
        
        filesize = self.socket.recv(1024)
        if filesize == b"":
            print("Ficheiro vazio, cancelando")
            return

        filesize = int.from_bytes(filesize, byteorder='big')
        print("Fazendo download de um ficheiro com",filesize,"bytes")
        filename = os.path.split(filepath)[1]
        f = open(filename,'wb')
        data = self.socket.recv(1024)
        totalRecv = len(data)
        f.write(data)
        while totalRecv < filesize:
            data = self.socket.recv(4096)
            totalRecv += len(data)
            f.write(data)
            print("Almost there",totalRecv,"/",filesize)
        print("Download complete")



    