import VueRouter from "vue-router";

import Login from '../views/login/Login'
import Register from "../views/login/Register";
import Home from "../views/home/Home";


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
        }
    ]
})