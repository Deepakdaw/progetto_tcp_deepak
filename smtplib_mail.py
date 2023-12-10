import smtplib as smtp
from datetime import datetime

def invia_mail():
    tempo = datetime.now()
    data = tempo.date()
    ora = tempo.time()
    oggetto_mail = "Subject: Tupla Eliminata dal DataBase\n\n"
    contenuto_mail= f"Un utente ha eliminato una tupla da un database.\n DATA ELIMINAZIONE:{data}\n ORA ELIMINAZIONE:{ora}"

    messaggio= str(oggetto_mail+contenuto_mail)

    mail_server= "smtp.gmail.com"
    port_mail_server= 587

    mail= "personal email" #mail mittente
    password= "password per applicazione 'Python'" #password mittente 
    destination_email= "personbal email 2" #mail destinatario

    email= smtp.SMTP(mail_server, port_mail_server)

    email.ehlo()

    email.starttls()

    email.login(mail, password)

    email.sendmail(mail, destination_email, messaggio)

    email.quit()
if __name__ == "__main__":
    invia_mail()
