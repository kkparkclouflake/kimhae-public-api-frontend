import requests
import json
import pymongo 

# API의 HTTP 통신해 데이터 호출
url = "https://smartcity.gimhae.go.kr/smart_tour/dashboard/api/publicData/location/ap"
response = requests.get(url)
# JSON 타입의 데이터를 추출해 Python 데이터로 변환 
jsonArray = json.loads(response.text)
# 변환한 데이터 중 필요한 데이터만 추출
storeInfosArray = jsonArray.get("data")

print("WiFI count -> " + str(len(storeInfosArray)))

# mongoDB 접속
client = pymongo.MongoClient("mongodb://root:mongodb@172.30.1.70:27017")
# DB내 database 접속
db = client.get_database('kimhae')
targetDb = db.wifi

# 기존 DB 데이터 전체 삭제
targetDb.remove({ });

# DB에 data insert
results = targetDb.insert_many(storeInfosArray)
# for result in results.inserted_ids:
#     print (result)
# DB에 insert 된 값 출력
# items = targetDb.find()
#for item in items : 
#    print (item)
