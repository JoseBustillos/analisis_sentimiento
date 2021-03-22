<template lang="html">
  <div class="container">
    <div class="row">
      <div class="col text-left" id="app">
        <h2>Listado de data consulta</h2>
        <div class="col-md-12">
          <b-table striped hover :items="datos" :fields="fields">
          </b-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {
        fields: [
          {key: 'data', label: 'Data consulta'}
        ],
        datos: []
      }
    },
    methods: {
      getDatos() {
        const path = 'http://localhost:8000/api/v1.0/data.json'
        axios.get(path).then((response) => {
          this.datos = response.data
        })
          .catch((error) => {
            console.log(error)
          })
      }
    },
    created() {
      this.getDatos()
    }
  }
</script>

<style scoped>

</style>
