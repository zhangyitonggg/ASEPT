import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

const actions = {
    storeUname(context, uname) {
        context.commit('storeUname', uname)
    },
    storeToken(context, token) {
        context.commit('storeToken', token)
    }
}

const mutations = {
    storeUname(state, uname) {
        state.uname = uname
    },
    storeToken(state, token) {
        state.token = token
    }
}

const state = {
    uname: '',
    token: '',
    ulevel:0,
    uquestionNum:0,
}

export default new Vuex.Store({
    actions,
    mutations,
    state,
})