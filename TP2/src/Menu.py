import numpy as np
import sys
from threading import Thread
from Client import Client


def inputNumber(prompt):
    while True:
        try: 
            num = float(input(prompt))
            break
        except ValueError:
            pass
        
    return num



def displayMenu(items):

    for i in range(len(items)):
        print("{:d}-> {:s}".format(i+1, items[i]))
    option = 0
    while not (np.any(option == np.arange(len(items))+1)):
        print("\n")
        option = inputNumber("Escolha um item >> ")

    return option

if __name__ == "__main__":
    cliente = Client()
    menuItems = np.array(["Verificar ficheiros","Download de um ficheiro"])
    
    while True:
        print("\n")
        #Display Menu
        option = displayMenu(menuItems)

        #Connect
        if option == 1:
            cliente.browse()
        #Show_Content
        elif option == 2:
            cliente.download()
        else :
            print("Opção desconhecida")
        