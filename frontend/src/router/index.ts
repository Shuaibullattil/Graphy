import { createRouter, createWebHistory } from 'vue-router'
import PageOne from '../views/pageone.vue'
import LandingPage from '../components/landingpage.vue'
import LoginRegisterPage from '../views/Login.vue'
import { Component } from 'lucide-vue-next'
import Dashboard from '@/views/Dashboard.vue'

const routes = [
  { path: '/', component: PageOne },
  { path: '/auth/login', component: LoginRegisterPage },
  { path: '/convert', component: LandingPage },
  { path: '/dashboard', component: Dashboard}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
