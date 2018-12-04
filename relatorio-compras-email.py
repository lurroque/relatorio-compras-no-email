import MySQLdb
from mailjet_rest import Client
import schedule
import time
import os

def envia_relatorio_por_email():
    db = MySQLdb.connect(
        host = "IP do Banco",
        user = "usuario",
        passwd = "senha",
        db = "Banco"
    )

    cur = db.cursor()

    query = cur.execute(
        """SELECT * FROM COMPRAS
        WHERE data >= curdate()
        """
    )

    linhas = cur.fetchall()

    retorno = "<table border=1>"
    for linha in linhas:
        retorno += """<tr>
        <td>{}</td>
        <td>{}</td>
        </tr>""".format(linha[2], linha[3])
    retorno += "</table>"

    mailjet = Client(auth=("sua_api_key", "sua_api_secret"), version='v3')

    lista_emails = EMAILS.split(",")
    obj_inicial = []
    for email in lista_emails:
            obj_inicial.append({"Email" : email})

    data = {
    'FromEmail': 'emailqueiraenviar@qualquercoisa.com.br',
    'FromName': 'Sistema',
    'Subject': 'Título',
    'Html-Part': retorno,
    'Recipients': obj_inicial,
    }

    result = mailjet.send.create(data=data)

    db.close()

# Schedule para automatizar o envio de emails em determinado horário do dia
schedule.every().day.at("00:00").do(tarefa)

while True:
    schedule.run_pending()
    time.sleep(1)
