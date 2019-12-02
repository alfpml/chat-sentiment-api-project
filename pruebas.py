from pymongo import MongoClient
import getpass
import json
import mongofnc as mf

#Get Password
password = getpass.getpass("Insert your AtlasMongoDB admin_1019 password: ")
connection = "mongodb+srv://alfpml:{}@cluster0-c3fib.mongodb.net/test?retryWrites=true&w=majority".format(password)
#Connect to DB
client = MongoClient(connection)

db, coll = mf.connectCollection('chats','chatprueba')

with open('input/chats.json') as f:
    chats_json = json.load(f)
coll.insert_many(chats_json)