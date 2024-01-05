import Vue from 'vue'
import VueRouter from 'vue-router'
import Access from '../components/Access.vue'
import Manager from '../components/Manager.vue'
import User from '../components/User.vue'

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
  },
  {
    path: '/',
    name: 'User',
    component: User,
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

export default router
