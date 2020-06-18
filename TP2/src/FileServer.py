

import socket
import threading
import os
import psutil
import time
import statistics

class FileServer :


    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.rx_array = []
        self.rx_median = 0
        self.tx_array = []
        self.tx_median = 0
        l = threading.Thread(target=self.control_thread)

    def listen_connections(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind(('',self.port))
        #self.sock.setblocking(False)
        #self.sock.settimeout(5)
        

        while True:
            print("Waiting for requests")
            data, addr = self.sock.recvfrom(1024)
            request = data.decode()
            if request == "Browse":
                self.browse(addr)
            elif request == "Download":
                self.download(addr)
            elif request == "Control":
                pass
                #Control information -> server load balance
            else:
                print("Received unknown request")
            

    """
        Send file to client
    """
    def download(self, address):
        filename = self.sock.recv(1024).decode()

        if os.path.isfile(filename):
            filesize = os.path.getsize(filename)
            print("File size:",filesize)
            # Dizer que o ficheiro existe
            self.sock.sendto(bytes("OK","UTF-8"), address)
            # Dizer o seu tamanho
            self.sock.sendto(filesize.to_bytes(99, byteorder='big'),address)

            with open(filename,'rb') as f:
                _bytes = f.read(1024)
                self.sock.sendto(_bytes,address)
                while _bytes != b'':
                    _bytes = f.read(1024)
                    self.sock.sendto(_bytes,address)
        else:
            self.sock.sendto(bytes("FAILED - NO FILE","UTF-8"),address)

    """
        Send file list to client
    """
    def browse(self, address):
        
        directory = self.sock.recv(1024).decode()
        
        if directory != "":
            print("Diretoria:",directory)
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]
        else:
            files = [f for f in os.listdir() if os.path.isfile(f)]
        
        print("Only files",files)

        join_files = "!".join(files)
        self.sock.sendto(bytes(join_files,'UTF-8'), address)
        

    def control(self,address):
        cpu_usage = psutil.cpu_percent()
        
        msg = str(rx_median) + "-" + str(tx_median) + "-" + str(cpu_usage)
        print("Sending",msg)
        self.sock.sendto(bytes(msg,"UTF-8"), address)


    def control_thread(self):
        while True:

            rx, tx = get_network_bytes('wlp3s0')
            time.sleep(60)

            #stats
            rx1, tx1 = get_network_bytes('wlp3s0')
            rx_diff = (rx1 - rx) / 60
            tx_diff = (tx1 - tx) / 60
            self.rx_array.append(rx_diff)
            self.tx_array.append(tx_diff)
            self.rx_median = statistics.median(self.rx_array)
            self.tx_median = statistics.median(self.tx_array)

            time.sleep(300) #sleep 5 min then count again

    def get_network_bytes(self,interface):
        for line in open('/proc/net/dev','r'):
            if interface in line:
                data = line.split('%s:' & interface)[1].split()
                rx_bytes, tx_bytes = (data[0],data[8])
                return (int(rx_bytes),int(tx_bytes))
        


if __name__ == "__main__":
    f = FileServer('127.0.0.1',5000)
    f.listen_connections()