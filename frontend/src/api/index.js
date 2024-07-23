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
    createProblem: async(problemData) => {
      console.log("createProblem");
        return await router.post(path.baseUrl + path.createProblem,problemData);
    },
    getMyProblem: async() => {
      console.log("getMyProblem");
        return await router.get(path.baseUrl + path.getMyProblem);
    },
    showJoinedGroups: async() => {
      console.log("showJoinedGroups");
      return await router.get(path.baseUrl + path.showJoinedGroups);
    },
    leaveGroup:async(gid) => {
      console.log("leaveGroup");
      return await router.post(path.baseUrl + path.leaveGroup, {}, {params: {gid: gid}});
    },
    showCreatedGroups: async() => {
      console.log("showCreatedGroups");
      return await router.get(path.baseUrl + path.showCreatedGroups);
    },
    createGroup: async(group_name, description, password) => {
      console.log("createGroup");
      return await router.post(path.baseUrl + path.createGroup, {group_name: group_name, description: description, password: password});
    },
    modifyGroup: async(gid, group_name, description, password) => {
      console.log("modifyGroup");
      return await router.post(path.baseUrl + path.modifyGroup, {gid: gid, password: password, description: description, group_name: group_name});
    },
    showUnGroups: async() => {
      console.log("showUnGroups");
      return await router.get(path.baseUrl + path.showUnGroups);
    },
    joinGroup: async(gid, password) => {
      console.log("joinGroup");
      return await router.post(path.baseUrl + path.joinGroup, {gid: gid, password: password});
    }
};

export default api;