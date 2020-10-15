import sqlalchemy
from json import dumps
from httplib2 import Http
import random
import string

import smtplib

def get_random_string(length):
    # put your letters in the following string
    sample_letters = string.printable.replace(string.punctuation + string.whitespace, "")
    result = ''.join((random.choice(sample_letters) for i in range(length)))
    return result
def send_msg(msg, webhook):
    bot_message = {'text' : msg}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=webhook,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print(response)
def send_mail(dest, password):
    gmail_user = 'alan.alanson34@gmail.com'
    gmail_password = 'AlanAlanson34'

    sent_from = gmail_user
    #to = ['webhelp-asarrion@premium-cloud-support.com']
    to = [dest]
    subject = 'Test e-mail from Python'
    body = 'Today\'s password is: ' + password

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()


# Set the following variables depending on your specific
# connection name and root password from the earlier steps:
connection_name = "wave34-webhelp-vrodriguez:europe-west1:mysql"
db_password ="sirAndrew"
db_name = "improvedArrivalRegister"

db_user = "andrew"
driver_name = 'mysql+pymysql'
query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})

def main_function(thing):
    
    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
          drivername=driver_name,
          username=db_user,
          password=db_password,
          database=db_name,
          query=query_string,
      ),
      pool_size=5,
      max_overflow=2,
      pool_timeout=30,
      pool_recycle=1800
    )

    acooper_pass = get_random_string(16)
    vkoval_pass = get_random_string(16)
    malaman_pass = get_random_string(16)
    asarrion_pass = get_random_string(16)
    vrodriguez_pass = get_random_string(16)
    apau_pass = get_random_string(16)

    with db.connect() as conn:
        conn.execute("UPDATE passwords SET password=\'{}\' WHERE ldap ='acooper';".format(acooper_pass))
        conn.execute("UPDATE passwords SET password=\'{}\' WHERE ldap ='vkoval';".format(vkoval_pass))
        conn.execute("UPDATE passwords SET password=\'{}\' WHERE ldap ='malaman';".format(malaman_pass))
        conn.execute("UPDATE passwords SET password=\'{}\' WHERE ldap ='vrodriguez';".format(vrodriguez_pass))
        conn.execute("UPDATE passwords SET password= \'{}\' WHERE ldap ='apau';".format(apau_pass))
        conn.execute("UPDATE passwords SET password=\'{}\' WHERE ldap ='asarrion';".format(asarrion_pass))

#    send_mail("webhelp-apau@premium-cloud-support.com", apau_pass)
#    send_mail("webhelp-vkoval@premium-cloud-support.com", vkoval_pass)
#    send_mail("webhelp-malaman@premium-cloud-support.com", malaman_pass)
#    send_mail("webhelp-asarrion@premium-cloud-support.com", asarrion_pass)
#    send_mail("webhelp-vrodriguez@premium-cloud-support.com", vrodriguez_pass)
#    send_mail("webhelp-acooper@premium-cloud-support.com", acooper_pass)
    webhookDic = {"vkoval":"https://chat.googleapis.com/v1/spaces/AAAAwFCytaE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=HF9uyK9eKn8gieGaDNuHJJdZPuMyEcxN5x4d75btWEk%3D","acooper":"https://chat.googleapis.com/v1/spaces/AAAAlVHmCMQ/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=PekYCybxoMHKEQi5XGOx8H7j_RXih8mKLwtghzJvFGk%3D","vrodriguez":"https://chat.googleapis.com/v1/spaces/AAAAKsRMvx0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=J5R2p_Tvcud4W2EdVSd87RL-QLATrXBVyvLPxhfADN4%3D","apau":"https://chat.googleapis.com/v1/spaces/AAAABcxf3ME/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=2m9gaKaoQjY25eDlm1Mshk6r00OtKeF5-h2eLW8HKaU%3D","malaman":"https://chat.googleapis.com/v1/spaces/AAAATszTQmA/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ZiPuE77rQiHmY7xrjoE4e8lh-bahRq_CAZBa_nUexXw%3D","asarrion":"https://chat.googleapis.com/v1/spaces/AAAATBKDzq4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=jvR9ljkhah_z4ni-gFH7ze_5P0DnXiECRpAbtccY0FQ%3D"}   
    address = "https://finalversion-at4mdhyjyq-ew.a.run.app/"
    passDic={"vkoval":vkoval_pass, "acooper":acooper_pass, "asarrion":asarrion_pass, "apau":apau_pass, "malaman":malaman_pass, "vrodriguez":vrodriguez_pass}
    for key, value in webhookDic.items():
        send_msg(f"The password is {passDic[key]} and user is {key}. The link is {address}",webhookDic[key])
    return 'YAYYYYY'
