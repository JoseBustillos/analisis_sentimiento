<template>
  <b-container class="bv-example-row">
    <div>{{this.$route.params}}</div>
    <div>{{info}}</div>
  </b-container>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {
        info: ''
      }
    },
    mounted() {
      this.getTweets();
    },
    methods: {
      async getTweets() {
        axios.get('http://127.0.0.1:8000/api/v1.0/usuarios/' + this.$route.params.user +
          '/' + this.$route.params.tweet.substring(1) + '.json')
          .then(response => {
              this.info = response.data
            }
          ).catch(e => console.log(e))
      }
    }
  }
</script>

<style scoped>

</style>
