import VueRouter from "vue-router";

import Login from '../views/login/Login'
import Register from "../views/login/Register";
import Home from "../views/home/Home";
import Mine from "../mine/Mine.vue";
import Group from "../views/group/Group.vue";

export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login',
            component: Login
        },
        {
            path: '/register',
            component: Register
        },
        {
            path: '/home',
            component: Home
        },
        {
            path: '/mine',
            component: Mine
        },
        {
            path: '/Groups',
            component: Group
        }
    ]
})