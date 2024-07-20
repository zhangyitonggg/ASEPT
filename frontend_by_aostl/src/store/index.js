import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api/index.js';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    _show_platform_frame_: true,
    _user_name_: null,
    _alert_: {
      show: false,
      message: "test",
      type: "success"
    },
    _token_: null,
    _app_title_: "Test",
  },
  getters: {
    username: state => state._user_name_ == null ? "UnauthorizedUser" : state._user_name_,
  },
  mutations: {
    checkToken(state) {
      if (!state._user_name_ || state._user_name_ === "UnauthorizedUser") {
        state._show_platform_frame_ = false;
      }
    },
    cancelAlert(state) {
      state._alert_.show = false;
    },
    showPlatformFrame(state) {
      state._show_platform_frame_ = true;
    },
    setAlert(state, alert) {
      state._alert_.message= alert.message;
      if (alert.type) {
        state._alert_.type = alert.type;
        state._alert_.show = true;
        setTimeout(() => {
          state._alert_.show = false;
        }, 3000);
      } else {
        state._alert_.show = false;
      }
    },
    getToken(state) {
      let token = localStorage.getItem('__token__');
      if (!token) {
        token = sessionStorage.getItem('__token__');
      } state._token_ = token;
    },
    getUserName(state) {
      let user_name = localStorage.getItem('__user_name__');
      if (!user_name) {
        user_name = sessionStorage.getItem('__user_name__');
      } state._user_name_ = user_name;
    },
    setAppTitle(state, title) {
      state._app_title_ = title;
    }
  },
  actions: {
    async login(context, { username, password, remember }) {
      if (!username || !password) {
        throw "用户名或密码不合法。";
      }
      try {
        await api.login(username, password)
          .then(response => {
            if (remember) {
              localStorage.setItem('__token__', response.data.access_token);
              localStorage.setItem('__user_name__', username);
            } else {
              sessionStorage.setItem('__token__', response.data.access_token);
              sessionStorage.setItem('__user_name__', username);
            }
          })
      } catch (error) {
        throw "用户名或密码错误。";
      }
    },
    getNews(context) {
      return new Promise((resolve, reject) => {
        api.getnews()
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    }
  },
  modules: {
  }
})
