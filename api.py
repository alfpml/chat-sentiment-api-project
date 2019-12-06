from bottle import route, run, get, post, request
from bson.json_util import dumps
import json
import dns
import requests
import mongofnc as mf
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

@route("/")
def index():
    return {'This is the chat sentiment api'}

@get("/<chat_id>/messages")
def getMessages(chat_id):
    """Get messages from a given chat"""
    return dumps(coll.find({'idChat':int(chat_id)}))

@get("/users")
def getUsers():
    """Get all users"""
    return dumps(coll.aggregate([{"$group":{"_id": {"idUser":"$idUser", "userName":"$userName"}}}]))

@get("/<username>/usermessages")
def getUserMessages(username):
    """Gets user messages"""
    return dumps(coll.find({'userName':str(username)},{"text": 1,"_id":0}))

@post('/user/create')
def createuser():
    """New user creation"""
    name = str(request.forms.get("name"))
    new_id = max(user.distinct("idUser")) + 1
    names = list(user.aggregate([{'$project':{'userName':1}}]))

    if name in [n['userName'] for n in names]:
        return "name already in database"
    else:
        new_user = {
            "idUser": new_id,
            "userName": name
        }
        user.insert_one(new_user)
        return f"user_id for {name} is {new_id}"

@post('/chat/<chat_id>/addmessage')
def addMessage(chat_id):
    """Add messages to a given chat and user (creates user if n ot created"""
    idUser = max(user.distinct('idUser')) +1
    names = list(user.aggregate([{'$project':{'userName':1, 'idUser':1,'_id':0}}]))
    name = str(request.forms.get("name"))
    message = str(request.forms.get("message"))
    new_id = max(coll.distinct("idMessage"))+ 1
    for n in names:
        if n['userName']==name:
            idUser = n['idUser']
    new_message = {
        "idUser":idUser,
        "userName": name,
        "idChat": int(chat_id),
        "idMessage":new_id,
        "text" : message
    }
    new_user = {
        "idUser":idUser,
        "userName":name
    }
    if name not in [n['userName'] for n in names]:
        user.insert_one(new_user)
    coll.insert_one(new_message)

@get('/<chat_id>/sentiment')
def getSentiment(chat_id):
    """Returns sentiment metrics of a given chat"""
    query = list(coll.find({'idChat':int(chat_id)}, {"userName":1,"text": 1,"_id":0}))
    texts = [e['text'] for e in query]
    sid = SentimentIntensityAnalyzer()
    sentiment = [sid.polarity_scores(string) for string in texts]
    average_sentiment = {
        "Average Sentiment in the Chat":{
            "Negativity": sum(e['neg'] for e in sentiment)/len(sentiment),
            "Neutral": sum(e['neu'] for e in sentiment)/len(sentiment),
            "Positivity": sum(e['pos'] for e in sentiment)/len(sentiment),
            "Compound": sum(e['compound'] for e in sentiment)/len(sentiment)
    }}
    return average_sentiment

db, coll = mf.connectCollection('apichats', 'chat1')
db, user = mf.connectCollection('apichats', 'users')
run(host="0.0.0.0", port=8080, debug=True)
