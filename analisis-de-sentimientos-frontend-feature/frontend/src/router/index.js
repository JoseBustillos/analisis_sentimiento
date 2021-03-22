import Vue from 'vue'
import Router from 'vue-router'
import listData from '@/components/dataConsulta/listData'
import newDato from '@/components/dataConsulta/newDato'
import reputacion from '@/components/dataConsulta/reputacion'
import sentiHashtag from '@/components/dataConsulta/sentiHashtag'
import sentiTweets from '@/components/dataConsulta/sentiTweets'
import usuarioTweets from '@/components/dataConsulta/usuarioTweets'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/data',
      name: 'listData',
      component: listData
    },
    {
      path: '/',
      name: 'newDato',
      component: newDato
    },
    {
      path: '/reputacion/:tweet',
      name: 'reputacion',
      component: reputacion
    },
    {
      path: '/sentiHashtag/:senti/:hashtag/:tweet',
      name: 'sentiHashtag',
      component: sentiHashtag
    },
    {
      path: '/sentiTweet/:senti/:tweet',
      name: 'sentiTweets',
      component: sentiTweets
    },
    {
      path: '/usuarioTweets/:user/:tweet',
      name: 'usuarioTweets',
      component: usuarioTweets
    }
  ],
  mode: 'history'
})
