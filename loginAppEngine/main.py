from flask import Flask
from flask import request, redirect, render_template
import flask
app = Flask(__name__)
@app.route('/')
def displayIndexPage():
    return flask.send_file("index.html")
@app.route('/databaseViewer')
def displayDatabase():
    query = "SELECT * FROM logins;"
    import pymysql
    message = ""
    connection = pymysql.connect(
        unix_socket='/cloudsql/wave34-webhelp-vrodriguez:europe-west1:mysql', user='andrew', password='sirAndrew',
        db="improvedArrivalRegister")
    try:
        with connection.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            message += "<pre><h3>LogID      LDAP                 IP                  TIMESTAMP</h3></pre>"
            message += "<h3>------------------------------------------------------------------------------------------------------</h3>"
            for row in data:
                message += "<pre><h3>"
                message += f"{row[0]:<10} {row[1]:20} {row[2]:20} {row[3]:20}"
                message += "</h3></pre>"
    except Exception as e:
        print (e)
    finally:
        connection.close()
        return message
@app.route('/newEntry', methods=["POST", "GET"])
def addNewUser():
    if (request.method == "GET"):
        print (request.remote_addr)
        return "Please get back to the front page and specify your ldap"
    elif (request.method == "POST"):
        trainers = ["tester", "another"]
        ldap = request.form["ldap"]
        pw = request.form["pw"]
        ip = request.environ['REMOTE_ADDR']
        # ADDTIME converts from UTC to UTC+2
        # change this command when the clock changes in Spain!
        insert_query = f"INSERT INTO logins (ldap, ip, timestamp) VALUES ('{ldap}', '{ip}', ADDTIME (CURRENT_TIMESTAMP(), '2:0:0'));"
        password_query = f"SELECT * from passwords where ldap="
        import pymysql
        connection = pymysql.connect(
            unix_socket='/cloudsql/wave34-webhelp-vrodriguez:europe-west1:mysql', user='andrew', password='sirAndrew', db="improvedArrivalRegister")
        # THIS IS TO CHECK THE USER for trainees
        if pw:
            print("I have a password")
            message = ""
            try:
                password_query +=  "'" + ldap + "' AND password =" + "'" + pw + "';"
                print(password_query)
                with connection.cursor() as cur:
                    print(password_query)
                    cur.execute(password_query)
                    data = cur.fetchall()
                    print(data, type(data))
                if data:
                    # processing and insert record
                    with connection.cursor() as cur:
                        cur.execute(insert_query)
                        connection.commit()
                        message += "RECORD INSERTED"
                else:
                    # add error here
                    message += "The credentials provided are not correct"
            except Exception as e:
                print (e)
            finally:
                connection.close()
                return message
        # This part will be for the trainers
        elif ldap in trainers:
            return "this is a trainer"
if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=5000)
