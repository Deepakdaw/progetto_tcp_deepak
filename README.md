# Progetto Server Python con Connessione a MySQL

## Descrizione

Questo progetto è un server Python che si connette a un database MySQL. Il server è progettato per gestire le operazioni di base come creare, leggere, aggiornare ed eliminare (CRUD) dati nel database.
progetto_server.py: Il file principale che avvia il server e gestisce le connessioni dei client.
progetto_client.py: Contengono funzioni per eseguire operazioni specifiche sul database, come creazione, lettura, aggiornamento ed eliminazione.

## Requisiti

- Python 3.x
- MySQL Server installato e in esecuzione

## Configurazione

1. Installa le dipendenze Python eseguendo il seguente comando:

   ```bash
   pip install mysql-connector-python

Installa le dipendenze Python eseguendo il seguente comando:
 
Configura le informazioni di connessione al database nel file progetto_server.py. Modifica le variabili seguenti con le tue credenziali e dettagli del database:
  ```python
import mysql.connector
host = "127.0.0.1"
user = "root"
password = "la_tua_password"
database = "il_tuo_database"

## License

[MIT](https://choosealicense.com/licenses/mit/)
