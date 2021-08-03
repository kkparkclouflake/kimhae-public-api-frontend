<template>
  <div id="bicycle">
    <div id="header">
      <img src="../assets/wifi.png" id="logo" alt="logo">
      <span id="title">김해<span style="font-weight: bold;">공공WiFi</span>스테이션</span>
    </div>
    <div id="container">
      <ul class="links">
        <li v-for="location in locations" :key="location.mgtNo">
          <div style="text-align: left;">
            <div class="mgtNo"><img src="../assets/wifi.png" class="icon" alt="logo">&nbsp;<span>{{ location.mgtNo }}</span></div>
            <div class="name">{{ location.name }}</div>
            <div class="addr">{{ location.addr }}</div>
          </div>
        </li>
      </ul>
      <div id="map"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WiFi',
  data() {
    return {
      locations: []
    }
  },
  created() {
    this.axios.get("/api/wifi")
        .then(value => this.locations = value.data )
        .catch(reason => console.error(reason));
  },
  mounted() {
    if (window.kakao && window.kakao.maps) {
      this.initMap()
    } else {
      const script = document.createElement('script')
      script.onload = () => kakao.maps.load(this.initMap);
      script.src = 'http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=fd62880c001e22689fef1c44e27f3642'
      document.head.appendChild(script)
    }
  },
  methods: {
    initMap() {
      const container = document.querySelector('#map')
      const options = {
        center: new kakao.maps.LatLng(35.228585174781415, 128.88936315765298),
        level: 3
      }
      const map = new kakao.maps.Map(container, options);

      let $this = this;

      let untilLoad = function () {
        if (!$this || !$this.locations || $this.locations.length <= 0) {
          setTimeout(untilLoad, 200);
          // console.log("Waiting... " + Math.random())
          return;
        }

        $this.locations.forEach(function (dat) {
          dat.latlng = new kakao.maps.LatLng(dat.yCoordinate, dat.xCoordinate)
        })
        // 마커를 생성합니다
        $this.locations.forEach(function(pos) {
          let marker = new kakao.maps.Marker({
            map: map, // 마커를 표시할 지도
            position: pos.latlng, // 마커의 위치
            // image: markerImage,
          });

          var customOverlay = new kakao.maps.CustomOverlay({
            position: pos.latlng,
            xAnchor: 0.5,
            yAnchor: 1.05,
          });

          var content = document.createElement('div');
          content.className = 'overlaybox';
          content.style = "border-radius: 10px;" +
              "background: white;" +
              "box-shadow: 0 0 10px 3px rgba(0, 0, 0, 0.15);" +
              "padding: 5px 10px 0px;";

          var title = document.createElement('div');
          title.className = 'map-popup-title';

          var store = document.createElement('h3');
          store.style = "margin: 0;";
          store.className = 'popup-name';
          store.appendChild(document.createTextNode(pos.name));
          title.appendChild(store);
          content.appendChild(title);

          var location = document.createElement('span');
          location.style = "font-size: 9pt;";
          location.className = 'store-location';
          location.appendChild(document.createTextNode(pos.addr));
          content.appendChild(location);

          var mgtNo = document.createElement('p');
          mgtNo.style = "margin: 0;";
          mgtNo.className = 'time-text';
          mgtNo.appendChild(document.createTextNode(pos.mgtNo));
          location.appendChild(mgtNo);

          var buttonContainer = document.createElement('div');
          buttonContainer.className = 'popup-buttons';

          var closeBtn = document.createElement('button');
          closeBtn.className = 'popup-button';
          closeBtn.style = "background: none;" +
              "border: none;"
          closeBtn.innerHTML = "<img style='width: 30px;' src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAADk0lEQVRoge1ZzW9MURQ/CG0QtLQkbUUnpTb4C1otFj6SaqWU/4OFthsadrUlM9P+DywrkmIhEoQu2qiQGKJRG51KWWCcX999cd6d9/3um3aS+SW/ZDLvfN075517zh2iGmqoIQ1sYu5hZhTxeeOaRhSA7cwrzBxzhvmLWdKI794ws8whpbPmOMycZP6g8oCDuMycYHZWPGpGE1mB//EJcIn5UXHJRw428mSlWUVwjvnNJZBZ5k1mL7PRRW+3ejbGnHPRh82zKcdOo8y/muPnzBMxbHUzpzRbsD1iJFIX3NGcfWFeYm5IaLePuaDZHk9oswyjmoOXzFaD9tuYrzQfxn4J5LxMmwfMraaMC2xj3idnOp1JahTVRr6w2Pk0grdRx5wW/hbJevljY5KcOW8ybbzQrHzZfnNxDeGQknV+0EOui3mN2RLBdqvS6fJ43i/8/qaYh53cfZRKt2pzTDmAzEJIR530v+pA96iH3EPhPx8lcAB9imwPej3kBshZOT4zO3zsdigZqdPvIXtcyBTJeslD47JQnvWR28J8qgVUIKsD1ZFRz6QsdDf72H8rZC9GWUBOKN4IkMXOPKHyRbQLmf3MD5rMM+aOANu3hPy9KAuYoeD0kdhJ1nsiA0QTd4CsF/a99gyHllu/pOOk0HkdNngMHj+FYtg63EDWOSEDfaeon+INIW02Cb0VCjkUNQul7yEd2djFfEHOgCUx0EQ9mIpCP1TLnREKhYjOAOyaTEGbaKH3xbD3SdhoD5BdRdUvQOZdVaZQ1b/EwHopo6eETugyCmSF4liAbJoH2W0hfzfKAoaE4pyPXNqtxLyQ9eqGXYFmblkod3vIXdACMtnM9QgZvMiRB6kJYWDKQwatcNJ2+oiH3CPhP9ZQA0dyoOnzkMNQcpWiDTQtSsdroJG/LBZ5KIJtB/LCEHatLa6hCNhLzpEym8QYDg451KP8pTnU1zMfC3+Jh3oA133yWgVXH3VJjbqgnpzXKkjf06aMj5CzckyT1bWaAtJG7jx43aD9VYxrDpCn5w3YHSBnzpcohatFG8NUfrmL24OeGLagI0tlSdk2vvM6cN23qDkGMYBjhsUY6NY14jv0NmgP5l30v5LBnA8CKgMOF78/OHB6FhSLPnKo81kyUG3iAAdMPiBAvwViEw5WPGoX4GzAvQ2uPtD2onfXA15Rz9BVDlK650liYPBAv2//zdpI6/xv1hpqqFb8A63t1qzsy8cSAAAAAElFTkSuQmCC\" />";
          closeBtn.onclick = function () {
            customOverlay.setMap(null);
          };

          buttonContainer.appendChild(closeBtn);

          content.appendChild(buttonContainer);

          kakao.maps.event.addListener(marker, 'click', function () {
            customOverlay.setMap(map);
          });

          customOverlay.setContent(content);
        });
      }

      setTimeout(untilLoad, 100);

      // let imageSrc = require('@/assets/marker.png'), // 마커이미지의 주소입니다
      //     imageSize = new kakao.maps.Size(24, 35), // 마커이미지의 크기입니다
      //     imageOption = { offset: new kakao.maps.Point(20, 35) }; // 마커이미지의 옵션입니다. 마커의 좌표와 일치시킬 이미지 안에서의 좌표를 설정합니다.

      // 마커의 이미지정보를 가지고 있는 마커이미지를 생성합니다
      // let markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption);

    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.links .icon {
  width: 14px;
  height: 14px;
  margin: 3px 0 0 1px;
}

.links .mgtNo {
  font-size: 10pt;
  font-weight: bold;
  display: flex;
}

.links .addr {
  font-weight: 300;
}

.links .name {
  font-weight: 900;
  padding: 5px 0;
  font-size: 12pt;
}

.links {
  height: 100%;
  overflow-y: scroll;
  width: 330px;
  margin: 0;
}

.links li {
  margin: auto;
  display: list-item;
  text-align: center;
  padding: 5px 20px;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 20px;
  vertical-align: center;
}

.links li:hover {
  background-color: lightgray;
  width: auto;
}

#container {
  height: calc(100% - 50px);
}

#header #logo {
  margin: 5px 6px 0 10px;
  height: 40px;
}

#header #title {
  font-weight: lighter;
  font-size: 1.1em;
}

#header {
  display: flex;
  text-align: left;
  line-height: 50px;
  height: 50px;
  box-shadow: 0 0 7px 7px rgba(0, 0, 0, 0.15);
  z-index: 999999999999;
  position: relative;
}

#bicycle {
  height: 100%;
}

#map {
  position: absolute;
  top: 50px;
  right: 0;
  width: calc(100% - 330px);
  height: calc(100% - 50px);
}

h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
