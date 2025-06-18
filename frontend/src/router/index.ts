import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '@/lib/auth'
import LoginView from '@/views/Login.vue'
import DevicesView from '@/views/Devices.vue'
import BackupView from '@/views/Backups.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'devices',
      component: DevicesView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/backups',
      name: 'backups',
      component: BackupView,
      meta: {
        requiresAuth: true,
      },
    },
  ],
})

// Navigation guard to check authentication
router.beforeEach(async (to, from, next) => {
  if (to?.meta?.requiresAuth) {
    const auth = await isAuthenticated()
    if (!auth) {
      return next({
        name: 'login',
      })
    }
  }

  if (to.path === '/login') {
    const auth = await isAuthenticated()
    if (auth) {
      return next({
        name: 'devices',
      })
    }
    return next()
  }

  next()
})

export default router
