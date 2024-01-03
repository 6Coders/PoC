import Vue from 'vue'
import VueRouter from 'vue-router'
import Access from '../components/Access.vue'
import Manager from '../components/Manager.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Access
  },
  {
    path: '/',
    name: 'Manager',
    component: Manager,
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

export default router
