import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import store from '../store'
import NotFound from '../views/NotFound.vue'
import PersonalCenter from '../views/PersonalCenter.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      requiresAuth: true,
      title: '首页'
    }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
    meta: {
      requiresAuth: false,
      title: '关于'
    }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginPanel.vue'),
    meta: {
      requiresNotAuthed: true,
      title: '登录'
    }
  },
  {
    path: '/groups',
    name: 'groups',
    component: () => import('../views/GroupView.vue')
  },
  { 
    path: '/exercises',
    name: 'exercises',
    component: HomeView // todo
  },
  {
    path: '/me',
    name: 'me',
    component: PersonalCenter // todo
  },
  {
    path: '*',
    name: 'NotFound',
    component: NotFound,
    meta: {
      title: '404 Not Found',
      requiresAuth: false
    }
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

router.beforeEach((to, from, next) => {
  store.commit("getUserName");
  store.commit("getToken");
  const name = store.state._user_name_;
  const token = store.state._token_;
  const default_title = ' - ASEPT';
  const title = to.meta == null ? " " : to.meta.title;
  if (name == null || token == null) {
    localStorage.removeItem('__token__');
    localStorage.removeItem('__user_name__');
    sessionStorage.removeItem('__token__');
    sessionStorage.removeItem('__user_name__');
    if (to.matched.some(record => record.meta.requiresAuth)) {
        next({ name: 'login' });
    } else {
      document.title =  title + default_title;
      next();
    }
  } else {
    store.commit("showPlatformFrame");
    if (to.matched.some(record => record.meta.requiresNotAuthed)) {
      next({ name: 'home' });
    } else {
      document.title =  title + default_title;
      next();
    }
  }
});

export default router
