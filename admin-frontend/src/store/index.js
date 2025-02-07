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
    _problem_id_: 0,
    particles: true,
  },
  getters: {
    username: state => state._user_name_ == null ? "UnauthorizedUser" : state._user_name_,
    problemid: state => state._problem_id_,
    particles: state => state.particles,
  },
  mutations: {
    checkToken(state) {
      if (!state._user_name_ || state._user_name_ === "UnauthorizedUser") {
        state._show_platform_frame_ = false;
      }
    },
    setParticles(state, payload) {
      state.particles = payload;
    },
    cancelAlert(state) {
      state._alert_.show = false;
    },
    showPlatformFrame(state) {
      state._show_platform_frame_ = true;
    },
    hidePlatformFrame(state) {
      state._show_platform_frame_ = false;
    },
    setAlert(state, alert) {
      state._alert_.message = alert.message;
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
    },
    setProblemid(state, id) {
      state._problem_id_ = id;
    },
    clearPersonalInfo(state) {
      state._user_name_ = null;
      state._token_ = null;
      localStorage.removeItem('__token__');
      localStorage.removeItem('__user_name__');
      sessionStorage.removeItem('__token__');
      sessionStorage.removeItem('__user_name__');
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
    updateParticles({ commit }, payload) {
      commit('setParticles', payload);
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
    },
    getFeedbacks(context) {
      return new Promise((resolve, reject) => {
        api.getFeedbacks()
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    register(context, { username, password }) {
      return new Promise((resolve, reject) => {
        api.register(username, password)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    createProblem(context, problemData) {
      return new Promise((resolve, reject) => {
        api.createProblem(problemData)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    getMyProblem(context) {
      return new Promise((resolve, reject) => {
        api.getAllProblem()
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    getProblemsRecommended(context) {
      return new Promise((resolve, reject) => {
        api.getProblemsRecommended()
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    getProblemById(context, pid) {
      return new Promise((resolve, reject) => {
        api.getProblemById(pid)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    getCorrectAnswersById(context, pid) {
      return new Promise((resolve, reject) => {
        api.getProblemById(pid)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    addProblemToList(context, data) {
      return new Promise((resolve, reject) => {
        api.add_problem_to_group(data.pgid, data.pid)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    createProblemList(context, list) {
      return new Promise((resolve, reject) => {
        api.createProblemList(list)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    getProblemTags(context) {
      return new Promise((resolve, reject) => {
        api.getProblemTag()
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    getProblemGroup(context) {
      return new Promise((resolve, reject) => {
        api.get_problem_groups()
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    getMyProblemGroup(context) {
      return new Promise((resolve, reject) => {
        api.get_all_problem_groups()
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    getProblemsInList(context, pgid) {
      return new Promise((resolve, reject) => {
        api.get_problem_group_problems(pgid.pgid)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    shareProblemList(context, data) {
      return new Promise((resolve, reject) => {
        api.share_problem_group_to_user_group(data.pgid, data.gid)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    searchProblemByTag(context, tag) {
      return new Promise((resolve, reject) => {
        api.search_problem_by_tag(tag)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    addTagToProblem(context, data) {
      return new Promise((resolve, reject) => {
        api.add_problem_tag(data.pid, data.tag)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    submitAnswer(context, data) {
      return new Promise((resolve, reject) => {
        api.submit_problem(data.pid, data.answer)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    deleteGroup(context, { gid }) {
      return new Promise((resolve, reject) => {
        api.deleteGroup(gid)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    leaveGroup(context, { gid }) {
      return new Promise((resolve, reject) => {
        api.leaveGroup(gid)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    showJoinedGroups(context) {                               // new
      return new Promise((resolve, reject) => {
        api.showAllGroups()
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    showAllUsers(context) {                               // new
      return new Promise((resolve, reject) => {
        api.showAllUsers()
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    setPermission(context, { username, permission, cancel }) {
      return new Promise((resolve, reject) => {
        api.setPermission(username, permission, cancel)
          .then(response => {
            resolve(response.data);
          })
          .catch(e => {
            reject(e);
          })
      })
    },
    createGroup(context, { group_name, description, password }) {
      return new Promise((resolve, reject) => {
        api.createGroup(group_name, description, password)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    modifyGroup(context, { gid, group_name, description, password }) {
      return new Promise((resolve, reject) => {
        api.modifyGroup(gid, group_name, description, password)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    showUnGroups(context) {
      return new Promise((resolve, reject) => {
        api.showUnGroups()
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    joinGroup(context, { gid, password }) {
      return new Promise((resolve, reject) => {
        api.joinGroup(gid, password)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    userModify(context, { username, originalPassword, newPassword }) {
      return new Promise((resolve, reject) => {
        api.userModify(username, originalPassword, newPassword)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    publishAnnouncement(context, { title, content }) {
      return new Promise((resolve, reject) => {
        api.publishAnnouncement(title, content)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    modifyAnnouncement(context, { aid, title, content, is_active }) {
      return new Promise((resolve, reject) => {
        api.modifyAnnouncement(aid, title, content, is_active)
          .then(response => {
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
  },
  modules: {
  }
})
