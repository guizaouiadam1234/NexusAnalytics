import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import AnalyticsView from '@/views/AnalyticsView.vue'
import ReportsView from '@/views/ReportsView.vue'
import DocsView from '@/views/DocsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', name: 'dashboard', component: DashboardView },
    { path: '/analytics', name: 'analytics', component: AnalyticsView },
    { path: '/reports', name: 'reports', component: ReportsView },
    { path: '/docs', name: 'docs', component: DocsView },
  ],
})

export default router
