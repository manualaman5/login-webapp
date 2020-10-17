from flask import Flask
from flask import request, redirect, render_template
import flask
app = Flask(__name__)

#The default route renders the index and shows the form
@app.route('/')
def displayIndexPage():
    return flask.send_file("index.html")

"""
This is the route for the database viewer, when the user clicks the database button in the index, this route will query the database and show the records in the logins table.
"""
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

"""
This is the route for the login, when the user sends the form, this route will check if the user is correct, if they are a trainer and insert the record in logins accordingly.
"""
@app.route('/newEntry', methods=["POST", "GET"])
def addNewUser():
    if (request.method == "GET"):
        print (request.remote_addr)
        return "Please get back to the front page and specify your ldap"
    elif (request.method == "POST"):
        #This will be the list of the trainers
        trainers = ["malaman"]

        #Get the variables from the request
        ldap = request.form["ldap"]
        pw = request.form["pw"]
        ip = request.environ['REMOTE_ADDR']
        # ADDTIME converts from UTC to UTC+2
        # change this command when the clock changes in Spain!
        
        insert_query = f"INSERT INTO logins (ldap, ip, timestamp) VALUES ('{ldap}', '{ip}', ADDTIME (CURRENT_TIMESTAMP(), '2:0:0'));"
        
        import pymysql
        connection = pymysql.connect(
            unix_socket='/cloudsql/wave34-webhelp-vrodriguez:europe-west1:mysql', user='andrew', password='sirAndrew', db="improvedArrivalRegister")
        try:
            password_query = f"SELECT * FROM passwords WHERE ldap='{ldap}' 'ldap' AND password ='{pw}';"
            #print('This is the password query',password_query)
            
            with connection.cursor() as cur:
                cur.execute(password_query)
                data = cur.fetchall()
            
            #When the combination of user and password is not in the database, we will render the wrong credentials template.
            if not data:
                return render_template("wrongcred.html")
            #When the combination is in the database, we will check if they are a trainer or insert the login record
            else:
                if ldap not in trainers:
                    print("This is not a trainer")
                    with connection.cursor() as cur:
                        cur.execute(insert_query)
                        connection.commit()
                        print ("RECORD INSERTED")
                    return render_template("success.html")
                else:
                    print("This is a trainer")
                    return render_template("trainers.html")
        except Exception as e:
            print (e)
        finally:
            connection.close()
            print('Connection closed!')


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=5000)
