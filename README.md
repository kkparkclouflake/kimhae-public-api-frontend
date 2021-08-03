# 김해 공공 API 정보 출력

카카오 지도에 김해 공공 와이파이 설치 정보를 뿌려 시각화한 서비스 구축

## 김해 공공 API 

[API 정보](https://smartcity.gimhae.go.kr/smart_tour/contents/contents.do?ciIdx=843&menuId=992)

API sample

```json
{
    "mgtNo": "AP_002",
    "name": "테마형 특화단지 WIFI 002(연지공원(풍력폴1))",
    "xCoordinate": "128.868472",
    "yCoordinate": "35.247056",
    "addr": "경상남도 김해시 내외동 115"
},
{
   "mgtNo": "AP_003",
   "name": "테마형 특화단지 WIFI 003(연지공원역(타고가야))",
   "xCoordinate": "128.869694",
   "yCoordinate": "35.249417",
   "addr": "경상남도 김해시 구산동 1072-16"
},
```



## 프로젝트 구성도

![](https://raw.githubusercontent.com/kkparkclouflake/kimhae-public-api-frontend/main/image/구성도.png)



##  서비스 구현

### 1. API값 불러와 MongoDB 저장 후 출력

​		(Crawler Docker / CronJob Service)

```python
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
db = client.get_database(‘kimhae')
targetDb = db.wifi

# 기존 DB 데이터 전체 삭제
targetDb.remove({ });

# DB에 data insert
results = targetDb.insert_many(storeInfosArray)
# for result in results.inserted_ids:
#     print (result)
 
# DB에 insert 된 값 출력
items = targetDb.find()
#for item in items : 
#    print (item)
```



![](https://raw.githubusercontent.com/kkparkclouflake/kimhae-public-api-frontend/main/image/crawler.png)

---

### 2. MongoDB Flask 출력

​		(DBserver Docker / Cluster IP로 Deployment Service)

```python
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
client = pymongo.MongoClient("mongodb://root:mongodb@172.30.1.70:27017")

db = client.get_database('kimhae')

# DB내 database 접속
targetDb = db.wifi

@app.route('/wifi')
def wifi():
    rtnArray = []
    for dat in targetDb.find():
        rtnArray.append(dat)
    
    return JSONEncoder().encode(rtnArray)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=False)
```

---

### 3. DBserver Docker Cluster IP로 Deployment Service

​		Backend Pod로 MongoDB 값을 Frontend로 전달

Dockerfile

```dockerfile
# python alpine 이미지 (python docker hub 중 가장 가볍다) 
FROM python:3.9.6-alpine
# 제작자 및 author 기입
LABEL maintainer chomh
# 해당 디렉토리에 있는 모든 하위항목들을 '/app/server`로 복사한다
COPY . /app/server
# image의 directory로 이동하고
WORKDIR /app/server
# 필요한 의존성 file들 설치
RUN pip3 install -r requirements.txt
# container가 구동되면 실행
ENTRYPOINT ["python3", "api_python.py"]
```

requirements.txt

```
pymongo
flask
```

1-backend.yaml

```yaml
#kimhae namespace 생성
apiVersion: v1
kind: Namespace
metadata:
 name: kimhae
# Harbor 접속 정보 저장
---
apiVersion: v1
data:
  .dockerconfigjson: eyJhdXRocyI6eyIxNzIuMzAuMS43MCI6eyJ1c2VybmFtZ
SI6Im1oY2hvIiwicGFzc3dvcmQiOiIxUTJ3M2U0ciIsImVtYWlsIjoibWhjaG9AY2x
vdWZsYWtlLmNvbSIsImF1dGgiOiJiV2hqYUc4Nk1WRXlkek5sTkhJPSJ9fX0=
kind: Secret
metadata:
  name: harbor
  namespace: kimhae
type: kubernetes.io/dockerconfigjson
# Harbor에서 이미지 가저와 Deployment Pod 생성
---
apiVersion: apps/v1
kind: Deployment
metadata:
 name: dbserver
 namespace: kimhae
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dbserver
  template:
    metadata:
      labels:
        app: dbserver
    spec:
      containers:
      - image: "172.30.1.70/kimhae/dbserver:0.0.1"
        name: dbserver
        ports:
        - containerPort: 5000
      imagePullSecrets:
      - name: harbor
# 생성된 Pod로 ClusterIP 서비스 생성
---
apiVersion: v1
kind: Service
metadata:
  name: dbserver-service
  namespace: kimhae
spec:
  type: ClusterIP
  selector:
    app: dbserver
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
```

---

### 4. Crawler Docker / CronJob Service

​		김해 공공 API 정보를 5분에 1번씩 가저와 DB에 저장하는 Pod

Dockerfile

```dockerfile
# python alpine 이미지 (python docker hub 중 가장 가볍다) 
FROM python: 3.9.6-alpine
# 제작자 및 author 기입
LABEL maintainer chomh
# 해당 디렉토리에 있는 모든 하위항목들을 '/app/server`로 복사한다
COPY . /app/server
# image의 directory로 이동하고
WORKDIR /app/server
# 필요한 의존성 file들 설치
RUN pip3 install -r requirements.txt
# container가 구동되면 실행
ENTRYPOINT ["python3", “crawl.py"]
```

requirements.txt

```
requests
pymongo
```

crawl.yaml

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
 name: crawler
 namespace: kimhae
spec:
 jobTemplate:
  spec:
   template:
    spec:
     containers:
      - command: ~
        image: "172.30.1.70/kimhae/crawler:0.0.1"
        imagePullPolicy: IfNotPresent
        name: crawler
# Harbor 접속 비밀번호 지정
     imagePullSecrets:
     - name: harbor
     restartPolicy: OnFailure
 schedule: "*/5 * * * *"
```

---

### 5. kubernetis Pod 및 Service 확인

Pod 정보

![](https://raw.githubusercontent.com/kkparkclouflake/kimhae-public-api-frontend/main/image/get pod.png)

Service 정보

![](https://raw.githubusercontent.com/kkparkclouflake/kimhae-public-api-frontend/main/image/get service.png)

Frontend 연동 결과

![](https://raw.githubusercontent.com/kkparkclouflake/kimhae-public-api-frontend/main/image/result.png)