<template lang="html">
  <div class="container">
    <div class="row">
      <div class="col text-md-center">
        <b-container fluid class="bv-example-row">
          <b-row>
            <b-col md="6" offset-md="3">
              <b-card img-src="../../../../static/img/index_cart.jpg" title="Buscador de tweets" img-alt="Image" img-top>
                <b-card-text>
                  <form @submit="onSubmit">
                    <div class="form-group row">
                      <label for="data" class="col">Ingresar data</label>
                      <div class="col-4">
                        <input type="text" placeholder="@user o #hashtag" name="data" class="form-control"
                               v-model.trim="form.data">
                      </div>
                      <div class="col">
                        <b-button type="" submit variant="primary" v-model.trim="form.data">
                          <b-icon icon="search" animation="throb"></b-icon>
                          Buscar
                        </b-button>
                      </div>
                    </div>
                  </form>
                </b-card-text>
              </b-card>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        form: {
          data: ''
        }
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault()
        // endpoint
        const path = 'http://127.0.0.1:8000/api/v1.0/data.json'
        // realizar petición post usando axios
        axios.post(path, this.form).then((response) => {
          // llenar los campos del json
          this.form.data = response.data.data
          // control de errores por el backend
          if (response.data.error) {
            // mostrar mensaje de alerta al usuario
            this.$alert(response.data.error);
          } else {
            // obtener data de consulta
            var tweet = response.data.data
            // dirigirnos al siguiente componente enviando data de consulta
            this.$router.push({
                name: 'reputacion',
                params: {tweet}
              }
            );
          }
        })
          // control de error al endpoint
          .catch((error) => {
            console.log(error)
          })
      }
    }
  }
</script>


