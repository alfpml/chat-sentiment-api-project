from bottle import route, run, get, post, request
from bson.json_util import dumps
import json
import dns
import requests
import mongofnc as mf

@route("/")
def index():
    """To get all the data from the DB"""
    return dumps(coll.find())

@get("/<chat_id>/messages")
def getMessages(chat_id):
    """Get messages from a given chat"""
    return dumps(coll.find({'idChat':int(chat_id)}))
    

@get("/users")
def getUsers():
    """Get all users"""
    return dumps(coll.aggregate([{"$group":{"_id": {"idUser":"$idUser", "userName":"$userName"}}}]))

@post('/user/create')
def createuser():
    """New user creation"""
    name = str(request.forms.get("name"))
    new_id = coll.distinct("idUser")[-1] + 1

        "idUser":new_id,
        "userName":name
    }
    coll.insert_one(new_user)

@post('/chat/<chat_id>/addmessage')
def createMessage(chat_id):
    db1, coll1 = mc.connectCollection('apiproject','chats')
    user = dumps(coll1.find({"idChat":int(chat_id)},{"idUser":1,"userName":1}))
    
    message = str(request.forms.get("message"))
    new_id = coll.distinct("idMessage")[-1] + 1
    new_message = {
        "idUser":idUser,
        "userName": username,
        "idChat": int(chat_id),
        "idMessage":new_id,
        "text" : message
    }
    coll.insert_one(new_message)


db, coll = mf.connectCollection('apichats', 'chat1')
run(host="0.0.0.0", port=8080, debug=True)