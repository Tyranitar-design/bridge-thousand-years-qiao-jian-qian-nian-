import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'bridges',
        name: 'Bridges',
        component: () => import('@/views/BridgeGallery.vue'),
        meta: { title: '桥梁博览' }
      },
      {
        path: 'bridges/:id',
        name: 'BridgeDetail',
        component: () => import('@/views/BridgeDetail.vue'),
        meta: { title: '桥梁详情' }
      },
      {
        path: 'timeline',
        name: 'Timeline',
        component: () => import('@/views/Timeline.vue'),
        meta: { title: '时间轴' }
      },
      {
        path: 'ai-qa',
        name: 'AIQA',
        component: () => import('@/views/AIQA.vue'),
        meta: { title: 'AI问答' }
      },
      {
        path: 'structure',
        name: 'Structure',
        component: () => import('@/views/Structure.vue'),
        meta: { title: '结构剖析' }
      },
      {
        path: 'craftsmen',
        name: 'Craftsmen',
        component: () => import('@/views/Craftsmen.vue'),
        meta: { title: '匠心人物' }
      },
      {
        path: 'builder',
        name: 'BridgeBuilder',
        component: () => import('@/views/BridgeBuilder.vue'),
        meta: { title: '古桥建造坊' }
      },
      {
        path: 'compare',
        name: 'BridgeCompare',
        component: () => import('@/views/BridgeCompare.vue'),
        meta: { title: '桥梁对比' }
      },
      {
        path: 'quiz',
        name: 'BridgeQuiz',
        component: () => import('@/views/BridgeQuiz.vue'),
        meta: { title: '知识挑战' }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('@/views/Statistics.vue'),
        meta: { title: '数据统计' }
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('@/views/About.vue'),
        meta: { title: '关于项目' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 设置页面标题
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || '首页'} - 桥见千年`
  next()
})

export default router
