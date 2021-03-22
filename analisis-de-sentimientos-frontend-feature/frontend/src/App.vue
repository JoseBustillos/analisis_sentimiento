<template>
  <body style="background-image: url(static/img/index_background.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;">
  <div id="app">
    <router-view/>
  </div>
  </body>
</template>
<script>
  export default {
    name: 'App'
  }
</script>


