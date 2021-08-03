<template>
  <div id="app">
    <WiFi/>
  </div>
</template>

<script>
import WiFi from './components/WiFi.vue'

export default {
  name: 'App',
  components: {
    WiFi
  }
}
</script>

<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard-dynamic-subset.css');

html * {
  font-family: Pretendard, 'Spoqa Han Sans Neo', 'Source Han Sans KR', 'NanumBarunGothic', sans-serif !important;
}

html, body {
  height: 100%;
  padding: 0;
  margin: 0;
  overflow-y: hidden;
}

#app {
  height: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /*margin-top: 60px;*/
}
</style>
