import mysql.connector
import os

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = os.environ.get('DATABASE_PASSWORD')
)

cursorObject = dataBase.cursor()

cursorObject.execute('CREATE DATABASE formsite')

print("All Done!")