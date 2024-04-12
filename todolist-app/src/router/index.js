import { createRouter, createWebHistory } from 'vue-router'
const routes = [
  {
    path: '/',
    name: 'todologin',
    component: () => import ('../views/todoList/LoginView.vue'),
    props: true,
    meta: { requiresAuth: false ,title: 'todo list' },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import ('../views/member/RegisterView.vue'),
    props: true,
    meta: { title: 'register' }
  },
  {
    path: '/update',
    name: 'update',
    component: () => import ('../views/member/RegisterView.vue'),
    props: true,
    meta: { requiresAuth: true ,title: 'udate' },
    // component: MemberUpdateView
  },
  
  {
    path: '/todolist',
    name: 'todolist',
    component: () => import ('../views/todoList/TodoListView.vue'),
    props: true,
    meta: { requiresAuth: true ,title: 'todo list' },
  },
  {
    path: '/todologin',
    name: 'todologin',
    component: () => import ('../views/todoList/LoginView.vue'),
    props: true,
    meta: { requiresAuth: false ,title: 'todo list' },
  },
  {
    path: '/todologin',
    name: 'login',
    component: () => import ('../views/todoList/LoginView.vue'),
    props: true,
    meta: { requiresAuth: false ,title: 'todo list' },
  },
  
  { path: '/:pathMatch(.*)*',
  component: () => import('../views/PageNotFound.vue')
  },
]
 /* eslint-disable */ 
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior (to, from, savedPosition) {
    return { top: 0 }
  }
})
import store from "../store";
router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title || 'todolst';
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isLoggedIn = store.state.session.userId !== null;
  if (requiresAuth && !isLoggedIn) {
    next("todologin");
  } else {
    next();
  }
});

export default router
