import router from "../utils/network";
import path from "./path";

const api = {
    login: async(username, password) => {
        const response = await router.post(path.baseUrl + path.login, {
          username: username,
          password: password
        }, {
          useQs: true
        });
        return response;
    },
    getnews: async() => {
        const response = await router.get(path.baseUrl + path.news_getannouncements);
        return response;
    },
    register: async(username, password) => {
      return await router.post(path.baseUrl + path.logon, {}, {params: {username: username, password: password}});
    },
    showJoinedGroups: async() => {
      console.log("showJoinedGroups");
      return await router.get(path.baseUrl + path.showJoinedGroups);
    },
    leaveGroup:async(gid) => {
      return await router.post(path.baseUrl + path.leaveGroup, {}, {params: {gid: gid}});
    },
    showUnGroups: async() => {
      console.log("showUnGroups");
      return await router.get(path.baseUrl + path.showUnGroups);
    },
};

export default api;