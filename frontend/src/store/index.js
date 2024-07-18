import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

const actions = {
    storeUname(context, uname) {
        console.log('invue');
        context.commit('storeUname', uname)
    },
    storeToken(context, token) {
        context.commit('storeToken', token)
    }
}

const mutations = {
    storeUname(state, uname) {
        state.uname = uname
        localStorage.setItem('uname', uname);
    },
    storeToken(state, token) {
        state.token = token
        localStorage.setItem('token', token);
    }
}

const state = {
    uname: localStorage.getItem('uname') || 'noname',
    token: localStorage.getItem('token') || '',
    ulevel:parseInt(localStorage.getItem('ulevel')) || 0,
    uquestionNum:parseInt(localStorage.getItem('uquestionNum')) || 0,
}

export default new Vuex.Store({
    actions,
    mutations,
    state,
})