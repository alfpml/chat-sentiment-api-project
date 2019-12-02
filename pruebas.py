from pymongo import MongoClient
import getpass
import json
import mongofnc as mf

db, coll = mf.connectCollection('chats','chatprueba')

with open('input/chats.json') as f:
    chats_json = json.load(f)
coll.insert_many(chats_json)