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

![](https://raw.githubusercontent.com/kkparkclouflake/kimhae-public-api-frontend/main/image/system.png)



##  서비스 구현

### 1. API값 불러와 MongoDB 저장 후 출력


![](https://raw.githubusercontent.com/kkparkclouflake/kimhae-public-api-frontend/main/image/crawler.png)

---

### 2. MongoDB Flask 출력

​		(DBserver Docker / Cluster IP로 Deployment Service)

---

### 3. DBserver Docker Cluster IP로 Deployment Service

​		Backend Pod로 MongoDB 값을 Frontend로 전달

---

### 4. Crawler Docker / CronJob Service

​		김해 공공 API 정보를 5분에 1번씩 가저와 DB에 저장하는 Pod

---

### 5. kubernetis Pod 및 Service 확인

Pod 정보

![](https://raw.githubusercontent.com/kkparkclouflake/kimhae-public-api-frontend/main/image/getpod.png)

Service 정보

![](https://raw.githubusercontent.com/kkparkclouflake/kimhae-public-api-frontend/main/image/getservice.png)

Frontend 연동 결과

![](https://raw.githubusercontent.com/kkparkclouflake/kimhae-public-api-frontend/main/image/result.png)
