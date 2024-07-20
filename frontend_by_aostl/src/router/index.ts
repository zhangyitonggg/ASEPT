import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import store from '../store'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {requiresAuth: true}
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginPanel.vue'),
    meta: {requiresNotAuthed: true}
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
    path: '/mine',
    name: 'mine',
    component: HomeView // todo
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
  if (name == null || token == null) {
    localStorage.removeItem('__token__');
    localStorage.removeItem('__user_name__');
    sessionStorage.removeItem('__token__');
    sessionStorage.removeItem('__user_name__');
    if (to.matched.some(record => record.meta.requiresAuth)) {
        next({ name: 'login' });
    } else {
      next();
    }
  } else {
    store.commit("showPlatformFrame");
    if (to.matched.some(record => record.meta.requiresNotAuthed)) {
      next({ name: 'home' });
    } else {
      next();
    }
  }
});

export default router
