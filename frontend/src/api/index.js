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
    getProblemsRecommended: async() => {
      console.log("getProblemsRecommended");
      return await router.get(path.baseUrl + path.getProblemsRecommended);
    },
    getProblemById: async(pid) => {
      console.log("getProblemById");
      return await router.get(path.baseUrl + path.getProblemById,{params:{pid :pid }});
    },
    createProblemList: async(list) => {
      console.log("createProblemList: ", list);
      return await router.post(path.baseUrl + path.createProblemGroup,{},{params:{name :list.name,description:list.description }});
    },
    showJoinedGroups: async() => {
      return await router.get(path.baseUrl + path.showJoinedGroups);
    },
    leaveGroup:async(gid) => {
      return await router.post(path.baseUrl + path.leaveGroup, {}, {params: {gid: gid}});
    },
    showCreatedGroups: async() => {
      return await router.get(path.baseUrl + path.showCreatedGroups);
    },
    createGroup: async(group_name, description, password) => {
      return await router.post(path.baseUrl + path.createGroup, {group_name: group_name, description: description, password: password});
    },
    modifyGroup: async(gid, group_name, description, password) => {
      return await router.post(path.baseUrl + path.modifyGroup, {gid: gid, password: password, description: description, group_name: group_name});
    },
    showUnGroups: async() => {
      return await router.get(path.baseUrl + path.showUnGroups, {}, {params: {sub_name: ""}});
    },
    joinGroup: async(gid, password) => {
      return await router.post(path.baseUrl + path.joinGroup, {gid: gid, password: password});
    },
    createProblemGroup: async(group_name, description) => {
      console.log("createProblemGroup");
      return await router.post(path.baseUrl + path.createProblemGroup, {name: group_name, description: description});
    },
    change_problem_group_info: async(pgid, group_name, description) => {
      console.log("change_problem_group_info");
      return await router.post(path.baseUrl + path.change_problem_group_info, {pgid: pgid, name: group_name, description: description});
    },
    add_problem_to_group: async(pgid, pid) => {
      console.log("add_problem_to_group");
      return await router.post(path.baseUrl + path.add_problem_to_group, {pgid: pgid, pid: pid});
    },
    share_problem_group_to_user_group: async(pgid, gid) => {
      console.log("share_problem_group_to_user_group");
      return await router.post(path.baseUrl + path.share_problem_group_to_user_group, {pgid: pgid, gid: gid});
    },
    add_problem_tag: async(pid, tag) => {
      console.log("add_problem_tag");
      return await router.post(path.baseUrl + path.add_problem_tag, {pid: pid, tag: tag});
    },
    search_problem_by_tag: async(tag) => {
      console.log("search_problem_by_tag");
      return await router.get(path.baseUrl + path.search_problem_by_tag, {tag: tag});
    },
    get_my_problems: async() => {
      console.log("get_my_problems");
      return await router.get(path.baseUrl + path.get_my_problems);
    },
    submit_problem: async(pid, answer) => {
      console.log("submit_problem");
      return await router.post(path.baseUrl + path.submit_problem, {pid: pid, answer: answer});
    },
    get_user_statistics: async() => {
      console.log("get_user_statistics");
      return await router.get(path.baseUrl + path.get_user_statistics);
    },
    get_problem_recommend: async() => {
      console.log("get_problem_recommend");
      return await router.get(path.baseUrl + path.get_problem_recommend);
    },
    get_problem: async(pid) => {
      console.log("get_problem");
      return await router.get(path.baseUrl + path.get_problem, {pid: pid});
    },
    get_problem_group_info: async(pgid) => {
      console.log("get_problem_group_info");
      return await router.get(path.baseUrl + path.get_problem_group_info, {pgid: pgid});
    },
    get_problem_group_problems: async(pgid) => {
      console.log("get_problem_group_problems");
      return await router.get(path.baseUrl + path.get_problem_group_problems, {pgid: pgid});
    },
    get_problem_groups: async() => {
      console.log("get_problem_groups");
      return await router.get(path.baseUrl + path.get_problem_groups);
    },
};

export default api;