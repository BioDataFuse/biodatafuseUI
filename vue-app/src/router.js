import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth'

// Import views
import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import ProfileView from './views/ProfileView.vue'
import InputView from './views/InputView.vue'
import MappingResultsView from './views/MappingResultsView.vue'
import DataSourceView from './views/DataSourceView.vue'
import AnnotationsResultsView from './views/AnnotationResultsView.vue'
import VisualizeAndAnalysisView from './views/VisualizeAndAnalysisView.vue'
import CytoscapeView from './views/CytoscapeView.vue'
import GraphDBView from './views/GraphDBView.vue'
import Neo4jView from './views/Neo4jView.vue'
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
    name: 'Input',
    component: InputView,
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
    path: '/query/annotations',
    name: 'Annotations',
    component: AnnotationsResultsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/visualize&analysis',
    name: 'Visualize and Analysis',
    component: VisualizeAndAnalysisView,
    meta: { requiresAuth: true }
  },
  {
    path: '/visualize&analysis/cytoscape',
    name: 'Cytoscape',
    component: CytoscapeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/visualize&analysis/graphdb',
    name: 'GraphDB',
    component: () => import('./views/GraphDBView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/visualize&analysis/neo4j',
    name: 'Neo4j',
    component: Neo4jView,
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