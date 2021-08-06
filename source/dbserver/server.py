import os
import pymongo 
from flask import Flask, jsonify
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)

# mongoDB 접속
client = pymongo.MongoClient("mongodb://" + os.environ['DB_USER'] + ":" + os.environ['DB_PASS']
                              + "@" + os.environ['DB_URL'])
# DB내 database 접속
db = client.get_database(os.environ['DB_DATABASE'])
targetDb = db[os.environ['DB_COLLECTION']]

@app.route('/wifi')
def wifi():
    rtnArray = []
    for dat in targetDb.find():
        rtnArray.append(dat)
    
    return JSONEncoder().encode(rtnArray)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=False)
