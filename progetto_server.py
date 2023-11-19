import socket
import mysql.connector
import pickle
import threading as th  





def db_colonne(cur, nome):

    cur.execute(f"DESCRIBE {nome}")

    colonna = [column[0] for column in cur.fetchall()]
    return colonna

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def db_update(cur, conn, tab, att, n, id, val):

    id_str = ", ".join(id)
    query = f"UPDATE {tab} SET {att} = %s WHERE {id_str} = %s"   #escape
    cur.execute(query, (n, val))
    conn.commit()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def db_read(cur,att, tab):

    att_str = ", ".join(att)
    query = f"SELECT {att_str} FROM {tab}"
    cur.execute(query)
    dati = cur.fetchall()
    return dati


 #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def update_id_dopo_delete(cur, conn, tab, att):


    att_str = ', '.join(att)
    query_select = f"SELECT {att_str} FROM {tab} ORDER BY {att_str} ASC"
    cur.execute(query_select)
    id_values = [b[0] for b in cur.fetchall()]

    for i, id_value in enumerate(id_values, start=1):    #i = iterazione       id_value= valore nella lista id
        update_query = f"UPDATE {tab} SET {att_str} = %s WHERE {att_str} = %s"   #escape
        cur.execute(update_query, (i, id_value))

    conn.commit()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def db_create(cur,conn,tab, valori):

    lista_valori = ','.join(['%s'] * len(valori))

    query = f"INSERT INTO {tab} VALUES ({lista_valori})"

    cur.execute(query, valori)
    conn.commit()



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def db_delete(cur, conn, att, tab, temp):

    temp_str = ', '.join(temp)
    query = f"DELETE FROM {tab} WHERE {temp_str} = %s" #escape
    cur.execute(query, (att,))
    conn.commit()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def richiesta(cur):
    cur.execute("SHOW TABLES LIKE '%_deepak_dawlehar'")
    dati = cur.fetchall()
    return [dati[0] for dati in dati]

#USARLO A SCUOLA PER VEDERE SOLO LE TABELLE FATTE DA ME
"""
def richiesta(cur):
    cur.execute("SHOW TABLES")
    dati = cur.fetchall()
    return [dati[0] for dati in dati]
"""
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

