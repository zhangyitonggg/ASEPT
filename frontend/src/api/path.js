const base = {
    baseUrl: 'http://localhost:8000',
    login: '/security/token',
    logon: '/create_user',
    userModify: '/user/modify',
    deleteGroup: '/user_group/delete_group',
    news_getannouncements: '/news/get_announcements?max_announcements=20',
    showJoinedGroups: '/user_group/show_joined_groups',
    leaveGroup: '/user_group/leave_group',
    showCreatedGroups: '/user_group/show_create_groups',
    createGroup: '/user_group/create_group',
    modifyGroup: '/user_group/modify_group',
    showUnGroups: '/user_group/show_unentered_groups',
    createProblem: '/problems/upload_problem',
    createProblemGroup: '/problems/create_problem_group',
    change_problem_group_info: '/problems/change_problem_group_info',
    add_problem_to_group: '/problems/add_problem_to_group',
    share_problem_group_to_user_group: '/problems/share_problem_group_to_user_group',
    add_problem_tag: '/problems/add_problem_tag',
    search_problem_by_tag: '/problems/search_problem_by_tag',
    get_my_problems: '/problems/get_my_problems',
    submit_problem: '/problems/submit_problem',
    get_user_statistics: '/user/get_user_statistics',
    get_problem_recommend: '/problems/get_problem_recommend',
    get_problem: '/problems/get_problem',
    joinGroup: '/user_group/join_group',
    getMyProblem: '/problems/my_problems',
    getProblemById: '/problems/get_problem',
    get_problem_group_info: '/problems/get_problem_group_info',
    get_problem_group_problems: '/problems/get_problem_group_problems',
    get_problem_groups: '/problems/accessible_problem_groups',
    getProblemsRecommended: '/problems/get_problem_recommend',
    get_my_problem_groups: '/problems/my_problem_groups',
    get_problem_ans_by_id: '/problems/get_problem_answer',
    uploadFile: '/problem_file_upload',
    getTime: '/news/current_time',
    get_all_problems: '/problems/get_all_problems',
    getProblemTags: '/problems/get_all_tags',
}

export default base;