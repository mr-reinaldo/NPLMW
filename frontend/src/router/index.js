// Composables
import { createRouter, createWebHistory } from 'vue-router'

// Routes
import loginRoutes from '@/modules/auth/routes'
import homeRoutes from '@/modules/home/routes'

// Middleware
import authMiddleware from '@/middleware/auth'

const routes = [
  ...loginRoutes,
  ...homeRoutes,
  {
    path: '',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,

})

// Middleware para liberar rotas que precisam de autenticação.
router.beforeEach(authMiddleware)

export default router
