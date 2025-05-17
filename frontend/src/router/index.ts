import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../components/landingpage.vue'
import PageOne from '../views/pageone.vue'
import PageTwo from '../views/pagetwo.vue'
import PageThree from '../views/pagethree.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/pageone', component: PageOne },
  { path: '/pagetwo', component: PageTwo },
  { path: '/pagethree', component: PageThree },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
