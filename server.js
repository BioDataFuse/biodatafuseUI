import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import RDFGenerationView from '../views/RDFGenerationView.vue'

// Import other views that exist in the application
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import QueryView from '../views/QueryView.vue'
import MappingResultsView from '../views/MappingResultsView.vue'
import DataSourceView from '../views/DataSourceView.vue'
import AnnotationResultsView from '../views/AnnotationResultsView.vue'
import VisualizationView from '../views/VisualizationView.vue'
import AnalysisView from '../views/AnalysisView.vue'
import GraphDBView from '../views/GraphDBView.vue'
import Neo4jView from '../views/Neo4jView.vue'
import CytoscapeView from '../views/CytoscapeView.vue'
import VisualizeAndAnalysisView from '../views/VisualizeAndAnalysisView.vue'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/home',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/query',
    name: 'Query',
    component: QueryView,
    meta: { requiresAuth: true }
  },
  {
    path: '/query/mapping-results',
    name: 'MappingResults',
    component: MappingResultsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/query/datasources',
    name: 'DataSources',
    component: DataSourceView,
    meta: { requiresAuth: true }
  },
  {
    path: '/query/annotations',
    name: 'AnnotationResults',
    component: AnnotationResultsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/rdf-generation',
    name: 'RDFGeneration',
    component: RDFGenerationView,
    meta: { requiresAuth: true }
  },
  {
    path: '/visualization',
    name: 'Visualization',
    component: VisualizationView,
    meta: { requiresAuth: true }
  },
  {
    path: '/visualize&analysis',
    name: 'VisualizeAndAnalysis',
    component: VisualizeAndAnalysisView,
    meta: { requiresAuth: true }
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: AnalysisView,
    meta: { requiresAuth: true }
  },
  {
    path: '/graphdb',
    name: 'GraphDB',
    component: GraphDBView,
    meta: { requiresAuth: true }
  },
  {
    path: '/neo4j',
    name: 'Neo4j',
    component: Neo4jView,
    meta: { requiresAuth: true }
  },
  {
    path: '/cytoscape',
    name: 'Cytoscape',
    component: CytoscapeView,
    meta: { requiresAuth: true }
  },
  // Redirect routes for common navigation patterns
  {
    path: '/query/mapping',
    redirect: '/query/mapping-results'
  },
  {
    path: '/query/results',
    redirect: '/query/annotations'
  }
]

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = !!localStorage.getItem('user')

  if (requiresAuth && !isAuthenticated) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router

app.use(require('connect-history-api-fallback')());