def connectCollection(database,collection):
    db = client[database]
    coll = db[collection]
    return db, coll