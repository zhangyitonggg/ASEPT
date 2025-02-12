const base = {
  baseUrl: 'https://api.asept.aostl.ink',
  login: '/security/admin',
  logon: '/create_user',
  userModify: '/user/modify',
  deleteGroup: '/user_group/delete_group',
  news_getannouncements: '/news/get_all_announcements?max_announcements=20',
  get_feedbacks: '/admin/get_feedbacks',
  showJoinedGroups: '/user_group/show_joined_groups',
  leaveGroup: '/user_group/leave_group',
  showAllGroups: '/admin/get_all_groups',
  createGroup: '/user_group/create_group',
  modifyGroup: '/user_group/modify_group',
  showUnGroups: '/user_group/show_unentered_groups',
  createProblem: '/problems/upload_problem',
  createProblemGroup: '/problems/create_problem_group',
  change_problem_group_info: '/problems/change_problem_group_info',
  add_problem_to_group: '/problems/add_problem_to_group',
  getProblemTags: '/problems/get_all_tags',
  share_problem_group_to_user_group: '/problems/share_problem_group_to_user_group',
  add_problem_tag: '/problems/add_tag_to_problem',
  search_problem_by_tag: '/problems/search_problem_by_tag',
  get_my_problems: '/problems/get_my_problems',
  submit_problem: '/problems/submit_problem',
  get_user_statistics: '/problems/get_user_statistics',
  get_problem_recommend: '/problems/get_problem_recommend',
  get_problem: '/problems/get_problem',
  joinGroup: '/user_group/join_group',
  getAllProblem: '/admin/get_all_problems',
  getProblemById: '/problems/get_problem',
  get_problem_group_info: '/problems/get_problem_group_info',
  get_problem_group_problems: '/problems/get_problem_group_problems',
  get_problem_groups: '/problems/accessible_problem_groups',
  getProblemsRecommended: '/problems/get_problem_recommend',
  get_all_problem_groups: '/admin/get_all_problem_groups',
  showAllUsers: '/admin/get_all_users',
  setPermission: '/admin/set_permission',
  publishAnnouncement: '/admin/open_announcement',
  modifyAnnouncement: '/admin/modify_announcement',
  getTime: '/news/current_time',
}

export default base;