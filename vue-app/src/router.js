import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth'

// Import views
import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import ProfileView from './views/ProfileView.vue'
import QueryView from './views/QueryView.vue'
import MappingResultsView from './views/MappingResultsView.vue'
import DataSourceView from './views/DataSourceView.vue'
import AnalysisView from './views/AnalysisView.vue'
import AboutView from './views/AboutView.vue'
import NotFoundView from './views/NotFoundView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { requiresGuest: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/query',
    name: 'Query',
    component: QueryView,
    meta: { requiresAuth: true }
  },
  {
    path: '/query/mapping',
    name: 'Mapping',
    component: MappingResultsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/query/datasources',
    name: 'DataSource',
    component: DataSourceView,
    meta: { requiresAuth: true }
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: AnalysisView,
    meta: { requiresAuth: true }
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  }
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  
  // Check for protected route
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }
  
  // Check for guest-only route
  if (to.meta.requiresGuest && auth.isAuthenticated) {
    next({ name: 'Home' })
    return
  }
  
  next()
})

export default router