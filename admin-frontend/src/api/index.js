import router from "../utils/network";
import path from "./path";

const api = {
  login: async (username, password) => {
    const response = await router.post(path.baseUrl + path.login, {
      username: username,
      password: password
    }, {
      useQs: true
    });
    return response;
  },
  getnews: async () => {
    const response = await router.get(path.baseUrl + path.news_getannouncements);
    return response;
  },
  getFeedbacks: async () => {
    const response = await router.get(path.baseUrl + path.get_feedbacks);
    return response;
  },
  getProblemTag:  async() => {
    return await router.get(path.baseUrl + path.getProblemTags);
  },
  register: async (username, password) => {
    return await router.post(path.baseUrl + path.logon, {}, { params: { username: username, password: password } });
  },
  deleteGroup: async (gid) => {
    return await router.delete(path.baseUrl + path.deleteGroup, { params: { gid: gid } });
  },
  createProblem: async (problemData) => {
    return await router.post(path.baseUrl + path.createProblem, problemData);
  },
  getAllProblem: async () => {
    return await router.get(path.baseUrl + path.getAllProblem);
  },
  getProblemsRecommended: async () => {
    return await router.get(path.baseUrl + path.getProblemsRecommended);
  },
  getProblemById: async (pid) => {
    return await router.get(path.baseUrl + path.getProblemById, { params: { pid: pid } });
  },
  createProblemList: async (list) => {
    return await router.post(path.baseUrl + path.createProblemGroup, {}, { params: { name: list.name, description: list.description } });
  },
  showJoinedGroups: async () => {
    return await router.get(path.baseUrl + path.showJoinedGroups);
  },
  leaveGroup: async (gid) => {
    return await router.post(path.baseUrl + path.leaveGroup, {}, { params: { gid: gid } });
  },
  showAllGroups: async () => {
    return await router.get(path.baseUrl + path.showAllGroups);
  },
  createGroup: async (group_name, description, password) => {
    return await router.post(path.baseUrl + path.createGroup, { group_name: group_name, description: description, password: password });
  },
  modifyGroup: async (gid, group_name, description, password) => {
    return await router.post(path.baseUrl + path.modifyGroup, { gid: gid, password: password, description: description, group_name: group_name });
  },
  showUnGroups: async () => {
    return await router.get(path.baseUrl + path.showUnGroups, {}, { params: { sub_name: "" } });
  },
  joinGroup: async (gid, password) => {
    return await router.post(path.baseUrl + path.joinGroup, { gid: gid, password: password });
  },
  publishAnnouncement: async (title, content) => {
    return await router.post(path.baseUrl + path.publishAnnouncement, {
      title: title,
      content: content
    });
  },
  modifyAnnouncement: async (aid, title, content, is_active) => {
    return await router.post(path.baseUrl + path.modifyAnnouncement, {
      aid: aid,
      title: title,
      content: content,
      is_active: is_active,
    });
  },
  createProblemGroup: async (group_name, description) => {
    return await router.post(path.baseUrl + path.createProblemGroup, { name: group_name, description: description });
  },
  change_problem_group_info: async (pgid, group_name, description) => {
    return await router.post(path.baseUrl + path.change_problem_group_info, { pgid: pgid, name: group_name, description: description });
  },
  add_problem_to_group: async (ppgid, ppid) => {
    return await router.post(path.baseUrl + path.add_problem_to_group, {}, { params: { pid: ppid, pgid: ppgid } });
  },
  share_problem_group_to_user_group: async (pgid, gid) => {
    return await router.post(path.baseUrl + path.share_problem_group_to_user_group, {}, { params: { pgid: pgid, gid: gid } });
  },
  add_problem_tag: async (pid, tag) => {
    return await router.post(path.baseUrl + path.add_problem_tag, {}, { params: { pid: pid, tag_name: tag } });
  },
  search_problem_by_tag: async (tag) => {
    return await router.get(path.baseUrl + path.search_problem_by_tag, { params: { tag: tag } });
  },
  get_my_problems: async () => {
    return await router.get(path.baseUrl + path.get_my_problems);
  },
  submit_problem: async (pid, answer) => {
    return await router.get(path.baseUrl + path.submit_problem, { params: { pid: pid, answer: answer } });
  },
  get_user_statistics: async () => {
    return await router.get(path.baseUrl + path.get_user_statistics);
  },
  get_problem_recommend: async () => {
    return await router.get(path.baseUrl + path.get_problem_recommend);
  },
  get_problem: async (pid) => {
    return await router.get(path.baseUrl + path.get_problem, { params: { pid: pid } });
  },
  get_problem_group_info: async (pgid) => {
    return await router.get(path.baseUrl + path.get_problem_group_info, { pgid: pgid });
  },
  get_problem_group_problems: async (pgid) => {
    return await router.get(path.baseUrl + path.get_problem_group_problems, { params: { pgid: pgid } });
  },
  get_problem_groups: async () => {
    return await router.get(path.baseUrl + path.get_problem_groups);
  },
  get_all_problem_groups: async () => {
    return await router.get(path.baseUrl + path.get_all_problem_groups);
  },
  userModify: async (username, originalPassword, newPassword) => {
    return await router.post(path.baseUrl + path.userModify, { originalPassword: originalPassword, newPassword: newPassword });
  },
  showAllUsers: async () => {
    return await router.get(path.baseUrl + path.showAllUsers);
  },
  setPermission: async (username, permission, cancel) => {
    return await router.post(path.baseUrl + path.setPermission, { target_user_name: username, permission: permission, cancel: cancel });
  },
  getTime: async() => {
    return await router.get(path.baseUrl + path.getTime);
  },
};

export default api;