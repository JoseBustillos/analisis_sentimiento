<template>
  <div class="container">
    <div class="row">
      <div class="col text-md-center  ">
        <hr>
        <h1 class="text-white">Analiza el sentimiento de la red social</h1>
        <h1 class="text-white">Twitter sobre tu institución {{this.$route.params.tweet}}</h1>
        <b-container class="bv-example-row">
          <hr>
          <b-row cols="5" cols-sm="5" cols-md="10" cols-lg="10">
            <!-- ciclo vuejs para generar enlaces de los router para consultas adicionales -->
            <b-col class="alert-success" v-for="valor in info.hastag" v-if="valor.sentimiento == 'Positivo'"
                   :key="valor.hashtag">
              <router-link :to="{
              name:'sentiHashtag',
              params:{senti: valor.sentimiento,
              hashtag:valor.hashtag
              }}">
                {{valor.hashtag}} {{valor.sentimiento}}
              </router-link>
            </b-col>
            <b-col class="alert-danger" v-for="valor in info.hastag" v-if="valor.sentimiento == 'Negativo'"
                   :key="valor.hashtag">
              <router-link :to="{
              name:'sentiHashtag',
              params:{senti: valor.sentimiento,
              hashtag:valor.hashtag
              }}">
                {{valor.hashtag}} {{valor.sentimiento}}
              </router-link>
            </b-col>
          </b-row>
          <hr>
          <b-row>
            <b-button variant="outline-primary" size="lg">
              <b-col class="alert-success">
                <b-icon icon="emoji-smile" animation="throb"></b-icon>
                <router-link :to="{
              name:'sentiTweets',
              params:{
              senti: 'Positivo',
              tweet:this.$route.params.tweet
              }}">
                  POSITIVO - {{info.posTotal}}
                </router-link>
              </b-col>
            </b-button>
            <b-button variant="outline-primary" size="lg">
              <b-col class="alert-danger">
                <b-icon icon="emoji-frown" animation="throb"></b-icon>
                <router-link :to="{
              name:'sentiTweets',
              params:{
              senti: 'Negativo',
              tweet:this.$route.params.tweet
              }}">
                  NEGATIVO - {{info.negTotal}}
                </router-link>
              </b-col>
            </b-button>
            <b-button disabled size="lg">
              <b-col class="alert-primary">
                <b-icon icon="wallet-fill" animation="fade"></b-icon>
                total - {{info.totalTweet}}
              </b-col>
            </b-button>
            <!--<b-col class="alert-dark">nivel reputación - {{info.reputacion}}</b-col>-->
          </b-row>
          <hr>
          <b-row>
            <b-col cols="8">{{info.sentimiento}}
              <div class="hello" ref="chartdiv">
              </div>
            </b-col>
            <b-col cols="4" class="bg-light">
              <b-container class="bv-example-row">
                <h5>Influencer</h5>
                <b-row cols="1" cols-sm="1" cols-md="10">
                  <b-col>
                    <b-row>
                      <b-col cols="4">
                        Número seguidores
                      </b-col>
                      <!--<b-col cols="4">
                        Imagen Usuario
                      </b-col>-->
                      <b-col cols="4">
                        Nombre Usuario
                      </b-col>
                    </b-row>
                  </b-col>
                  <b-col v-for="valor in info.usuarios" :key="valor.usuarios">
                    <b-row>
                      <b-col cols="4">
                        <a :href="valor.url">{{valor.seguidores}}
                        </a>
                      </b-col>
                     <!-- <b-col cols="4">
                        <b-img :src="valor.imagen"></b-img>
                      </b-col>-->
                      <b-col cols="4" class="text-right">
                        <router-link :to="{
                      name:'usuarioTweets',
                      params:{
                      user: parseInt(valor.idUser),
                      tweet: $route.params.tweet
                      }}">
                          {{valor.usuario}}
                        </router-link>
                      </b-col>
                    </b-row>
                  </b-col>
                </b-row>
              </b-container>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import * as am4core from "@amcharts/amcharts4/core";
  import * as am4charts from "@amcharts/amcharts4/charts";
  import am4themes_animated from "@amcharts/amcharts4/themes/animated";

  am4core.useTheme(am4themes_animated);
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
        let chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart);
        axios.get('http://127.0.0.1:8000/api/v1.0/tweets/' + this.$route.params.tweet.substring(1) + '.json')
          .then(response => {
              this.info = response.data;
              // Add data
              chart.data = [{
                "name": "POSITIVO",
                "points": this.info.posTotal,
                "color": chart.colors.next(),
                "bullet": "https://www.amcharts.com/lib/images/faces/B03.png"
              }, {
                "name": "NEGATIVO",
                "points": this.info.negTotal,
                "color": chart.colors.next(),
                "bullet": "https://www.amcharts.com/lib/images/faces/O05.png"
              }];
            }
          ).catch(e => console.log(e))
// Create axes
        var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "name";
        categoryAxis.renderer.grid.template.disabled = true;
        categoryAxis.renderer.minGridDistance = 30;
        categoryAxis.renderer.inside = true;
        categoryAxis.renderer.labels.template.fill = am4core.color("#fff");
        categoryAxis.renderer.labels.template.fontSize = 20;
        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.renderer.grid.template.strokeDasharray = "4,4";
        valueAxis.renderer.labels.template.disabled = true;
        valueAxis.min = 0;
// Do not crop bullets
        chart.maskBullets = false;
// Remove padding
        chart.paddingBottom = 0;
// Create series
        var series = chart.series.push(new am4charts.ColumnSeries());
        series.dataFields.valueY = "points";
        series.dataFields.categoryX = "name";
        series.columns.template.propertyFields.fill = "color";
        series.columns.template.propertyFields.stroke = "color";
        series.columns.template.column.cornerRadiusTopLeft = 15;
        series.columns.template.column.cornerRadiusTopRight = 15;
        series.columns.template.tooltipText = "{categoryX}: [bold]{valueY}[/b]";
// Add bullets
        var bullet = series.bullets.push(new am4charts.Bullet());
        var image = bullet.createChild(am4core.Image);
        image.horizontalCenter = "middle";
        image.verticalCenter = "bottom";
        image.dy = 20;
        image.y = am4core.percent(100);
        image.propertyFields.href = "bullet";
        image.tooltipText = series.columns.template.tooltipText;
        image.propertyFields.fill = "color";
        image.filters.push(new am4core.DropShadowFilter());
      }
    },
    beforeDestroy() {
      if (this.chart) {
        this.chart.dispose();
      }
    }
  }
</script>
<style scoped>
  .hello {
    width: 100%;
    height: 500px;
  }
</style>
