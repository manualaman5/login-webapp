##Login web app

This is a web application developed in Python and meant to be built in Google Cloud. The web application registers users in a database with a new password every single day. There is a cloud function that sends those passwords over a private Google chat. The web application allows t
he user to register the time when they log in and you can also see all the records from the login database.

1. Create CloudSQL Instance:

gcloud sql instances create mysqlinstance --tier=db-n1-standard-1 --region=europe-west1

2. Create Database:

gcloud sql databases create improvedArrivalRegister --instance=mysqlinstance

3. Create User:

gcloud sql users create andrew --instance=mysqlinstance --password=sirAndrew --host=%

4. Create Tables:
CREATE TABLE passwords (
  ldap varchar(25) NOT NULL,
  password varchar(16),
  PRIMARY KEY (ldap)
);

CREATE TABLE logins (
  logid int AUTO_INCREMENT,
  ldap varchar(25) NOT NULL,
  ip varchar(25) NOT NULL,
  timestamp varchar(25) NOT NULL,
  PRIMARY KEY (logid),
  FOREIGN KEY (ldap) REFERENCES passwords(ldap)
);

5. Commands for inserting rows:
INSERT INTO passwords (ldap, password) VALUES ("ldaphere", "passwordhere");

INSERT INTO logins (ldap, ip, timestamp) VALUES ("ldaphere", "192.192.192", ADDTIME (CURRENT_TIMESTAMP(), '2:0:0'
));

The function ADDTIME adds two hours to the UTC time, it needs to be changed when the clock changes in Spain!!

6. Execute loginAppFunction/commands.sh in order to create the Scheduler and the Cloud Function (make sure there is already one row for each ldap in the ‘passwords’ table because the function doesn’t delete and create, it just changes the password field from existing rows).

7. Build image in CloudBuild:

Enter into the folder ‘loginAppEngine’ and:

gcloud builds submit --tag gcr.io/wave34-webhelp-vrodrigu
ez/nameOfTheImage

8. Use cloud run: Create Service, choose region and service name, allow unauthenticated, next, select the image you just created and choose the latest version, show advanced settings, containerPort 5000, reduce maximum number of instances, connections, add cloudsql connections, click create.
