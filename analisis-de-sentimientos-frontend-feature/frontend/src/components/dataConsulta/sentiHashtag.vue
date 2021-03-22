<template>
  <b-container class="bv-example-row">
    <b-row>
      <b-col md="6" offset-md="3" class="text-right">
        <hr>
        <h3 class="text-white"><p>Sentimiento: {{this.$route.params.senti}}</p>
          <p>Hashtag: {{this.$route.params.hashtag}}</p></h3>
      </b-col>
      <!--{{this.$route.params}}-->
    </b-row>
    <b-row class="bg-light">
      <b-col>
        <div v-for="valor in info.original">
          <b-row>
            <b-col>
              <b-img :src="valor.usuario"></b-img>
            </b-col>
            <b-col>{{valor.nombre}}</b-col>
            <b-col>{{valor.verificado}}</b-col>
          </b-row>
          <a :href="valor.url">{{valor.texto}}</a>
          <b-row>
            <b-col>Likes: {{valor.numlikes}}</b-col>
            <b-col>Citado: {{valor.numcitado}}</b-col>
            <b-col>Retweet: {{valor.numretweet}}</b-col>
            <b-col>Respuestas: {{valor.numrespuesta}}</b-col>
          </b-row>
          <hr>
        </div>
      </b-col>
      <b-col>
        <div v-for="valor in info.ret">
          <b-row>
            <b-col>
              <b-img :src="valor.usuario"></b-img>
            </b-col>
            <b-col>{{valor.nombre}}</b-col>
            <b-col>{{valor.verificado}}</b-col>
          </b-row>
          <a :href="valor.url">{{valor.texto}}</a>
          <b-row>
            <b-col>Likes: {{valor.numlikes}}</b-col>
            <b-col>Citado: {{valor.numcitado}}</b-col>
            <b-col>Retweet: {{valor.numretweet}}</b-col>
            <b-col>Respuestas: {{valor.numrespuesta}}</b-col>
          </b-row>
          <hr>
        </div>
      </b-col>
    </b-row>
    <!-- <p>
       {{info}}
     </p>-->
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
        axios.get('http://127.0.0.1:8000/api/v1.0/hashtag/' + this.$route.params.senti +
          '/' + this.$route.params.hashtag +
          '/' + this.$route.params.tweet + '.json')
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
