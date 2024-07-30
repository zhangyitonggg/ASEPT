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
    deleteGroup: async(gid) => {
      return await router.delete(path.baseUrl + path.deleteGroup,{params: {gid: gid}});
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
      console.log('create: ',problemData);
      return await router.post(path.baseUrl + path.createProblem,problemData);
    },
    updateproblem: async(problemData) => {
      console.log("updateProblem");
      console.log('update: ',problemData.problem);
      console.log('pid:', problemData.pid);
      return await router.post(path.baseUrl + path.updateproblem,problemData.problem,{params:{pid: problemData.pid}});
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
    add_problem_to_group: async(ppgid, ppid) => {
      console.log("add_problem_to_group");
      return await router.post(path.baseUrl + path.add_problem_to_group,{},{ params: {pid: ppid,pgid: ppgid}});
    },
    share_problem_group_to_user_group: async(pgid, gid) => {
      console.log(pgid,gid);
      return await router.post(path.baseUrl + path.share_problem_group_to_user_group,{}, {params: {pgid: pgid, gid: gid}});
    },
    add_problem_tag: async(pid, tag) => {
      console.log("add_problem_tag");
      return await router.post(path.baseUrl + path.add_problem_tag,{}, {params: {pid: pid, tag_name: tag}});
    },
    search_problem_by_tag: async(data) => {
      let param = {};
      if(data.tag && data.keyword) param = {tid: data.tag, key:data.keyword};
      else if(data.tag) param = {tid: data.tag};
      else if(data.keyword) param = {key:data.keyword};
      return await router.get(path.baseUrl + path.search_problem_by_tag, {params: param});
    },
    get_my_problems: async() => {
      return await router.get(path.baseUrl + path.get_my_problems);
    },
    getAllProblems: async() => {
      return await router.get(path.baseUrl + path.get_all_problems);
    },
    submit_problem: async(pid, answer) => {
      console.log('sub: ',pid,answer);
      return await router.get(path.baseUrl + path.submit_problem,{params: {pid: pid, answer: answer}});
    },
    get_user_statistics: async() => {
      return await router.get(path.baseUrl + path.get_user_statistics);
    },
    get_problem_recommend: async() => {
      console.log("get_problem_recommend");
      return await router.get(path.baseUrl + path.get_problem_recommend);
    },
    get_problem: async(pid) => {
      console.log("get_problem");
      console.log(pid);
      return await router.get(path.baseUrl + path.get_problem, {params:{pid: pid}});
    },
    get_problem_group_info: async(pgid) => {
      console.log("get_problem_group_info");
      return await router.get(path.baseUrl + path.get_problem_group_info, {pgid: pgid});
    },
    get_problem_group_problems: async(pgid) => {
      console.log("get_problem_group_problems");
      return await router.get(path.baseUrl + path.get_problem_group_problems, {params: {pgid: pgid}});
    },
    get_problem_groups: async() => {
      console.log("get_problem_groups");
      return await router.get(path.baseUrl + path.get_problem_groups);
    },
    get_my_problem_groups: async() => {
      console.log("get_my_problem_groups");
      return await router.get(path.baseUrl + path.get_my_problem_groups);
    },
    getProblemAnsById:async(pid) => {
      console.log("get_problem_ans_by_id");
      return await router.get(path.baseUrl + path.get_problem_ans_by_id,{params: {pid:pid}});
    },
    userModify: async(username, originalPassword, newPassword) => {
      return await router.post(path.baseUrl + path.userModify, {originalPassword: originalPassword, newPassword: newPassword});
    },
    uploadFile: async(file) => {
      const formData = new FormData();
      formData.append('file', file);
      return await router.post(path.baseUrl + path.uploadFile, formData, {useMultipart: true});
    },
    getTime: async() => {
      return await router.get(path.baseUrl + path.getTime);
    },
    getProblemTag:  async() => {
      return await router.get(path.baseUrl + path.getProblemTags);
    },
    submitFeedback: async(name, email, advice, complaint) => {
      return await router.post(path.baseUrl + path.submitFeedback, {name: name, email: email, advice: advice, complaint: complaint});
    }
};

export default api;