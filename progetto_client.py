import socket
import pickle
from datetime import datetime

def controlla_data(data):
    try:
        data_ris = datetime.strptime(data, '%Y-%m-%d')
        formato_corretto = data_ris.strftime('%Y-%m-%d') == data
        return formato_corretto, data_ris
    except ValueError:
        return False, None


def list_to_bytes(tabelle):
    """
    metodo per trasformare le liste in bytes prima di inviarle con l'utilizzo del metodo send
    della libreria socket
    """
    if not isinstance(tabelle, list):
        raise Exception("devi passare una lista alla funzione list_to_bytes")
    list_converted = pickle.dumps(tabelle)
    return list_converted



def bytes_to_list(data):
    """
    metodo per trasformare i bytes in liste una volta ricevute con l'utilizzo del metodo recv
    della libreria socket
    """
    if not isinstance(data, bytes):
        raise Exception("devi passare dei bytes alla funzione bytes_to_list")

    return pickle.loads(data)


HOST = 'localhost'    # Il nodo remoto, qui metti il tuo indirizzo IP per provare connessione server e client dalla tua macchina alla tua macchina
PORT = 50010             # La stessa porta usata dal server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = ""
data2 = ""


while True:
    while data != "password corretta inizia la comunicazione".encode():
        data = s.recv(1024)
        print(data.decode())
        if data == "tentativi massimi raggiunti. Chiudo la connessione".encode() :
            raise SystemExit("Connessione Chiusa")
        elif(data == "password corretta inizia la comunicazione".encode()):
            data = s.recv(1024)
            tabelle = bytes_to_list(data)
            print(s.recv(1024).decode())
            print(tabelle)
            scelta = input("")
            while scelta != tabelle[0] and scelta != tabelle[1]:
                scelta = input("inserire una tabella esistente: ")
            s.send(scelta.encode())
            colonne = s.recv(1024)
            colonne = bytes_to_list(colonne)
            print(colonne)
            s.send("colonne ricevute".encode())
            print(s.recv(1024).decode())
            scelta = int(input(""))
            while(scelta<1 and scelta >4):
                scelta = int(input("inserire una scelta valida compresa tra 1 e 4"))
            s.send(str(scelta).encode())
            lista = []

            #-------------------------------------------------------------------------------------------------------------------------------------------------------

            if scelta == 1:
                fk = bytes_to_list(s.recv(1024))
                for i in colonne:
                    print(s.recv(1024).decode())
                    data2 = input()
                    if i == "pos_lavorativa":
                        while True:
                            formato_corretto, data_ris = controlla_data(data2)
                            if formato_corretto :
                                print(f"La data {data2} è nel formato corretto.")
                                break 
                            else:
                                print(f'La data {data2} non è nel formato corretto o non è valida. Riprova.')
                                data2 = input("Inserisci una data nel formato YYYY-MM-DD: ")
                    if i == "numero_clienti":
                        while data2 not in str(fk):
                            data2 = input(f"inserire un valore della esistente della primary key\n{fk} ")
                    s.send(data2.encode())
                print(s.recv(1024).decode()) 

            #-------------------------------------------------------------------------------------------------------------------------------------------------------

            elif scelta == 2:
                testo = s.recv(1024).decode()
                print(testo)
                while(data != "x"):
                    print("per finire scrivi x")
                    data = input()
                    if data == "x": break
                    while data not in colonne or data in lista:
                        data = input(f"{data} non è un attributo esistente o è già presente nella lista\nREINSERIRE: ")
                    lista.append(data)
                s.send(list_to_bytes(lista))
                l = bytes_to_list(s.recv(1024))
                for row in l:
                    print(row,"\n")

            #-------------------------------------------------------------------------------------------------------------------------------------------------------

            elif scelta == 3:
                lettura = bytes_to_list(s.recv(1024))
                for row in lettura:
                    print(row,"\n")
                s.send("ricevuto".encode())
                print(s.recv(1024).decode())
                temp = bytes_to_list(s.recv(1024))
                l = int(input())
                while l not in temp:
                    l = int(input("inserire un valore esistente"))
                s.send(str(l).encode())
                print(colonne)
                print(s.recv(1024).decode())
                while(data != "x"):
                    print("per finire scrivi x")
                    data = input()
                    if data == "x": break
                    while data not in colonne or data in lista:
                        data = input(f"{data} non è un attributo esistente o è già presente nella lista\nREINSERIRE: ")
                    lista.append(data)
                s.send(list_to_bytes(lista))
                for i in lista:
                    print(s.recv(1024).decode())
                    print(i)
                    data = input()
                    if i == "data_assunzione":
                        while True:
                            formato_corretto, data_ris = controlla_data(data)
                            if formato_corretto :
                                print(f"La data {data} è nel formato corretto.")
                                break 
                            else:
                                print(f'La data {data} non è nel formato corretto o non è valida. Riprova.')
                                data = input("Inserisci una data nel formato YYYY-MM-DD: ")
                    s.send(data.encode())
                print(s.recv(1024).decode()) 

            #-------------------------------------------------------------------------------------------------------------------------------------------------------

            elif scelta == 4:
                s.send("ricevuto".encode())
                temp = bytes_to_list(s.recv(1024))
                temp.sort()
                lettura = bytes_to_list(s.recv(1024))
                s.send("ricevuto".encode())
                for row in lettura:
                    print(row,"\n")
                print(s.recv(1024).decode())
                print("\n",temp)
                data = int(input())
                while data not in temp:
                    data = int(input("inserire un valore esistente"))
                s.send(str(data).encode())
                print(s.recv(1024).decode())
        else:
            testo = input().encode()
            s.send(testo)
    data = s.recv(1024)
    print(data)
    s.send(input().encode())

s.close()
