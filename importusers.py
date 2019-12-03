import json
import pandas as pd
import os
import getpass
import mongofnc as mf
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

chats = pd.read_json("input/chats.json")
users = chats[['idUser','userName']]
users = users.drop_duplicates()

##Get Password
password = getpass.getpass("Insert your AtlasMongoDB admin_1019 password: ")
connection = "mongodb+srv://alfpml:{}@cluster0-c3fib.mongodb.net/test?retryWrites=true&w=majority".format(password)

#Connect to DB
client = MongoClient(connection)
db, coll = mf.connectCollection('apichats','users')

with open('output/users.json') as f:
    users_json = json.load(f)
coll.insert_many(users_json)


