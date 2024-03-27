import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


#connect to mysql
dataBase = mysql.connector.connect(
  host= "localhost",
  user= "root",
  passwd= os.environ.get('MYSQL_PASSWORD'),
  auth_plugin='mysql_native_password'
)

#prepare a cursor object
cursorObject = dataBase.cursor()

#create a db
cursorObject.execute("CREATE DATABASE dcrm")

print("database done!")