def gestione_comunicazione(lista_conn,z,lock, tabelle, ins, i):
    while(i<3 and ins != PASSWORD):
        dati = "inserisci password, " + str(3-i) + " tentativi rimasti"
        lista_conn[z][0].send(dati.encode())
        i+=1
        ins = lista_conn[z][0].recv(1024).decode()

    if(ins == PASSWORD):
        lista_conn[z][0].send("password corretta inizia la comunicazione".encode())
    else:
        lista_conn[z][0].send("tentativi massimi raggiunti. Chiudo la connessione".encode())
        lista_conn[z][0].close()
        print("Connection Closed",lista_conn[z][1])
        exit()
    
    while True:
        tabelle = richiesta(cur)
        tabelle_byte = list_to_bytes(tabelle)
        lista_conn[z][0].send(tabelle_byte)
        lista_conn[z][0].send("Con quale tabella vuoi lavorare: ".encode())
        tab = lista_conn[z][0].recv(1024).decode()
        print(tab)
        colonne = db_colonne(cur,str(tab))
        colonne_byte = list_to_bytes(colonne)
        lista_conn[z][0].send(colonne_byte)
        print(lista_conn[z][0].recv(1024).decode())
        menu = "Cosa vuoi fare?\n1. Creare\n2. Leggere\n3. Modificare\n4. Eliminare\nScelta: "
        lista_conn[z][0].send(menu.encode())
        data = lista_conn[z][0].recv(1024)
        scelta = int(data)
        temp = []
        temp.append("id")
        fk = db_read(cur,temp, "dipendenti_deepak_dawlehar")
        fk2 = [elemento[0] for elemento in fk]
        valore = []
        temp = []
        print("HAI SCELTO: ", scelta)
        if scelta == 1:
            lock.acquire()
            lista_conn[z][0].send(list_to_bytes(fk2))
            for i in colonne:
                temp.append(str(colonne[0]))
                temp1 = db_read(cur,temp, str(tab))
                temp2 = [elemento[0] for elemento in temp1]
                temp2.sort()
                temp1 = len(temp2)-1 
                if i == "id" or i == "id_zona": 
                    valore.append((temp2[temp1]+1))
                    print(temp2[temp1]+1)
                else: 
                    riga = f"inserire un valore nell'attributo {i}"
                    lista_conn[z][0].send(riga.encode())
                    valore.append(lista_conn[z][0].recv(1024).decode())  
            db_create(cur,conn_sql,str(tab),valore)
            lista_conn[z][0].send("CREAZIONE AVVENUTA CORRETTAMENTE".encode())
            lista_conn[z][0].close()
            lock.release()
            return 0
        elif scelta == 2:
            lista_conn[z][0].send("Inserire gli attributi da visualizzare( UNO alla volta) : ".encode())
            attributi = lista_conn[z][0].recv(1024)
            attributi = bytes_to_list(attributi)
            lettura = db_read(cur,attributi, str(tab))
            lista_conn[z][0].send(list_to_bytes(lettura))
            lista_conn[z][0].close()
            return 0
        elif scelta == 3:
            lock.acquire()
            lettura = db_read(cur,colonne, str(tab))
            lista_conn[z][0].send(list_to_bytes(lettura))
            print(lista_conn[z][0].recv(1024).decode())
            lista_conn[z][0].send("inserire l'id della tupla da modificare".encode())
            temp.append(str(colonne[0]))
            temp1 = db_read(cur,temp, str(tab))
            temp2 = [elemento[0] for elemento in temp1]
            lista_conn[z][0].send(list_to_bytes(temp2))
            l = lista_conn[z][0].recv(1024).decode()
            lista_conn[z][0].send("Inserire gli attributi da modificare( UNO alla volta) : ".encode())
            attributi = lista_conn[z][0].recv(1024)
            attributi = bytes_to_list(attributi)
            for i in attributi:
                riga = f"inserire un valore nell'attributo {i}"
                lista_conn[z][0].send(riga.encode())
                v = lista_conn[z][0].recv(1024).decode()
                print(str(tab),i,v,temp,l)
                db_update(cur,conn_sql,str(tab),i,v,temp,l)
            lista_conn[z][0].send("ENTITÀ AGGIORNATA CORRETTAMENTE".encode())
            lock.release()
            lista_conn[z][0].close()
            return 0
        elif scelta == 4:
            lock.acquire()
            lista_conn[z][0].recv(1024).decode()
            temp.append(str(colonne[0]))
            temp1 = db_read(cur,temp, str(tab))
            temp2 = [elemento[0] for elemento in temp1]
            lista_conn[z][0].send(list_to_bytes(temp2))
            lettura = db_read(cur,colonne, str(tab))
            lista_conn[z][0].send(list_to_bytes(lettura))
            lista_conn[z][0].recv(1024).decode()
            lista_conn[z][0].send("inserire l'id della tupla che vuoi eliminare: ".encode())
            data = lista_conn[z][0].recv(1024).decode()  
            db_delete(cur,conn_sql,str(data), str(tab), temp)
            update_id_dopo_delete(cur,conn_sql,str(tab),temp) 
            lista_conn[z][0].send("ENTITÀ ELIMINATA CORRETTAMENTE".encode())
            lista_conn[z][0].close()
            lock.release()
            return 0
#########################################################################################################################################################################################################


if __name__ == '__main__':

    conn_sql = mysql.connector.connect(
        host="127.0.0.1", #127.0.0.10.10.0.10
        user="root",    
        #password="dawlehar1234",
        database="dbtepsit",
        port=3306, 
        )
      
    cur = conn_sql.cursor()


    PASSWORD = "1234"
    HOST = 'localhost'                 # Nome simbolico che rappresenta il nodo locale
    PORT = 50010              # Porta non privilegiata arbitraria
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("server avviato, in ascolto...")
    lista_conn = []
    z = 0
    i = 0
    thread = []
    lock = th.Lock()
    tabelle = []
    ins = ""

    while True:
        lista_conn.append(s.accept())
        print('Connected by', lista_conn[z][1])
        thread.append(th.Thread(target=gestione_comunicazione, args = (lista_conn,z,lock, tabelle, ins, i) )) 
        thread[z].start()
        z=z+1
   






